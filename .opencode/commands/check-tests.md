---
description: Check de tests después de un cambio (solo si la solicitud lo requiere)
---

Lo aplica el agente, solo cuando la solicitud lo amerita (cambio que incluye o afecta tests); no requiere que el usuario lo invoque.
Si la solicitud no requiere tests, se omite; para cambios de código se verifican siempre lint y typecheck.

Después del cambio, verifica que la implementación no introdujo errores y cumple el criterio de aceptación.
No asumas que el código funciona solo porque fue generado.

Sigue la estrategia de testing de AGENTS.md: fixtures en `tests/fixtures/`, tests de integración etiquetados, LLM mockable, SQLite temporal.

Verifica y marca cada punto:

- [ ] Se identificaron los tests relevantes para este cambio.
- [ ] Se ejecutó la suite completa (`pytest tests/`) si es rápida; si solo se corre el subconjunto relevante, se declara en la evidencia.
- [ ] Los tests existentes del área afectada siguen pasando (regresión del área).
- [ ] Se agregó o actualizó algún test si el cambio lo amerita.
- [ ] Se revisaron edge cases básicos.
- [ ] Lint y typecheck pasan, siempre que haya cambios de código.
- [ ] Build o ejecución pasan, si aplican.
- [ ] No aparecen errores nuevos.
- [ ] El comportamiento esperado se cumple.
- [ ] El resultado verifica el criterio de aceptación definido en el plan (`check-planeacion`).

Formato de respuesta esperado:

- Tests ejecutados:
- Tests agregados/modificados:
- Resultado:
- Errores encontrados:
- Cambios adicionales necesarios:
- Evidencia breve:

Si hay errores, resume la causa probable y el siguiente paso mínimo para corregirlos.
No pegues logs completos si no son necesarios.
