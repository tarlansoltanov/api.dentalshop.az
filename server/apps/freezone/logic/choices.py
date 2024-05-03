from django.db import models


class FreeZoneStatus(models.IntegerChoices):
    """Choices for FreezoneItem status."""

    PENDING = 0, "Təsdiq gözləyir"
    VERIFIED = 1, "Təsdiqlənib"
    REJECTED = 2, "Rədd edilib"
