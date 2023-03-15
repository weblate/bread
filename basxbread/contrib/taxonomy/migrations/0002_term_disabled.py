# Generated by Django 4.1.5 on 2023-02-09 07:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("taxonomy", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="term",
            name="disabled",
            field=models.BooleanField(
                default=False,
                help_text="Do not allow this term to be selected",
                verbose_name="Disabled",
            ),
        ),
    ]