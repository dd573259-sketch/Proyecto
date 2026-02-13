from django.urls import path
from app.views.Categorias.views import *
from app.views.Facturas.views import *
from app.views.Venta.views import *
from app.views.pago.views import *

app_name = 'app'
urlpatterns = [
    #path('listar_categorias/', listar_categorias , name='listar_categorias'),
    path('listar_categorias/', categoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    
    
    #path('', index , name='index'),
    path('facturas/', FacturaListView.as_view() , name='listar_facturas'),
    path('crear_factura/', FacturaCreateView.as_view() , name='crear_factura'),
    path('editar_factura/<int:pk>/', FacturaUpdateView.as_view(), name='editar_factura'),
    path('eliminar_factura/<int:pk>/', FacturaDeleteView.as_view(), name='eliminar_factura'),
    
    
    path('ventas/', VentaListView.as_view(), name='listar_ventas'),
    path('ventas/crear/', VentaCreateView.as_view(), name='crear_venta'),
    path('eliminar_venta/<int:pk>/', VentaDeleteView.as_view(), name='eliminar_venta'),
    
    
    path('pagos/', PagoListView.as_view(), name='listar_pagos'),
    path('crear_pagos/', PagoCreateView.as_view(), name='crear_pago'),
    path('pagos/editar/<int:pk>/', PagoUpdateView.as_view(), name='editar_pago'),
    path('eliminar_pago/<int:pk>/', PagoDeleteView.as_view(), name='eliminar_pago'),

]
