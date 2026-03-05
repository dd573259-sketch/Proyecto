from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import Venta, Usuario
from app.forms import VentaForm


class VentaListView(ListView):
    model = Venta
    template_name = 'venta/listar.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        return Venta.objects.select_related('usuario', 'pedido')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Ventas'
        context['icono'] = 'fas fa-cash-register'
        return context


class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'venta/crear.html'
    success_url = reverse_lazy('app:listar_ventas')

    def form_valid(self, form):

        pedido = form.cleaned_data['pedido']

        # usuario temporal para pruebas
        usuario = Usuario.objects.first()

        total = 0

        # obtener detalles del pedido
        detalles = pedido.detalle_productos.all()

        # sumar subtotales
        for detalle in detalles:
            total += detalle.subtotal

        # asignar datos
        form.instance.usuario = usuario
        form.instance.total = total

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Venta'
        context['icono'] = 'fas fa-plus'
        context['listar_url'] = reverse_lazy('app:listar_ventas')
        return context


class VentaUpdateView(UpdateView):
    model = Venta
    fields = '__all__'
    template_name = 'venta/crear.html'
    success_url = reverse_lazy('app:listar_ventas')


class VentaDeleteView(DeleteView):
    model = Venta
    template_name = 'venta/eliminar.html'
    success_url = reverse_lazy('app:listar_ventas')


# pagar venta
def pagar_venta(request, venta_id):

    venta = get_object_or_404(Venta, id_venta=venta_id)

    venta.estado = 'PAGADA'
    venta.save()

    return redirect('app:listar_ventas')

