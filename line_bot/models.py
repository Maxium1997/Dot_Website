from django.db import models

# Create your models here.


class UserInfo(models.Model):
    uid = models.CharField(max_length=50, null=False, default='')               # user_id
    name = models.CharField(max_length=255, blank=True, null=False)             # LINE名字
    pic_url = models.CharField(max_length=255, null=False)                      # 大頭貼網址
    message_text = models.CharField(max_length=255, blank=True, null=False)     # 文字訊息紀錄
    message_created_dt = models.DateTimeField(auto_now=True)                    # 物件儲存的日期時間

    def __str__(self):
        return self.uid
