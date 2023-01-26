# Generated by Django 4.1.3 on 2023-01-25 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('geoportal_core', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='layer',
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name='layer',
            name='area',
        ),
        migrations.RemoveField(
            model_name='layer',
            name='module',
        ),
        migrations.RemoveField(
            model_name='simplefeature',
            name='layer',
        ),
        migrations.RemoveField(
            model_name='simplefeaturefield',
            name='feature',
        ),
        migrations.DeleteModel(
            name='Area',
        ),
        migrations.DeleteModel(
            name='Layer',
        ),
        migrations.DeleteModel(
            name='SimpleFeature',
        ),
        migrations.DeleteModel(
            name='SimpleFeatureField',
        ),
    ]
