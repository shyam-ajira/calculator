# Generated by Django 5.1.6 on 2025-02-20 06:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ajira', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='summary',
            name='total_carpet_area',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
