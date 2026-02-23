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
        context['icono'] = 'fa-solid fa-clipboard-list'
        context['crear_url'] = reverse_lazy('app:crear_comanda')
        return context

# Crear una nueva comanda
class ComandaCreateView(CreateView):
    model = Comanda
    form_class = ComandaForm
    template_name = 'Comanda/crear.html'
    success_url = reverse_lazy('app:listar_comandas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nueva Comanda'
        return context


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