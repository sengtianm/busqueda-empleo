---
description: Check de verificación final y cierre antes de cerrar una tarea
---

El agente aplica este check automáticamente al terminar la implementación y su verificación; no requiere que el usuario lo invoque.
Incluye la ejecución de los revisores (code-reviewer y docs-reviewer) como parte de la verificación previa al cierre.

Antes de cerrar la tarea, verifica que el cambio esté completo, revisado y documentado.
No des por terminado el trabajo si quedan puntos abiertos sin registrar.

Verifica y marca cada punto:

- [ ] El criterio de aceptación se cumple.
- [ ] El diff final fue revisado.
- [ ] Los revisores (code-reviewer, docs-reviewer) revisaron el cambio y no quedaron violaciones pendientes.
- [ ] No quedaron cambios accidentales.
- [ ] No se modificaron archivos fuera de alcance.
- [ ] Las pruebas relevantes pasan.
- [ ] No hay errores nuevos visibles.
- [ ] Se actualizó documentación si era necesario.
- [ ] Se registraron tareas pendientes si quedaron abiertas.
- [ ] Existe un resumen claro del cambio.
- [ ] Se definió si conviene continuar en esta conversación o abrir una nueva.

Formato de respuesta esperado:

## Resumen final

- Cambio implementado:
- Archivos modificados:
- Pruebas ejecutadas:
- Resultado:
- Pendientes:
- Riesgos o notas:
- Recomendación para siguiente iteración:

Si algún punto crítico no está completo, no cierres la tarea. Indica exactamente qué falta.