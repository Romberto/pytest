from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession

from core.config import settings


class DataBaseHelper:
    def __init__(self, url:str, echo:bool=False, echo_pool:bool=False,max_overflow:int=10, pool_size:int =15):
        self.engine: AsyncEngine = create_async_engine(
            url=url,
            echo=echo,
            echo_pool=echo_pool,
            max_overflow =max_overflow,
            pool_size=pool_size,
            )

        self.session_factory:async_sessionmaker[AsyncSession] = async_sessionmaker(
            bind=self.engine,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False
            )
    async def dispose(self):
        await self.engine.dispose()

    async def session_getter(self):
        async with self.session_factory() as session:
            yield  session

DEBUG = settings.run.debug
if not DEBUG:
    url_db = str(settings.db.url)
else:
    url_db = str(settings.db.test_url)

db_helper = DataBaseHelper(
    url=url_db,
    echo=settings.db.echo,
    echo_pool=settings.db.echo_pool,
    max_overflow=settings.db.max_overflow,
    pool_size=settings.db.pool_size
    )