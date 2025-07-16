# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from api.crud.dish import DishCRUD
from core.config import settings
from models import Base
from models.db_helper import DataBaseHelper
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


@pytest.fixture(scope='function')
async def session(prepare_database) -> AsyncSession:
    """Открывает сессию на время теста."""
    async with test_db_helper.session_factory() as session:
        yield session


@pytest.fixture(scope='function')
async def add_dishes(session:AsyncSession):
    dishes = [
        DishCreate(name="frfefe", price=12),
        DishCreate(name="deded", price=23.43),
        DishCreate(name="frefrfe", price=34),
        ]
    for dish in dishes:
        await DishCRUD(session).add_dish(dish)
