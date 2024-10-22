from config import MINIO_BUCKET_NAME
from lib.media_service.client import MinioClient


class MinioStorage:
    client = MinioClient()
    minio = client.minio

    async def put_object(self, file_name, file_bytes, bytes_len):
        await self.minio.put_object(MINIO_BUCKET_NAME, file_name, file_bytes, bytes_len)
        file_url = await self.minio.get_presigned_url('GET', MINIO_BUCKET_NAME, file_name)
        return file_url

    async def delete(self, file_name):
        result = await self.minio.remove_object(bucket_name=MINIO_BUCKET_NAME, object_name=file_name)
        return result
