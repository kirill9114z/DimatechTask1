# app/schemas/payment.py
from pydantic import BaseModel

class PaymentResponse(BaseModel):
    id: int
    transaction_id: str
    account_id: int
    amount: float

    model_config = {"from_attributes": True}

class WebhookPayload(BaseModel):
    transaction_id: str
    account_id: int
    user_id: int
    amount: float
    signature: str