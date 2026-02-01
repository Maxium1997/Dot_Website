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
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'csp.middleware.CSPMiddleware',     # For Content Security Policy (CSP) Header Not Set, 沒有設定 CSP
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

# 信任的網域來源，用於 CSRF 驗證
CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
    'https://*.ngrok.io',
    'https://DotWebsiteOfficial.pythonanywhere.com',
    'https://*.railway.app'
]

# 辨識 Proxy 轉發的 HTTPS 狀態
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
USE_X_FORWARDED_HOST = True
USE_X_FORWARDED_PORT = True

# For Content Security Policy (CSP) Header Not Set, 沒有設定 CSP
SECURE_CONTENT_TYPE_NOSNIFF = True

CONTENT_SECURITY_POLICY = {
    "DIRECTIVES": {
        "default-src": ("'self'",),
        "script-src": ("'self'", "https://cdn.jsdelivr.net"),
        "style-src": ("'self'", "https://fonts.googleapis.com"),
        "font-src": ("'self'", "https://fonts.gstatic.com"),
    }
}

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
