from crud.answer import get_answers_by_task_id
from crud.task import get_tasks_by_difficulty
from database import get_db_task_session as get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.answer import Answer
from schemas.task import Task
from typing import List

router = APIRouter(
    prefix="/task",
    tags=["Tasks"],
)


@router.get("", response_model=List[Task])
async def get_tasks(difficulty_min: float, difficulty_max: float, limit: int, db: AsyncSession = Depends(get_db_session)):
    db_tasks = await get_tasks_by_difficulty(db, difficulty_min, difficulty_max, limit)
    return db_tasks


@router.get("/ans/{task_id}", response_model=List[Answer])
async def get_answers(task_id: int, db: AsyncSession = Depends(get_db_session)):
    db_answers = await get_answers_by_task_id(db, task_id)
    return db_answers
