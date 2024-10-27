from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_limiter import FastAPILimiter

from fastapi import FastAPI
from fastapi_users import FastAPIUsers

from lib.app.routing import UserRouting
from lib.auth.auth import user_auth_backend, clinic_auth_backend
from lib.auth.db.redis import redis_cli
# from lib.auth.routes.clinic_router import FastCliUsers
from lib.auth.routes.user_router import FastUsers
from lib.auth.model.models import User, Clinic
from lib.auth.controller import get_user_manager, get_clinic_manager
from lib.logger.logger import get_logger


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:

    FastAPICache.init(RedisBackend(await redis_cli), prefix="cache")

    await FastAPILimiter.init(await redis_cli)

    yield


app = FastAPI(lifespan=lifespan,
              title="Auth",
              description="Register and authorize here")

logger = get_logger()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [user_auth_backend],
)


fast_users = FastUsers[User, int](
    get_user_manager,
    [user_auth_backend],
)

fastapi_cli_users = FastAPIUsers[Clinic, int](
    get_clinic_manager,
    [clinic_auth_backend],
)

fastcli_users = FastUsers[Clinic, int](
    get_clinic_manager,
    [clinic_auth_backend],
)

current_user = fastapi_users.current_user()
current_clinic = fastapi_cli_users.current_user()


app_routing = UserRouting(logger=logger, current_user=current_user)
