from django.contrib import admin
from .models import Reserva, Pedido, ItemPedido
from django.db.models import Sum
from cliente.models import Cliente
from django.utils.html import format_html
from django import forms
from django.contrib.admin import SimpleListFilter
import csv
from django.http import HttpResponse

# Filtro para las fechas
class FechaPedidoFilter(SimpleListFilter):
    title = 'Fecha del Pedido'
    parameter_name = 'fecha_pedido'

    def lookups(self, request, model_admin):
        return (
            ('today', 'Hoy'),
            ('week', 'Esta Semana'),
            ('month', 'Este Mes'),
            ('year', 'Este Año'),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        if self.value() == 'today':
            return queryset.filter(fecha_pedido__date=timezone.now().date())
        elif self.value() == 'week':
            return queryset.filter(fecha_pedido__gte=timezone.now() - timezone.timedelta(weeks=1))
        elif self.value() == 'month':
            return queryset.filter(fecha_pedido__month=timezone.now().month)
        elif self.value() == 'year':
            return queryset.filter(fecha_pedido__year=timezone.now().year)
        return queryset

# Administrador para reporte de ventas
class ReporteVentasAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'total', 'fecha_pedido', 'estado')
    list_filter = (FechaPedidoFilter,)
    search_fields = ('cliente__nombre', 'total')
    actions = ['generar_reporte_ventas']

    def generar_reporte_ventas(self, request, queryset):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        if fecha_inicio and fecha_fin:
            ventas = Pedido.objects.filter(fecha_pedido__range=[fecha_inicio, fecha_fin])
        else:
            ventas = Pedido.objects.all()

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_ventas.csv"'
        writer = csv.writer(response,delimiter=';')
        writer.writerow(['ID', 'Cliente', 'Total', 'Fecha de Pedido', 'Estado'])

        for venta in ventas:
            writer.writerow([venta.id, venta.cliente.nombre, venta.total, venta.fecha_pedido, venta.estado])

        return response

    generar_reporte_ventas.short_description = "Generar Reporte de Ventas (Descargar CSV)"

# Administrador para reporte de reservas
class ReporteReservasAdmin(admin.ModelAdmin):
    list_display = ('id', 'cliente', 'mesa', 'fecha_reserva', 'estado')
    actions = ['generar_reporte_reservas']

    def generar_reporte_reservas(self, request, queryset):
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')
        estado = request.GET.get('estado')

        reservas = Reserva.objects.all()

        if fecha_inicio and fecha_fin:
            reservas = reservas.filter(fecha_reserva__range=[fecha_inicio, fecha_fin])
        if estado:
            reservas = reservas.filter(estado=estado)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="reporte_reservas.csv"'
        writer = csv.writer(response, delimiter=';')
        writer.writerow(['ID', 'Cliente', 'Mesa', 'Fecha de Reserva', 'Estado'])

        for reserva in reservas:
            writer.writerow([reserva.id, reserva.cliente.nombre, reserva.mesa.id, reserva.fecha_reserva, reserva.estado])

        return response

    generar_reporte_reservas.short_description = "Generar Reporte de Reservas (Descargar CSV)"

# Registro en admin
admin.site.register(Pedido, ReporteVentasAdmin)
admin.site.register(Reserva, ReporteReservasAdmin)
admin.site.register(Cliente)
admin.site.register(ItemPedido)
