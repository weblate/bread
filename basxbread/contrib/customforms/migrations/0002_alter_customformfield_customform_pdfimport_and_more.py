# Generated by Django 4.1.2 on 2022-11-09 07:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customforms", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customformfield",
            name="customform",
            field=models.ForeignKey(
                editable=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="customformfields",
                to="customforms.customform",
                verbose_name="Custom form",
            ),
        ),
        migrations.CreateModel(
            name="PDFImport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf",
                    models.FileField(upload_to="pdf_import", verbose_name="PDF form"),
                ),
                (
                    "customform",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="customforms.customform",
                    ),
                ),
            ],
            options={
                "verbose_name": "PDF import",
                "verbose_name_plural": "PDF imports",
            },
        ),
        migrations.CreateModel(
            name="PDFFormField",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "pdf_field_name",
                    models.CharField(max_length=256, verbose_name="PDF field name"),
                ),
                (
                    "customform_field",
                    models.ForeignKey(
                        limit_choices_to={
                            "customform": models.F("pdfimport__customform")
                        },
                        on_delete=django.db.models.deletion.CASCADE,
                        to="customforms.customformfield",
                    ),
                ),
                (
                    "pdfimport",
                    models.ForeignKey(
                        editable=False,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="fields",
                        to="customforms.pdfimport",
                        verbose_name="PDF form field",
                    ),
                ),
            ],
            options={
                "verbose_name": "PDF import field",
                "verbose_name_plural": "PDF import fields",
                "unique_together": {
                    ("pdfimport", "pdf_field_name"),
                    ("pdfimport", "customform_field"),
                },
            },
        ),
    ]