---
description: Actualiza la sesión del día en Historial de sesiones.md
---

Actualiza (o crea si no existe) la entrada del día actual en `Historial de sesiones.md`.

Reglas:

- Solo existe **una sesión por día calendario**. Si ya hay una entrada con la fecha de hoy, se actualiza; si no, se crea una nueva.
- El número de sesión se incrementa secuencialmente: es el último número existente + 1.
- La fecha debe usar formato `DD/MM/YYYY` (sin hora).
- Los campos a registrar son: **Temas tratados**, **Decisiones**, **Acuerdos**, **Estado al cierre**.
- El contenido debe ser **suficientemente detallado** en cada campo para que una sesión futura recupere el contexto completo sin ambigüedad.
- No se puede eliminar ni resumir información de sesiones pasadas. El historial es acumulativo.
- **Acuerdos** y **Estado al cierre** deben contener únicamente información de la sesión actual, sin repetir datos de sesiones anteriores. Para referenciar continuidad basta una línea como *"Se mantienen los acuerdos de sesiones anteriores"*.
- El contenido se deduce de la conversación que acaba de ocurrir.
- Si algo no está claro, preguntar antes de escribir.
- Después de actualizar el historial, actualizar también `Seguimiento MVP.md` si alguna tarea cambió de estado durante la sesión.
