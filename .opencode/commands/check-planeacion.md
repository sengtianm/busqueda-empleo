---
description: Check de planeación: crea el plan de la tarea para aprobación del usuario
---

Usar cuando el usuario lo invoca para crear el plan de una tarea ya definida y analizada.
La tarea queda definida por la solicitud del usuario; el análisis previo lo aplicó el agente automáticamente (check-analisis).
No generes implementación todavía.

El plan parte del output del check-analisis (estado del proyecto, brecha, impacto, riesgos y enfoques viables). No vuelvas a diagnosticar el proyecto: consúmelo y refiérete a él.

Verifica y marca cada punto:

- [ ] Objetivo: ¿qué resultado se espera obtener?
- [ ] Restricciones: ¿qué limitaciones técnicas, funcionales o de negocio existen?
- [ ] Archivos/módulos afectados: ¿qué partes del proyecto podrían verse afectadas?
- [ ] Enfoque elegido: ¿qué enfoque de los viables del análisis se selecciona y por qué?
- [ ] Plan mínimo: ¿cuál es el cambio más pequeño posible, en pasos?
- [ ] Criterio de aceptación: ¿cómo sabremos que la tarea está correctamente terminada?
- [ ] Fuera de alcance: ¿qué no se debe modificar, agregar o refactorizar?
- [ ] Comandos de verificación: ¿qué validaciones aplican (lint, typecheck, tests)?
- [ ] Contexto persistente: ¿hay documentación, instrucciones o reglas del proyecto que deban revisarse?

Formato de respuesta esperado:

## Plan propuesto

- Objetivo:
- Restricciones:
- Archivos/módulos afectados:
- Enfoque elegido:
  - opción: del análisis + por qué
- Plan mínimo:
  - paso 1
  - paso 2
  - paso 3
- Riesgos:
  - riesgo 1
  - riesgo 2
- Fuera de alcance:
- Criterio de aceptación:
- Comandos de verificación:
- Contexto persistente:

Si falta información para el plan, lista solo las preguntas necesarias para desbloquearlo.
El plan queda pendiente de aprobación del usuario: si sugiere cambios, se ajusta e itera hasta su aprobación; tras la aprobación, el usuario invoca `/check-implementacion`.
