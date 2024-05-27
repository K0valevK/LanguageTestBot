from crud.statistics import create_statistic, get_statistic_by_user_id, upd_statistic, lb_correct_ans, lb_unlimited_score
from database import get_db_stats_session as get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.statistics import Statistics, StatisticsCreate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter(
    prefix="/statistics",
    tags=["Statistics"],
)


@router.post("", response_model=Statistics)
async def post_statistics(statistics: StatisticsCreate, db: AsyncSession = Depends(get_db_session)):
    db_statistics = await get_statistic_by_user_id(db, statistics.user_id)

    if db_statistics is not None:
        return db_statistics

    db_statistics = await create_statistic(db, statistics)
    return db_statistics


@router.get("/{user_id}", response_model=Statistics)
async def get_statistics(user_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await get_statistic_by_user_id(db, user_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    return result


@router.put("", response_model=Statistics)
async def update_statistics(statistics: StatisticsCreate, db: AsyncSession = Depends(get_db_session)):
    db_statistics = await get_statistic_by_user_id(db, statistics.user_id)

    if db_statistics is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    return await upd_statistic(db, statistics)


@router.get("/leaders/tasks", response_model=List[Statistics])
async def get_leaders_tasks(db: AsyncSession = Depends(get_db_session)):
    db_leaders_most_correct = await lb_correct_ans(db)

    return db_leaders_most_correct


@router.get("/leaders/endless", response_model=List[Statistics])
async def get_leaders_endless(db: AsyncSession = Depends(get_db_session)):
    db_leaders_endless = await lb_unlimited_score(db)

    return db_leaders_endless
