# Generated by Django 4.1.7 on 2023-07-13 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontend', '0007_street_osm_imported'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='text',
            field=models.CharField(blank=True, default='', max_length=2000),
        ),
    ]
