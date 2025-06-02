import os
from decouple import config


## Django settings for saas_project project.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


## Secret key
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "sumit",
)
STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")


# Base settings
DEBUG = True
USE_TZ = True
USE_I18N = True
TIME_ZONE = "UTC"
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Kolkata"
AUTH_USER_MODEL = "app.User"


##
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")


##
ROOT_URLCONF = "saas_project.urls"
WSGI_APPLICATION = "saas_project.wsgi.application"


## Accept request from any host
ALLOWED_HOSTS = ["*"]


## Django App
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "app",
]


## Middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


## Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


## Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config(
            "DB_NAME",
            default="saas_db",
        ),
        "USER": config(
            "DB_USER",
            default="postgres",
        ),
        "PASSWORD": config(
            "DB_PASSWORD",
            default="postgres",
        ),
        "HOST": config(
            "DB_HOST",
            default="saas_db",
        ),
        "PORT": config(
            "DB_PORT",
            default=5432,
        ),
    }
}


# REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
}


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
