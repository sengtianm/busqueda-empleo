# Análisis Comparativo: Ficha técnica Módulo 1 vs. diseño y código actual

> Documento de referencia para el análisis de la Fase 4 (Módulo 1 — Descubrimiento de oportunidades).
> Compara la especificación canónica `docs/diagrams/Ficha técnica - Diagrama de flujo (Descubrimiento de oportunidades).md` contra los documentos de diseño (DOC-*) y el código implementado en las Fases 1-3.

**Fecha:** 07/08/2026 · **Rama:** `modulo-1`

---

## Alcance y fuentes analizadas

- **Ficha técnica** (completa, 1364 líneas): 13 especificaciones canónicas (INICIO + 6 procesos + 6 decisiones + Finalizar Proceso).
- **Código:** `shared/models.py`, `shared/persistence.py`, `shared/errors.py`, `shared/config.py`, `shared/retry.py`, `shared/logging_setup.py`, `shared/state_machine.py`, `config/config.yaml`.
- **Documentos de diseño:** DOC-00 a DOC-13 (relevantes: 01, 04, 06, 07, 09, 11, 12, 13, 13A) y Apéndices 5A y 9A.

> Aclaración previa: la ficha tiene **13 nodos canónicos, no 11** (INICIO + 5 procesos + 6 decisiones + Finalizar Proceso). El tracker del MVP ya lo refleja así.

---

## 1. CONFLICTOS con la arquitectura actual

| # | Ficha técnica | Diseño/código actual | Contradicción exacta | Qué cambiar |
|---|---|---|---|---|
| C1 | "¿Existe al menos una fuente configurada?" RN-02: *"No existen estados habilitada/deshabilitada en esta etapa del diseño"* | Tabla `fuentes.activa` (`shared/persistence.py:38`) y entidad Source con `active: bool` (Documento 13A §2.2, con constraint "no asociar ofertas a fuente inactiva") | La ficha niega el estado habilitada/deshabilitada pero el modelo de datos y la BD ya lo tienen | **Documento**: resolver la semántica. Se recomienda mantener `activa` como atributo de catálogo (gestión manual posterior) y que la ficha lo ignore en runtime; decidirlo explícitamente y anotarlo en DOC-01/DOC-13A |
| C2 | Nodo "Registrar ofertas en 'Ofertas Totales'": *"información original íntegra tal como llegó del adaptador"*, `id_externo_url` nullable, prohibido transformar | Esquema `ofertas` con `titulo TEXT NOT NULL, descripcion_original TEXT NOT NULL, url TEXT NOT NULL` (persistence.py:69-74) | Si el adaptador devuelve una oferta sin título o sin descripción, el INSERT crudo falla por NOT NULL — contradice "lo crudo se conserva crudo" | **Código** (esquema): relajar NOT NULL de `titulo`/`descripcion_original` (mantener `url` o `source_identifier` como referente) |
| C3 | Todo registro lleva `run_id` + `source_id` + `session_id` + `set_indice` (RN-01 de INICIO; RN-06 de Selección; trazabilidad en todos los nodos) | Tabla `ofertas` no tiene ninguna de esas columnas; solo `fuente_id` (FK) y `source_identifier` | La trazabilidad exigida por la ficha no tiene dónde persistirse | **Código + DOC-13/13A**: agregar columnas `run_id`, `session_id`, `set_indice`, `id_externo_url` (o mapear `source_identifier`) |
| C4 | "verifica disponibilidad y permisos de escritura de **las bases de datos del módulo**: 'Ofertas Totales', 'errores o sucesos', 'control de sesiones'..." | DOC-11: SQLite de archivo único `job_search.db`; persistence.py maneja una sola BD con 5 tablas; no existen "errores o sucesos" ni "control de sesiones" | "Multi-BD" se lee como multi-archivo | No es contradicción real (la ficha es agnóstica de tecnología, §1.13 de INICIO). **Resolución recomendada**: un único archivo SQLite con tablas lógicas separadas (`ofertas`, `eventos`, `sesiones`, `corridas`, `bloqueo`). Anotarlo en DOC-04/DOC-11 |
| C5 | "Ofertas Totales" como almacén crudo, inserción de filas nuevas "sin deduplicación" | Tabla `ofertas` única y central con `estado` CHECK ('discovered'...'finalized') | La ficha no menciona el campo `estado`; la base lo exige (CHECK, default 'discovered') | Compatible si se documenta: M1 inserta con `estado='discovered'` (asignación EST-001 que DOC-01/FP-01 atribuye a M1). Agregar nota en DOC-01 y en el nodo de registro |
| C6 | Reintentos "condicionales por código" (solo `fuente_inalcanzable`, `timeout_*`) con backoff; cada reintento desde canal cerrado | `shared/retry.py` = tenacity genérico: reintenta la función completa ante cualquier excepción, sin distinguir códigos | El mecanismo actual reintentaría bloqueos/captcha (prohibido por RN-03 de "Entrar" y RN-06 de "Aplicar filtros") | **Código**: en el módulo discovery no reusar `retry_decorator` directamente; implementar helper de reintento condicional por código |
| C7 | La ficha usa códigos locales `ERR-01..ERR-12`, `EVT-01` por nodo y "codigo_motivo" (`fuente_inalcanzable`, `bloqueo_plataforma`, ...) | `shared/errors.py` con jerarquía ER-RED/ER-NAV/ER-EXT/... `ER-\<CATÉGORIA\>-\<NNN\>` (DOC-06, categorías CER-001..010) | Dos nomenclaturas paralelas; la ficha no mapea ERR-nn a ER-CAT | **No es contradicción**: los ERR-nn son códigos de negocio por nodo; los ER-Cat son la capa técnica. Documentar el mapeo (p. ej. `fuente_inalcanzable` → ER-RED/ER-EXT, `bloqueo_plataforma` → ER-NAV) en DOC-06 |

**Conclusión C1-C7:** el único conflicto que requiere cambio de diseño es C1 (semántica de `activa`); C2 y C3 requieren cambio de esquema; C4 es de redacción; C5 requiere aclaración; C6 y C7 son puntos de integración del código nuevo.

*No determinado con certeza:* el alcance de C1 (qué hace `activa` para Módulo 2+) no está decidido en ningún documento — requiere definición de negocio del usuario.

---

## 2. ELEMENTOS NUEVOS que la ficha introduce y NO existen

| Concepto | Qué hace según la ficha | ¿Existe algo similar? | ¿Crear o adaptar? |
|---|---|---|---|
| `corrida` + `run_id` | Instancia de ejecución única; todo registro queda enlazado (RN-01 de INICIO) | Antecedentes de requisito: DI-001 (DOC-01), RER-016 (DOC-06), DFT-001 (DOC-04), sin implementación | **Crear**: entidad `corridas` + generador de ID (patrón `PREFIXES`; nuevo prefijo, ej. COR — actualizar Apéndice 5A) |
| Contexto de ejecución (objeto único transmitido entre nodos) | Estructura única con config validada, lista filtrada, iteradores, bloqueo, conexiones y resultados por nodo | No existe (solo `shared/config.py` estático con caché) | **Crear** (nuevo módulo `modules/discovery/run_context.py`) |
| Bloqueo de concurrencia persistente + umbral de obsolescencia | Solo una corrida activa; bloqueo en BD con `run_id` + timestamp; obsolescencia configurable (ERR-06/07/09) | Nada | **Crear**: tabla `bloqueo` + operaciones adquirir/liberar/verificar |
| `session_id` + almacén "control de sesiones" | Sesión de plataforma solo en éxito; auditoría por (session_id, set_indice) | Nada (el modelo de datos no tiene entidad Sesión) | **Crear**: tabla `sesiones` + modelo `AuditoriaSesion` |
| Almacén seguro de credenciales | Accedido solo por "Entrar a la fuente"; nunca se registra en logs/BD | `config/.env` via dotenv (`shared/config.py`) existe, sin concepto de "almacén seguro" | **Adaptar**: usar `.env` (referencias en config; valores en `.env`) o keyring del SO; decisión técnica pendiente |
| Ficha de acceso por fuente (tipo `publico|con_autenticacion`, referencia de credenciales, criterio verificable de ingreso exitoso, timeout) | Esquema de acceso de cada fuente, validado en INICIO | Entidad `Source` de DOC-13A casi vacía en esto | **Extender** `Source` (modelo + config) o crear `FichaAcceso` |
| `sets_de_filtros` por fuente (lista ordenada; set vacío = búsqueda base) | Iterador de sets en "Aplicar filtros" | `config.yaml > search.keywords` global (una lista plana) | **Adaptar**: reestructurar; los keywords pueden ser el primer set. Crear `SetFiltros` |
| `politicas_de_captura` por fuente (`max_paginas`, `max_ofertas_por_corrida`, `pausa_entre_lotes`, `estrategia_anti_bloqueo`) + defaults globales (RN-11) | Límites y pausas de captura | `search.max_pages` (5) y `search.max_offers_per_page` (25) existen pero globales y de otra semántica | **Adaptar**: mover a `captura` (default global) + por fuente (opcional) |
| "errores o sucesos" (almacén de eventos) | Eventos críticos/sucesos con run_id + tipología | Entidad `Event` **existe en DOC-13A** (entidad n.º 10 del inventario) pero no hay tabla ni código | **Crear**: tabla `eventos` en SQLite (adaptando la entidad Event del 13A) |
| `entry_result`, `search_result`, `capture_batch`, `estado_captura`, `set_indice` | Contratos estructurados entre nodos | Nada | **Crear** modelos Pydantic (en `shared/models.py` o en el módulo discovery) |
| Grupo A / Grupo B de códigos (comprometen fuente vs. propios del set) | Política centralizada de cierre de fuente (RN-03 de la decisión de sets) | Nada | **Crear** (Enums + clasificación en el nodo de decisión) |
| Adaptador de plataforma (mecanismo masivo/incremental, RN-10) | Encapsula filtros, parsado y captura por fuente | DOC-12 §10.1 describe el modelo adaptador; interfaces INT-001/INT-003 declaradas | **Crear**: `modules/discovery/adapters/linkedin.py` conforme a INT-001/INT-003 |
| Descarte de fuente por ficha incompleta (ERR-12) + tri-nivel aborto / terminación controlada / descarte | Operativa de inspección de fuentes | DOC-06 REC-008 "terminación controlada" existe como estrategia | Compatible; mantener |
| Registro crítico local como respaldo (ERR-01..04) | Consola/archivo cuando el almacén de eventos no está disponible | Loguru (`shared/logging_setup.py`) lo cubre | **Adaptar** (reusar loguru como mecanismo local); documentar destino |

---

## 3. ELEMENTOS ACTUALES que la ficha NO menciona o contradice

| Existe actualmente | ¿La ficha lo reemplaza, ignora o es compatible? | ¿Mantener, modificar o eliminar? |
|---|---|---|
| `config/config.yaml > search` (keywords, location, modality, max_pages, max_offers_per_page) | **Reemplaza** (por fuente con ficha + sets + políticas) | **Modificar**: desmontar; keywords → primer set base; límites → `politicas_de_captura` globales |
| `config.yaml > browser` (headless, timeout_seconds, profile_path) | **Sustituye** (timeout por fuente con default global) | Mantener como defaults globales; `profile_path` puede servir para LinkedIn con sesión persistida |
| Sección `retries` global (3 intentos, backoff 2-30 s) | **Complementa**: la ficha usa "máx. reintentos por defecto 2" global | Mantener como default global; ajustable por nodo |
| `shared/models.py > Offer.source_identifier` | **Equivale** a `id_externo_url` (best-effort, nullable) | Mantener; documentar `id_externo_url` como alias conceptual |
| `ofertas.estado` + `shared/state_machine.py` (7 estados EST) | **Ignora** (M1 no usa estados de oferta; DISCOVERED→PREPARED es del Módulo 2) | Mantener intacto; M1 escribe `discovered` por defecto |
| `BaseError` con `source_module`, `offer_id`, severidad SV-1..5 | **Compatible**; la ficha exige además run/source/session/set en los eventos | Mantener + extender con campos de trazabilidad |
| `shared/ia_service.py`, `shared/decision_engine.py` | **Ignora** totalmente (M1 no usa IA ni decisión) | Intactos |
| `shared/retry.py` (tenacity genérico) | Válido global; insuficiente para lógica condicional (ver C6) | Mantener para otros módulos; helper nuevo para M1 |
| `shared/logging_setup.py` | Compatible como "registro crítico local" | Mantener sin cambios |
| Tabla `fuentes` (id, nombre, tipo, url_base, activa) | **Insuficiente**: falta casi toda la ficha de acceso | Modificar: expandir con campos de ficha o crear tabla auxiliar (decisión técnica) |
| `persistence.py > write_row` (INSERT con commit por fila) | **Insuficiente** para lote transaccional (RN-06 "todo o nada") | Modificar: añadir `write_batch` transaccional + rollback |

---

## 4. EVALUACIÓN COMPARATIVA: ¿Es mejor el diseño de la ficha?

| Área | Diseño actual | Propuesta de la ficha | ¿Cuál es mejor? | Justificación |
|---|---|---|---|---|
| Arquitectura de persistencia | SQLite 1 archivo, 5 tablas, sin eventos/sesiones/corridas | Almacenes lógicos ("Ofertas Totales", "errores o sucesos", "control de sesiones", bloqueo) | **Ficha** (con matiz: un solo SQLite) | Separa responsabilidades, habilita auditoría y trazabilidad; no requiere multi-archivo |
| Modelo de ejecución | Sin contexto; utilidades independientes | Contexto único con `run_id`, iteradores, bloqueo, sesión | **Ficha** | Sin contexto no hay reinicio seguro, trazabilidad integral ni concurrencia; DOC-04/06 ya pedían IDs de ejecución (DI-001/RER-016) |
| Manejo de errores | REP-* genéricos + log | ERR-nn locales + codigo_motivo + Grupo A/B + aborto/terminación/descarte | **Ficha** (dual: ERR-nn = negocio, REP-* = técnico) | REP-* no distingue reintentable/irreversible ni escala por nodo; los codigos de motivo habilitan política centralizada |
| Configuración de fuentes | `search` global + `Source` mínima | Ficha de acceso + `sets_de_filtros` + `politicas_de_captura` por fuente | **Ficha** | Múltiples búsquedas, control de límites y credenciales; coherente con DOC-09 (LinkedIn) y con la entidad Source del 13A |
| Concurrencia | No existe | Bloqueo persistente con obsolescencia | **Ficha** | Evita ejecuciones paralelas duplicadas; la obsolescencia permite recuperar corridas caídas |
| Sesiones y credenciales | No existe (solo `.env` genérico) | Almacén seguro + `session_id` + auditoría de sesión | **Ficha** | Reuso de sesión entre sets/lotes, control de expiración (`sesion_lle_expira`), nunca registrar credenciales |
| Trazabilidad | `fuente_id` + fechas | `run_id` + `source_id` + `session_id` + `set_indice` en todo registro | **Ficha** | Requisito explícito de DOC-04 (DFT-001) y DOC-06 (RER-016); permite auditoría completa |
| Adaptadores de plataforma | No existe módulo | Patrón adaptador (masivo/incremental, reintentos, parseo) | **Ficha** | Único camino para cumplir DOC-09/9A (LinkedIn cambiante, captchas) manteniendo extensibilidad a otras fuentes |
| Reintentos | Genéricos (tenacity sobre cualquier excepción) | Condicionales por código + backoff + cierre de canal | **Ficha** | Reintentar captcha/autenticación rechazada aumenta el riesgo de bloqueo (DE-LI-007 de 9A) sin beneficio |

**Veredicto: la ficha es superior en todas las áreas.** No reemplaza los DOC (principios y catálogos); es la especificación operativa que faltaba y es coherente con todos ellos.

---

## 5. IMPACTO en documentos de diseño existentes (priorizado)

| Pri. | Documento | Cambio | Criticidad |
|---|---|---|---|
| 1 | **DOC-13 + Documento 13A** (Modelo de datos) | Entidad Offer amplía trazabilidad; nuevas entidades: Corrida, Sesión, Bloqueo de corrida; formalizar Evento; resolver constraint de `activa` (C1) | **Mayor** (reescribir dominio M1) |
| 2 | **DOC-04** (Flujo de datos) | Agregar el flujo detallado de M1 (orquestación por nodos con `run_id`); trazabilidad; envolver los almacenes (ofertas/errores/sesiones) | **Mayor** (nueva sección M1) |
| 3 | **DOC-06** (Manejo de errores) | Catálogo local ERR-nn por nodo + mapeo a REP-* categorías; reintentos condicionales por código (REC-003); estados de terminación normal/concurrencia/error; Grupo A/B | **Mayor** (nuevo catálogo M1) |
| 4 | **DOC-01** (Requisitos) | RF del M1: corrida, concurrencia, sesión, credenciales, políticas, sets; resolver C1; asignación de estado "discovered" | **Medio** |
| 5 | **DOC-12** (Arquitectura) | CMP-001 detallado en submódulos; servicios: run manager, lock, adaptadores (SRV-003, SRV-004, SRV-005); almacén de credenciales | **Medio** |
| 6 | **DOC-09 + Anexo 9A** | Definir la implementación para LinkedIn: criterio verificable de ingreso exitoso, sets de filtros oficiales, políticas de captura, tratamiento de captcha/bloqueo → códigos | **Medio** |
| 7 | **DOC-00** (Glosario) | Nuevos términos: corrida, run_id, session_id, lote, set_indice, políticas de captura, bloqueo, almacenes, entry_/search_/capture_ result, estado_captura, Grupo A/B, adaptador | **Menor** |
| 8 | **Apéndice 5A** | Nuevos prefijos: COR (corridas), SES, EVT, BLO | **Menor** |
| 9 | **DOC-05 / Ap 5C** | Formatos de eventos/auditoría; convención para códigos por nodo | **Menor** |

**Sin cambios necesarios:** DOC-02, DOC-03, DOC-07, DOC-08, DOC-11 (SQLite confirmado).

---

## 6. IMPACTO EN CÓDIGO YA IMPLEMENTADO (Fases 1-3)

### 6.1 Archivos a modificar

| Archivo | Cambio | No cambiar |
|---|---|---|
| `shared/persistence.py` | Nuevas tablas (`corridas`, `eventos`, `sesiones`, `bloqueo`); `write_batch` transaccional (todo o nada + rollback); métodos de bloqueo (acquire/release/check + obsolescencia); `PREFIXES` actualizado | `generate_id`, `read_table`, `find_by_id`, `update`, `change_path` |
| `shared/models.py` | Nuevos modelos: `Corrida`, `RunContext`, `EventoAlmacen`, `AuditoriaSesion`, `PoliticasCaptura`, `FichaFuente/FuenteAcceso`, `SetFiltros`, `EntryResult`, `SearchResult`, `CaptureBatch`, `EstadoCaptura`; extender `Offer` con `run_id`, `session_id`, `set_indice`, `id_externo_url` | Modelos existentes |
| `shared/errors.py` | Extender `BaseError` con campos opcionales `run_id`, `source_id`, `session_id`, `set_indice`; añadir categoría `RE-SES` solo si se requiere | Jerarquía y severidades |
| `shared/retry.py` | Añadir `retry_conditional(codes)` / `should_retry(code)` para reintento por código | `retry_decorator` para los demás módulos |
| `config/config.yaml` | Sustituir/adaptar sección `search`; agregar `fuentes` (ficha de acceso, sets, políticas), `almacen_credenciales` (referencias), `concurrencia` (umbral), `captura` (defaults globales RN-11) | Resto de secciones |

### 6.2 Archivos SIN cambios

- `shared/config.py` (lectura YAML genérica)
- `shared/state_machine.py` (M1 no usa estados de oferta)
- `shared/llm_service.py` y `shared/decision_engine.py` (pertenecen a otros módulos)
- `shared/logging_setup.py` (servirá de "registro crítico local" tal cual)

### 6.3 Pruebas

- `tests/conftest.py`: fixture de BD debe inicializar las nuevas tablas; nuevos fixtures (`example_fuente`, `example_set`, `example_politicas`, ...). Mantener los existentes.

### 6.4 Nuevo paquete

- `modules/discovery/` (nodo por nodo, según plan Fase 4): `run_context.py`, implementación de los 13 nodos, `adapters/linkedin.py`, reintento condicional.

### 6.5 Puntos abiertos DENTRO de la ficha

1. Nodo **"Registrar error o suceso en 'errores o sucesos'"** — la ficha lo referencia constantemente en las ramas No de las decisiones, pero **no tiene especificación canónica propia**.
2. **"¿Es la primera ejecución del ciclo?"** — la especificación de la decisión de existencia aún lo nombra como sucesor Sí (líneas 160/186) mientras el resto del documento lo superó por "¿Quedan fuentes por procesar?" (inconsistencia interna).
3. **"Capturar ofertas" v1.1** — reedición con `set_indice` en `estado_captura`, "aprobada y por entregar", aún sin escribir.
4. **"Finalizar Proceso"** — spec en estado *borrador*, con 6 puntos de validación pendientes de aprobación.

---

## 7. RECOMENDACIÓN FINAL

**a) ¿Es la ficha un mejor diseño que el actual? — Sí, claramente.**
La ficha es la especificación operativa del Módulo 1 que faltaba: contratos por nodo, trazabilidad completa (`run_id`/`source_id`/`session_id`/`set_indice`), concurrencia, sesiones, políticas de captura y reintentos condicionales. Los DOC definían principios y catálogos sin "cómo ejecutar"; la ficha los confirma sin contradecirlos. El código de Fases 1-3 no se pierde: son servicios transversales que se extienden, no se reescriben.

**b) ¿Qué NO implementar?**
- **Multi-archivo de BD**: los almacenes serán tablas lógicas de un único SQLite (DOC-11; la ficha es agnóstica).
- **Auditoría de sesión completa en el MVP**: mínimo viable `{session_id, run_id, source_id, set_indice, timestamp, total_declarado, conteo, estado}`; ampliar después.
- **Complejidad extra de concurrencia**: implementación simple (tabla `bloqueo` + umbral), sin infraestructura adicional.

**c) ¿Qué es imprescindible?** — La trazabilidad en cada registro, la ficha de acceso por fuente, `sets_de_filtros`, `politicas_de_captura`, el bloqueo persistente, el almacén seguro de credenciales, el adaptador de plataforma, los reintentos condicionales y los códigos de error por nodo. Sin ellos el módulo no cumple DOC-01/FF-01 ni DOC-04/DFT.

**d) Estrategia: adoptarla completamente** como especificación canónica del M1, resolviendo:
1. Los 4 puntos abiertos internos (§6.5).
2. Las dos adaptaciones técnicas: un único SQLite (almacenes lógicos) y la semántica de `activa` (C1).

La construcción nodo por nodo del plan Fase 4 ya existe y queda alineada con la ficha.

**e) Orden de actualización de documentos ANTES de escribir código**
1. **DOC-13 + 13A** (esquemas, entidades nuevas) — bloquea a `persistence.py`.
2. **DOC-04** (flujo de datos M1) — bloquea la orquestación y los almacenes.
3. **DOC-06** (catálogo ERR + mapeo ER-* + reintentos condicionales) — bloquea "INICIO" y manejadores.
4. **DOC-01** (RF del M1 + resolución C1) — bloquea RN-08.
5. **DOC-12** (submódulos, servicios, adaptadores) — bloquea la arquitectura de `modules/discovery`.
6. **DOC-09/Anexo 9A** (especificación LinkedIn: criterio de ingreso, sets, políticas por defecto) — bloquea "Entrar a la fuente" y "Aplicar filtros".
7. **DOC-00 + Ap 5A + DOC-05** (glosario, prefijos, formatos de eventos).
8. Después: `config.yaml`, `persistence.py`, `models.py` y el módulo discovery.

---

## Información requerida para cerrar el análisis

1. Decisión sobre la semántica de `activa` (C1).
2. Confirmación de "un único SQLite, almacenes lógicos".
3. Aprobación de los 6 puntos de validación de "Finalizar Proceso" y de la reedición "Capturar ofertas v1.1".
4. Mecanismo de almacenamiento de credenciales (`.env` vs. almacén del sistema).