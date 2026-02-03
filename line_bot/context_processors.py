from allauth.socialaccount.models import SocialAccount
from django.db.utils import OperationalError, ProgrammingError


def line_status(request):
    """
    Safe context processor for LINE user status.

    原則：
    - 未登入直接回預設值
    - ORM 查詢必須 try/except
    - 任何失敗都不能影響 page render
    """

    is_line_user = False
    line_user_img = ""

    # 未登入，直接回預設值（最重要）
    if not getattr(request, "user", None) or not request.user.is_authenticated:
        return {
            "is_line_user": False,
            "LINE_USER_IMG": "",
        }

    try:
        social_acc = (
            SocialAccount.objects
            .filter(user=request.user, provider="line")
            .only("extra_data")
            .first()
        )

        if social_acc and isinstance(social_acc.extra_data, dict):
            is_line_user = True
            line_user_img = (
                social_acc.extra_data.get("pictureUrl")
                or social_acc.extra_data.get("picture_url")
                or ""
            )

    except (OperationalError, ProgrammingError):
        # DB 尚未 ready / migration 尚未完成
        # 在 context processor 中一定要吞掉
        pass
    except Exception:
        # 保守：任何非預期錯誤都不能讓頁面 500
        pass

    return {
        "is_line_user": is_line_user,
        "LINE_USER_IMG": line_user_img,
    }
