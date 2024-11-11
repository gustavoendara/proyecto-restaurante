from django.contrib import admin
from .models import Reserva, Pedido, ItemPedido

admin.site.register(Reserva)
admin.site.register(Pedido)
admin.site.register(ItemPedido)

