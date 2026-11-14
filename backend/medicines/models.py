
from django.db import models


class Medicine(models.Model):

    medicine_code = models.CharField(
        max_length=30,
        unique=True
    )

    name = models.CharField(
        max_length=150,
        db_index=True
    )

    generic_name = models.CharField(
        max_length=150,
        db_index=True
    )

    manufacturer = models.CharField(
        max_length=150
    )

    strength = models.CharField(
        max_length=50
    )

    dosage_form = models.CharField(
        max_length=50
    )

    category = models.CharField(
        max_length=100
    )

    prescription_required = models.BooleanField(
        default=False
    )

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Medicine"
        verbose_name_plural = "Medicines"

    def __str__(self):
        return f"{self.name} ({self.medicine_code})"
