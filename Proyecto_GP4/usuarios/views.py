from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, View
from django.contrib.auth.models import User
from django.contrib import messages
from .models import PerfilUsuario
from .forms import UserForm, PerfilForm
from django.shortcuts import get_object_or_404
from .forms import UserEditForm

#  LISTAR USUARIOS 
class ListarUsuariosView(ListView):
    
    def get_context_data(self, **kwargs) -> dict[str]:
        context = super().get_context_data(**kwargs)
        context["titulo"] = "Listado de Usuarios"
        context['icono'] = 'fas fa-cash-register'
        return context
    
    model = User
    template_name = 'usuarios/listar.html'
    context_object_name = 'usuarios'

    def get_queryset(self):
        # Evitamos listar superusuarios del sistema 
        return User.objects.filter(is_superuser=False).select_related('perfil')

#  CREAR USUARIO 
class CrearUsuarioView(View):
    def get(self, request):
        #  formularios vacios
        context = {
            'titulo': 'Crear Nuevo Usuario',
            'user_form': UserForm(),
            'perfil_form': PerfilForm()
        }
        return render(request, 'usuarios/crear.html', context)

    def post(self, request):
        #  datos de los dos formularios
        user_form = UserForm(request.POST)
        perfil_form = PerfilForm(request.POST)

        if user_form.is_valid() and perfil_form.is_valid():
            # 1. Guardamos el User pero sin commit
            user = user_form.save(commit=False)
            # Encriptamos la contraseña
            user.set_password(user_form.cleaned_data['password'])
            user.save() # Ahora  guardamos el usuario

            # 2. Guardamos el Perfil y lo enlazamos al User creado
            perfil = perfil_form.save(commit=False)
            perfil.user = user
            perfil.save()

            messages.success(request, 'Usuario creado exitosamente.')
            return redirect('usuarios:listar') 

        # Si hay errores, recargamos 
        context = {
            'titulo': 'Crear Nuevo Usuario',
            'user_form': user_form,
            'perfil_form': perfil_form
        }
        return render(request, 'usuarios/crear.html', context)
    
#  EDITAR USUARIO 
class EditarUsuarioView(View):
    def get(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        # Obtenemos el perfil, o lo creamos si por alguna razon no existe
        perfil, created = PerfilUsuario.objects.get_or_create(user=usuario)
        
        context = {
            'titulo': 'Editar Usuario',
            'user_form': UserEditForm(instance=usuario),
            'perfil_form': PerfilForm(instance=perfil),
            'usuario': usuario
        }
        return render(request, 'usuarios/editar.html', context)

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        perfil = get_object_or_404(PerfilUsuario, user=usuario)
        
        user_form = UserEditForm(request.POST, instance=usuario)
        perfil_form = PerfilForm(request.POST, instance=perfil)

        if user_form.is_valid() and perfil_form.is_valid():
            user = user_form.save(commit=False)
            
            # Solo actualizamos la contraseña si el usuario escribio una nueva
            nueva_password = user_form.cleaned_data.get('password')
            if nueva_password:
                user.set_password(nueva_password)
                
            user.save()
            perfil_form.save()

            messages.success(request, 'Usuario actualizado exitosamente.')
            return redirect('usuarios:listar')

        context = {
            'titulo': 'Editar Usuario',
            'user_form': user_form,
            'perfil_form': perfil_form,
            'usuario': usuario
        }
        return render(request, 'usuarios/editar.html', context)

# DESACTIVAR USUARIO
class DesactivarUsuarioView(View):
    def get(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        context = {
            'titulo': 'Desactivar Usuario',
            'object': usuario,
            'listar_url': reverse_lazy('usuarios:listar')
        }
        return render(request, 'usuarios/eliminar.html', context)

    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        
        # En lugar de usuario.delete(), lo desactivamos:
        usuario.is_active = False 
        usuario.save()
        
        messages.success(request, 'Usuario desactivado correctamente.')
        return redirect('usuarios:listar')
    
class CambiarEstadoUsuarioView(View):
    def post(self, request, pk):
        usuario = get_object_or_404(User, pk=pk)
        
        # Invertimos el estado
        usuario.is_active = not usuario.is_active
        usuario.save()
        
        # Mensaje dinamico
        estado = "activado" if usuario.is_active else "desactivado"
        messages.success(request, f'Usuario {estado} correctamente.')
        
        return redirect('usuarios:listar')