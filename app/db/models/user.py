from sqlalchemy import Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

from uuid import uuid4

class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)  # ← было password
    full_name: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(default=False, nullable=False)

    accounts: Mapped[list["Account"]] = relationship(
        "Account", back_populates="user", lazy="raise"
    )
