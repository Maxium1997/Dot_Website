# Generated by Django 4.2.6 on 2024-01-28 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_place', '0008_order_created_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]