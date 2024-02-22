# Generated by Django 4.2.6 on 2024-02-18 16:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('business', '0020_certificateapplication'),
    ]

    operations = [
        migrations.CreateModel(
            name='OceanStation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
                ('manage_administration_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('administrative_district', models.CharField(blank=True, max_length=5, null=True)),
                ('address', models.CharField(blank=True, max_length=50, null=True)),
                ('contact_number', models.CharField(blank=True, max_length=12, null=True)),
                ('coordinate_longitude', models.CharField(blank=True, max_length=12, null=True)),
                ('coordinate_latitude', models.CharField(blank=True, max_length=12, null=True)),
                ('service_items', models.PositiveSmallIntegerField(default=1)),
                ('fans_page_url', models.URLField(blank=True, null=True)),
                ('manage_administration_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
        ),
    ]
