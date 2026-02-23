from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *
from app.models import Pedido
from app.forms import PedidoForm 


class PedidoListView(ListView):
    model = Pedido
    template_name = 'Pedido/listar.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Pedidos'
        context['crear_url'] = reverse_lazy('app:crear_pedido')
        context['buscar'] = self.request.GET.get('buscar', '')
        context['fecha'] = self.request.GET.get('fecha', '')

        return context
    def get_queryset(self):
        queryset = super().get_queryset()
        estado = self.request.GET.get('buscar')
        fecha = self.request.GET.get('fecha')

        if estado:
            queryset = queryset.filter(estado__icontains=estado)
        
        
        if fecha: 
            queryset = queryset.filter(fecha_hora__date=fecha)


        return queryset
class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Pedido/crear.html'
    success_url = reverse_lazy('app:listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nuevo Pedido'
        return context

class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Pedido/crear.html'
    success_url = reverse_lazy('app:listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Pedido'
        context['listar_url'] = reverse_lazy('app:listar_pedidos')
        return context


class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'Pedido/eliminar.html'
    success_url = reverse_lazy('app:listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = '¿Eliminar Pedido?'
        return context
    
class DetallePedidoView(DetailView):
    model = Pedido
    template_name = "pedido/detalle.html"
    context_object_name = "pedido"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle del Pedido'
        return context