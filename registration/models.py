from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class Member(AbstractUser):
    pass
    # email_validation_status = models.BooleanField(default=False)
    # date_of_birth = models.DateTimeField(null=True, blank=True)
    # phone_number = models.CharField(max_length=10, null=True, blank=True)
    # GENDER_CHOICES = (
    #     (0, 'Other'),
    #     (1, 'Male'),
    #     (2, 'Female'),
    # )
    # gender = models.PositiveSmallIntegerField(default=0, choices=GENDER_CHOICES, null=True, blank=True)
    # groups = models.ManyToManyField(Group, related_name='members')
    # user_permissions = models.ManyToManyField(Permission, related_name='members_permissions')
    #
    # def __str__(self) -> str:
    #     return self.username
