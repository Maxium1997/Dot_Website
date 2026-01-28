from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        if sociallogin.account.provider == 'line':
            # LINE 暱稱通常存在 extra_data 的 display_name 或 displayName
            extra_data = sociallogin.account.extra_data
            display_name = extra_data.get('display_name') or extra_data.get('displayName')
            if display_name:
                user.first_name = display_name
                user.save()     # 存入資料庫，避免 500 錯誤
        return user
