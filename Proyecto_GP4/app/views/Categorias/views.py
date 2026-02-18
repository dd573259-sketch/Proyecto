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
def listar_categorias(request):
    nombre = {
        
        'categorias': Categoria.objects.all()
    }
    return render(request, 'Categoria/listar.html', nombre)

class categoriaListView(listView):
    model = Categoria
    template_name = 'Categoria/listar.html'
    
    #METODO DISPATCH
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #if request.method == 'GET':
            #return redirect('app:listar_categorias')    
        return super().dispatch(request, *args, **kwargs)
        
    
    #METODO POST
    def post(sefl, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    #METODO GET CONTEXT DATA
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Categorias'
        context['crear_url'] = reverse_lazy('app:crear_categoria')
        return context
    
class CategoriaCreateView(CreateView):
    model = Categoria
    template_name = 'Categoria/crear.html'
    form_class = CategoriaForm
    success_url = reverse_lazy('app:listar_categorias')
    
    #@method_decorator(csrf_exempt)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Categoria'
        return context
    
    
    
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'Categoria/crear.html'
    success_url = reverse_lazy('app:listar_categorias')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Categoria'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context
    
    
class CategoriaDeleteView(DeleteView):
    model = Categoria
    template_name = 'categoria/eliminar.html'
    success_url = reverse_lazy('app:listar_categorias')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Categoria'
        context['listar_url'] = reverse_lazy('app:listar_categorias')
        return context