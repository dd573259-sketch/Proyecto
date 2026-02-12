from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView as listView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from app.models import *
from app.forms import NotificacionForm

def index(request):
    return render(request, 'main.html')
# Create your views here.
def listar_notificaciones(request):
    nombre = {
        
        'notificaciones': Notificacion.objects.all()
    }
    return render(request, 'Notificacion/listar.html', nombre)

class notificacionListView(listView):
    model = Notificacion
    template_name = 'Notificacion/listar.html'
    
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
        context['titulo'] = 'Listado de Notificaciones'
        context['crear_url'] = reverse_lazy('app:crear_notificacion')
        return context
    
class NotificacionCreateView(CreateView):
    model = Notificacion
    template_name = 'Notificacion/crear.html'
    form_class = NotificacionForm
    success_url = reverse_lazy('app:listar_notificaciones')
    
    #@method_decorator(csrf_exempt)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Crear Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificaciones')
        return context
    
    
    
class NotificacionUpdateView(UpdateView):
    model = Notificacion
    form_class = NotificacionForm
    template_name = 'Notificacion/crear.html'
    success_url = reverse_lazy('app:listar_notificaciones')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Editar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificaciones')
        return context
    
    
class NotificacionDeleteView(DeleteView):
    model = Notificacion
    template_name = 'Notificacion/eliminar.html'
    success_url = reverse_lazy('app:listar_notificaciones')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = 'Eliminar Notificación'
        context['listar_url'] = reverse_lazy('app:listar_notificaciones')
        return context