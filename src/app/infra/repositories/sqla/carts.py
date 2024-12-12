from logging import getLogger
from uuid import UUID

from sqlalchemy import select, Row
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.carts.dto import CartDTO
from app.domain.carts.entities import Cart
from app.domain.carts.value_objects import CartStatusEnum
from app.domain.interfaces.repositories.carts.exceptions import ActiveCartAlreadyExistsError, CartNotFoundError
from app.domain.interfaces.repositories.carts.repo import ICartsRepository
from app.infra.repositories.sqla import models
from app.LOGGING import update_context

logger = getLogger(__name__)


class CartsRepository(ICartsRepository):
    """
    Responsible for interacting with the database to perform CRUD operations on the
    Cart objects. It provides methods to create a new cart, retrieve an existing
    cart, update a cart's status, clear a cart's items, get a list of carts, get the
    cart configuration, update the cart configuration, and find abandoned carts based
    on certain criteria.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def create(self, cart: Cart) -> Cart:
        """
        Creates a new cart in the database and returns the created cart object.
        """

        stmt = insert(models.Cart).values(
            created_at=cart.created_at,
            id=cart.id,
            user_id=cart.user_id,
            status=cart.status,
        )

        try:
            await self._session.execute(stmt)
        except IntegrityError:
            raise ActiveCartAlreadyExistsError

        await update_context(cart_id=cart.id)

        return cart

    async def retrieve(self, cart_id: UUID) -> Cart:
        """
        Retrieve an existing cart from the database based on the provided cart ID
        and returns the retrieved cart object.
        :param cart_id:
        :return:
        """
        stmt = (
            select(models.Cart)
            .where(
                models.Cart.id == cart_id,
                models.Cart.status != CartStatusEnum.DEACTIVATED
            )
        )
        result = await self._session.scalars(stmt)
        obj = result.first()

        if not obj:
            raise CartNotFoundError

        cart = await self._get_cart(obj)
        logger.debug("Got cart: %s", vars(cart))

        return cart

    @staticmethod
    async def _get_cart(obj: Row):
        cart = Cart(
            data=CartDTO.model_validate(obj),
        )
        return cart
