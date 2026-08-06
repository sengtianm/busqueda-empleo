---
description: Check de implementación: aprueba el plan y autoriza la implementación
---

Este check lo invoca el usuario para aprobar el plan e iniciar la implementación. No se implementa nada sin esa autorización.
La tarea queda definida por la solicitud del usuario; el análisis lo aplicó el agente (`check-analisis`) y el plan aprobado viene de `check-planeacion`.

Antes de implementar, confirma que existe un plan aprobado y que el cambio será controlado.
No amplíes el alcance. No refactorices si no se pidió explícitamente. No agregues dependencias sin aprobación.

Si el usuario lo invoca sin un plan aprobado, detente y pide invocar `check-planeacion` antes de continuar.

Verifica y marca cada punto:

- [ ] El plan fue aprobado por el usuario y es la única fuente del cambio; el plan mínimo está definido.
- [ ] El análisis previo fue revisado y es correcto.
- [ ] El objetivo de la tarea sigue siendo claro.
- [ ] El criterio de aceptación del plan está claro y se usará para validar el cambio.
- [ ] Los archivos a modificar están identificados.
- [ ] El cambio propuesto es pequeño y revisable.
- [ ] No se están incluyendo cambios fuera de alcance.
- [ ] No se están modificando archivos innecesarios.
- [ ] No se están agregando dependencias no solicitadas.
- [ ] Se respetan las convenciones del proyecto.
- [ ] Se puede verificar el cambio con tests, lint, build o ejecución.

Instrucción para el agente:

Implementa solo el cambio mínimo aprobado en `check-planeacion`.
Si detectas que necesitas tocar más archivos o ampliar el alcance, detente y explica antes de continuar.

Tras implementar: valida el cambio (lint y typecheck siempre que haya cambios de código; tests solo si la solicitud lo requiere) y aplica el `check-cierre` automáticamente; reporta y espera la aprobación del usuario antes de continuar.

Formato de respuesta esperado:

- Cambio a realizar:
- Archivos a tocar:
- Cambio explícitamente no incluido:
- Forma de verificación:
