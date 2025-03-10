# Generated by Django 5.0.4 on 2025-03-08 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0004_alter_customer_email_alter_customer_website_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(error_messages={'invalid': 'Enter a valid email address'}, max_length=254),
        ),
        migrations.AlterField(
            model_name='customer',
            name='website_url',
            field=models.URLField(error_messages={'invalid': 'Enter a valid URL'}),
        ),
    ]
