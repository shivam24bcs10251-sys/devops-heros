from datetime import datetime, timezone
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
def now():
    return datetime.now(timezone.utc)
class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (CheckConstraint("available >= 0 AND available <= total", name="valid_stock"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_tag: Mapped[str] = mapped_column(String(40), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(160), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(Text, default="")
    total: Mapped[int] = mapped_column(Integer, nullable=False)
    available: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
class Loan(Base):
    __tablename__ = "loans"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    asset_id: Mapped[int] = mapped_column(ForeignKey("assets.id"), nullable=False, index=True)
    asset_name: Mapped[str] = mapped_column(String(160), nullable=False)
    borrower: Mapped[str] = mapped_column(String(100), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    borrowed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=now)
    returned_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
