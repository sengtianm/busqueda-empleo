# Plan de Preparación: Fase 4 (Módulo 1 — Descubrimiento de oportunidades)

> Plan de preparación previo a la construcción de la Fase 4, construido **exclusivamente** sobre el informe `docs/reports/Análisis Comparativo - Ficha técnica Módulo 1.md` (referencias: C1-C7, elementos nuevos §2, tabla §5, código §6.1, paquete §6.4, puntos abiertos §6.5, recomendación §7).
> No se propone nada que el análisis no haya identificado.

**Fecha:** 07/08/2026 · **Rama:** `modulo-1`

---

## 1. RESOLUCIÓN DE LOS 4 PUNTOS ABIERTOS

| # | Pregunta binaria (A vs B) | Opción recomendada por el análisis | Por qué | Documentos/archivos afectados | ¿Bloquea? |
|---|---|---|---|---|---|
| **D1** | C1: ¿`fuentes.activa` se mantiene como **atributo de catálogo** (gestión manual, ignorado en runtime) o se **elimina** del esquema? | **A — Mantener** (§1, "mantener `activa` como atributo de catálogo y que la ficha lo ignore en runtime") | El dato ya existe en BD (`persistence.py:38`) y modelo (13A §2.2); eliminarlo obliga una migración sin beneficio; la ficha niega el estado solo "en esta etapa del diseño" (RN-02) | DOC-01 (RF), DOC-13A §2.2 (constraint), `fuentes.activa`, config `fuentes` | **SÍ — ALTA**: bloquea DOC-13/13A, DOC-01 y config.yaml |
| **D2** | C4: ¿**un único SQLite con almacenes lógicos** (`ofertas`, `eventos`, `sesiones`, `corridas`, `bloqueo`) o **multi-archivo**? | **A — Único SQLite, almacenes lógicos** (§1 C4; §4 "Ficha (con matiz: un solo SQLite)"; §7b "No implementar multi-archivo") | DOC-11 ya confirma SQLite de archivo único; la ficha es agnóstica de tecnología (§1.13 de INICIO); multi-archivo añade complejidad sin beneficio (§7b) | DOC-04 (almacenes), DOC-13 (tablas lógicas), `persistence.py` | **SÍ: ALTA**: bloquea DOC-13/13A, DOC-04 y `persistence.py` |
| **D3** | ¿Se aprueban los 6 puntos de validación de "Finalizar Proceso" y la reedición "Capturar ofertas v1.1" **con alcance MVP mínimo** (auditoría `{session_id, run_id, source_id, set_indice, timestamp, total_declarado, conteo, estado}` de §7b) o **con auditoría completa**? | El análisis define el **mínimo viable como criterio en §7b**, pero **no da recomendación A/B explícita** sobre los 6 puntos | §6.5: son 2 de los 4 puntos abiertos internos de la ficha; §7b recorta auditoría de sesión y complejidad de concurrencia para el MVP | Ficha técnica (nodos "Capturar ofertas" y "Finalizar Proceso"), DOC-01/DOC-04 (alcance de sesión) | **NO** bloquea la preparación (MEDIA): bloquea los nodos "Capturar" y "Finalizar" en la construcción |
| **D4** | ¿Credenciales en **`.env`** (**referencias en config, valores en `.env`** — patrón ya usado por `shared/config.py` vía dotenv) o **keyring del SO**? | El análisis **no recomienda explícitamente** ("`.env` ... o keyring del SO; decisión técnica pendiente", fila de almacén seguro en §2) | Dato factual: la infraestructura dotenv ya existe (§2, "Adaptar"); no hay más información en el análisis | config.yaml (sección `almacen_credenciales`), DOC-01 (RF credenciales), DOC-12 (almacén) | **MEDIA**: bloquea config.yaml, DOC-01 y DOC-12; no bloquea DOC-13 ni `persistence.py` |

**Nota:** el análisis pide "definición de negocio del usuario" solo para C1 (§1). Para D3 y D4 el análisis no da información suficiente para recomendar una opción; quedan a decisión del usuario (ver §6).

---

## 2. PLAN DE ACTUALIZACIÓN DE DOCUMENTOS (tabla §5 del análisis, prioridades 1-9)

| Prio | Documento | Secciones específicas a cambiar | Qué aporta el análisis | Depende de | Criterio de validación |
|---|---|---|---|---|---|
| 1 | **DOC-13 + Documento 13A** | Entidad Offer: ampliar trazabilidad (`run_id`, `session_id`, `set_indice`, `id_externo_url`); nuevas entidades: Corrida, Sesión, Bloqueo de corrida; formalizar Evento (entidad n.º 10 del 13A); resolver constraint de `activa` (C1) | §5 prio 1; C1, C3, C5; elementos nuevos de §2 (corrida, sesión, bloqueo, eventos) | **D1, D2** | Cualquier tabla nueva de `persistence.py` mapea 1:1 a una entidad del 13A; Offer con los 4 campos de trazabilidad; Evento con `run_id` + tipología; `activa` resuelto según D1 |
| 2 | **DOC-04** | Nueva sección de flujo M1: orquestación por nodos con `run_id`; envolver los almacenes lógicos (ofertas, errores o sucesos, control de sesiones) | §5 prio 2; C4 (resolución "un SQLite, almacenes lógicos"); trazabilidad (DFT-001 citado en §4) | DOC-13/13A (5) | El flujo cubre los **13 nodos** con sus contratos (`entry_result`, `search_result`, `capture_batch`); cada nodo conecta a un almacén lógico |
| 3 | **DOC-06** | Catálogo local **ERR-01..ERR-12 + EVT-01** por nodo con `codigo_motivo`; tabla de mapeo ERR-nn → categoría ER-* (CER-001..010); reintentos condicionales (REC-003); Grupo A/B; estados de terminación (normal / concurrencia / error) | §5 prio 3; C7 (mapeo dual; ejemplos: `fuente_inalcanzable` → ER-RED/ER-EXT, `bloqueo_plataforma` → ER-NAV) | DOC-13/13A | Cada `codigo_motivo` de la ficha tiene mapeo a ≥1 ER-*; el catálogo identifica qué códigos se reintentan (solo `fuente_inalcanzable`, `timeout_*`) y qué códigos bloquean la fuente (Grupo A). Nota: el análisis usa "REP-*" y "ER-*" de forma intercambiable (C7 vs §4/§5); fijar una sola nomenclatura en DOC-06 |
| 4 | **DOC-01** | RF del M1: corrida, concurrencia, sesión, credenciales, políticas, sets; nota de asignación `estado='discovered'` (C5); resolución C1 (D1) | §5 prio 4; C1, C5 ("agregar nota en DOC-01"); §7c (imprescindibles FF-01) | **D1, D4**, DOC-13 | Cada RF de la lista "imprescindible" de §7c (trazabilidad, ficha de acceso, sets, políticas, bloqueo, credenciales, adaptador, reintentos, códigos) existe como RF numerada |
| 5 | **DOC-12** | CMP-001 desglosado en submódulos; servicios run manager, lock, adaptadores (**SRV-003, SRV-004, SRV-005**); almacén de credenciales; interfaces **INT-001/INT-003** | §5 prio 5; §2 (adaptador conforme a INT-001/003, DOC-12 §10.1) | DOC-01, DOC-13/13A | La estructura de `modules/discovery/` (package, `run_context.py`, `adapters/`) es derivable 1:1 de DOC-12 |
| 6 | **DOC-09 + Anexo 9A** | Criterio verificable de ingreso exitoso; sets de filtros oficiales; políticas de captura por defecto; captcha/bloqueo → códigos | §5 prio 6; §4 (DE-LI-007: reintentar captcha aumenta riesgo de bloqueo) | DOC-12, DOC-01 | Con solo DOC-09/9A + la ficha se puede implementar "Entrar a la fuente" y "Aplicar filtros" |
| 7 | **DOC-00 (Glosario)** | Nuevos términos: corrida, run_id, session_id, lote, set_indice, políticas de captura, bloqueo, almacenes, entry_/search_/capture_result, estado_captura, Grupo A/B, adaptador | §5 prio 7 | Documentos 1-6 ya actualizados | Todos los términos usados en DOC-01/04/06/12/09 tienen entrada en el glosario |
| 8 | **Apéndice 5A** | Nuevos prefijos: **COR** (corridas), **SES**, **EVT**, **BLO** | §5 prio 8; §2 (fila corrida: "nuevo prefijo, ej. COR") | DOC-13/13A | `generate_id('COR')` produce IDs válidos; prefijos registrados y únicos |
| 9 | **DOC-05 / Ap 5C** | Formatos de eventos / auditoría; convención de códigos por nodo | §5 prio 9 | DOC-06, DOC-04 | Un evento de ejemplo cumple el formato del Ap 5C y la auditoría mínima de §7b |

**Aclaración:** DOC-11 **no requiere cambios** ("SQLite confirmado", §5 y §7), aunque C4 lo cita ("anotarlo en DOC-04/DOC-11"); la anotación se hará solo en DOC-04.

---

## 3. PLAN DE CAMBIOS EN CÓDIGO EXISTENTE (§6.1 del análisis)

| Archivo | Cambio específico | Justificación (análisis) | Documento previo | Tests a agregar/modificar | Riesgo de romper |
|---|---|---|---|---|---|
| `shared/models.py` | Modelos nuevos: `Corrida`, `RunContext`, `EventoAlmacen`, `AuditoriaSesion`, `PoliticasCaptura`, `FichaFuente/FuenteAcceso`, `SetFiltros`, `EntryResult`, `SearchResult`, `CaptureBatch`, `EstadoCaptura`; enums Grupo A/B (§2); **extender `Offer`** con `run_id`, `session_id`, `set_indice`, `id_externo_url` (opcionales) | §6.1; C3; §2 (elementos nuevos) | DOC-13/13A | Tests de validación para los nuevos modelos y campos; los tests de `Offer` actuales siguen pasando (campos opcionales) | **Bajo**: campos opcionales no rompen constructores existentes |
| `shared/persistence.py` | Nuevas tablas: `corridas`, `eventos`, `sesiones`, `bloqueo`; `write_batch` transaccional (todo-o-nada + rollback, RN-06 "todo o nada" de la ficha; §3 fila `write_row`); métodos de bloqueo `acquire/release/check` con umbral de obsolescencia; `PREFIXES` actualizado; relajar NOT NULL de `titulo`/`descripcion_original` (C2) | §6.1; C2, C3; §2 (bloqueo, corrida, sesión, eventos) | DOC-13/13A, Ap 5A | Tests de las 4 tablas nuevas, `write_batch` (rollback en fallo a mitad), lock (adquirir/release/obsolescencia), IDs con prefijos nuevos; los tests existentes de las 5 tablas se mantienen | **Medio**: `init_db` crea tablas nuevas sin tocar las existentes, pero **relajar NOT NULL en SQLite requiere migración** de la BD existente `job_search.db` — **el análisis NO especifica el procedimiento** (ver §6, punto 1) |
| `shared/errors.py` | Extender `BaseError` con campos opcionales `run_id`, `source_id`, `session_id`, `set_indice`; añadir `RE-SES` solo si se requiere | §3 (fila BaseError: "mantener + extender con campos de trazabilidad"); §6.1 | DOC-06 | Tests: `BaseError` conserva trazabilidad cuando se provee; jerarquía y severidad intactas | **Bajo** |
| `shared/retry.py` | Añadir `retry_conditional(codes)` / `should_retry(code)` para reintento por código | C6 ("en el módulo discovery no reusar `retry_decorator` directamente"); §6.1 | DOC-06 | Tests unitarios: `should_retry` true/false por código; no reintenta `bloqueo_plataforma`; reintenta `fuente_inalcanzable` hasta el límite | **Bajo** (`retry_decorator` intacto para otros módulos, §3) |
| `config/config.yaml` | Sustituir sección `search` (keywords → **primer set base**; límites → `captura` globales); agregar `fuentes` (ficha de acceso, sets, políticas), `almacen_credenciales` (referencias), `concurrencia` (umbral), `captura` (defaults globales RN-11); `browser` y `retries` como defaults globales (§3) | §6.1; §2 (fichas, sets, políticas); §3 (filas `search`, `browser`, `retries`) | D2, D4, DOC-01, DOC-09/9A | Tests de carga del YAML restructurado (config.py intacto, §6.2) | **Medio**: cualquier lector de `search.*` en código/tests de Fases 1-3 se rompe; el análisis solo identifica `shared/config.py` como inocuo — revisar consumidores |

**Tests transversales (§6.3):** `tests/conftest.py` — el fixture de BD debe inicializar las **tablas nuevas**; nuevos fixtures: `example_fuente`, `example_set`, `example_politicas`, etc. Mantener los existentes.

**Código SIN cambios (§6.2):** `shared/config.py`, `shared/state_machine.py` (M1 no usa estados), `shared/llm_service.py`, `shared/decision_engine.py`, `shared/logging_setup.py` (servirá de "registro crítico local" tal cual, §2).

---

## 4. PLAN DE CREACIÓN DE CÓDIGO NUEVO (§6.4 + tabla de elementos nuevos §2)

| Componente nuevo | Archivo/módulo | Responsabilidad única | Dependencias previas | Contrato de entrada/salida | Tests mínimos |
|---|---|---|---|---|---|
| Contexto de ejecución | `modules/discovery/run_context.py` | Objeto único transmitido entre nodos: config validada, lista filtrada, iteradores, bloqueo, conexiones y resultados por nodo (nace en INICIO) | DOC-04, DOC-12; `models.py`; `persistence.py`; config.yaml | In: config validada + fuentes → Out: contexto con iteradores (sets) y slots de resultados, consumido por los 13 nodos | Construcción con config válida/inválida (ERR-12); iteración de un set; referencia al bloqueo |
| Contratos entre nodos | `shared/models.py` → `EntryResult`, `SearchResult`, `CaptureBatch`, `EstadoCaptura`, `SetIndice` | Describir los resultados estructurados que fluyen entre nodos (§2 fila "entry_result...") | DOC-13/13A; DOC-04 | Entrada: datos de nodo A → Salida: objeto de contrato para el nodo B | Validación de campos de cada contrato |
| Ficha de acceso por fuente | `shared/models.py` → `FichaFuente/FuenteAcceso` + config `fuentes` | Esquema de acceso por fuente (público/autenticado, credencial, criterio de ingreso, timeout), validado en INICIO (ERR-12) | DOC-13 (entidad Source); D4 (credenciales) | Entrada: datos de acceso → Sale: ficha completa o descarte (ERR-12) | Ficha incompleta → descarte (ERR-12) |
| Corridas y generador de ID | Tabla `corridas` + prefijo `COR` (Ap 5A) | Instancia de ejecución única (RN-01 de INICIO); toda traza enlaza `run_id` | DOC-13; Ap 5A; `persistence.py` | Nuevo inicio → `run_id` único para la corrida | Generación única; formato del prefijo |
| Bloqueo de concurrencia persistente | Tabla `bloqueo` + ops en `persistence.py` | Una sola corrida activa; umbral de obsolescencia configurable (ERR-06/07/09) | DOC-13; D2; concurrencia config | Petición de bloqueo → adquirido (run_id) o rechazado; liberación/check con obsolescencia | Concurrencia: segundo intento rechazado; obsolescencia revoca |
| Almacén de sesiones y auditoría | Tabla `sesiones` + modelo `AuditoriaSesion` | Sesión de plataforma registrada solo en éxito; auditoría por `(session_id, set_indice)` | DOC-13; §7b (auditoría mínima) | Éxito de ingreso → registro `{session_id, run_id, source_id, set_indice, timestamp, total_declarado, conteo, estado}` | Campos de la auditoría mínima |
| Almacén de eventos "errores o sucesos" | Tabla `eventos` + modelo `EventoAlmacen` | Eventos críticos con `run_id` + tipología (adaptando entidad Event del 13A) | DOC-13A (entidad n.º 10); DOC-06 | Suceso → evento con `run_id` + tipología | Escritura en tabla; respaldo al registro crítico local (Loguru) |
| Almacén seguro de credenciales | `.env` (o almacén del sistema, según D4) + referencias en config | Accedido solo por "Entrar la fuente"; nunca en logs/BD | D4; DOC-01 | Fuente autenticada → referencia de credenciales | No se registra credencial; referencia válida |
| `set_de_filtros` y `politicas_de_captura` | `shared/models.py` (SetFiltros, PoliticasCaptura) + config | Iterador ordenado de sets por fuente (set vacío = búsqueda base); límites y pausas por fuente con defaults globales (RN-11) | DOC-01; DOC-09 (sets oficiales); D2 | Fuente → lista de sets + políticas (global o por fuente) | merge de defaults; iteración en orden |
| Grupo A / Grupo B de códigos | Enums en `shared/models.py` + clasificación en el nodo de decisión (Fase 4) | Política centralizada: qué códigos comprometen la fuente vs. propios del set | DOC-06 | Código de fallo → clasificación A/B | Clasificación de los códigos del catálogo |
| Adaptador de plataforma | `modules/discovery/adapters/linkedin.py` | Encapsula filtros, parsado y captura por fuente; mecanismo masivo/incremental (RN-10); "información original íntegra" (C2) | DOC-12 (INT-001/INT-003); DOC-09/9A | Entrada: ficha de acceso + credenciales + set + políticas → Salida: `entry_result`, `search_result`, `capture_batch`, `estado_captura`, `codigo_motivo` | Mock de página (HTML fixture): parseo, `id_externo_url` nullable (C2), bloqueo → `bloqueo_plataforma` |
| Reintento condicional | **en `shared/retry.py`** (añadir `retry_conditional`), consumido por el módulo discovery | Reintenta solo `fuente_inalcanzable`/`timeout_*` con backoff desde canal cerrado; nunca captcha/autenticación rechazada | DOC-06; ficha RN-03/RN-06 | Entrada: función + límites → Salida: resultado o `BaseError` no reintentable | `should_retry` por código; límites |

**Nota:** los **13 nodos** se implementan en la construcción misma de la Fase 4, nodo por nodo (plan existente, §7d "la construcción nodo por nodo del plan Fase 4 ya existe"). Esta sección cubre los componentes de infraestructura que la preparación debe dejar listos.

---

## 5. SECUENCIA DE EJECUCIÓN (todas las tareas, lineal)

**Tipo:** DOCUMENTO | CÓDIGO_EXISTENTE | CÓDIGO_NUEVO | DECISIÓN
**Prioridad:** ALTA (bloquea todo) | MEDIA (bloquea una fase) | BAJA (puede esperar)
**Esfuerzo:** P (< 1 hora) | M (1-4 horas) | G (> 4 horas)

| # | Tarea | Tipo | Prioridad | Depende de | Bloquea a | Esfuerzo |
|---|---|---|---|---|---|---|
| 1 | D1 — semántica de `activa` (atributo de catálogo) | DECISIÓN | ALTA | — | 5, 7, 13 | P |
| 2 | D2 — único SQLite, almacenes lógicos | DECISIÓN | ALTA | — | 5, 6, 15 | P |
| 3 | D3 — aprobar 6 puntos de "Finalizar Proceso" + reedición "Capturar v1.1" (alcance MVP §7b) | DECISIÓN | MEDIA | — | 5 (alcance sesión); nodos Capturar/Finalizar en la construcción | P |
| 4 | D4 — mecanismo de credenciales | DECISIÓN | MEDIA | — | 7, 9, 13 | P |
| 5 | DOC-13 + Documento 13A (entidades nuevas, Offer, Evento, constraint) | DOCUMENTO | ALTA | 1, 2, 3 | 6, 7, 8, 14, 15 | G |
| 6 | DOC-04 (flujo M1 por nodos, almacenes lógicos) | DOCUMENTO | ALTA | 5 | 9, 19 | M |
| 7 | DOC-06 (catálogo ERR-nn, mapeo ER-*, Grupo A/B, reintentos) | DOCUMENTO | ALTA | 5 | 10, 16, 17 | M |
| 8 | DOC-01 (RF del M1; C1 resuelto; estado `discovered`) | DOCUMENTO | ALTA | 5, 1, 4 | 10, 13, 14 | M |
| 9 | DOC-12 (submódulos, SRV-003/004/005, INT-001/003, almacén) | DOCUMENTO | MEDIA | 6, 8 | 10, 19, 20 | M |
| 10 | DOC-09 + Anexo 9A (LinkedIn: criterio de ingreso, sets, políticas, captcha) | DOCUMENTO | MEDIA | 9, 8 | 13, 20 | M |
| 11 | DOC-05 / Ap 5C (formatos de eventos; convención por nodo) | DOCUMENTO | BAJA | 7, 6 | 15 | P |
| 12 | DOC-00 Glosario + Ap 5A (prefijos COR/SES/EVT/BLO) | DOCUMENTO | MEDIA | 5 | 14 | P |
| 13 | config/config.yaml (fuentes, sets, políticas, concurrencia, almacén, captura) | CÓDIGO_EXISTENTE | ALTA | 1, 2, 4, 8, 10 | 15, 18 | M |
| 14 | `shared/models.py` (modelos nuevos, Offer, enums Grupo A/B) | CÓDIGO_EXISTENTE | ALTA | 5, 12 | 15, 18 | M |
| 15 | `shared/persistence.py` (tablas, `write_batch`, bloqueo, prefijos, C2) | CÓDIGO_EXISTENTE | ALTA | 5, 14, 12 | 18, 19 | M |
| 16 | `shared/errors.py` (campos opcionales de traza en BaseError) | CÓDIGO_EXISTENTE | ALTA | 7 | 17 | P |
| 17 | `shared/retry.py` (`retry_conditional` / `should_retry`) | CÓDIGO_EXISTENTE | MEDIA | 7 | 18 | P |
| 18 | `tests/conftest.py` (nuevas tablas en fixture + fixtures nuevos) | CÓDIGO_EXISTENTE | ALTA | 13, 14, 15, 16, 17 | 21 | M |
| 19 | `modules/discovery/` (scaffold + `run_context.py`) | CÓDIGO_NUEVO | MEDIA | 6, 9, 14, 15 | 21; nodo INICIO | M |
| 20 | `modules/discovery/adapters/linkedin.py` (INT-001/003) | CÓDIGO_NUEVO | MEDIA | 9, 10, 13, 14 | 21; nodos "Entrar"/"Filtros" | G |
| 21 | Validación "LISTO PARA CONSTRUIR FASE 4" (§6) + suite Ruff/mypy/pytest | VALIDACIÓN | ALTA | 1-20 | Construcción Fase 4 (nodo INICIO) | M |

> Los 13 nodos se implementan en la construcción de la Fase 4, nodo por nodo (plan existente, §7d de la recomendación); no se enumeran aquí.

---

## 6. CRITERIO "LISTO PARA CONSTRUIR FASE 4"

Para escribir la primera línea de código del nodo INICIO del Módulo 1, todo lo siguiente debe estar completado:

- [ ] Decisiones D1-D4 resueltas y formalizadas
- [ ] DOC-13/13A: entidades Corrida/Sesión/Bloqueo, Evento formalizado, Offer con trazabilidad; `activa` resuelto (D1)
- [ ] DOC-04: flujo M1 por los 13 nodos con `run_id` y almacenes lógicos (D2)
- [ ] DOC-06: catálogo ERR-01..12 + EVT-01; mapeo ERR-nn → ER-*; Grupo A/B; política de reintento por código
- [ ] DOC-01: RF del M1 (imprescindibles §7c) + nota `estado='discovered'` (C5)
- [ ] DOC-12, DOC-09/9A, DOC-00, Apéndice 5A, DOC-05/Ap 5C actualizados
- [ ] `config.yaml`: `fuentes` (ficha+sets+políticas), `captura`, `concurrencia`, `almacen_credenciales`; `search` desmontado; carga correcta
- [ ] `shared/models.py` + `shared/persistence.py`: modelos nuevos, Offer extendida, 4 tablas nuevas, `write_batch`, lock, esquema relajado (C2) con migración resuelta
- [ ] `shared/errors.py` (campos de traza) y `shared/retry.py` (`retry_conditional`)
- [ ] `tests/conftest.py` con 9 tablas + fixtures nuevos; **Ruff 0, mypy 0, pytest completo** (48 existentes + nuevos)
- [ ] `modules/discovery/` scaffoldeado con `run_context.py` y `adapters/` (INT-001/INT-003)

### Puntos donde el análisis no da información suficiente (decisión del usuario)

1. **Migración de BD** para relajar NOT NULL de `titulo`/`descripcion_original` (C2): el análisis no define el método (SQLite no permite DROP NOT NULL directamente).
2. **Mapeo completo de `codigo_motivo` → ER-***: el análisis solo da 2 ejemplos (`fuente_inalcanzable` → ER-RED/ER-EXT; `bloqueo_plataforma` → ER-NAV); el resto se decide al redactar DOC-06.
3. **Ubicación de `RunContext`**: §6.1 lo lista en `shared/models.py`; §6.4 y §2 lo ubican en `modules/discovery/run_context.py`. Pendiente de resolver en la implementación (tarea 19).
4. **Los 6 puntos de validación de "Finalizar Proceso"**: el análisis solo indica que son 6 (sin detallarlos).

---

## 7. RESULTADO ESPERADO

- Documentación oficial alineada con la ficha técnica (fuente única de verdad del M1).
- Infraestructura de código extendida: trazabilidad (`run_id`/`source_id`/`session_id`/`set_indice`), bloqueo, sesiones, eventos, reintentos condicionales.
- Suite verde sin regresiones (48 tests existentes + nuevos).
- Preparación terminada → inicio de la construcción nodo por nodo (nodo INICIO).