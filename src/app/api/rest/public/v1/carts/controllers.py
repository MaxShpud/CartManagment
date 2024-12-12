from uuid import UUID

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends

from app.api.rest.errors import ACTIVE_CART_ALREADY_EXISTS_HTTP_ERROR, RETRIEVE_CART_HTTP_ERROR
from app.api.rest.public.v1.view_models import CartViewModel
from app.app_layer.interfaces.auth_system.exceptions import InvalidAuthDataError
from app.app_layer.use_cases.carts.create_cart import CreateCartUseCase
from app.app_layer.use_cases.carts.dto import CartRetrieveInputDTO
from app.app_layer.use_cases.carts.retrieve_cart import CartRetrieveUseCase
from app.containers import Container
from app.domain.interfaces.repositories.carts.exceptions import ActiveCartAlreadyExistsError, CartNotFoundError

router = APIRouter()


@router.post("/{user_id}")
@inject
async def create(
        user_id: int,
        use_case: CreateCartUseCase = Depends(Provide[Container.create_cart_use_case])
) -> CartViewModel:
    try:
        result = await use_case.create_cart(user_id=user_id)
    except ActiveCartAlreadyExistsError:
        raise ACTIVE_CART_ALREADY_EXISTS_HTTP_ERROR

    return CartViewModel.model_validate(result)


@router.get('/{card_id}')
@inject
async def retrieve(
        cart_id: UUID,
        use_case: CartRetrieveUseCase = Depends(Provide[Container.cart_retrieve_use_case])
) -> CartViewModel:
    try:
        result = await use_case.execute(
            data=CartRetrieveInputDTO(
                cart_id=cart_id,
            )
        )
    except CartNotFoundError:
        raise RETRIEVE_CART_HTTP_ERROR
    return CartViewModel.model_validate(result)
