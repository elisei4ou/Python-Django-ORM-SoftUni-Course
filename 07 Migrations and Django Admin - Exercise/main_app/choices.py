from django.db import models


class Statuses(models.TextChoices):
    PENDING = 'PE', 'Pending'
    COMPLETED = 'COM', 'Completed'
    CANCELLED = 'CAN', 'Cancelled'