
from django.db.models import Sum, Count
from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from medicines.models import Medicine
from batches.models import Batch


class StockReportView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        today = timezone.localdate()

        total_medicines = Medicine.objects.filter(
            is_active=True
        ).count()

        total_batches = Batch.objects.count()

        total_stock = Batch.objects.aggregate(
            total=Sum("available_quantity")
        )["total"] or 0

        expired_batches = Batch.objects.filter(
            expiry_date__lt=today,
            available_quantity__gt=0
        ).count()

        expiring_soon = Batch.objects.filter(
            expiry_date__gte=today,
            expiry_date__lte=today + timezone.timedelta(days=30),
            available_quantity__gt=0
        ).count()

        low_stock_batches = Batch.objects.filter(
            available_quantity__gt=0,
            available_quantity__lte=10
        ).count()

        return Response({
            "report_date": today,
            "summary": {
                "total_medicines": total_medicines,
                "total_batches": total_batches,
                "total_stock_units": total_stock,
                "expired_batches": expired_batches,
                "expiring_within_30_days": expiring_soon,
                "low_stock_batches": low_stock_batches
            }
        })
