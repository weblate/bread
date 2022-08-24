import htmlgenerator as hg
from django import forms
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _
from jinja2.sandbox import SandboxedEnvironment

from basxbread import layout
from basxbread.querysetfield import QuerysetField, parsequeryexpression

from ...layout.components.datatable import DataTableColumn


def available_report_filters(modelfield, request, report):
    from django.conf import settings

    return tuple((i, i) for i in getattr(settings, "REPORT_FILTERS", {}).keys())


class Report(models.Model):
    created = models.DateField(_("Created"), auto_now_add=True)
    name = models.CharField(_("Name"), max_length=255)
    model = models.ForeignKey(
        ContentType, on_delete=models.PROTECT, verbose_name=_("Model")
    )
    model.formfield_kwargs = {
        "queryset": ContentType.objects.all().order_by("app_label", "model")
    }
    filter = QuerysetField(_("Filter"), modelfieldname="model")
    custom_queryset = models.CharField(
        _("Custom Filter"),
        max_length=255,
        help_text=_(
            "Key in 'settings.REPORT_FILTERS' must be a function returning a queryset"
        ),
        blank=True,
    )
    custom_queryset.lazy_choices = available_report_filters
    pagination = models.PositiveIntegerField(
        _("Pagination"),
        default=0,
        help_text=_(
            "How many items to display per page when viewing the "
            "report in the browser, 0 for everything on one page"
        ),
    )

    @property
    def preview(self):
        columns = []
        for column in self.columns.all():
            columns.append(
                DataTableColumn(
                    header=column.header,
                    cell=column.render_element("row"),
                )
            )
        qs = self.queryset
        if qs is None:
            return hg.BaseElement("Model does no longer exists!")

        return layout.datatable.DataTable.from_queryset(
            title=_("Preview"),
            helper_text="",
            queryset=qs[:10],
            columns=columns,
            primary_button="",
        )

    @property
    def queryset(self):
        if self.custom_queryset and self.custom_queryset in getattr(
            settings, "REPORT_FILTERS", {}
        ):
            # do not check whether the settings exists, an exception can be raised automatically
            ret = getattr(settings, "REPORT_FILTERS", {}).get(
                self.custom_queryset, lambda model: model.objects.none()
            )(self.model.model_class())
            if not isinstance(ret, models.QuerySet):
                raise ValueError(
                    _(
                        'settings.REPORT_FILTERS["%s"] did not return a queryset but returned: %s'
                    )
                    % (self.custom_queryset, ret)
                )
            if ret.model != self.model.model_class():
                raise ValueError(
                    _(
                        'settings.REPORT_FILTERS["%s"] did not return a queryset for %s but for %s'
                    )
                    % (self.custom_queryset, self.model.model_class(), ret.model)
                )
            return parsequeryexpression(ret, self.filter.raw).queryset
        return self.filter.queryset

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Report")
        verbose_name_plural = _("Reports")
        ordering = ["name"]


class ReportColumn(models.Model):
    AGGREGATIONS = {
        "count": "",
        "sum": "",
    }
    report = models.ForeignKey(Report, on_delete=models.CASCADE, related_name="columns")
    header = models.CharField(_("Header"), max_length=255)
    column = models.CharField(
        _("Column"), max_length=255, help_text=_("Value expression (see 'Help')")
    )
    cell_template = models.TextField(
        _("Cell template"),
        blank=True,
        help_text=hg.mark_safe(
            _(
                "Optional Jinja template with 'value' in context.<br/>Use e.g. {{ value }} to simply display the value."
            )
        ),
    )
    cell_template.formfield_kwargs = {"widget": forms.Textarea(attrs={"rows": 1})}
    sortingname = models.CharField(
        _("Sortingname"),
        max_length=255,
        blank=True,
        help_text=_("Django sorting expression"),
    )
    aggregation = models.CharField(
        _("Aggregation"), max_length=64, choices=tuple(AGGREGATIONS.items()), blank=True
    )

    def render_element(self, rowvariable):
        if self.cell_template:

            def render(context):
                elementenv = SandboxedEnvironment()
                elementenv.filters["map"] = lambda value, map: map.get(value, value)
                try:
                    return elementenv.from_string(self.cell_template).render(
                        value=hg.resolve_lookup(context[rowvariable], self.column),
                    )
                except Exception as e:
                    return f"### ERROR: {e} ###"

            return hg.BaseElement(hg.F(render))

        return layout.ObjectFieldValue(self.column, rowvariable)

    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        order_with_respect_to = "report"
