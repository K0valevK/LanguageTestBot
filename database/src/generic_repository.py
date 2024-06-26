from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select


class GenericRepository:
    def __init__(self, db_engine, class_=AsyncSession):
        self._engine = db_engine
        self.async_session = sessionmaker(bind=db_engine, expire_on_commit=False)
        self._session: AsyncSession = self.async_session()
        
    async def save(self, entity):
        self._session.add(entity)
        await self._session.commit()

    async def delete(self, entity):
        await self._session.delete(entity)
        await self._session.commit()

    async def get_all(self, entity):
        return (await self._session.execute(select(entity))).scalars().all()

    async def get_one_by_expression(self, entity, where_clause):
        return (await self._session.execute(select(entity).where(where_clause))).scalars().one()

    async def get_all_by_expression(self, entity, where_clause):
        return (await self._session.execute(select(entity).where(where_clause))).scalars().all()
