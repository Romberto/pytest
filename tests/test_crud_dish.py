from contextlib import nullcontext as does_not_raise
from decimal import Decimal

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.dish import DishCRUD
from models.dish import DishModel
from shemas.dish import DishCreate


@pytest.mark.anyio
async def test_add_multiple_dishes(session: AsyncSession):
    crud = DishCRUD(session)

    dishes_to_add = [
        DishCreate(name="Pizza", price=12.5),
        DishCreate(name="Tomatos", price=20),
        DishCreate(name="Chice", price=12.45),
        ]

    # Добавляем все 3 блюда
    for dish_data in dishes_to_add:
        await crud.add_dish(dish_data)

    # Получаем все блюда из БД
    result = await session.execute(select(DishModel))
    dishes = result.scalars().all()

    assert len(dishes) == 3


@pytest.mark.parametrize(
    "name, price, expected", [
        ("Pizza", 12.5, does_not_raise()),
        ("Tomatos", 20, does_not_raise()),
        ('Chice', 12.45, does_not_raise()),
        ("Rom", -23, pytest.raises(ValueError)),
        ("RTH", "12", does_not_raise()),
        ("fdgt", "one", pytest.raises(ValidationError)),
        ('frtgfdd', "32.56", does_not_raise()),
        ('deewedwedwe', "23,43", pytest.raises(ValidationError))
        ],
    )
@pytest.mark.anyio
async def test_add_dish(name, price, expected, session: AsyncSession):
    with expected:
        crud = DishCRUD(session)
        payload = DishCreate(name=name, price=price)
        dish = await crud.add_dish(payload)

        assert dish.id is not None
        assert dish.name == name
        expected_price = Decimal(str(price))
        actual_price = Decimal(str(dish.price))
        assert actual_price == expected_price

        from sqlalchemy import select
        result = await session.execute(select(DishModel).where(DishModel.id == dish.id))
        dish_from_db = result.scalar_one()

        assert dish_from_db.name == name

        assert Decimal(str(dish_from_db.price)) == Decimal(str(price))
