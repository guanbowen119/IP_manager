# Generated by Django 5.0.4 on 2024-09-27 05:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devices', '0002_alter_device_options_alter_device_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='is_login',
            field=models.BooleanField(default=False),
        ),
    ]
