from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from app.models import Cliente  
from app.forms import ClienteForm
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import Http404

# Listar todas las clientes
class ClienteListView(PermissionRequiredMixin,ListView):
    model = Cliente
    template_name = 'Cliente/listar.html'
    context_object_name = 'clientes'
    permission_required = "app.view_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        raise Http404("No se encontro la pagina")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Clientes'
        context['icono'] = 'fa-solid fa-users'
        context['crear_url'] = reverse_lazy('app:crear_cliente')
        context['buscar'] = self.request.GET.get('buscar', '')
        return context

    def get_queryset(self):
        queryset = Cliente.objects.all()
        buscar = self.request.GET.get('buscar')

        if buscar:
            queryset = queryset.filter(numero_documento__icontains=buscar)

        return queryset

# Crear una nueva cliente
class ClienteCreateView(PermissionRequiredMixin,CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Cliente/crear.html'
    success_url = reverse_lazy('app:listar_clientes')
    permission_required = "app.add_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        raise Http404("No se encontro la pagina")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-user-plus'
        context['titulo'] = 'Registrar Nuevo Cliente'
        context['listar_url'] = reverse_lazy('app:listar_clientes')
        return context

# Editar estado o usuario de la cliente
class ClienteUpdateView(PermissionRequiredMixin,UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Cliente/crear.html' # Reutilizamos el template de crear
    success_url = reverse_lazy('app:listar_clientes')
    permission_required = "app.change_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        raise Http404("No se encontro la pagina")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Cliente'
        context['icono'] = 'fa-solid fa-user-edit'
        context['listar_url'] = reverse_lazy('app:listar_clientes')
        return context

# Eliminar cliente
class ClienteDeleteView(PermissionRequiredMixin,DeleteView):
    model = Cliente
    template_name = 'Cliente/eliminar.html'
    success_url = reverse_lazy('app:listar_clientes')
    permission_required = "app.delete_categoria"
    raise_exception = True
    
    def handle_no_permission(self):
        raise Http404("No se encontro la pagina")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-user-xmark'
        context['titulo'] = '¿Eliminar Cliente?'
        context['listar_url'] = reverse_lazy('app:listar_clientes')
        return context