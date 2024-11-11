from django.db import models

class Mesa(models.Model):
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)
    
    
    def __str__(self):
        return f"Mesa {self.id} - Capacidad: {self.capacidad}"
