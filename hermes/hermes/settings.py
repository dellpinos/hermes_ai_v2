from pathlib import Path
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: secret!
SECRET_KEY = config("APP_SECRET_KEY", default='default-secret-key')

# SECURITY WARNING
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost', cast=lambda v: v.split(','))

CSRF_TRUSTED_ORIGINS = config('CSRF_TRUSTED_ORIGINS', default='http://localhost:5173', cast=lambda v: v.split(','))

PASSWORD_RESET_TIMEOUT = 86400  # 1 day

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'api',
    'llm',
    'chat',
    "django_vite"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hermes.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'hermes' / 'templates',  # Global project's templates
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hermes.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE'),
        'NAME': config('DB_DATABASE'),
        'USER': config('DB_USERNAME'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', cast=int)
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Auth redirections
LOGIN_URL = '/auth/login/'
LOGIN_REDIRECT_URL = '/chat/'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/' # Este es parte del SRC en las etiquetas HTML tanto en dev como con el build

# Production
STATIC_ROOT = BASE_DIR / '../staticfiles'

# Static files, this changes becaouse in dev there aren't "dist"
if config('DJANGO_VITE_DEV_MODE', default=True, cast=bool):

    STATICFILES_DIRS = [
        BASE_DIR / "frontend/static/src",  # Assets before build
    ]

else:
    STATICFILES_DIRS = [
        BASE_DIR / 'frontend/static/dist/.vite',
        BASE_DIR / "frontend/static/dist",  # Assets before build
    ]
    
# Route to manifest.json in STATIC_ROOT
DJANGO_VITE = {
    'default': {
        "dev_mode": config('DJANGO_VITE_DEV_MODE', default=True, cast=bool),
        'manifest_path': BASE_DIR / 'staticfiles' / 'manifest.json',
        'dev_server_port': 3000

    }
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')

EMAIL_HOST = config('EMAIL_HOST', default='sandbox.smtp.mailtrap.io')
EMAIL_PORT = config('EMAIL_PORT', default=255, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='test@test.com')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='1234')