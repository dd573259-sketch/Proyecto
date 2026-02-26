from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from app.models import Cliente  
from app.forms import ClienteForm 

# Listar todas las clientes
class ClienteListView(ListView):
    model = Cliente
    template_name = 'Cliente/listar.html'
    context_object_name = 'clientes'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Clientes'
        context['crear_url'] = reverse_lazy('app:crear_cliente')
        return context

    def get_queryset(self):
        queryset = Cliente.objects.all()
        buscar = self.request.GET.get('buscar')

        if buscar:
            queryset = queryset.filter(numero_documento__icontains=buscar)

        return queryset

# Crear una nueva cliente
class ClienteCreateView(CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Cliente/crear.html'
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nuevo Cliente'
        context['listar_url'] = reverse_lazy('app:listar_clientes')
        return context

# Editar estado o usuario de la cliente
class ClienteUpdateView(UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = 'Cliente/crear.html' # Reutilizamos el template de crear
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Cliente'
        context['listar_url'] = reverse_lazy('app:listar_clientes')
        return context

# Eliminar cliente
class ClienteDeleteView(DeleteView):
    model = Cliente
    template_name = 'Cliente/eliminar.html'
    success_url = reverse_lazy('app:listar_clientes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = '¿Eliminar Cliente?'
        context['listar_url'] = reverse_lazy('app:listar_clientes')
        return context