"""
Bread comes with a list of "improved" django views. All views are based
on the standard class-based views of django and are should easily be
extendable and composable by subclassing them. Most of the views require
an argument "admin" which is an instance of the according BreadAdmin class
"""
import urllib

from crispy_forms.layout import Layout
from crispy_forms.utils import TEMPLATE_PACK
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView
from guardian.mixins import PermissionRequiredMixin

from ..utils import CustomizableClass, filter_fieldlist, get_modelfields
from .util import CustomFormMixin


class EditView(
    CustomizableClass,
    CustomFormMixin,
    SuccessMessageMixin,
    PermissionRequiredMixin,
    UpdateView,
):
    template_name = f"{TEMPLATE_PACK}/form.html"
    admin = None
    sidebarfields = []
    accept_global_perms = True

    def get_success_message(self, cleaned_data):
        return f"Saved {self.object}"

    def __init__(self, admin, *args, **kwargs):
        self.admin = admin
        self.model = admin.model
        field_config = kwargs.get("fields", self.fields)
        if not isinstance(field_config, Layout):
            self.layout = Layout(
                *filter_fieldlist(self.model, field_config, for_form=True)
            )
        else:
            self.layout = field_config
        self.fields = [i[1] for i in self.layout.get_field_names()]
        self.sidebarfields = get_modelfields(
            self.model, kwargs.get("sidebarfields", self.sidebarfields)
        )
        super().__init__(*args, **kwargs)

    def get_required_permissions(self, request):
        return [f"{self.model._meta.app_label}.change_{self.model.__name__.lower()}"]

    def get_success_url(self):
        if "quicksave" in self.request.POST:
            return self.request.get_full_path()
        if self.request.GET.get("next"):
            return urllib.parse.unquote(self.request.GET["next"])
        return self.admin.reverse("index")
