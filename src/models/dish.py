from decimal import Decimal

from sqlalchemy import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column

from models.base import Base


class DishModel(Base):
    __tablename__ = "dish"
    name:Mapped[str]
    price:Mapped[Decimal] = mapped_column(DECIMAL(10,2))

