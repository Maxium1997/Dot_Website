# Generated by Django 4.2.6 on 2024-01-15 15:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('business', '0019_remove_subcategory_category_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CertificateApplication',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usage', models.PositiveSmallIntegerField(choices=[(1, 'Personal'), (2, 'Agency'), (3, 'Server')], default=1)),
                ('applicant_name', models.CharField(max_length=10)),
                ('applicant_contact_number', models.CharField(max_length=10)),
                ('applicant_unit_object_id', models.PositiveIntegerField(blank=True, null=True)),
                ('applicant_address', models.CharField(max_length=255)),
                ('custodian_commission', models.PositiveIntegerField(choices=[(5140302, 'Non Set'), (1329999161, 'General'), (1329999160, 'Lieutenant General'), (1329999159, 'Major General'), (1329999157, 'Colonel'), (1329999156, 'Lieutenant Colonel'), (1329999155, 'Major'), (1329999154, 'Captain'), (1329999153, 'First Lieutenant'), (20294, 'Second Lieutenant'), (1330785593, 'Sergeant Major'), (1330785592, 'First Sergeant'), (1330785591, 'Sergeant First Class'), (1330785590, 'Staff Sergeant'), (1330785589, 'Sergeant'), (1330785588, 'Corporal'), (1330785587, 'Private First Class'), (1330785586, 'Private E2'), (1330785585, 'Private')], default=5140302)),
                ('custodian_name', models.CharField(max_length=10)),
                ('custodian_ID_number', models.CharField(max_length=10)),
                ('custodian_contact_number', models.CharField(max_length=10)),
                ('custodian_email', models.CharField(max_length=255)),
                ('custodian_classification', models.PositiveSmallIntegerField(choices=[(1, 'Unit'), (2, 'Voluntary Military'), (3, 'Obligatory Military'), (4, 'CivilServant'), (5, 'Police'), (6, 'Outsource')], default=1)),
                ('storage', models.PositiveSmallIntegerField(choices=[(1, 'IC Card'), (2, 'Magnetic Disk')], default=1)),
                ('process', models.PositiveSmallIntegerField(choices=[(1, 'Apply'), (2, 'Undo'), (3, 'Reissue'), (4, 'Report a Loss'), (5, 'Recover'), (6, 'Reschedule')], default=1)),
                ('use_for', models.PositiveSmallIntegerField(choices=[(1, 'Duty'), (2, 'Business'), (3, 'System Using'), (4, 'Register'), (5, 'New Position'), (6, 'Transfer Position'), (7, 'Retirement'), (8, 'Change Soft Certificate'), (9, 'Broken Reapply')], default=2)),
                ('applied_date', models.DateTimeField(auto_now_add=True)),
                ('edited_date', models.DateTimeField(auto_now=True)),
                ('applicant_unit_content_type', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='contenttypes.contenttype')),
            ],
        ),
    ]
