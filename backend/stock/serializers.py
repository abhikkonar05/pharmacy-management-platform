from rest_framework import serializers
from .models import StockMovement


class StockMovementSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockMovement
        fields = [
            "id",
            "batch",
            "movement_type",
            "direction",
            "quantity",
            "quantity_before",
            "quantity_after",
            "reference",
            "notes",
            "created_at",
        ]

        read_only_fields = [
            "id",
            "quantity_before",
            "quantity_after",
            "created_at",
        ]

    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError(
                "Quantity must be greater than zero."
            )
        return value