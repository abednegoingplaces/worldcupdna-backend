from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.modules.payments import service
from app.modules.payments.schemas import (
    MpesaPayment,
    SubscriptionCreate,
    SubscriptionOut,
)
from app.modules.users.models import User

router = APIRouter(prefix="/payments", tags=["payments"])


@router.get("/subscription")
def get_subscription(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    sub = service.active_for(db, user.id)
    if not sub:
        return {"subscription": None, "plan": "free"}
    return {"subscription": SubscriptionOut.model_validate(sub), "plan": sub.plan}


@router.post("/subscribe", response_model=SubscriptionOut, status_code=201)
def subscribe(
    payload: SubscriptionCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.subscribe(db, user.id, payload.plan)


@router.patch("/subscription/cancel", response_model=SubscriptionOut)
def cancel(
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    return service.cancel(db, user.id)


@router.post("/mpesa/initiate")
def initiate_mpesa(
    payload: MpesaPayment,
    user: User = Depends(get_current_user),
):
    return service.initiate_mpesa(user.id, payload.phone_number, payload.amount, payload.plan)
