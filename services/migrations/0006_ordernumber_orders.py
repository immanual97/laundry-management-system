# Generated by Django 3.1.7 on 2021-05-22 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_orders_homedelivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordernumber',
            name='orders',
            field=models.IntegerField(default=0),
        ),
    ]
