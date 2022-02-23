from django.shortcuts import render
#
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer

from .models import Product


# Create your views here.

class ListProductUser(ListAPIView):
    serializer_class = ProductSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        usuario = self.request.user
        print(Product.objects.productos_por_user(usuario))
        return Product.objects.productos_por_user(usuario)


class ListProductoStock(ListAPIView):
    serializer_class = ProductSerializer
    # authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        usuario = self.request.user
        print(Product.objects.productos_con_stock())
        return Product.objects.productos_con_stock()


class ListProductoGenero(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        genero = self.kwargs['gender']
        return Product.objects.productos_por_genero(genero)


class FiltrarProductos(ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        male = self.request.query_params.get('man', False)
        female = self.request.query_params.get('woman', False)
        name = self.request.query_params.get('name', False)
        print(male, female, name)
        return Product.objects.filtrar_productos(man=male, woman=female, name=name)
