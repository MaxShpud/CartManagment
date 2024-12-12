from logging import getLogger

from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork
from app.app_layer.use_cases.carts.dto import CartOutputDTO
from app.domain.carts.entities import Cart

logger = getLogger(__name__)


class CreateCartUseCase:

    def __init__(self,
                 uow: IUnitOfWork
                 ) -> None:
        self._uow = uow

    async def create_cart(self, user_id: int) -> CartOutputDTO:
        """
        Creates a cart for the user based on their user ID.
        """
        return await self._create(user_id)

    async def _create(self, user_id: int) -> CartOutputDTO:
        async with self._uow(autocommit=True):
            cart = Cart.create(user_id=user_id)
            await self._uow.carts.create(cart=cart)

        logger.debug("Cart %s successfully created for user %s.", cart.id, cart.user_id)

        return CartOutputDTO.model_validate(cart)
