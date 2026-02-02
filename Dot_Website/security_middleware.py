"""
Security audit middleware — NIST DE.CM-1 / ISO 27001 A.12.4.1.
Logs authentication and authorization events for audit trail (Zero Trust: verify & log).
"""
import logging
import time

logger = logging.getLogger('security')


class SecurityAuditMiddleware:
    """
    Logs security-relevant events: login attempts, logout, and access to protected views.
    Place after AuthenticationMiddleware so request.user is available.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Log access to sensitive paths (NIST DE.CM-1 audit trail)
        if getattr(request, 'user', None) and request.user.is_authenticated:
            path = request.path.rstrip('/')
            sensitive_prefixes = (
                '/admin',
                '/accounts/logout',
                '/badminton_court_management/api/create-booking',
                '/coast_guard_mart/checkout',
                '/coast_guard_mart/staff',
            )
            if any(path == p or path.startswith(p + '/') for p in sensitive_prefixes):
                logger.info(
                    'auth_access user=%s path=%s method=%s',
                    request.user.get_username(),
                    request.path,
                    request.method,
                )
        return response


class SecurityHeadersMiddleware:
    """
    Add security headers aligned with NIST PR.DS-5 / ISO A.12.1.2.
    Complements Django's SecurityMiddleware (Referrer-Policy set via SECURE_REFERRER_POLICY).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.get('X-Frame-Options') is None:
            response['X-Frame-Options'] = 'DENY'
        response.setdefault('Permissions-Policy', 'geolocation=(), microphone=(), camera=()')
        return response
