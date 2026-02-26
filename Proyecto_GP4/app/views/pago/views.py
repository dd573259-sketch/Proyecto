from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import PagoForm

class PagoListView(listView):
    model = Pago
    template_name = 'pago/listar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Pagos'
        context['icono'] = 'fas fa-cash-register'
        context['crear_url'] = reverse_lazy('app:crear_pago')
        return context


class PagoCreateView(CreateView):
    model = Pago
    template_name = 'pago/crear.html'
    form_class = PagoForm
    success_url = reverse_lazy('app:listar_pagos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Pago'
        context['icono'] = 'fas fa-cash-register'
        return context


class PagoUpdateView(UpdateView):
    model = Pago
    form_class = PagoForm
    template_name = 'pago/crear.html'
    success_url = reverse_lazy('app:listar_pagos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Pago'
        context['icono'] = 'fas fa-cash-register'
        context['listar_url'] = reverse_lazy('app:listar_pagos')
        return context


class PagoDeleteView(DeleteView):
    model = Pago
    template_name = 'pago/eliminar.html'
    success_url = reverse_lazy('app:listar_pagos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago'
        context['icono'] = 'fas fa-cash-register'
        context['listar_url'] = reverse_lazy('app:listar_pagos')
        return context