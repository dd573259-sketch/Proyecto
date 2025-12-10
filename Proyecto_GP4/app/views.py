from django.shortcuts import render

def index(request):
    return render(request, 'body.html')
# Create your views here.
