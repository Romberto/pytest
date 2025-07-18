# tests/conftest.py
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.dish import DishCRUD
from core.config import settings
from main import my_app
from models import Base, DishModel
from models.db_helper import DataBaseHelper, db_helper
from shemas.dish import DishCreate

# Создаём test db_helper
test_db_helper = DataBaseHelper(
    url=str(settings.db.test_url),
    echo=False,
    echo_pool=False,
    )


@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session')
async def prepare_database():
    """Создаёт все таблицы и удаляет после завершения сессии."""
    if settings.run.debug != 1:
        pytest.exit("❌ Запуск тестов разрешён только в режиме DEBUG (settings.run.debug == 1)", returncode=1)

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    await test_db_helper.dispose()

@pytest.fixture(scope="function")
async def add_dishes_to_db(session: AsyncSession):
    dishes_data = [
        {"name": "Item1", "price": 12},
        {"name": "Item2", "price": 23.43},
        {"name": "Item3", "price": 34},
    ]
    dishes = []
    for data in dishes_data:
        dish = DishModel(name=data["name"], price=data["price"])
        session.add(dish)
        dishes.append(dish)

    await session.commit()

    yield [
        {"id": str(dish.id), "name": dish.name, "price": float(dish.price)}
        for dish in dishes
    ]
    for dish in dishes:
        await session.delete(dish)
        await session.commit()


@pytest.fixture(scope='function')
async def session(prepare_database) -> AsyncSession:
    """Открывает сессию на время теста."""
    async with test_db_helper.session_factory() as session:
        yield session






@pytest.fixture(autouse=True)
def override_get_db(session: AsyncSession):
    my_app.dependency_overrides[db_helper.session_getter] = lambda: session
    yield
    my_app.dependency_overrides = {}


