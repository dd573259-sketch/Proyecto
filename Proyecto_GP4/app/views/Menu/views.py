from django.shortcuts import render, redirect, get_object_or_404
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
def listar_menu(request):
    nombre = {
        
        'menu': menu.objects.all()
    }
    return render(request, 'menu/listar.html', nombre)

class MenuListView(listView):
    model = Menu
    template_name = 'menu/listar.html'
    
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
        context['titulo'] = 'Listado de menu'
        context['crear_url'] = reverse_lazy('app:crear_menu')
        return context
    
class MenuCreateView(CreateView):
    model = Menu
    template_name = 'menu/crear.html'
    form_class = MenuForm
    success_url = reverse_lazy('app:listar_menu')
    
    #@method_decorator(csrf_exempt)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Menu'
        return context
    
    
    
'''class MenuUpdateView(UpdateView):
    model = Menu
    form_class = MenuForm
    template_name = 'menu/crear.html'
    success_url = reverse_lazy('app:listar_menu')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Menu'
        context['listar_url'] = reverse_lazy('app:listar_menu')
        return context'''

def editar_menu(request, pk):
    menu = get_object_or_404(Menu, pk=pk)

    if menu.plato:
        return redirect('app:editar_plato', menu.plato.id_plato)

    if menu.producto:
        return redirect('app:editar_producto', menu.producto.id_producto)

    return redirect('app:listar_menu')
    
    
class MenuDeleteView(DeleteView):
    model = Menu
    template_name = 'menu/eliminar.html'
    success_url = reverse_lazy('app:listar_menu')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Menu'
        context['listar_url'] = reverse_lazy('app:listar_menu')
        return context
    
