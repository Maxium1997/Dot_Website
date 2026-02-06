from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('badminton_court_management', '0002_topuporder_topupplan_topuporderlog_topuporder_plan_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GymStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('manager', 'Manager'), ('clerk', 'Clerk')], default='clerk', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_roles', to='badminton_court_management.gym')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gym_roles', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '球館權限',
                'verbose_name_plural': '球館權限',
                'unique_together': {('user', 'gym')},
            },
        ),
    ]
