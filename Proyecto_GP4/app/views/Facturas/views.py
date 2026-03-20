from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView,DetailView, View
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *
from django.shortcuts import get_object_or_404
from django.contrib import messages

class FacturaListView(listView):
    model = Factura
    template_name = 'facturas/listar.html'
    context_object_name = 'facturas' 
    paginate_by = 5
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Facturas'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        context['crear_url'] = reverse_lazy('app:crear_factura')
        
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

def crear_factura(request, pago_id):

    pago = get_object_or_404(Pago, id_pago=pago_id)

    if pago.factura:
        messages.warning(request, "Este pago ya tiene factura generada.")
        return redirect('app:listar_pagos')

    factura = Factura.objects.create(
        venta=pago.venta,
        valor_total=pago.monto,
        metodo_pago=pago.metodo_pago
    )

    pago.factura = factura.id
    pago.save()

    messages.success(request, f"Factura #{factura.id} creada correctamente.")

    return redirect('app:listar_facturas')

class FacturaDetailView(DetailView):
    model = Factura
    template_name = 'facturas/detalle.html'
    context_object_name = 'factura'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle de Factura'
        context['icono'] = 'fa-solid fa-file-invoice-dollar'
        return context
    