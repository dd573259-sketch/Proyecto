from django.urls import path
from app.views.Categorias.views import *
from app.views.Platos.views import *
from app.views.Notificaciones.views import *
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
    
    #path('', index , name='index'),
]
