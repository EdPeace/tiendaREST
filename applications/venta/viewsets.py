from datetime import timezone

from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Sale, SaleDetail

from .serializers import VentaReportSerializers, VentaProcesoSerializersPlus
from applications.producto.models import Product


# Este no trabaja con Modelo
# Al trabajar con viewset se reescribe todito
class VentasViewSet(viewsets.ViewSet):
    serializer_class = VentaReportSerializers
    queryset = Sale.objects.all()

    def get_permissions(self):
        if self.action == 'list':
            permission_classes = [AllowAny]
        else:
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    # se deben sobreescribir estos dos
    def list(self, request):
        serializer = VentaReportSerializers(self.queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = VentaProcesoSerializersPlus(data=request.data)
        serializer.is_valid(raise_exception=True)
        venta = Sale.objects.create(
            date_sale=timezone.now(),
            amount=0,
            count=0,
            type_invoce=serializer.validated_data['type_invoce'],
            type_payment=serializer.validated_data['type_payment'],
            adreese_send=serializer.validated_data['adreese_send'],
            user=self.request.user,
        )
        amount = 0
        count = 0
        prod = Product.objects.filter(
            id__in=serializer.validated_data['productos']
        )
        cantidades = serializer.validated_data['count']
        ventas_detalle = []
        for pr, can in zip(prod, cantidades):
            venta_detalle = SaleDetail(
                sale=venta,
                product=pr,
                count=can,
                price_purchase=pr.price_purchase,
                price_sale=pr.price_sale,
            )
            amount += pr.price_sale * can
            count += can
            ventas_detalle.append(venta_detalle)
        venta.amount = amount
        venta.count = count
        venta.save
        SaleDetail.objects.bulk_create(ventas_detalle)
        venta.save()
        return Response({'msj': 'What do I spot? A New Happy Owner!'})

    def retrieve(self, request, pk=None):
        #venta = Sale.objects.get(id=pk)
        venta = get_object_or_404(Sale.objects.all(), pk=pk)
        serializer = VentaReportSerializers(venta)
        return Response(serializer.data)
