# Generated by Django 4.2.6 on 2024-02-22 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0021_oceanstation'),
    ]

    operations = [
        migrations.AddField(
            model_name='oceanstation',
            name='cover_photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='oceanstation',
            name='name',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
