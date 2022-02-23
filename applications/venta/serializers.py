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

    def validate(self, attrs):
        if attrs['type_payment'] != '0' or attrs['type_payment'] != '1' or attrs['type_payment'] != '2':
            raise serializers.ValidationError('Ingresa un tipo de pago correctos')
        return attrs
    def validate_type_invoce(self,value):
        if value != '0' or value != '3' or value != '4':
            raise serializers.ValidationError('Ingresa Valores correctos')
        return value
