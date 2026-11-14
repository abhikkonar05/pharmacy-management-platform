
from django.db import models
from django.db.models import Q, F


class Batch(models.Model):

    medicine = models.ForeignKey(
        "medicines.Medicine",
        on_delete=models.PROTECT,
        related_name="batches"
    )

    batch_number = models.CharField(
        max_length=50
    )

    manufacturing_date = models.DateField()

    expiry_date = models.DateField(
        db_index=True
    )

    purchase_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    selling_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    quantity_received = models.PositiveIntegerField()

    available_quantity = models.PositiveIntegerField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["expiry_date"]

        constraints = [
            models.UniqueConstraint(
                fields=["medicine", "batch_number"],
                name="unique_medicine_batch"
            ),
            models.CheckConstraint(
                condition=Q(expiry_date__gt=F("manufacturing_date")),
                name="batch_expiry_after_manufacturing"
            ),
            models.CheckConstraint(
                condition=Q(quantity_received__gt=0),
                name="batch_received_quantity_positive"
            ),
            models.CheckConstraint(
                condition=Q(purchase_price__gte=0),
                name="batch_purchase_price_nonnegative"
            ),
            models.CheckConstraint(
                condition=Q(selling_price__gte=0),
                name="batch_selling_price_nonnegative"
            ),
        ]

    def __str__(self):
        return f"{self.medicine.name} - {self.batch_number}"
