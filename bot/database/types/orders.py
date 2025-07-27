from typing import TypedDict, Literal


class OrderDTO(TypedDict):
    time: int
    type: Literal["BUY", "SELL"]
    price: str
    level_up: str
    level_down: str
    status: Literal["OPENED", "DEFERRED"]


class OrderEntity(OrderDTO):
    id: int
