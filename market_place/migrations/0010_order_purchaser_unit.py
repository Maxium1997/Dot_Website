# Generated by Django 4.2.6 on 2024-01-28 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market_place', '0009_alter_order_created_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='purchaser_unit',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
