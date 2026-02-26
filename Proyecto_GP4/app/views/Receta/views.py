from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import *

def index(request):
    return render(request, 'main.html')
# Create your views here.
def listar_receta(request):
    nombre = {
        
        'recetas': Receta.objects.all()
    }
    return render(request, 'receta/listar.html', nombre)


class RecetaListView(listView):
    model = Receta
    template_name = 'receta/listar.html'
    
    
    #METODO DISPATCH
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #if request.method == 'GET':
            #return redirect('app:listar_categorias')    
        return super().dispatch(request, *args, **kwargs)
        
    
    #METODO POST
    def post(sefl, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        return Receta.objects.prefetch_related('detalles__insumo')
    
    #METODO GET CONTEXT DATA
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de recetas'
        context['icono'] = 'fas fa-utensils'
        context['crear_url'] = reverse_lazy('app:crear_receta')
        return context
    
class RecetaCreateView(CreateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/crear.html'
    success_url = reverse_lazy('app:listar_receta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.POST:
            context['formset'] = DetalleFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['formset'] = DetalleFormSet()

        context['titulo'] = 'Crear Receta'
        context['icono'] = 'fas fa-plus-circle'
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)

        return self.render_to_response(self.get_context_data(form=form))
    
    
class RecetaUpdateView(UpdateView):
    model = Receta
    form_class = RecetaForm
    template_name = 'receta/crear.html'
    success_url = reverse_lazy('app:listar_receta')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Receta'
        context['icono'] = 'fas fa-edit'
        context['listar_url'] = reverse_lazy('app:listar_receta')

        if self.request.POST:
            context['formset'] = DetalleFormSet(
                self.request.POST,
                instance=self.object
            )
        else:
            context['formset'] = DetalleFormSet(
                instance=self.object
            )

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return redirect(self.success_url)

        # 🔥 IMPORTANTE: mostrar errores
        print(formset.errors)

        return self.render_to_response(self.get_context_data(form=form))
class RecetaDeleteView(DeleteView):
    model = Receta
    template_name = 'receta/eliminar.html'
    success_url = reverse_lazy('app:listar_receta')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Receta'
        context['icono'] = 'fas fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_receta')
        return context