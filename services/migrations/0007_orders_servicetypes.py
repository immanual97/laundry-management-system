# Generated by Django 3.1.7 on 2021-05-23 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0006_ordernumber_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='servicetypes',
            field=models.CharField(default=None, max_length=25),
        ),
    ]
