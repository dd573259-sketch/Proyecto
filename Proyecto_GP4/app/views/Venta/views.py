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

        queryset = Venta.objects.select_related('usuario', 'pedido')

        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        # filtro por usuario
        if usuario:
            queryset = queryset.filter(usuario__nombre__icontains=usuario)

        # filtro por fecha
        if fecha:
            queryset = queryset.filter(fecha_venta__date=fecha)

        # filtro por estado de pago
        if estado == 'pagado':
            queryset = queryset.filter(pago__estado='PAGADA')
        elif estado == 'pendiente':
            queryset = queryset.exclude(pago__estado='PAGADA')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Listado de Ventas'
        context['icono'] = 'fas fa-cash-register'

        # mantener filtros en el input
        context['usuario'] = self.request.GET.get('usuario', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        context['estado'] = self.request.GET.get('estado', '')

        return context


from django.contrib import messages

class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'venta/crear.html'
    success_url = reverse_lazy('app:listar_ventas')

    def form_valid(self, form):

        pedido = form.cleaned_data['pedido']

        # VALIDACION 1: verificar si ya existe una venta para ese pedido
        if Venta.objects.filter(pedido=pedido).exists():

            messages.error(self.request, "⚠ Este pedido ya tiene una venta registrada.")

            return redirect('app:crear_venta')

        # VALIDACION 2: verificar que el pedido tenga productos
        detalles = pedido.detalle_productos.all()

        if not detalles.exists():

            messages.error(self.request, "⚠ No se puede crear una venta sin productos en el pedido.")

            return redirect('app:crear_venta')

        # usuario temporal
        usuario = Usuario.objects.first()

        total = 0

        for detalle in detalles:
            total += detalle.subtotal

        form.instance.usuario = usuario
        form.instance.total = total

        return super().form_valid(form)


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

