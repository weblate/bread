# Generated by Django 3.2.6 on 2022-02-08 12:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triggers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='datefieldtrigger',
            name='ignore_year',
            field=models.BooleanField(default=False, help_text='Check this in order to trigger every year', verbose_name='Ignore year'),
        ),
        migrations.AlterField(
            model_name='datefieldtrigger',
            name='field',
            field=models.CharField(help_text='The field of the selected model which should trigger an action', max_length=255, verbose_name='Field'),
        ),
        migrations.AlterField(
            model_name='datefieldtrigger',
            name='offset_amount',
            field=models.IntegerField(help_text='Can be negative (before) or positive (after)', verbose_name='Offset amount'),
        ),
        migrations.AlterField(
            model_name='datefieldtrigger',
            name='offset_type',
            field=models.CharField(choices=[('minutes', 'Minutes'), ('hours', 'Hours'), ('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')], max_length=255, verbose_name='Offset type'),
        ),
    ]
