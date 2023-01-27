# Generated by Django 4.1.3 on 2023-01-27 09:04

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=15)),
                ('alias', models.CharField(max_length=50)),
                ('bbox', django.contrib.gis.db.models.fields.MultiPointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='RasterFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=15)),
                ('r_file', models.FilePathField()),
            ],
        ),
        migrations.CreateModel(
            name='SomeGISModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('int_property', models.IntegerField(max_length=2)),
                ('point_field', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Layer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SlugField(max_length=15)),
                ('alias', models.CharField(max_length=50)),
                ('ordering', models.IntegerField(max_length=5)),
                ('layer_type', models.CharField(choices=[('V', 'Vector'), ('R', 'Raster')], max_length=1)),
                ('area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='module_template.area')),
            ],
        ),
    ]