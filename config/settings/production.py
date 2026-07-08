from .base import *

# --------------------------------------------------
# Production Settings
# --------------------------------------------------

DEBUG = False

ALLOWED_HOSTS = [
    # 나중에 서버 배포 시 추가
    # "kwr010212.duckdns.org",
    # "your-domain.com",
]

# --------------------------------------------------
# Security (추후 Beta 버전에서 추가)
# --------------------------------------------------

# CSRF, HTTPS, SecurityMiddleware 관련 설정은
# 서버 배포 단계에서 적용할 예정