import os
import dj_database_url

db_from_env = dj_database_url.config(
    conn_max_age=500,
    ssl_require=os.getenv("DATABASE_SSL", False),
)
DATABASES = {"default": db_from_env}

INSTALLED_APPS = (
    "django.contrib.contenttypes",
    "django.contrib.staticfiles",
    "django.contrib.auth",
    "django_filters",
    "tests",
)

MIDDLEWARE = []

ROOT_URLCONF = "tests.urls"

USE_TZ = True

TIME_ZONE = "UTC"

SECRET_KEY = "foobar"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
    }
]
