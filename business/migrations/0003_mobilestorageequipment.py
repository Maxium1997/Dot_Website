# Generated by Django 4.2.6 on 2023-11-28 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0002_subcategorydetail_sub_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MobileStorageEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=9)),
                ('name', models.CharField(max_length=20)),
                ('builtin_memory', models.BooleanField(default=False)),
                ('brand', models.CharField(max_length=20)),
                ('type', models.CharField(max_length=20)),
                ('capacity', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('storage_unit', models.PositiveSmallIntegerField(choices=[(1, 'KB'), (2, 'MB'), (3, 'GB'), (4, 'TB')], default=3)),
                ('manage_unit', models.PositiveIntegerField(choices=[(804012, 'CIE_squad'), (704310, 'first_patrol_station'), (704320, 'second_patrol_station')], default=804012)),
                ('manager', models.CharField(max_length=10)),
                ('deputy_manager', models.CharField(max_length=10)),
                ('remarks', models.TextField(blank=True, null=True)),
            ],
        ),
    ]