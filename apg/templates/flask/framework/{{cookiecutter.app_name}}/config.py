import os

SESSION_COOKIE_NAME = 'session'
SESSION_COOKIE_PATH = '/'
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
UPLOAD_DIR = 'static/upload'

SENTRY_DSN = os.environ.get("SENTRY_DSN")

{% if cookiecutter.use_celery == 'y' -%}
CELERY_RESULT_BACKEND = 'redis://'
RABBITMQ_DEFAULT_USER = os.environ.get("RABBITMQ_DEFAULT_USER")
RABBITMQ_DEFAULT_PASS = os.environ.get("RABBITMQ_DEFAULT_PASS")
RABBITMQ_HOST = os.environ.get("RABBITMQ_HOST")
RABBITMQ_PORT = os.environ.get("RABBITMQ_PORT")
BROKER_URL = f'pyamqp://{RABBITMQ_DEFAULT_USER}:{RABBITMQ_DEFAULT_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//'
{% endif -%}

POSTGRES_USER = os.environ.get("POSTGRES_USER", 'postgres')
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", 'hg56LK76h0')
POSTGRES_DB = os.environ.get("POSTGRES_DB", '{{cookiecutter.app_name}}')
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", '{{cookiecutter.app_name}}-db')
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", '5432')
DATABASE_URL = f'{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{DATABASE_URL}'

SECRET_KEY = os.environ.get("SECRET_KEY")

SERVER_NAME = os.environ.get("SERVER_NAME")

{% if cookiecutter.use_mail == 'y' -%}
MAIL_SERVER = os.environ.get("MAIL_SERVER", 'localhost')
MAIL_PORT = os.environ.get("MAIL_PORT", 25)
MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", False)
MAIL_USE_SSL = os.environ.get("MAIL_USE_SSL", False)
MAIL_USERNAME = os.environ.get("MAIL_USERNAME", None)
MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", None)
MAIL_DEBUG = os.environ.get("MAIL_DEBUG", True)
{% endif -%}

{% if cookiecutter.use_jwt_authorization == 'y' -%}
JWT_EXPIRE_HOURS = os.environ.get('JWT_EXPIRE_HOURS', 8)
JWT_ISSUER = os.environ.get('JWT_ISSUER', 'jwt_auth')
JWT_KEY = os.environ.get('JWT_KEY', 'jwt_auth_secret_key')
JWT_ALGORITHM = os.environ.get('JWT_ALGORITHM', 'HS256')
JWT_COOKIE_NAME = os.environ.get('JWT_COOKIE_NAME', 'JAT')
JWT_HEADER_NAME = os.environ.get('JWT_HEADER_NAME', 'X-Auth-Token')
PASSWORD_SALT = os.environ.get('PASSWORD_SALT', 'app_pwd_salt)(*&^%$#@!')
{% endif -%}