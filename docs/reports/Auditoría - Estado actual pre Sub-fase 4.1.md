# AUDITORÍA DEL ESTADO ACTUAL — Preparación Sub-fase 4.1 (nodo INICIO)

**Fecha:** 08/08/2026 · **Rama:** `main` · **Referencia:** `docs/reports/Plan de Preparación - Fase 4 Módulo 1.md`

---

## 1. Estructura de `modules/discovery/` ✅

| Ruta | Líneas | Contenido |
|---|---|---|
| `modules/discovery/__init__.py` | 6 | Solo docstring del módulo (sin clases) |
| `modules/discovery/.gitkeep` | 0 | Vacío (archivo de marcador) |
| `modules/discovery/run_context.py` | 226 | Clase `RunContext` (ver §2) |
| `modules/discovery/adapters/__init__.py` | 5 | Solo docstring: "Adapters implement the INT-001... and use the INT-003..." |
| `modules/discovery/adapters/linkedin.py` | 380 | `FlowError` (línea 66) + `LinkedInAdapter` (línea 75) (ver §9) |
| `modules/discovery/nodes/__init__.py` | 5 | **Placeholder** — "the thirteen nodes... are implemented node by node during the construction phase" |

⚠️ **Lo que NO existe:** el paquete `nodes/` está vacío (sin nodos). Los 13 nodos, incluido INICIO, NO están implementados — correcto para la preparación, pero confirma que la Sub-fase 4.1 parte de cero aquí.

## 2. Estado de `modules/discovery/run_context.py` ✅

Existe y está completo.

- **Clase:** `RunContext` (`run_context.py:33`)
- **Campos de `__init__`** (líneas 48-69): `run_id` (generado con `generate_id("corridas")`), `timestamp_inicio`, `fuentes_filtradas: list[FichaFuente]`, `_sets_validos`, `_politicas_por_fuente`, `iterador_fuentes`, `iterador_sets: dict[str, int]`, `bloqueo_adquirido`, `session_id`, `handle_sesion`, `entry_result`, `search_result`, `capture_batch`, `estado_captura`, `paginas_consumidas`, `capturadas_acumuladas_fuente`, `limite_alcanzado`
- **Métodos solicitados:**
  - `reset_iteradores()` — línea 208 ✅
  - `seleccionar_siguiente_set(source_id)` — línea 222 ✅
  - `sets_validos(fuente)` — línea 200 ✅
  - `politicas(fuente)` — línea 203 ✅
  - Extra: `set_filtros(fuente, indice)` — línea 191
- **Validaciones en `__init__`** (líneas 42-127): lista de fuentes no vacía (ERR-12); `ficha_acceso` obligatoria; `source_id`/`nombre`/`url` obligatorios; `criterio_exito` obligatorio; `tipo_acceso` ∈ {`publico`, `con_autenticacion`} (`_TIPOS_ACCESO`, línea 26); fuente autenticada exige `credenciales_referencia`

## 3. Estado de `shared/models.py` — modelos M1 ✅

| Modelo | Estado | Línea |
|---|---|---|
| Corrida | ✅ existe | 98 |
| EventoAlmacen | ✅ existe | 104 |
| AuditoriaSesion | ✅ existe | 117 |
| PoliticasCaptura | ✅ existe | 128 |
| FichaFuente | ✅ existe (como `FichaFuente`; **no hay clase `FichaAcceso`**) | 135 |
| SetFiltros | ✅ existe | 145 |
| EntryResult | ✅ existe | 151 |
| SearchResult | ✅ existe | 158 |
| CaptureBatch | ✅ existe | 169 |
| EstadoCaptura | ✅ existe | 178 |
| GrupoCodigo (enum) | ✅ existe (`grupo_a`/`grupo_b`) | 81 |
| TipoEvento (enum) | ✅ existe (`error`/`suceso`) | 86 |
| EstadoCorrida (enum) | ✅ existe | 91 |

- **Offer:** tiene los 4 campos opcionales de trazabilidad — `run_id: str | None` (75), `session_id: str | None` (76), `set_indice: int | None` (77), `id_externo_url: str | None` (78) ✅
- ⚠️ Discrepancia factual menor: el enum `EstadoCorrida` define 4 valores (`en_ejecucion`, `completada`, `error`, `concurrencia`), mientras que el 13A (§5.5.14, línea 2302) cataloga 5 (`en_ejecucion`, `corrida_completada`, `sin_fuentes`, `error`, `concurrencia`). No bloquea INICIO, pero existe diferencia de catálogo.

## 4. Estado de `shared/persistence.py` ✅

| Ítem | Estado | Línea |
|---|---|---|
| 4 tablas en `ESQUEMAS` | ✅ `corridas` (96), `eventos` (103), `sesiones` (117), `bloqueo` (129) |
| `write_batch` | ✅ línea 323 — transaccional con `rollback` explícito en excepción (345-347) |
| `acquire_lock` / `release_lock` / `check_lock` | ✅ líneas 357 / 387 / 396 (con umbral de obsolescencia, 352-354) |
| `PREFIXES` con COR/SES/EVT/BLO | ✅ líneas 16-19 |
| `_migrate_ofertas` (C2) | ✅ línea 209 — idempotente, reconstruye `ofertas` sin NOT NULL |
| `titulo` / `descripcion_original` nullable | ✅ sí — `titulo TEXT DEFAULT ''` (77), `descripcion_original TEXT DEFAULT ''` (78); NOT NULL solo en `url` (76) |
| `init_db` con 9 tablas | ✅ líneas 196-206 (lista en 199-200, incluye `_migrate_ofertas` en 203) |

⚠️ Detalle factual: `set_indice INTEGER DEFAULT ''` en el esquema de `ofertas` (línea 92) — mezcla de tipo SQL (`INTEGER`) con valor por defecto de texto. Funciona en SQLite, pero es incoherente tipográficamente con el 13A.

## 5. Estado de `shared/errors.py` ✅

- `BaseError` tiene los 4 campos opcionales: `run_id` (22), `source_id` (23), `session_id` (24), `set_indice` (25); reflejados en `__str__` (44-51) y `to_dict` (54-66)
- Jerarquía intacta (todas con prefijo de código): `NetworkError` ER-RED (69), `BrowserError` ER-NAV (74), `ExtractionError` ER-EXT (79), `ValidationError` ER-VAL (84), `LLMError` ER-LLM (89), `DataError` ER-DAT (94), `PersistenceError` ER-DB (99), `ConfigurationError` ER-CFG (104), `InternalError` ER-INT (109), `ExternalError` ER-EXTS (114)
- `RE-SES` NO fue añadido (el plan lo condicionaba a "solo si se requiere") — sin impacto

## 6. Estado de `shared/retry.py` ✅

| Ítem | Estado | Línea |
|---|---|---|
| `should_retry(codigo_motivo)` | ✅ | 62 (codes en 25-30: `fuente_inalcanzable`, `timeout_ingreso`, `timeout_consulta`, `timeout_captura`) |
| `retry_conditional` | ✅ | 66 — reintenta solo códigos retornados por `should_retry`; lee política de `retries` del config |
| `retry_decorator` original | ✅ intacto | 43-59 (usa `tenacity_retry` genérico, sin cambio) |

## 7. Estado de `config/config.yaml` ✅

| Sección | Estado | Líneas |
|---|---|---|
| `fuentes` (ficha_acceso, sets_de_filtros, politicas_de_captura) | ✅ | 2-26 (fuente `linkedin`) |
| `captura` (defaults globales) | ✅ | 29-33 |
| `concurrencia` (umbral_obsolescencia_minutos: 120) | ✅ | 36-37 |
| `almacen_credenciales` (`.env`, referencias) | ✅ | 40-45 |
| `search` | ✅ eliminada/reemplazada — **no existe ninguna clave `search`** |
| `browser` | ✅ intacta | 60-63 |
| `retries` | ✅ intacta | 95-99 |

## 8. Estado de `tests/conftest.py` ✅

- **Fixture de BD:** `temp_db_file` (44-52) llama a `init_db()` → inicializa las **9 tablas** ✅
- **Fixtures nuevos (nombres efectivos):** `example_ficha_fuente` (138) · `example_set_filtros` (151) · `example_politicas_captura` (164) · `example_run_context` (174) · `example_entry_result` (206) · `example_entry_result_fallo` (212) · `example_search_result` (220) · `example_capture_batch` (250)
- ⚠️ Nota de nomenclatura: el plan (§6.3) los llamaba `example_fuente`/`example_set`/`example_politias`; la implementación los nombró `example_ficha_fuente`/`example_set_filtros`/`example_politicas_captura` — equivalentes funcionales
- **Fixtures existentes operativos:** `example_source` (55), `example_company` (65), `example_location` (75), `example_offer` (80), `example_processed_offer` (97), `example_evaluation` (108), `example_profile` (122) + `clear_config_cache` autouse (27) y `tests_dir`/`fixtures_dir`

## 9. Estado de `modules/discovery/adapters/linkedin.py` ✅

- Existe (380 líneas). Clases: `FlowError` (66, portador de `codigo_motivo`) y `LinkedInAdapter` (75)
- Métodos públicos: `enter_source` (84), `apply_filters` (114), `capture_batch` (132), `close_session` (189)
- Métodos internos: `_autenticar` (198), `_criterio_ingreso_cumplido` (207), `_revisar_estado_pagina/captura/bloqueo_html` (212-227), `_parsear_resultados` (232), `_extraer_referencias` (266), `_hay_pagina_siguiente` (275), `_capturar_oferta` (279), `_declarar_evento` (311), `_pausa_entre_lotes` (322), `_construir_url_busqueda` (333), `_construir_pagina_siguiente` (354)
- **INT-001/INT-003 (DOC-12):** ✅ implementa — DOC-12 define INT-001 "Job search platform" (769) e INT-003 "Automated browser" (793) a nivel de propósito; el adaptador cumple el patrón (navegación sobre objeto `page` inyectado; métodos `enter_source`/`apply_filters`/`capture_batch`). Clasifica fallos con `codigo_motivo` oficial (DOC-06 §11) y declara eventos con tipología `EventoAlmacen` (311-320)

## 10. Estado de la documentación (criterios del Plan de Preparación)

| Doc | Criterio | Estado | Evidencia |
|---|---|---|---|
| Document 13A | Entidades Corrida/Sesión/Bloqueo/Evento formalizadas | ✅ | Inventario (24-26); Corrida §2.14 (1322-1379), Sesión §2.15 (1402), Bloqueo §2.16 (1466-1502), Evento (953); versión 1.3 (2516) |
| DOC-13 | Ídem | ⚠️ | Solo decisiones D1/D2/D3 en §13.8 (1276-1283); las entidades detalladas viven en el 13A, no en DOC-13 (documento de política) |
| DOC-04 | Flujo M1 con 13 nodos | ✅ | §15 (1787-1860): tabla de 13 nodos (1793-1822), contratos DFT-M1-002, almacenes DFT-M1-003, trazabilidad DFT-M1-004 |
| DOC-06 | Catálogo ERR-nn + mapeo ER-* + Grupo A/B + reintentos condicionales | ✅ | "Module 1: Error Catalog" (3308-3390): por nodo (3312), catálogo con mapeo + `Retry?` (3332), política condicional (3369), Grupo A/B (3379), estados de terminación (3390) |
| DOC-01 | RF del M1 + nota `estado='discovered'` | ✅ | §20 (1437): RF-M1-001..009 (1441-1477); nota C5 `estado='discovered'` (1481); nota D1 `activa` (1484-1487); set imprescindible §21 (1489-1505) |
| DOC-12 | CMP-001 desglosado en submódulos | ✅ | Estructura interna (280-298): `run_context.py`, 13 nodos, `adapters/`; SRV-003/004/005; INT-001 (769), INT-003 (793); almacén de credenciales (298) |
| DOC-09 + Anexo 9A | Criterio verificable de ingreso LinkedIn | ✅ | DOC-09 §6 (301-302: `global-nav` + `timeout_ingreso`); §6.4 captcha (337-346); 9A DE-LI-010 (295-320: criterio DOM verificable, prohibición de reintento tras captcha) |

Complementarios verificados: Apéndice 5A con prefijos COR/SES/EVT/BLO (128-131) ✅ · DOC-00 glosario con corrida/run_id/session_id/lote/set_indice/políticas/Grupo A-B/adaptador (362-427) ✅

## 11. Resultado de validaciones

| Comando | Resultado |
|---|---|
| `ruff check .` | 0 errores ("All checks passed!") |
| `mypy .` | 0 errores ("Success: no issues found in 27 source files") |
| `pytest tests/` | 102 passed / 0 failed / 0 errores (25.19s) |

⚠️ Dato: AGENTS.md declara "48 passing" — desactualizado (hoy son 102).

---

## Conclusión factual

**Listo para la Sub-fase 4.1 (nodo INICIO):** la infraestructura de preparación está completa y validada (Ruff 0, mypy 0, 102 tests). Todos los ítems del checklist §6 del Plan de Preparación están cumplidos salvo la construcción misma de los nodos (`modules/discovery/nodes/` está vacío). Únicas observaciones menores (no bloqueantes): diferencia de catálogo en `EstadoCorrida` vs 13A, `set_indice INTEGER DEFAULT ''` en el esquema, y nomenclatura de fixtures distinta a la del plan.