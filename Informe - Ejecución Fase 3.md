# Informe de ejecución — Fase 3

**Proyecto:** Automatización de búsqueda de empleo (MVP)
**Fecha:** 24/07/2026
**Estado:** Tarea completada con observaciones

---

## 1. Objetivo

Ejecutar la Fase 3 del Plan de ejecución del MVP, que consiste en crear los prompts iniciales del sistema:
- `prompts/evaluacion_inicial/` — prompt para analizar la compatibilidad oferta-perfil mediante LLM
- `prompts/procesamiento/` — prompts para el procesamiento profundo de ofertas aceptadas

---

## 2. Actividades realizadas

### 2.1. Tarea 1 — Crear `prompts/evaluacion_inicial/`

**Archivo creado:** `prompts/evaluacion_inicial/compatibilidad.md`

**Identificador:** PRM-001

**Propósito:** Analizar la compatibilidad cualitativa entre una oferta procesada y el perfil profesional del usuario, cubriendo aspectos no determinísticos que el motor de reglas no puede capturar (cultura empresarial, factores diferenciadores, brechas cualitativas).

**Estructura (Anexo 5C §C.9):**
- Objetivo, Entradas (`OfertaProcesada` + `Perfil`), Variables (`{{ oferta }}`, `{{ perfil }}`), Instrucciones, Resultado esperado (JSON con campos `compatibilidad`, `justificacion`, `factores_clave`, `brechas`, `compatibilidad_cultural`), Observaciones, Versión v1.

---

### 2.2. Tarea 2 — Crear `prompts/procesamiento/`

**Archivos creados (4):**

| Archivo | ID | Propósito | Variables | Resultado esperado |
|---------|----|-----------|-----------|--------------------|
| `diagnostico.md` | PRM-002 | Analizar la vacante en profundidad | `{{ oferta }}` | JSON: diagnostico, requisitos_clave, competencias, responsabilidades, beneficios, cultura_empresarial |
| `extraccion_estrategica.md` | PRM-003 | Extraer factores diferenciales y riesgos | `{{ oferta }}`, `{{ perfil }}` | JSON: diferenciadores, requisitos_negociables, riesgos, oportunidades, posicionamiento |
| `diseno_candidatura.md` | PRM-004 | Diseñar estrategia de postulación | `{{ oferta }}`, `{{ perfil }}`, `{{ diagnostico }}` | JSON: puntos_fuertes, brechas, narrativa, estrategia_postulacion, argumentos_clave |
| `insumos.md` | PRM-005 | Generar carta de presentación y preparación de entrevista | `{{ oferta }}`, `{{ perfil }}`, `{{ estrategia }}` | JSON: borrador_carta, preparacion_entrevista, preguntas_clave |

Todos los prompts siguen la plantilla oficial del Anexo 5C §C.9 con las 8 secciones obligatorias.

---

### 2.3. Tarea 3 — Plantilla oficial Anexo 5C

Los 5 prompts se estructuraron con:

```markdown
## PRM-XXX Nombre del prompt

**Objetivo.**
**Entradas.**
**Variables.**
**Instrucciones.**
**Resultado esperado.**
```json
{ ... }
```
**Observaciones.**
**Versión:** v1
```

Cada prompt define explícitamente:
- Los campos de `OfertaProcesada` y `Perfil` que utiliza
- El formato JSON exacto que debe devolver el LLM
- Instrucciones claras para evitar texto adicional y bloques Markdown

---

### 2.4. Tarea 4 — Prueba manual con Ollama (pendiente)

**Estado:** ⏳ No completada

**Qué se verificó:**
- Los prompts se cargan correctamente desde `shared/ia_service.py::cargar_prompt()`
- Las variables `{{ }}` se renderizan sin errores desde `renderizar_prompt()`
- La comunicación con Ollama funciona (verificado con `curl` y `httpx` directo)

**Problema detectado:**
- Los modelos disponibles en el equipo (`qwen3.5:9b`, `qwen3.5:4b`) incluyen un proceso interno de "thinking" que hace que las respuestas tarden entre 120 y 180 segundos
- El timeout por defecto de 60s en `config.yaml` no es suficiente
- Aumentando el timeout a 200s funciona, pero el tiempo total de prueba para 5 prompts secuenciales es impracticable en la sesión actual

**Recomendación:** Ejecutar la prueba localmente con:
```bash
cd /ruta/del/proyecto
# Ajustar timeout en config/config.yaml si es necesario
ollama run qwen3.5:9b  # Para pre-cargar el modelo
python3 -c "
from shared.ia_service import analizar
import json

oferta = { ... }  # Oferta real o de ejemplo
perfil = { ... }  # Perfil desde config.yaml

resultado = analizar('evaluacion_inicial/compatibilidad', {
    'oferta': json.dumps(oferta),
    'perfil': json.dumps(perfil)
})
print(resultado)
"
```

---

### 2.5. Tarea 5 — Versión v1 (pendiente de aprobación)

**Estado:** ⬜ Pendiente

Los 5 prompts están creados como versión `v1` pero no se consideran aprobados hasta que:
1. Se ejecute la prueba manual con Ollama (Tarea 4)
2. El Arquitecto del Proyecto revise y apruebe

---

## 3. Archivos creados

| Archivo | Líneas |
|---------|--------|
| `prompts/evaluacion_inicial/compatibilidad.md` | 46 |
| `prompts/procesamiento/diagnostico.md` | 52 |
| `prompts/procesamiento/extraccion_estrategica.md` | 51 |
| `prompts/procesamiento/diseno_candidatura.md` | 55 |
| `prompts/procesamiento/insumos.md` | 53 |
| **Total** | **~257 líneas** |

## 4. Archivos modificados

| Archivo | Cambio |
|---------|--------|
| `Plan de ejecución del MVP.md` | Tareas 3 y 4 de Fase 3 detalladas con plantilla Anexo 5C y especificación de ambos prompts |
| `Seguimiento MVP.md` | Estado de Fase 3 actualizado (tareas 1-3 ✅, tarea 4 ⏳, tarea 5 ⬜) |
| `config/config.yaml` | Modelo cambiado a `qwen3.5:9b` por disponibilidad local; timeout restaurado a 60s |

## 5. Validaciones

| Herramienta | Resultado |
|-------------|-----------|
| `ruff check .` | 0 errors |
| `mypy .` | 0 errors |
| `pytest tests/` | 39/39 passed |

## 6. Commits realizados

| Hash | Mensaje |
|------|---------|
| `3d9e8c7` | add weight-sum validation to decision_engine with fail-fast ErrorConfiguracion |
| `7db5e3f` | fase 3: prompts iniciales del MVP (PRM-001 a PRM-005) |
| `f2d0063` | update historial de sesiones: fase 3 y validacion de pesos |

## 7. Problemas encontrados

1. **Rendimiento de Ollama:** Los modelos locales `qwen3.5:9b` y `qwen3.5:4b` incluyen un proceso de "thinking" que incrementa significativamente el tiempo de respuesta (>120s). La prueba manual no pudo completarse en esta sesión.

2. **Modelo no disponible:** El modelo configurado originalmente (`qwen:8b`) no está disponible en el equipo. Se actualizó a `qwen3.5:9b`, la versión más cercana disponible.

## 8. Riesgos identificados

- Los prompts no han sido probados con un LLM real, por lo que podrían requerir ajustes en la próxima sesión de prueba
- Si el usuario cambia de modelo LLM en el futuro, los prompts están diseñados para ser independientes del modelo (CPR-005 de DOC-05), pero puede requerir ajustes menores

## 9. Observaciones

- Fase 4 (Descubrimiento) puede comenzar sin necesidad de esperar la prueba manual de Fase 3, ya que son flujos independientes
- Los prompts de `procesamiento/` tienen dependencia secuencial: PRM-002 → PRM-003 → PRM-004 → PRM-005, donde cada uno consume la salida del anterior
- El prompt `evaluacion_inicial/compatibilidad` es opcional en Fase 6 — el motor de reglas (`decision_engine.py`) es el que toma la decisión principal

---

*Fin del reporte — Versión v1 pendiente de prueba manual y aprobación del Arquitecto.*