# Generated by Django 2.2.10 on 2020-08-30 17:21

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('multistore', '0006_auto_20200830_2250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime(2020, 8, 30, 17, 21, 42, 785943, tzinfo=utc)),
        ),
    ]
