"""Carga datos FICTICIOS de demostración (idempotente). Dueño: Base de datos.

    python manage.py seed_demo

Crea un usuario por rol, tipos de servicio, clientes, presupuestos en todos los estados y
obras en todos los estados (toda obra EN_PROCESO tiene técnico), con facturas y costos. Nunca usar datos reales de FYAG.
Se niega a correr con DEBUG=False salvo que se use --force (staging para la demostración).
"""

import os
from datetime import date, timedelta
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Rol, Usuario
from apps.clientes.models import Cliente
from apps.cobranzas.models import CostoObra, EstadoPago, Factura
from apps.obras.models import EstadoObra, Obra, ObraTecnico, TipoServicio
from apps.presupuestos.models import EstadoPresupuesto, Presupuesto, PresupuestoItem

TIPOS_SERVICIO = [
    "Proyecto", "Mantención", "Climatización", "Proyecto eléctrico",
    "Emergencia", "Garantía", "Venta de repuestos", "Mejoras",
]

USUARIOS = [
    ("gerencia@fyag.local", "Gabriela Gerencia", Rol.GERENCIA),
    ("finanzas@fyag.local", "Felipe Finanzas", Rol.ADMINISTRATIVO),
    ("supervisor@fyag.local", "Sofía Supervisora", Rol.SUPERVISOR),
    ("tecnico1@fyag.local", "Tomás Técnico", Rol.TECNICO),
    ("tecnico2@fyag.local", "Teresa Técnica", Rol.TECNICO),
]

CLIENTES = [
    ("76.000.001-1", "Frigorífico Los Andes SpA"),
    ("76.000.002-2", "Agrícola Valle Verde Ltda."),
    ("76.000.003-3", "Cámaras del Sur S.A."),
]

IVA = Decimal("0.19")


class Command(BaseCommand):
    help = "Carga datos ficticios de demostración."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Permite correr con DEBUG=False (staging).")

    @transaction.atomic
    def handle(self, *args, **opts):
        if not settings.DEBUG and not opts["force"]:
            raise CommandError("Con DEBUG=False usa --force (solo staging; nunca producción con datos reales).")

        clave = os.environ.get("SEED_PASSWORD", "demo-cambiar-123")
        users = {}
        for correo, nombre, rol in USUARIOS:
            user, creado = Usuario.objects.get_or_create(correo=correo, defaults={"nombre_completo": nombre, "rol": rol})
            if creado:
                user.set_password(clave)
                user.save()
            users[correo.split("@")[0]] = user

        tipos = {n: TipoServicio.objects.get_or_create(nombre=n)[0] for n in TIPOS_SERVICIO}
        clientes = [
            Cliente.objects.get_or_create(rut=rut, defaults={"razon_social": rs, "email": f"contacto@cliente{i}.test"})[0]
            for i, (rut, rs) in enumerate(CLIENTES, start=1)
        ]

        hoy = date.today()
        fin = users["finanzas"]

        def presupuesto(folio, cliente, estado, items):
            obj = Presupuesto.objects.filter(folio=folio).first()
            if obj:
                return obj
            subtotal = sum((Decimal(c) * Decimal(p) for _, _, c, p in items), Decimal("0"))
            iva = (subtotal * IVA).quantize(Decimal("0.01"))
            obj = Presupuesto.objects.create(
                folio=folio, cliente=cliente, fecha_emision=hoy - timedelta(days=30), subtotal=subtotal,
                iva=iva, monto_total=subtotal + iva, estado=estado, creado_por=fin,
            )
            for tipo, desc, cant, precio in items:
                PresupuestoItem.objects.create(
                    presupuesto=obj, tipo=tipo, descripcion=desc, cantidad=Decimal(cant), precio_unitario=Decimal(precio)
                )
            return obj

        base_items = [
            ("SERVICIO", "Mano de obra técnica", "40", "18000"),
            ("MATERIAL", "Compresor semihermético", "1", "950000"),
        ]
        P = EstadoPresupuesto
        presupuesto("P-0001", clientes[0], P.BORRADOR, base_items)
        presupuesto("P-0002", clientes[1], P.ENVIADO, base_items)
        presupuesto("P-0003", clientes[2], P.RECHAZADO, base_items)
        aprobados = [presupuesto(f"P-010{i}", clientes[i % 3], P.APROBADO, base_items) for i in range(1, 6)]

        def obra(nombre, ppto, tipo, estado, tecnicos=()):
            o, creada = Obra.objects.get_or_create(
                presupuesto=ppto,
                defaults={
                    "nombre_obra": nombre, "tipo_servicio": tipos[tipo], "ubicacion": "Concepción, Biobío",
                    "fecha_inicio": hoy - timedelta(days=20), "fecha_fin_estimada": hoy + timedelta(days=20),
                    "estado_operativo": estado,
                    "confirmada_en": timezone.now() if estado in {EstadoObra.FINALIZADA, EstadoObra.COBRADA} else None,
                },
            )
            if creada:
                for t in tecnicos:
                    ObraTecnico.objects.create(obra=o, tecnico=t)
            return o

        E = EstadoObra
        obra("Cámara de frío bodega norte", aprobados[0], "Proyecto", E.EN_PROCESO, [users["tecnico2"]])
        o_proceso = obra("Mantención planta Valle Verde", aprobados[1], "Mantención", E.EN_PROCESO, [users["tecnico1"]])
        o_finalizada = obra("Climatización sala de proceso", aprobados[2], "Climatización", E.FINALIZADA, [users["tecnico2"]])
        obra("Emergencia túnel de congelado", aprobados[3], "Emergencia", E.SUSPENDIDA, [users["tecnico1"]])
        o_cobrada = obra("Garantía evaporador", aprobados[4], "Garantía", E.COBRADA, [users["tecnico1"], users["tecnico2"]])

        def factura(num, o, monto, estado, vence_en_dias, pagada=False):
            if Factura.objects.filter(numero_factura=num).exists():
                return
            Factura.objects.create(
                obra=o, numero_factura=num, monto=Decimal(monto), estado_pago=estado,
                fecha_emision=hoy - timedelta(days=25), fecha_vencimiento=hoy + timedelta(days=vence_en_dias),
                fecha_pago=hoy - timedelta(days=5) if pagada else None,
            )

        factura("F-0001", o_proceso, "500000", EstadoPago.PENDIENTE, 15)
        factura("F-0002", o_finalizada, "1200000", EstadoPago.PENDIENTE, -10)  # vencida
        factura("F-0003", o_cobrada, o_cobrada.presupuesto.monto_total, EstadoPago.PAGADO, -5, pagada=True)

        if not CostoObra.objects.exists():
            for o, desc, monto in [
                (o_proceso, "Gas refrigerante R404A", "180000"),
                (o_finalizada, "Cañería de cobre", "240000"),
                (o_cobrada, "Transporte de equipos", "90000"),
            ]:
                CostoObra.objects.create(
                    obra=o, descripcion=desc, categoria="MATERIALES", monto=Decimal(monto),
                    fecha=hoy - timedelta(days=15), registrado_por=fin,
                )

        self.stdout.write(self.style.SUCCESS("Datos de demostración cargados."))
        self.stdout.write("Usuarios: gerencia@, finanzas@, supervisor@, tecnico1@, tecnico2@ (dominio fyag.local).")
        self.stdout.write("Clave: la variable SEED_PASSWORD, o 'demo-cambiar-123' si no está definida.")
