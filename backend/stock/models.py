from django.db import models
from django.db.models import Q


class StockMovement(models.Model):

    class MovementType(models.TextChoices):
        OPENING = "OPENING", "Opening Stock"
        PURCHASE = "PURCHASE", "Purchase"
        SALE = "SALE", "Sale"
        RETURN = "RETURN", "Return"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"

    class Direction(models.TextChoices):
        IN = "IN", "Stock In"
        OUT = "OUT", "Stock Out"

    batch = models.ForeignKey(
        "batches.Batch",
        on_delete=models.PROTECT,
        related_name="stock_movements"
    )

    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices
    )

    direction = models.CharField(
        max_length=3,
        choices=Direction.choices
    )

    quantity = models.PositiveIntegerField()

    quantity_before = models.PositiveIntegerField()
    quantity_after = models.PositiveIntegerField()

    reference = models.CharField(
        max_length=100,
        blank=True
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=Q(quantity__gt=0),
                name="movement_quantity_positive"
            ),
        ]

    def __str__(self):
        return (
            f"{self.movement_type} - "
            f"{self.batch.batch_number} - {self.quantity}"
        )