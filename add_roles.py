import asyncio
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import PG_USER, PG_PASSWORD, PG_AUTH_DB_NAME, PG_PORT, PG_HOST
from lib.app.database import async_session_maker
from lib.auth.model.models import Role

# Создание движка и сессии
# engine = create_engine(DATABASE_URL)
# Session = sessionmaker(bind=engine)
# session = Session()

# Добавление ролей
roles = [
    Role(name='user'),
    Role(name='clinic')
]


async def main():
    async with async_session_maker() as session:
        session.add_all(roles)
        await session.commit()

asyncio.run(main())

print("Roles added successfully.")
