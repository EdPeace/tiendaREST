from django.shortcuts import render
from rest_framework.authentication import TokenAuthentication
from django.utils import timezone
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from applications.producto.models import Product
from .serializers import VentaReportSerializers, VentaProcesoSerializers,VentaProcesoSerializersPlus
from .models import Sale, SaleDetail


# Create your views here.

class ReportVentasList(ListAPIView):
    serializer_class = VentaReportSerializers

    def get_queryset(self):
        return Sale.objects.all()


class RegistrarVenta(CreateAPIView):
    serializer_class = VentaProcesoSerializers
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = VentaProcesoSerializers(data=request.data)
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
        prod = serializer.validated_data['productos']
        ventas_detalle = []
        for pr in prod:
            p = Product.objects.get(id=pr['pk'])

            venta_detalle = SaleDetail(
                sale=venta,
                product=p,
                count=pr['count'],
                price_purchase=p.price_purchase,
                price_sale=p.price_sale,
            )
            amount+= p.price_sale*pr['count']
            count+=pr['count']
            ventas_detalle.append(venta_detalle)
        venta.amount=amount
        venta.count=count
        venta.save
        SaleDetail.objects.bulk_create(ventas_detalle)
        venta.save()
        return Response({'msj':'What do I spot? A New Happy Owner!'})


class RegistrarVentaPlus(CreateAPIView):
    serializer_class = VentaProcesoSerializersPlus
    authentication_classes = (TokenAuthentication,)
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
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
        for pr,can in zip(prod,cantidades):

            venta_detalle = SaleDetail(
                sale=venta,
                product=pr,
                count=can,
                price_purchase=pr.price_purchase,
                price_sale=pr.price_sale,
            )
            amount+= pr.price_sale*can
            count+=can
            ventas_detalle.append(venta_detalle)
        venta.amount=amount
        venta.count=count
        venta.save
        SaleDetail.objects.bulk_create(ventas_detalle)
        venta.save()
        return Response({'msj':'What do I spot? A New Happy Owner!'})