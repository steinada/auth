from datetime import datetime
from typing import Type

from sqlalchemy import Select, update, select, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession

from lib.profile.db.protocols import PrP, PiP


class SQLAlchemyProfileDatabase:

    session: AsyncSession
    profile_table: Type[PrP]

    def __init__(
        self,
        session: AsyncSession,
        profile_table: Type[PrP],
    ):
        self.session = session
        self.profile_table = profile_table

    async def create(self, **create_dict):
        profile = self.profile_table(**create_dict)
        self.session.add(profile)
        await self.session.commit()
        await self.session.refresh(profile)
        return profile

    async def update(self, user_id, **params):
        query = (update(self.profile_table)
                 .where(self.profile_table.user_id == user_id)
                 .values(**params)
                 .returning(self.profile_table.id,
                            self.profile_table.user_id,
                            self.profile_table.sex,
                            self.profile_table.name,
                            self.profile_table.surname,
                            self.profile_table.date_of_birth,
                            self.profile_table.city))
        result = await self._get_profile(query)
        await self.session.commit()
        return result

    async def get_one(self, user_id: int):
        query = (select(self.profile_table)
                 .where(self.profile_table.user_id == user_id))
        return await self._get_profile(query)

    async def _get_profile(self, statement: Select):
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()


class SQLAlchemyPictureDatabase:

    session: AsyncSession
    picture_table: Type[PiP]

    def __init__(
        self,
        session: AsyncSession,
        picture_table: Type[PiP],
    ):
        self.session = session
        self.picture_table = picture_table

    async def add(self, user_id, master, picture_url, file_name):
        picture = self.picture_table(user_id=user_id,
                                     picture_url=picture_url,
                                     upload_date=datetime.now(),
                                     master=master,
                                     file_name=file_name)
        self.session.add(picture)
        await self.session.commit()
        await self.session.refresh(picture)
        return picture

    async def set_master(self, picture_id, user_id):
        query = (update(self.picture_table)
                 .where(and_(self.picture_table.user_id == user_id, self.picture_table.id == picture_id))
                 .values(master=True))
        results = await self.session.execute(query)
        await self.session.commit()
        return results

    async def unset_master(self, user_id):
        query = (update(self.picture_table)
                 .where(and_(self.picture_table.user_id == user_id, self.picture_table.master))
                 .values(master=False))
        results = await self.session.execute(query)
        await self.session.commit()
        return results

    async def get_many(self, user_id: int, page: int, limit: int):
        query = (select(self.picture_table)
                 .where(and_(self.picture_table.user_id == user_id, self.picture_table.master == False))
                 .offset(page*limit)
                 .limit(limit))
        results = await self.session.execute(query)
        return results.scalars().all()

    async def get_main(self, user_id: int):
        query = (select(self.picture_table)
                 .where(and_(self.picture_table.user_id == user_id, self.picture_table.master)))
        return await self._get_picture(query)

    async def delete(self, user_id: int, file_id: int):
        query = (delete(self.picture_table)
                 .where(and_(self.picture_table.user_id == user_id, self.picture_table.id == file_id))
                 .returning(self.picture_table.file_name))
        result = await self._get_picture(query)
        await self.session.commit()
        return result

    async def _get_picture(self, statement: Select):
        results = await self.session.execute(statement)
        return results.unique().scalar_one_or_none()

