# Plan de ejecución del MVP — Automatización de búsqueda de empleo

> **Documento de trabajo.** Define el orden exacto de construcción del MVP, paso a paso, basado en los documentos aprobados (DOC-00 a DOC-13, Anexos 5A, 5B, 5C, 9A).

---

## Fase 0. Preparación de arranque

1. Confirmar alcance del MVP contra DOC-01, DOC-08, DOC-09 (LinkedIn como única fuente).
2. Definir reglas de trabajo con OpenCode: una tarea a la vez, sin avanzar sin aprobación.
3. Establecer criterio de aceptación por paso: código escrito, pasa lint+typecheck+pruebas, se revisa y se aprueba.
4. Decidir estrategia de pruebas:
   - **Unitarias (pytest):** lógica de negocio, reglas, transformaciones. Fixtures en `tests/fixtures/`.
   - **Integración con LinkedIn real:** Playwright + selectores reales (etiquetadas `integration`).
   - **LLM:** prompts probados con Ollama local, respuestas mockeables en unitarias.
   - **Data layer:** tests con archivos .db temporales (SQLite).

---

## Fase 1. Base común del sistema (infraestructura)

#### Ya completadas

1. **Estructura de directorios** según DOC-07 (raíz completa con `docs/`, `config/`, `modules/`, `shared/`, `data/`, `logs/`, `temp/`, `scripts/`, `tests/`, `prompts/`). Incluye migración de `Documentación Inicial/` a `docs/` y creación de `.gitkeep` en directorios vacíos.

2. **Fase 1.2a — Inicialización del control de versiones:**
   - `git init` en la raíz del proyecto.
   - Crear `.gitignore` acorde al stack del proyecto.
   - Verificar que los `.gitkeep` preservan los directorios vacíos.
   - Primer commit con estructura base y documentación migrada.
   - Crear repositorio remoto en GitHub y publicar.

#### Pendientes (orden de ejecución)

3. **venv + requirements.txt** — Inicializar `venv`, crear `requirements.txt` con todo el stack (DOC-11), instalar dependencias y ejecutar `playwright install chromium`. Validar: venv correcto, pip del venv, todos los paquetes instalados, playwright install sin errores.

4. **config.yaml + .env.template** — Crear `config/config.yaml` con parámetros funcionales + `config/.env.template`.

5. **pyproject.toml** — Configurar Black, Ruff, mypy para el proyecto.

6. **shared/config.py** — Implementar carga unificada de config.yaml + .env.

7. **shared/errors.py** — Jerarquía de excepciones por categoría (ER-RED, ER-NAV, ER-LLM, etc., DOC-06). Atributos: código, severidad (SV-1 a SV-5), módulo_origen, oferta_id, timestamp.

8. **shared/logging_setup.py** — Loguru con formato estándar, rotación y directorio `logs/`.

9. **shared/retry.py** — Wrapper con Tenacity, políticas según DOC-06.

10. **shared/models.py** — Modelos Pydantic v2: `Oferta`, `Evaluacion`, `Resultado`, `Empresa`, etc. (DOC-13). IDs como string secuencial, campos `fecha_creacion`/`fecha_actualizacion` en ISO 8601.

11. **shared/persistence.py** — Acceso a SQLite via sqlite3. Métodos: leer, escribir, actualizar, buscar por ID, generar IDs secuenciales. Path desde config.

12. **tests/conftest.py + tests/fixtures/** — Fixtures básicos (config de prueba, logger mock, persistence temp) y directorio `tests/fixtures/` con `.gitkeep`.

13. **Validación final:**
    - `ruff check .` sin errores.
    - `mypy .` sin errores.
    - `python -c "import shared.config, shared.errors, shared.logging_setup, shared.retry, shared.models, shared.persistence"` — todos los módulos importables sin error.
    - `pytest tests/` — todas las pruebas pasan.

---

## Fase 2. Servicios compartidos (capa transversal)

### Orden de ejecución optimizado

> La Fase 3 (prompts) puede comenzar inmediatamente después de completar la **Tarea 2** (`ia_service.py`). Las tareas restantes (3, 4, 5, 6) no bloquean Fase 3.

| Orden | Tarea | Depende de | ¿Bloquea Fase 3? |
|-------|-------|------------|------------------|
| 1 | Añadir modelo `Perfil` a `shared/models.py` + sección `perfil` en `config.yaml` | Nada | No |
| 2 | `shared/ia_service.py` (Ollama + prompt loader) | Tarea 1 (débil) | **Sí** |
| 3 | `shared/decision_engine.py` (reglas + puntuación) | Tarea 1 (fuerte) | No |
| 4 | `shared/state_machine.py` (estados + transiciones) | Nada (independiente) | No |
| 5 | Tests unitarios (ia_service, decision_engine, persistence, state_machine) | Tareas 2-4 | No |
| 6 | Validación final (ruff → mypy → pytest) | Tarea 5 | No |

---

#### Tarea 1 — Modelo `Perfil` + sección en config

**Archivos:** modificar `shared/models.py` y `config/config.yaml`.

**Objetivo:** Crear el modelo Pydantic `Perfil` que representa el perfil profesional del usuario, necesario para que el motor de decisiones evalúe ofertas contra el perfil. Sus valores se cargan desde una nueva sección `perfil` en `config.yaml`.

**Modelo `Perfil`** (añadir en `shared/models.py`):

```python
class Perfil(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    tecnologias: dict[str, int] = Field(default_factory=dict)
    experiencia_anios: int = 0
    idiomas: dict[str, str] = Field(default_factory=dict)
    ubicaciones_preferidas: list[str] = Field(default_factory=list)
    modalidades_preferidas: list[str] = Field(default_factory=list)
    salario_minimo: float | None = None
    seniority: str = ""
    empresas_objetivo: list[str] = Field(default_factory=list)
    empresas_excluidas: list[str] = Field(default_factory=list)
    educacion_nivel: str = ""
```

**Sección `perfil`** (añadir en `config/config.yaml`):

```yaml
perfil:
  tecnologias: {}
  experiencia_anios: 0
  seniority: ""
  idiomas: {}
  ubicaciones_preferidas: []
  modalidades_preferidas: []
  salario_minimo: null
  empresas_objetivo: []
  empresas_excluidas: []
  educacion_nivel: ""
```

**Fundamento:** Basado en DOC-10 (tecnologías, experiencia, idiomas, preferencias laborales) y los criterios CE-001 a CE-012 de DOC-03. El `Perfil` es un modelo de valor (no entidad persistente), coherente con DOC-13/13A que no lo define como entidad.

---

#### Tarea 2 — `shared/ia_service.py`

**Archivo a crear:** `shared/ia_service.py`

**Objetivo:** Implementar el servicio de IA con soporte multi-proveedor (SRV-002 según DOC-12), capaz de enrutar solicitudes al modelo local o cloud según el propósito.

**Componentes:**

| Componente | Descripción |
|---|---|
| `cargar_prompt(prompt_id: str) -> str` | Carga template desde `prompts/{categoria}/{prompt_id}.md`. Lanza `ErrorConfiguracion` si no existe. |
| `renderizar_prompt(template: str, contexto: dict) -> str` | Reemplaza `{{ variable }}` con valores del contexto. |
| `_route_provider(proposito: str) -> str` | Determina qué proveedor usar según `config.yaml` → `ia_routing`. |
| `_enviar_local(prompt: str) -> str` | httpx POST a Ollama local (`http://{host}:{puerto}/api/generate`). |
| `_enviar_cloud(prompt: str) -> str` | httpx POST a Ollama Cloud con API Key y endpoint desde config. |
| `_validar_respuesta(respuesta_raw: str) -> dict` | Parseo de JSON, validación de estructura mínima esperada. |
| `analizar(prompt_id: str, contexto: dict, proposito: str = "evaluacion") -> dict` | Orquesta: cargar → renderizar → enrutar → enviar → validar → retornar dict. |

**Manejo de errores:** `ErrorLLM` con códigos ER-LLM-001 (conexión), ER-LLM-002 (timeout), ER-LLM-003 (respuesta inválida), ER-LLM-004 (formato inesperado).

**Reintentos:** Usar `decorador_reintento` de `shared/retry.py` con política desde `config.yaml` → `reintentos` (bloque global).

**Enrutamiento:** Definido en `config.yaml` → `ia_routing`. Por defecto: evaluación → local, procesamiento → cloud.

**Prompt loader:** Busca en `prompts/{categoria}/{prompt_id}.md`. Soporta subdirectorios. Cada interacción se registra con Loguru.

---

#### Tarea 3 — `shared/decision_engine.py`

**Archivo a crear:** `shared/decision_engine.py`

**Objetivo:** Implementar el motor de evaluación basado en reglas (SRV-001 según DOC-12).

**Componentes:**

| Componente | Descripción |
|---|---|
| `cargar_perfil() -> Perfil` | Construye un `Perfil` a partir de la sección `perfil` de `config.yaml`. |
| `evaluar(oferta: OfertaProcesada, perfil: Perfil) -> Evaluacion` | Evalúa compatibilidad oferta vs perfil usando criterios ponderados. |
| `_calcular_puntaje(oferta, perfil, pesos) -> float` | Calcula puntaje 0-100 aplicando pesos configurados. |
| `_clasificar(puntaje: float) -> ResultadoEvaluacion` | Usa umbrales de config: ≥80 → ALTA, ≥50 → MEDIA, <50 → BAJA. |
| `_decidir(resultado: ResultadoEvaluacion) -> DecisionEvaluacion` | ALTA/MEDIA → CONTINUAR, BAJA → DESCARTAR. |
| `_justificar(oferta, perfil, puntajes_parciales) -> str` | Genera texto con desglose de puntuación. |

**Criterios evaluados** (pesos desde `config.yaml` → `evaluacion.pesos`):

| Criterio | Peso configurable | Matching |
|---|---|---|
| Experiencia | 0.30 | `perfil.experiencia_anios` vs oferta |
| Tecnología | 0.25 | RapidFuzz entre `perfil.tecnologias` y `oferta.tecnologias` |
| Ubicación | 0.15 | RapidFuzz entre `perfil.ubicaciones_preferidas` y oferta |
| Modalidad | 0.10 | Coincidencia exacta contra `perfil.modalidades_preferidas` |
| Idiomas | 0.10 | Coincidencia de nivel entre `perfil.idiomas` y `oferta.idiomas` |
| Seniority | 0.10 | Coincidencia entre `perfil.seniority` y oferta |

**Reglas de negocio:**
- Empresas en `perfil.empresas_excluidas` → descarte automático (puntaje = 0).
- `perfil.salario_minimo` no cubierto → puntaje penalizado.
- La justificación incluye desglose por criterio.

---

#### Tarea 4 — `shared/state_machine.py`

**Archivo a crear:** `shared/state_machine.py`

**Objetivo:** Implementar la máquina de estados del ciclo de vida de las ofertas (basada en DOC-03 RTD-001 a RTD-010 y DOC-04 EPD-001 a EPD-010).

**Componentes:**

| Componente | Descripción |
|---|---|
| `TRANSICIONES_VALIDAS: dict[EstadoOferta, list[EstadoOferta]]` | Mapa de transiciones permitidas. |
| `transicionar(estado_actual: EstadoOferta, estado_destino: EstadoOferta) -> EstadoOferta` | Valida y ejecuta transición. Lanza `ErrorInterno` (ER-INT-010) si es inválida. |
| `transiciones_posibles(estado: EstadoOferta) -> list[EstadoOferta]` | Retorna destinos válidos desde un estado. |

**Transiciones definidas:**

```
DESCUBIERTA  → PREPARADA
PREPARADA    → EVALUADA
EVALUADA     → ACEPTADA | DESCARTA
ACEPTADA     → PROCESADA
DESCARTA     → FINALIZADA
PROCESADA    → FINALIZADA
```

**Validaciones:** Aplica RTD-001 a RTD-010: solo transiciones definidas, no omitir etapas, no retroceder.

---

#### Tarea 5 — Tests unitarios

**Archivos a crear:**

| Archivo | Contenido |
|---|---|
| `tests/test_ia_service.py` | Tests con mock de httpx (respuesta Ollama simulada), carga de prompts, error si prompt no existe. |
| `tests/test_decision_engine.py` | Tests con fixtures `oferta_procesada_ejemplo` + nuevo `perfil_ejemplo`. Verificar puntuaciones y clasificaciones. |
| `tests/test_persistence.py` | Tests CRUD con `archivo_bd_temporal`: generar_id, leer_tabla, escribir_fila, buscar_por_id, actualizar. |
| `tests/test_state_machine.py` | Tests de transiciones válidas e inválidas. |

**Fixture adicional en `conftest.py`:** `perfil_ejemplo() -> Perfil`

---

#### Tarea 6 — Validación final

```bash
ruff check .
mypy .
pytest tests/ -v
```

**Criterio:** 0 errores en ruff, 0 errores en mypy, todos los tests verdes.

---

## Fase 3. Prompts iniciales

1. Crear `prompts/evaluacion_inicial/` — prompt para analizar compatibilidad oferta/perfil.
2. Crear `prompts/procesamiento/` — prompts para extracción estratégica y generación de insumos.
3. Cada prompt: archivo con identificador (PRM-XXX), sección de instrucciones, variables `{{ }}`, formato de salida esperado.
4. Probar cada prompt manualmente con Ollama + una oferta real.
5. Ajustar y dejar versión 1 aprobada.

---

## Fase 4. Módulo 1 — Descubrimiento de oportunidades

1. Crear `modules/descubrimiento/` con capas (interfaz, orquestación, servicios).
2. Implementar con Playwright:
   - Login/logout en LinkedIn (sesión reusable).
   - Búsqueda con filtros desde config.
   - Navegación de resultados (paginación).
3. Extraer HTML crudo → pasarlo a `shared/models.py` (BeautifulSoup4 + lxml).
4. Guardar ofertas descubiertas via `shared/persistence.py`.
5. Registrar logs y eventos.
6. Manejo de errores: ER-NAV, ER-RED, ER-EXT con reintentos (Tenacity).
7. Pruebas:
   - Unitarias: parsing de HTML simulado.
   - Integración: LinkedIn real (etiquetadas `integration`).
8. **Validación:** lint → typecheck → pytest → se ejecuta contra LinkedIn y se revisan resultados.

---

## Fase 5. Módulo 2 — Preparación de ofertas

1. Crear `modules/preparacion/`.
2. Leer ofertas crudas desde persistencia.
3. Limpiar campos (espacios, saltos de línea, HTML residual).
4. Normalizar: fechas (ISO 8601), salarios (número + moneda), ubicaciones, modalidad.
5. Validar campos obligatorios, integridad, consistencia.
6. Detectar duplicados (RapidFuzz en título + empresa).
7. Asignar estado inicial (`recibida` / `preparada`).
8. Guardar versión preparada + log de transformaciones.
9. Manejo de errores: ER-VAL, ER-DAT.
10. Pruebas:
    - Unitarias con ofertas reales anonimizadas como fixtures.
    - Edge cases: campos vacíos, formatos raros, ofertas duplicadas.
11. **Validación.**

---

## Fase 6. Módulo 3 — Evaluación inicial

1. Crear `modules/evaluacion/`.
2. Cargar ofertas preparadas + perfil profesional del usuario.
3. Invocar `shared/decision_engine.py`:
   - Aplicar criterios DOC-03, pesos configurables.
   - Calcular puntuación de compatibilidad.
4. Opcional: llamar LLM (prompt de evaluación) para rubros no determinísticos.
5. Clasificar: Alta / Media / Baja.
6. Decidir: continúa o descarta (con justificación).
7. Guardar resultados + trazabilidad.
8. Manejo de errores: ER-LLM, ER-DAT, ER-INT.
9. Pruebas:
   - Unitarias: reglas aplicadas a perfiles mock.
   - LLM mockeado para tests determinísticos.
10. **Validación.**

---

## Fase 7. Módulo 4 — Procesamiento profundo

1. Crear `modules/procesamiento/`.
2. Cargar ofertas aceptadas en evaluación.
3. Invocar LLM con prompts de `prompts/procesamiento/`:
   - Diagnóstico de la vacante.
   - Extracción estratégica (requisitos clave, cultura, diferenciadores).
   - Diseño de candidatura (puntos fuertes a destacar, brechas a mitigar).
   - Generación de insumos (carta de presentación borrador, preparación de entrevista).
4. Validar consistencia del resultado (Pydantic).
5. Guardar productos en persistencia + `data/salida/`.
6. Registrar historial completo.
7. Manejo de errores: ER-LLM, ER-INT.
8. Pruebas:
   - Con prompts reales + oferta real → inspeccionar calidad.
   - Con respuestas mock → validar parseo y estructuras.
9. **Validación.**

---

## Fase 8. Módulo 5 — Gestión de resultados

1. Crear `modules/gestion/`.
2. Implementar: historial completo por oferta, gestión de estados, seguimiento.
3. Reportes:
   - Resumen de ofertas (procesadas, descartadas, pendientes).
   - Exportación a formato compatible (`data/salida/`).
4. Validar trazabilidad completa (cada decisión → su justificación → log).
5. Manejo de errores: ER-DB, ER-DAT.
6. Pruebas:
   - Unitarias: consultas, filtros, exportación.
   - Integración: datos reales → reporte generado.
7. **Validación.**

---

## Fase 9. Integración del MVP

1. Crear `scripts/run_mvp.py` — orquestador que ejecuta las 5 fases en secuencia.
2. Probar flujo completo end-to-end con un conjunto pequeño de ofertas reales.
3. Verificar: logs, errores, estados, persistencia, archivos generados.
4. Corregir dependencias rotas y ajustar secuencia.
5. Ejecutar pytest de regresión (lint → typecheck → tests).
6. Revisar cobertura: ¿alguna funcionalidad de DOC-01 no implementada? ¿documentación inconsistente?
7. **Aprobación final del MVP.**

---

## Criterio de validación por paso

Cada paso numerado en las fases anteriores se considerará completado cuando:

1. El código está escrito y ubicado según DOC-07.
2. `ruff check .` pasa sin errores.
3. `mypy .` pasa sin errores.
4. `pytest tests/` pasa (tests relevantes al paso existen y son verdes).
5. Se revisa el resultado y se aprueba antes de pasar al siguiente paso.

---

## Referencias

| Documento | Propósito |
|-----------|-----------|
| DOC-01 | Requisitos funcionales |
| DOC-03 | Modelo de decisiones |
| DOC-04 | Flujo de datos |
| DOC-05 | Estándares del proyecto |
| DOC-06 | Manejo de errores |
| DOC-07 | Arquitectura de carpetas |
| DOC-08 | Alcance y objetivos |
| DOC-09 | Investigación de fuentes (LinkedIn) |
| DOC-11 | Stack tecnológico |
| DOC-12 | Arquitectura general del sistema |
| DOC-13 | Modelo de datos |
| Anexo 5A | Catálogo de prefijos |
| Anexo 5B | Estándares técnicos oficiales |
| Anexo 9A | Decisiones estratégicas LinkedIn |
