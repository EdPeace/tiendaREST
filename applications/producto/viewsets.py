from rest_framework import viewsets
from rest_framework.response import Response

from .models import Colors, Product

from .serializers import ColorSerializer, ProductSerializerVS, PaginationSerializer


class ColorViewSet(viewsets.ModelViewSet):
    serializer_class = ColorSerializer
    queryset = Colors.objects.all()


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializerVS
    queryset = Product.objects.all()
    pagination_class = PaginationSerializer

    def perform_create(self, serializer):
        serializer.save(video="Link Aqui")
