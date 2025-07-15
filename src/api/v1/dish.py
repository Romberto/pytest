from uuid import UUID

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.dish import DishCRUD
from models.db_helper import db_helper
from models.dish import DishModel
from shemas.dish import DishCreate, DishUpdate

router = APIRouter(
    tags=['Dish'],
    prefix="/dish",
    )


@router.get('/all')
async def get_all_dish(session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        return await DishCRUD(session).get_all_dish()
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при получении блюд")

@router.get('/get', response_model=DishUpdate)
async def get_by_id(dish_id:UUID, session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        return await DishCRUD(session).get_by_id(dish_id)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при получение блюда по ID")


@router.post('/create')
async def create_dish(payload: DishCreate, session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        return await DishCRUD(session).add_dish(payload)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при добавление блюд")

@router.post('/remove')
async def remove_dish(dish_id:UUID, session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        return await DishCRUD(session).delete(dish_id)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail="Ошибка при удаление блюда")

@router.post('/update')
async def update_dish(payload:DishUpdate, session: AsyncSession = Depends(db_helper.session_getter)):
    try:
        return await DishCRUD(session).update(payload)
    except SQLAlchemyError:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Ошибка при изменение блюда {payload.name}")


