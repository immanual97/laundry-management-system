# Generated by Django 3.1.7 on 2021-05-25 08:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0012_remove_orders_usename'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orders',
            name='status',
        ),
        migrations.AddField(
            model_name='orders',
            name='statusid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='services.status'),
        ),
    ]