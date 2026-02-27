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


class CompraListView(listView):        
    model = Compra
    template_name = 'compra/listar.html'
    context_object_name = 'object_list'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['crear_url'] = reverse_lazy('app:crear_compra')
        context['titulo'] = 'Listado de Compras'
        return context

class CompraCreateView(CreateView):
    model = Compra
    form_class = CompraForm
    template_name = 'compra/crear.html'
    success_url = reverse_lazy('app:listar_compras')
    def form_valid(self, form):
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Compra'
        return context


class CompraDeleteView(DeleteView):
    model = Compra
    template_name = 'compra/eliminar.html'
    success_url = reverse_lazy('app:listar_compras')
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Compra'
        return context


class CompraUpdateView(UpdateView):   
    model = Compra
    form_class = CompraForm
    template_name = 'compra/crear.html'
    success_url = reverse_lazy('app:listar_compras')
    def form_valid(self, form):
        return super().form_valid(form)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Compra'
        return context
        