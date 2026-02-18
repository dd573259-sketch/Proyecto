from django.urls import path
from app.views.Categorias.views import *
from app.views.Usuario.views import *
from app.views.Proveedor.views import *
from app.views.Producto.views import *
from app.views.Compra.views import *

app_name = 'app'
urlpatterns = [
    #path('listar_categorias/', listar_categorias , name='listar_categorias'),
    path('listar_categorias/', categoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

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
    

]


