from django import forms
from .models import Cliente 
from .models import Producto



class ClienteCreateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'ape_nombre', 'fec_registro']
        labels = {
            'id_cliente': 'DNI',
            'ape_nombre': 'Apellidos y Nombres',
            'fec_registro': 'Fecha de Registro'
        }
            
        widgets = {
            'id_cliente': forms.TextInput(attrs={
                'maxlength': '8', 
                'placeholder': 'Ingrese DNI'
            }),
            'ape_nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese Apellidos y Nombres'
            }),
            'fec_registro': forms.DateInput(attrs={
                'type': 'date'
            }),
        }
        
        error_messages = {
            'id_cliente': {
                'max_length': 'El DNI debe tener 8 caracteres.',
                'required': 'El DNI es obligatorio.',
            },
            'ape_nombre': {
                'required': 'El nombre es obligatorio.',
            },
            'fec_registro': {
                'required': 'La fecha de registro es obligatoria.',
            },
        }


class ProductoCreateForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nom_prod', 'des_prod', 'precio', 'cantidad', 'fec_vencimiento']
        labels = {
            'nom_prod': 'Nombre del Producto',
            'des_prod': 'Descripción',
            'precio': 'Precio',
            'cantidad': 'Cantidad',
            'fec_vencimiento': 'Fecha de Vencimiento'
        }

        widgets = {
            'nom_prod': forms.TextInput(attrs={'placeholder': 'Ingrese nombre del producto'}),
            'des_prod': forms.Textarea(attrs={'placeholder': 'Ingrese descripción del producto'}),
            'precio': forms.NumberInput(attrs={'step': '0.01'}),
            'cantidad': forms.NumberInput(),
            'fec_vencimiento': forms.DateInput(attrs={'type': 'date'}),
        }
        error_messages = {
            'nom_prod': {
                'required': 'El nombre del producto es obligatorio.',
            },
            'des_prod': {
                'required': 'La descripción es obligatoria.',
            },
            'precio': {
                'required': 'El precio es obligatorio.',
                'invalid': 'Ingrese un precio válido.',
            },
            'cantidad': {
                'required': 'La cantidad es obligatoria.',
                'invalid': 'Ingrese una cantidad válida.',
            },
            'fec_vencimiento': {
                'required': 'La fecha de vencimiento es obligatoria.',
            },
        }


def clean_id_cliente(self):
    id_cliente = self.cleaned_data.get('id_cliente')

    if id_cliente:
        if Cliente.objects.filter(id_cliente=id_cliente).exists():
            raise forms.ValidationError("El DNI ya está registrado.")
        return id_cliente


class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['id_cliente', 'ape_nombre', 'fec_registro']
        labels = {
            'id_cliente': 'DNI',
            'ape_nombre': 'Apellidos y Nombres',
            'fec_registro': 'Fecha de Registro'
        }
        widgets = {
            'id_cliente': forms.TextInput(attrs={
                'readonly': True,
                'class': 'readonly-field',
            }),
            'ape_nombre': forms.TextInput(attrs={
                'placeholder': 'Ingrese Apellidos y Nombres'
            }),
            'fec_registro': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'form-control'
                },
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.fec_registro:
            self.initial['fec_registro'] = self.instance.fec_registro.strftime('%Y-%m-%d')