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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        venta_id = self.kwargs.get('venta_id')
        venta = get_object_or_404(Venta, id_venta=venta_id)

        context['venta'] = venta

        return context

    def form_valid(self, form):

        venta_id = self.kwargs.get('venta_id')
        venta = get_object_or_404(Venta, id_venta=venta_id)

        pago = form.save(commit=False)
        pago.venta = venta
        pago.monto = venta.total   # 👈 se toma automáticamente
        pago.estado = 'PAGADA'
        pago.save()

        return super().form_valid(form)
    
class EliminarPagoView(DeleteView):
    model = Pago
    template_name = 'pago/eliminar.html'
    context_object_name = 'object'
    success_url = reverse_lazy('app:listar_pagos')
    pk_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        """Agregar mensaje de éxito al eliminar"""
        self.object = self.get_object()
        pago_id = self.object.id_pago
        venta_id = self.object.venta.id_venta if self.object.venta else None
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Pago #{pago_id} de la venta #{venta_id} eliminado correctamente.")
        return response

    def get_context_data(self, **kwargs):
        """Pasar la URL de listado al template para el botón Cancelar"""
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Pago'
        context['listar_url'] = reverse_lazy('app:listar_ventas')
        return context

def registrar_pago(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)

    if request.method == "POST":
        metodo = request.POST.get('metodo_pago')

        if not metodo:
            messages.error(request, "⚠ Debes seleccionar un método de pago.")
            return redirect('app:crear_pago', venta_id=venta.id_venta)

        # Crear el pago
        Pago.objects.create(
            venta=venta,
            monto=venta.total,
            metodo_pago=metodo
        )

        # Marcar la venta como pagada
        venta.estado = "PAGADA"
        venta.save()

        messages.success(request, f"Pago registrado correctamente para la venta #{venta.id_venta}.")

        # Redirigir a listar pagos
        return redirect('app:listar_pagos')

    # Si no es POST, mostramos el formulario
    return render(request, 'pago/crear.html', {'venta': venta})