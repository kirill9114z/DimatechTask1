from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.schemas.payment import WebhookPayload
from app.services import webhook as webhook_service

router = APIRouter(prefix="/webhook", tags=["Webhook"])


@router.post("/payment")
async def handle_payment_webhook(
    payload: WebhookPayload,
    db: AsyncSession = Depends(get_db),
):
    return await webhook_service.process_webhook(payload, db)