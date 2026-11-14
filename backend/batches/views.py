from rest_framework import generics
from rest_framework.permissions import AllowAny

from .models import Batch
from .serializers import BatchSerializer


class BatchListCreateView(generics.ListCreateAPIView):
    queryset = Batch.objects.select_related("medicine").all()
    serializer_class = BatchSerializer
    permission_classes = [AllowAny]


class BatchDetailView(generics.RetrieveUpdateAPIView):
    queryset = Batch.objects.select_related("medicine").all()
    serializer_class = BatchSerializer
    permission_classes = [AllowAny]