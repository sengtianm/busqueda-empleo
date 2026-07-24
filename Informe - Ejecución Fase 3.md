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

### 2.4. Tarea 4 — Prueba manual con IA (pendiente)

**Estado:** ⏳ No completada

**Qué se verificó:**
- Los prompts se cargan correctamente desde `shared/ia_service.py::cargar_prompt()`
- Las variables `{{ }}` se renderizan sin errores desde `renderizar_prompt()`

**Nota sobre estrategia de modelos:**
Se adoptó una estrategia híbrida: el modelo local (`qwen3.5:4b`) se usará para PRM-001 (evaluación), y el modelo cloud (`gemma4:31b` vía Ollama Cloud) para PRM-002 al PRM-005 (procesamiento). Esto permite que la prueba manual se realice en dos pasos:

1. **PRM-001** con `qwen3.5:4b` local (cabe en 4GB VRAM, respuestas rápidas)
2. **PRM-002 al PRM-005** con `gemma4:31b` cloud (mejor calidad, requiere API Key)

**Recomendación:** Ejecutar la prueba localmente con:
```bash
cd /ruta/del/proyecto
# PRM-001 con modelo local
python3 -c "
from shared.ia_service import analizar
import json

resultado = analizar('evaluacion_inicial/compatibilidad', {
    'oferta': json.dumps(oferta),
    'perfil': json.dumps(perfil)
}, proposito='evaluacion')
print(resultado)
"
# PRM-002 al PRM-005 con modelo cloud
python3 -c "
resultado = analizar('procesamiento/diagnostico', {
    'oferta': json.dumps(oferta)
}, proposito='procesamiento')
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

1. **Rendimiento de Ollama local:** El modelo `qwen3.5:9b` (6.6 GB) no cabe en los 4GB de VRAM de la GPU, causando lentitud. Se adoptó `qwen3.5:4b` (3.4 GB) como modelo local, que sí cabe en VRAM.

2. **Estrategia híbrida:** Se reemplazó la estrategia local-only por una híbrida: `qwen3.5:4b` local para evaluación + `gemma4:31b` cloud para procesamiento. Esto requirió actualizar `DOC-11`, `ia_service.py` y la configuración.

3. **Modelo no disponible:** El modelo configurado originalmente (`qwen:8b`) no está disponible en el equipo. Se actualizó a `qwen3.5:4b` como modelo local.

## 8. Riesgos identificados

- Los prompts no han sido probados con un LLM real, por lo que podrían requerir ajustes en la próxima sesión de prueba
- Si el usuario cambia de modelo LLM en el futuro, los prompts están diseñados para ser independientes del modelo (CPR-005 de DOC-05), pero puede requerir ajustes menores
- El modelo cloud (`gemma4:31b`) requiere API Key de Ollama Cloud y conexión a Internet; sin ella el procesamiento profundo no estará disponible

## 9. Observaciones

- Fase 4 (Descubrimiento) puede comenzar sin necesidad de esperar la prueba manual de Fase 3, ya que son flujos independientes
- Los prompts de `procesamiento/` tienen dependencia secuencial: PRM-002 → PRM-003 → PRM-004 → PRM-005, donde cada uno consume la salida del anterior
- El prompt `evaluacion_inicial/compatibilidad` usa modelo local (`qwen3.5:4b`) y es opcional en Fase 6 — el motor de reglas (`decision_engine.py`) es el que toma la decisión principal
- Los prompts de `procesamiento/` (PRM-002 al PRM-005) usan modelo cloud (`gemma4:31b`) para máxima calidad

---

*Fin del reporte — Versión v1 pendiente de prueba manual y aprobación del Arquitecto.*