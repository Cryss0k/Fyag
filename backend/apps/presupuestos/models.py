"""presupuestos — models. Dueño: Back 1. Esquema v1 + D-04 (folio, subtotal, iva, ítems)."""

from django.conf import settings
from django.db import models
from django.db.models import Q


class EstadoPresupuesto(models.TextChoices):
    BORRADOR = "BORRADOR", "Borrador"
    ENVIADO = "ENVIADO", "Enviado"
    APROBADO = "APROBADO", "Aprobado"
    RECHAZADO = "RECHAZADO", "Rechazado"


class Presupuesto(models.Model):
    id_presupuesto = models.AutoField(primary_key=True)
    folio = models.CharField(max_length=20, unique=True)
    cliente = models.ForeignKey(
        "clientes.Cliente", on_delete=models.PROTECT, db_column="id_cliente", related_name="presupuestos"
    )
    fecha_emision = models.DateField()
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    monto_total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    estado = models.CharField(max_length=10, choices=EstadoPresupuesto.choices, default=EstadoPresupuesto.BORRADOR)
    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column="id_creado_por", related_name="+"
    )

    class Meta:
        db_table = "presupuestos"
        constraints = [
            models.CheckConstraint(condition=Q(monto_total__gte=0), name="ck_presupuesto_monto_total_no_negativo"),
        ]

    def __str__(self):
        return self.folio


class TipoItem(models.TextChoices):
    SERVICIO = "SERVICIO", "Servicio"
    MATERIAL = "MATERIAL", "Material"


class PresupuestoItem(models.Model):
    id_item = models.AutoField(primary_key=True)
    presupuesto = models.ForeignKey(
        Presupuesto, on_delete=models.CASCADE, db_column="id_presupuesto", related_name="items"
    )
    tipo = models.CharField(max_length=10, choices=TipoItem.choices)
    descripcion = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        db_table = "presupuesto_items"
        constraints = [
            models.CheckConstraint(condition=Q(cantidad__gt=0), name="ck_item_cantidad_positiva"),
            models.CheckConstraint(condition=Q(precio_unitario__gt=0), name="ck_item_precio_positivo"),
        ]
