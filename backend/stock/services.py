
from django.db import transaction
from django.core.exceptions import ValidationError
from django.utils import timezone

from batches.models import Batch
from .models import StockMovement


@transaction.atomic
def apply_stock_movement(
    batch_id,
    movement_type,
    direction,
    quantity,
    reference="",
    notes=""
):
    # Validate quantity
    if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
        raise ValidationError("Quantity must be a positive integer.")

    # Validate movement type
    valid_types = [
        StockMovement.MovementType.PURCHASE,
        StockMovement.MovementType.SALE,
        StockMovement.MovementType.RETURN,
        StockMovement.MovementType.ADJUSTMENT,
    ]

    if movement_type not in valid_types:
        raise ValidationError("Invalid movement type.")

    # Validate direction
    if direction not in [
        StockMovement.Direction.IN,
        StockMovement.Direction.OUT,
    ]:
        raise ValidationError("Invalid stock direction.")

    # Validate movement direction
    if movement_type in [
        StockMovement.MovementType.PURCHASE,
        StockMovement.MovementType.RETURN,
    ] and direction != StockMovement.Direction.IN:
        raise ValidationError("Purchase and Return must increase stock.")

    if movement_type == StockMovement.MovementType.SALE:
        if direction != StockMovement.Direction.OUT:
            raise ValidationError("Sale must decrease stock.")

    # Lock batch row
    try:
        batch = Batch.objects.select_for_update().select_related(
            "medicine"
        ).get(pk=batch_id)
    except Batch.DoesNotExist:
        raise ValidationError("Batch does not exist.")

    # Reject inactive medicine
    if not batch.medicine.is_active:
        raise ValidationError("Medicine is inactive.")

    # Reject expired batch sales
    if (
        movement_type == StockMovement.MovementType.SALE
        and batch.expiry_date <= timezone.localdate()
    ):
        raise ValidationError("Cannot sell an expired batch.")

    quantity_before = batch.available_quantity

    # Calculate stock
    if direction == StockMovement.Direction.OUT:
        if quantity > quantity_before:
            raise ValidationError("Insufficient stock.")

        quantity_after = quantity_before - quantity
    else:
        quantity_after = quantity_before + quantity

    # Update batch
    batch.available_quantity = quantity_after
    batch.save(update_fields=["available_quantity", "updated_at"])

    # Create audit record
    movement = StockMovement.objects.create(
        batch=batch,
        movement_type=movement_type,
        direction=direction,
        quantity=quantity,
        quantity_before=quantity_before,
        quantity_after=quantity_after,
        reference=reference,
        notes=notes,
    )

    return movement
