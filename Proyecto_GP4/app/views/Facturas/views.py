from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView,DetailView, View, DeleteView, ListView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages
from itertools import groupby
from django.db.models.functions import TruncMonth

class FacturaListView(listView): 
    model = Factura
    template_name = 'facturas/listar.html'
    context_object_name = 'facturas'
    paginate_by = 5
    ordering = ('-fecha_hora',)

    def get_queryset(self):
        queryset = Factura.objects.select_related('venta', 'venta__usuario', 'venta__pedido')
        usuario = self.request.GET.get('usuario')
        fecha = self.request.GET.get('fecha')
        estado = self.request.GET.get('estado')

        # Filtrar solo el mes actual por defecto
        hoy = timezone.now()
        queryset = queryset.filter(
            fecha_hora__year=hoy.year,
            fecha_hora__month=hoy.month
        )

        # 🔍 Filtros (ajustados a tu modelo)
        if usuario:
            queryset = queryset.filter(venta__usuario__nombre__icontains=usuario)

        if fecha:
            queryset = queryset.filter(fecha_hora__date=fecha)

        if estado == 'pagado':
            queryset = queryset.filter(activo=True)
        elif estado == 'pendiente':
            queryset = queryset.filter(activo=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Facturas'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['usuario'] = self.request.GET.get('usuario', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        context['estado'] = self.request.GET.get('estado', '')
        context['mes_actual'] = timezone.now().strftime('%B %Y').capitalize()
        return context

class FacturaCreateView(CreateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/crear.html'
    success_url = reverse_lazy('app:listar_facturas')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['titulo'] = 'Crear Nueva Factura'
        return context
    

class FacturaDesactivarView(View):
    
    def get(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)
        if not factura.activo:
            messages.warning(request, "Esta factura ya está desactivada.")
            return redirect('app:listar_facturas')
        return render(request, 'facturas/desactivar.html', {
            'object': factura,
            'titulo': 'Desactivar Factura',      # ← añadir
            'icono': 'fa-solid fa-ban',           # ← añadir
        })

    def post(self, request, pk):
        factura = get_object_or_404(Factura, pk=pk)

        observacion = request.POST.get('observacion', '').strip()
        if not observacion:
            messages.error(request, "⚠ Debes ingresar una observación para desactivar la factura.")
            return render(request, 'facturas/desactivar.html', {
                'object': factura,
                'titulo': 'Desactivar Factura',  # ← añadir también aquí
                'icono': 'fa-solid fa-ban',
            })

        factura.activo = False
        factura.observacion = observacion
        factura.save()

        Pago.objects.filter(venta=factura.venta).update(activo=False)

        factura.venta.activo = False
        factura.venta.save()

        messages.success(request, f"Factura #{factura.id} desactivada correctamente.")
        return redirect('app:listar_facturas')



class FacturaUpdateView(UpdateView):
    model = Factura
    form_class = FacturaForm
    template_name = 'facturas/editar.html'
    success_url = reverse_lazy('app:listar_facturas') 
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Factura'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['listar_url'] = reverse_lazy('app:listar_facturas')
        return context


class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'facturas/detalle.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Factura'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        return context

class FacturaHistorialView(ListView):
    model = Factura
    template_name = 'facturas/historial.html'
    context_object_name = 'facturas'
    paginate_by = 5


    def get_queryset(self):
        queryset = Factura.objects.select_related('venta').order_by('-fecha_hora')

        mes = self.request.GET.get('mes')

        if mes:
            año, mes_num = mes.split('-')
            queryset = queryset.filter(
                fecha_hora__year=año,
                fecha_hora__month=mes_num
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Historial de Facturas por Mes'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'

        facturas = context['facturas']
        historial = {}

        for factura in facturas:
            clave = factura.fecha_hora.strftime('%B %Y').capitalize()
            if clave not in historial:
                historial[clave] = []
            historial[clave].append(factura)

        context['historial'] = historial
        context['mes_seleccionado'] = self.request.GET.get('mes', '')

        return context
    
def crear_factura(request, pago_id):
    pago = get_object_or_404(Pago, id_pago=pago_id)

    if pago.factura:
        messages.warning(request, "Este pago ya tiene factura generada.")
        return redirect('app:listar_pagos')

    if pago.venta and Factura.objects.filter(venta=pago.venta, activo=True).exists():
        messages.warning(request, "Esta venta ya tiene una factura activa.")
        return redirect('app:listar_pagos')

    factura = Factura.objects.create(
        venta=pago.venta,
        valor_total=pago.monto,
        metodo_pago=pago.metodo_pago
    )

    pago.factura = str(factura.id)
    pago.save()

    messages.success(request, f"Factura #{factura.id} creada correctamente.")
    return redirect('app:listar_facturas')