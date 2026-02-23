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
def listar_insumos(request):
    nombre = {
        
        'insumos': insumos.objects.all()
    }
    return render(request, 'insumos/listar.html', nombre)

class InsumosListView(listView):
    model = insumo
    template_name = 'insumos/listar.html'
    context_object_name = 'insumos'
    
    
    def get_queryset(self):
        queryset = super().get_queryset()
        buscar = self.request.GET.get('buscar', '')
        
        if buscar:
            queryset = queryset.filter(nombre__icontains=buscar)
            
        return queryset
    
    
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
        context['titulo'] = 'Listado de insumos'
        context['icono'] = 'fa-solid fa-boxes-stacked'
        context['crear_url'] = reverse_lazy('app:crear_insumos')
        context['buscar'] = self.request.GET.get('buscar', '')
        return context
    
class InsumosCreateView(CreateView):
    model = insumo
    template_name = 'insumos/crear.html'
    form_class = InsumosForm
    success_url = reverse_lazy('app:listar_insumos')
    
    #@method_decorator(csrf_exempt)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['icono'] = 'fa-solid fa-boxes-stacked'
        context['titulo'] = 'Crear Insumo'
        return context
    
    
    
class InsumosUpdateView(UpdateView):
    model = insumo
    form_class = InsumosForm
    template_name = 'insumos/crear.html'
    success_url = reverse_lazy('app:listar_insumos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Insumo'
        context['icono'] = 'fa-solid fa-boxes-stacked'
        context['listar_url'] = reverse_lazy('app:listar_insumos')
        return context
    
    
class InsumosDeleteView(DeleteView):
    model = insumo
    template_name = 'insumos/eliminar.html'
    success_url = reverse_lazy('app:listar_insumos')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Insumo'
        context['icono'] = 'fa-solid fa-boxes-stacked'
        context['listar_url'] = reverse_lazy('app:listar_insumos')
        return context

