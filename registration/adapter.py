from allauth.socialaccount.adapter import DefaultSocialAccountAdapter


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        # 1. 先執行原本的存檔動作取得 user 物件
        user = super().save_user(request, sociallogin, form)

        # 2. 取得 LINE 提供的原始資料
        extra_data = sociallogin.account.extra_data
        print(f"DEBUG: LINE extra_data content: {extra_data}")  # 可以在後端 Log 查看抓到了什麼

        # 3. 嘗試多種可能的 Key (LINE 官方通常是 displayName)
        display_name = (
                extra_data.get('displayName') or
                extra_data.get('display_name') or
                extra_data.get('name')
        )

        if display_name:
            user.first_name = display_name
            # 如果您也想更新 last_name 或 username，可以在此處處理
            user.save()
            print(f"DEBUG: Successfully saved name: {display_name}")

        return user

    def populate_user(self, request, sociallogin, data):
        """
        在填充使用者資料時就先預設好名稱 (選用)
        """
        user = super().populate_user(request, sociallogin, data)
        display_name = sociallogin.account.extra_data.get('displayName')
        if display_name:
            user.first_name = display_name
        return user
