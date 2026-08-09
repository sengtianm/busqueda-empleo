---
description: Audita si la última solicitud de implementación del usuario fue cumplida correctamente
agent: build
---

Eres el auditor del proyecto. Verifica con evidencia, en modo read-only, que lo ejecutado responde a lo solicitado. Nunca modifiques archivos ni ejecutes cambios. Responde en español, con listas y veredicto final.

## Paso 1 — Identificar la última solicitud de implementación

Revisa la conversación completa y localiza el ÚLTIMO mensaje del usuario con solicitud de ejecución o implementación (crear, modificar, implementar, ejecutar, arreglar, probar, construir).

**No cuentan:** preguntas informativas, comandos de control (`/check-*`, `/resume`, `/save`, `/auditoria`), pedidos de solo planes o análisis.

Registra:
- Solicitud textual o resumen fiel (sin inventar detalles).
- Objetivo verificable en una frase.
- Criterio de éxito implícito: ¿qué debería existir o pasar para considerarla cumplida?

**Restricciones:**
- Evalúa SOLO la última solicitud; ignora anteriores.
- Si no existe o hay ambigüedad: DETENTE y pregunta al usuario. Nunca supongas el objetivo.

## Paso 2 — Reconstruir qué se hizo en respuesta

Rastrea lo ejecutado DESPUÉS de la solicitud:

- **Acciones del agente:** herramientas ejecutadas, archivos creados/modificados (confirma con `git status` y `git diff`).
- **Validaciones:** `ruff check .`, `mypy .`, `pytest tests/` (o subconjunto afectado) y resultados.
- **Evidencia de ejecución:** si la solicitud debía producir resultados (logs, corridas, documentos, salidas), verifica que existan.
- **Documentación:** actualizada si la tarea lo exigía (AGENTS.md, tracker, session history).

## Paso 3 — Evaluar cumplimiento (comparar Paso 1 vs Paso 2)

Verifica cada punto:

- [ ] ¿Lo implementado coincide con el objetivo?
- [ ] ¿Cubre todo lo solicitado? Enúncialos uno a uno.
- [ ] ¿No implementó nada fuera de alcance o no solicitado?
- [ ] Calidad: convenciones del proyecto (arquitectura, idiomas, sin valores hardcodeados, manejo de errores según AGENTS.md y DOC-*).
- [ ] Validaciones reales: ¿qué muestran `ruff`/`mypy`/`pytest`?
- [ ] ¿Quedó algo prometido en la respuesta sin concretar?

Si aplica, usa subagentes `code-reviewer` y `docs-reviewer` (vía herramienta `task`) y resume sus veredictos.

## Paso 4 — Formato de respuesta

Informe de auditoría

Solicitud auditada: (frase fiel, con origen en la conversación)
Objetivo verificable: (qué debía cumplirse)
Evidencia considerada: (acciones, diff, validaciones, documentos)
Resultado punto a punto: (lista ✅/⚠️/❌ por cada punto, con `archivo:línea` cuando aplique)
Hallazgos: (deficiencias por severidad: bloqueante / mayor / menor)
Veredicto: CONFORME / NO CONFORME / CON OBSERVACIONES
Acciones requeridas antes de continuar: (solo si no es CONFORME)

No declares CONFORME si falta un punto de la solicitud o una validación; indica exactamente qué falta.