from typing import Union, Optional
from uuid import UUID

from pydantic import BaseModel, field_validator


class DishCreate(BaseModel):
    name: str
    price: Union[int, float]

    @field_validator('price', mode='after')
    @classmethod
    def is_valid_price(cls, price):
        if price <= 0:
            raise ValueError("Цена должна быть больше нуля")

        str_price = str(price)

        if '.' in str_price:
            integer_part, decimal_part = str_price.split('.')
            if len(integer_part) > 8:
                raise ValueError("Целая часть цены не должна превышать 8 знаков")
            if len(decimal_part) > 2:
                raise ValueError("Дробная часть цены не должна превышать 2 знака")
        else:
            if len(str_price) > 10:
                raise ValueError("Цена не должна превышать 10 знаков")

        return price

    @field_validator('name', mode='after')
    @classmethod
    def is_name(cls, name):
        if len(name) <= 3:
            raise ValueError("длина названия должна быть не менее 4-х сибволов")
        return name


class DishUpdate(BaseModel):
    id: UUID
    name: Optional[str]
    price: Optional[int | float]

    @field_validator('price', mode='after')
    @classmethod
    def is_more_zero(cls, price):
        if price <= 0:
            raise ValueError("цена должна быть больше нуля")
        return price
