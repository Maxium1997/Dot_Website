from allauth.socialaccount.models import SocialAccount


def line_status(request):
    is_line_user = False
    if request.user.is_authenticated:
        is_line_user = SocialAccount.objects.filter(user=request.user, provider='line').exists()
    return {'is_line_user': is_line_user}
