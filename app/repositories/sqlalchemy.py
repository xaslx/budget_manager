from app.repositories.base import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, delete, update, select
from sqlalchemy.exc import SQLAlchemyError
from dataclasses import dataclass
import logging


logger = logging.getLogger(__name__)




@dataclass
class SQLAlchemyRepository(BaseRepository):


    async def add(
        self,
        **data: dict,
    ):
        try:
            stmt = (
                insert(self.model)
                .values(**data)
                .returning(self.model.__table__.columns)
            )
            res = await self.session.execute(stmt)
            await self.session.commit()
            return res.mappings().one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.info('Ошибка при добавлении')


    async def find_one_or_none(
        self,
        **filter_by,
    ):
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return res.scalar_one_or_none()
        except (SQLAlchemyError, Exception) as e:
            logger.error('Ошибка при поиске')


    async def find_all(self, **filter_by):
        try:
            stmt = select(self.model).filter_by(**filter_by)
            res = await self.session.execute(stmt)
            return res.scalars().all()
        except (SQLAlchemyError, Exception) as e:
            logger.error('Ошибка при поиске всех значений')


    async def delete(self):
        ...