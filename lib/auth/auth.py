from fastapi_users.authentication import CookieTransport, JWTStrategy, AuthenticationBackend

from config import USER_AUTH_SECRET, CLINIC_AUTH_SECRET

user_cookie_transport = CookieTransport(cookie_max_age=3600000)
clinic_cookie_transport = CookieTransport(cookie_max_age=3600000)


def get_user_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=USER_AUTH_SECRET, lifetime_seconds=3600000)


def get_clinic_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=CLINIC_AUTH_SECRET, lifetime_seconds=3600000)


user_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=user_cookie_transport,
    get_strategy=get_user_jwt_strategy,
)

clinic_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=clinic_cookie_transport,
    get_strategy=get_clinic_jwt_strategy,
)
