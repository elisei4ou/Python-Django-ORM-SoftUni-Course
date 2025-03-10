# Generated by Django 5.0.4 on 2025-03-08 12:53

import django.core.validators
import main_app.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, validators=[main_app.validators.name_validator])),
                ('age', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(18, 'Age must be greater than or equal to 18')])),
                ('email', models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator('Enter a valid email address')])),
                ('phone_number', models.CharField(max_length=13, validators=[main_app.validators.phone_number_validator])),
                ('website_url', models.URLField(validators=[django.core.validators.URLValidator('Enter a valid URL')])),
            ],
        ),
    ]
