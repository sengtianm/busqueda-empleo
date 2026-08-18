# Tablas de la base de datos — `job_search.db`

Reporte as-built de la base de datos SQLite del proyecto (ruta: `data/job_search.db`). Para cada tabla se documenta el propósito, sus columnas, qué hace cada una y en qué momento del flujo se diligencia (quién la escribe y desde qué nodo o función).

Fuente de verdad: `shared/persistence.py` (esquemas y funciones de escritura) y los nodos del módulo de descubrimiento (`modules/discovery/`).

## 1. Resumen

La BD tiene 8 tablas. Se habilita con `init_db()` (crea tablas y aplica migraciones idempotentes, incluida la migración al catálogo español D7/D8, la limpieza D31 y la creación de índices, decisión D16). Fechas en formato `YYYY-MM-DD HH:MM:SS` (hora local). IDs secuenciales con prefijo por tabla (`EMP`, `UBI`, `OFE`, `COR`, `SES`, `EVT`, `BLO`) generados por `generar_id()`.

**Regla de gestión de datos (decisión D31, 2026-08-18):** ningún campo persistido puede quedar vacío (`''`/NULL); cuando un valor no aplica o no está disponible se guarda `N/A` (o `N/R`). La normalización ocurre en la frontera de persistencia (`escribir_evento()`, `_upsert_ofertas_en()`) y las columnas afectadas declaran `DEFAULT 'N/A'`. Exenciones: `id_externo` (colisionaría en la deduplicación) y `fecha_ultima_verificacion` (por instrucción explícita del usuario; vacía hasta que una re-visita la refresca). Las consultas de conteo tratan `N/A` como vacío (`contar_distintos` excluye NULL, `''` y `'N/A'`).

Índices (creados con `CREATE INDEX IF NOT EXISTS`, no únicos — la unicidad estricta es del Módulo 2, decisión D4): `idx_ofertas_id_externo` (deduplicación por oferta), `idx_ofertas_id_corrida` y `idx_eventos_id_corrida` (métricas de cierre y auditoría).

Estado actual (conteos al momento del reporte, tras la migración D31):

| Tabla | Filas | Escritor principal |
|---|---|---|
| `secuencia_ids` | 4 | Automática (generador de IDs) |
| `empresas` | 0 | — (catálogo reservado; sin escritura en Módulo 1) |
| `ubicaciones` | 0 | — (catálogo reservado; sin escritura en Módulo 1) |
| `ofertas` | 62 | Nodo Captura → `upsert_oferta()` |
| `corridas` | 1 | Nodo INICIO → `registrar_corrida()`; Nodo Finalizar → `actualizar_corrida()` |
| `eventos` | 28 | Nodos del flujo → `escribir_evento()` |
| `sesiones` | 13 | Nodo Captura → `escribir_fila("sesiones")` |
| `bloqueo` | 0 | Nodo INICIO → `adquirir_bloqueo()`; Nodo Finalizar → `liberar_bloqueo()` |

### Momentos del flujo que diligencian las tablas

1. **INICIO**: prueba de escritura (`sondear_escritura()`, insert+rollback en `bloqueo`), adquisición del bloqueo (`adquirir_bloqueo()` → `bloqueo`) y registro de la corrida (`registrar_corrida()` → `corridas` con estado `en_ejecucion`). Ante fallos escribe eventos de error (`eventos`).
2. **Control de fuentes / Ingreso / Búsqueda**: no escriben en BD; en caso de aborto o error crítico registran eventos de error (`eventos`).
3. **Registro**: registra el resultado del registro de la fuente como evento de éxito o fallo (`eventos`).
4. **Captura**: audita cada lote capturado escribiendo la sesión de plataforma (`sesiones`) y registra las ofertas (`upsert_oferta()` → `ofertas`); emite eventos de éxito/registro parcial (`eventos`).
5. **Finalizar**: cierra la corrida con estado final y métricas (`actualizar_corrida()` → `corridas`), escribe el evento de terminación (`eventos`) y libera el bloqueo (`liberar_bloqueo()` → `bloqueo`).

## 2. Detalle por tabla

### 2.1. `secuencia_ids`

Control interno del generador de IDs secuenciales (`PREFIJO-NNNN`). No se escribe manualmente: `generar_id()` la inserta (`ultimo_numero = 1`) o incrementa (`ultimo_numero + 1`) al crear cualquier ID de otra tabla.

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `tabla_nombre` | TEXT (PK) | Nombre de la tabla para la que se lleva la secuencia | En el primer `generar_id()` de esa tabla (automático) |
| `prefijo` | TEXT NOT NULL | Prefijo del ID de esa tabla (`EMP`, `UBI`, `OFE`, `COR`, `SES`, `EVT`, `BLO`) | En el primer `generar_id()` de esa tabla (automático) |
| `ultimo_numero` | INTEGER NOT NULL DEFAULT 0 | Último número asignado (se incrementa en 1 por cada ID) | En cada `generar_id()` (automático) |

> **D31:** la secuencia de `fuentes` fue eliminada junto con la tabla (2026-08-18).

### 2.2. `empresas`

Catálogo de empresas. **En el MVP del Módulo 1 no se escribe en esta tabla** (0 filas): el Módulo 1 no extrae la empresa de las tarjetas (decisión D29; las columnas crudas `empresa_nombre`/`ubicacion_nombre` de `ofertas` fueron eliminadas); la tabla queda reservada para la gestión del catálogo.

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `id` | TEXT (PK) | ID único (prefijo `EMP`) | No se diligencia en el Módulo 1 |
| `nombre` | TEXT NOT NULL | Nombre oficial de la empresa | No se diligencia en el Módulo 1 |
| `nombre_normalizado` | TEXT DEFAULT '' | Nombre estandarizado para evitar duplicados | No se diligencia en el Módulo 1 |
| `sitio_web` | TEXT DEFAULT '' | Sitio web oficial | No se diligencia en el Módulo 1 |
| `perfil_linkedin` | TEXT DEFAULT '' | URL del perfil de LinkedIn | No se diligencia en el Módulo 1 |
| `sector` | TEXT DEFAULT '' | Sector económico | No se diligencia en el Módulo 1 |
| `tamano` | TEXT DEFAULT '' | Clasificación de tamaño de empresa | No se diligencia en el Módulo 1 |
| `descripcion` | TEXT DEFAULT '' | Descripción general | No se diligencia en el Módulo 1 |
| `fecha_creacion` | TEXT DEFAULT '' | Fecha/hora de alta del registro | Automática al insertar |
| `fecha_ultima_edicion` | TEXT DEFAULT '' | Fecha/hora de la última actualización | Automática en cada insert/update |

### 2.3. `ubicaciones`

Catálogo de ubicaciones. **En el MVP del Módulo 1 no se escribe en esta tabla** (0 filas): el Módulo 1 no extrae la ubicación de las tarjetas (decisión D29); la tabla queda reservada para la gestión del catálogo.

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `id` | TEXT (PK) | ID único (prefijo `UBI`) | No se diligencia en el Módulo 1 |
| `ciudad` | TEXT DEFAULT '' | Ciudad de la vacante | No se diligencia en el Módulo 1 |
| `region` | TEXT DEFAULT '' | Estado, provincia o departamento | No se diligencia en el Módulo 1 |
| `pais` | TEXT DEFAULT '' | País | No se diligencia en el Módulo 1 |
| `modalidad` | TEXT DEFAULT '' | Modalidad de trabajo asociada | No se diligencia en el Módulo 1 |
| `fecha_creacion` | TEXT DEFAULT '' | Fecha/hora de alta del registro | Automática al insertar |
| `fecha_ultima_edicion` | TEXT DEFAULT '' | Fecha/hora de la última actualización | Automática en cada insert/update |

### 2.4. `ofertas`

Oportunidades (vacantes) descubiertas. La escribe el **nodo Captura** mediante `upsert_oferta()`: si ya existe una fila con el mismo `id_externo` no inserta de nuevo, solo refresca `fecha_ultima_verificacion` y devuelve el `id` existente; si no, genera un ID (`OFE-NNNN`) e inserta la fila. Regla D31: los campos sin valor se guardan como `N/A` (nunca `''`/NULL); `fecha_ultima_verificacion` queda exenta (vacía hasta una re-visita).

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `id` | TEXT (PK) | ID único de la oferta (prefijo `OFE`) | Automático en la inserción (`upsert_oferta`) |
| `enlace` | TEXT NOT NULL | Enlace original de la oferta | En la inserción, desde la oferta capturada (obligatorio) |
| `titulo` | TEXT DEFAULT '' | Título original de la oferta | En la inserción, desde la oferta capturada |
| `descripcion_original` | TEXT DEFAULT 'N/A' | Contenido original obtenido en el descubrimiento (no se sobrescribe); `N/A` si no hay descripción (D31) | En la inserción, desde la oferta capturada |
| `fecha_publicacion` | TEXT DEFAULT 'N/A' | Fecha de publicación indicada por la fuente; en el Módulo 1 es timestamp aproximado derivado de "Publicado hace N <unidad>" (±1 h; mes = 30 días) (D28); `N/A` si la tarjeta no muestra fecha relativa (D31) | En la inserción, desde la oferta capturada |
| `fecha_descubrimiento` | TEXT DEFAULT '' | Fecha/hora en que la automatización descubrió la oferta | En la inserción, con la hora actual (`_now()`) |
| `estado` | TEXT DEFAULT 'descubierta' | Estado en el flujo de procesamiento (7 valores: `descubierta`, `preparada`, `evaluada`, `aceptada`, `descartada`, `procesada`, `finalizada`) | En la inserción queda `descubierta` (valor por defecto); los demás estados los asumirán módulos posteriores |
| `observaciones` | TEXT DEFAULT 'N/A' | Información adicional relevante; en el Módulo 1 conserva el texto crudo de la fecha relativa (p. ej. "Publicado hace 9 horas") (D28); `N/A` si no hay texto (D31) | En la inserción, desde la oferta capturada |
| `fecha_creacion` | TEXT DEFAULT '' | Fecha/hora de alta del registro | Automática en la inserción |
| `fecha_ultima_edicion` | TEXT DEFAULT '' | Fecha/hora de la última actualización | Automática en la inserción y en cada actualización |
| `fuente_id` | TEXT DEFAULT '' | Fuente de origen de la oferta (identificador de la fuente configurada) | En la inserción, desde la oferta capturada |
| `empresa_id` | TEXT DEFAULT 'N/A' | Referencia a la empresa del catálogo; `N/A` mientras no haya catálogo (D4: NULL en MVP; D29: el Módulo 1 no extrae la empresa; D31: NULL → `N/A`) | Sin escritura en el Módulo 1 (futuros módulos) |
| `ubicacion_id` | TEXT DEFAULT 'N/A' | Referencia a la ubicación del catálogo; `N/A` mientras no haya catálogo (D4: NULL en MVP; D29: el Módulo 1 no extrae la ubicación; D31: NULL → `N/A`) | Sin escritura en el Módulo 1 (futuros módulos) |
| `id_corrida` | TEXT DEFAULT '' | Corrida que descubrió la oferta | En la inserción, desde el contexto de la corrida |
| `id_sesion` | TEXT DEFAULT '' | Sesión de plataforma usada al descubrirla | En la inserción, desde el contexto de la sesión |
| `indice_set` | INTEGER DEFAULT '' | Índice del set de filtros que la produjo | En la inserción, desde el contexto del set actual |
| `id_externo` | TEXT DEFAULT '' | Identificador externo de la oferta en la fuente; clave de deduplicación del upsert (no se normaliza a `N/A` — D31) | En la inserción, desde la oferta capturada |
| `fecha_ultima_verificacion` | TEXT DEFAULT '' | Última fecha/hora en que la oferta fue vista de nuevo en una captura (exenta de la regla N/A — D31, punto 4) | Solo en re-visitas: `upsert_oferta()` la actualiza cuando ya existe una fila con el mismo `id_externo` |

> **D31:** la columna `identificador_origen` fue eliminada (duplicado muerto de `id_externo`, nunca escrita).

### 2.5. `corridas`

Registro de cada corrida (ejecución completa del flujo). Se crea en el **nodo INICIO** con `registrar_corrida()` (insert idempotente por `id_corrida`) y se cierra en el **nodo Finalizar** con `actualizar_corrida()`.

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `id_corrida` | TEXT (PK) | ID único de la corrida (prefijo `COR`) | En el INICIO, al crear la corrida |
| `fecha_inicio` | TEXT NOT NULL | Fecha/hora de inicio de la corrida | En el INICIO, al crear la corrida |
| `estado` | TEXT NOT NULL | Estado de la corrida (`en_ejecucion`, `corrida_completada`, `sin_fuentes`, `error`, `concurrencia`) | En el INICIO queda `en_ejecucion`; en el Finalizar se actualiza al estado final |
| `fecha_fin` | TEXT DEFAULT '' | Fecha/hora de fin de la corrida | En el Finalizar, al cerrar la corrida |
| `motivo_terminacion` | TEXT DEFAULT '' | Motivo de terminación (`corrida_completada`, `sin_fuentes`, aborto, etc.) | En el Finalizar, al cerrar la corrida |
| `total_ofertas` | INTEGER DEFAULT 0 | Ofertas registradas en la corrida (solo nuevas, por deduplicación) | En el Finalizar, desde las métricas del cierre |
| `total_errores` | INTEGER DEFAULT 0 | Total de eventos de error de la corrida | En el Finalizar, desde las métricas del cierre |
| `total_sucesos` | INTEGER DEFAULT 0 | Total de eventos de éxito de la corrida | En el Finalizar, desde las métricas del cierre |
| `fuentes_procesadas` | INTEGER DEFAULT 0 | Número de fuentes procesadas en la corrida | En el Finalizar, desde las métricas del cierre |

### 2.6. `eventos`

Bitácora de eventos (errores y sucesos) de las corridas, con `tipo` `error` o `suceso` y código de negocio. La escribe `escribir_evento()` desde los nodos: INICIO (fallos de inicialización, p. ej. ERR-10), Control de fuentes (abortos, ERR-01), Registro (resultado del registro), Captura (éxito `ofertas_registradas`, `registro_parcial`), Finalizar (terminación: `corrida_completada` como suceso o el motivo como error). Nunca se eliminan (auditoría). Regla D31: los campos sin valor se guardan como `N/A` (p. ej. el evento de terminación no tiene fuente ni sesión); `indice_set` conserva `0` como valor válido.

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `evento_id` | TEXT (PK) | ID único del evento (prefijo `EVT`) | Automático en cada `escribir_evento()` |
| `id_corrida` | TEXT NOT NULL | Corrida a la que pertenece el evento (obligatorio) | En cada `escribir_evento()`, desde el contexto de la corrida |
| `fuente_id` | TEXT DEFAULT 'N/A' | Fuente sobre la que ocurrió el evento; `N/A` en eventos de corrida (INICIO, Finalizar) | En eventos con contexto de fuente (Captura, Registro); `N/A` en el resto (D31) |
| `id_sesion` | TEXT DEFAULT 'N/A' | Sesión de plataforma del evento; `N/A` si el evento no es de sesión | En eventos de Captura/Registro con sesión activa; `N/A` en el resto (D31) |
| `indice_set` | INTEGER DEFAULT 'N/A' | Índice del set de filtros donde ocurrió; `N/A` si no aplica (`0` es válido) | En eventos de Captura/Registro con set activo; `N/A` en el resto (D31) |
| `marca_temporal` | TEXT NOT NULL | Fecha/hora exacta del evento | En cada `escribir_evento()` (o automática si no se provee) |
| `tipo` | TEXT NOT NULL | Clasificación: `error` o `suceso` | En cada `escribir_evento()`, según el resultado del nodo |
| `codigo` | TEXT NOT NULL | Código de negocio (`ERR-01`, `ERR-10`, `ofertas_registradas`, `registro_parcial`, motivo de terminación, etc.) | En cada `escribir_evento()` |
| `evidencia` | TEXT DEFAULT 'N/A' | Evidencia: trazas, fragmentos, métricas asociadas; `N/A` si no hay payload | En cada `escribir_evento()` (nunca credenciales); `N/A` si vacío (D31) |

> **D31:** la columna `id_oferta` fue eliminada (nunca escrita en el Módulo 1; la trazabilidad evento-oferta no está implementada).

### 2.7. `sesiones`

Auditoría de las sesiones de plataforma por lote capturado. La escribe el **nodo Captura** con `escribir_fila("sesiones")` tras procesar cada lote (con reintento si falla).

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `id` | TEXT (PK) | ID único del registro de sesión (prefijo `SES`; en migración hereda el valor de `id_sesion`) | Automático en la inserción |
| `id_sesion` | TEXT NOT NULL | Identificador de la sesión asignado por la plataforma/fuente | En la Captura, desde el contexto de la sesión |
| `id_corrida` | TEXT NOT NULL | Corrida bajo la cual se estableció la sesión | En la Captura, desde el contexto de la corrida |
| `fuente_id` | TEXT NOT NULL | Fuente sobre la que se estableció la sesión | En la Captura, desde la fuente corriente |
| `indice_set` | INTEGER DEFAULT '' | Índice del set de filtros de la sesión | En la Captura, desde el set corriente |
| `marca_temporal` | TEXT NOT NULL | Fecha/hora de establecimiento de la sesión | En la Captura, con la hora actual |
| `total_declarado` | INTEGER DEFAULT '' | Total de ofertas declarado por la fuente, cuando lo expone | En la Captura, desde la página de resultados |
| `conteo` | INTEGER DEFAULT '' | Ofertas capturadas en el lote | En la Captura: tamaño del lote procesado |
| `estado` | TEXT NOT NULL | Estado final de la sesión | En la Captura, al auditar el lote (`completa`) |
| `fecha_creacion` | TEXT DEFAULT '' | Fecha/hora de alta del registro | Automática en la inserción |
| `fecha_ultima_edicion` | TEXT DEFAULT '' | Fecha/hora de la última actualización | Automática en la inserción y en cada actualización |

### 2.8. `bloqueo`

Bloqueo de concurrencia de corridas (una sola corrida activa a la vez). Máximo una fila. La escribe el **nodo INICIO** con `adquirir_bloqueo()` (insert, o update por obsolescencia o con `forzar`) y la elimina el **nodo Finalizar** con `liberar_bloqueo()`. El INICIO también hace una prueba de escritura con `sondear_escritura()` (insert + rollback, sin dejar datos).

| Columna | Tipo | Qué hace | Cuándo se diligencia |
|---|---|---|---|
| `id_corrida` | TEXT (PK) | Corrida dueña del bloqueo | En el INICIO, al adquirir el bloqueo (insert o update por obsolescencia/forzado) |
| `marca_temporal` | TEXT NOT NULL | Fecha/hora de adquisición del bloqueo; base para el umbral de obsolescencia | En el INICIO, al adquirir el bloqueo; se actualiza al renovar el bloqueo |
