from crud.user import create_user, get_user_by_id, get_user_by_name, upd_user, lb_correct_ans, lb_unlimited_score
from database import get_db_stats_session as get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

router = APIRouter(
    prefix="/user",
    tags=["Users"],
)


@router.post("", response_model=User)
async def post_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user_by_id(db, user.telegram_id)

    if db_user is not None:
        return db_user

    db_user = await create_user(db, user)
    return db_user


@router.get("/{telegram_id}", response_model=User)
async def get_user(telegram_id: int, db: AsyncSession = Depends(get_db_session)):
    result = await get_user_by_id(db, telegram_id)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    return result


@router.get("/name/{username}", response_model=User)
async def get_user_name(username: str, db: AsyncSession = Depends(get_db_session)):
    result = await get_user_by_name(db, username)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User does not exist")

    return result


@router.put("", response_model=User)
async def update_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user_by_id(db, user.telegram_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not exist")

    return await upd_user(db, user)


@router.get("/leaders/tasks", response_model=List[User])
async def get_leaders_tasks(db: AsyncSession = Depends(get_db_session)):
    db_leaders_most_correct = await lb_correct_ans(db)

    return db_leaders_most_correct


@router.get("/leaders/endless", response_model=List[User])
async def get_leaders_endless(db: AsyncSession = Depends(get_db_session)):
    db_leaders_endless = await lb_unlimited_score(db)

    return db_leaders_endless

