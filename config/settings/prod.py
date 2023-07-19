from .base import *

ALLOWED_HOSTS = ["*"]
DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": env("DBNAME"),
        "USER": env("USER"),
        "PASSWORD": env("PASSWORD"),
        "HOST": env("HOST"),
        "PORT": env("PORT"),
        "OPTIONS": {"autocommit": True, "charset": "utf8mb4"},
    }
}
