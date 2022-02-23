from django.urls import path

from . import views

app_name = "venta_app"

urlpatterns = [
    path('api/sales/report/', views.ReportVentasList.as_view(),name='report'),
    path('api/sales/create/', views.RegistrarVenta.as_view(),name='register'),
    path('api/sales/add/', views.RegistrarVentaPlus.as_view(),name='add'),

]
