# Generated by Django 4.2.6 on 2023-12-16 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0008_remove_patrolstation_serial_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patrolstation',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='patrolstation',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AddField(
            model_name='patrolstation',
            name='intercom_phone',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='patrolstation',
            name='landline_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='inspectionoffice',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='inspectionoffice',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='inspectionoffice',
            name='intercom_phone',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AlterField(
            model_name='inspectionoffice',
            name='landline_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]