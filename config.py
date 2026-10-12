import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WEDDING_PASSWORD_HASH = os.environ.get('WEDDING_PASSWORD_HASH')
    WEDDING_DATA_FILE = os.environ.get('WEDDING_DATA_FILE')
    PERMANENT_SESSION_LIFETIME = timedelta(days=14)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('COOKIE_SECURE', '0') == '1'
    MAX_CONTENT_LENGTH = 1 * 1024 * 1024


class DevConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///local.db'


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'

    @classmethod
    def validate(cls):
        missing = [name for name in ('SECRET_KEY', 'DATABASE_URL', 'WEDDING_PASSWORD_HASH') if not os.environ.get(name)]
        if missing:
            raise RuntimeError(f"Missing required production environment variables: {', '.join(missing)}")
