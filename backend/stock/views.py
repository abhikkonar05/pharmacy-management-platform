from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError

from .models import StockMovement
from .serializers import StockMovementSerializer
from .services import apply_stock_movement


class StockMovementListCreateView(generics.ListCreateAPIView):

    serializer_class = StockMovementSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return StockMovement.objects.select_related(
            "batch",
            "batch__medicine"
        ).all()

    def perform_create(self, serializer):
        data = serializer.validated_data

        try:
            movement = apply_stock_movement(
                batch_id=data["batch"].id,
                movement_type=data["movement_type"],
                direction=data["direction"],
                quantity=data["quantity"],
                reference=data.get("reference", ""),
                notes=data.get("notes", ""),
            )
        except Exception as exc:
            if hasattr(exc, "messages"):
                raise ValidationError({
                    "stock": exc.messages
                })
            raise

        self.created_movement = movement

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        if hasattr(self, "created_movement"):
            response.data = self.get_serializer(
                self.created_movement
            ).data

        return response