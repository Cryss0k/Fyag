-- Esquema v1 (BORRADOR de referencia). Nombres y tipos alineados con backend/apps/*/models.py.
-- Decisiones aplicadas: D-02 (estados del informe + COBRADA), D-03 (obra_tecnicos), D-04 (ajustes), D-05 (1 presupuesto = 1 obra), D-06.

CREATE TABLE usuarios (
    id_usuario        SERIAL PRIMARY KEY,
    nombre_completo   VARCHAR(100) NOT NULL,
    correo            VARCHAR(100) NOT NULL UNIQUE,
    password          VARCHAR(128) NOT NULL,              -- hash Argon2 (nunca texto plano)
    rol               VARCHAR(20)  NOT NULL CHECK (rol IN ('GERENCIA','ADMINISTRATIVO','SUPERVISOR','TECNICO')),
    activo            BOOLEAN      NOT NULL DEFAULT TRUE,
    intentos_fallidos SMALLINT     NOT NULL DEFAULT 0,
    bloqueado_hasta   TIMESTAMPTZ
);

CREATE TABLE clientes (
    id_cliente      SERIAL PRIMARY KEY,
    rut             VARCHAR(12)  NOT NULL UNIQUE,
    razon_social    VARCHAR(150) NOT NULL,
    contacto_nombre VARCHAR(100),
    telefono        VARCHAR(20),
    email           VARCHAR(100)
);

CREATE TABLE tipos_servicio (
    id_tipo_servicio SERIAL PRIMARY KEY,
    nombre           VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE presupuestos (
    id_presupuesto SERIAL PRIMARY KEY,
    folio          VARCHAR(20) NOT NULL UNIQUE,
    id_cliente     INT NOT NULL REFERENCES clientes(id_cliente) ON DELETE RESTRICT,
    fecha_emision  DATE NOT NULL,
    subtotal       NUMERIC(12,2) NOT NULL DEFAULT 0,
    iva            NUMERIC(12,2) NOT NULL DEFAULT 0,
    monto_total    NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (monto_total >= 0),
    estado         VARCHAR(10) NOT NULL DEFAULT 'BORRADOR' CHECK (estado IN ('BORRADOR','ENVIADO','APROBADO','RECHAZADO')),
    id_creado_por  INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

CREATE TABLE presupuesto_items (
    id_item         SERIAL PRIMARY KEY,
    id_presupuesto  INT NOT NULL REFERENCES presupuestos(id_presupuesto) ON DELETE CASCADE,
    tipo            VARCHAR(10) NOT NULL CHECK (tipo IN ('SERVICIO','MATERIAL')),
    descripcion     VARCHAR(200) NOT NULL,
    cantidad        NUMERIC(10,2) NOT NULL CHECK (cantidad > 0),
    precio_unitario NUMERIC(12,2) NOT NULL CHECK (precio_unitario > 0)
);

CREATE TABLE obras (
    id_obra            SERIAL PRIMARY KEY,
    nombre_obra        VARCHAR(150) NOT NULL,
    id_presupuesto     INT NOT NULL UNIQUE REFERENCES presupuestos(id_presupuesto) ON DELETE RESTRICT,
    id_tipo_servicio   INT NOT NULL REFERENCES tipos_servicio(id_tipo_servicio) ON DELETE RESTRICT,
    ubicacion          VARCHAR(200) NOT NULL,
    fecha_inicio       DATE NOT NULL,
    fecha_fin_estimada DATE,
    estado_operativo   VARCHAR(12) NOT NULL DEFAULT 'EN_PROCESO'
        CHECK (estado_operativo IN ('EN_PROCESO','SUSPENDIDA','FINALIZADA','CANCELADA','COBRADA')),
    confirmada_en      TIMESTAMPTZ
);

CREATE TABLE obra_tecnicos (
    id_obra_tecnico  SERIAL PRIMARY KEY,
    id_obra          INT NOT NULL REFERENCES obras(id_obra) ON DELETE CASCADE,
    id_tecnico       INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT,
    fecha_asignacion TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT uq_obra_tecnico UNIQUE (id_obra, id_tecnico)
);

CREATE TABLE facturas (
    id_factura        SERIAL PRIMARY KEY,
    id_obra           INT NOT NULL REFERENCES obras(id_obra) ON DELETE RESTRICT,
    numero_factura    VARCHAR(50) NOT NULL UNIQUE,
    monto             NUMERIC(12,2) NOT NULL CHECK (monto > 0),
    fecha_emision     DATE NOT NULL,
    fecha_vencimiento DATE NOT NULL,
    fecha_pago        DATE,
    estado_pago       VARCHAR(10) NOT NULL DEFAULT 'PENDIENTE' CHECK (estado_pago IN ('PENDIENTE','PAGADO','ANULADA')),
    motivo_anulacion  VARCHAR(255) NOT NULL DEFAULT ''
);

CREATE TABLE costos_obra (
    id_costo          SERIAL PRIMARY KEY,
    id_obra           INT NOT NULL REFERENCES obras(id_obra) ON DELETE RESTRICT,
    descripcion       VARCHAR(200) NOT NULL,
    categoria         VARCHAR(30)  NOT NULL,
    monto             NUMERIC(12,2) NOT NULL CHECK (monto > 0),
    fecha             DATE NOT NULL,
    id_registrado_por INT NOT NULL REFERENCES usuarios(id_usuario) ON DELETE RESTRICT
);

-- Índices en claves foráneas y columnas de filtro (Normas §8)
CREATE INDEX ix_presupuestos_cliente ON presupuestos(id_cliente);
CREATE INDEX ix_presupuestos_estado  ON presupuestos(estado);
CREATE INDEX ix_obras_estado         ON obras(estado_operativo);
CREATE INDEX ix_obras_tipo           ON obras(id_tipo_servicio);
CREATE INDEX ix_obra_tecnicos_tecnico ON obra_tecnicos(id_tecnico);
CREATE INDEX ix_facturas_obra        ON facturas(id_obra);
CREATE INDEX ix_facturas_estado_venc ON facturas(estado_pago, fecha_vencimiento);
CREATE INDEX ix_costos_obra          ON costos_obra(id_obra);
