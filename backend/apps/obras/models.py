"""obras — models. Dueño: Back 2. Esquema v1 + D-02 (estados del informe), D-03 (técnicos N:M), D-04."""

from django.conf import settings
from django.db import models


class EstadoObra(models.TextChoices):
    EN_PROCESO = "EN_PROCESO", "En proceso"
    SUSPENDIDA = "SUSPENDIDA", "Suspendida"
    FINALIZADA = "FINALIZADA", "Finalizada"
    CANCELADA = "CANCELADA", "Cancelada"
    COBRADA = "COBRADA", "Cobrada"


class TipoServicio(models.Model):
    id_tipo_servicio = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = "tipos_servicio"

    def __str__(self):
        return self.nombre


class Obra(models.Model):
    id_obra = models.AutoField(primary_key=True)
    nombre_obra = models.CharField(max_length=150)
    # OneToOne => UNIQUE: un presupuesto tiene como máximo una obra (D-05).
    presupuesto = models.OneToOneField(
        "presupuestos.Presupuesto", on_delete=models.PROTECT, db_column="id_presupuesto", related_name="obra"
    )
    tipo_servicio = models.ForeignKey(
        TipoServicio, on_delete=models.PROTECT, db_column="id_tipo_servicio", related_name="obras"
    )
    ubicacion = models.CharField(max_length=200)
    fecha_inicio = models.DateField()
    fecha_fin_estimada = models.DateField(null=True, blank=True)
    estado_operativo = models.CharField(max_length=12, choices=EstadoObra.choices, default=EstadoObra.EN_PROCESO)
    confirmada_en = models.DateTimeField(null=True, blank=True)  # confirmación de ejecución del supervisor
    tecnicos = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="ObraTecnico", related_name="obras_asignadas"
    )

    class Meta:
        db_table = "obras"

    def __str__(self):
        return self.nombre_obra


class ObraTecnico(models.Model):
    id_obra_tecnico = models.AutoField(primary_key=True)
    obra = models.ForeignKey(Obra, on_delete=models.CASCADE, db_column="id_obra")
    tecnico = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, db_column="id_tecnico")
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "obra_tecnicos"
        constraints = [models.UniqueConstraint(fields=["obra", "tecnico"], name="uq_obra_tecnico")]
