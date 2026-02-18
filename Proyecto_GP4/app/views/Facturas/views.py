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

class FacturaListView(listView):
    model = Factura
    template_name = 'facturas/listar.html'
    context_object_name = 'facturas' 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Facturas'
        context['crear_url'] = reverse_lazy('app:crear_factura')
        return context   

class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/crear.html'
    success_url = reverse_lazy('app:listar_facturas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Nueva Factura'
        return context
    

class FacturaDeleteView(DeleteView):
    model = Factura
    template_name = 'facturas/eliminar.html'
    success_url = reverse_lazy('app:listar_facturas') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Factura'
        return context


class FacturaUpdateView(UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/editar.html'
    success_url = reverse_lazy('app:listar_facturas') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Factura'
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context

