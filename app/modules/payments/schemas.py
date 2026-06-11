from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class SubscriptionCreate(BaseModel):
    plan: str = "premium"


class MpesaPayment(BaseModel):
    phone_number: str
    amount: float
    plan: str = "premium"


class SubscriptionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    plan: str
    status: str
    starts_at: Optional[datetime] = None
    ends_at: Optional[datetime] = None
