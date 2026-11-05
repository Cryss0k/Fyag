"""cobranzas — models. Dueño: Back 2. Esquema v1 + D-04 (ANULADA, fecha_pago, costos_obra)."""

from django.conf import settings
from django.db import models
from django.db.models import Q


class EstadoPago(models.TextChoices):
    PENDIENTE = "PENDIENTE", "Pendiente"
    PAGADO = "PAGADO", "Pagado"
    ANULADA = "ANULADA", "Anulada"


class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    obra = models.ForeignKey("obras.Obra", on_delete=models.PROTECT, db_column="id_obra", related_name="facturas")
    numero_factura = models.CharField(max_length=50, unique=True)
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha_emision = models.DateField()
    fecha_vencimiento = models.DateField()
    fecha_pago = models.DateField(null=True, blank=True)
    estado_pago = models.CharField(max_length=10, choices=EstadoPago.choices, default=EstadoPago.PENDIENTE)
    motivo_anulacion = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        db_table = "facturas"
        constraints = [models.CheckConstraint(condition=Q(monto__gt=0), name="ck_factura_monto_positivo")]


class CostoObra(models.Model):
    id_costo = models.AutoField(primary_key=True)
    obra = models.ForeignKey("obras.Obra", on_delete=models.PROTECT, db_column="id_obra", related_name="costos")
    descripcion = models.CharField(max_length=200)
    categoria = models.CharField(max_length=30)  # p. ej. MATERIALES, MANO_DE_OBRA, TRANSPORTE
    monto = models.DecimalField(max_digits=12, decimal_places=2)
    fecha = models.DateField()
    registrado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column="id_registrado_por", related_name="+"
    )

    class Meta:
        db_table = "costos_obra"
        constraints = [models.CheckConstraint(condition=Q(monto__gt=0), name="ck_costo_monto_positivo")]
