# Generated by Django 2.2.10 on 2020-08-28 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('multistore', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location_name', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_code', models.CharField(max_length=64)),
            ],
        ),
        migrations.AlterField(
            model_name='stock',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='multistore.Location'),
        ),
        migrations.AlterField(
            model_name='stock',
            name='sku',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='multistore.SKU'),
        ),
    ]
