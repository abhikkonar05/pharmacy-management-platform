
from datetime import date

from django.db import transaction
from rest_framework import serializers

from .models import Batch
from stock.models import StockMovement


class BatchSerializer(serializers.ModelSerializer):

    class Meta:
        model = Batch

        fields = [
            "id",
            "medicine",
            "batch_number",
            "manufacturing_date",
            "expiry_date",
            "purchase_price",
            "selling_price",
            "quantity_received",
            "available_quantity",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "available_quantity",
            "created_at",
            "updated_at",
        ]

    def validate_batch_number(self, value):
        value = value.strip().upper()

        if not value:
            raise serializers.ValidationError(
                "Batch number cannot be empty."
            )

        return value

    def validate(self, attrs):
        medicine = attrs.get(
            "medicine",
            self.instance.medicine if self.instance else None
        )

        batch_number = attrs.get(
            "batch_number",
            self.instance.batch_number if self.instance else None
        )

        manufacturing_date = attrs.get(
            "manufacturing_date",
            self.instance.manufacturing_date if self.instance else None
        )

        expiry_date = attrs.get(
            "expiry_date",
            self.instance.expiry_date if self.instance else None
        )

        purchase_price = attrs.get(
            "purchase_price",
            self.instance.purchase_price if self.instance else None
        )

        selling_price = attrs.get(
            "selling_price",
            self.instance.selling_price if self.instance else None
        )

        quantity_received = attrs.get(
            "quantity_received",
            self.instance.quantity_received if self.instance else None
        )

        if medicine and not medicine.is_active:
            raise serializers.ValidationError({
                "medicine": "Cannot create a batch for an inactive medicine."
            })

        if manufacturing_date and expiry_date:
            if expiry_date <= manufacturing_date:
                raise serializers.ValidationError({
                    "expiry_date": "Expiry date must be after manufacturing date."
                })

        if manufacturing_date and manufacturing_date > date.today():
            raise serializers.ValidationError({
                "manufacturing_date": "Manufacturing date cannot be in the future."
            })

        if purchase_price is not None and purchase_price < 0:
            raise serializers.ValidationError({
                "purchase_price": "Purchase price cannot be negative."
            })

        if selling_price is not None and selling_price < 0:
            raise serializers.ValidationError({
                "selling_price": "Selling price cannot be negative."
            })

        if quantity_received is not None and quantity_received <= 0:
            raise serializers.ValidationError({
                "quantity_received": "Quantity received must be greater than zero."
            })

        if self.instance and "quantity_received" in attrs:
            if quantity_received != self.instance.quantity_received:
                raise serializers.ValidationError({
                    "quantity_received": "Received quantity cannot be changed after batch creation."
                })

        if medicine and batch_number:
            existing = Batch.objects.filter(
                medicine=medicine,
                batch_number__iexact=batch_number
            )

            if self.instance:
                existing = existing.exclude(pk=self.instance.pk)

            if existing.exists():
                raise serializers.ValidationError({
                    "batch_number": "This batch number already exists for this medicine."
                })

        return attrs

    @transaction.atomic
    def create(self, validated_data):
        validated_data["available_quantity"] = validated_data[
            "quantity_received"
        ]

        batch = super().create(validated_data)

        StockMovement.objects.create(
            batch=batch,
            movement_type=StockMovement.MovementType.OPENING,
            direction=StockMovement.Direction.IN,
            quantity=batch.quantity_received,
            quantity_before=0,
            quantity_after=batch.quantity_received,
            reference=f"OPENING-{batch.batch_number}",
            notes="Initial stock recorded during batch creation."
        )

        return batch
