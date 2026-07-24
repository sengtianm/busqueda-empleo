# Informe de ejecución — Fase 2: Servicios compartidos (capa transversal)

> **Fecha:** 24/07/2026
> **Proyecto:** Automatización de búsqueda de empleo
> **Objetivo:** Implementar la capa de servicios compartidos (SRV-001, SRV-002, SRV-005, SRV-009 del DOC-12) y sus tests unitarios.

---

## 1. Objetivo ejecutado

Implementar los 3 servicios compartidos restantes (`ia_service`, `decision_engine`, `state_machine`), el modelo `Perfil`, sus tests unitarios y validación final, siguiendo el orden optimizado del plan de ejecución del MVP.

---

## 2. Actividades realizadas

| Orden | Tarea | Descripción |
|-------|-------|-------------|
| 1 | Modelo `Perfil` + sección en `config.yaml` | Añadida clase `Perfil(BaseModel)` con 11 campos a `shared/models.py`. Añadida sección `perfil` con valores por defecto en `config/config.yaml`. |
| 2 | `shared/ia_service.py` | Servicio IA multi-proveedor: `cargar_prompt()`, `renderizar_prompt()`, `_route_provider()`, `_enviar_local()` (Ollama), `_enviar_cloud()` (Ollama Cloud), `_validar_respuesta()`, `analizar(proposito)`. 4 códigos de error ER-LLM. |
| 3 | `shared/decision_engine.py` | Motor de reglas: `evaluar(oferta, perfil)`, 6 criterios ponderados con RapidFuzz, `cargar_perfil()` desde config, penalización por salario, exclusión automática de empresas. |
| 4 | `shared/state_machine.py` | Máquina de estados: mapa `TRANSICIONES_VALIDAS` con 6 transiciones, `transicionar()` con validación, `transiciones_posibles()`. Lanza `ErrorInterno` ER-INT-010 si es inválida. |
| 5 | Tests unitarios | 4 archivos creados: `test_ia_service.py` (10), `test_decision_engine.py` (11), `test_persistence.py` (6), `test_state_machine.py` (10) = **37 tests**. Añadida fixture `perfil_ejemplo` en `conftest.py`. |
| 6 | Validación final | `ruff check .` → 0 errors. `mypy .` → 0 errors. `pytest tests/ -v` → 37/37 passed. Todos los módulos importables OK. |

---

## 3. Archivos creados

| Archivo | Líneas aprox | Propósito |
|---------|-------------|-----------|
| `shared/ia_service.py` | ~190 | Comunicación multi-proveedor (Ollama local + Ollama Cloud), prompt loader, routing por propósito, validación de respuestas |
| `shared/decision_engine.py` | ~120 | Evaluación ponderada oferta vs perfil con 6 criterios |
| `shared/state_machine.py` | ~40 | Control de transiciones de estado del ciclo de vida |
| `tests/test_ia_service.py` | ~90 | 10 tests (mocks httpx, validación, errores ER-LLM) |
| `tests/test_decision_engine.py` | ~100 | 11 tests (puntuación, clasificación, exclusión) |
| `tests/test_persistence.py` | ~50 | 6 tests (CRUD con archivos temporales) |
| `tests/test_state_machine.py` | ~60 | 10 tests (6 válidas, 1 inválida, transiciones_posibles) |

---

## 4. Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `shared/models.py` | +14 líneas: clase `Perfil(BaseModel)` con 11 campos |
| `config/config.yaml` | +13 líneas: sección `perfil` con valores por defecto |
| `tests/conftest.py` | +17 líneas: fixture `perfil_ejemplo()` con datos de prueba típicos |
| `Plan de ejecución del MVP.md` | Fase 2 reescrita con especificación detallada de 6 tareas |
| `Seguimiento MVP.md` | Tabla de Fase 2 actualizada con estado ✅ |
| `Historial de sesiones.md` | Sesión 2 actualizada con actividades de la tarde/noche |

---

## 5. Detalle de implementación

### 5.1. Modelo `Perfil`

Clase Pydantic con 11 campos cargados desde `config.yaml`:

| Campo | Tipo | Propósito |
|-------|------|-----------|
| `tecnologias` | `dict[str, int]` | Tecnologías conocidas con nivel de dominio |
| `experiencia_anios` | `int` | Años de experiencia profesional |
| `idiomas` | `dict[str, str]` | Idiomas con nivel (ej. "C1") |
| `ubicaciones_preferidas` | `list[str]` | Ubicaciones donde buscar empleo |
| `modalidades_preferidas` | `list[str]` | Modalidades aceptadas (remoto, híbrido, etc.) |
| `salario_minimo` | `float \| None` | Salario mínimo aceptable |
| `seniority` | `str` | Nivel de seniority |
| `empresas_objetivo` | `list[str]` | Empresas de interés |
| `empresas_excluidas` | `list[str]` | Empresas a evitar (descarte automático) |
| `educacion_nivel` | `str` | Nivel educativo alcanzado |

### 5.2. `shared/ia_service.py`

Arquitectura del servicio multi-proveedor:

```
analizar(prompt_id, contexto, proposito="evaluacion")
  ├── cargar_prompt(prompt_id) → str
  │     └── Lee prompts/{categoria}/{prompt_id}.md
  │     └── ErrorConfiguracion si no existe
  ├── renderizar_prompt(template, contexto) → str
  │     └── Reemplaza {{ variable }} por valores
  ├── _route_provider(proposito) → "local" | "cloud"
  │     └── Routing desde config.yaml → ia_routing
  │     └── ErrorConfiguracion si proveedor inválido
  ├── _enviar_local(prompt) → str  [@decorador_reintento]
  │     └── httpx POST a http://{host}:{puerto}/api/generate
  │     └── ErrorLLM-001 (conexión), ER-LLM-002 (timeout), ER-LLM-003 (HTTP)
  ├── _enviar_cloud(prompt) → str  [@decorador_reintento]
  │     └── httpx POST a {endpoint}/api/generate con API Key
  │     └── ErrorLLM-001 (conexión), ER-LLM-002 (timeout), ER-LLM-003 (HTTP)
  └── _validar_respuesta(raw) → dict
        └── ErrorLLM-003 (no JSON), ER-LLM-004 (no dict)
```

### 5.3. `shared/decision_engine.py`

Criterios de evaluación con pesos desde `config.yaml`:

| Criterio | Peso | Algoritmo de matching |
|----------|------|----------------------|
| Experiencia | 0.30 | Comparación de años (`min(100, perfil / oferta * 100)`) |
| Tecnología | 0.25 | RapidFuzz `token_sort_ratio` promedio |
| Ubicación | 0.15 | RapidFuzz `partial_ratio` contra preferencias |
| Modalidad | 0.10 | Coincidencia exacta (case-insensitive) |
| Idiomas | 0.10 | Proporción de idiomas cubiertos |
| Seniority | 0.10 | Coincidencia por nivel (con tolerancia de 1 nivel) |

Reglas de negocio adicionales:
- Empresa en `empresas_excluidas` → **descarte automático** (puntaje = 0)
- Salario oferta < `salario_minimo` → **penalización** de hasta 30 puntos
- Clasificación: ≥80 → ALTA, ≥50 → MEDIA, <50 → BAJA
- Decisión: ALTA/MEDIA → CONTINUAR, BAJA → DESCARTAR

### 5.4. `shared/state_machine.py`

Transiciones válidas definidas:

```
DESCUBIERTA  → PREPARADA
PREPARADA    → EVALUADA
EVALUADA     → ACEPTADA | DESCARTA
ACEPTADA     → PROCESADA
DESCARTA     → FINALIZADA
PROCESADA    → FINALIZADA
```

Cualquier otra transición lanza `ErrorInterno` (ER-INT-010).

---

## 6. Validaciones ejecutadas

| Herramienta | Comando | Resultado |
|------------|---------|-----------|
| Ruff | `ruff check .` | 0 errores |
| MyPy | `mypy .` | 0 errores (16 archivos) |
| Pytest | `pytest tests/ -v` | 37/37 passed (12.53s) |
| Importabilidad | `python -c "import shared.ia_service, shared.decision_engine, shared.state_machine"` | OK |

---

## 7. Problemas encontrados y correcciones

| Problema | Archivo | Corrección |
|----------|---------|------------|
| `typing.Any` importado pero no usado | `shared/decision_engine.py` | Eliminado el import |
| 43 errores mypy por falta de `-> None` | 4 archivos de test | Añadidas anotaciones de tipo a todas las funciones |
| `type: ignore` no usado | `tests/test_decision_engine.py` | Reemplazados por `uuid4()` directo |
| Mock parameters sin tipo | `tests/test_ia_service.py` | Añadido tipo `MagicMock` a 4 parámetros |

---

## 8. Riesgos identificados

- `ia_service.py` soporta dos proveedores: Ollama local (para evaluación) y Ollama Cloud (para procesamiento). Los tests utilizan mocks de httpx para ambos.
- El proveedor cloud requiere conexión a Internet y una API Key de Ollama Cloud configurada en `.env`. Sin ella, el procesamiento profundo (Fase 7) no funcionará.
- El plan gratuito de Ollama Cloud tiene límites de uso que deben monitorizarse durante la Fase 7.
- Los pesos de evaluación en `config.yaml` (`evaluacion.pesos`) representan valores iniciales y pueden requerir ajuste fino durante la Fase 6 (Evaluación inicial) con ofertas reales.
- El prompt loader de `ia_service` lee del directorio `prompts/` que actualmente solo contiene `.gitkeep`. Los prompts se crearán en la Fase 3.
- El comando `git add` omitió incorrectamente `.opencode/commands/save.md` y `AGENTS.md` en commits anteriores; fueron incluidos en el commit final de esta fase.

---

## 9. Estado actual del proyecto

| Fase | Estado |
|------|--------|
| Fase 0 — Preparación de arranque | ✅ Completada |
| Fase 1 — Base común del sistema | ✅ Completada |
| **Fase 2 — Servicios compartidos** | **✅ Completada** |
| Fase 3 — Prompts iniciales | ⬜ Pendiente |
| Fase 4 — Módulo 1: Descubrimiento | ⬜ Pendiente |
| Fase 5 — Módulo 2: Preparación | ⬜ Pendiente |
| Fase 6 — Módulo 3: Evaluación inicial | ⬜ Pendiente |
| Fase 7 — Módulo 4: Procesamiento profundo | ⬜ Pendiente |
| Fase 8 — Módulo 5: Gestión de resultados | ⬜ Pendiente |
| Fase 9 — Integración del MVP | ⬜ Pendiente |

---

## 10. Commit y despliegue

| Aspecto | Detalle |
|---------|---------|
| Hash | `32b2723` |
| Mensaje | `feat: complete Fase 2 — shared services layer` |
| Archivos en commit | 15 (7 creados, 8 modificados) |
| Líneas agregadas | +1009 |
| Push | `main → origin/main` (GitHub) |

---

*Fin del informe*
