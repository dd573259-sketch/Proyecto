from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from app.models import *
from app.forms import PagoForm
from django.contrib import messages


class PagoListView(ListView):
    model = Pago
    template_name = 'pago/listar.html'
    paginate_by = 15

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
        id_venta = self.kwargs.get('id_venta')  # ✅ nombre correcto
        venta = get_object_or_404(Venta, id_venta=id_venta)
        context['venta'] = venta
        context['titulo'] = 'Registrar Pago'
        context['icono'] = 'fas fa-cash-register'
        return context

    def form_valid(self, form):
        id_venta = self.kwargs.get('id_venta')  # ✅ nombre correcto
        venta = get_object_or_404(Venta, id_venta=id_venta)

        pago = form.save(commit=False)
        pago.venta = venta
        pago.monto = venta.total
        pago.save()

        # ✅ Marcar el pedido como pagado
        pedido = venta.pedido
        pedido.pago = True
        pedido.save()

        messages.success(self.request, "Pago registrado correctamente.")
        return redirect(self.success_url)


class EliminarPagoView(DeleteView):
    model = Pago
    template_name = 'pago/eliminar.html'
    context_object_name = 'object'
    success_url = reverse_lazy('app:listar_pagos')
    pk_url_kwarg = 'pk'

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        id_pago = self.object.id_pago
        id_venta = self.object.venta.id_venta if self.object.venta else None
        response = super().delete(request, *args, **kwargs)
        messages.success(request, f"Pago #{id_pago} de la venta #{id_venta} eliminado correctamente.")
        return response

    def get_context_data(self, **kwargs):
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

        Pago.objects.create(
            venta=venta,
            monto=venta.total,
            metodo_pago=metodo
        )

        # ✅ Marcar el pedido como pagado
        pedido = venta.pedido
        pedido.pago = True
        pedido.save()

        messages.success(request, f"Pago registrado correctamente para la venta #{venta.id_venta}.")
        return redirect('app:listar_pagos')

    return render(request, 'pago/crear.html', {'venta': venta})