# coast_guard_mart/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import MemberCredit
from django.utils import timezone
from datetime import timedelta


@receiver(post_save, sender=User)
def create_member_credit(sender, instance, created, **kwargs):
    if created:
        # 當新使用者建立時（第一次 LINE 登入），自動給予當年度效期的 3000 元
        MemberCredit.objects.create(
            user=instance,
            fiscal_year=timezone.now().year,
            start_date=timezone.now(),
            # end_date=timezone.now().replace(month=12, day=31, hour=23, minute=59),
            end_date=timezone.now() + timedelta(days=60),
            balance=3000.00
        )
