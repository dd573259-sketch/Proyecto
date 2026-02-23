from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.models import Mesa
from app.forms import MesaForm 

class MesaListView(ListView):
    model = Mesa
    template_name = 'Mesa/listar.html'
    context_object_name = 'mesas'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Mesas'
        context['icono'] = 'fas fa-table'
        context['crear_url'] = reverse_lazy('app:crear_mesa')
        return context

class MesaCreateView(CreateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'Mesa/crear.html'
    success_url = reverse_lazy('app:listar_mesas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Registrar Nueva Mesa'
        context['icono'] = 'fas fa-table'
        context['listar_url'] = reverse_lazy('app:listar_mesas')
        return context

class MesaUpdateView(UpdateView):
    model = Mesa
    form_class = MesaForm
    template_name = 'Mesa/crear.html' # Reutilizamos el template de crear
    success_url = reverse_lazy('app:listar_mesas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Actualizar Mesa'
        context['icono'] = 'fas fa-table'
        context['listar_url'] = reverse_lazy('app:listar_mesas')
        return context

# Eliminar mesa
class MesaDeleteView(DeleteView):
    model = Mesa
    template_name = 'Mesa/eliminar.html'
    success_url = reverse_lazy('app:listar_mesas')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fas fa-table'
        context['titulo'] = '¿Eliminar Mesa?'
        context['listar_url'] = reverse_lazy('app:listar_mesas')
        return context