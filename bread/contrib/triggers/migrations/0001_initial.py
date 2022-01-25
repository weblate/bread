# Generated by Django 3.2.6 on 2022-01-18 09:45

import django.db.models.deletion
from django.db import migrations, models

import bread.querysetfield


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
    ]

    operations = [
        migrations.CreateModel(
            name="Action",
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
                ("description", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Action",
                "verbose_name_plural": "Actions",
            },
        ),
        migrations.CreateModel(
            name="SendEmail",
            fields=[
                (
                    "action_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="triggers.action",
                    ),
                ),
                (
                    "email",
                    models.CharField(
                        help_text="\nSyntax:\n- Email: example@example.com\n- User/Group: @username\n- From object: manager.email (actually object.manager.email)\n\nMultiple values van be separated by comma , e.g.\nboss@example.com, @adminuser, @reviewteam, primary_email_address.email\n",
                        max_length=255,
                        verbose_name="Email",
                    ),
                ),
                ("subject", models.CharField(max_length=255, verbose_name="Subject")),
                ("message", models.TextField(verbose_name="Message")),
            ],
            options={
                "verbose_name": "Send Email Action",
                "verbose_name_plural": "Send Email Actions",
            },
            bases=("triggers.action",),
        ),
        migrations.CreateModel(
            name="DateFieldTrigger",
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
                    "filter",
                    bread.querysetfield.QuerysetField(
                        blank=True, modelfieldname="model", verbose_name="Filter"
                    ),
                ),
                ("enable", models.BooleanField(default=True)),
                ("field", models.CharField(max_length=255)),
                (
                    "date_offset",
                    models.CharField(
                        help_text="Use e.g. '2 days ago' or 'in 2 week' to trigger 2 days before the specified date field or 2 weeks after it ",
                        max_length=255,
                    ),
                ),
                (
                    "action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="triggers.action",
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
                "verbose_name": "Date field trigger",
                "verbose_name_plural": "Date field triggers",
            },
        ),
        migrations.CreateModel(
            name="DataChangeTrigger",
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
                    "filter",
                    bread.querysetfield.QuerysetField(
                        blank=True, modelfieldname="model", verbose_name="Filter"
                    ),
                ),
                ("enable", models.BooleanField(default=True)),
                (
                    "type",
                    models.TextField(
                        choices=[
                            ("added", "Added"),
                            ("changed", "Changed"),
                            ("deleted", "Deleted"),
                        ],
                        verbose_name="Type",
                    ),
                ),
                (
                    "action",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        to="triggers.action",
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
                "verbose_name": "Data change trigger",
                "verbose_name_plural": "Data change triggers",
            },
        ),
    ]
