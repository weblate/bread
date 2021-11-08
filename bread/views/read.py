import htmlgenerator as hg
from django import forms
from django.http import HttpResponseNotAllowed
from django.views.generic import DetailView as DjangoReadView
from guardian.mixins import PermissionRequiredMixin

from .. import layout as _layout  # prevent name clashing
from ..formatters import format_value
from ..forms.fields import FormsetField
from ..forms.forms import breadmodelform_factory
from ..utils import expand_ALL_constant
from .edit import EditView
from .util import BreadView


# Read view is the same as the edit view but form elements are disabled
class ReadView(EditView):
    """TODO: documentation"""

    accept_global_perms = True
    fields = None
    urlparams = (("pk", int),)

    def post(self, *args, **kwargs):
        return HttpResponseNotAllowed(["GET"])

    def get_form_class(self, form=forms.models.ModelForm):
        return breadmodelform_factory(
            request=self.request,
            model=self.model,
            layout=self._get_layout_cached(),
            instance=self.object,
            baseformclass=form,
            cache_querysets=False,
        )

    def get_form(self, *args, **kwargs):
        form = super().get_form(*args, **kwargs)
        for field in form.fields.values():
            field.disabled = True
            if isinstance(field, FormsetField):
                for subfield in field.formsetclass.form.base_fields.values():
                    subfield.disabled = True
        return form

    def get_layout(self):
        return layoutasreadonly(super().get_layout())

    def get_required_permissions(self, request):
        return [f"{self.model._meta.app_label}.view_{self.model.__name__.lower()}"]


class TableReadView(
    BreadView,
    PermissionRequiredMixin,
    DjangoReadView,
):

    accept_global_perms = True
    fields = ["__all__"]
    urlparams = (("pk", int),)

    def __init__(self, *args, **kwargs):
        self.fields = expand_ALL_constant(
            kwargs["model"], kwargs.get("fields") or self.fields
        )
        super().__init__(*args, **kwargs)

    def get_layout(self):
        return hg.BaseElement(
            hg.H3(self.object),
            _layout.datatable.DataTable(
                columns=[
                    _layout.datatable.DataTableColumn(header="", cell=hg.C("row.0")),
                    _layout.datatable.DataTableColumn(header="", cell=hg.C("row.1")),
                ],
                row_iterator=(
                    (
                        field
                        if isinstance(field, tuple)
                        else (
                            _layout.ObjectFieldLabel(field),
                            _layout.ObjectFieldValue(field, formatter=format_value),
                        )
                    )
                    for field in self.fields
                ),
            ),
        )

    def get_required_permissions(self, request):
        return [f"{self.model._meta.app_label}.view_{self.model.__name__.lower()}"]


def layoutasreadonly(layout):
    layout.wrap(
        lambda element, ancestors: isinstance(element, _layout.form.Form)
        and element.standalone,
        hg.FIELDSET(readonly="true"),
    )

    layout.delete(
        lambda element, ancestors: any(
            [isinstance(a, _layout.form.Form) for a in ancestors]
        )
        and (
            (
                isinstance(
                    element,
                    hg.BUTTON,
                )
                and "bx--tag" not in element.attributes.get("_class", "")
            )
            or getattr(element, "attributes", {}).get("type") == "submit"
        )
    )
    for form in layout.filter(lambda element, ancestors: isinstance(element, hg.FORM)):
        form.attributes["onsubmit"] = "return false;"
    return layout
