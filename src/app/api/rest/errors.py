from fastapi import HTTPException, status

ACTIVE_CART_ALREADY_EXISTS_HTTP_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 2001, "message": "Active cart already exists."},
)

RETRIEVE_CART_HTTP_ERROR = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail={"code": 2000, "message": "Cart not found."},
)
