"""Premium subscriptions.

Payment provider integration (M-Pesa STK push / Stripe) is stubbed — the
endpoints model the flow so the frontend can be built against a stable shape.
Wire the provider in ``initiate_mpesa`` and a confirmation webhook when ready.
"""
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.modules.payments.models import Subscription


def active_for(db: Session, user_id: str) -> Optional[Subscription]:
    return (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id)
        .order_by(Subscription.created_at.desc())
        .first()
    )


def subscribe(db: Session, user_id: str, plan: str = "premium") -> Subscription:
    existing = (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id, Subscription.status == "active")
        .first()
    )
    if existing:
        raise HTTPException(status_code=400, detail="Already has an active subscription")

    now = datetime.now(timezone.utc)
    sub = Subscription(
        user_id=user_id,
        plan=plan,
        status="active",
        starts_at=now,
        ends_at=now + timedelta(days=30),
    )
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub


def cancel(db: Session, user_id: str) -> Subscription:
    sub = (
        db.query(Subscription)
        .filter(Subscription.user_id == user_id, Subscription.status == "active")
        .first()
    )
    if not sub:
        raise HTTPException(status_code=404, detail="No active subscription found")
    sub.status = "cancelled"
    db.commit()
    db.refresh(sub)
    return sub


def initiate_mpesa(user_id: str, phone_number: str, amount: float, plan: str) -> dict:
    # TODO: integrate Daraja STK push. For now return a pending acknowledgement.
    return {
        "status": "pending",
        "phone": phone_number,
        "amount": amount,
        "plan": plan,
        "note": "M-Pesa STK push integration coming soon",
    }
