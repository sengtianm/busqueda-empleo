---
name: review-against-documentation
description: Use this skill whenever reviewing an implementation against the project's official documentation, architecture, requirements, backlog, or design decisions.
---

## Purpose

Verificar que una implementación coincida con la documentación oficial del proyecto. Detectar inconsistencias entre implementación y: requisitos documentados, decisiones de arquitectura, reglas de negocio, workflows, modelo de datos y estándares.

## Applicability

**Usar para:** revisar trabajo completado, validar implementaciones terminadas, comparar código contra documentación, verificar cumplimiento de decisiones de arquitectura, revisar tareas del backlog, confirmar respeto a requisitos documentados.

**No usar para:** debugging, implementación de código, refactorizaciones no solicitadas, proponer mejoras no documentadas, tomar decisiones de diseño sin respaldo documental, revisión exploratoria sin documentación aplicable.

## Required Inputs

Antes de revisar, identificar:

- Alcance: tarea, ticket, feature, módulo, PR o commit
- Implementación: archivos, módulos, endpoints, componentes o cambios
- Documentación aplicable: arquitectura, modelo de datos, workflow, estándares, decisiones de diseño, backlog, requisitos funcionales/técnicos
- Criterios de aceptación (si existen)

**Si falta información mínima:** indicar qué falta, qué no puede validarse y qué documentación/aclaración se necesita. No completar vacíos con suposiciones.

## Documentation Precedence

Orden de prioridad:

1. Architecture Decision Records / decisiones explícitas de diseño
2. Documentación de arquitectura
3. Documentación de modelo de datos
4. Documentación de workflow, flujos o procesos
5. Requisitos de backlog, tickets o tareas
6. Estándares de código, naming o convenciones
7. Otra documentación de soporte

**Ante contradicción entre documentos:** no elegir silenciosamente; reportar como `Documentation Conflict`; indicar cuál prevalece según jerarquía; solicitar aclaración si el conflicto impide validar.

## Review Workflow

1. **Identificar implementación:** archivos modificados/relevantes, módulos afectados, interfaces/endpoints/componentes/servicios, alcance real del cambio.
2. **Identificar documentación aplicable:** arquitectura, modelo de datos, workflows, reglas de negocio, estándares, decisiones de diseño, backlog/requisitos, cualquier documento relevante al alcance.
3. **Aplicar jerarquía documental:** determinar qué documentos aplican, detectar conflictos, identificar vacíos o ambigüedades.
4. **Comparar implementación vs documentación:** comportamiento funcional, reglas de negocio, responsabilidades de módulos, interfaces y contratos, modelo de datos, workflow esperado, naming (si documentado), restricciones técnicas/funcionales, decisiones de arquitectura.
5. **Detectar inconsistencias:** funcionalidad faltante, funcionalidad extra no documentada, violaciones de arquitectura, suposiciones incorrectas, desajustes documentación-implementación, documentación desactualizada/ambigua/incompleta.
6. **No proponer mejoras no documentadas:** la revisión no es refactorización; no recomendar cambios por preferencias personales; solo reportar desviaciones frente a documentación vigente.
7. **Producir revisión:** clasificar cada hallazgo, explicar razón, referenciar documento, incluir evidencia en código, indicar acción recomendada.

## Finding Categories

| Category | Definition |
|---|---|
| `Compliant` | Implementación cumple con documentación |
| `Non-compliant` | Implementación contradice documentación |
| `Missing` | Falta implementación requerida por documentación |
| `Extra` | Existe implementación no contemplada en documentación |
| `Risk` | Riesgo funcional/técnico/arquitectónico ligado a requisito documentado |
| `Documentation Gap` | Falta documentación necesaria para validar |
| `Documentation Conflict` | Dos documentos se contradicen |
| `Documentation Issue` | Implementación puede ser correcta pero documentación está desactualizada/incompleta/ambigua |
| `Unable to Validate` | Información insuficiente para determinar cumplimiento |

## Severity Levels

| Severity | Definition |
|---|---|
| `Blocker` | Viola decisión de arquitectura, regla de negocio, restricción crítica o requisito documentado. Impide aprobar |
| `Major` | Desviación funcional con impacto material |
| `Minor` | Desviación de bajo impacto (naming, estructura) si está documentada |
| `Info` | Observación informativa sin violación documental |
| `Documentation Issue` | Problema en documentación, no necesariamente en código |

## Mandatory Rules

**Siempre:**

- Documentación como fuente de verdad
- Explicar y referenciar cada hallazgo con documento que lo respalda
- Citar evidencia concreta en implementación
- Distinguir hechos de suposiciones
- Reportar vacíos y conflictos documentales
- Recomendar actualización de documentación cuando implementación correcta no esté documentada
- Esperar aprobación del usuario antes de proponer cambios de implementación

**Nunca:**

- Inventar requisitos
- Recomendar cambios no documentados
- Ignorar decisiones de arquitectura
- Asumir comportamiento no documentado
- Marcar `Non-compliant` sin referencia documental
- Completar vacíos documentales con opiniones personales
- Proponer implementación de código como acción automática
- Ocultar incertidumbre cuando no se pueda validar

## Output Format

La revisión debe responder: **¿la implementación coincide con la documentación oficial del proyecto?** Si no hay documentación suficiente, indicar explícitamente qué no puede validarse y qué información falta.

```markdown
# Documentation Compliance Review

## Summary
Qué se revisó, qué documentación se usó, resultado general, principales riesgos o bloqueos.

## Compliance Status
[Compliant / Partially Compliant / Non-compliant / Unable to Validate]

## Findings

### F-001
- Severity: [Blocker / Major / Minor / Info / Documentation Issue]
- Category: [Compliant / Non-compliant / Missing / Extra / Risk / Documentation Gap / Documentation Conflict / Documentation Issue / Unable to Validate]
- Description: [Descripción clara del hallazgo]
- Evidence in code: [Archivo, función, endpoint, línea o fragmento relevante]
- Documentation reference: [Documento, sección o requisito]
- Recommended action: [Acción recomendada]

## Documentation References
- [Documento 1]
- [Documento 2]

## Required Corrections
Solo correcciones justificadas por documentación. Cada una indica: qué corregir, por qué está mal según documentación, qué documento lo exige, si es corrección de código o de documentación. Si requiere cambios de implementación: listar como propuesta y esperar aprobación explícita antes de ejecutar o generar código.

## Documentation Updates Needed
Indicar si la documentación debe actualizarse por: implementación correcta no documentada, documentación desactualizada, ambigüedad o conflictos entre documentos.

## Open Questions / Clarifications Needed
Preguntas necesarias por: documentación ambigua, información faltante, conflictos documentales, comportamiento no validable o decisión requerida del usuario/equipo.
```

Hallazgos sin respaldo documental deben marcarse como `Documentation Gap`, `Unable to Validate` o `Documentation Conflict` según corresponda.