from dataclasses import field
from django.forms import ModelForm
from app.models import *
from django import forms

class CategoriaForm(ModelForm):
    class Meta:
        model = Categoria
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la categoria'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la categoria',
                    'rows': 3,
                    'cols': 3}),
        }

class MenuForm(ModelForm):
    class Meta:
        model = Menu
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del menu'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del menu',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del menu'}),
        }

class RecetaForm(ModelForm):
    class Meta:
        model = recetas
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre de la receta'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion de la receta',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio de la receta'}),
        }

class InsumosForm(ModelForm):
    class Meta:
        model = insumo
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese el nombre del insumo'}),
            'descripcion': 
                forms.Textarea(attrs={
                    'placeholder': 'Ingrese la descripcion del insumo',
                    'rows': 3,
                    'cols': 3}),
            'precio': forms.NumberInput(attrs={
                'placeholder': 'Ingrese el precio del insumo'}),
        }
    def clean_nombre(self):
            nombre = self.cleaned_data.get('nombre')
            if len(nombre) < 3:
                raise forms.ValidationError('El nombre debe tener al menos 3 caracteres')
            return nombre 
    def clean_descripcion(self):
        descripcion = self.cleaned_data['descripcion']
        if len(descripcion) <10:
            raise forms.ValidationError('La descripcion debe tener al menos 10 caracteres')
        return descripcion
    
    def clean(self):
        cleaned_data  = super().clean()
        unidad = self.cleaned_data.get('unidad')
        valor = self.cleaned_data.get('valor')
        if int(unidad) < 0 or int(valor) < 0:
            raise forms.ValidationError("El valor y la unidad debe ser mayor a 0")
        return unidad