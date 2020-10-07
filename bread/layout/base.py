import copy

from crispy_forms.layout import LayoutObject as CrispyLayoutObject
from crispy_forms.utils import TEMPLATE_PACK, flatatt
from django.core.exceptions import FieldDoesNotExist
from django.template import Template

from .. import formatters
from ..utils import pretty_fieldname, title


class ItemContainer(CrispyLayoutObject):
    def __init__(self, iterable_name, item_name, inline_layout, *args, **kwargs):
        """
            iterable_name: Name of a context variable over which should be iterated
            item_name: Name which the loop-variable should be called
            inline_layout: Layout which will be rendered for each item
        """
        super().__init__(*args, **kwargs)
        self.inline_layout = inline_layout
        self.template = Template(
            "{% load bread_tags %}{% for "
            + item_name
            + " in "
            + iterable_name
            + " %}{% crispy_html layout %}{% endfor %}"
        )

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        context.update({"layout": self.inline_layout})
        return self.template.render(context)


class HTMLTag(CrispyLayoutObject):
    tag = "div"

    def __init__(self, *fields, **kwargs):
        self.fields = list(fields)
        if "css_class" in kwargs:
            kwargs["class"] = kwargs.pop("css_class")
        self.flat_attrs = flatatt(kwargs)
        self.template = Template(
            """
<{{ element.tag }} {% if element.css_id %}id="{{ element.css_id }}"{% endif %} {{ element.flat_attrs|safe }}>
    {{ fields|safe }}
</{{ element.tag }}>
        """
        )

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        fields = self.get_rendered_fields(
            form, form_style, context, template_pack, **kwargs
        )
        c = copy.copy(context)
        c.update({"element": self, "fields": fields})
        return self.template.render(c)


Div = HTMLTag


class NonFormField(CrispyLayoutObject):
    """Prevents components to contribute to the list of form fields"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = []


class FieldLabel(NonFormField):
    """Renders the verbose name of a field """

    def __init__(self, field, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.field = field

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        obj = (
            context.get("object")
            or getattr(context.get("object_list"), "model", None)
            or context["form"].instance
        )
        field = None
        if hasattr(obj, "_meta"):
            try:
                field = obj._meta.get_field(self.field)
            except FieldDoesNotExist:
                pass
        if field:
            return pretty_fieldname(obj._meta.get_field(self.field))
        elif hasattr(getattr(obj, self.field, None), "verbose_name"):
            return title(getattr(obj, self.field).verbose_name)
        return title(self.field.replace("_", " "))


class FieldValue(NonFormField):
    """Accepts an optional parameter ``renderer`` which will be called with the
    object and the field name when this field is beeing rendered"""

    def __init__(self, field, *args, **kwargs):
        self.renderer = kwargs.pop("renderer", formatters.render_field)
        super().__init__(*args, **kwargs)
        self.field = field

    def render(self, form, form_style, context, template_pack=TEMPLATE_PACK, **kwargs):
        obj = context.get("object") or context["form"].instance
        ret = str(self.renderer(obj, self.field))
        return ret


# Layout helper methods


def convert_to_formless_layout(layout_object, show_label=True):
    """Recursively convert fields of type string to FieldValue.
    Usefull if a layout has been defined for native crispy-form layouts
    and should be reused on a read-only view."""
    for i, field in enumerate(layout_object.fields):
        if isinstance(field, str):
            if show_label:
                layout_object.fields[i] = Div(FieldLabel(field), FieldValue(field))
            else:
                layout_object.fields[i] = FieldValue(field)
        elif hasattr(field, "fields"):
            convert_to_formless_layout(field, show_label)


def with_str_fields_replaced(
    layout_object, layout_generator=lambda f: Div(FieldLabel(f), FieldValue(f))
):
    """Recursively convert fields of type string in the given layout to the
    desired object, generated by the layout_generator."""
    layout_object = copy.deepcopy(layout_object)

    def _recursive_replace(layout):
        for i, field in enumerate(layout.fields):
            if isinstance(field, str):
                layout.fields[i] = layout_generator(field)
            elif hasattr(field, "fields"):
                _recursive_replace(field)

    _recursive_replace(layout_object)

    return layout_object


def get_fieldnames(layout):
    if hasattr(layout, "field"):
        yield layout.field
    else:
        for field in getattr(layout, "fields", ()):
            yield from get_fieldnames(field)


# Some standard HTML tags


class TABLE(HTMLTag):
    tag = "table"


class TBODY(HTMLTag):
    tag = "tbody"


class THEAD(HTMLTag):
    tag = "thead"


class TR(HTMLTag):
    tag = "tr"

    @classmethod
    def with_td(cls, *args):
        return TR(*[TD(arg) for arg in args])

    @classmethod
    def with_th(cls, *args):
        return TR(*[TH(arg) for arg in args])


class TD(HTMLTag):
    tag = "td"


class TH(HTMLTag):
    tag = "th"


class A(HTMLTag):
    tag = "a"
