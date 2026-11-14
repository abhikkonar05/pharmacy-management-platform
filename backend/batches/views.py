from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Batch
from .serializers import BatchSerializer


class BatchListCreateView(generics.ListCreateAPIView):
    queryset = Batch.objects.select_related("medicine").all()
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]


class BatchDetailView(generics.RetrieveUpdateAPIView):
    queryset = Batch.objects.select_related("medicine").all()
    serializer_class = BatchSerializer
    permission_classes = [IsAuthenticated]