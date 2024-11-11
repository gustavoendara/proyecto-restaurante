from django.db import models

class MetodoPago(models.Model):
    tipo = models.CharField(max_length=50)
    descripcion = models.TextField()
    
    def __str__(self):
        return self.tipo
