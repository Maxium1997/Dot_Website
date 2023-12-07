# Generated by Django 4.2.6 on 2023-12-07 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0012_rename_brand_mobiledevice_sp_brand_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='mobiledevice',
            name='owner_unit',
            field=models.PositiveIntegerField(blank=True, choices=[(804000, 'Non Set'), (804012, 'CIE Squad'), (704310, 'First Patrol Station'), (704320, 'Second Patrol Station'), (704010, 'XuCuoLiao Inspection Office'), (704020, 'Mailiao Harbor Inspection Office'), (704030, 'WenGang Inspection Office'), (704040, 'WuTiaoGang Fishing Harbor Inspection Office'), (704050, 'TaiXi Fishing Harbor Inspection Office'), (704060, 'SanTiaoLu Fishing Harbor Inspection Office'), (704070, 'BoZiLiao Fishing Harbor Inspection Office'), (704080, 'JinHu Fishing Harbor Inspection Office'), (704090, 'TaiZiVillage Fishing Harbor Inspection Office'), (704110, 'XiaHuKou Inspection Office'), (704210, 'FuLai Fishing Harbor Inspection Office'), (704220, 'XingCuo Fishing Harbor Inspection Office'), (704230, 'WenGang Fishing Harbor Inspection Office'), (704240, 'DongShi Fishing Harbor Inspection Office'), (704250, 'WangLiau Fishing Harbor Inspection Office'), (704260, 'BaiShuiHu Fishing Harbor Inspection Office'), (704270, 'BuDai Fishing Port Inspection Office'), (704280, 'BuDai Port Inspection Office'), (704290, 'HauMeiVillage Fishing Harbor Inspection Office')], default=804000, null=True),
        ),
        migrations.AlterField(
            model_name='mobiledevicelist',
            name='manage_unit',
            field=models.PositiveIntegerField(choices=[(804000, 'Non Set'), (804012, 'CIE Squad'), (704310, 'First Patrol Station'), (704320, 'Second Patrol Station'), (704010, 'XuCuoLiao Inspection Office'), (704020, 'Mailiao Harbor Inspection Office'), (704030, 'WenGang Inspection Office'), (704040, 'WuTiaoGang Fishing Harbor Inspection Office'), (704050, 'TaiXi Fishing Harbor Inspection Office'), (704060, 'SanTiaoLu Fishing Harbor Inspection Office'), (704070, 'BoZiLiao Fishing Harbor Inspection Office'), (704080, 'JinHu Fishing Harbor Inspection Office'), (704090, 'TaiZiVillage Fishing Harbor Inspection Office'), (704110, 'XiaHuKou Inspection Office'), (704210, 'FuLai Fishing Harbor Inspection Office'), (704220, 'XingCuo Fishing Harbor Inspection Office'), (704230, 'WenGang Fishing Harbor Inspection Office'), (704240, 'DongShi Fishing Harbor Inspection Office'), (704250, 'WangLiau Fishing Harbor Inspection Office'), (704260, 'BaiShuiHu Fishing Harbor Inspection Office'), (704270, 'BuDai Fishing Port Inspection Office'), (704280, 'BuDai Port Inspection Office'), (704290, 'HauMeiVillage Fishing Harbor Inspection Office')], default=804012),
        ),
        migrations.AlterField(
            model_name='mobilestorageequipment',
            name='manage_unit',
            field=models.PositiveIntegerField(choices=[(804000, 'Non Set'), (804012, 'CIE Squad'), (704310, 'First Patrol Station'), (704320, 'Second Patrol Station'), (704010, 'XuCuoLiao Inspection Office'), (704020, 'Mailiao Harbor Inspection Office'), (704030, 'WenGang Inspection Office'), (704040, 'WuTiaoGang Fishing Harbor Inspection Office'), (704050, 'TaiXi Fishing Harbor Inspection Office'), (704060, 'SanTiaoLu Fishing Harbor Inspection Office'), (704070, 'BoZiLiao Fishing Harbor Inspection Office'), (704080, 'JinHu Fishing Harbor Inspection Office'), (704090, 'TaiZiVillage Fishing Harbor Inspection Office'), (704110, 'XiaHuKou Inspection Office'), (704210, 'FuLai Fishing Harbor Inspection Office'), (704220, 'XingCuo Fishing Harbor Inspection Office'), (704230, 'WenGang Fishing Harbor Inspection Office'), (704240, 'DongShi Fishing Harbor Inspection Office'), (704250, 'WangLiau Fishing Harbor Inspection Office'), (704260, 'BaiShuiHu Fishing Harbor Inspection Office'), (704270, 'BuDai Fishing Port Inspection Office'), (704280, 'BuDai Port Inspection Office'), (704290, 'HauMeiVillage Fishing Harbor Inspection Office')], default=804012),
        ),
    ]
