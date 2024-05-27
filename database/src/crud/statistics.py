from models import Statistics as StatisticsDBModel
from schemas import StatisticsCreate as StatisticsCreateDBSchema
from schemas import Statistics as StatisticsDBSchema
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession


async def create_statistic(db: AsyncSession, statistic: StatisticsCreateDBSchema):
    db_statistic = StatisticsDBModel(**statistic.model_dump())

    db.add(db_statistic)
    await db.commit()
    await db.refresh(db_statistic)

    return db_statistic


async def upd_statistic(db: AsyncSession, args: StatisticsCreateDBSchema):
    db_statistic = await get_statistic_by_user_id(db, args.user_id)

    for key, value in vars(args).items():
        if value is None:
            continue
        if key == "user_id":
            continue
        if key == "max_unlimited_score":
            setattr(db_statistic, key, max(value, db_statistic.max_unlimited_score))
            continue
        setattr(db_statistic, key, getattr(db_statistic, key) + value)

    await db.commit()
    await db.refresh(db_statistic)

    return db_statistic


async def get_statistic_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(StatisticsDBModel).where(StatisticsDBModel.user_id == user_id))
    return result.scalars().one_or_none()


async def lb_unlimited_score(db: AsyncSession):
    result = await db.execute(select(StatisticsDBModel).order_by(desc(StatisticsDBModel.max_unlimited_score)).limit(3))
    return result.scalars().all()


async def lb_correct_ans(db: AsyncSession):
    result = await db.execute(select(StatisticsDBModel).order_by(desc(StatisticsDBModel.correct_answers)).limit(3))
    return result.scalars().all()
