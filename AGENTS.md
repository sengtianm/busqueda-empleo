# AGENTS.md — Automatización de búsqueda de empleo

## Estado del proyecto

**Fase de planificación/documentación.** No hay código implementado. Todo el contenido está en `docs/`. El desarrollo del MVP no comenzará hasta que la documentación sea aprobada (ver `docs/planes/DOC - Plan del proyecto.md`).

## Stack tecnológico (definido, no implementado)

- **Lenguaje:** Python 3.12
- **Sin framework** — arquitectura modular propia
- **Navegador:** Playwright (Chromium)
- **HTML:** BeautifulSoup4 + lxml
- **Validación:** Pydantic v2
- **Logging:** Loguru
- **Fuzzy matching:** RapidFuzz
- **Reintentos:** Tenacity
- **HTTP:** httpx
- **LLM local:** Ollama + Qwen 3.5 4B (evaluación)
- **LLM cloud:** Ollama Cloud + Gemma 4 31B (procesamiento profundo)
- **Persistencia:** .xlsx via openpyxl
- **Config:** PyYAML (config.yaml) + python-dotenv (.env)
- **Deps:** pip + requirements.txt, venv
- **Herramientas:** Black, Ruff, mypy, pytest

## Documentación clave (leer en este orden)

| Doc | Contenido |
|-----|-----------|
| DOC-00 | Glosario del proyecto |
| DOC-01 | Requisitos funcionales |
| DOC-02 | Requisitos no funcionales |
| DOC-03 | Modelo de decisiones |
| DOC-04 | Flujo de datos |
| DOC-05 | Estándares del proyecto |
| DOC-06 | Manejo de errores |
| DOC-07 | Arquitectura de carpetas |
| DOC-08 | Alcance y objetivos |
| DOC-09 | Investigación de fuentes (LinkedIn) |
| DOC-10 | Perfil profesional del usuario |
| DOC-11 | Stack tecnológico |
| DOC-12 | Arquitectura general del sistema |
| DOC-13 | Modelo de datos |
| Anexo 5A | Catálogo de prefijos |
| Anexo 5B | Estándares técnicos oficiales |
| Anexo 5C | Plantillas oficiales |
| Anexo 9A | Decisiones LinkedIn |

## Arquitectura

**Tres niveles:** funcional (módulos de negocio), servicios transversales (shared), infraestructura.

**Flujo de procesamiento (secuencial):**
1. Descubrimiento → 2. Preparación → 3. Evaluación inicial → 4. Procesamiento profundo → 5. Gestión de resultados

**Módulos en `/modules/`:** `descubrimiento/`, `preparacion/`, `evaluacion/`, `procesamiento/`, `gestion/`

**Estructura de directorios planificada:**
```
/
├── docs/
├── config/
├── prompts/
├── modules/
├── shared/
├── data/{entrada,procesamiento,salida,respaldo}/
├── logs/
├── temp/
├── scripts/
├── tests/
└── README.md
```

## Convenciones críticas

- **Idioma:** Documentación y nombres en español. No mezclar idiomas.
- **IDs:** formato `<PREFIJO>-<NÚMERO>` (ej. RF-001, MOD-001, ER-NAV-003). Ver Anexo 5A.
- **Fechas:** `YYYY-MM-DD` ; datetime: `YYYY-MM-DDTHH:mm:ssZ` (ISO 8601, UTC).
- **Versiones:** SemVer (`vMayor.Menor.Corrección`).
- **Documentos:** `DOC-NN - Título.md`.
- **Configuración separada de lógica:** `config.yaml` (funcional) + `.env` (entorno).
- **Prompts separados del código:** en `/prompts/`.
- **Errores:** clasificación `ER-<CATEGORÍA>-<NNN>`, severidad SV-1 a SV-5.

## Reglas de diseño

- Sin valores configurables hardcodeados.
- Sin acceso directo a persistencia desde módulos funcionales — usar servicio compartido.
- Sin dependencias de APIs de terceros para IA — todo local via Ollama.
- Toda transformación preserva el dato original.
- Decisiones automáticas solo basadas en reglas documentadas.
- El usuario retiene todas las decisiones estratégicas.

## Para OpenCode sessions futuras

- **No hay código para ejecutar ni modificar** — el proyecto está en fase de documentación.
- Si necesitas crear código nuevo, respeta la estructura de carpetas de DOC-07, el stack de DOC-11, y los estándares de DOC-05.
- Lee siempre `DOC-00` (Glosario) primero para conocer la terminología exacta.
- Los prefijos de identificadores son obligatorios y están en el Anexo 5A.
- La fuente única de empleo para el MVP es LinkedIn (ver DOC-09).

# Reglas de trabajo para la construcción del MVP

## 1. Propósito

Las presentes reglas establecen la forma de trabajo entre el Usuario, el Arquitecto del Proyecto (ChatGPT) y OpenCode durante la construcción del MVP de la automatización de búsqueda de empleo.

Su objetivo es garantizar un desarrollo controlado, consistente con la documentación oficial del proyecto y con la máxima calidad técnica.

---

# 2. Reglas de planificación

## RT-001. Una tarea a la vez

Solo podrá ejecutarse una única tarea del Plan de ejecución del MVP de manera simultánea.

No se iniciará ninguna tarea nueva hasta finalizar completamente la anterior.

---

## RT-002. Plan obligatorio antes de ejecutar

Antes de realizar cualquier implementación, OpenCode deberá presentar un plan de ejecución específico para la tarea correspondiente.

Ninguna implementación podrá comenzar sin que dicho plan haya sido revisado y aprobado.

---

## RT-003. Respetar el alcance de la tarea

Cada plan deberá limitarse exclusivamente al alcance de la tarea definida en el Plan de ejecución del MVP.

No deberán agregarse actividades, decisiones o implementaciones que pertenezcan a tareas posteriores.

---

# 3. Reglas de revisión

## RT-004. Revisión obligatoria del Arquitecto

Todo plan elaborado por OpenCode deberá ser revisado por el Arquitecto del Proyecto antes de su ejecución.

La aprobación podrá ser:

- Aprobado.
- Aprobado con ajustes.
- Rechazado.

---

## RT-005. No avanzar sin aprobación

OpenCode no podrá ejecutar ninguna tarea hasta recibir aprobación explícita del Arquitecto.

De igual forma, una vez finalizada una tarea, no podrá comenzar la siguiente hasta obtener una nueva aprobación.

---

## RT-006. Ajustes obligatorios

Si durante la revisión se solicitan modificaciones al plan o a la implementación, estas deberán realizarse antes de continuar.

---

# 4. Reglas de implementación

## RT-007. Respetar la documentación oficial

Toda implementación deberá cumplir estrictamente con la documentación oficial del proyecto.

En caso de conflicto entre documentos, OpenCode deberá detener la ejecución e informar la situación antes de implementar cualquier solución.

---

## RT-008. No tomar decisiones de arquitectura

OpenCode no podrá modificar la arquitectura, el flujo del sistema, el modelo de datos, el stack tecnológico ni las decisiones funcionales previamente aprobadas.

Cualquier cambio deberá ser autorizado previamente.

---

## RT-009. No asumir comportamientos

Cuando una implementación requiera información que no exista en la documentación oficial, OpenCode deberá solicitar la decisión correspondiente antes de continuar.

Nunca deberá completar vacíos mediante suposiciones.

---

## RT-010. Mantener el alcance aprobado

Durante la implementación no deberán incorporarse mejoras, optimizaciones o funcionalidades adicionales que no hagan parte de la tarea en ejecución.

---

# 5. Reglas de validación

## RT-011. Validación obligatoria

Toda tarea que implique implementación deberá completar satisfactoriamente el proceso de validación definido para el proyecto antes de considerarse terminada.

---

## RT-012. Reporte de resultados

Al finalizar una tarea, OpenCode deberá presentar un resumen indicando como mínimo:

- Objetivo ejecutado.
- Archivos creados o modificados.
- Resultado obtenido.
- Validaciones realizadas.
- Problemas encontrados (si existen).

---

## RT-013. Declaración explícita de finalización

Toda tarea deberá finalizar indicando expresamente uno de los siguientes estados:

- Tarea completada.
- Tarea completada con observaciones.
- Tarea bloqueada.

---

# 6. Reglas de comunicación

## RT-014. Informar desviaciones

Si durante la ejecución se identifica una inconsistencia documental, un riesgo técnico o una dependencia no prevista, OpenCode deberá detener la ejecución e informar la situación antes de continuar.

---

## RT-015. Justificar propuestas de cambio

Toda propuesta de modificación deberá incluir:

- Problema identificado.
- Justificación técnica.
- Impacto esperado.
- Documentos afectados.

---

## RT-016. No modificar documentación por iniciativa propia

OpenCode únicamente podrá crear o modificar documentación cuando la tarea correspondiente lo requiera o exista una instrucción explícita para hacerlo.

---

# 7. Regla general

## RT-017. Prioridad de la documentación oficial

Ante cualquier duda o conflicto, prevalecerá siempre la documentación oficial aprobada del proyecto sobre cualquier interpretación, recomendación o criterio de implementación.

---

## RT-018. Una sesión por día calendario

Cada día calendario corresponde a una única entrada en `Historial de sesiones.md`. No pueden existir múltiples entradas de sesión en la misma fecha.

---

## RT-019. Actualización automática de sesión en modo build

Al finalizar cada tarea del MVP ejecutada en modo build, OpenCode deberá verificar la fecha actual y actualizar la sesión del día en `Historial de sesiones.md` (o crearla si no existe), registrando los temas tratados, decisiones, acuerdos y estado al cierre. El número de sesión se incrementa secuencialmente por día.

---

## RT-020. Formato de fecha en historial de sesiones

Todas las fechas en las entradas de `Historial de sesiones.md` deben usar el formato `DD/MM/YYYY`.

---

## RT-021. Detalle completo en historial de sesiones

Todas las entradas de `Historial de sesiones.md` deben contener información suficientemente detallada en cada campo (Temas tratados, Decisiones, Acuerdos, Estado al cierre) para que una sesión futura pueda recuperar el contexto completo sin ambigüedad.

No se puede eliminar ni resumir información de sesiones pasadas. El historial es acumulativo y debe preservar íntegramente lo registrado.

---

## RT-022. Cada campo del historial solo refleja la sesión actual

Los campos **Acuerdos** y **Estado al cierre** de cada entrada deben contener únicamente información correspondiente a esa sesión, sin repetir ni arrastrar acuerdos o estados de sesiones anteriores.

Para referenciar continuidad, basta una línea como *"Se mantienen los acuerdos de sesiones anteriores"*. El cierre debe reflejar exclusivamente qué cambió o avanzó en la sesión que termina.

# Criterio de aceptación para las tareas del MVP

## 1. Propósito

El presente criterio de aceptación establece las condiciones mínimas que deberá cumplir cada tarea del Plan de ejecución del MVP antes de considerarse finalizada y permitir el inicio de la siguiente.

Ninguna tarea podrá darse por completada mientras exista al menos uno de estos criterios sin cumplir.

---

# CA-001. Alcance cumplido

La implementación deberá cumplir completamente el objetivo definido para la tarea correspondiente.

No deberán quedar actividades parcialmente implementadas.

---

# CA-002. Respeto de la documentación oficial

La solución implementada deberá ser consistente con toda la documentación oficial del proyecto.

No deberá contradecir:

- Requisitos funcionales.
- Requisitos no funcionales.
- Modelo de decisiones.
- Flujo de datos.
- Estándares.
- Manejo de errores.
- Arquitectura.
- Modelo de datos.
- Stack tecnológico.
- Demás documentos oficiales.

---

# CA-003. Ubicación correcta

Todo archivo creado o modificado deberá respetar la arquitectura de carpetas y las convenciones oficiales del proyecto.

---

# CA-004. Calidad del código

El código deberá:

- Ser legible.
- Ser consistente con los estándares del proyecto.
- Evitar duplicación innecesaria.
- Mantener responsabilidades claramente definidas.
- No incorporar código muerto ni experimental.

---

# CA-005. Validación técnica

Cuando aplique, la implementación deberá superar satisfactoriamente las siguientes validaciones:

- `ruff check .`
- `mypy .`
- `pytest tests/`

No deberán existir errores pendientes antes de considerar finalizada la tarea.

---

# CA-006. Validación funcional

La funcionalidad implementada deberá comportarse exactamente como fue especificada para la tarea correspondiente.

No deberá presentar errores funcionales conocidos.

---

# CA-007. Ausencia de regresiones

La implementación no deberá afectar funcionalidades previamente aprobadas.

Cuando corresponda, deberán ejecutarse las pruebas necesarias para verificarlo.

---

# CA-008. Documentación actualizada

Cuando la tarea implique documentación, esta deberá quedar actualizada, consistente y alineada con la implementación realizada.

---

# CA-009. Reporte de ejecución

Al finalizar cada tarea deberá entregarse un reporte indicando como mínimo:

- Objetivo ejecutado.
- Actividades realizadas.
- Archivos creados.
- Archivos modificados.
- Validaciones ejecutadas.
- Resultado de cada validación.
- Problemas encontrados.
- Riesgos identificados.
- Observaciones relevantes.

---

# CA-010. Revisión del Arquitecto

Toda implementación deberá ser revisada por el Arquitecto del Proyecto.

La revisión podrá producir uno de los siguientes resultados:

- Aprobada.
- Aprobada con ajustes.
- Rechazada.

---

# CA-011. Aprobación final

Una tarea únicamente podrá considerarse completada cuando:

- Todos los criterios anteriores hayan sido cumplidos.
- El Arquitecto del Proyecto haya emitido una aprobación explícita.

Hasta ese momento, la tarea permanecerá abierta y no podrá iniciarse la siguiente actividad del Plan de ejecución del MVP.

# Estrategia oficial de pruebas del MVP

## 1. Propósito

La presente estrategia define el conjunto de pruebas que deberán aplicarse durante la construcción del MVP de la automatización de búsqueda de empleo.

Su objetivo es garantizar que cada implementación sea correcta, estable, verificable y consistente con la documentación oficial del proyecto.

---

# 2. Principios generales

## EP-001. Calidad antes que velocidad

Ninguna tarea se considerará finalizada sin haber sido validada mediante las pruebas que le correspondan.

---

## EP-002. Proporcionalidad

No todas las tareas requieren el mismo nivel de pruebas.

Cada tarea deberá ejecutar únicamente las pruebas que correspondan según su naturaleza.

---

## EP-003. Automatización

Siempre que sea posible, las pruebas deberán ejecutarse automáticamente.

Las validaciones manuales únicamente se utilizarán cuando la naturaleza de la funcionalidad lo requiera.

---

## EP-004. Independencia

Cada prueba deberá poder ejecutarse de forma independiente sin depender del resultado de otras pruebas.

---

## EP-005. Reproducibilidad

Una prueba deberá producir el mismo resultado cuando se ejecute bajo las mismas condiciones.

---

# 3. Tipos de pruebas

## EP-101. Pruebas unitarias

### Objetivo

Validar componentes individuales de forma aislada.

### Aplican para

- Lógica de negocio.
- Reglas.
- Validaciones.
- Transformaciones.
- Utilidades.
- Servicios compartidos.
- Modelos.

### Herramienta

- pytest

### Recursos

- Fixtures ubicados en:

```text
tests/fixtures/
```

---

## EP-102. Pruebas de integración

### Objetivo

Validar la interacción entre módulos y componentes reales.

### Aplican para

- Navegación web.
- Integración con LinkedIn.
- Persistencia.
- Flujo entre módulos.
- Orquestación.

### Herramientas

- Playwright
- pytest

### Convención

Todas deberán etiquetarse como:

```python
@pytest.mark.integration
```

---

## EP-103. Pruebas del motor de IA

### Objetivo

Validar el comportamiento del servicio de IA y de los prompts.

### Alcance

- Comunicación con Ollama.
- Validación del formato de respuesta.
- Parseo.
- Manejo de errores.
- Reintentos.

### Estrategia

Las pruebas unitarias deberán utilizar respuestas simuladas (mocks).

Las pruebas manuales utilizarán Ollama local.

---

## EP-104. Pruebas de persistencia

### Objetivo

Validar todas las operaciones sobre archivos Excel.

### Alcance

- Lectura.
- Escritura.
- Actualización.
- Búsquedas.
- Integridad de datos.

### Estrategia

Todas las pruebas deberán utilizar archivos temporales.

Nunca deberán modificar los archivos reales del proyecto.

---

## EP-105. Pruebas funcionales

### Objetivo

Verificar que la funcionalidad implementada cumple exactamente con el comportamiento esperado.

Estas pruebas podrán ser automáticas o manuales dependiendo de la naturaleza de la tarea.

---

# 4. Cuándo ejecutar cada prueba

## EP-201. Cambios de lógica

Obligatorio ejecutar:

- Ruff.
- MyPy.
- Pruebas unitarias.

---

## EP-202. Cambios de integración

Obligatorio ejecutar:

- Ruff.
- MyPy.
- Pruebas unitarias.
- Pruebas de integración.

---

## EP-203. Cambios relacionados con IA

Obligatorio ejecutar:

- Ruff.
- MyPy.
- Pruebas unitarias.
- Validación manual con Ollama.

---

## EP-204. Cambios en persistencia

Obligatorio ejecutar:

- Ruff.
- MyPy.
- Pruebas unitarias.
- Pruebas sobre archivos temporales.

---

## EP-205. Cambios exclusivamente documentales

No requieren ejecución de pruebas técnicas.

Únicamente requieren revisión documental.

---

# 5. Validaciones obligatorias

Toda tarea que incluya implementación de código deberá ejecutar como mínimo:

```bash
ruff check .
```

```bash
mypy .
```

Y las pruebas correspondientes según la naturaleza de la tarea.

---

# 6. Manejo de fallos

## EP-301. Fallo de validación

Si cualquiera de las validaciones obligatorias falla:

- La tarea no podrá considerarse terminada.
- No podrá iniciarse la siguiente tarea.
- Deberán corregirse los errores antes de solicitar aprobación.

---

## EP-302. Regresiones

Si una implementación rompe una funcionalidad previamente aprobada:

- La regresión tendrá prioridad sobre el desarrollo de nuevas funcionalidades.
- Deberá corregirse antes de continuar.

---

# 7. Evidencias de ejecución

Al finalizar cada tarea, OpenCode deberá indicar:

- Pruebas ejecutadas.
- Resultado de cada prueba.
- Validaciones omitidas (si aplica).
- Justificación de cualquier prueba no ejecutada.

---

# 8. Criterio final

Una tarea únicamente podrá considerarse validada cuando:

- Se hayan ejecutado todas las pruebas obligatorias para esa tarea.
- Todas las pruebas obligatorias hayan sido satisfactorias.
- No existan regresiones conocidas.
- El Arquitecto del Proyecto apruebe el resultado final.
