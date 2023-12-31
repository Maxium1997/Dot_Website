# Generated by Django 4.2.6 on 2023-12-31 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('market_place', '0003_alter_certificateapplication_applicant_unit_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField()),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=20)),
                ('purchaser', models.CharField(max_length=50)),
                ('content', models.TextField(blank=True, null=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(0, 'Pending'), (1, 'Confirmed'), (2, 'Process'), (3, 'Completed'), (4, 'Canceled')], default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=150)),
                ('creator', models.CharField(max_length=50)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('serial_number', models.CharField(max_length=20)),
                ('name', models.CharField(max_length=20)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Available'), (2, 'Reserved'), (3, 'In Transit'), (4, 'Damaged'), (5, 'Picking'), (6, 'In Progress'), (7, 'Delivered'), (0, 'Returned')], default=1)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='market_place.category')),
            ],
        ),
    ]
