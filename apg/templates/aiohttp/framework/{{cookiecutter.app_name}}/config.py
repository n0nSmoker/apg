import os
from pathlib import Path

from dotenv import load_dotenv


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)


DEBUG = int(os.getenv("DEBUG", '0'))
TEST = int(os.getenv("TEST", '0'))
SENTRY_DSN = os.getenv("SENTRY_DSN")

EXAMPLE_API_DOMAIN = os.getenv('EXAMPLE_POINT_API_DOMAIN', 'https://example-api.localhost/api')
{% if cookiecutter.use_database == 'y' %}
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB', '{{cookiecutter.app_name}}')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', '{{cookiecutter.app_name}}-db')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', '5432')
POSTGRES_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
{% endif %}