"""Imports every ORM model so they register on ``Base.metadata``.

Import this module once at startup before calling ``Base.metadata.create_all``.
Keeping the imports in one place means new modules only need a single line here
to get their tables created.
"""
from app.modules.matches.models import Match  # noqa: F401
from app.modules.notifications.models import Notification  # noqa: F401
from app.modules.payments.models import Subscription  # noqa: F401
from app.modules.predictions.models import Prediction  # noqa: F401
from app.modules.users.models import User  # noqa: F401
from app.modules.venues.models import Venue, VenueSubmission  # noqa: F401

__all__ = [
    "Match",
    "Notification",
    "Subscription",
    "Prediction",
    "User",
    "Venue",
    "VenueSubmission",
]
