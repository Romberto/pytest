import pytest

from api.crud.dish import DishCRUD
from models.base import Base
from models.db_helper import db_helper
from shemas.dish import DishCreate


@pytest.fixture(scope="session", autouse=True)
async def prepare_db():
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

@pytest.fixture(scope="function", autouse=True)
async def session():
    return await db_helper.session_getter()

@pytest.fixture
def dishes():
    return [
        DishCreate(name="name1", price=23),
        DishCreate(name="name2", price=23.65),
        DishCreate(name="name3", price=236),
        DishCreate(name="name4", price=2343),
        ]

class TestDishCRUD:

    async def test_add_dish(self, dishes, session):
        for dish in dishes:
            await DishCRUD(session).add_dish(dish)