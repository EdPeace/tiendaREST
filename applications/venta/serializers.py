from rest_framework import serializers

from .models import Sale, SaleDetail


class DetalleVentaProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetail
        fields = ('__all__')


class VentaReportSerializers(serializers.ModelSerializer):
    productos = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = (
            'id',
            'date_sale',
            'amount',
            'count',
            'type_invoce',
            'cancelado',
            'type_payment',
            'state',
            'adreese_send',
            'user',
            'productos'
        )

    def get_productos(self, obj):
        query = SaleDetail.objects.productos_por_venta(obj.id)
        productos_serializados = DetalleVentaProductoSerializer(query, many=True).data
        return productos_serializados


class ProductDetailSerializers(serializers.Serializer):
    pk = serializers.IntegerField()
    count = serializers.IntegerField()


class VentaProcesoSerializers(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos = ProductDetailSerializers(many=True)


class ArrayIntegerSerializer(serializers.ListField):
    child = serializers.IntegerField()


class VentaProcesoSerializersPlus(serializers.Serializer):
    type_invoce = serializers.CharField()
    type_payment = serializers.CharField()
    adreese_send = serializers.CharField()
    productos =  ArrayIntegerSerializer()
    count = ArrayIntegerSerializer()
