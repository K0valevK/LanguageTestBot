from models import Task as TaskDBModel
from schemas import TaskCreate as TaskCreateDBSchema
from schemas import Task as TaskDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tasks_by_difficulty(db: AsyncSession, difficulty_min: float, difficulty_max: float):
    result = await db.execute(select(TaskDBModel).where(
        (difficulty_min <= TaskDBModel.difficulty) and (TaskDBModel.difficulty <= difficulty_max)))
    return result.scalars().all()
