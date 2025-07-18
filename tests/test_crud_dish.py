from contextlib import nullcontext as does_not_raise
from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count, func

from api.crud.dish import DishCRUD
from models.dish import DishModel
from shemas.dish import DishCreate, DishUpdate
from tests.conftest import session


@pytest.mark.anyio
async def test_add_multiple_dishes(session: AsyncSession):
    result = await session.execute(select(func.count()).select_from(DishModel))
    start_count = result.scalars().one()
    dishes_to_add = [
        DishCreate(name="Pizj", price=12.5),
        DishCreate(name="Tomato", price=20),
        DishCreate(name="Chic", price=12.45),
        ]

    # Добавляем все 3 блюда
    for dish_data in dishes_to_add:
        await DishCRUD(session).add_dish(dish_data)

    # Получаем все блюда из БД
    result_all = await session.execute(select(DishModel))
    dishes = result_all.scalars().all()

    assert start_count != len(dishes)
    assert start_count == len(dishes) - len(dishes_to_add)


@pytest.mark.parametrize(
    "name, price, expected", [
        ("Pizzadf", 12.5, does_not_raise()),
        ("Tomatosfdd", 20, does_not_raise()),
        ('Chicefcx', 12.45, does_not_raise()),
        ('Chice2', 1234567891.45, pytest.raises(ValidationError)),
        ("Rome", -23, pytest.raises(ValidationError)),
        ("Rom", -23, pytest.raises(ValidationError)),
        ("RTHwe", "12", does_not_raise()),
        ("fdgt", "one", pytest.raises(ValidationError)),
        ('frtgfdd', "32.56", does_not_raise()),
        ('deewedwedwe', "23,43", pytest.raises(ValidationError)),
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


@pytest.mark.anyio
async def test_get_all_dish(session: AsyncSession, add_dishes_to_db):
    result = await session.execute(select(DishModel))
    count = result.scalars().all()
    dish = await DishCRUD(session).get_all_dish()
    assert count == dish


@pytest.mark.anyio
async def test_get_by_id(session: AsyncSession, add_dishes_to_db):
    TEST_DISH = add_dishes_to_db[0]
    if TEST_DISH:
        dish = await DishCRUD(session).get_by_id(TEST_DISH['id'])
        assert dish.id == UUID(TEST_DISH['id'])


@pytest.mark.parametrize(
    "name, price, expected_raise", [
        ("newName", 50, does_not_raise()),
        ("RTUH", 23.54, does_not_raise()),
        ('derfd', 34.5, does_not_raise()),
        ("4ererds45", -34, pytest.raises(ValidationError)),
        ('frerd', 'dsfsdfs', pytest.raises(ValidationError)),
        ],
    )
@pytest.mark.anyio
async def test_update(session: AsyncSession, add_dishes_to_db, name, price, expected_raise):
    # Получаем первую запись
    with expected_raise:
        result = await session.execute(select(DishModel))
        existing_dish = result.scalars().first()

        if not existing_dish:
            raise AssertionError("Нет объекта с таким ID")

        update_data = DishUpdate(id=existing_dish.id, name=name, price=price)
        updated_dish = await DishCRUD(session).update(update_data)

        assert updated_dish.id == existing_dish.id
        assert updated_dish.name == name
        assert Decimal(str(updated_dish.price)) == Decimal(str(price))

        # Проверка из БД
        refreshed = await session.get(DishModel, existing_dish.id)
        assert refreshed.name == name
        assert Decimal(str(refreshed.price)) == Decimal(str(price))


@pytest.mark.anyio
async def test_delete(session: AsyncSession, add_dishes_to_db):
    result = await session.execute(select(DishModel))
    deleted_dish = result.scalars().first()
    if not deleted_dish:
        raise AssertionError("Нет объекта с таким ID")

    deleted_dish_id = await DishCRUD(session).delete(deleted_dish.id)
    assert deleted_dish.id == deleted_dish_id
    check = await session.get(DishModel, deleted_dish_id)
    assert check is None
