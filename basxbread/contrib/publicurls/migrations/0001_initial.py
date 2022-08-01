# Generated by Django 4.0.5 on 2022-07-15 09:56

from typing import List

from django.db import migrations, models

import basxbread.contrib.publicurls.models


class Migration(migrations.Migration):

    initial = True

    dependencies: List[None] = []

    operations = [
        migrations.CreateModel(
            name="PublicURL",
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
                ("name", models.CharField(max_length=255, verbose_name="Name")),
                (
                    "url",
                    models.CharField(
                        max_length=2048,
                        validators=[basxbread.contrib.publicurls.models.validate_url],
                        verbose_name="URL",
                    ),
                ),
                (
                    "salt",
                    models.CharField(
                        editable=False, max_length=32, verbose_name="Salt"
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, verbose_name="Created"),
                ),
                (
                    "valid_for",
                    models.DurationField(
                        blank=True, null=True, verbose_name="Valid for"
                    ),
                ),
                (
                    "has_form",
                    models.BooleanField(default=False, verbose_name="Has form"),
                ),
            ],
            options={
                "verbose_name": "Public URL",
                "verbose_name_plural": "Public URLs",
            },
        ),
    ]