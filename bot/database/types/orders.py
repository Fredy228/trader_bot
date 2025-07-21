from typing import TypedDict, Literal


class OrderDTO(TypedDict):
    name: str
    time: int
    type: Literal["BUY", "SELL"]
    price: str
    level_up: str
    level_down: str
    status: Literal["OPENED", "CLOSED", "CANCELED"]


class OrderEntity(OrderDTO):
    id: int
