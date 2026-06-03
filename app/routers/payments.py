from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models.models import Subscription
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])

class SubscriptionCreate(BaseModel):
    user_id: str
    plan: str = "premium"

class MpesaPayment(BaseModel):
    user_id: str
    phone_number: str
    amount: float
    plan: str = "premium"

@router.post("/subscribe")
def create_subscription(
    payload: SubscriptionCreate,
    db: Session = Depends(get_db)
):
    existing = db.query(Subscription)\
        .filter(Subscription.user_id == payload.user_id)\
        .first()

    if existing and existing.status == "active":
        raise HTTPException(status_code=400, detail="Already has active subscription")

    subscription = Subscription(
        user_id=payload.user_id,
        plan=payload.plan,
        status="active",
        starts_at=datetime.utcnow(),
        ends_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(subscription)
    db.commit()
    db.refresh(subscription)
    return {
        "message": "Subscription created successfully",
        "subscription": {
            "id": subscription.id,
            "plan": subscription.plan,
            "status": subscription.status,
            "starts_at": str(subscription.starts_at),
            "ends_at": str(subscription.ends_at)
        }
    }

@router.get("/subscription")
def get_subscription(user_id: str, db: Session = Depends(get_db)):
    subscription = db.query(Subscription)\
        .filter(Subscription.user_id == user_id)\
        .order_by(Subscription.created_at.desc())\
        .first()

    if not subscription:
        return {"subscription": None, "plan": "free"}

    return {
        "subscription": {
            "id": subscription.id,
            "plan": subscription.plan,
            "status": subscription.status,
            "starts_at": str(subscription.starts_at),
            "ends_at": str(subscription.ends_at)
        }
    }

@router.patch("/subscription/cancel")
def cancel_subscription(user_id: str, db: Session = Depends(get_db)):
    subscription = db.query(Subscription)\
        .filter(
            Subscription.user_id == user_id,
            Subscription.status == "active"
        ).first()

    if not subscription:
        raise HTTPException(status_code=404, detail="No active subscription found")

    subscription.status = "cancelled"
    db.commit()
    return {"message": "Subscription cancelled successfully"}

@router.post("/mpesa/initiate")
def initiate_mpesa(payload: MpesaPayment):
    return {
        "message": "Mpesa payment initiated",
        "phone": payload.phone_number,
        "amount": payload.amount,
        "plan": payload.plan,
        "status": "pending",
        "note": "Mpesa STK push integration coming soon"
    }

@router.post("/webhook")
def payment_webhook(data: dict):
    return {"message": "Webhook received", "status": "ok"}