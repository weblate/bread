# Generated by Django 3.2.10 on 2022-01-25 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('triggers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datefieldtrigger',
            name='date_offset',
            field=models.CharField(help_text="Use e.g. '2 days ago' or 'in 1 week' to trigger 2 days before the specified date field or 1 week after it ", max_length=255),
        ),
        migrations.AlterField(
            model_name='sendemail',
            name='message',
            field=models.TextField(help_text="Will be rendered as a Django template with the name 'object' in the context", verbose_name='Message'),
        ),
        migrations.AlterField(
            model_name='sendemail',
            name='subject',
            field=models.CharField(help_text="Will be rendered as a Django template with the name 'object' in the context", max_length=255, verbose_name='Subject'),
        ),
    ]
