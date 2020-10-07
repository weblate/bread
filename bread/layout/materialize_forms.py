from crispy_forms.bootstrap import Container, ContainerHolder
from crispy_forms.layout import HTML, Layout
from crispy_forms.utils import TEMPLATE_PACK, render_field
from django.core.exceptions import ImproperlyConfigured
from django.forms.formsets import DELETION_FIELD_NAME
from django.template import Template
from django.template.loader import render_to_string

from ..templatetags.bread_tags import querystring_order, updated_querystring
from .base import (
    TABLE,
    TBODY,
    THEAD,
    TR,
    A,
    Div,
    FieldLabel,
    FieldValue,
    HTMLTag,
    ItemContainer,
    NonFormField,
    get_fieldnames,
    with_str_fields_replaced,
)


class Collapsible(Container):
    template = "%s/collapsible.html"


class CollapsibleGroup(ContainerHolder):
    template = "%s/collapsible-group.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        content = []
        self.open_target_group_for_form(form)

        for group in self.fields:
            group.data_parent = self.css_id
            content.append(
                render_field(
                    group,
                    form,
                    form_style,
                    context,
                    template_pack=template_pack,
                    **kwargs,
                )
            )

        template = self.get_template_name(template_pack)
        context.update({"collapsible": self, "content": "\n".join(content)})

        return render_to_string(template, context.flatten())


class Tab(Container):
    css_class = "tab"
    link_template = "%s/tab.html"

    def render_link(self, template_pack=TEMPLATE_PACK, **kwargs):
        return render_to_string(self.link_template % template_pack, {"tab": self})


class Tabs(ContainerHolder):
    template = "%s/tabs.html"

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        if form:
            for tab in self.fields:
                tab.errors = False

            for tab in self.fields:
                tab.errors = any(e in tab for e in form.errors.keys())

            self.open_target_group_for_form(form)
        links = "".join(tab.render_link(template_pack) for tab in self.fields)
        content = self.get_rendered_fields(form, form_style, context, template_pack)

        context.update({"tabs": self, "links": links, "content": content})
        template = self.get_template_name(template_pack)
        return render_to_string(template, context.flatten())


class Row(HTMLTag):
    @classmethod
    def with_columns(cls, *args):
        return Row(*[Col(width, field) for field, width in args])

    def __init__(self, *args, **kwargs):
        kwargs["css_class"] = kwargs.get("css_class", "") + " row"
        super().__init__(*args, **kwargs)


class Col(HTMLTag):
    def __init__(self, width=1, *args, **kwargs):
        kwargs["css_class"] = kwargs.get("css_class", "") + f" col s{width}"
        if not 1 <= width <= 12:
            raise ImproperlyConfigured("width must be a number between 1 and 12")
        super().__init__(*args, **kwargs)


class ObjectActions(NonFormField):
    def __init__(self, slice_start=None, slice_end=None, **kwargs):
        super().__init__(**kwargs)
        self.slice_start = slice_start
        self.slice_end = slice_end
        self.field = ""

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        if "object" in context:
            t = Template(
                f"""{{% load bread_tags %}}
    {{% object_actions view.admin request object as allactions %}}
    {{% for action in allactions|slice:"{self.slice_start}:{self.slice_end}" %}}
    <a href="{{% linkurl action %}}" class="btn-small">{{{{ action.label }}}}</a>
    {{% endfor %}}"""
            )
            return t.render(context)
        return ""


class ObjectActionsDropDown(HTMLTag):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = ""
        self.fields = []

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        return render_to_string(
            "materialize_forms/object_actions.html", context.flatten()
        )


class InlineLayout(Layout):
    """Used to render inline forms"""

    def __init__(self, inlinefield, *args, **kwargs):
        super().__init__(inlinefield)
        self.fieldname = inlinefield
        self.wrapper = kwargs.pop("wrapper", Div())
        self.args = args
        self.kwargs = kwargs

    def get_wrapper_layout(self):
        return self.wrapper

    def get_inline_layout(self):
        if (
            DELETION_FIELD_NAME not in self.args
            and DELETION_FIELD_NAME not in self.kwargs
        ):
            self.args = self.args + (DELETION_FIELD_NAME, "id")
        return Layout(
            Div(
                *self.args,
                **self.kwargs,
                css_class="card-panel",
                style="position: relative",
            )
        )


class SortableHeader(NonFormField):
    def __init__(self, field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = field

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):

        """
        <a href="{% updated_querystring "order" new_order_string %}">
            {{ prettyname }}
            {% if '-'|add:field in request.GET.order %}
                <i class="material-icons tiny">keyboard_arrow_up</i>
            {% elif field in request.GET.order %}
                <i class="material-icons tiny">keyboard_arrow_down</i>
            {% endif %}
        </a>
        """
        order = context.get("request").GET.get("order", "")
        href = updated_querystring(
            context, "order", querystring_order(order, self.field),
        )
        if "-" + self.field in order:
            return render_field(
                A(
                    FieldLabel(self.field),
                    MaterialIcon("keyboard_arrow_up", css_class="tiny"),
                    href=href,
                ),
                {},
                None,
                context,
            )
        elif self.field in order:
            return render_field(
                A(
                    FieldLabel(self.field),
                    MaterialIcon("keyboard_arrow_down", css_class="tiny"),
                    href=href,
                ),
                {},
                None,
                context,
            )
        return render_field(A(FieldLabel(self.field), href=href), {}, None, context)


class MaterialIcon(HTMLTag):
    tag = "i"

    def __init__(self, icon, css_class=""):
        super().__init__(HTML(icon), css_class="material-icons " + css_class)


def default_list_layout(fields, sortable_by):
    fields = with_str_fields_replaced(
        Layout(TR.with_td(ObjectActionsDropDown(), *fields)),
        layout_generator=lambda f: FieldValue(f),
    )
    headers = []
    for fieldname in get_fieldnames(fields):
        if fieldname in sortable_by:
            headers.append(SortableHeader(fieldname))
        else:
            headers.append(FieldLabel(fieldname))

    return Layout(
        TABLE(
            THEAD(TR.with_th(*headers)),
            TBODY(ItemContainer("object_list", "object", fields)),
            css_class="responsive-table striped highlight",
        )
    )
