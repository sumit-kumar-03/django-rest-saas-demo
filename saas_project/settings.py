import os
from decouple import config


## Django settings for saas_project project.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


## Secret key
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "sumit",
)


## Base settings
DEBUG = os.getenv(
    "DEBUG",
    True,
)
USE_TZ = os.getenv(
    "USE_TZ",
    True,
)
USE_I18N = os.getenv(
    "USE_I18N",
    True,
)
TIME_ZONE = os.getenv(
    "TIME_ZONE",
    "UTC",
)
LANGUAGE_CODE = os.getenv(
    "LANGUAGE_CODE",
    "en-us",
)
TIME_ZONE = os.getenv(
    "TIME_ZONE",
    "Asia/Kolkata",
)


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
    "saas_project.app",
]


## Middleware
MIDDLEWARE = [
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
    "saas_project.app.middlewares.auth.CustomRequestMiddleware",
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


## Celery settings
BROKER_URL = "{schema}://{username}:{password}@{host}:{port}//".format(
    schema=os.getenv(
        "RABBITMQ_SCHEMA",
        "amqp",
    ),
    username=os.getenv(
        "RABBITMQ_USERNAME",
        "guest",
    ),
    password=os.getenv(
        "RABBITMQ_PASSWORD",
        "guest",
    ),
    host=os.getenv(
        "RABBITMQ_HOST",
        "rabbitmq",
    ),
    port=os.getenv(
        "RABBITMQ_PORT",
        5672,
    ),
)


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


## Rest Framework
REST_FRAMEWORK = {
    "PAGE_SIZE": 50,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
}
