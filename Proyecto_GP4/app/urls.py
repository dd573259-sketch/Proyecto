from django.urls import path
from app.views.Categorias.views import *
from app.views.Platos.views import *
from app.views.Notificaciones.views import *
from app.views.Menu.views import *
from app.views.Receta.views import *
from app.views.Insumos.views import *
app_name = 'app'
urlpatterns = [
    #urls de categorias
    #path('listar_categorias/', listar_categorias , name='listar_categorias'),
    path('listar_categorias/', categoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),

    #urls de platos
    path('listar_platos/', PlatoListView.as_view() , name='listar_platos'),
    path('crear_plato/', PlatoCreateView.as_view() , name='crear_plato'),
    path('editar_plato/<int:pk>/', PlatoUpdateView.as_view(), name='editar_plato'),
    path('eliminar_plato/<int:pk>/', PlatoDeleteView.as_view(), name='eliminar_plato'),
    
    # urls de notificaciones
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
    #path('', index , name='index'),
]
