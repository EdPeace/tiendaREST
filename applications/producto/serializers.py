from rest_framework import serializers, pagination
#
from .models import Product, Colors


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Colors
        fields = ('color',)


class ProductSerializer(serializers.ModelSerializer):
    colors = ColorSerializer(many=True)

    class Meta:
        model = Product
        fields = ('__all__')


class PaginationSerializer(pagination.PageNumberPagination):
    page_size = 5
    max_page_size = 50


class ProductSerializerVS(serializers.ModelSerializer):
    # colors = ColorSerializer(many=True)
    class Meta:
        model = Product
        fields = ('__all__')
