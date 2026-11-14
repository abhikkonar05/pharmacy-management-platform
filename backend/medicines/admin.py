
from django.contrib import admin
from .models import Medicine


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "medicine_code",
        "name",
        "generic_name",
        "manufacturer",
        "strength",
        "is_active",
    )

    search_fields = (
        "medicine_code",
        "name",
        "generic_name",
        "manufacturer",
    )

    list_filter = (
        "category",
        "dosage_form",
        "prescription_required",
        "is_active",
    )

    ordering = ("name",)
