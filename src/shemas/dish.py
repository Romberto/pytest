from typing import Union, Optional
from uuid import UUID

from pydantic import BaseModel


class DishCreate(BaseModel):
    name: str
    price: Union[int, float]


class DishUpdate(BaseModel):
    id: UUID
    name: Optional[str]
    price: Optional[int | float]
