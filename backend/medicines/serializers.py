
from rest_framework import serializers
from .models import Medicine


class MedicineSerializer(serializers.ModelSerializer):

    class Meta:
        model = Medicine

        fields = [
            "id",
            "medicine_code",
            "name",
            "generic_name",
            "manufacturer",
            "strength",
            "dosage_form",
            "category",
            "prescription_required",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_medicine_code(self, value):
        code = value.strip().upper()

        existing = Medicine.objects.filter(
            medicine_code__iexact=code
        )

        if self.instance:
            existing = existing.exclude(pk=self.instance.pk)

        if existing.exists():
            raise serializers.ValidationError(
                "This medicine code already exists."
            )

        return code

    def validate_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Medicine name cannot be empty."
            )

        return value

    def validate_generic_name(self, value):
        value = value.strip()

        if not value:
            raise serializers.ValidationError(
                "Generic name cannot be empty."
            )

        return value
