import os

from .base import *

import dj_database_url

DATABASE_URL = os.environ.get("DATABASE_URL")

DATABASES["default"] = dj_database_url.config()

REDIS_URL = os.environ.get("REDIS_URL")

RQ_QUEUES = {
    "default": {"URL": REDIS_URL},
}

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

ALLOWED_HOSTS = ["*"]

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static")
