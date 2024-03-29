from models import Task as TaskDBModel
from models import Answer as AnswerDBModel
from schemas import TaskCreate as TaskCreateDBSchema
from schemas import Task as TaskDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_tasks_by_difficulty(db: AsyncSession, difficulty_min: float, difficulty_max: float, limit: int):
    result = await db.execute(select(TaskDBModel).where(difficulty_min <= TaskDBModel.difficulty,
                                                        TaskDBModel.difficulty <= difficulty_max).limit(limit))
    return result.scalars().all()


async def get_answers_by_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(AnswerDBModel).where(AnswerDBModel.task_id == task_id))
    return result.scalars().all()
