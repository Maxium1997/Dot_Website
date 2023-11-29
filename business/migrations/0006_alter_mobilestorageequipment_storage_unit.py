# Generated by Django 4.2.6 on 2023-11-28 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0005_alter_mobilestorageequipment_storage_unit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mobilestorageequipment',
            name='storage_unit',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(1, 'KB'), (2, 'MB'), (3, 'GB'), (4, 'TB')], null=True),
        ),
    ]
