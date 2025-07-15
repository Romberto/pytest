import uvicorn
from fastapi import FastAPI

from core.config import settings

my_app = FastAPI()

import logging

logging.basicConfig(
    level=logging.INFO,  # или DEBUG, WARNING и т.д.
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    uvicorn.run('main:my_app',
                host=settings.run.host,
                port=int(settings.run.port),
                reload=True)

