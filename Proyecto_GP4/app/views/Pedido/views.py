from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import *
from app.models import Pedido
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

            # Asociamos y guardamos los platos
            formset_platos.instance = self.object
            formset_platos.save()

            # Asociamos y guardamos los productos
            formset_productos.instance = self.object
            formset_productos.save()

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
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset_platos = context['formset_platos']
        formset_productos = context['formset_productos']

        if formset_platos.is_valid() and formset_productos.is_valid():
            self.object = form.save()

            formset_platos.instance = self.object
            formset_platos.save()

            formset_productos.instance = self.object
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