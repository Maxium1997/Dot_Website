# Generated by Django 4.2.6 on 2023-12-06 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0010_mobiledevice_owner_commission'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobiledevice',
            name='owner_commission',
            field=models.CharField(default=5140302, max_length=10),
        ),
    ]
