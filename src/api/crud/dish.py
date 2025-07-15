from uuid import UUID

from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from models.dish import DishModel
from shemas.dish import DishCreate, DishUpdate


class DishCRUD:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all_dish(self):
        result = await self.session.execute(select(DishModel))
        return result.scalars().all()

    async def add_dish(self, payload: DishCreate):
        dish = DishModel(name=payload.name, price=payload.price)
        self.session.add(dish)
        await self.session.commit()
        await self.session.refresh(dish)
        return dish

    async def get_by_id(self, dish_id: UUID) -> DishModel | None:
        result = await self.session.execute(
            select(DishModel).where(DishModel.id == dish_id),
            )
        return result.scalar_one_or_none()

    async def delete(self, dish_id: UUID) -> UUID:
        try:
            result = await self.session.execute(
                delete(DishModel).where(DishModel.id == dish_id),
                )
            if result.rowcount == 0:
                raise HTTPException(status_code=404, detail="Блюда с таким ID нет")
            await self.session.commit()
            return dish_id
        except SQLAlchemyError:
            await self.session.rollback()
            raise HTTPException(status_code=500, detail="Ошибка при удалении блюда")

    async def update(self, payload: DishUpdate) -> DishModel | None:
        id, name, price = payload.model_dump().values()
        dish = await self.get_by_id(id)
        if not dish:
            raise HTTPException(status_code=500, detail="блюда с таким ID нет")
        if name is not None:
            dish.name = name
        if price is not None:
            dish.price = price
        await self.session.commit()
        await self.session.refresh(dish)
        return dish
