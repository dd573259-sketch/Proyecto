from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from app.models import Receta, DetalleReceta, insumo
from app.forms import RecetaForm, DetalleFormSet

class RecetaListView(ListView):
    model = Receta
    template_name = 'receta/listar.html'
    
    def get_queryset(self):
        # Programación Senior: Evitamos el problema N+1 con prefetch_related
        return Receta.objects.prefetch_related('detalles__insumo')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        recetas_data = []
        for receta in context['object_list']:
            detalles_data = []
            for detalle in receta.detalles.all():
                # Traemos los datos crudos y directos de la base de datos
                detalles_data.append({
                    'insumo_nombre': detalle.insumo.nombre,
                    'cantidad': float(detalle.cantidad),
                    'unidad': detalle.insumo.unidad,  # Directo del modelo insumo
                    'precio_unitario': float(detalle.insumo.valor),
                    'stock_suficiente': detalle.insumo.stock >= detalle.cantidad,
                })
            
            recetas_data.append({
                'id': receta.id,
                'plato_nombre': receta.plato.nombre,
                'detalles': detalles_data,
            })
        
        context.update({
            'recetas_data': recetas_data,
            'titulo': 'Gestión de Recetas',
            'crear_url': reverse_lazy('app:crear_receta')
        })
        return context

class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/crear.html'
    success_url = reverse_lazy('app:listar_receta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = DetalleFormSet(self.request.POST or None)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)
        return self.render_to_response(context)

class RecetaUpdateView(UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/crear.html'
    success_url = reverse_lazy('app:listar_receta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = DetalleFormSet(self.request.POST or None, instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            form.save()
            formset.save()
            return redirect(self.success_url)
        return self.render_to_response(context)

class RecetaDeleteView(DeleteView):
    model = Receta
    template_name = 'receta/eliminar.html'
    success_url = reverse_lazy('app:listar_receta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Receta'
        context['icono'] = 'fa-solid fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_receta')
        return context