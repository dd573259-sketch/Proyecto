from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import PagoForm


class PagoListView(ListView):

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

    def get_initial(self):
        initial = super().get_initial()
        venta_id = self.kwargs.get('venta_id')
        if venta_id:
            initial['venta'] = get_object_or_404(Venta, id_venta=venta_id)
        return initial

    def form_valid(self, form):
        pago = form.save(commit=False)
        pago.monto = pago.venta.total
        pago.estado = 'PAGADA'
        pago.save()

