# Generated by Django 3.2.13 on 2022-05-19 10:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triggers', '0002_auto_20220208_1215'),
    ]

    operations = [
        migrations.AddField(
            model_name='datachangetrigger',
            name='description',
            field=models.CharField(default='Missing description', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='datefieldtrigger',
            name='description',
            field=models.CharField(default='Missing description', max_length=255),
            preserve_default=False,
        ),
    ]
