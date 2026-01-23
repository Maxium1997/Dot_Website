# registration/adapter.py
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        # 取得 LINE 傳回的資料
        if sociallogin.account.provider == 'line':
            display_name = sociallogin.account.extra_data.get('display_name')
            if display_name:
                # 自動將 LINE 暱稱存入 Member 模型的 first_name 欄位
                user = sociallogin.user
                user.first_name = display_name
