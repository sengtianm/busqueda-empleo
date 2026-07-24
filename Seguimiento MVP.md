# Seguimiento del MVP

> Estado actual de cada tarea del [Plan de ejecución del MVP](Plan%20de%20ejecución%20del%20MVP.md).

## Leyenda

| Símbolo | Significado |
|---------|-------------|
| ⬜ | Pendiente — no se ha iniciado |
| ⏳ | En progreso — se está trabajando |
| ✅ | Completado — pasó validación y se aprobó |
| ❌ | Bloqueado — algo impide avanzar |

---

## Fase 0. Preparación de arranque

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | Confirmar alcance del MVP (fuente única LinkedIn) | DOC-01, DOC-08, DOC-09 | ✅ | Sin contradicciones documentales. LinkedIn confirmada como única fuente del MVP (DOC-09 §3.10). |
| 2 | Definir reglas de trabajo con OpenCode | — | ✅ | 17 reglas documentadas en AGENTS.md (RT-001 a RT-017). |
| 3 | Establecer criterio de aceptación por paso | Plan ejecución | ✅ | 11 criterios documentados en AGENTS.md (CA-001 a CA-011). |
| 4 | Decidir estrategia de pruebas | Plan ejecución | ✅ | 8 secciones (EP-001 a EP-302) documentadas en AGENTS.md. |

---

## Fase 1. Base común del sistema (infraestructura)

| Orden | # | Tarea | Docs fuente | Estado | Obs |
|-------|---|-------|-------------|--------|-----|
| 1 | 1 | Estructura de directorios | DOC-07 | ✅ | 19 directorios + README.md creados. Documentación migrada a `docs/`. 17 `.gitkeep` añadidos. |
| 2 | 2a | Inicialización del control de versiones | — | ✅ | `git init`, `.gitignore`, commit inicial. Repo: `github.com/sengtianm/busqueda-empleo`. |
| 3 | 3 | venv + requirements.txt | DOC-11 | ✅ | Python 3.14.6 (3.12 no disponible). Stack completo. `playwright install chromium` ejecutado. |
| 4 | 4 | config.yaml + .env.template | DOC-05 | ✅ | config.yaml con secciones de navegación, evaluación, persistencia, IA, reintentos, logging, perfil. |
| 5 | 11 | pyproject.toml (Black, Ruff, mypy) | DOC-05, DOC-11 | ✅ | Black (100 chars, py312), Ruff (E/F/I/N/W), mypy (strict). |
| 6 | 5 | shared/config.py | DOC-05, DOC-11 | ✅ | Carga unificada YAML + .env con caché. |
| 7 | 7 | shared/errors.py (jerarquía ER) | DOC-06, Anexo 5A | ✅ | BaseError + 10 subclases (ER-RED, ER-NAV, ER-EXT, ER-VAL, ER-LLM, ER-DAT, ER-DB, ER-CFG, ER-INT, ER-EXTS). |
| 8 | 6 | shared/logging_setup.py | DOC-06 | ✅ | Loguru con stdout + rotación a archivo. |
| 9 | 8 | shared/retry.py (Tenacity) | DOC-06 | ✅ | decorador_reintento con políticas desde config + exponencial. |
| 10 | 10 | shared/models.py (Pydantic) | DOC-13 | ✅ | Oferta, Empresa, Fuente, Ubicacion, OfertaProcesada, Evaluacion, ResultadoProcesamiento. 3 Enums. |
| 11 | 9 | shared/persistence.py (xlsx) | DOC-13 | ✅ | leer_hoja, escribir_fila, buscar_por_id, actualizar. openpyxl, archivos temporales. |
| 12 | 12 | tests/conftest.py + tests/fixtures/ | — | ✅ | Fixtures: limpiar_cache_config, modelos_ejemplo, archivo_xlsx_temporal. |
| 13 | 13 | Validación final | — | ✅ | ruff → 0 errors. mypy → 0 errors. Todos los imports OK. pytest (0 tests, infra lista). |

---

## Fase 2. Servicios compartidos (capa transversal)

> **Orden optimizado:** Fase 3 puede comenzar tras completar la tarea 2 (`ia_service.py`).

| Orden | # | Tarea | Docs fuente | Estado | Obs |
|-------|---|-------|-------------|--------|-----|
| 1 | 1 | Modelo `Perfil` en `shared/models.py` + sección `perfil` en `config.yaml` | DOC-10, DOC-03 | ✅ | Se carga desde config.yaml como modelo de valor (no entidad persistente). |
| 2 | 2 | `shared/ia_service.py` (Ollama + prompt loader) | DOC-11, DOC-12 | ✅ | httpx + Ollama. Prompt loader desde `prompts/`. Reintentos con tenacity. 4 códigos de error ER-LLM. |
| 3 | 3 | `shared/decision_engine.py` (reglas + puntuación) | DOC-03, DOC-10 | ✅ | `evaluar(oferta, perfil)`. 6 criterios ponderados. RapidFuzz. Penalización por salario. Exclusión automática. |
| 4 | 4 | `shared/state_machine.py` (estados + transiciones) | DOC-03, DOC-04 | ✅ | 6 transiciones definidas en mapa inmutable. Lanza ER-INT-010 si es inválida. |
| 5 | 5 | Tests: ia_service, decision_engine, persistence, state_machine | — | ✅ | 37 tests (11 decision_engine, 10 ia_service, 6 persistence, 10 state_machine). Fixture `perfil_ejemplo`. |
| 6 | 6 | Validación: ruff → mypy → pytest | — | ✅ | ruff 0 errors, mypy 0 errors, 37/37 tests passed. Todos los módulos importables. |

---

## Fase 3. Prompts iniciales

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | prompts/evaluacion_inicial/ | DOC-03, DOC-12 | ✅ | Creado PRM-001 compatibilidad.md con estructura Anexo 5C. |
| 2 | prompts/procesamiento/ | DOC-12 | ✅ | Creados PRM-002 a PRM-005: diagnostico, extraccion_estrategica, diseno_candidatura, insumos. |
| 3 | Identificadores PRM-XXX + plantilla Anexo 5C | Anexo 5A, 5C | ✅ | Los 5 prompts siguen la plantilla oficial C.9 (Objetivo, Entradas, Variables, Instrucciones, Resultado, Observaciones, Versión). |
| 4 | Prueba manual con Ollama + oferta real | — | ⏳ | Pendiente de ejecución local. Los prompts se cargan y renderizan correctamente (verificado). Ollama requiere timeout >120s en este equipo. |
| 5 | Versión 1 aprobada | — | ⬜ | Pendiente de prueba manual y aprobación del Arquitecto. |

---

## Fase 4. Módulo 1 — Descubrimiento de oportunidades

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | Estructura modules/descubrimiento/ | DOC-07 | ⬜ | |
| 2 | Playwright: login/logout LinkedIn | DOC-09, Anexo 9A | ⬜ | |
| 3 | Playwright: búsqueda con filtros | DOC-09 | ⬜ | |
| 4 | Playwright: paginación de resultados | DOC-09 | ⬜ | |
| 5 | Parseo HTML → Oferta (BS4 + lxml) | DOC-13 | ⬜ | |
| 6 | Persistencia de ofertas descubiertas | DOC-04 | ⬜ | |
| 7 | Logs y manejo de errores (ER-NAV, ER-RED, ER-EXT) | DOC-06 | ⬜ | |
| 8 | Tests unitarios e integración | — | ⬜ | |
| 9 | Validación | — | ⬜ | |

---

## Fase 5. Módulo 2 — Preparación de ofertas

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | Estructura modules/preparacion/ | DOC-07 | ⬜ | |
| 2 | Carga de ofertas crudas desde persistencia | DOC-04 | ⬜ | |
| 3 | Limpieza de campos (espacios, HTML residual) | DOC-05 | ⬜ | |
| 4 | Normalización (fechas, salarios, ubicación, modalidad) | DOC-05, DOC-13 | ⬜ | |
| 5 | Validación de integridad y campos obligatorios | DOC-01 | ⬜ | |
| 6 | Detección de duplicados (RapidFuzz) | DOC-01 | ⬜ | |
| 7 | Asignación de estado inicial | DOC-03 | ⬜ | |
| 8 | Persistencia de versión preparada + log | DOC-04 | ⬜ | |
| 9 | Manejo de errores (ER-VAL, ER-DAT) | DOC-06 | ⬜ | |
| 10 | Tests | — | ⬜ | |
| 11 | Validación | — | ⬜ | |

---

## Fase 6. Módulo 3 — Evaluación inicial

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | Estructura modules/evaluacion/ | DOC-07 | ⬜ | |
| 2 | Carga de ofertas preparadas + perfil | DOC-04 | ⬜ | |
| 3 | Motor de reglas (decision_engine) | DOC-03 | ⬜ | |
| 4 | Invocación opcional a LLM | DOC-12 | ⬜ | |
| 5 | Clasificación (Alta / Media / Baja) | DOC-01 | ⬜ | |
| 6 | Decisión continuar/descartar + justificación | DOC-03 | ⬜ | |
| 7 | Persistencia de resultados + trazabilidad | DOC-04 | ⬜ | |
| 8 | Manejo de errores (ER-LLM, ER-DAT, ER-INT) | DOC-06 | ⬜ | |
| 9 | Tests | — | ⬜ | |
| 10 | Validación | — | ⬜ | |

---

## Fase 7. Módulo 4 — Procesamiento profundo

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | Estructura modules/procesamiento/ | DOC-07 | ⬜ | |
| 2 | Carga de ofertas aceptadas | DOC-04 | ⬜ | |
| 3 | LLM: diagnóstico de la vacante | DOC-01 | ⬜ | |
| 4 | LLM: extracción estratégica | DOC-01 | ⬜ | |
| 5 | LLM: diseño de candidatura | DOC-01 | ⬜ | |
| 6 | LLM: insumos (carta, preparación entrevista) | DOC-01 | ⬜ | |
| 7 | Validación de resultados (Pydantic) | DOC-13 | ⬜ | |
| 8 | Persistencia en data/salida/ | DOC-04 | ⬜ | |
| 9 | Manejo de errores (ER-LLM, ER-INT) | DOC-06 | ⬜ | |
| 10 | Tests | — | ⬜ | |
| 11 | Validación | — | ⬜ | |

---

## Fase 8. Módulo 5 — Gestión de resultados

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | Estructura modules/gestion/ | DOC-07 | ⬜ | |
| 2 | Historial por oferta + gestión de estados | DOC-01, DOC-03 | ⬜ | |
| 3 | Reporte resumen de ofertas | DOC-01 | ⬜ | |
| 4 | Exportación a .xlsx formateado | DOC-01 | ⬜ | |
| 5 | Validación de trazabilidad | DOC-04 | ⬜ | |
| 6 | Manejo de errores (ER-DB, ER-DAT) | DOC-06 | ⬜ | |
| 7 | Tests | — | ⬜ | |
| 8 | Validación | — | ⬜ | |

---

## Fase 9. Integración del MVP

| # | Tarea | Docs fuente | Estado | Obs |
|---|-------|-------------|--------|-----|
| 1 | scripts/run_mvp.py (orquestador) | DOC-12 | ⬜ | |
| 2 | Prueba E2E con ofertas reales pequeñas | DOC-01 | ⬜ | |
| 3 | Verificación: logs, errores, persistencia | — | ⬜ | |
| 4 | Corrección de dependencias y secuencia | — | ⬜ | |
| 5 | Regresión: lint → typecheck → pytest | — | ⬜ | |
| 6 | Revisión de cobertura vs DOC-01 | — | ⬜ | |
| 7 | Aprobación final del MVP | — | ⬜ | |
