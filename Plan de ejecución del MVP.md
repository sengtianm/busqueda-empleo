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
   - **Data layer:** tests con archivos .xlsx temporales.

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

10. **shared/models.py** — Modelos Pydantic v2: `Oferta`, `Evaluacion`, `Resultado`, `Empresa`, etc. (DOC-13).

11. **shared/persistence.py** — Acceso a .xlsx via openpyxl. Métodos: leer hoja, escribir fila, actualizar, buscar por ID. Path desde config.

12. **tests/conftest.py + tests/fixtures/** — Fixtures básicos (config de prueba, logger mock, persistence temp) y directorio `tests/fixtures/` con `.gitkeep`.

13. **Validación final:**
    - `ruff check .` sin errores.
    - `mypy .` sin errores.
    - `python -c "import shared.config, shared.errors, shared.logging_setup, shared.retry, shared.models, shared.persistence"` — todos los módulos importables sin error.
    - `pytest tests/` — todas las pruebas pasan.

---

## Fase 2. Servicios compartidos (capa transversal)

1. Implementar `shared/ia_service.py`:
   - Comunicación con Ollama (httpx a `localhost:11434`).
   - Prompt loader desde `prompts/`.
   - Validación de respuestas (estructura esperada, reintentos).
   - Métodos: `analizar(prompt_id: str, contexto: dict) -> dict`.
2. Implementar `shared/decision_engine.py`:
   - Motor de reglas simple evaluable desde dicts.
   - Método `evaluar(oferta: Oferta, perfil: Perfil) -> ResultadoEvaluacion`.
   - Reglas cargadas desde `config/config.yaml` (umbrales, pesos, criterios — DOC-03).
3. Implementar `shared/state_machine.py`:
   - Definir estados del ciclo de vida (DOC-04, DOC-03).
   - Transiciones válidas.
   - Método `transicionar(oferta_id, estado_origen, estado_destino) -> bool`.
4. Crear `tests/test_ia_service.py`, `tests/test_decision_engine.py`, `tests/test_persistence.py`.
5. **Validación:** lint → typecheck → pytest.

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
   - Exportación a .xlsx formateado (`data/salida/`).
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
