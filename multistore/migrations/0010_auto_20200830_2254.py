# Generated by Django 2.2.10 on 2020-08-30 17:24

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('multistore', '0009_auto_20200830_2253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='stock',
            name='timestamp',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
