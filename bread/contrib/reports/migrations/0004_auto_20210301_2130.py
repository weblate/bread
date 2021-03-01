# Generated by Django 3.1.5 on 2021-03-01 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0003_auto_20210301_1229'),
    ]

    operations = [
        migrations.AddField(
            model_name='reportcolumn',
            name='name',
            field=models.CharField(default='???', max_length=255, verbose_name='Name'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='report',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Name'),
        ),
        migrations.AlterField(
            model_name='reportcolumn',
            name='column',
            field=models.CharField(max_length=255, verbose_name='Column'),
        ),
    ]
