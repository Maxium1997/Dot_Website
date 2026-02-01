from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

# Create your models here.


class Member(AbstractUser):
    pass

    @property
    def get_display_name(self):
        # 優先回傳 first_name，若無則回傳 username，但在 LINE 登入情境下建議邏輯如下：
        if self.first_name:
            return self.first_name
        return "使用者"

    def __str__(self):
        # 讓系統優先顯示姓名，如果沒有姓名才顯示 ID
        return self.first_name if self.first_name else self.username
