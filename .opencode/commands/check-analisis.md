---
description: Check de análisis y alcance antes de ejecutar una tarea
---

Este check lo aplica el agente automáticamente, inmediatamente después de cada solicitud del usuario; no requiere que el usuario lo invoque.
Analiza qué pide la solicitud contra el estado actual del proyecto. No generes código ni un plan formal todavía (ese es el `check-planeacion`).

Verifica y marca cada punto:

- [ ] Tarea interpretada: ¿qué pide la solicitud en una frase? ¿qué queda fuera de alcance?
- [ ] Gate de comprensión: si la solicitud es ambigua, detente el análisis y haz solo preguntas de desbloqueo antes de continuar.
- [ ] Estado del proyecto: ¿qué existe ya en el proyecto para ejecutar esta tarea (archivos, servicios, configuración, prompts, documentación)?
- [ ] Brecha: ¿qué falta para ejecutarla (componentes inexistentes, dependencias ausentes, autorizaciones pendientes)?
- [ ] Impacto: ¿qué cambia en el proyecto (archivos nuevos/modificados y efecto colateral) y qué no se toca?
- [ ] Riesgos: ¿qué podría romper el comportamiento existente o desviar el alcance?
- [ ] Enfoques viables: ¿qué caminos posibles existen? Solo opciones con pros/contras en bruto, sin plan formal.
- [ ] Alcance del análisis: ¿solo se revisó el área que el objetivo pide, sin expandirse?

Formato de respuesta esperado:

1. Tarea interpretada:
   - objetivo:
   - fuera de alcance:

2. Estado del proyecto relevante:
   - qué existe hoy: resumen breve

3. Brecha (qué falta):
   - falta 1
   - falta 2

4. Impacto (qué cambia):
   - cambio 1
   - cambio 2

5. Riesgos:
   - riesgo 1
   - riesgo 2

6. Enfoques viables:
   - opción A: pros/contras resumidos
   - opción B: pros/contras resumidos

7. Decisión mínima:
   - apto para planear: OK / FALTA INFORMACIÓN

Si la solicitud es ambigua o el análisis no es suficiente, detente e indica solo las preguntas necesarias para desbloquearla. No implementes nada aquí.