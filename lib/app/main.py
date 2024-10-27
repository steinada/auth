import asyncio
import uvicorn

from config import API_PORT, API_HOST
from lib.app import fastapi_users, app, fast_users, app_routing, fastcli_users, fastapi_cli_users, current_clinic, \
    logger, current_user
from lib.app.utils.error_handlers import sqlalchemy_error_handler, server_error_handler
from lib.auth.auth import clinic_auth_backend, user_auth_backend
from lib.auth.model.schemas import UserRead, UserCreate, ClinicRead, ClinicCreate

app.include_router(
    fastapi_users.get_auth_router(user_auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastcli_users.get_auth_router(clinic_auth_backend),
    prefix="/clinic-auth/jwt",
    tags=["clinic-auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastcli_users.get_register_router(ClinicRead, ClinicCreate),
    prefix="/clinic-auth",
    tags=["clinic-auth"],
)

app.include_router(
    fast_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    fastcli_users.get_reset_password_router(),
    prefix="/clinic-auth",
    tags=["clinic-auth"],
)

app.include_router(
    fastapi_cli_users.get_reset_password_router(),
    prefix="/clinic-auth",
    tags=["clinic-auth"],
)

app.include_router(
    fastcli_users.get_custom_auth_router(current_clinic, logger),
    prefix="/clinic-auth",
    tags=["clinic-auth"],
)

app.include_router(
    fast_users.get_custom_auth_router(current_user, logger),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(
    app_routing.get_profile_router(),
    prefix="/profile",
    tags=["profile"],
)

app.include_router(
    app_routing.get_diary_router(),
    prefix="/diary",
    tags=["diary"],
)


app.add_exception_handler(Exception, sqlalchemy_error_handler)
app.add_exception_handler(500, server_error_handler)


def run_app():
    config = uvicorn.Config(app, port=API_PORT, host=API_HOST)
    server = uvicorn.Server(config)
    asyncio.new_event_loop().run_until_complete(server.serve())


if __name__ == '__main__':
    run_app()

    # проверить аус
    # проврить сурент юзер и сурент клиник



