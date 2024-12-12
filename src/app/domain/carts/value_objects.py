import enum


class CartStatusEnum(enum.Enum):
    OPENED = "OPENED"
    DEACTIVATED = "DEACTIVATED"
    LOCKED = "LOCKED"
    COMPLETED = "COMPLETED"
