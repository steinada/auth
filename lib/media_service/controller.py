import io

from lib.media_service.storage import MinioStorage


class MinioManager:
    def __init__(self, logger):
        self.storage = MinioStorage()
        self.logger = logger

    async def put_object(self, file_bytes, file_name, bytes_len):
        file_bytes = io.BytesIO(file_bytes)
        file_url = await self.storage.put_object(file_name=file_name, file_bytes=file_bytes, bytes_len=bytes_len)
        return file_url

    async def delete(self, file_name):
        await self.storage.delete(file_name=file_name)
