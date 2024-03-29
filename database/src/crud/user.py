from models import User as UserDBModel
from schemas import UserCreate as UserCreateDBSchema
from schemas import User as UserDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreateDBSchema):
    db_user = UserDBModel(**user.model_dump())

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def upd_user(db: AsyncSession, user: UserDBModel):
    for key, value in vars(user):
        if key == "telegram_id":
            continue
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)

    return user


async def get_user_by_id(db: AsyncSession, telegram_id: int):
    result = await db.execute(select(UserDBModel).where(UserDBModel.telegram_id == telegram_id))
    return result.scalars().one_or_none()
