from django.shortcuts import render, redirect, get_object_or_404
from .models import Reserva, Pedido
from django.db.models import Sum
from .forms import ReservaForm, PedidoForm, RegisterForm
from cliente.models import Cliente
from mesa.models import Mesa
from metodopago.models import MetodoPago
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required, user_passes_test



def index(request):
    return render(request, 'gestion_restaurante/index.html')

def lista_reservas(request):
    reservas = Reserva.objects.all().order_by('-fecha_reserva')
    return render(request, 'gestion_restaurante/lista_reservas.html', {'reservas': reservas})


def crear_reserva(request):
    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_reservas')  
    else:
        form = ReservaForm()
    return render(request, 'gestion_restaurante/crear_reserva.html', {'form': form})


def detalle_reserva(request, reserva_id):
    reserva = get_object_or_404(Reserva, id=reserva_id)
    return render(request, 'gestion_restaurante/detalle_reserva.html', {'reserva': reserva})

def lista_pedidos(request):
    pedidos = Pedido.objects.all().order_by('-fecha_pedido')
    return render(request, 'gestion_restaurante/lista_pedidos.html', {'pedidos': pedidos})

def crear_pedido(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_pedidos')  
    else:
        form = PedidoForm()
    return render(request, 'gestion_restaurante/crear_pedido.html', {'form': form})

def detalle_pedido(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    return render(request, 'gestion_restaurante/detalle_pedido.html', {'pedido': pedido})

def reporte_ventas(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    pedidos = Pedido.objects.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])
    total_ventas = pedidos.aggregate(Sum('total'))
    
    
    return render(request, 'gestion_restaurante/reporte_ventas.html', {
        'pedidos': pedidos,
        'total_ventas': total_ventas
    })
    


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'gestion_restaurante/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'gestion_restaurante/login.html'
    

def logout_view(request):
    logout(request)
    return redirect('index')

def es_admin(user):
    return user.is_superuser


@login_required
@user_passes_test(es_admin)
def historial_pedidos_cliente(request, cliente_id):
    cliente = Cliente.objects.get(id=cliente_id)
    pedidos = Pedido.objects.filter(cliente=cliente)
    
    return render(request, 'gestion_restaurante/historial_pedidos_cliente.html', {
        'cliente': cliente,
        'pedidos': pedidos
    })

def reporte_reservas(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    reservas = Reserva.objects.filter(fecha_reserva__range=[fecha_inicio, fecha_fin])
    
    return render(request, 'gestion_restaurante/reporte_reservas.html', {
        'reservas': reservas
    })

def reporte_ingresos(request):
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    pedidos = Pedido.objects.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])
    total_ingresos = pedidos.aggregate(Sum('total'))
    
    return render(request, 'gestion_restaurante/reporte_ingresos.html', {
        'pedidos': pedidos,
        'total_ingresos': total_ingresos
    })

