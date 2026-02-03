from django.urls import path
from app.views import *
app_name = 'app'
urlpatterns = [
    path('listar_categorias/', listar_categorias , name='listar_categorias'),
    #path('', index , name='index'),
]


                                                                                                                                                  