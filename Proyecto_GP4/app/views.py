from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from app.models import Categoria

def index(request):
    return render(request, 'main.html')
# Create your views here.
def listar_categorias(request):
    nombre = {
        'titulo': 'Listado de Categorias',
        'categorias': Categoria.objects.all()
    }
    return render(request, 'Categoria/listar.html', nombre)