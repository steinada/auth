from dotenv import load_dotenv
import os

load_dotenv()

MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY")
MINIO_HOST = os.environ.get("MINIO_HOST")
MINIO_PORT = os.environ.get("MINIO_PORT")
MINIO_BUCKET_NAME = os.environ.get("MINIO_BUCKET_NAME")

PG_HOST = os.environ.get("PG_HOST")
PG_PORT = int(os.environ.get("PG_PORT"))
PG_AUTH_DB_NAME = os.environ.get("PG_AUTH_DB_NAME")
PG_USER = os.environ.get("PG_USER")
PG_PASSWORD = os.environ.get("PG_PASSWORD")

API_PORT = int(os.environ.get("API_PORT"))
API_HOST = os.environ.get("API_HOST")

USER_AUTH_SECRET = os.environ.get("USER_AUTH_SECRET")
CLINIC_AUTH_SECRET = os.environ.get("CLINIC_AUTH_SECRET")

EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")

APP_NAME = os.environ.get("APP_NAME")

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = int(os.environ.get("REDIS_PORT"))
REDIS_URL = os.environ.get("REDIS_URL")

LOGGING_LEVEL = os.environ.get("LOGGING_LEVEL")

SECRET_CSRF = os.environ.get("SECRET_CSRF")

