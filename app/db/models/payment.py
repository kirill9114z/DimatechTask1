from sqlalchemy import ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class Payment(Base):
    __tablename__ = 'payment'

    transaction_id: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    amount: Mapped[float] = mapped_column(nullable=False)
    account_id: Mapped[int] = mapped_column(ForeignKey("account.id"), nullable=False)  # ← account.id
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)