# tests/conftest.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from models import Base
from models.db_helper import DataBaseHelper

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
