from django.db import models
from cliente.models import Cliente
from mesa.models import Mesa
from metodopago.models import MetodoPago

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    mesa = models.ForeignKey(Mesa, on_delete=models.CASCADE)
    fecha_reserva = models.DateTimeField()
    estado = models.CharField(max_length=50)

    def __str__(self):
        return f"Reserva {self.id} - {self.cliente.nombre} - {self.fecha_reserva}"

class Pedido(models.Model):
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE, null=True, blank=True)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_pedido = models.DateTimeField()
    estado = models.CharField(max_length=50)
    metodo_pago = models.ForeignKey(MetodoPago, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"Pedido {self.id} - Cliente: {self.cliente.nombre}"

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.CharField(max_length=100)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.producto} - {self.cantidad} unidades"
