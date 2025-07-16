from typing import Union, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class DishCreate(BaseModel):
    name: str
    price: Union[int, float]

    @field_validator('price', mode='after')
    @classmethod
    def is_more_zero(cls, price):
        if price <= 0:
            raise ValueError("цена должна быть больше нуля")
        return price


class DishUpdate(BaseModel):
    id: UUID
    name: Optional[str]
    price: Optional[int | float]
