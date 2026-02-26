from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import PlatoForm

def index(request):
    return render(request, 'main.html')
# Create your views here.
def listar_platos(request):
    nombre = {
        
        'platos': Plato.objects.all()
    }
    return render(request, 'Plato/listar.html', nombre)

class PlatoListView(listView):
    model = Plato
    template_name = 'Plato/listar.html'
    
    #METODO DISPATCH
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        #if request.method == 'GET':
            #return redirect('app:listar_categorias')    
        return super().dispatch(request, *args, **kwargs)
        
    
    #METODO POST
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    #METODO GET CONTEXT DATA
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Listado de Platos'
        context['icono'] = 'fa-solid fa-utensils'
        context['crear_url'] = reverse_lazy('app:crear_plato')
        return context
    
class PlatoCreateView(CreateView):
    model = Plato
    template_name = 'Plato/crear.html'
    form_class = PlatoForm
    success_url = reverse_lazy('app:listar_platos')
    
    #@method_decorator(csrf_exempt)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Plato'
        context['listar_url'] = reverse_lazy('app:listar_platos')
        context['icono'] = 'fa-solid fa-plus-circle'
        return context
    
    
    
class PlatoUpdateView(UpdateView):
    model = Plato
    form_class = PlatoForm
    template_name = 'Plato/crear.html'
    success_url = reverse_lazy('app:listar_platos')
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Plato'
        context['icono'] = 'fa-solid fa-pen-to-square'
        context['listar_url'] = reverse_lazy('app:listar_platos')
        return context
    
      
class PlatoDeleteView(DeleteView):
    model = Plato
    template_name = 'Plato/eliminar.html'
    success_url = reverse_lazy('app:listar_platos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Plato'
        context['icono'] = 'fa-solid fa-trash'
        context['listar_url'] = reverse_lazy('app:listar_platos')
        return context