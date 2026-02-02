import os
from pathlib import Path
import dj_database_url
from dotenv import load_dotenv

# 加載環境變數
load_dotenv(encoding="utf-8")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- 基礎安全設定 ---

# 從 .env 讀取 SECRET_KEY，不再硬編碼
SECRET_KEY = os.getenv('SECRET_KEY')

# 從 .env 控制 DEBUG 模式，生產環境應為 False
DEBUG = os.getenv('DEBUG', 'False') == 'True'

# 強化 ALLOWED_HOSTS 解析邏輯，自動過濾掉空格與空值
raw_hosts = os.getenv('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = [host.strip() for host in raw_hosts.split(',') if host.strip()]
# 如果解析後為空，則預設本地端
if not ALLOWED_HOSTS:
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# --- LINE 與 API 設定 ---

CHANNEL_SECRET = os.getenv('CHANNEL_SECRET')
CHANNEL_ACCESS_TOKEN = os.getenv('CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
LINE_CHANNEL_SECRET = os.getenv('LINE_CHANNEL_SECRET')
LINE_LIFF_ID = os.getenv('LINE_LIFF_ID')
YOUTUBE_DATA_API_KEY = os.getenv('YOUTUBE_DATA_API_KEY')

# --- 應用程式定義 ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'import_export',
    'qrcode',

    # Content Security Policy (CSP) Header Not Set, 沒有設定 CSP
    'csp',

    # Allauth 核心
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.line',

    'ckeditor',
    'registration',
    'website',
    'organization',
    'business',
    'market_place',
    'coast_guard_mart',
    'playground',
    'line_bot',
    'badminton_court_management',
]

SITE_ID = 1
AUTH_USER_MODEL = 'registration.Member'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # 靜態檔案處理
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',    # CSRF 防護核心
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'Dot_Website.security_middleware.SecurityAuditMiddleware',   # NIST/ISO 稽核日誌
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',     # CSP
    'Dot_Website.security_middleware.SecurityHeadersMiddleware',  # 安全標頭
]

ROOT_URLCONF = 'Dot_Website.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'line_bot.context_processors.line_status',
            ],
        },
    },
]

WSGI_APPLICATION = 'Dot_Website.wsgi.application'

# --- 資料庫設定 ---

DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600
    )
}

# --- 生產環境安全強化 (當 DEBUG = False 時) ---

if not DEBUG:
    # 確保 Cookie 僅透過 HTTPS 傳輸
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SECURE = True

    # 防止 JS 讀取敏感 Cookie
    CSRF_COOKIE_HTTPONLY = True
    SESSION_COOKIE_HTTPONLY = True

    # 強制 HTTPS 導向與 HSTS
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # 增加環境變數判斷，讓您能靈活開啟/關閉跳轉
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'False') == 'True'
else:
    # DEBUG 為 True 時，務必關閉強制跳轉，否則本地 runserver 會無法開啟
    SECURE_SSL_REDIRECT = False

# 信任的網域來源，用於 CSRF 驗證（Django 不支援萬用字元，請依部署網域新增）
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
    'https://DotWebsiteOfficial.pythonanywhere.com',
    'https://*.railway.app',
]
# 可從環境變數追加，例如：CSRF_TRUSTED_ORIGINS += os.getenv('CSRF_ORIGINS', '').split(',')
_extra_csrf = os.getenv('CSRF_TRUSTED_ORIGINS', '')
if _extra_csrf:
    CSRF_TRUSTED_ORIGINS.extend(origin.strip() for origin in _extra_csrf.split(',') if origin.strip())

# 辨識 Proxy 轉發的 HTTPS 狀態
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# For Content Security Policy (CSP) Header Not Set, 沒有設定 CSP
SECURE_CONTENT_TYPE_NOSNIFF = True

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": (
            "'self'",
            "'unsafe-inline'",
            "https://api.line.me",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
            "https://static.line-scdn.net",
        ),
        "style-src": (
            "'self'",
            "'unsafe-inline'",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
        ),
        "font-src": (
            "'self'",
            "https://fonts.gstatic.com",
            "https://cdn.jsdelivr.net",
            "https://cdnjs.cloudflare.com",
        ),
        "img-src": (
            "'self'",
            "data:",
            "https://web-production-ecc7b.up.railway.app",
            "https://profile.line-scdn.net",
            "https://cdn-icons-png.flaticon.com",
            "https://profile.line-scdn.net",    # 允許 LINE 使用者頭像
            "https://*.railway.app",    # 允許圖片在其他 Railway 服務
        ),
    }
}

# --- NIST / ISO 27001 / Zero Trust 對齊設定 ---

# NIST PR.AC-1, ISO A.9.4.1: 身份與存取管理 — 密碼原則
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 10}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Zero Trust / ISO A.9.4.2: 工作階段安全 — 限時、重啟後失效、僅 HTTPS
SESSION_COOKIE_AGE = 60 * 60 * 2  # 2 小時
SESSION_SAVE_EVERY_REQUEST = True  # 每次請求更新過期時間
SESSION_EXPIRE_AT_BROWSER_CLOSE = True  # 關閉瀏覽器即過期
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # 明確使用 DB 儲存，利於稽核

# Zero Trust: 明確驗證 — 登入網址保護
LOGIN_URL = '/accounts/login/'

# 確保稽核日誌目錄存在
_LOGS_DIR = os.path.join(BASE_DIR, 'logs')
os.makedirs(_LOGS_DIR, exist_ok=True)

# NIST DE.CM-1 / ISO A.12.4.1: 安全稽核與日誌
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'security': {
            'format': '[%(asctime)s] %(levelname)s %(name)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S',
        },
    },
    'handlers': {
        'security_file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs', 'security.log'),
            'formatter': 'security',
        },
        'security_console': {
            'level': 'WARNING',
            'class': 'logging.StreamHandler',
            'formatter': 'security',
        },
    },
    'loggers': {
        'security': {
            'handlers': ['security_file', 'security_console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# 安全標頭（NIST PR.DS-5 / ISO A.12.1.2）
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'

# --- 其他設定 ---

TIME_ZONE = 'Asia/Taipei'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Allauth & LINE 設定
SOCIALACCOUNT_PROVIDERS = {
    'line': {
        'SCOPE': ['profile', 'openid'],
    }
}
# 必須確保路徑完全正確（應用程式名稱.檔案名稱.類別名稱），以LINE登入後執行
SOCIALACCOUNT_ADAPTER = 'registration.adapter.MySocialAccountAdapter'
# 當使用者透過 LINE 登入時，自動將資料填充到 User Model
SOCIALACCOUNT_QUERY_EMAIL = True
SOCIALACCOUNT_AUTO_SIGNUP = True

# 讓 Django 在 Social Login 時自動更新欄位
SOCIALACCOUNT_FORMS = {
    'signup': 'allauth.socialaccount.forms.SignupForm',
}
# 登入後要跳轉的 URL (例如首頁或預約頁面)
LOGIN_REDIRECT_URL = '/'

# 如果需要，也可以設定登出後的跳轉 URL
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_AUTO_SIGNUP = True
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'
