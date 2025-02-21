# Generated by Django 5.1.6 on 2025-02-20 10:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('land_area', models.CharField(choices=[('2.5-3.0', '2.5 to 3.0 aana'), ('3.0-3.5', '3.0 to 3.5 aana'), ('3.5-4.0', '3.5 to 4.0 aana'), ('4.0-4.5', '4.0 to 4.5 aana'), ('4.5-5.0', '4.5 to 5.0 aana'), ('> 5.0', 'Greater than 5 aana')], max_length=20)),
                ('ground_coverage', models.FloatField(max_length=50)),
                ('construction_standard', models.CharField(choices=[('affordable', 'Affordable Construction'), ('premium', 'Premium Construction')], max_length=20)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Floor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_number', models.PositiveIntegerField()),
                ('staircase', models.BooleanField(default=False)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='floor', to='ajira.home')),
            ],
        ),
        migrations.CreateModel(
            name='Municipality',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipalities', to='ajira.district')),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_number', models.CharField(blank=True, max_length=13, null=True, unique=True)),
                ('submitted_at', models.DateTimeField(auto_now_add=True)),
                ('district', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ajira.district')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locations', to='ajira.home')),
                ('municipality', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ajira.municipality')),
            ],
        ),
        migrations.CreateModel(
            name='Other',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13)),
                ('finish_type', models.CharField(max_length=50)),
                ('finish', models.CharField(max_length=50)),
                ('qty', models.CharField(max_length=100)),
                ('rate', models.PositiveIntegerField(default=0)),
                ('cost', models.PositiveIntegerField(default=0)),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='other', to='ajira.home')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_numm', models.PositiveIntegerField(default=0)),
                ('room_type', models.CharField(choices=[('bedroom', 'Bedroom'), ('living', 'Living'), ('kitchen', 'Kitchen'), ('bathroom', 'Bathroom'), ('parking', 'Parking'), ('puja', 'Puja Room'), ('laundry', 'Laundry Room'), ('store', 'Store Room')], max_length=50)),
                ('quantity', models.PositiveIntegerField(default=0)),
                ('flooring_type', models.CharField(choices=[('none', 'None'), ('tile', 'Tile'), ('granite', 'Granite'), ('parquet', 'Parquet'), ('sisou', 'Sisou')], default='none', max_length=50)),
                ('room_area', models.PositiveIntegerField(default=0)),
                ('rate', models.PositiveIntegerField(default=0)),
                ('cost', models.PositiveIntegerField(default=0)),
                ('window_area', models.PositiveIntegerField(default=0)),
                ('floor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to='ajira.floor')),
                ('user_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='room', to='ajira.home')),
            ],
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=13)),
                ('total_house_area', models.PositiveIntegerField(default=0)),
                ('no_of_floors', models.PositiveIntegerField(default=0)),
                ('total_carpet_area', models.PositiveIntegerField(default=0)),
                ('user_name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='summary', to='ajira.home')),
            ],
        ),
    ]
