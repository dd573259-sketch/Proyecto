from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *


class ProveedorListView(listView):        
    model = Proveedor
    template_name = 'proveedor/listar.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('app:crear_proveedor')
        context['icono'] = 'fas fa-truck'
        context['titulo'] = 'Listado de Proveedor'
        return context


class ProveedorCreateView(CreateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Proveedor'
        context['icono'] = 'fas fa-plus-circle'
        return context
    

class ProveedorDeleteView(DeleteView):
    model = Proveedor
    template_name = 'proveedor/eliminar.html'
    success_url = reverse_lazy('app:listar_proveedores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context
        context['titulo'] = 'Eliminar Proveedor'
        return context


class ProveedorUpdateView(UpdateView):
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'proveedor/crear.html'
    success_url = reverse_lazy('app:listar_proveedores')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fas fa-edit'
        context['titulo'] = 'Editar Proveedor'
        return context