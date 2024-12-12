import uuid
from datetime import datetime
from logging import getLogger

from app.domain.carts.value_objects import CartStatusEnum
from app.domain.carts.dto import CartDTO
logger = getLogger(__name__)


class Cart:
    """
    Represents a shopping cart and provides methods to modify and manage the cart
    items, apply coupons, and change the cart status.
    """
    STATUS_TRANSITION_RULESET: dict[CartStatusEnum, set[CartStatusEnum]] = {
        CartStatusEnum.OPENED: {CartStatusEnum.DEACTIVATED, CartStatusEnum.LOCKED},
        CartStatusEnum.DEACTIVATED: {},
        CartStatusEnum.LOCKED: {CartStatusEnum.OPENED, CartStatusEnum.COMPLETED},
        CartStatusEnum.COMPLETED: {},
    }

    def __init__(
            self,
            data: CartDTO,
    ) -> None:
        self.created_at = data.created_at
        self.id = data.id
        self.user_id = data.user_id
        self.status = data.status

    @classmethod
    def create(cls, user_id: int) -> "Cart":
        """Creates a new cart with the specified user ID."""
        return cls(
            data=CartDTO(
                created_at=datetime.now(),
                id=uuid.uuid4(),
                user_id=user_id,
                status=CartStatusEnum.OPENED
            )
        )
