from django.urls import path
from .views import ListarUsuariosView, CrearUsuarioView, EditarUsuarioView, DesactivarUsuarioView, CambiarEstadoUsuarioView
from .permisos_views import ListarPermisosView, EditarPermisosGrupoView

app_name = 'usuarios'

urlpatterns = [
    path('listar/', ListarUsuariosView.as_view(), name='listar'),
    path('crear/', CrearUsuarioView.as_view(), name='crear'),
    path('editar/<int:pk>/', EditarUsuarioView.as_view(), name='editar'),
    path('desactivar/<int:pk>/', DesactivarUsuarioView.as_view(), name='desactivar'),
    path('estado/<int:pk>/', CambiarEstadoUsuarioView.as_view(), name='cambiar_estado'),
    
    # Panel de Permisos
    path('permisos/', ListarPermisosView.as_view(), name='listar_permisos'),
    path('permisos/editar/<int:pk>/', EditarPermisosGrupoView.as_view(), name='editar_permisos'),

]