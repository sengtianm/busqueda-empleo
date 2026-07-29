# Historial de sesiones

> Registro cronológico de sesiones de trabajo con OpenCode.

---

## Sesión 1 — 23/07/2026

**Temas tratados:**
- Creación del plan de ejecución del MVP en 9 fases
- Creación de Seguimiento MVP.md y sistema de persistencia de sesiones (comandos /save y /retomar)
- Confirmación de alcance del MVP (LinkedIn como única fuente)
- Definición de 17 reglas de trabajo (RT-001 a RT-017), 11 criterios de aceptación (CA-001 a CA-011) y estrategia oficial de pruebas (EP-001 a EP-302)
- Creación de estructura de directorios según DOC-07 y migración de documentación a docs/
- Inicialización de control de versiones (git init, .gitignore, commit inicial, GitHub)
- Ejecución completa de Fase 1 Tasks 3 a 13: venv, requirements.txt, config.yaml, .env.template, pyproject.toml, shared/* (6 módulos), tests/*, validación final
- Reordenamiento del plan Fase 1 con dependencias correctas
- Depuración de bugs de lint/typecheck (N818, ErrorBase, tenacity)
- Commit y push a GitHub del trabajo completado

**Decisiones:**
- Aprobado plan de 9 fases
- LinkedIn confirmada como única fuente del MVP (DOC-09 §3.10)
- 17 reglas RT, 11 criterios CA, estrategia EP documentados en AGENTS.md
- Se añadió tarea 1.2a (control de versiones) al plan
- Repositorio remoto: sengtianm/automatizaci-n-busqueda-empleo
- N818 ignorado por convención de nombres en español
- ErrorBase renombrado a BaseError; tenacity.before_sleep_log con logging.getLogger
- Historial de sesiones.md excluido de git
- Reglas de sesión (RT-018 a RT-021) incorporadas: una sesión por día, guardado automático en modo build, formato DD/MM/YYYY, detalle completo y acumulativo

**Acuerdos:**
- No iniciar implementación del MVP sin orden explícita
- Las reglas RT-001 a RT-021 rigen el desarrollo del MVP
- Al finalizar modo build, actualizar automáticamente Historial de sesiones.md
- Una sesión por día calendario con formato DD/MM/YYYY

**Estado al cierre:**
- Fase 0 completada (✅) — Preparación de arranque finalizada
- Fase 1 completamente terminada (✅) — 11 tareas ejecutadas y validadas
- 13 archivos creados (~645 líneas de código/config)
- Validaciones: ruff 0 errors, mypy 0 errors, imports OK
- Pendiente de aprobación del Arquitecto para iniciar Fase 2

---

## Sesión 2 — 24/07/2026

**Temas tratados:**

*Revisión y reglas de sesión (mañana):*
- Revisión de reglas de guardado del historial de sesiones
- Identificación de que el guardado en Historial de sesiones.md no estaba cubierto por las reglas formales (RT, CA, EP)
- Propuesta y aprobación de reglas de sesión (RT-018, RT-019, RT-020, RT-021)
- Actualización de AGENTS.md con las 4 nuevas reglas
- Actualización de .opencode/commands/save.md para reflejar las nuevas reglas
- Consolidación del Historial de sesiones.md (5 sesiones del 23/07/2026 fusionadas en una sola Sesión 1)
- Aplicación del formato DD/MM/YYYY en todas las fechas del historial
- Solicitud del usuario de añadir RT-021 para garantizar detalle completo

*Planificación de Fase 2 (tarde):*
- Revisión de integridad de Fase 1 y detección de gap: faltaba el modelo `Perfil` para `decision_engine` — no existe como entidad en DOC-13/13A
- Análisis de coherencia entre Fases 1, 2 y 3 del plan de ejecución
- Elaboración de plan detallado de Fase 2 con orden optimizado (6 tareas) para desbloquear Fase 3 inmediatamente tras `ia_service.py`
- Recomendación y aprobación del modelo `Perfil` como modelo de valor Pydantic cargado desde nueva sección `perfil` en `config.yaml`
- Actualización de `Plan de ejecución del MVP.md` con Fase 2 reescrita
- Actualización de `Seguimiento MVP.md` con nueva estructura de tareas de Fase 2

*Ejecución de Fase 2 (noche):*
- Ejecución completa de las 6 tareas de Fase 2:
  - Tarea 1: Modelo `Perfil` en `shared/models.py` + sección `perfil` en `config/config.yaml`
  - Tarea 2: `shared/ia_service.py` — comunicación Ollama vía httpx, prompt loader, renderizado `{{ variables }}`, reintentos Tenacity, 4 códigos ER-LLM
  - Tarea 3: `shared/decision_engine.py` — 6 criterios ponderados, RapidFuzz, penalización salarial, exclusión automática
  - Tarea 4: `shared/state_machine.py` — mapa inmutable de 6 transiciones, ER-INT-010 para transiciones inválidas
  - Tarea 5: 37 tests (11 decision_engine, 10 ia_service, 6 persistence, 10 state_machine) + fixture `perfil_ejemplo`
  - Tarea 6: Validación — ruff 0, mypy 0, pytest 37/37
- Commit `32b2723` y push a GitHub
- Creación de `Informe - Ejecución Fase 2.md`

*Mejora de robustez (noche — continuación):*
- Validación de pesos en `decision_engine.py`: incorporada validación fail-fast con `math.isclose` que lanza `ErrorConfiguracion` (ER-CFG-002) si la suma de pesos no es 1.0
- 2 tests nuevos (pesos válidos, pesos inválidos con verificación de mensaje)
- Commit `3d9e8c7`
- Análisis de coherencia entre Fase 2 → Fase 3 y Fase 3 → Fase 4
- Se detectó que Fase 3 necesitaba alinear sus tareas con la plantilla oficial del Anexo 5C §C.9
- Actualización del `Plan de ejecución del MVP.md` con tareas detalladas

*Ejecución de Fase 3 (sesión extendida):*
- Tarea 1: Creado `prompts/evaluacion_inicial/compatibilidad.md` (PRM-001) — análisis cualitativo oferta-perfil con campos compatibilidad, justificacion, factores_clave, brechas, compatibilidad_cultural
- Tarea 2: Creados 4 prompts en `prompts/procesamiento/`: diagnostico (PRM-002), extraccion_estrategica (PRM-003), diseno_candidatura (PRM-004), insumos (PRM-005)
- Tarea 3: Los 5 prompts siguen la plantilla oficial Anexo 5C §C.9 con las 8 secciones (Objetivo, Entradas, Variables, Instrucciones, Resultado esperado, Observaciones, Versión)
- Tarea 4: Prueba manual con Ollama no completada — los modelos qwen3.5 requieren timeout >120s en este equipo debido al proceso interno de "thinking". Se verificó que los prompts se cargan y renderizan correctamente.
- Tarea 5: Versión v1 creada, pendiente de prueba manual y aprobación
- Validaciones: ruff 0, mypy 0, pytest 39/39
- Commit `7db5e3f`
- Creación de `Informe - Ejecución Fase 3.md`

**Decisiones:**

- RT-018 a RT-021: una sesión por día calendario, guardado automático en modo build, formato DD/MM/YYYY, detalle completo y prohibición de eliminar/resumir sesiones pasadas
- Modelo `Perfil` como modelo de valor Pydantic en `shared/models.py`, cargado desde `config.yaml` — no es entidad persistente
- Fase 2 reorganizada en 6 tareas con orden optimizado (Fase 3 puede comenzar tras `ia_service.py`)
- RapidFuzz para matching difuso en tecnología y ubicación del motor de decisiones
- Se aprueba incorporar validación de suma de pesos en `decision_engine.py` como mejora de robustez (código ER-CFG-002, alineado con DOC-06)
- Los prompts de Fase 3 se entregan como versión v1, pendientes de prueba manual con Ollama
- La prueba manual de Fase 3 se difiere a una sesión local del usuario por limitaciones de tiempo de respuesta de Ollama en este entorno
- Fase 4 no está bloqueada por la prueba manual pendiente de Fase 3

**Acuerdos:**

- Se mantienen los acuerdos de sesiones anteriores
- No iniciar implementación del MVP sin orden explícita
- Las reglas RT-001 a RT-021 rigen el desarrollo del MVP

**Estado al cierre:**

- Fase 0 y Fase 1: completamente terminadas (✅)
- Fase 2: completamente terminada (✅) — 6 tareas ejecutadas, commit `32b2723`
- Fase 3: completada parcialmente — tareas 1-3 ejecutadas (✅), tarea 4 pendiente de prueba local (⏳), tarea 5 pendiente de aprobación (⬜)
- Validación general: ruff 0, mypy 0, pytest 39/39
- Commits del día: `32b2723` (Fase 2), `3d9e8c7` (validación pesos), `7db5e3f` (Fase 3), `f2d0063` (historial)
- Pendiente de aprobación del Arquitecto para iniciar Fase 4

---

## Sesión 4 — 29/07/2026

**Temas tratados:**

*Rollback de Fase 4:*
- Decisión de rehacer Fase 4 desde cero
- Reset destructivo del repositorio al commit `4fc1852` (fin de Fase 3, Sesión 2)
- Eliminación de rama `experiment/scroll-inventario`
- Force push a GitHub
- Limpieza de `data/automatizacion.db`, `data/perfil_chrome/`, `__pycache__/`
- Proyecto restaurado al estado post-Fase 3: Fases 0-3 completas, Fase 4 limpia

**Decisiones:**
- Se descarta todo el código de la implementación anterior de Fase 4 (módulo descubrimiento, migración SQLite)
- La persistencia vuelve a openpyxl/Excel (la original de Fase 1)
- `shared/persistence.py` en su versión Excel (pre-SQLite)

**Acuerdos:**
- Se mantienen los acuerdos de sesiones anteriores
- Fase 4 se reimplementará desde cero

**Estado al cierre:**
- Fases 0, 1, 2, 3: completamente terminadas (✅)
- Fase 4: completamente reiniciada (⬜) — lista para reimplementar
- HEAD en `4fc1852`
- Validaciones pendientes de ejecutar tras el reset

---

## Sesión 5 — 29/07/2026

**Temas tratados:**

*Migración de persistencia (pre-Fase 4):*
- Decisión de migrar de Excel/openpyxl a SQLite antes de iniciar Fase 4
- Aprobación del plan de migración: 7 tablas normalizadas + secuencia_ids
- IDs secuenciales con prefijo personalizado (EMP-0001, OFE-0001, etc.)
- Uso de DB Browser for SQLite como herramienta auxiliar

*Implementación:*
- `shared/models.py`: todos los `id: UUID` → `id: str`, añadidos `fecha_creacion` y `fecha_actualizacion` a todos los modelos Pydantic
- `config/config.yaml`: sección `persistencia` simplificada a `archivo_bd: data/busqueda_empleo.db`
- `shared/persistence.py`: implementación completa con SQLite — 8 tablas (secuencia_ids + fuentes + empresas + ubicaciones + ofertas + ofertas_procesadas + evaluaciones + resultados_procesamiento), funciones `generar_id`, `inicializar_bd`, `leer_tabla`, `escribir_fila`, `buscar_por_id`, `actualizar`, serialización/deserialización de tipos complejos (bool, list, dict, datetime)
- `tests/conftest.py`: `archivo_bd_temporal` con fixture generador que crea/limpia base en `tmp_path`
- `tests/test_persistence.py`: 10 tests para SQLite (secuencias, CRUD, JSON, ID explícito)
- `tests/test_decision_engine.py`: `uuid4()` → strings tipo `"OFP-T1"`
- `requirements.txt`: eliminada dependencia `openpyxl`

*Documentación actualizada:*
- `docs/DOC-11 - Stack tecnológico.md`: capítulo 10 reescrito (SQLite), sección 6.4 (uuid→sqlite3)
- `docs/anexos/DOC-Anexo 5A - Catálogo oficial de prefijos.md`: sección A.9b con prefijos FNT, EMP, UBI, OFE, OFP, EVL, RSP
- `AGENTS.md`: stack actualizado, EP-104 actualizado (Excel→SQLite)
- `README.md`: stack actualizado
- `Plan de ejecución del MVP.md`: referencias a openpyxl→SQLite
- `Seguimiento MVP.md`: tarea de migración añadida como pre-Fase 4

**Decisiones:**
- SQLite reemplaza a openpyxl/Excel como capa de persistencia
- IDs con formato `{PREFIJO}-{NUM:04d}` mediante tabla `secuencia_ids` con ON CONFLICT
- Fechas almacenadas en ISO 8601 (`YYYY-MM-DD HH:mm:ss`) en SQLite
- DB Browser for SQLite como herramienta auxiliar de consulta/edición
- Todo en rama `modulo-1`; sin merge a main sin orden explícita
- 7 tablas normalizadas para los dominios del modelo Pydantic

**Acuerdos:**
- Se mantienen los acuerdos de sesiones anteriores
- La migración a SQLite queda como prerrequisito completado antes de Fase 4
- La rama `modulo-1` contendrá este cambio; se mergeará a main cuando el Arquitecto lo apruebe

**Estado al cierre:**
- Pre-migración: completada (✅) — SQLite implementado, IDs secuenciales, tests pasando
- Fases 0, 1, 2, 3: completamente terminadas (✅)
- Fase 4: pendiente (⬜) — módulo descubrimiento listo para implementar sobre SQLite
- Validaciones: ruff 0, mypy 0, pytest 47/47
- Rama activa: `modulo-1`
