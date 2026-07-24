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

**Temas tratados (mañana):**
- Revisión de reglas de guardado del historial de sesiones
- Identificación de que el guardado en Historial de sesiones.md no estaba cubierto por las reglas formales (RT, CA, EP)
- Propuesta y aprobación de reglas de sesión (RT-018, RT-019, RT-020, RT-021)
- Actualización de AGENTS.md con las 4 nuevas reglas
- Actualización de .opencode/commands/save.md para reflejar las nuevas reglas
- Consolidación del Historial de sesiones.md (5 sesiones del 23/07/2026 fusionadas en una sola Sesión 1)
- Aplicación del formato DD/MM/YYYY en todas las fechas del historial
- Solicitud del usuario de añadir RT-021 para garantizar detalle completo en todas las entradas del historial y prohibir eliminación de información de sesiones pasadas

**Temas tratados (tarde):**
- Revisión de integridad de Fase 1 y detección de gap: faltaba el modelo `Perfil` para el motor de decisiones (`decision_engine`) — no existe como entidad en DOC-13/13A
- Análisis de coherencia entre Fases 1, 2 y 3 del plan de ejecución del MVP
- Elaboración de plan detallado de Fase 2 con orden optimizado (6 tareas) para desbloquear Fase 3 inmediatamente tras completar `ia_service.py`
- Recomendación y aprobación del enfoque para el modelo `Perfil`: modelo de valor Pydantic cargado desde nueva sección `perfil` en `config.yaml`
- Actualización de `Plan de ejecución del MVP.md` con la Fase 2 reescrita en detalle
- Actualización de `Seguimiento MVP.md` con la nueva estructura de tareas de Fase 2

**Temas tratados (noche — ejecución Fase 2):**
- Ejecución completa de las 6 tareas de Fase 2 en orden:
  - Tarea 1: Añadido modelo `Perfil` a `shared/models.py` y sección `perfil` a `config/config.yaml`
  - Tarea 2: Creado `shared/ia_service.py` con comunicación Ollama vía httpx, prompt loader, renderizado `{{ variables }}`, reintentos con tenacity, 4 códigos de error ER-LLM (conexión, timeout, respuesta inválida, formato inesperado)
  - Tarea 3: Creado `shared/decision_engine.py` con 6 criterios ponderados (experiencia 0.30, tecnología 0.25, ubicación 0.15, modalidad 0.10, idiomas 0.10, seniority 0.10), RapidFuzz para matching difuso, penalización por salario mínimo no cubierto, descarte automático por empresas excluidas, método `cargar_perfil()` desde config
  - Tarea 4: Creado `shared/state_machine.py` con mapa inmutable de 6 transiciones válidas, método `transicionar()` que lanza ER-INT-010 si la transición es inválida
  - Tarea 5: Creados 4 tests (11 de decision_engine, 10 de ia_service, 6 de persistence, 10 de state_machine) + fixture `perfil_ejemplo` en conftest.py — total 37 tests
  - Tarea 6: Validación final — ruff 0 errors, mypy 0 errors, pytest 37/37 passed, todos los módulos importables
- Commit y push a GitHub del trabajo de Fase 2 (commit `32b2723`)
- Creación de `Informe - Ejecución Fase 2.md` con el reporte detallado de la fase

**Decisiones:**
- RT-018: una sesión por día calendario
- RT-019: guardado automático de sesión al finalizar tarea en modo build
- RT-020: formato de fecha DD/MM/YYYY en el historial
- RT-021: todas las entradas deben ser detalladas; no se puede eliminar ni resumir información de sesiones pasadas
- Reglas documentadas en AGENTS.md + save.md (aprobación del usuario)
- Modelo `Perfil` se implementa como modelo Pydantic en `shared/models.py` y sus datos se cargan desde una nueva sección `perfil` en `config.yaml` — no se trata como entidad persistente, sino como modelo de valor, coherente con DOC-13/13A que no lo define como entidad
- Fase 2 se reorganiza en 6 tareas con orden optimizado: (1) Perfil + config, (2) ia_service, (3) decision_engine, (4) state_machine, (5) tests, (6) validación
- Fase 3 puede comenzar tras completar la tarea 2 (`ia_service.py`), sin esperar a `decision_engine` ni `state_machine`
- Uso de RapidFuzz para matching difuso en tecnología y ubicación dentro del motor de decisiones

**Acuerdos:**
- Se mantienen los acuerdos de sesiones anteriores

**Estado al cierre:**
- Fase 2 completada: 6 tareas ejecutadas, commit `32b2723` pusheado a GitHub
- Creado `Informe - Ejecución Fase 2.md` con reporte detallado de la fase
- Pendiente de aprobación del Arquitecto para iniciar Fase 3

**Temas tratados (noche — continuación):**
- Validación de pesos en decision_engine: incorporada validación fail-fast con `math.isclose` que lanza `ErrorConfiguracion` si la suma de pesos no es 1.0. Código ER-CFG-002 alineado con DOC-06. 2 tests nuevos (pesos válidos e inválidos). 39/39 tests.
- Commit `3d9e8c7`
- Análisis de coherencia entre Fase 2 → Fase 3 y Fase 3 → Fase 4. Se detectó que Fase 3 necesitaba alinear sus tareas con la plantilla oficial del Anexo 5C §C.9. Se actualizó el Plan de ejecución.

**Temas tratados (día 2 — ejecución Fase 3):**
- Ejecución de Fase 3 completa:
  - Tarea 1: Creado `prompts/evaluacion_inicial/compatibilidad.md` (PRM-001) para análisis cualitativo oferta-perfil
  - Tarea 2: Creados 4 prompts en `prompts/procesamiento/`: diagnostico (PRM-002), extraccion_estrategica (PRM-003), diseno_candidatura (PRM-004), insumos (PRM-005)
  - Tarea 3: Los 5 prompts siguen la plantilla oficial Anexo 5C §C.9 (Objetivo, Entradas, Variables, Instrucciones, Resultado esperado, Observaciones, Versión)
  - Tarea 4: Prueba manual con Ollama no completada — los modelos qwen3.5 requieren timeout >120s en este equipo. Se documentó como pendiente.
  - Tarea 5: Versión v1 creada, pendiente de prueba manual y aprobación
- Validaciones: ruff 0, mypy 0, pytest 39/39
- Commit `7db5e3f`

**Decisiones adicionales:**
- Se aprueba incorporar validación de suma de pesos en decision_engine como mejora de robustez
- Los prompts de Fase 3 se entregan como versión v1, pendientes de prueba manual con Ollama
- La prueba manual se difiere a una sesión local del usuario debido a limitaciones de tiempo de respuesta de Ollama en este entorno

**Estado al cierre:**
- Fase 3 completada parcialmente (tareas 1-3 ✅, tarea 4 ⏳ pendiente de prueba local, tarea 5 ⬜ pendiente de aprobación)
- Fase 4 puede comenzar sin depender de la prueba manual de Fase 3
- Commit `7db5e3f` en GitHub
