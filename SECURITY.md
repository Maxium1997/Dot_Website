# Security & Compliance Overview

This project aligns with **NIST Cybersecurity Framework**, **ISO/IEC 27001**, and **Zero Trust** principles where applicable to a Django web application.

---

## 1. NIST Cybersecurity Framework Mapping

| NIST Function | Control / Practice | Implementation in This Project |
|---------------|--------------------|--------------------------------|
| **Identify (ID)** | Asset management, risk assessment | `SECRET_KEY` and secrets from env; `ALLOWED_HOSTS`; no hardcoded credentials. |
| **Protect (PR)** | Access control (PR.AC-1) | `AUTH_PASSWORD_VALIDATORS`, `login_required` / `user_passes_test` on sensitive views; `LOGIN_URL`. |
| | Data security (PR.DS-5) | HTTPS-only cookies in production; HSTS; `SECURE_CONTENT_TYPE_NOSNIFF`; CSP; `X-Frame-Options`; `Referrer-Policy`. |
| | Secure config (PR.IP-1) | `DEBUG` from env; `SECURE_SSL_REDIRECT`; `SECURE_PROXY_SSL_HEADER`. |
| **Detect (DE)** | Monitoring (DE.CM-1) | Security audit logging: `Dot_Website.security_middleware.SecurityAuditMiddleware`, `Dot_Website.security_signals` (login/logout/failure); logs under `logs/security.log`. |
| **Respond (RS)** | Response planning | Logs and audit trail support incident response; ensure `logs/` is retained and reviewed. |
| **Recover (RC)** | Recovery planning | Session and DB-backed design; backups and recovery are operational/deployment responsibilities. |

---

## 2. ISO/IEC 27001 Mapping (Selected Controls)

| ISO 27001 Control | Description | Implementation |
|-------------------|-------------|----------------|
| **A.9.4.1** | Information access restriction | Django auth, `login_required`, role checks (`user_passes_test`, `staff_member_required`) on admin and staff views. |
| **A.9.4.2** | Secure log-on | Password validators; session timeout (`SESSION_COOKIE_AGE`); `SESSION_EXPIRE_AT_BROWSER_CLOSE`; HTTPS-only session/CSRF cookies in production. |
| **A.9.4.3** | Password management | `AUTH_PASSWORD_VALIDATORS`: minimum length, common password check, numeric-only check, similarity to user attributes. |
| **A.10.1.1** | Cryptographic controls | TLS in production; secure and HttpOnly cookies; no sensitive data in client-side storage by design. |
| **A.12.1.2** | Operational procedures / change management | Security headers (CSP, X-Frame-Options, Referrer-Policy, Permissions-Policy) applied consistently. |
| **A.12.4.1** | Event logging | Security logger `security`; file handler to `logs/security.log`; login success/failure and access to sensitive paths logged. |
| **A.12.6.1** | Technical vulnerability management | Use supported Django version and dependencies; keep `requirements.txt` and deployments updated. |
| **A.13.1.1** | Network controls | `ALLOWED_HOSTS`; HTTPS and HSTS in production; CSP to restrict script/source origins. |

---

## 3. Zero Trust Alignment

| Principle | Application |
|-----------|-------------|
| **Never trust, always verify** | Every sensitive view requires authentication (`@login_required`); staff/admin views use `user_passes_test` / `staff_member_required`. |
| **Explicit verification** | Session is DB-backed and timeout-based; `SESSION_SAVE_EVERY_REQUEST` refreshes expiry on activity; CSRF on forms and APIs. |
| **Least privilege** | Role-based access (e.g. staff-only dashboards); no blanket trust of network. |
| **Assume breach / minimize blast radius** | Security audit log for login/logout and access to sensitive paths; logs support detection and response. |

---

## 4. Implemented Security Controls Summary

- **Secrets**: `SECRET_KEY` and API keys from environment (e.g. `.env`), not hardcoded.
- **HTTPS**: In production (`DEBUG=False`): secure cookies, HSTS, optional `SECURE_SSL_REDIRECT` via env.
- **Cookies**: `HttpOnly` and `Secure` for session and CSRF in production.
- **Sessions**: 2-hour idle timeout; expire at browser close; DB-backed; refresh on each request.
- **Passwords**: Django validators (length ≥10, common password, numeric-only, similarity).
- **Headers**: CSP, `X-Frame-Options`, `X-Content-Type-Options`, `Referrer-Policy`, `Permissions-Policy`.
- **CSRF**: Enabled globally; `CSRF_TRUSTED_ORIGINS` for allowed origins (set explicitly; add ngrok/other domains via `CSRF_TRUSTED_ORIGINS` env as needed).
- **Audit**: Security logger writes to `logs/security.log`; login success/failure and access to admin, logout, booking API, checkout, staff area are logged.

---

## 5. Deployment Checklist

- [ ] Set `DEBUG=False` and use a strong `SECRET_KEY`.
- [ ] Configure `ALLOWED_HOSTS` and `CSRF_TRUSTED_ORIGINS` for your domain(s).
- [ ] Enable HTTPS and set `SECURE_SSL_REDIRECT=True` if using a reverse proxy.
- [ ] Ensure `logs/` exists and is writable; retain and rotate `security.log` for audit.
- [ ] Restrict read access to `.env` and any secret files.
- [ ] Keep Django and dependencies updated; review release notes for security fixes.

---

## 6. Security Log Location

- **File**: `logs/security.log` (created automatically at startup).
- **Events**: `login_success`, `login_failed`, `logout`, `auth_access` (sensitive paths).
- **Format**: `[timestamp] LEVEL logger message` (e.g. user, IP, path). Use for audit and incident response.
