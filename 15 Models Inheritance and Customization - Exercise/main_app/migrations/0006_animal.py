# Generated by Django 5.0.4 on 2025-03-07 07:51

import main_app.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_hotel_room_regularreservation_specialreservation'),
    ]

    operations = [
        migrations.CreateModel(
            name='Animal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('animal_id', main_app.fields.AnimalIDField()),
            ],
        ),
    ]
