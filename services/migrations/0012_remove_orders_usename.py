# Generated by Django 3.1.7 on 2021-05-24 18:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0011_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='usename',
        ),
    ]
