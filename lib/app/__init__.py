from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from lib.app.routing import AppRouting
from lib.auth.auth import auth_backend
from lib.auth.db.redis import redis_cli
from lib.auth.routes.user_router import FastUsers
from lib.auth.model.models import User
from lib.auth.manager import get_user_manager
from lib.logger.logger import get_logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:

    FastAPICache.init(RedisBackend(await redis_cli), prefix="cache")

    await FastAPILimiter.init(await redis_cli)

    yield


app = FastAPI(lifespan=lifespan,
              title="Auth",
              description="Register and authorize here")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


fast_users = FastUsers[User, int](
    get_user_manager,
    [auth_backend],
)


current_user = fastapi_users.current_user()

logger = get_logger()
app_routing = AppRouting(logger=logger, current_user=current_user)
