from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import Venta, Usuario, Pedido
from django.contrib import messages
from app.forms import VentaForm


class VentaListView(ListView):
    model = Venta
    template_name = 'venta/listar.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        # Solo trae ventas que ya existen
        queryset = Venta.objects.select_related('usuario', 'pedido')
        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        if usuario:
            queryset = queryset.filter(usuario__nombre__icontains=usuario)
        if fecha:
            queryset = queryset.filter(fecha_venta__date=fecha)
        if estado == 'pagado':
            queryset = queryset.filter(estado='PAGADA')
        elif estado == 'pendiente':
            queryset = queryset.exclude(estado='PAGADA')

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


class VentaListView(ListView):
    model = Venta
    template_name = 'venta/listar.html'
    context_object_name = 'ventas'

    def get_queryset(self):
        queryset = Venta.objects.select_related('usuario', 'pedido')

        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        if usuario:
            queryset = queryset.filter(usuario__nombre__icontains=usuario)
        if fecha:
            queryset = queryset.filter(fecha_venta__date=fecha)
        if estado == 'pagado':
            queryset = queryset.filter(estado='PAGADA')
        elif estado == 'pendiente':
            queryset = queryset.exclude(estado='PAGADA')

        return queryset
    
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from app.models import Venta, Pedido, Usuario
from app.forms import VentaForm

class VentaCreateView(CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'venta/crear.html'
    success_url = reverse_lazy('app:listar_ventas')

    def form_valid(self, form):
        pedido = form.cleaned_data['pedido']

        # Validar que no exista venta para ese pedido
        if Venta.objects.filter(pedido=pedido).exists():
            messages.error(self.request, f"⚠ El pedido #{pedido.id_pedido} ya tiene una venta registrada.")
            return redirect('app:crear_venta')

        # Validar que el pedido tenga productos o platos
        if not pedido.detalle_productos.exists() and not pedido.detalle_platos.exists():
            messages.error(self.request, f"⚠ No se puede crear una venta sin items en el pedido #{pedido.id_pedido}.")
            return redirect('app:crear_venta')

        # Asignar usuario (puedes cambiarlo según tu lógica)
        usuario = Usuario.objects.first()
        if not usuario:
            messages.error(self.request, "⚠ No hay usuarios disponibles para asignar a la venta.")
            return redirect('app:crear_venta')

        # Asignar total del pedido
        form.instance.usuario = usuario
        form.instance.total = pedido.total

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


# oagar venta
def pagar_venta(request, venta_id):
    venta = get_object_or_404(Venta, id_venta=venta_id)
    venta.estado = 'PAGADA'
    venta.save()
    return redirect('app:listar_ventas')

def crear_venta_desde_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id_pedido=pedido_id)

    if Venta.objects.filter(pedido=pedido).exists():
        messages.error(request, f"⚠ El pedido #{pedido.id_pedido} ya tiene una venta registrada.")
        return redirect('app:listar_ventas')

    if not pedido.detalle_productos.exists() and not pedido.detalle_platos.exists():
        messages.error(request, f"⚠ No se puede crear una venta sin items en el pedido #{pedido.id_pedido}.")
        return redirect('app:listar_ventas')

    usuario = Usuario.objects.first()

    Venta.objects.create(
        pedido=pedido,
        usuario=usuario,
        total=pedido.total
    )

    messages.success(request, f"Venta creada correctamente para el pedido #{pedido.id_pedido}.")
    return redirect('app:listar_ventas')