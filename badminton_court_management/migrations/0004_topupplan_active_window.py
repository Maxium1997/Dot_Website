from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badminton_court_management', '0003_gymstaff'),
    ]

    operations = [
        migrations.AddField(
            model_name='topupplan',
            name='active_start',
            field=models.DateTimeField(blank=True, null=True, verbose_name='活動開始時間'),
        ),
        migrations.AddField(
            model_name='topupplan',
            name='active_end',
            field=models.DateTimeField(blank=True, null=True, verbose_name='活動結束時間'),
        ),
    ]
