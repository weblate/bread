# Generated by Django 4.1.2 on 2022-11-07 07:56

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="CustomForm",
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
                ("title", models.CharField(max_length=255, verbose_name="Title")),
                (
                    "pk_fields",
                    models.CharField(
                        blank=True,
                        help_text="If the form should be used to update items,\nthis fields specifies the fields that are used to\nfilter for the instance to update",
                        max_length=1024,
                        verbose_name="PK fields",
                    ),
                ),
                (
                    "model",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="contenttypes.contenttype",
                        verbose_name="Model",
                    ),
                ),
            ],
            options={
                "verbose_name": "Custom form",
                "verbose_name_plural": "Custom forms",
            },
        ),
        migrations.CreateModel(
            name="CustomFormField",
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
                    "fieldname",
                    models.CharField(
                        help_text="See help for list of possible fiel name",
                        max_length=1024,
                        verbose_name="Field name",
                    ),
                ),
                (
                    "label",
                    models.CharField(
                        blank=True,
                        help_text="Only use to override default label",
                        max_length=1024,
                        verbose_name="Label",
                    ),
                ),
                (
                    "help_text",
                    models.TextField(
                        blank=True,
                        help_text="Only use to override default help text",
                        verbose_name="Help text",
                    ),
                ),
                (
                    "customform",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="customformfields",
                        to="customforms.customform",
                        verbose_name="Custom form",
                    ),
                ),
            ],
            options={
                "verbose_name": "Custom form field",
                "verbose_name_plural": "Custom form fields",
            },
        ),
    ]
