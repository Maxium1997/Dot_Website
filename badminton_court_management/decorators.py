from functools import wraps
from django.core.exceptions import PermissionDenied
from .models import GymStaff


def require_active_gym_staff(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not GymStaff.objects.filter(user=request.user, is_active=True).exists():
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped
