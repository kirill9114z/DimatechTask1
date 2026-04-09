from pydantic import BaseModel


class Account(BaseModel):
    id: int
    balance: float

    model_config = {"from_attributes": True}


