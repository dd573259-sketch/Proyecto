from django.urls import path
from app.views.Categorias.views import *
from app.views.Platos.views import *
from app.views.Notificaciones.views import *
from app.views.Menu.views import *
from app.views.Receta.views import *
from app.views.Insumos.views import *
from app.views.Facturas.views import *
from app.views.Venta.views import *
from app.views.pago.views import *
from app.views.usuario.views import *
from app.views.proveedor.views import *
from app.views.producto.views import *
from app.views.compra.views import *
from app.views.Comanda.views import *
from app.views.Mesa.views import *
from app.views.Pedido.views import *
from app.views.Cliente.views import *

app_name = 'app'
urlpatterns = [
#urls de categorias
    path('listar_categorias/', categoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

#urls de platos
    path('listar_platos/', PlatoListView.as_view() , name='listar_platos'),
    path('crear_plato/', PlatoCreateView.as_view() , name='crear_plato'),
    path('editar_plato/<int:pk>/', PlatoUpdateView.as_view(), name='editar_plato'),
    path('eliminar_plato/<int:pk>/', PlatoDeleteView.as_view(), name='eliminar_plato'),
    
#urls de notificaciones
    path('listar_notificaciones/', notificacionListView.as_view() , name='listar_notificaciones'),
    path('crear_notificacion/', NotificacionCreateView.as_view() , name='crear_notificacion'),
    path('editar_notificacion/<int:pk>/', NotificacionUpdateView.as_view(), name='editar_notificacion'),
    path('eliminar_notificacion/<int:pk>/', NotificacionDeleteView.as_view(), name='eliminar_notificacion'),
    
#MENU
    path('listar_menu/', MenuListView.as_view() , name='listar_menu'),
    path('crear_menu/', MenuCreateView.as_view() , name='crear_menu'),
    path('editar_menu/<int:pk>/', MenuUpdateView.as_view(), name='editar_menu'),
    path('eliminar_menu/<int:pk>/', MenuDeleteView.as_view(), name='eliminar_menu'),
    
#RECETA
    path('listar_receta/', RecetaListView.as_view() , name='listar_receta'),
    path('crear_receta/', RecetaCreateView.as_view() , name='crear_receta'),
    path('editar_receta/<int:pk>/', RecetaUpdateView.as_view(), name='editar_receta'),
    path('eliminar_receta/<int:pk>/', RecetaDeleteView.as_view(), name='eliminar_receta'),
    
#INSUMOS
    path('listar_insumos/', InsumosListView.as_view() , name='listar_insumos'),
    path('crear_insumos/', InsumosCreateView.as_view() , name='crear_insumos'),
    path('editar_insumos/<int:pk>/', InsumosUpdateView.as_view(), name='editar_insumos'),
    path('eliminar_insumos/<int:pk>/', InsumosDeleteView.as_view(), name='eliminar_insumos'),
    
# FACTURAS
    path('listar_facturas/', FacturaListView.as_view() , name='listar_facturas'),
    path('crear_factura/', FacturaCreateView.as_view() , name='crear_factura'),
    path('editar_factura/<int:pk>/', FacturaUpdateView.as_view(), name='editar_factura'),
    path('eliminar_factura/<int:pk>/', FacturaDeleteView.as_view(), name='eliminar_factura'),
    
# VENTAS
    path('listar_ventas/', VentaListView.as_view(), name='listar_ventas'),
    path('crear_venta/', VentaCreateView.as_view(), name='crear_venta'),
    path('eliminar_venta/<int:pk>/', VentaDeleteView.as_view(), name='eliminar_venta'),
    
# PAGOS
    path('listar_pagos/', PagoListView.as_view(), name='listar_pagos'),
    path('crear_pago/', PagoCreateView.as_view(), name='crear_pago'),
    path('editar_pago/<int:pk>/', PagoUpdateView.as_view(), name='editar_pago'),
    path('eliminar_pago/<int:pk>/', PagoDeleteView.as_view(), name='eliminar_pago'),
    
# USUARIOS
    path('listar_usuarios/', UsuarioListView.as_view(), name='listar_usuarios'),
    path('crear_usuario/', UsuarioCreateView.as_view(), name='crear_usuario'),
    path('eliminar_usuario/<int:pk>/', UsuarioDeleteView.as_view(), name='eliminar_usuario'),
    path('editar_usuario/<int:pk>/', UsuarioUpdateView.as_view(), name='editar_usuario'),

#PROVEEDORES

    path('listar_proveedores/', ProveedorListView.as_view(), name='listar_proveedores'),
    path('crear_proveedor/', ProveedorCreateView.as_view(), name='crear_proveedor'),
    path('eliminar_proveedor/<int:pk>/', ProveedorDeleteView.as_view(), name='eliminar_proveedor'),
    path('editar_proveedor/<int:pk>/', ProveedorUpdateView.as_view(), name='editar_proveedor'),

# PRODUCTO
    path('listar_productos/', ProductoListView.as_view(), name='listar_productos'),
    path('crear_producto/', ProductoCreateView.as_view(), name='crear_producto'),
    path('eliminar_producto/<int:pk>/', ProductoDeleteView.as_view(), name='eliminar_producto'),
    path('editar_producto/<int:pk>/', ProductoUpdateView.as_view(), name='editar_producto'),

# COMPRA 
    path('listar_compras/', CompraListView.as_view(), name='listar_compras'),
    path('crear_compra/', CompraCreateView.as_view(), name='crear_compra'),
    path('eliminar_compra/<int:pk>/', CompraDeleteView.as_view(), name='eliminar_compra'),
    path('editar_compra/<int:pk>/', CompraUpdateView.as_view(), name='editar_compra'),
    
# COMANDA
    path('listar_comanda/', ComandaListView.as_view() , name='listar_comandas'),
    
    
# MESA
    path('listar_mesa/', MesaListView.as_view() , name='listar_mesas'),
    path('crear_mesa/', MesaCreateView.as_view() , name='crear_mesa'),
    path('editar_mesa/<int:pk>/', MesaUpdateView.as_view(), name='editar_mesa'),
    path('eliminar_mesa/<int:pk>/', MesaDeleteView.as_view(), name='eliminar_mesa'),
    
# PEDIDO
    path('listar_pedido/', PedidoListView.as_view() , name='listar_pedidos'),
    path('crear_pedido/', PedidoCreateView.as_view() , name='crear_pedido'),
    path('editar_pedido/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('eliminar_pedido/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
    
# CLIENTE
    path('listar_cliente/', ClienteListView.as_view() , name='listar_clientes'),
    path('crear_cliente/', ClienteCreateView.as_view() , name='crear_cliente'),
    path('editar_cliente/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),   
]


