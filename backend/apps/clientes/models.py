"""clientes — models. Dueño: Back 1."""

from django.db import models


class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=12, unique=True)
    razon_social = models.CharField(max_length=150)
    contacto_nombre = models.CharField(max_length=100, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

    class Meta:
        db_table = "clientes"

    def __str__(self):
        return self.razon_social
