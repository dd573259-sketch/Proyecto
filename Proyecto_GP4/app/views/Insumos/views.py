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
    context_object_name = 'object_list'
    paginate_by = 7

    def get_queryset(self):
        queryset = super().get_queryset()

        categoria = self.request.GET.get('categoria')
        stock_bajo = self.request.GET.get('stock_bajo')
        orden = self.request.GET.get('orden')

        if categoria:
            queryset = queryset.filter(categoria_id=categoria)

        if stock_bajo == "1":
            queryset = queryset.filter(stock__lt=10)

        if orden == "desc":
            queryset = queryset.order_by('-stock')
        elif orden == "asc":
            queryset = queryset.order_by('stock')

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['titulo'] = 'Listado de insumos'
        context['icono'] = 'fa-solid fa-boxes-stacked'
        context['crear_url'] = reverse_lazy('app:crear_insumos')
        context['Categoria'] = Categoria.objects.all()
        context['categoria_seleccionada'] = self.request.GET.get('categoria', '')
        context['stock_bajo'] = self.request.GET.get('stock_bajo', '')
        context['orden'] = self.request.GET.get('orden', '')

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

