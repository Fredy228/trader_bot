from typing import TypedDict, Literal


class OrderArchiveDTO(TypedDict):
    time: int
    type: Literal["BUY", "SELL"]
    price: str
    status: Literal["OPENED", "CLOSED", "CANCELED"]
    profit: int


class OrderArchiveEntity(OrderArchiveDTO):
    id: int
