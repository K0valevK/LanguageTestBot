from models import User as UserDBModel
from schemas import UserCreate as UserCreateDBSchema
from schemas import User as UserDBSchema
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(db: AsyncSession, user: UserCreateDBSchema):
    db_user = UserDBModel(**user.model_dump())

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def upd_user(db: AsyncSession, args: UserCreateDBSchema):
    db_user = await get_user_by_id(db, args.telegram_id)

    for key, value in vars(args).items():
        if value is None:
            continue
        if key == "telegram_id":
            continue
        if key == "username":
            setattr(db_user, key, value)
            continue
        if key == "max_unlimited_score":
            setattr(db_user, key, max(value, db_user.max_unlimited_score))
            continue
        setattr(db_user, key, getattr(db_user, key) + value)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def get_user_from_fk(db: AsyncSession, id: int):
    result = await db.execute(select(UserDBModel).where(UserDBModel.id == id))
    return result.scalars().one_or_none()


async def get_user_by_id(db: AsyncSession, telegram_id: int):
    result = await db.execute(select(UserDBModel).where(UserDBModel.telegram_id == telegram_id))
    return result.scalars().one_or_none()


async def get_user_by_name(db: AsyncSession, username: str):
    result = await db.execute(select(UserDBModel).where(UserDBModel.username == username))
    return result.scalars().one_or_none()
