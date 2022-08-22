# Generated by Django 4.0.5 on 2022-08-19 06:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triggers', '0003_auto_20220519_1018'),
    ]

    operations = [
        migrations.AddField(
            model_name='datachangetrigger',
            name='field',
            field=models.CharField(blank=True, help_text='Only trigger when a certain field has changed', max_length=255, verbose_name='Field'),
        ),
    ]
