# Generated by Django 4.2.6 on 2023-12-16 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0002_branch_remove_basicorginfo_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='branch',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='branch',
            name='landline_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='coastpatrolcorps',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='coastpatrolcorps',
            name='central_exchange_intercom',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
        migrations.AddField(
            model_name='coastpatrolcorps',
            name='landline_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='administration',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='administration',
            name='landline_phone',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
