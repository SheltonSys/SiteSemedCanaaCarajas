
import os
from django.contrib.messages import constants as messages
from pathlib import Path




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


MAINTENANCE_MODE = False  # Altere para True durante a manutenção



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-zrvbu@igm3yi3k&l)8tt3=94!#tgo&1io_#s1=tl^apan#w=$0'

# Debug com variável de ambiente
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

# Hosts permitidos
ALLOWED_HOSTS = ["*","portal.semedcanaadoscarajas.pa.gov.br", "54.207.94.5", "127.0.0.1", "10.19.34.132"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'semedapp',
    'widget_tweaks',
    'django_otp',
    'django_otp.plugins.otp_totp',
    'django_otp.plugins.otp_static',  # ← ESSENCIAL para o pacote funcionar!

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',

    # Sessão e autenticação primeiro
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',

    # Autenticação antes da manutenção
    'django.contrib.auth.middleware.AuthenticationMiddleware',

    # Agora pode verificar request.user com segurança
    'semedweb.middlewares.maintenance_mode.MaintenanceModeMiddleware',

    # Demais middlewares personalizados
    'semedweb.middlewares.input_sanitization.InputSanitizationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'semedapp.middleware.AccessLogMiddleware',
]


ROOT_URLCONF = 'semedweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'semedapp.context_processors.pdde_status',
            ],
        },
    },
]


WSGI_APPLICATION = 'semedweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'siedge_db',
        'USER': 'siedge_user',
        'PASSWORD': '@Drik16091985',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'charset': 'utf8mb4',
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}





# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = '/media/'

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# settings.py
LOGIN_URL = 'login'  # URL para login
LOGIN_REDIRECT_URL = '/dashboardadmin/'  # Redirecionamento após login bem-sucedido
LOGOUT_REDIRECT_URL = 'login'  # Redirecionamento após logout

DEBUG = True

MESSAGE_TAGS = {
    messages.DEBUG: 'debug',
    messages.INFO: 'info',
    messages.SUCCESS: 'success',
    messages.WARNING: 'warning',
    messages.ERROR: 'danger',
}



# Certifique-se de configurar o backend da sessão
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_COOKIE_AGE = 1209600  # Duração da sessão (em segundos)


EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "shelton.oliveira.barbosa@gmail.com"  # Substitua pelo seu e-mail
EMAIL_HOST_PASSWORD = "nhiq aagp vxvx fzlo"  # Use a senha de aplicativo do Gmail
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


# settings.py

DATA_UPLOAD_MAX_NUMBER_FIELDS = 50000  # Aumente o valor conforme necessário


AUTH_USER_MODEL = 'semedapp.CustomUserProf'


SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = True  # se estiver usando HTTPS
CSRF_COOKIE_SECURE = True


