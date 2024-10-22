from contextlib import asynccontextmanager
from dataclasses import dataclass

import aiohttp
from miniopy_async import Minio

from config import MINIO_HOST, MINIO_PORT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY


@dataclass
class MinioClient:
    def __init__(self):
        self.host = MINIO_HOST
        self.port = MINIO_PORT
        self.access_key = MINIO_ACCESS_KEY
        self.secret_key = MINIO_SECRET_KEY

        self.minio: Minio
        self._get_minio_client()

    def _get_minio_client(self):
        self.minio = Minio(
            f'{self.host}:{self.port}',
            access_key=self.access_key,
            secret_key=self.secret_key,
            cert_check=False,
            secure=False
        )

    @asynccontextmanager
    async def get_connection(self):
        session = aiohttp.ClientSession(trust_env=True)
        try:
            yield session
        finally:
            await session.close()
