from contextlib import nullcontext as does_not_raise
from decimal import Decimal
from uuid import UUID

import pytest
from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.dish import DishCRUD
from models.dish import DishModel
from shemas.dish import DishCreate, DishUpdate
from tests.conftest import session


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

    assert len(dishes) == len(dishes_to_add)


@pytest.mark.parametrize(
    "name, price, expected", [
        ("Pizza", 12.5, does_not_raise()),
        ("Tomatos", 20, does_not_raise()),
        ('Chice', 12.45, does_not_raise()),
        ("Rom", -23, pytest.raises(ValueError)),
        ("RTH", "12", does_not_raise()),
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
async def test_get_all_dish(session: AsyncSession, add_dishes):
    result = await session.execute(select(DishModel))
    count = result.scalars().all()
    dish = await DishCRUD(session).get_all_dish()
    assert count == dish


@pytest.mark.anyio
async def test_get_by_id(session: AsyncSession, add_dishes):
    result = await session.execute(select(DishModel))
    first_dish = result.scalars().first()
    dish = await DishCRUD(session).get_by_id(first_dish.id)
    assert dish.id == first_dish.id


@pytest.mark.anyio
async def test_get_by_id_invalid_uuid_raises():
    with pytest.raises(ValueError):
        UUID("")


@pytest.mark.parametrize(
    "name, price, expected_raise", [
        ("newName", 50, does_not_raise()),
        ("RTUH", 23.54, does_not_raise()),
        ('derfd', 34.5, does_not_raise()),
        ("4ererds45", -34, pytest.raises(ValueError)),
        ('frerd', 'dsfsdfs', pytest.raises(ValidationError)),
        ],
    )
@pytest.mark.anyio
async def test_update(session: AsyncSession, add_dishes, name, price, expected_raise):
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
async def test_delete(session: AsyncSession, add_dishes):
    result = await session.execute(select(DishModel))
    deleted_dish = result.scalars().first()
    if not deleted_dish:
        raise AssertionError("Нет объекта с таким ID")

    deleted_dish_id = await DishCRUD(session).delete(deleted_dish.id)
    assert deleted_dish.id == deleted_dish_id
    check = await session.get(DishModel, deleted_dish_id)
    assert check is None

