# Generated by Django 3.2.6 on 2021-08-26 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0004_auto_20210619_1502"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
        migrations.AlterField(
            model_name="reportcolumn",
            name="id",
            field=models.BigAutoField(
                auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
            ),
        ),
    ]
