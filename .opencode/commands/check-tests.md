---
description: Check de tests después de un cambio
---

Después del cambio, verifica que la implementación no introdujo errores y cumple el criterio de aceptación.
No asumas que el código funciona solo porque fue generado.

Verifica y marca cada punto:

- [ ] Se identificaron los tests relevantes para este cambio.
- [ ] Se ejecutaron los tests relevantes.
- [ ] Los tests existentes siguen pasando.
- [ ] Se agregó o actualizó algún test si el cambio lo amerita.
- [ ] Se revisaron edge cases básicos.
- [ ] Lint o typecheck pasan, si aplican.
- [ ] Build o ejecución pasan, si aplican.
- [ ] No aparecen errores nuevos.
- [ ] El comportamiento esperado se cumple.

Formato de respuesta esperado:

- Tests ejecutados:
- Resultado:
- Errores encontrados:
- Cambios adicionales necesarios:
- Evidencia breve:

Si hay errores, resume la causa probable y el siguiente paso mínimo para corregirlos.
No pegues logs completos si no son necesarios.