from database import get_db_session
from crud.answer import get_answers_by_task_id
from crud.task import get_tasks_by_difficulty
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.answer import Answer
from schemas.task import Task

router = APIRouter(
    prefix="/task",
    tags=["Tasks"],
)

