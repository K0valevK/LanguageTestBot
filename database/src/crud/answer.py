from models import Answer as AnswerDBModel
from schemas import AnswerCreate as AnswerCreateDBSchema
from schemas import Answer as AnswerDBSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


async def get_answers_by_task_id(db: AsyncSession, task_id: int):
    result = await db.execute(select(AnswerDBModel).where(AnswerDBModel.task_id == task_id))
    return result.scalars().all()
