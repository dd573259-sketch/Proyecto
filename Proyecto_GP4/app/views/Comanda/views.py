from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.models import Comanda  
from app.forms import ComandaForm 

# Listar todas las comandas
class ComandaListView(ListView):
    model = Comanda
    template_name = 'Comanda/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Comandas'
        context['crear_url'] = reverse_lazy('app:crear_comanda')
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
    
    def get_queryset(self):
        return Comanda.objects.select_related(
            "pedido",
            "pedido__mesa",
            "pedido__usuario"
        ).prefetch_related(
            "pedido__detalle_platos__plato",
            "pedido__detalle_productos__producto"
        )


class ComandaUpdateView(UpdateView):
    model = Comanda
    form_class = ComandaForm
    template_name = 'Comanda/crear.html' 
    success_url = reverse_lazy('app:listar_comandas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Comanda'
        context['listar_url'] = reverse_lazy('app:listar_comandas')
        return context

# Eliminar comanda
class ComandaDeleteView(DeleteView):
    model = Comanda
    template_name = 'Comanda/eliminar.html'
    success_url = reverse_lazy('app:listar_comandas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = '¿Eliminar Comanda?'
        context['listar_url'] = reverse_lazy('app:listar_comandas')
        return context