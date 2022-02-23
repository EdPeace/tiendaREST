from django.urls import path

from . import views

app_name="producto_app"

urlpatterns = [
    path('api/product/por-usuario/',views.ListProductUser.as_view(),name='by_user'),
    path('api/product/por-stock/',views.ListProductoStock.as_view(),name='by_stock'),
    path('api/product/por-genero/<gender>/',views.ListProductoGenero.as_view(),name='by_gender'),
    path('api/product/filtrar/',views.FiltrarProductos.as_view(),name='filter'),
]