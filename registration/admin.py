from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MemberCreationForm, MemberChangeForm
from .models import Member


# Register your models here.

class MemberAdmin(UserAdmin):
    add_form = MemberCreationForm
    form = MemberChangeForm
    model = Member
    list_display = ["email", "username",]

admin.site.register(Member, MemberAdmin)