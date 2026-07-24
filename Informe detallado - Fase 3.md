# Informe detallado — Fase 3: Prompts iniciales

**Proyecto:** Automatización de búsqueda de empleo (MVP)
**Fecha de ejecución:** 24/07/2026
**Sesión:** Sesión 2 (extendida, mañana + tarde + noche)
**Estado final:** ✅ Tarea completada

---

## Índice

1. [Resumen ejecutivo](#1-resumen-ejecutivo)
2. [Contexto y plan original](#2-contexto-y-plan-original)
3. [Tarea 1 — Prompt de evaluación inicial](#3-tarea-1--prompt-de-evaluación-inicial)
4. [Tarea 2 — Prompts de procesamiento](#4-tarea-2--prompts-de-procesamiento)
5. [Tarea 3 — Plantilla oficial Anexo 5C](#5-tarea-3--plantilla-oficial-anexo-5c)
6. [Tarea 4 — Prueba manual con IA](#6-tarea-4--prueba-manual-con-ia)
7. [Tarea 5 — Versión 1 aprobada](#7-tarea-5--versión-1-aprobada)
8. [Infraestructura de prueba creada](#8-infraestructura-de-prueba-creada)
9. [Crisis de estrategia de IA y resolución](#9-crisis-de-estrategia-de-ia-y-resolución)
10. [Archivos creados y modificados](#10-archivos-creados-y-modificados)
11. [Validaciones](#11-validaciones)
12. [Problemas encontrados](#12-problemas-encontrados)
13. [Decisiones adoptadas](#13-decisiones-adoptadas)
14. [Estado final](#14-estado-final)

---

## 1. Resumen ejecutivo

La Fase 3 consistió en crear los prompts de inteligencia artificial que el sistema utiliza para analizar ofertas de empleo y generar insumos de postulación. Se crearon **5 prompts** organizados en dos categorías, siguiendo la plantilla oficial del Anexo 5C §C.9. Durante la ejecución se identificó que el hardware disponible (GTX 1650 4GB VRAM) no podía ejecutar modelos locales de forma eficiente, lo que provocó un cambio de estrategia: de local-only → híbrida → cloud-only con `gemma4:31b-cloud` vía Ollama local como proxy.

Todos los prompts fueron probados exitosamente contra el modelo cloud, devolviendo JSON válido y contenido coherente. Se creó además infraestructura de prueba para facilitar pruebas futuras: script CLI (`scripts/probar_prompt.py`), contextos de prueba (`tests/fixtures/contextos_prompt.yaml`) y guía de usuario (`scripts/LEEME-pruebas.md`).

---

## 2. Contexto y plan original

### 2.1. ¿Qué dice el plan?

El Plan de ejecución del MVP define la Fase 3 con 5 tareas:

| # | Tarea | Descripción |
|---|-------|-------------|
| 1 | `prompts/evaluacion_inicial/` | Prompt para analizar compatibilidad oferta/perfil |
| 2 | `prompts/procesamiento/` | Prompts para extracción estratégica y generación de insumos |
| 3 | Identificadores PRM-XXX + plantilla Anexo 5C | Cada prompt con formato oficial |
| 4 | Prueba manual con Ollama | Verificar que cada prompt funciona con un LLM real |
| 5 | Versión 1 aprobada | Ajustar y dejar versión aprobada |

### 2.2. Dependencias

La Fase 3 depende de la Fase 2 (especialmente de `shared/ia_service.py` que implementa `cargar_prompt()` y `analizar()`). La Fase 3 **no bloquea** la Fase 4 (Descubrimiento), ya que son flujos independientes.

---

## 3. Tarea 1 — Prompt de evaluación inicial

### 3.1. Archivo creado

```
prompts/evaluacion_inicial/compatibilidad.md
```

### 3.2. Identificador

**PRM-001**

### 3.3. Propósito

Analizar la compatibilidad cualitativa entre una oferta de empleo procesada y el perfil profesional del usuario, cubriendo aspectos **no determinísticos** que el motor de reglas (`decision_engine.py`) no puede capturar: cultura empresarial, factores diferenciadores, brechas cualitativas, contexto.

### 3.4. Entradas

| Variable | Contenido |
|----------|-----------|
| `{{ oferta }}` | OfertaProcesada JSON: titulo_limpio, descripcion_limpia, salario_min/max, moneda, ubicacion_limpia, modalidad, requisitos, tecnologias, idiomas, experiencia_anios |
| `{{ perfil }}` | Perfil JSON: tecnologias, experiencia_anios, idiomas, ubicaciones_preferidas, modalidades_preferidas, salario_minimo, seniority, empresas_objetivo/excluidas, educacion_nivel |

### 3.5. Resultado esperado

```json
{
  "compatibilidad": "ALTA|MEDIA|BAJA",
  "justificacion": "Texto explicativo de la evaluación general.",
  "factores_clave": ["Factor positivo 1", "Factor positivo 2"],
  "brechas": ["Brecha o riesgo 1", "Brecha o riesgo 2"],
  "compatibilidad_cultural": "Texto sobre la afinidad cultural percibida."
}
```

### 3.6. Rol del prompt

Este prompt es **complementario** al motor de reglas. Mientras `decision_engine.py` asigna una puntuación numérica determinística (0-100) basada en 6 criterios ponderados, PRM-001 añade una capa cualitativa que evalúa aspectos como:

- ¿La cultura empresarial encaja con el candidato?
- ¿Hay factores diferenciadores que las reglas no ponderan?
- ¿Existen brechas cualitativas (no solo cuantitativas)?

En la arquitectura final, PRM-001 se ejecuta **después** del motor de reglas, solo si la puntuación determinística lo justifica (ofertas en el umbral MEDIA, por ejemplo).

---

## 4. Tarea 2 — Prompts de procesamiento

Se crearon **4 prompts** en `prompts/procesamiento/`, formando una **cadena secuencial** donde cada prompt consume la salida del anterior:

```
PRM-002 (Diagnóstico)
    ↓
PRM-003 (Extracción estratégica)
    ↓
PRM-004 (Diseño de candidatura)
    ↓
PRM-005 (Insumos)
```

### 4.1. PRM-002 — Diagnóstico de la vacante

**Archivo:** `prompts/procesamiento/diagnostico.md`

**Propósito:** Analizar en profundidad una oferta para comprender la naturaleza de la vacante: qué busca realmente la empresa, qué requisitos son obligatorios vs deseables, competencias necesarias, responsabilidades, beneficios y cultura empresarial.

**Entrada:** Solo `{{ oferta }}` (no necesita perfil del candidato).

**Salida:**
```json
{
  "diagnostico": "Resumen ejecutivo del análisis de la vacante.",
  "requisitos_clave": [
    {"requisito": "Descripción", "tipo": "obligatorio|deseable"}
  ],
  "competencias": {
    "tecnicas": ["Python", "SQL"],
    "blandas": ["Comunicación", "Autonomía"]
  },
  "responsabilidades": ["Diseñar pipelines"],
  "beneficios": ["Trabajo remoto"],
  "cultura_empresarial": "Descripción de indicios culturales."
}
```

**Importancia:** Es la base de toda la cadena de procesamiento. Sin un buen diagnóstico, los prompts posteriores producirán resultados de baja calidad.

---

### 4.2. PRM-003 — Extracción estratégica

**Archivo:** `prompts/procesamiento/extraccion_estrategica.md`

**Propósito:** Identificar elementos estratégicos que maximicen las posibilidades de éxito: factores diferenciadores, requisitos negociables, riesgos, oportunidades y posicionamiento recomendado.

**Entradas:** `{{ oferta }}`, `{{ perfil }}`

**Salida:**
```json
{
  "diferenciadores": ["Experiencia financiera"],
  "requisitos_negociables": [
    {"requisito": "Kafka", "estrategia": "Compensar con Spark"}
  ],
  "riesgos": [
    {"riesgo": "Sin Terraform", "severidad": "media"}
  ],
  "oportunidades": ["Aprender Kafka"],
  "posicionamiento": "Destacar experiencia financiera."
}
```

---

### 4.3. PRM-004 — Diseño de candidatura

**Archivo:** `prompts/procesamiento/diseno_candidatura.md`

**Propósito:** Diseñar una estrategia de postulación personalizada: puntos fuertes a destacar, brechas a mitigar, narrativa profesional, estrategia para CV/carta/LinkedIn, y argumentos clave.

**Entradas:** `{{ oferta }}`, `{{ perfil }}`, `{{ diagnostico }}` (salida de PRM-002)

**Salida:**
```json
{
  "puntos_fuertes": ["8 años experiencia"],
  "brechas": [{"brecha": "Sin Kafka", "mitigacion": "Cursos básicos"}],
  "narrativa": "Historia profesional...",
  "estrategia_postulacion": {
    "cv": "Enfoque...",
    "carta": "Enfoque...",
    "linkedin": "Ajustes..."
  },
  "argumentos_clave": ["Experiencia superior"]
}
```

---

### 4.4. PRM-005 — Insumos para la candidatura

**Archivo:** `prompts/procesamiento/insumos.md`

**Propósito:** Generar recursos concretos: borrador de carta de presentación, guía de preparación para entrevista, y preguntas clave que el candidato debería hacer al empleador.

**Entradas:** `{{ oferta }}`, `{{ perfil }}`, `{{ estrategia }}` (salida de PRM-004)

**Salida:**
```json
{
  "borrador_carta": "Texto completo de la carta en Markdown.",
  "preparacion_entrevista": {
    "introduccion": "Consejos generales.",
    "preguntas_probables": [
      {"pregunta": "¿...?", "respuesta_sugerida": "Enfoque..."}
    ],
    "consejos": ["Consejo 1"]
  },
  "preguntas_clave": [
    {"pregunta": "¿...?", "proposito": "Qué obtener."}
  ]
}
```

---

## 5. Tarea 3 — Plantilla oficial Anexo 5C

### 5.1. Estructura aplicada

Los 5 prompts siguen la **plantilla oficial C.9** del Anexo 5C con las siguientes secciones obligatorias:

| Sección | Descripción |
|---------|-------------|
| **PRM-XXX Nombre** | Identificador único según catálogo de prefijos (Anexo 5A) + nombre descriptivo |
| **Objetivo** | Propósito del prompt en una frase |
| **Entradas** | Lista de modelos/objetos que necesita el prompt |
| **Variables** | Variables `{{ }}` que se renderizan con contexto |
| **Instrucciones** | Instrucciones detalladas para el LLM (rol, tareas, restricciones) |
| **Resultado esperado** | Esquema JSON exacto que debe devolver el modelo |
| **Observaciones** | Notas adicionales, dependencias, restricciones |
| **Versión** | `v1` |

### 5.2. Principios de diseño

1. **Independencia del modelo (CPR-005):** Los prompts no mencionan modelos específicos, proveedores, ni formatos de API. El routing se define en `config.yaml`.
2. **Formato JSON estricto:** Todos exigen respuesta JSON sin texto adicional ni bloques Markdown, facilitando el parseo automático.
3. **Campos tipados:** Los esquemas JSON definen tipos (string, array, objeto anidado) para validación posterior con Pydantic.
4. **Instrucciones sin ambigüedad:** Roles claros ("Eres un analista laboral experto"), tareas numeradas, y formato de salida exacto.

---

## 6. Tarea 4 — Prueba manual con IA

### 6.1. Primer intento (modelo local)

En la primera ejecución de la tarde, se intentó probar los prompts con el modelo local `qwen3.5:9b`. Resultado: **timeout >120s**. El modelo de 6.6GB no cabía en los 4GB de VRAM de la GTX 1650, desbordándose a RAM compartida y volviéndose extremadamente lento.

### 6.2. Segundo intento (modelo local más pequeño)

Se cambió a `qwen3.5:4b` (3.4GB, cabe en VRAM). Resultado: **timeout >60s**. Aunque cabía en VRAM, el proceso interno de "thinking" del modelo era demasiado lento para uso interactivo.

### 6.3. Tercer intento (estrategia híbrida)

Se diseñó una estrategia híbrida:
- **PRM-001** (evaluación) → `qwen3.5:4b` local (respuestas rápidas, análisis simple)
- **PRM-002 al PRM-005** (procesamiento) → `gemma4:31b` cloud (mejor calidad)

Se refactorizó `shared/ia_service.py` para soportar multi-proveedor con enrutamiento por propósito. Se actualizó `config.yaml` con secciones `ia_local`, `ia_cloud`, `ia_routing`.

### 6.4. Cuarto intento (solo cloud)

Al probar el modelo local `qwen3.5:4b` se confirmó que incluso el modelo pequeño era demasiado lento (60s+ por respuesta). Decisión final:

- **Ambos propósitos** (evaluación y procesamiento) → `gemma4:31b-cloud`
- Ollama local actúa como **proxy** al cloud (sin API Key externa)
- El modelo local `qwen3.5:4b` se conserva en configuración como alternativa futura

### 6.5. Resultados de la prueba

Los 5 prompts se probaron contra `gemma4:31b-cloud` con el siguiente resultado:

| Prompt | ¿JSON válido? | ¿Contenido coherente? | Observaciones |
|--------|:---:|:---:|---------------|
| PRM-001 | ✅ | ✅ | Análisis cualitativo correcto, identifica brechas reales |
| PRM-002 | ✅ | ✅ | Diagnóstico detallado, diferencia obligatorios/deseables |
| PRM-003 | ✅ | ✅ | Extracción estratégica con riesgos priorizados |
| PRM-004 | ✅ | ✅ | Narrativa convincente, brechas con mitigación |
| PRM-005 | ✅ | ✅ | Carta de presentación usable, preguntas relevantes |

**Tiempo de respuesta:** ~15-30 segundos por prompt (dependiendo de la carga del servidor Ollama Cloud).

### 6.6. Herramienta de prueba

Se creó `scripts/probar_prompt.py` para facilitar pruebas futuras:

```bash
# Ver prompt renderizado sin enviar al modelo
python scripts/probar_prompt.py PRM-001 --dry-run

# Ejecutar contra el modelo
python scripts/probar_prompt.py PRM-001

# Usar contexto alternativo
python scripts/probar_prompt.py PRM-002 --context ruta/contexto.yaml
```

El script:
1. Carga el contexto desde `tests/fixtures/contextos_prompt.yaml`
2. Construye las variables necesarias según el prompt (`VARS_POR_PROMPT`)
3. Renderiza el prompt con `renderizar_prompt()`
4. Envía al proveedor correcto según `config.yaml` → `ia_routing`
5. Muestra la respuesta JSON del modelo

---

## 7. Tarea 5 — Versión 1 aprobada

### 7.1. Estado de aprobación

Los 5 prompts (PRM-001 al PRM-005) se consideran **versión v1 funcional**:
- Estructura correcta según Anexo 5C ✅
- Carga y renderizado sin errores ✅
- Prueba contra LLM real con resultados coherentes ✅
- Todos los campos JSON esperados presentes ✅

### 7.2. Pendiente

La **revisión formal del Arquitecto del Proyecto** está pendiente. Cualquier ajuste solicitado se aplicará antes de considerar la Fase 3 como definitivamente cerrada.

---

## 8. Infraestructura de prueba creada

### 8.1. `tests/fixtures/contextos_prompt.yaml`

Archivo YAML con datos de prueba realistas:

| Clave | Contenido |
|-------|-----------|
| `oferta_ejemplo` | Data Engineer Senior, salario 65-85k EUR, remoto España, stack Python/Spark/AWS/Kafka |
| `perfil_ejemplo` | 8 años experiencia, Python/SQL/Spark, inglés C1, remoto/híbrido, salario min 60k |
| `diagnostico_ejemplo` | Diagnóstico simulado de PRM-002 (requisitos, competencias, cultura) |
| `estrategia_ejemplo` | Estrategia simulada de PRM-003 (puntos fuertes, brechas, narrativa) |
| `plan_candidatura_ejemplo` | Plan simulado de PRM-004 (puntos fuertes, brechas, acciones) |

### 8.2. `scripts/probar_prompt.py`

CLI para probar prompts individualmente con:
- Modo `--dry-run` para inspeccionar el prompt renderizado sin enviar al modelo
- Contexto por defecto desde `contextos_prompt.yaml`
- Soporte para contexto alternativo con `--context`
- Enrutamiento automático según `config.yaml` → `ia_routing`

### 8.3. `scripts/LEEME-pruebas.md`

Guía rápida con:
- Requisitos (Ollama local, API Key cloud)
- Comandos de ejecución para cada prompt
- Criterios de aceptación (JSON válido, campos presentes, coherencia)
- Tabla de resolución de problemas (Connection refused, 401, prompt no encontrado, timeout)

---

## 9. Crisis de estrategia de IA y resolución

### 9.1. Línea de tiempo de cambios

```
Estado original (DOC-11):
  Ollama + Gemma 4 31B cloud (todos los propósitos)
  
↓ Sesión 2 — mañana

Primer cambio (por disponibilidad local):
  qwen3.5:9b local (único modelo disponible en el equipo)
  → Timeout >120s (no cabe en 4GB VRAM)

↓

Segundo cambio:
  qwen3.5:4b local (3.4GB, cabe en VRAM)
  → Timeout >60s (demasiado lento)

↓

Tercer cambio (estrategia híbrida):
  Evaluación → qwen3.5:4b local (rápido)
  Procesamiento → gemma4:31b cloud (calidad)
  → Se refactoriza ia_service.py para multi-proveedor

↓

Cuarto cambio (cloud-only):
  Evaluación → gemma4:31b-cloud
  Procesamiento → gemma4:31b-cloud
  → qwen3.5:4b también es lento; se descarta

↓

Estado final:
  gemma4:31b-cloud como ÚNICO modelo LLM
  Ollama local como proxy al cloud
  Sin API Key externa
```

### 9.2. Problema de raíz

La **GTX 1650 Mobile con 4GB VRAM** es insuficiente para ejecutar modelos de razonamiento modernos:
- `qwen3.5:9b` (6.6GB) → no cabe en VRAM, usa RAM compartida → extremadamente lento
- `qwen3.5:4b` (3.4GB) → cabe en VRAM, pero el proceso interno "thinking" es intensivo → >60s por respuesta

### 9.3. Decisión final

| Aspecto | Decisión |
|---------|----------|
| Modelo | `gemma4:31b-cloud` (único) |
| Proveedor | Ollama local como proxy al cloud |
| Autenticación | Automática (Ollama local gestiona el cloud) |
| API Key externa | No necesaria (opcional en `.env.template`) |
| Modelo local | `qwen3.5:4b` conservado en config como alternativa futura |
| Routing | Ambos propósitos → cloud |

### 9.4. Documentos actualizados por el cambio

| Documento | Cambio |
|-----------|--------|
| `config/config.yaml` | Nuevas secciones `ia_local`, `ia_cloud`, `ia_routing` |
| `config/.env.template` | Variables `IA_CLOUD_API_KEY` e `IA_CLOUD_ENDPOINT` |
| `shared/ia_service.py` | Refactor completo a multi-proveedor |
| `docs/DOC-11 - Stack tecnológico.md` | Sección 9 reescrita con estrategia híbrida → cloud |
| `AGENTS.md` | Stack actualizado: `gemma4:31b-cloud` |
| `README.md` | Stack actualizado |
| `tests/test_ia_service.py` | 7 nuevos tests (cloud, routing) |

---

## 10. Archivos creados y modificados

### 10.1. Archivos creados

| Archivo | Líneas | Propósito |
|---------|--------|-----------|
| `prompts/evaluacion_inicial/compatibilidad.md` | 46 | PRM-001: Evaluación oferta-perfil |
| `prompts/procesamiento/diagnostico.md` | 52 | PRM-002: Diagnóstico de vacante |
| `prompts/procesamiento/extraccion_estrategica.md` | 51 | PRM-003: Extracción estratégica |
| `prompts/procesamiento/diseno_candidatura.md` | 55 | PRM-004: Diseño de candidatura |
| `prompts/procesamiento/insumos.md` | 53 | PRM-005: Insumos (carta, entrevista) |
| `scripts/probar_prompt.py` | 163 | CLI para probar prompts |
| `scripts/LEEME-pruebas.md` | 55 | Guía rápida de pruebas |
| `tests/fixtures/contextos_prompt.yaml` | 165 | Datos de prueba para prompts |
| `Informe - Ejecución Fase 3.md` | 180 | Informe de ejecución |

### 10.2. Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `config/config.yaml` | Secciones `ia_local`, `ia_cloud`, `ia_routing`; timeout; modelo |
| `config/.env.template` | Variables de cloud (`IA_CLOUD_API_KEY`, `IA_CLOUD_ENDPOINT`) |
| `shared/ia_service.py` | Refactor a multi-proveedor: `_route_provider()`, `_enviar_local()`, `_enviar_cloud()` |
| `docs/DOC-11 - Stack tecnológico.md` | Sección 9 reescrita |
| `AGENTS.md` | Stack actualizado |
| `README.md` | Stack actualizado |
| `tests/test_ia_service.py` | +7 tests (cloud, routing) |
| `Plan de ejecución del MVP.md` | Tareas de Fase 3 detalladas; Tarea 2 actualizada |
| `Seguimiento MVP.md` | Estado de Fase 3 actualizado |

---

## 11. Validaciones

### 11.1. Código

| Herramienta | Resultado |
|-------------|:---------:|
| `ruff check .` | 0 errors |
| `mypy .` | 0 errors |
| `pytest tests/` | 44/44 passed |

### 11.2. Prompts

| Verificación | Resultado |
|-------------|:---------:|
| Carga desde `cargar_prompt()` | ✅ Los 5 se cargan sin error |
| Renderizado de variables `{{ }}` | ✅ Todas las variables se reemplazan correctamente |
| Formato JSON de respuesta | ✅ Los 5 devuelven JSON válido |
| Coherencia del contenido | ✅ Análisis de calidad aceptable |

### 11.3. Commits

| Hash | Mensaje |
|------|---------|
| `3d9e8c7` | add weight-sum validation to decision_engine with fail-fast ErrorConfiguracion |
| `7db5e3f` | fase 3: prompts iniciales del MVP (PRM-001 a PRM-005) |
| `f2d0063` | update historial de sesiones: fase 3 y validacion de pesos |
| `6d4d55e` | estrategia hibrida IA: refactor multi-proveedor local+cloud |

---

## 12. Problemas encontrados

### 12.1. Rendimiento insuficiente de GPU (crítico)

- **Síntoma:** Timeout >60s con cualquier modelo local
- **Causa:** GTX 1650 Mobile 4GB VRAM insuficiente para qwen3.5 (incluso el de 3.4GB)
- **Solución:** Migrar a `gemma4:31b-cloud` vía Ollama local como proxy
- **Impacto:** Dependencia de conexión a Internet para usar LLM

### 12.2. Modelo no disponible

- **Síntoma:** `qwen:8b` no existe en el equipo
- **Causa:** Configuración original asumía un modelo que no estaba instalado
- **Solución:** Actualizar a `qwen3.5:4b` (disponible localmente)
- **Lección:** Verificar disponibilidad de modelos antes de configurarlos

### 12.3. Estrategia híbrida mal estimada

- **Síntoma:** Se diseñó una arquitectura multi-proveedor completa que resultó innecesaria
- **Causa:** Se asumió que `qwen3.5:4b` sería rápido por caber en VRAM
- **Solución:** Simplificar a cloud-only, conservando la arquitectura multi-proveedor como future-proofing
- **Lección:** No asumir rendimiento sin benchmarks reales

### 12.4. Prompt no probado inicialmente

- **Síntoma:** El primer `Informe - Ejecución Fase 3.md` reportaba "prueba manual no completada"
- **Causa:** Los modelos locales eran demasiado lentos para probar
- **Solución:** Persistir con la prueba cloud hasta obtener resultados

---

## 13. Decisiones adoptadas

| ID | Decisión | Justificación |
|----|----------|---------------|
| D-001 | `gemma4:31b-cloud` como único modelo LLM | Único modelo que ofrece calidad aceptable con tiempos de respuesta viables |
| D-002 | Ollama local como proxy al cloud | Elimina necesidad de API Key externa; Ollama gestiona la autenticación |
| D-003 | Ambos propósitos (evaluación y procesamiento) usan cloud | El modelo local es inviable incluso para evaluación simple |
| D-004 | `qwen3.5:4b` conservado en config como alternativa futura | Si se mejora el hardware, puede reactivarse sin cambios de código |
| D-005 | Prompts independientes del modelo (CPR-005) | El routing puede cambiarse en `config.yaml` sin modificar prompts |
| D-006 | `IA_CLOUD_API_KEY` opcional en `.env.template` | Para cuando se quiera usar API directa sin proxy Ollama |
| D-007 | Fase 3 completada sin revisión formal del Arquitecto | Pendiente de aprobación; las tareas técnicas están ejecutadas |

---

## 14. Estado final

### 14.1. Resumen de tareas

| Tarea | Estado |
|-------|:------:|
| 1. `prompts/evaluacion_inicial/compatibilidad.md` | ✅ |
| 2. Prompts de procesamiento (PRM-002 al PRM-005) | ✅ |
| 3. Identificadores PRM + plantilla Anexo 5C | ✅ |
| 4. Prueba manual con Ollama (local + cloud) | ✅ |
| 5. Versión v1 funcional | ✅ (pendiente aprobación Arquitecto) |

### 14.2. Métricas finales

| Métrica | Valor |
|---------|-------|
| Prompts creados | 5 (PRM-001 al PRM-005) |
| Líneas de prompts | ~257 |
| Líneas de infraestructura de prueba | ~383 (script + fixture + guía) |
| Commits relacionados | 4 |
| Validaciones pasadas | ruff 0, mypy 0, pytest 44/44 |
| Cambios de estrategia de IA | 3 (local → híbrida → cloud) |

### 14.3. Lo que sigue

La Fase 4 (Descubrimiento de oportunidades) puede comenzar sin bloqueos. Los prompts están listos para ser utilizados por los módulos de Evaluación (Fase 6) y Procesamiento (Fase 7) cuando llegue el momento.

---

*Fin del informe detallado — Fase 3: Prompts iniciales*
*24/07/2026*
