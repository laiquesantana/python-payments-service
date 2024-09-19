from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime


class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: str = Field(nullable=False, index=True)
    email: str = Field(nullable=False)
    amount_cents: int = Field(nullable=False)
    currency: str = Field(nullable=False)
    payment_method: str = Field(nullable=False)
    status: str = Field(nullable=False, default="pending")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

    class Config:
        table_name = "payments"
