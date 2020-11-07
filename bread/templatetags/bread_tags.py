import logging
import re
import warnings
from _strptime import TimeRE

from bread import menu as menuregister
from crispy_forms.utils import get_template_pack
from django import template
from django.contrib.staticfiles import finders
from django.core.cache import cache
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from django.forms import DateInput, Textarea, TextInput
from django.forms.utils import flatatt
from django.utils import formats
from django.utils.html import mark_safe

import plisplate

from ..formatters import as_object_link, format_value
from ..formatters import render_field as render_field_func
from ..formatters import render_field_aggregation as render_field_aggregation_func
from ..forms import forms
from ..utils import has_permission, pretty_fieldname, title
from ..utils.datetimeformatstring import to_php_formatstr

logger = logging.getLogger(__name__)
register = template.Library()

register.simple_tag(pretty_fieldname)
register.simple_tag(has_permission)
register.simple_tag(to_php_formatstr)
register.filter(format_value)


# tags


@register.simple_tag
def dateformatstr2regex(formatstr, format_key):
    formatstr = formatstr or formats.get_format(format_key)[0]
    # check: are local formats handled correctly?
    return TimeRE().compile(formatstr).pattern


@register.simple_tag
def linkpermission(link, request, obj=None):
    return link.has_permission(request, obj)


@register.simple_tag(takes_context=True)
def linkurl(context, link):
    return link.url(context["request"])


@register.simple_tag(takes_context=True)
def render_plisplate(context, element):
    return mark_safe(plisplate.render(element, context.flatten()))


@register.simple_tag
def display_link(link, request, obj=None, atag_class="", atag_style=""):
    warnings.warn(
        "the template tag display_link is deprecated, please use the tags linkpermission and linkurl"
    )

    ret = ""
    if link.has_permission(request, obj):
        url = link.url(request)
        target = (
            'target="_blank" rel="noopener noreferrer"'
            if url.startswith("http")
            else ""
        )
        ret += f'<a href="{url}" class="{atag_class}" style="{atag_style}" {target}>'
        if link.icon is not None:
            ret += f'<i class="material-icons" style="vertical-align:middle">{link.icon}</i> '
        if link.label is not None:
            ret += link.label
        ret += "</a>"
    return mark_safe(ret)


@register.simple_tag
def has_link_permission(link, request, obj=None):
    return link.has_permission(request, obj)


@register.simple_tag
def pretty_modelname(model, plural=False):
    if plural:
        return title(model._meta.verbose_name_plural)
    return title(model._meta.verbose_name)


@register.simple_tag
def modelname(model):
    return model._meta.model_name


@register.simple_tag
def adminurl(model, urlname, *args, **kwargs):
    from ..admin import site

    return site.get_default_admin(model).reverse(urlname, *args, **kwargs)


@register.simple_tag
def object_actions(admin, request, object):
    return admin.object_actions(request, object)


@register.simple_tag
def list_actions(admin, request):
    return admin.list_actions(request)


@register.simple_tag
def add_action(admin, request):
    return admin.add_action(request)


@register.simple_tag
def pagename(request):
    return " / ".join(
        [
            title(namespace.replace("_", " "))
            for namespace in request.resolver_match.namespaces
        ]
    )


@register.simple_tag(takes_context=True)
def render_field(context, instance, fieldname):
    admin = getattr(context.get("view"), "admin", None)
    if admin is None:
        from ..admin import site

        admin = site.get_default_admin(instance._meta.model)
    return render_field_func(instance, fieldname, admin)


@register.simple_tag(takes_context=True)
def object_link(context, instance, label=None):
    return as_object_link(instance, label)


@register.simple_tag(takes_context=True)
def render_field_aggregation(context, instance, fieldname):
    admin = getattr(context.get("view"), "admin", None)
    if admin is None:
        from ..admin import site

        admin = site.get_default_admin(instance._meta.model)
    return render_field_aggregation_func(instance, fieldname, admin)


@register.simple_tag
def querystring_order(current_order, fieldname):
    """Return order fields according to the current GET-parameters but change the order-parameter of the given field"""
    fieldname_rev = "-" + fieldname
    ordering = current_order.split(",")
    if fieldname in ordering:
        ordering.remove(fieldname)
        ordering.insert(0, fieldname_rev)
    elif fieldname_rev in ordering:
        ordering.remove(fieldname_rev)
    else:
        ordering.insert(0, fieldname)
    return ",".join(filter(None, ordering))


@register.simple_tag(takes_context=True)
def updated_querystring(context, key, value):
    """Take the current GET query and update/add an entry"""
    current_query = context["request"].GET.copy()
    current_query[key] = value
    return context["request"].path + "?" + current_query.urlencode()


@register.simple_tag(takes_context=True)
def crispy_html(context, layout):
    return mark_safe(layout.render({}, (), context, template_pack=get_template_pack()))


# filters


@register.filter
def is_external_url(url):
    """Return ``True`` if the url is linked to an external page"""
    return url.startswith("http")


@register.filter
def is_inline_formset(field):
    return isinstance(field.field, forms.FormsetField)


@register.filter
def is_textinput(field):
    return isinstance(field.field.widget, TextInput)


@register.filter
def is_textarea(field):
    return isinstance(field.field.widget, Textarea)


@register.filter
def is_dateinput(field):
    return isinstance(field.field.widget, DateInput)


@register.simple_tag
def menu(request):
    """
    returns nested iterables:
    [
        [group, active, (
            (item, active, url),
            (item, active, url),
        )],
        [group, active, (
            (item, active, url),
            (item, active, url),
        )]
    ]
    If no menu group is active will try to find active menu by comparing labels to current appname
    """
    menugroups = []
    has_active_menu = False
    for group in sorted(menuregister.main._registry.values()):
        if group.has_permission(request):
            has_active_menu = has_active_menu or group.active(request)
            menugroups.append(
                [
                    group.label,
                    group.icon,
                    group.active(request),
                    (
                        (item, item.active(request), item.link.url(request))
                        for item in sorted(group.items)
                        if item.has_permission(request)
                    ),
                ]
            )
    if not has_active_menu:
        for group in menugroups:
            if menuregister.main._registry[group[0]].active_in_current_app(request):
                group[1] = True
                break
    return menugroups


# TODO: check recursively?
@register.simple_tag
def list_delete_cascade(object):
    ret = []
    for field in object._meta.get_fields():
        if (
            hasattr(field, "on_delete")
            and field.on_delete == models.CASCADE
            and hasattr(object, field.get_accessor_name())
        ):
            related_objects = getattr(object, field.get_accessor_name())
            # hack so that we can always work with querysets
            if isinstance(related_objects, models.Model):
                ret.append(
                    related_objects._meta.model.objects.filter(id=related_objects.id)
                )
            elif related_objects.exists():
                ret.append(related_objects.all())
    return ret


# TODO: check recursively?
@register.simple_tag
def list_delete_protection(object):
    ret = []
    for field in object._meta.get_fields():
        if (
            hasattr(field, "on_delete")
            and field.on_delete == models.PROTECT
            and hasattr(object, field.get_accessor_name())
        ):
            related_objects = getattr(object, field.get_accessor_name())
            # hack so that we can always work with querysets
            if isinstance(related_objects, models.Model):
                ret.append(
                    related_objects._meta.model.objects.filter(id=related_objects.id)
                )
            elif related_objects.exists():
                ret.append(related_objects.all())
    return ret


@register.simple_tag
def carbon_icon(name, size, **kwargs):
    """Insert the SVG for a carvon icon.
    See https://www.carbondesignsystem.com/guidelines/icons/library for a list of all icons.
    In order to see the name which should be passed to this template tag, click on "Download SVG" for an
    icon and use the filename without the attribte, e.g. "thunderstorm--severe"."""
    kwargs["width"] = size
    kwargs["height"] = size
    name = "--".join(_camel_case_split(name))
    flatattribs = flatatt(
        {k.replace("_", "-"): v for k, v in kwargs.items()}
    )  # replace is because of hbs to django template transpilation
    key = (
        f"icon_{name}__{size}__{flatattribs}".lower().replace('"', "").replace(" ", "_")
    )
    if cache.get(key) is None:
        path = finders.find(f"design/carbon_design/icons/32/{name.lower()}.svg")
        if not path:
            logger.error(f"Missing icon: {name.lower()}.svg")
            return f"Missing icon {name.lower()}.svg"
        with open(path) as f:
            svg = "".join(
                [line.replace("<svg", f"<svg {flatattribs}") for line in f.readlines()]
            )
        cache.set(key, svg)
        return mark_safe(svg)
    return mark_safe(cache.get(key))


def _camel_case_split(identifier):
    matches = re.finditer(
        ".+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)", identifier
    )
    return [m.group(0) for m in matches]


# The select element is a bit tricky to implement in a custom way because the options are
# only attached in the widgets context and are not easily available in the template.
# That means we leverage the default django rendering mechanism for the select but modify
# the widget to have all necessary classes
@register.filter
def make_select(field):
    """Used to add carbon classes to a select input"""
    field.field.widget.attrs["class"] = (
        field.field.widget.attrs.get("class", "") + " bx--select-input"
    )
    field.field.widget.template_name = "carbon_design/widgets/select.html"
    return field


@register.filter
def make_option(widget):
    """Used to add carbon classes to a select input"""
    widget["attrs"]["class"] = widget["attrs"].get("class", "") + " bx--select-option"
    return widget


@register.filter
def getplaceholder(field):
    if hasattr(field.field.widget, "placeholder"):
        return field.field.widget.placeholder
    if hasattr(field.field, "placeholder"):
        return field.field.placeholder
    if hasattr(field.form, "_meta"):
        try:
            return getattr(
                field.form._meta.model._meta.get_field(field.name), "placeholder", ""
            )
        except FieldDoesNotExist:
            return ""
    return ""
