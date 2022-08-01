# Generated by Django 3.2.12 on 2022-04-06 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0008_rename_name_reportcolumn_header'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportcolumn',
            name='sortingname',
            field=models.CharField(blank=True, help_text='Django sorting expression', max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='reportcolumn',
            name='column',
            field=models.CharField(help_text="Value expression (see 'Help')", max_length=255, verbose_name='Column'),
        ),
        migrations.AlterField(
            model_name='reportcolumn',
            name='header',
            field=models.CharField(max_length=255, verbose_name='Header'),
        ),
    ]