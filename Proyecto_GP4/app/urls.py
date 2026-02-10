from django.urls import path
from app.views.Categorias.views import *
app_name = 'app'
urlpatterns = [
    #path('listar_categorias/', listar_categorias , name='listar_categorias'),
    path('listar_categorias/', categoriaListView.as_view() , name='listar_categorias'),
    path('crear_categoria/', CategoriaCreateView.as_view() , name='crear_categoria'),
    path('editar_categoria/<int:pk>/', CategoriaUpdateView.as_view(), name='editar_categoria'),
    path('eliminar_categoria/<int:pk>/', CategoriaDeleteView.as_view(), name='eliminar_categoria'),
    #path('', index , name='index'),
]
