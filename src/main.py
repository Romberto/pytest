import uvicorn
from fastapi import FastAPI

from core.config import settings

my_app = FastAPI()



if __name__ == '__main__':
    print(settings.model_dump())
    uvicorn.run('main:my_app',
                host=settings.run.host,
                port=int(settings.run.port),
                reload=True)

