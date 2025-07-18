import random
from string import ascii_uppercase

import pytest
from httpx import AsyncClient, ASGITransport
from pydantic_core import ValidationError
from sqlalchemy import select, func

from main import my_app
from models import DishModel
from shemas.dish import DishCreate
from contextlib import nullcontext as does_not_raise

BASE_URL_DISH = 'http://test/api/v1/dish'




@pytest.mark.anyio
async def test_api_get_all_dishes(session, add_dishes_to_db):
    async with AsyncClient(transport=ASGITransport(my_app), base_url=BASE_URL_DISH) as ac:
        result = await session.execute(select(func.count()).select_from(DishModel))
        count = result.scalar_one()
        response = await ac.get('/all')
        assert response.status_code == 200
        assert count == len(add_dishes_to_db)
        result = sorted(response.json(), key=lambda d: d["id"])
        expected = sorted(add_dishes_to_db, key=lambda d: d["id"])
        assert result == expected



@pytest.mark.anyio
async def test_api_get_by_id_dish(session, add_dishes_to_db):
    test_dish = add_dishes_to_db[0]
    async with AsyncClient(transport=ASGITransport(my_app), base_url=BASE_URL_DISH) as ac:
        response = await ac.get('/get', params={"dish_id":test_dish['id']})
        current_dish = response.json()
        assert  response.status_code == 200
        for field, value in test_dish.items():
            assert current_dish.get(field) == value






@pytest.mark.parametrize(
    'dish_data , expected', [
        ({"name": "ert",  "price": 12.5}, pytest.raises(ValidationError)),
        ({"name": "wedSa",  "price": 12.53}, does_not_raise()),
        ({"name": "ereedt",  "price": 12}, does_not_raise()),
        ({"name": "testr",  "price": 34}, does_not_raise()),
        ({"name": "test",  "price": 34345}, does_not_raise()),
    ]
)
@pytest.mark.anyio
async def test_api_create_dish(dish_data, session, expected):
    with expected:
        # ✅ Pydantic валидация
        dish_payload = DishCreate(**dish_data)

        async with AsyncClient(transport=ASGITransport(my_app), base_url=BASE_URL_DISH) as ac:
            response = await ac.post(url="/create", json=dish_payload.model_dump())

            # если мы до сюда дошли — значит ValidationError не произошло
            assert response.status_code == 200

            # Проверка что объект появился в БД
            result = await session.execute(select(DishModel).where(DishModel.name == dish_payload.name))
            added_dish = result.scalar_one_or_none()
            assert added_dish is not None
