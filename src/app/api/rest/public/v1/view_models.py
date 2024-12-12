from uuid import UUID

from pydantic import BaseModel

from app.domain.carts.value_objects import CartStatusEnum


class CartViewModel(BaseModel):
    class Config:
        from_attributes = True
        populate_by_name = True

    id: UUID
    user_id: int
    status: CartStatusEnum
