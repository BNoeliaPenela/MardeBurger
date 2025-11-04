from django import forms
from .models import Pedido


class PedidoForm(forms.ModelForm):
    """Formulario para crear un nuevo pedido"""
    
    class Meta:
        model = Pedido
        fields = [
            'nombre_cliente', 
            'telefono', 
            'direccion', 
            'tipo_entrega', 
            'metodo_pago', 
            'notas'
        ]
        
        widgets = {
            'nombre_cliente': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Juan Pérez',
                'required': True
            }),
            'telefono': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '2291 123456 o 11 1234-5678',
                'required': True
            }),
            'direccion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Calle, número, piso/depto, entre calles, referencias...'
            }),
            'tipo_entrega': forms.RadioSelect(attrs={
                'class': 'form-check-input'
            }),
            'metodo_pago': forms.Select(attrs={
                'class': 'form-select'
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Ej: Sin cebolla, extra queso, tocar timbre, etc.'
            }),
        }
        
        labels = {
            'nombre_cliente': 'Nombre completo',
            'telefono': 'Teléfono de contacto',
            'direccion': 'Dirección de entrega',
            'tipo_entrega': 'Tipo de entrega',
            'metodo_pago': 'Método de pago',
            'notas': 'Notas adicionales'
        }
        
        help_texts = {
            'direccion': 'Solo necesario si elegís delivery',
            'metodo_pago': 'El pago se coordina por WhatsApp',
        }
    
    def clean_telefono(self):
        """Validación personalizada para el teléfono"""
        telefono = self.cleaned_data.get('telefono')
        
        # Limpiar espacios y guiones
        telefono_limpio = telefono.replace(' ', '').replace('-', '')
        
        # Verificar que contenga solo números
        if not telefono_limpio.isdigit():
            raise forms.ValidationError(
                'El teléfono debe contener solo números, espacios o guiones'
            )
        
        # Verificar longitud mínima
        if len(telefono_limpio) < 8:
            raise forms.ValidationError(
                'El teléfono debe tener al menos 8 dígitos'
            )
        
        return telefono
    
    def clean(self):
        """Validación del formulario completo"""
        cleaned_data = super().clean()
        tipo_entrega = cleaned_data.get('tipo_entrega')
        direccion = cleaned_data.get('direccion')
        
        # Si es delivery, la dirección es obligatoria
        if tipo_entrega == 'delivery' and not direccion:
            self.add_error(
                'direccion',
                'Debes ingresar una dirección para el delivery'
            )
        
        return cleaned_data