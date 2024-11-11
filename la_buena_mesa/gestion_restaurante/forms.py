from django import forms
from .models import Reserva, Pedido
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class ReservaForm(forms.ModelForm):
    class Meta:
        model = Reserva
        fields = ['cliente', 'mesa', 'fecha_reserva', 'estado']

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['reserva', 'cliente', 'total', 'fecha_pedido', 'estado', 'metodo_pago']

class RegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
