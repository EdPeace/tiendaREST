from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Sale, SaleDetail

from .serializers import VentaReportSerializers, VentaProcesoSerializersPlus


# Este no trabaja con Modelo
class VentasViewSet(viewsets.ViewSet):
    #authentication_classes = (TokenAuthentication,)
    #permission_classes = [IsAuthenticated]
    #serializer_class = VentaReportSerializers
    queryset = Sale.objects.all()

    # se deben sobreescribir estos dos
    def list(self, request):
        serializer = VentaReportSerializers(self.queryset,many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        return Response({'code': 'OK'})

