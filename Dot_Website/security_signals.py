"""
Security audit signals — NIST DE.CM-1 / ISO A.12.4.1.
Log authentication success/failure for audit trail (Zero Trust: verify & log).
Import this module at startup (e.g. in ROOT_URLCONF) so handlers are registered.
"""
import logging
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

logger = logging.getLogger('security')


def log_user_logged_in(sender, request, user, **kwargs):
    logger.info(
        'login_success user=%s ip=%s',
        user.get_username(),
        request.META.get('REMOTE_ADDR', ''),
    )


def log_user_logged_out(sender, request, user, **kwargs):
    if user:
        logger.info(
            'logout user=%s ip=%s',
            user.get_username(),
            request.META.get('REMOTE_ADDR', ''),
        )


def log_login_failed(sender, credentials, request, **kwargs):
    logger.warning(
        'login_failed identifier=%s ip=%s',
        credentials.get('username', credentials.get('email', '')),
        request.META.get('REMOTE_ADDR', '') if request else '',
    )


user_logged_in.connect(log_user_logged_in)
user_logged_out.connect(log_user_logged_out)
user_login_failed.connect(log_login_failed)
