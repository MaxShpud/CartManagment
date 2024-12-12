from app.LOGGING import update_context
from app.app_layer.interfaces.unit_of_work.sql import IUnitOfWork
from app.app_layer.use_cases.carts.dto import CartRetrieveInputDTO, CartOutputDTO


class CartRetrieveUseCase:
    """
    Responsible for retrieving a cart.
    """

    def __init__(self, uow: IUnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: CartRetrieveInputDTO) -> CartOutputDTO:
        """
        Executes the use case  by retrieving the cart. Returns the retrieved
        cart as a CartOutputDTO object.
        :param data:
        :return:
        """
        await update_context(cart_id=data.cart_id)

        async with self._uow(autocommit=True):
            cart = await self._uow.carts.retrieve(cart_id=data.cart_id)

        return CartOutputDTO.model_validate(cart)
