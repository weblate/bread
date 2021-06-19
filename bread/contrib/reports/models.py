import htmlgenerator as hg
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.translation import gettext_lazy as _

from bread import layout

from ...layout.components.datatable import DataTableColumn
from .fields.queryfield import QuerysetField


def available_report_filters(modelfield, request, report):
    from django.conf import settings

    return tuple((i, i) for i in getattr(settings, "REPORT_FILTERS", {}).keys())


class Report(models.Model):
    created = models.DateField(_("Created"), auto_now_add=True)
    name = models.CharField(_("Name"), max_length=255)
    model = models.ForeignKey(
        ContentType,
        on_delete=models.PROTECT,
    )
    model.verbose_name = _("Model")
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

    @property
    def preview(self):
        columns = []
        for column in self.columns.all():
            columns.append(
                DataTableColumn(column.name, layout.FC(f"row.{column.column}"))
            )

        return hg.BaseElement(
            hg.H3(_("Preview")),
            layout.datatable.DataTable.from_queryset(
                self.queryset[:25], columns=columns, with_toolbar=False
            ),
        )

    @property
    def queryset(self):
        if self.custom_queryset:
            # do not check whether the settings exists, an exception can be raised automatically
            ret = settings.REPORT_FILTERS[self.custom_queryset]()
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
            return ret
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
    column = models.CharField(_("Column"), max_length=255)
    name = models.CharField(_("Name"), max_length=255)
    aggregation = models.CharField(
        _("Aggregation"), max_length=64, choices=tuple(AGGREGATIONS.items()), blank=True
    )

    class Meta:
        verbose_name = _("Column")
        verbose_name_plural = _("Columns")
        order_with_respect_to = "report"
