from .base import *

# --------------------------------------------------
# Development Settings
# --------------------------------------------------

DEBUG = env.bool("DEBUG", default=True)

ALLOWED_HOSTS = [
    "127.0.0.1",
    "localhost",
]