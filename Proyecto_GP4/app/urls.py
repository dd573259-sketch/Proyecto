from django.urls import path
from app.views.Categorias.views import *
from app.views.Comanda.views import *
from app.views.Mesa.views import *
from app.views.Pedido.views import *
from app.views.Cliente.views import *
app_name = 'app'
urlpatterns = [
    #path('listar_categorias/', listar_categorias , name='listar_categorias'),
    path('listar_categorias/', categoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    path('', index , name='index'),
    path('listar_comanda/', ComandaListView.as_view() , name='listar_comandas'),
    path('crear_comanda/', ComandaCreateView.as_view() , name='crear_comanda'),
    path('editar_comanda/<int:pk>/', ComandaUpdateView.as_view(), name='editar_comanda'),
    path('eliminar_comanda/<int:pk>/', ComandaDeleteView.as_view(), name='eliminar_comanda'),
    path('listar_mesa/', MesaListView.as_view() , name='listar_mesas'),
    path('crear_mesa/', MesaCreateView.as_view() , name='crear_mesa'),
    path('editar_mesa/<int:pk>/', MesaUpdateView.as_view(), name='editar_mesa'),
    path('eliminar_mesa/<int:pk>/', MesaDeleteView.as_view(), name='eliminar_mesa'),
    path('listar_pedido/', PedidoListView.as_view() , name='listar_pedidos'),
    path('crear_pedido/', PedidoCreateView.as_view() , name='crear_pedido'),
    path('editar_pedido/<int:pk>/', PedidoUpdateView.as_view(), name='editar_pedido'),
    path('eliminar_pedido/<int:pk>/', PedidoDeleteView.as_view(), name='eliminar_pedido'),
    path('listar_cliente/', ClienteListView.as_view() , name='listar_clientes'),
    path('crear_cliente/', ClienteCreateView.as_view() , name='crear_cliente'),
    path('editar_cliente/<int:pk>/', ClienteUpdateView.as_view(), name='editar_cliente'),
    path('eliminar_cliente/<int:pk>/', ClienteDeleteView.as_view(), name='eliminar_cliente'),
    
    
]
