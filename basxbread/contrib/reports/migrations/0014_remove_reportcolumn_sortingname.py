# Generated by Django 4.1.2 on 2022-11-30 04:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0013_fix_date_formatting"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="reportcolumn",
            name="sortingname",
        ),
    ]
