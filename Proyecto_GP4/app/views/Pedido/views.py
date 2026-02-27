from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
from app.models import Pedido, Plato, Producto, Comanda
import json
from app.forms import PedidoForm, DetallePedidoFormSet, DetallePlatoFormSet


class PedidoListView(ListView):
    model = Pedido
    template_name = 'Pedido/listar.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        queryset = Pedido.objects.all().prefetch_related(
            'detalle_platos__plato',      # platos del pedido
            'detalle_productos__producto', # productos del pedido
            'mesa',
            'usuario'
        )

        estado = self.request.GET.get('buscar')
        fecha = self.request.GET.get('fecha')

        if estado:
            queryset = queryset.filter(estado__icontains=estado)

        if fecha:
            queryset = queryset.filter(fecha_hora__date=fecha)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Gestión de Pedidos'
        context['icono'] = 'fas fa-shopping-cart'
        context['crear_url'] = reverse_lazy('app:crear_pedido')
        context['buscar'] = self.request.GET.get('buscar', '')
        context['fecha'] = self.request.GET.get('fecha', '')
        return context


class PedidoCreateView(CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Pedido/crear.html'
    success_url = reverse_lazy('app:listar_pedidos')

    def get_context_data(self, **kwargs):
        """
        Mandamos al template dos formsets:
        - formset_platos   → para agregar múltiples platos
        - formset_productos → para agregar múltiples productos
        """
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset_platos'] = DetallePlatoFormSet(self.request.POST)
            context['formset_productos'] = DetallePedidoFormSet(self.request.POST)
        else:
            context['formset_platos'] = DetallePlatoFormSet()
            context['formset_productos'] = DetallePedidoFormSet()

        context['titulo'] = 'Registrar Nuevo Pedido'
        context['icono'] = 'fas fa-shopping-cart'
        context['listar_url'] = reverse_lazy('app:listar_pedidos')
        # Datos usados por el template
        platos_qs = Plato.objects.all()
        productos_qs = Producto.objects.all()
        context['platos'] = platos_qs
        context['productos'] = productos_qs
        context['platos_json'] = json.dumps({p.id_plato: float(p.precio) for p in platos_qs})
        context['productos_json'] = json.dumps({p.id_producto: float(p.precio) for p in productos_qs})
        context['stock_json'] = json.dumps({p.id_producto: int(p.stock) for p in productos_qs})
        return context

    def form_valid(self, form):
        """
        Guardamos el Pedido primero, luego los
        platos y productos asociados al pedido.
        Solo guardamos si ambos formsets son válidos.
        """
        context = self.get_context_data()
        formset_platos = context['formset_platos']
        formset_productos = context['formset_productos']

        if formset_platos.is_valid() and formset_productos.is_valid():
            # Guardamos el pedido principal
            self.object = form.save()

            # Guardamos platos: rellenar precio_unitario antes de persistir
            formset_platos.instance = self.object
            for form_plato in formset_platos.forms:
                cleaned = form_plato.cleaned_data
                # Solo procesar si no está marcado para eliminar y tiene datos válidos
                if cleaned.get('plato') and not cleaned.get('DELETE', False):
                    form_plato.instance.precio_unitario = cleaned['plato'].precio
            formset_platos.save()

            # Guardamos productos: rellenar precio_unitario antes de persistir
            formset_productos.instance = self.object
            for form_producto in formset_productos.forms:
                cleaned = form_producto.cleaned_data
                # Solo procesar si no está marcado para eliminar y tiene datos válidos
                if cleaned.get('producto') and not cleaned.get('DELETE', False):
                    form_producto.instance.precio_unitario = cleaned['producto'].precio
            formset_productos.save()
            
            Comanda.objects.create(
                pedido=self.object,
                usuario=self.object.usuario,
                estado="Preparación"
            )

            return redirect(self.success_url)

        # Si algo falló, volvemos al formulario con los errores
        return self.render_to_response(self.get_context_data(form=form))
        
    


class PedidoUpdateView(UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'Pedido/crear.html'
    success_url = reverse_lazy('app:listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset_platos'] = DetallePlatoFormSet(
                self.request.POST,
                instance=self.object
            )
            context['formset_productos'] = DetallePedidoFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            # Al editar, cargamos los platos y productos que ya tiene el pedido
            context['formset_platos'] = DetallePlatoFormSet(
                instance=self.object
            )
            context['formset_productos'] = DetallePedidoFormSet(
                instance=self.object
            )

        context['titulo'] = 'Actualizar Pedido'
        context['icono'] = 'fas fa-shopping-cart'
        context['listar_url'] = reverse_lazy('app:listar_pedidos')
        # Datos usados por el template
        platos_qs = Plato.objects.all()
        productos_qs = Producto.objects.all()
        context['platos'] = platos_qs
        context['productos'] = productos_qs
        context['platos_json'] = json.dumps({p.id_plato: float(p.precio) for p in platos_qs})
        context['productos_json'] = json.dumps({p.id_producto: float(p.precio) for p in productos_qs})
        context['stock_json'] = json.dumps({p.id_producto: int(p.stock) for p in productos_qs})
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_platos = context['formset_platos']
        formset_productos = context['formset_productos']

        if formset_platos.is_valid() and formset_productos.is_valid():
            self.object = form.save()

            # Guardamos platos: rellenar precio_unitario antes de persistir
            formset_platos.instance = self.object
            for form_plato in formset_platos.forms:
                cleaned = form_plato.cleaned_data
                if cleaned.get('plato') and not cleaned.get('DELETE', False):
                    form_plato.instance.precio_unitario = cleaned['plato'].precio
            formset_platos.save()

            # Guardamos productos: rellenar precio_unitario antes de persistir
            formset_productos.instance = self.object
            for form_producto in formset_productos.forms:
                cleaned = form_producto.cleaned_data
                if cleaned.get('producto') and not cleaned.get('DELETE', False):
                    form_producto.instance.precio_unitario = cleaned['producto'].precio
            formset_productos.save()

            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))


class PedidoDeleteView(DeleteView):
    model = Pedido
    template_name = 'Pedido/eliminar.html'
    success_url = reverse_lazy('app:listar_pedidos')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = '¿Eliminar Pedido?'
        context['listar_url'] = reverse_lazy('app:listar_pedidos')
        return context


class DetallePedidoView(DetailView):
    model = Pedido
    template_name = "Pedido/detalle.html"
    context_object_name = "pedido"

    def get_queryset(self):
        """
        Traemos todos los platos y productos del pedido
        en una sola consulta para no sobrecargar la BD.
        """
        return Pedido.objects.prefetch_related(
            'detalle_platos__plato',
            'detalle_productos__producto',
            'mesa',
            'usuario'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Detalle del Pedido'
        return context