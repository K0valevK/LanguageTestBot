from crud.user import create_user, get_user_by_id, upd_user
from database import get_db_stats_session as get_db_session
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.user import User, UserCreate
from sqlalchemy.ext.asyncio import AsyncSession

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
    return await get_user_by_id(db, telegram_id)


@router.put("", response_model=User)
async def update_user(user: UserCreate, db: AsyncSession = Depends(get_db_session)):
    db_user = await get_user_by_id(db, user.telegram_id)

    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="This user does not exist")

    return await upd_user(db, db_user)
