import asyncio
from miniopy_async import Minio
from miniopy_async.error import S3Error

from config import MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, MINIO_BUCKET_NAME

# Получение переменных окружения
minio_host = MINIO_HOST
minio_port = MINIO_PORT
minio_access_key = MINIO_ACCESS_KEY
minio_secret_key = MINIO_SECRET_KEY
minio_bucket_name = MINIO_BUCKET_NAME

# Создание клиента MinIO
client = Minio(
    f"{minio_host}:{minio_port}",
    access_key=minio_access_key,
    secret_key=minio_secret_key,
    secure=False
)


async def create_bucket():
    try:
        # Проверка существования бакета и его создание, если он не существует
        if not await client.bucket_exists(minio_bucket_name):
            await client.make_bucket(minio_bucket_name)
            print(f"Bucket '{minio_bucket_name}' created successfully.")
        else:
            print(f"Bucket '{minio_bucket_name}' already exists.")
    except S3Error as err:
        print(f"Error occurred: {err}")

if __name__ == "__main__":
    asyncio.run(create_bucket())
