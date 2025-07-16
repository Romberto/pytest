import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api import router as api_router
from core.config import settings
from models.db_helper import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await db_helper.dispose()


my_app = FastAPI(lifespan=lifespan)

my_app.include_router(api_router)

logging.basicConfig(
    level=logging.INFO,  # или DEBUG, WARNING и т.д.
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    uvicorn.run(
        'main:my_app',
        host=settings.run.host,
        port=int(settings.run.port),
        reload=True,
        )
