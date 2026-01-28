from allauth.socialaccount.models import SocialAccount


def line_status(request):
    is_line_user = False
    line_user_img = ""

    if request.user.is_authenticated:
        # 取得該使用者的 LINE 社交帳號資料
        social_acc = SocialAccount.objects.filter(user=request.user, provider='line').first()

        if social_acc:
            is_line_user = True
            # 從 extra_data 提取頭像網址 (LINE 預設欄位名稱為 pictureUrl)
            line_user_img = social_acc.extra_data.get('pictureUrl') or \
                            social_acc.extra_data.get('picture_url')

    return {
        'is_line_user': is_line_user,
        'LINE_USER_IMG': line_user_img,  # 這之後可以在模板中直接使用 {{ LINE_USER_IMG }}
    }