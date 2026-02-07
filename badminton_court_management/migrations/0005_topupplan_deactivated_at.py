from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badminton_court_management', '0004_topupplan_active_window'),
    ]

    operations = [
        migrations.AddField(
            model_name='topupplan',
            name='deactivated_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='失效時間'),
        ),
    ]
