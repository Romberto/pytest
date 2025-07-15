from fastapi import APIRouter
from .dish import router as dish_router

router = APIRouter(
    prefix="/v1"
    )

router.include_router(dish_router)

