# Generated by Django 2.2.10 on 2020-08-30 17:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('multistore', '0002_auto_20200828_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='stock',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]