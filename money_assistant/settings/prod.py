import os

from .base import *

import dj_database_url

DATABASES["default"] = dj_database_url.config(os.environ.get("DB_URL"))

REDIS_URL = os.environ.get("REDIS_URL")

RQ_QUEUES = {
    "default": {"URL": REDIS_URL,},
}

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
