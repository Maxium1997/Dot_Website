from allauth.socialaccount.signals import social_account_added, social_account_updated
from django.dispatch import receiver


def _extract_display_name(extra_data):
    if not extra_data:
        return None
    return (
        extra_data.get('displayName')
        or extra_data.get('display_name')
        or extra_data.get('name')
    )


@receiver(social_account_added)
@receiver(social_account_updated)
def sync_line_display_name(sender, request, sociallogin, **kwargs):
    # LINE profile fields are stored in SocialAccount.extra_data
    display_name = _extract_display_name(getattr(sociallogin.account, 'extra_data', {}))
    if not display_name:
        return

    user = sociallogin.user
    if user.first_name != display_name:
        user.first_name = display_name
        user.save(update_fields=['first_name'])
