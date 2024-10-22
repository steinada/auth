from redis.asyncio.utils import from_url

from config import REDIS_HOST, REDIS_PORT


redis_cli = from_url(f"redis://{REDIS_HOST}:{REDIS_PORT}", decode_responses=True)


async def get_redis_generator():
    try:
        yield redis_cli
    finally:
        await redis_cli.close()
