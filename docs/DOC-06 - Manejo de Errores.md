# Documento 6 - Manejo de Errores

## 1. Propósito del documento

El presente documento define el modelo oficial para la detección, clasificación, registro, tratamiento, recuperación y seguimiento de los errores que puedan presentarse durante el funcionamiento de la automatización de búsqueda de empleo.

Su propósito es establecer un conjunto uniforme de principios, reglas y procedimientos que permitan gestionar los fallos de manera controlada, minimizando su impacto sobre la continuidad de los procesos, la integridad de la información y la experiencia del usuario.

Este documento constituye la referencia oficial para el manejo de errores en todos los módulos, procesos, componentes, servicios, integraciones, flujos de datos y recursos que conforman la automatización, independientemente de la tecnología utilizada para su implementación.

Asimismo, define los lineamientos necesarios para garantizar que todos los errores sean detectados oportunamente, registrados de forma consistente, clasificados según su severidad, tratados mediante estrategias de recuperación previamente establecidas y conservados para fines de auditoría, trazabilidad y mejora continua del sistema.

Las disposiciones contenidas en este documento serán de cumplimiento obligatorio para todos los componentes de la automatización y para cualquier desarrollo, modificación o ampliación futura que pueda introducir nuevas condiciones de error o mecanismos de recuperación.

---

# 2. Principios del manejo de errores

Los siguientes principios establecen las reglas generales que deberán regir la detección, clasificación, tratamiento, recuperación y seguimiento de todos los errores que puedan producirse durante el funcionamiento de la automatización de búsqueda de empleo.

Estos principios complementan el Glosario del Proyecto, los Requisitos Funcionales, los Requisitos No Funcionales, el Modelo de Decisiones, el Flujo de Datos y los Estándares del Proyecto, constituyendo la base normativa para garantizar un manejo uniforme y controlado de cualquier condición de error.

---

### PME-001. Detección oportuna

Todo error deberá detectarse tan pronto como sea posible, evitando que continúe propagándose a otros procesos o componentes del sistema.

---

### PME-002. Registro obligatorio

Todo error detectado deberá registrarse conforme a las convenciones oficiales de auditoría y trazabilidad definidas por el proyecto.

No se permitirá la existencia de errores silenciosos cuya ocurrencia no pueda verificarse posteriormente.

---

### PME-003. Clasificación uniforme

Todo error deberá clasificarse utilizando los criterios oficiales de severidad, origen e impacto definidos en este documento.

No podrán utilizarse clasificaciones alternativas para un mismo tipo de error.

---

### PME-004. Recuperación controlada

Siempre que sea técnicamente posible, el sistema deberá intentar recuperar automáticamente la ejecución mediante los mecanismos de recuperación autorizados.

Cuando la recuperación automática no sea viable, el proceso deberá finalizar de forma controlada.

---

### PME-005. Protección de la integridad

El manejo de errores nunca deberá comprometer la integridad, consistencia o trazabilidad de la información almacenada por la automatización.

---

### PME-006. Continuidad operacional

Los errores deberán aislarse para evitar que un fallo localizado interrumpa innecesariamente otros procesos independientes del sistema.

---

### PME-007. Reproducibilidad

Toda condición de error deberá contener la información suficiente para permitir su análisis, reproducción e investigación posterior.

---

### PME-008. Trazabilidad

Todo error deberá poder relacionarse con el proceso, módulo, componente, oferta, operación o recurso donde fue detectado.

---

### PME-009. Independencia tecnológica

Las reglas de manejo de errores deberán mantenerse independientes de cualquier lenguaje de programación, herramienta, proveedor o plataforma tecnológica.

---

### PME-010. Recuperación segura

Ningún mecanismo de recuperación podrá provocar pérdida de información, duplicidad de registros o alteración del flujo lógico definido para la automatización.

---

### PME-011. Escalabilidad

El modelo de manejo de errores deberá permitir incorporar nuevos tipos de errores, mecanismos de recuperación y fuentes de fallo sin modificar la estructura general del sistema.

---

### PME-012. Consistencia documental

Las reglas establecidas en este documento deberán mantenerse alineadas con toda la documentación oficial del proyecto.

Ningún procedimiento de manejo de errores podrá contradecir los documentos previamente aprobados.

---

### PME-013. Intervención mínima del usuario

Siempre que sea posible, la recuperación de errores deberá realizarse automáticamente, reduciendo al mínimo la necesidad de intervención del usuario.

Cuando dicha intervención sea necesaria, el sistema deberá proporcionar información suficiente para facilitar la toma de decisiones.

---

### PME-014. Auditabilidad

Todo el ciclo de vida de un error, desde su detección hasta su resolución, deberá poder ser auditado mediante los registros generados por la automatización.

---

### PME-015. Evolución controlada

Toda modificación al modelo de manejo de errores deberá documentarse previamente, justificarse y preservar la compatibilidad con los mecanismos existentes siempre que sea posible.

---

## Principios generales del manejo de errores

El manejo de errores deberá cumplir los siguientes principios:

- Detectar los errores de forma oportuna.
- Registrar todos los errores sin excepciones.
- Clasificar los errores de manera uniforme.
- Favorecer la recuperación automática cuando sea posible.
- Proteger la integridad y consistencia de la información.
- Garantizar la continuidad operacional.
- Mantener la trazabilidad completa del ciclo de vida de cada error.
- Facilitar la auditoría y el análisis posterior.
- Mantener independencia tecnológica.
- Permitir la evolución y escalabilidad del sistema.

---

# 3. Arquitectura del manejo de errores

La arquitectura del manejo de errores define el modelo conceptual mediante el cual la automatización detecta, clasifica, registra, trata, recupera y finaliza cualquier condición de error que pueda producirse durante la ejecución de sus procesos.

Su propósito es garantizar que todos los módulos del sistema respondan de forma uniforme ante los fallos, independientemente de su origen o naturaleza, preservando la continuidad operacional, la integridad de los datos y la trazabilidad completa del incidente.

La arquitectura de manejo de errores será aplicable a todos los procesos de la automatización, incluyendo los módulos de descubrimiento de oportunidades, preparación inicial de ofertas, evaluación inicial, procesamiento de ofertas, almacenamiento de información y cualquier componente que se incorpore en el futuro.

---

## Componentes del modelo de manejo de errores

La arquitectura estará compuesta por las siguientes etapas secuenciales:

### AME-01. Detección

Identificar la ocurrencia de una condición anómala o un comportamiento diferente al esperado durante la ejecución de un proceso.

---

### AME-02. Clasificación

Determinar el tipo, origen, severidad e impacto del error conforme a las reglas definidas en este documento.

---

### AME-03. Registro

Registrar toda la información necesaria para garantizar la trazabilidad, auditoría y análisis posterior del error.

El registro deberá realizarse antes de ejecutar cualquier acción de recuperación.

---

### AME-04. Evaluación

Determinar si el error puede resolverse automáticamente o si requiere la intervención de otro proceso o del usuario.

Esta evaluación deberá realizarse utilizando las políticas oficiales de recuperación.

---

### AME-05. Recuperación

Ejecutar la estrategia de recuperación correspondiente cuando exista un mecanismo autorizado para ello.

La recuperación podrá incluir, entre otras acciones:

- Reintentos.
- Reinicio controlado del proceso.
- Reejecución de una operación.
- Omisión controlada de una etapa.
- Continuación segura del flujo.
- Finalización controlada del proceso.

---

### AME-06. Validación

Verificar que la recuperación ejecutada haya resuelto correctamente la condición de error.

En caso contrario, el error deberá continuar con el proceso de escalamiento definido por el sistema.

---

### AME-07. Escalamiento

Cuando la recuperación automática no sea posible o resulte insuficiente, el error deberá escalarse conforme a las reglas establecidas para su nivel de severidad.

El escalamiento podrá implicar:

- Nuevos intentos de recuperación.
- Intervención de otro componente.
- Intervención del usuario.
- Finalización controlada del proceso.

---

### AME-08. Cierre

Finalizar formalmente la gestión del error una vez que la condición haya sido resuelta o el proceso haya concluido de forma controlada.

El cierre deberá conservar toda la información histórica generada durante el tratamiento del error.

---

### AME-09. Auditoría

Toda la información relacionada con el error permanecerá disponible para auditorías, análisis estadísticos, investigaciones técnicas y mejoras futuras del sistema.

---

## Flujo general del manejo de errores

Todo error identificado dentro de la automatización deberá seguir el siguiente flujo lógico:

1. Detectar el error.
2. Clasificar el error.
3. Registrar el incidente.
4. Evaluar la estrategia de recuperación.
5. Ejecutar la recuperación cuando corresponda.
6. Validar el resultado de la recuperación.
7. Escalar el error si la recuperación falla.
8. Cerrar el incidente.
9. Conservar toda la información para auditoría y trazabilidad.

---

## Alcance de la arquitectura

La arquitectura definida en este documento será obligatoria para todos los módulos y componentes de la automatización.

Ningún componente podrá implementar un flujo alternativo de manejo de errores que contradiga las etapas aquí establecidas, salvo que exista una excepción expresamente documentada y aprobada como parte de la documentación oficial del proyecto.

---

# 4. Clasificación de errores

La clasificación de errores establece el modelo oficial para identificar, categorizar y administrar todas las condiciones de error que puedan presentarse durante la ejecución de la automatización de búsqueda de empleo.

Su propósito es garantizar que todos los errores sean tratados de manera uniforme, facilitando su identificación, priorización, recuperación, auditoría y análisis estadístico.

Cada error deberá pertenecer a una única categoría principal y conservar dicha clasificación durante todo su ciclo de vida.

---

## Criterios de clasificación

Todo error deberá clasificarse utilizando los siguientes criterios:

### CE-001. Origen

Identifica el componente o recurso donde se produjo el error.

---

### CE-002. Naturaleza

Describe el tipo de fallo ocurrido.

---

### CE-003. Severidad

Determina el impacto operativo que produce el error sobre la automatización.

---

### CE-004. Recuperabilidad

Indica si el error puede resolverse automáticamente o requiere intervención adicional.

---

### CE-005. Persistencia

Determina si el error es temporal o permanente.

---

### CE-006. Alcance

Indica si el error afecta únicamente una operación específica o compromete procesos adicionales del sistema.

---

## Categorías oficiales de errores

Las siguientes categorías constituyen la clasificación oficial de errores del proyecto.

### CER-001. Errores de red (ER-RED)

Errores relacionados con problemas de conectividad, disponibilidad de servicios, tiempos de espera o fallos de comunicación entre componentes.

Ejemplos:

- Pérdida de conexión.
- Timeout.
- DNS no disponible.
- Servicio remoto inaccesible.

---

### CER-002. Errores del navegador (ER-NAV)

Errores producidos durante la automatización del navegador.

Ejemplos:

- Página no cargada.
- Elemento inexistente.
- Captcha.
- Cambio inesperado del DOM.
- Sesión expirada.

---

### CER-003. Errores de extracción (ER-EXT)

Errores durante la obtención de información desde una fuente de empleo.

Ejemplos:

- Información incompleta.
- Selectores inválidos.
- Datos no encontrados.
- Contenido inaccesible.

---

### CER-004. Errores de validación (ER-VAL)

Errores detectados durante la validación de la información procesada.

Ejemplos:

- Campos obligatorios ausentes.
- Formatos inválidos.
- Datos inconsistentes.
- Valores fuera de rango.

---

### CER-005. Errores del modelo de lenguaje (ER-LLM)

Errores relacionados con el procesamiento realizado por el modelo de lenguaje.

Ejemplos:

- Respuesta vacía.
- Respuesta inválida.
- Salida con formato incorrecto.
- Tiempo de respuesta excedido.
- Imposibilidad de interpretar el contenido.

---

### CER-006. Errores de datos (ER-DAT)

Errores relacionados con la integridad, consistencia o estructura de la información utilizada por la automatización.

Ejemplos:

- Datos corruptos.
- Datos duplicados.
- Datos incompatibles.
- Relaciones inconsistentes.

---

### CER-007. Errores de persistencia (ER-DB)

Errores ocurridos durante el almacenamiento o recuperación de información.

Ejemplos:

- Escritura fallida.
- Lectura fallida.
- Archivo inaccesible.
- Recurso bloqueado.

---

### CER-008. Errores de configuración (ER-CFG)

Errores ocasionados por configuraciones incorrectas o incompletas del sistema.

Ejemplos:

- Parámetros inexistentes.
- Variables obligatorias ausentes.
- Configuración incompatible.

---

### CER-009. Errores internos (ER-INT)

Errores producidos por el funcionamiento interno de la automatización.

Ejemplos:

- Excepciones no controladas.
- Estados inválidos.
- Flujo inconsistente.
- Dependencias no satisfechas.

---

### CER-010. Errores externos (ER-EXTS)

Errores ocasionados por servicios, plataformas o recursos externos sobre los cuales la automatización no posee control directo.

Ejemplos:

- API fuera de servicio.
- Cambios en plataformas de empleo.
- Restricciones temporales del proveedor.
- Mantenimiento del servicio.

---

## Convención oficial de identificadores

Todos los errores registrados deberán utilizar el siguiente formato:

```
ER-<CATEGORÍA>-<NÚMERO_SECUENCIAL>
```

Ejemplos:

- ER-RED-001
- ER-NAV-003
- ER-EXT-015
- ER-VAL-002
- ER-LLM-004
- ER-DAT-007
- ER-DB-001
- ER-CFG-002
- ER-INT-009
- ER-EXTS-003

Cada identificador será único, inmutable y reutilizable únicamente como referencia histórica del error correspondiente.

---

## Reglas generales

- Todo error deberá pertenecer a una única categoría principal.
- Todo error deberá poseer un identificador oficial.
- La categoría de un error no podrá modificarse una vez registrado.
- Las nuevas categorías únicamente podrán incorporarse mediante una actualización oficial de este documento.
- Ningún componente podrá utilizar clasificaciones distintas a las aquí definidas.

---

# 5. Fuentes de error

Las fuentes de error representan todos los orígenes desde los cuales puede generarse una condición de fallo durante la ejecución de la automatización de búsqueda de empleo.

Su identificación permite diseñar mecanismos preventivos, estrategias de recuperación y controles específicos para minimizar el impacto operativo de cada tipo de incidente.

Las fuentes de error definidas en este documento constituyen el catálogo oficial de orígenes potenciales de fallos y deberán utilizarse como referencia para el diseño, implementación, monitoreo y mantenimiento de la automatización.

---

## Clasificación de las fuentes de error

### FDE-001. Fuentes internas

Corresponden a errores originados por componentes propios de la automatización.

Incluyen, entre otros:

- Lógica de negocio.
- Flujos de procesamiento.
- Reglas de decisión.
- Procesos internos.
- Estados inconsistentes.
- Errores de programación.
- Excepciones no controladas.

---

### FDE-002. Fuentes de infraestructura

Corresponden a errores relacionados con el entorno donde se ejecuta la automatización.

Incluyen, entre otros:

- Sistema operativo.
- Recursos del equipo.
- Permisos.
- Espacio de almacenamiento.
- Procesos del sistema.
- Fallos del entorno de ejecución.

---

### FDE-003. Fuentes de red

Corresponden a problemas de comunicación entre la automatización y recursos externos.

Incluyen, entre otros:

- Pérdida de conectividad.
- Alta latencia.
- Timeout.
- DNS.
- Interrupciones del servicio.
- Restricciones temporales de acceso.

---

### FDE-004. Fuentes del navegador

Corresponden a errores producidos durante la automatización del navegador.

Incluyen, entre otros:

- Cambios en la interfaz.
- Elementos inexistentes.
- Captchas.
- Ventanas inesperadas.
- Sesiones expiradas.
- Recursos bloqueados.

---

### FDE-005. Fuentes de extracción

Corresponden a errores durante la obtención de información desde las plataformas de empleo.

Incluyen, entre otros:

- Información incompleta.
- Estructuras modificadas.
- Contenido dinámico.
- Datos inaccesibles.
- Cambios en selectores.
- Información inconsistente.

---

### FDE-006. Fuentes del modelo de lenguaje

Corresponden a errores producidos durante el procesamiento realizado por el modelo de lenguaje.

Incluyen, entre otros:

- Respuestas inválidas.
- Información insuficiente.
- Formatos inesperados.
- Errores de interpretación.
- Tiempo de respuesta excedido.
- Fallos de comunicación con el servicio.

---

### FDE-007. Fuentes de datos

Corresponden a errores relacionados con la información utilizada por la automatización.

Incluyen, entre otros:

- Datos incompletos.
- Registros duplicados.
- Inconsistencias.
- Formatos incompatibles.
- Relaciones inválidas.
- Información corrupta.

---

### FDE-008. Fuentes de persistencia

Corresponden a errores durante el almacenamiento o recuperación de información.

Incluyen, entre otros:

- Escrituras fallidas.
- Lecturas fallidas.
- Archivos inexistentes.
- Recursos bloqueados.
- Fallos de sincronización.
- Problemas de acceso.

---

### FDE-009. Fuentes de configuración

Corresponden a errores originados por configuraciones incorrectas del sistema.

Incluyen, entre otros:

- Parámetros inexistentes.
- Configuración incompleta.
- Variables obligatorias ausentes.
- Configuraciones incompatibles.
- Valores inválidos.

---

### FDE-010. Fuentes del usuario

Corresponden a errores provocados por acciones, decisiones o configuraciones realizadas por el usuario.

Incluyen, entre otros:

- Configuración incorrecta.
- Información incompleta.
- Parámetros inconsistentes.
- Interrupción manual del proceso.
- Decisiones incompatibles con el estado actual.

---

### FDE-011. Fuentes externas

Corresponden a errores originados por servicios, plataformas o recursos que no forman parte de la automatización.

Incluyen, entre otros:

- Plataformas de empleo.
- APIs externas.
- Servicios de autenticación.
- Servicios de inteligencia artificial.
- Cambios en proveedores.
- Mantenimientos programados.
- Restricciones impuestas por terceros.

---

### FDE-012. Fuentes desconocidas

Corresponden a errores cuyo origen no puede determinarse inmediatamente durante la ejecución.

Estos errores deberán registrarse con toda la información disponible y permanecer en observación hasta identificar su causa raíz.

---

## Reglas generales

- Todo error deberá poder asociarse al menos a una fuente de error.
- Una misma fuente podrá originar múltiples categorías de errores.
- Una condición de error podrá estar asociada a varias fuentes cuando exista evidencia suficiente.
- Las fuentes de error deberán mantenerse independientes de la tecnología utilizada.
- La incorporación de nuevas fuentes requerirá la actualización oficial de este documento.
- Ningún componente podrá definir fuentes de error incompatibles con las aquí establecidas.

---

# 6. Detección de errores

La detección de errores establece el modelo oficial mediante el cual la automatización identifica cualquier condición anómala que pueda afectar la correcta ejecución de sus procesos.

Su propósito es garantizar que todos los errores sean identificados de forma temprana, consistente y verificable, permitiendo activar oportunamente los mecanismos de clasificación, recuperación, registro y auditoría definidos en este documento.

La detección de errores deberá aplicarse de manera uniforme en todos los módulos, procesos, componentes, integraciones y recursos de la automatización.

---

## Principios de detección

### PDE-001. Detección temprana

Todo error deberá detectarse en la etapa más cercana posible a su origen para evitar la propagación de efectos secundarios sobre otros componentes.

---

### PDE-002. Detección automática

Siempre que sea técnicamente posible, la detección de errores deberá realizarse de forma automática, sin depender de la intervención del usuario.

---

### PDE-003. Detección verificable

Todo error detectado deberá poder demostrarse mediante evidencia objetiva obtenida durante la ejecución del proceso.

---

### PDE-004. Detección continua

La detección de errores deberá mantenerse activa durante todo el ciclo de vida de cada proceso de la automatización.

---

### PDE-005. No interrupción innecesaria

La detección de un error no implicará automáticamente la finalización del proceso.

La continuidad dependerá de las políticas de recuperación definidas para cada tipo de error.

---

## Mecanismos oficiales de detección

### MDE-001. Validaciones preventivas

Se ejecutarán antes de iniciar una operación para verificar que existan las condiciones necesarias para su ejecución.

Ejemplos:

- Existencia de configuraciones obligatorias.
- Disponibilidad de recursos.
- Parámetros válidos.
- Dependencias disponibles.

---

### MDE-002. Validaciones durante la ejecución

Se ejecutarán mientras el proceso se encuentra en funcionamiento.

Ejemplos:

- Verificación de respuestas.
- Confirmación de operaciones.
- Disponibilidad de elementos esperados.
- Estados válidos del proceso.

---

### MDE-003. Validaciones posteriores

Se ejecutarán una vez finalizada una operación para confirmar que el resultado obtenido sea consistente con el esperado.

Ejemplos:

- Confirmación de escritura.
- Verificación de almacenamiento.
- Validación de resultados generados.
- Confirmación de cambios de estado.

---

### MDE-004. Monitoreo continuo

La automatización deberá supervisar permanentemente el estado de los procesos críticos durante su ejecución.

El monitoreo podrá detectar, entre otros:

- Interrupciones inesperadas.
- Procesos detenidos.
- Consumo anormal de recursos.
- Comportamientos inconsistentes.

---

### MDE-005. Detección por tiempos de espera

Cuando una operación supere el tiempo máximo permitido definido por la automatización, deberá generarse una condición de error.

Esta validación será aplicable tanto a procesos internos como a recursos externos.

---

### MDE-006. Validación de integridad de datos

Toda información recibida, transformada, almacenada o recuperada deberá verificarse para garantizar su integridad y consistencia.

---

### MDE-007. Validación de respuestas del modelo de lenguaje

Toda respuesta generada por el modelo de lenguaje deberá verificarse antes de continuar con el flujo de procesamiento.

Como mínimo deberán validarse:

- Existencia de respuesta.
- Estructura esperada.
- Formato requerido.
- Información suficiente para continuar el proceso.

---

### MDE-008. Validación de recursos externos

Toda interacción con plataformas, APIs o servicios externos deberá confirmar que la operación fue ejecutada correctamente antes de continuar con el siguiente paso del flujo.

---

### MDE-009. Detección por reglas de negocio

La automatización deberá verificar permanentemente el cumplimiento de las reglas funcionales y del modelo de decisiones aprobado.

Cualquier incumplimiento deberá tratarse como una condición de error.

---

### MDE-010. Detección por consistencia del flujo

Durante la ejecución de cada proceso deberá verificarse que las transiciones de estado, decisiones y operaciones respeten el flujo oficial definido para la automatización.

---

## Reglas generales

- Todo error deberá detectarse antes de propagarse a otros componentes, siempre que sea técnicamente posible.
- Toda detección deberá generar evidencia suficiente para su posterior análisis.
- La ausencia de detección no implicará la inexistencia del error.
- Los mecanismos de detección deberán ser reutilizables por todos los módulos del sistema.
- La incorporación de nuevos mecanismos de detección deberá documentarse oficialmente antes de su utilización.
- Ningún módulo podrá implementar mecanismos de detección incompatibles con las reglas establecidas en este documento.

---

# 7. Registro de errores

El registro de errores establece el modelo oficial para documentar todas las condiciones de error detectadas durante la ejecución de la automatización de búsqueda de empleo.

Su propósito es garantizar que cada incidente quede registrado de forma uniforme, completa y trazable, permitiendo su análisis, recuperación, auditoría, monitoreo y mejora continua.

Todo error detectado por cualquier componente de la automatización deberá registrarse siguiendo las reglas definidas en este documento, independientemente de su severidad o de que haya sido recuperado automáticamente.

---

## Objetivos del registro de errores

El registro de errores deberá permitir:

- Conservar el historial completo de cada incidente.
- Facilitar la recuperación y el diagnóstico de fallos.
- Proporcionar evidencia para auditorías.
- Apoyar el monitoreo operativo.
- Identificar tendencias y errores recurrentes.
- Generar indicadores de confiabilidad.
- Facilitar la mejora continua del sistema.

---

## Información obligatoria del registro

Todo error registrado deberá contener, como mínimo, la siguiente información.

### RER-001. Identificador del error

Identificador único asignado conforme a la convención oficial de errores.

Ejemplo:

```
ER-LLM-003
```

---

### RER-002. Identificador del incidente

Identificador único del evento específico ocurrido.

Permitirá distinguir múltiples ocurrencias del mismo tipo de error.

---

### RER-003. Fecha y hora

Fecha y hora exactas en que se detectó el error.

Deberán utilizar el formato oficial definido por los estándares del proyecto.

---

### RER-004. Módulo

Nombre oficial del módulo donde ocurrió el error.

---

### RER-005. Proceso

Proceso específico que se encontraba en ejecución al momento del incidente.

---

### RER-006. Componente

Componente responsable de detectar o generar el error.

---

### RER-007. Categoría

Categoría oficial del error según la clasificación definida en este documento.

---

### RER-008. Nivel de severidad

Nivel de impacto asignado al error.

La severidad deberá determinarse utilizando las reglas oficiales del proyecto.

---

### RER-009. Fuente del error

Origen identificado del incidente.

Deberá corresponder a una de las fuentes oficiales definidas previamente.

---

### RER-010. Descripción

Descripción clara y objetiva del error detectado.

No deberá contener interpretaciones subjetivas.

---

### RER-011. Evidencia

Información objetiva que permita demostrar la ocurrencia del error.

Ejemplos:

- Mensajes del sistema.
- Respuestas recibidas.
- Valores procesados.
- Recursos afectados.
- Capturas o referencias cuando existan.

---

### RER-012. Acción ejecutada

Descripción de la acción realizada por la automatización después de detectar el error.

Ejemplos:

- Reintento.
- Recuperación.
- Escalamiento.
- Finalización controlada.
- Notificación.

---

### RER-013. Resultado de la acción

Resultado obtenido después de ejecutar la estrategia correspondiente.

Ejemplos:

- Recuperado.
- Recuperado parcialmente.
- No recuperado.
- Escalado.
- Finalizado.

---

### RER-014. Estado del incidente

Estado actual del tratamiento del error.

Ejemplos:

- Detectado.
- En recuperación.
- Escalado.
- Resuelto.
- Cerrado.

---

### RER-015. Identificador de la oferta

Cuando el error esté asociado a una oferta específica, deberá registrarse su identificador oficial.

---

### RER-016. Identificador de ejecución

Identificador único de la ejecución de la automatización donde ocurrió el incidente.

Permitirá relacionar múltiples errores ocurridos durante una misma ejecución.

---

### RER-017. Referencias de auditoría

Identificadores o enlaces internos que permitan relacionar el incidente con registros, decisiones, procesos o documentos asociados.

---

## Reglas generales

- Todo error detectado deberá registrarse antes de ejecutar cualquier estrategia de recuperación.
- Ningún error podrá eliminarse del historial una vez registrado.
- Toda modificación realizada sobre un incidente deberá conservar su trazabilidad.
- Los registros deberán mantener un formato uniforme en toda la automatización.
- La información registrada deberá ser suficiente para reproducir y analizar el incidente.
- Los registros deberán mantenerse disponibles durante todo el ciclo de vida definido por las políticas de conservación del proyecto.
- Ningún módulo podrá registrar errores utilizando estructuras distintas a las definidas en este documento.

---

# 8. Niveles de severidad

Los niveles de severidad establecen la clasificación oficial del impacto que produce un error sobre la automatización de búsqueda de empleo.

Su propósito es proporcionar un criterio uniforme para determinar la prioridad de atención, las estrategias de recuperación, las políticas de reintento, los mecanismos de escalamiento y las acciones correctivas aplicables a cada incidente.

Todo error registrado deberá clasificarse utilizando uno y solo uno de los niveles de severidad definidos en este documento.

---

## Criterios de evaluación

La severidad de un error deberá determinarse considerando, como mínimo, los siguientes aspectos:

### NSE-001. Impacto operacional

Grado en que el error afecta la continuidad de la automatización.

---

### NSE-002. Impacto sobre los datos

Nivel de afectación sobre la integridad, consistencia o disponibilidad de la información.

---

### NSE-003. Alcance

Cantidad de módulos, procesos o componentes afectados por el incidente.

---

### NSE-004. Recuperabilidad

Capacidad del sistema para resolver automáticamente la condición de error.

---

### NSE-005. Intervención requerida

Nivel de participación del usuario o de otros componentes necesario para resolver el incidente.

---

## Niveles oficiales de severidad

### SV-1. Crítico

Corresponde a errores que impiden la continuidad de la automatización o comprometen la integridad del sistema.

#### Características

- La ejecución no puede continuar.
- No existe recuperación automática viable.
- Puede comprometer información crítica.
- Requiere atención inmediata.

#### Ejemplos

- Corrupción de información.
- Fallo general de persistencia.
- Inconsistencia crítica del flujo.
- Error interno irrecuperable.

---

### SV-2. Alto

Corresponde a errores que impiden completar correctamente un proceso importante, aunque el resto de la automatización pueda continuar funcionando.

#### Características

- Afecta procesos principales.
- Puede requerir intervención.
- La recuperación automática puede no ser suficiente.

#### Ejemplos

- Imposibilidad de procesar una oferta.
- Error persistente del modelo de lenguaje.
- Error permanente en una plataforma externa.
- Fallo repetitivo durante la extracción.

---

### SV-3. Medio

Corresponde a errores que afectan parcialmente un proceso, pero cuya recuperación automática resulta posible en la mayoría de los casos.

#### Características

- Impacto limitado.
- Existe mecanismo oficial de recuperación.
- No compromete la integridad general del sistema.

#### Ejemplos

- Timeout temporal.
- Error transitorio de red.
- Recurso temporalmente no disponible.
- Respuesta incompleta recuperable.

---

### SV-4. Bajo

Corresponde a errores con impacto reducido que no impiden el funcionamiento general de la automatización.

#### Características

- El proceso puede continuar.
- El impacto operativo es mínimo.
- No requiere intervención inmediata.

#### Ejemplos

- Advertencias de validación.
- Información opcional ausente.
- Retrasos menores.
- Reintento exitoso en el primer intento.

---

### SV-5. Informativo

Corresponde a eventos registrados únicamente con fines de auditoría, monitoreo o análisis estadístico.

No representan una condición de fallo operativo.

#### Ejemplos

- Recuperación automática exitosa.
- Reintentos exitosos.
- Cambios de estado relevantes.
- Eventos de seguimiento.

---

## Reglas para la asignación de severidad

### RSE-001

Todo error deberá recibir un único nivel oficial de severidad.

---

### RSE-002

La severidad deberá asignarse inmediatamente después de clasificar el error.

---

### RSE-003

La severidad podrá actualizarse únicamente cuando exista evidencia objetiva de que el impacto real del incidente cambió durante su tratamiento.

Toda modificación deberá registrarse para fines de auditoría.

---

### RSE-004

La severidad nunca deberá asignarse considerando únicamente la causa del error.

También deberá evaluarse el impacto real producido sobre la automatización.

---

### RSE-005

Dos errores de la misma categoría podrán tener niveles de severidad diferentes cuando su impacto operativo sea distinto.

---

### RSE-006

Las estrategias de recuperación, reintento, notificación y escalamiento deberán basarse en el nivel de severidad asignado.

---

## Matriz general de severidad

| Nivel | Impacto | Recuperación automática | Intervención del usuario |
|--------|----------|-------------------------|--------------------------|
| SV-1 | Crítico | No | Obligatoria |
| SV-2 | Alto | Parcial o limitada | Probable |
| SV-3 | Medio | Sí, normalmente | Poco frecuente |
| SV-4 | Bajo | Sí | No requerida |
| SV-5 | Informativo | No aplica | No requerida |

---

## Reglas generales

- Todo error registrado deberá tener un nivel oficial de severidad.
- La severidad deberá determinar las acciones posteriores del manejo del error.
- La clasificación deberá mantenerse consistente en toda la automatización.
- Las modificaciones de severidad deberán conservar su historial.
- Ningún componente podrá utilizar niveles de severidad distintos a los definidos en este documento.

---

# 9. Estrategias de recuperación

Las estrategias de recuperación establecen el conjunto oficial de acciones que podrá ejecutar la automatización para restablecer el funcionamiento normal de un proceso después de detectar una condición de error.

Su propósito es minimizar el impacto operativo de los incidentes, preservar la integridad de la información, mantener la continuidad de los procesos y reducir al mínimo la necesidad de intervención del usuario.

Toda estrategia de recuperación deberá ejecutarse conforme a las reglas establecidas en este documento y únicamente después de haber detectado, clasificado y registrado el error correspondiente.

---

## Principios de recuperación

### PRE-001. Recuperación segura

Toda estrategia de recuperación deberá preservar la integridad, consistencia y trazabilidad de la información.

---

### PRE-002. Recuperación controlada

Ninguna recuperación podrá ejecutarse de forma arbitraria.

Toda acción deberá corresponder a una estrategia oficial aprobada.

---

### PRE-003. Recuperación proporcional

La estrategia aplicada deberá ser coherente con la severidad y naturaleza del error.

No deberán utilizarse mecanismos excesivos para resolver errores menores.

---

### PRE-004. Recuperación verificable

Toda recuperación deberá validarse antes de permitir la continuación del proceso.

---

### PRE-005. Recuperación auditable

Toda estrategia ejecutada deberá quedar registrada para fines de auditoría y análisis posterior.

---

## Catálogo oficial de estrategias de recuperación

### REC-001. Reintento automático

Consiste en ejecutar nuevamente la misma operación sin modificar su contexto de ejecución.

Aplicable principalmente a errores temporales.

Ejemplos:

- Timeout.
- Error transitorio de red.
- Servicio temporalmente no disponible.

---

### REC-002. Espera y reanudación

Consiste en suspender temporalmente la ejecución hasta que desaparezca la condición que originó el error.

Aplicable cuando exista una alta probabilidad de recuperación espontánea.

---

### REC-003. Reinicio controlado de la operación

Consiste en reiniciar únicamente la operación afectada, manteniendo intacto el resto del proceso.

Su objetivo es evitar la repetición innecesaria de tareas ya completadas correctamente.

---

### REC-004. Reprocesamiento

Consiste en ejecutar nuevamente una etapa previamente finalizada utilizando la información disponible.

Aplicable cuando exista evidencia de que el resultado obtenido pudo verse afectado por un error recuperable.

---

### REC-005. Continuación segura del flujo

Permite continuar el proceso omitiendo únicamente aquellas operaciones cuya ausencia no comprometa la integridad del resultado final.

Solo podrá utilizarse cuando exista autorización explícita dentro del modelo de decisiones.

---

### REC-006. Omisión controlada

Consiste en excluir una operación considerada opcional dentro del flujo funcional.

La omisión deberá registrarse y conservarse para auditoría.

---

### REC-007. Escalamiento

Consiste en transferir el tratamiento del error a otro mecanismo de recuperación, componente o usuario cuando la estrategia actual resulte insuficiente.

---

### REC-008. Finalización controlada

Consiste en detener la ejecución del proceso de forma ordenada cuando no exista una estrategia segura para continuar.

La finalización deberá preservar toda la información generada hasta ese momento.

---

### REC-009. Solicitud de intervención del usuario

Consiste en solicitar una decisión del usuario cuando el sistema no disponga de información suficiente para resolver automáticamente el incidente.

La automatización deberá proporcionar toda la información necesaria para facilitar dicha decisión.

---

## Selección de la estrategia

La estrategia de recuperación deberá seleccionarse considerando, como mínimo, los siguientes criterios:

### SRE-001. Severidad

Nivel de impacto del error.

---

### SRE-002. Recuperabilidad

Probabilidad de resolver automáticamente el incidente.

---

### SRE-003. Riesgo

Posibilidad de afectar la integridad de la información o del proceso.

---

### SRE-004. Continuidad operacional

Capacidad para continuar el flujo sin comprometer los resultados esperados.

---

### SRE-005. Dependencias

Existencia de componentes, servicios o recursos cuya disponibilidad sea necesaria para ejecutar la recuperación.

---

## Reglas generales

- Toda recuperación deberá utilizar una estrategia oficial.
- Ninguna estrategia podrá comprometer la integridad de la información.
- La recuperación siempre deberá validarse antes de continuar el flujo.
- Toda estrategia ejecutada deberá registrarse en el historial del incidente.
- Una misma condición de error podrá requerir varias estrategias ejecutadas de forma secuencial.
- Cuando ninguna estrategia resulte efectiva, el incidente deberá escalarse conforme a las reglas oficiales.
- La incorporación de nuevas estrategias requerirá la actualización formal de este documento.

---

# 10. Políticas de reintento

Las políticas de reintento establecen las reglas oficiales que regulan la repetición controlada de operaciones que hayan fallado durante la ejecución de la automatización.

Su propósito es maximizar la recuperación automática de errores temporales, evitando reintentos innecesarios que puedan degradar el rendimiento del sistema, generar bloqueos en plataformas externas o comprometer la integridad del procesamiento.

Toda estrategia de recuperación que contemple la repetición de una operación deberá cumplir las políticas definidas en este documento.

---

## Principios de los reintentos

### PRT-001. Reintentos controlados

Toda operación podrá reintentarse únicamente cuando exista una política oficial que lo autorice.

No se permitirán reintentos ilimitados.

---

### PRT-002. Reintentos seguros

Un reintento no deberá provocar duplicidad de información, inconsistencias o alteraciones del flujo oficial del sistema.

---

### PRT-003. Reintentos justificados

Solo podrán reintentarse operaciones cuya probabilidad de éxito aumente mediante una nueva ejecución.

---

### PRT-004. Reintentos auditables

Cada intento deberá registrarse como parte del historial del incidente.

---

### PRT-005. Reintentos independientes

Cada intento deberá evaluarse de forma independiente, verificando nuevamente las condiciones de éxito o fallo.

---

## Políticas oficiales de reintento

### POL-RET-001. Número máximo de reintentos

Toda operación susceptible de reintento deberá definir un número máximo de intentos permitidos.

Una vez alcanzado dicho límite, el sistema deberá aplicar otra estrategia de recuperación o escalar el incidente.

---

### POL-RET-002. Tiempo de espera

Entre dos reintentos consecutivos deberá existir un intervalo de espera.

El tiempo de espera deberá minimizar la probabilidad de repetir inmediatamente la condición que produjo el error.

---

### POL-RET-003. Incremento progresivo

Cuando una operación falle repetidamente, el tiempo de espera entre reintentos podrá incrementarse progresivamente conforme a la política definida para el proceso correspondiente.

El objetivo será reducir la carga sobre recursos internos y servicios externos.

---

### POL-RET-004. Verificación previa

Antes de ejecutar un nuevo intento, la automatización deberá verificar que la condición que originó el error haya cambiado o que existan posibilidades razonables de éxito.

---

### POL-RET-005. Cancelación de reintentos

Los reintentos deberán cancelarse inmediatamente cuando:

- Se alcance el número máximo permitido.
- El error sea clasificado como no recuperable.
- Se detecte riesgo para la integridad de la información.
- Continúe ejecutándose el reintento sin posibilidad objetiva de éxito.
- Una regla del modelo de decisiones así lo determine.

---

### POL-RET-006. Errores no reintentables

No deberán ejecutarse reintentos automáticos sobre errores cuya naturaleza impida razonablemente una recuperación mediante repetición.

Ejemplos:

- Configuración inválida.
- Parámetros obligatorios ausentes.
- Datos inconsistentes.
- Errores de lógica.
- Restricciones permanentes de un servicio externo.

---

### POL-RET-007. Registro obligatorio

Cada intento deberá registrarse indicando, como mínimo:

- Número de intento.
- Fecha y hora.
- Resultado obtenido.
- Tiempo de espera aplicado.
- Estrategia utilizada.
- Estado posterior del incidente.

---

### POL-RET-008. Cambio de estrategia

Cuando los reintentos autorizados no resuelvan el incidente, la automatización deberá abandonar la política de reintentos y aplicar la siguiente estrategia de recuperación correspondiente.

No se permitirá reiniciar el ciclo de reintentos indefinidamente.

---

### POL-RET-009. Independencia del proceso

El fracaso de una política de reintento no deberá afectar procesos independientes que continúen ejecutándose correctamente.

---

### POL-RET-010. Protección de servicios externos

Las políticas de reintento deberán evitar comportamientos que puedan interpretarse como abuso sobre plataformas, APIs o servicios externos.

La automatización deberá respetar los límites operativos establecidos por dichos servicios.

---

## Reglas generales

- Toda política de reintento deberá estar asociada a una estrategia oficial de recuperación.
- Ningún reintento podrá comprometer la integridad de la información.
- Todo intento deberá quedar registrado para auditoría.
- El número máximo de reintentos deberá definirse antes de iniciar la ejecución del proceso correspondiente.
- Una operación no podrá permanecer indefinidamente en estado de reintento.
- Finalizada la política de reintentos, el incidente deberá continuar con la estrategia oficial correspondiente.
- Ningún módulo podrá implementar políticas de reintento incompatibles con las definidas en este documento.

---

# 11. Manejo de errores por módulo

El manejo de errores por módulo establece las reglas específicas para la detección, recuperación y tratamiento de errores dentro de cada uno de los módulos funcionales de la automatización de búsqueda de empleo.

Su propósito es adaptar las políticas generales de manejo de errores a las características particulares de cada etapa del proceso, garantizando un comportamiento uniforme sin perder las necesidades específicas de cada módulo.

Todos los módulos deberán cumplir las reglas generales definidas en este documento y únicamente podrán aplicar estrategias adicionales cuando estas no contradigan las políticas oficiales.

---

# Módulo 1. Descubrimiento de oportunidades

## Objetivo

Gestionar los errores producidos durante la localización y obtención inicial de ofertas de empleo.

### Errores frecuentes

- Problemas de conectividad.
- Timeout.
- Cambios en la estructura de la plataforma.
- Captchas.
- Restricciones temporales.
- Errores de autenticación.
- Información inaccesible.

### Categorías aplicables

- ER-RED
- ER-NAV
- ER-EXT
- ER-EXTS

### Estrategias permitidas

- REC-001 Reintento automático.
- REC-002 Espera y reanudación.
- REC-003 Reinicio controlado.
- REC-007 Escalamiento.
- REC-008 Finalización controlada.

### Políticas de reintento

Aplicarán las políticas oficiales definidas para reintentos de servicios externos.

### Criterios de finalización

El módulo finalizará únicamente cuando:

- La extracción se complete correctamente.
- Se agoten las estrategias autorizadas.
- El modelo de decisiones determine la finalización.

---

# Módulo 2. Preparación inicial de ofertas

## Objetivo

Gestionar los errores producidos durante la limpieza, normalización y validación inicial de la información.

### Errores frecuentes

- Campos obligatorios ausentes.
- Formatos inválidos.
- Información inconsistente.
- Duplicados.
- Errores de transformación.

### Categorías aplicables

- ER-VAL
- ER-DAT
- ER-INT

### Estrategias permitidas

- REC-003 Reinicio controlado.
- REC-004 Reprocesamiento.
- REC-006 Omisión controlada.
- REC-008 Finalización controlada.

### Políticas de reintento

Únicamente cuando el origen del error sea recuperable.

Los errores de datos permanentes no deberán reintentarse.

### Criterios de finalización

El procesamiento finalizará cuando la oferta alcance un estado consistente o se determine que no puede recuperarse.

---

# Módulo 3. Evaluación inicial

## Objetivo

Gestionar los errores producidos durante la evaluación automática de compatibilidad de la oferta.

### Errores frecuentes

- Reglas inconsistentes.
- Información insuficiente.
- Errores de puntuación.
- Estados inválidos.

### Categorías aplicables

- ER-DAT
- ER-VAL
- ER-INT

### Estrategias permitidas

- REC-004 Reprocesamiento.
- REC-005 Continuación segura.
- REC-007 Escalamiento.
- REC-009 Intervención del usuario.

### Políticas de reintento

Solo cuando exista nueva información que permita repetir la evaluación con una expectativa razonable de éxito.

### Criterios de finalización

La evaluación concluirá cuando:

- Se obtenga un resultado válido.
- Se descarte definitivamente la oferta.
- El usuario intervenga cuando sea requerido.

---

# Módulo 4. Procesamiento de la oferta

## Objetivo

Gestionar los errores ocurridos durante el análisis profundo de las ofertas seleccionadas.

### Errores frecuentes

- Respuestas inválidas del modelo de lenguaje.
- Información insuficiente.
- Fallos durante el análisis.
- Errores de generación de resultados.

### Categorías aplicables

- ER-LLM
- ER-DAT
- ER-INT
- ER-EXTS

### Estrategias permitidas

- REC-001 Reintento automático.
- REC-004 Reprocesamiento.
- REC-007 Escalamiento.
- REC-009 Intervención del usuario.

### Políticas de reintento

Los reintentos deberán respetar las políticas oficiales para servicios de inteligencia artificial y recursos externos.

### Criterios de finalización

El módulo finalizará cuando:

- El análisis se complete correctamente.
- Se agoten las estrategias autorizadas.
- El usuario determine la continuación o finalización del proceso.

---

# Módulo 5. Gestión y seguimiento

## Objetivo

Gestionar los errores producidos durante el almacenamiento, actualización y seguimiento de la información.

### Errores frecuentes

- Escrituras fallidas.
- Lecturas fallidas.
- Historial inconsistente.
- Actualización incompleta.
- Errores de persistencia.

### Categorías aplicables

- ER-DB
- ER-DAT
- ER-INT

### Estrategias permitidas

- REC-003 Reinicio controlado.
- REC-004 Reprocesamiento.
- REC-007 Escalamiento.
- REC-008 Finalización controlada.

### Políticas de reintento

Los reintentos deberán garantizar que nunca se produzcan duplicados ni inconsistencias en la información almacenada.

### Criterios de finalización

El módulo finalizará únicamente cuando:

- La información haya sido almacenada correctamente.
- El historial permanezca consistente.
- El incidente haya sido tratado conforme a las reglas oficiales.

---

## Reglas generales

- Todos los módulos deberán utilizar exclusivamente las categorías oficiales de errores.
- Las estrategias de recuperación deberán corresponder a las autorizadas para cada módulo.
- Todo incidente deberá registrarse antes de ejecutar cualquier recuperación.
- Ningún módulo podrá implementar mecanismos de recuperación incompatibles con este documento.
- Las modificaciones futuras de un módulo no deberán afectar las reglas generales del manejo de errores.
- La incorporación de nuevos módulos requerirá la actualización oficial de esta sección.

---

# 12. Manejo de errores externos

El manejo de errores externos establece las reglas oficiales para identificar, tratar y recuperar los errores originados por recursos, plataformas o servicios que no forman parte de la automatización y sobre los cuales el sistema no posee control directo.

Su propósito es minimizar el impacto de las fallas externas, preservar la continuidad operacional cuando sea posible y garantizar una respuesta uniforme frente a incidentes ocasionados por dependencias de terceros.

Las reglas definidas en este capítulo serán aplicables a toda interacción con plataformas de empleo, servicios de inteligencia artificial, APIs, servicios de autenticación, infraestructura de red y cualquier otro recurso externo utilizado por la automatización.

---

## Principios

### MEE-001. Independencia operacional

La automatización deberá asumir que todo servicio externo puede fallar en cualquier momento.

Ningún flujo crítico dependerá de la disponibilidad permanente de un recurso externo.

---

### MEE-002. Validación obligatoria

Toda respuesta recibida desde un recurso externo deberá validarse antes de continuar el procesamiento.

---

### MEE-003. Recuperación controlada

La recuperación de errores externos deberá respetar las estrategias y políticas oficiales definidas en este documento.

---

### MEE-004. Protección de terceros

La automatización deberá evitar comportamientos que puedan generar sobrecarga, bloqueos o incumplimientos de las políticas de uso de servicios externos.

---

### MEE-005. Registro obligatorio

Toda falla producida por un recurso externo deberá registrarse para fines de auditoría y análisis posterior.

---

## Tipos de errores externos

### EEX-001. Plataformas de empleo

Errores ocasionados por sitios web utilizados para descubrir ofertas de empleo.

Ejemplos:

- Plataforma no disponible.
- Cambios en la estructura del sitio.
- Captchas.
- Restricciones de acceso.
- Autenticación fallida.
- Información inaccesible.

### Estrategias permitidas

- REC-001 Reintento automático.
- REC-002 Espera y reanudación.
- REC-003 Reinicio controlado.
- REC-007 Escalamiento.
- REC-008 Finalización controlada.

---

### EEX-002. APIs externas

Errores originados por interfaces de programación utilizadas por la automatización.

Ejemplos:

- Timeout.
- Respuesta inválida.
- Código de error.
- Servicio no disponible.
- Límite de solicitudes excedido.

### Estrategias permitidas

- REC-001
- REC-002
- REC-007

---

### EEX-003. Servicios del modelo de lenguaje

Errores ocasionados por servicios externos utilizados para el procesamiento mediante inteligencia artificial.

Ejemplos:

- Servicio no disponible.
- Tiempo de respuesta excedido.
- Respuesta inválida.
- Error de autenticación.
- Restricción temporal.

### Estrategias permitidas

- REC-001
- REC-002
- REC-004
- REC-007
- REC-009

---

### EEX-004. Servicios de autenticación

Errores relacionados con procesos de autenticación o autorización en recursos externos.

Ejemplos:

- Credenciales inválidas.
- Token expirado.
- Acceso denegado.
- Sesión inválida.

### Estrategias permitidas

- REC-003
- REC-007
- REC-009

---

### EEX-005. Servicios de red

Errores relacionados con la infraestructura de comunicación.

Ejemplos:

- DNS no disponible.
- Conectividad interrumpida.
- Alta latencia.
- Timeout.
- Rutas inaccesibles.

### Estrategias permitidas

- REC-001
- REC-002
- REC-007

---

### EEX-006. Cambios estructurales

Errores ocasionados por modificaciones realizadas por terceros sobre plataformas o servicios utilizados por la automatización.

Ejemplos:

- Cambio de estructura HTML.
- Cambio de selectores.
- Nuevos flujos de navegación.
- Eliminación de funcionalidades.

### Estrategias permitidas

- REC-007
- REC-008
- REC-009

---

### EEX-007. Restricciones operativas

Errores ocasionados por límites impuestos por servicios externos.

Ejemplos:

- Rate limiting.
- Restricción geográfica.
- Restricción temporal.
- Límite de uso alcanzado.

### Estrategias permitidas

- REC-002
- REC-007
- REC-009

---

### EEX-008. Mantenimiento de terceros

Errores ocasionados por interrupciones programadas o no programadas realizadas por proveedores externos.

Ejemplos:

- Ventanas de mantenimiento.
- Actualizaciones del servicio.
- Interrupciones temporales.

### Estrategias permitidas

- REC-002
- REC-007
- REC-008

---

## Reglas generales

- Todo recurso externo deberá considerarse potencialmente no disponible.
- Ninguna respuesta proveniente de un servicio externo podrá asumirse como válida sin verificación previa.
- Las estrategias de recuperación deberán respetar las políticas oficiales de reintento.
- La automatización deberá minimizar el impacto de los errores externos sobre otros módulos.
- Los errores externos nunca deberán comprometer la integridad de la información ya procesada.
- Toda interacción con servicios externos deberá conservar su trazabilidad completa.
- La incorporación de nuevos recursos externos requerirá la actualización oficial de este documento.

---

# 13. Manejo de errores del modelo de lenguaje (LLM)

El manejo de errores del modelo de lenguaje establece las reglas oficiales para detectar, validar, registrar, recuperar y tratar los errores producidos durante la interacción entre la automatización y el servicio de inteligencia artificial utilizado para el análisis y procesamiento de ofertas de empleo.

Debido a que el modelo de lenguaje constituye un componente crítico del sistema, sus respuestas nunca deberán utilizarse directamente sin haber sido previamente verificadas mediante los mecanismos oficiales definidos en este documento.

El objetivo de este capítulo es garantizar que la utilización del modelo de lenguaje no comprometa la consistencia de la información, el modelo de decisiones, el flujo de datos ni la confiabilidad general de la automatización.

---

## Principios

### MLLM-001. Desconfianza por defecto

Toda respuesta generada por el modelo de lenguaje deberá considerarse potencialmente incorrecta hasta completar exitosamente todas las validaciones correspondientes.

---

### MLLM-002. Validación obligatoria

Ninguna respuesta del modelo podrá utilizarse para tomar decisiones o modificar información del sistema sin haber sido validada previamente.

---

### MLLM-003. Independencia del procesamiento

La automatización nunca dependerá exclusivamente del modelo de lenguaje para garantizar la integridad del sistema.

Toda información crítica deberá poder verificarse mediante reglas adicionales cuando corresponda.

---

### MLLM-004. Recuperación controlada

Los errores relacionados con el modelo deberán recuperarse únicamente mediante las estrategias oficiales autorizadas.

---

### MLLM-005. Auditabilidad

Toda interacción con el modelo de lenguaje deberá conservar suficiente información para permitir su auditoría y análisis posterior.

---

## Tipos oficiales de errores del LLM

### ELLM-001. Respuesta vacía

El modelo no devuelve contenido utilizable.

---

### ELLM-002. Respuesta incompleta

La respuesta contiene únicamente parte de la información esperada.

---

### ELLM-003. Respuesta truncada

La generación finaliza antes de completar el contenido requerido.

---

### ELLM-004. Formato inválido

La respuesta no cumple el formato requerido por la automatización.

Ejemplos:

- JSON inválido.
- Markdown incorrecto.
- Campos obligatorios ausentes.
- Estructura inesperada.

---

### ELLM-005. Información inconsistente

La respuesta contiene contradicciones internas o resultados incompatibles con la información suministrada.

---

### ELLM-006. Interpretación incorrecta

El modelo interpreta erróneamente la información proporcionada.

---

### ELLM-007. Incumplimiento del prompt

La respuesta no sigue las instrucciones establecidas por el prompt correspondiente.

---

### ELLM-008. Alucinación

El modelo genera información que no puede justificarse mediante los datos de entrada ni mediante las reglas oficiales de la automatización.

---

### ELLM-009. Tiempo de respuesta excedido

El modelo no responde dentro del tiempo máximo permitido.

---

### ELLM-010. Error del servicio

El servicio del modelo de lenguaje devuelve una condición de error que impide completar la operación.

---

## Validaciones obligatorias

Toda respuesta generada por el modelo deberá superar, como mínimo, las siguientes validaciones.

### VLLM-001. Existencia

Verificar que exista una respuesta.

---

### VLLM-002. Integridad

Verificar que la respuesta esté completa.

---

### VLLM-003. Formato

Verificar que la estructura corresponda al formato esperado.

---

### VLLM-004. Consistencia

Verificar que no existan contradicciones internas.

---

### VLLM-005. Coherencia

Verificar que la respuesta sea coherente con la información proporcionada al modelo.

---

### VLLM-006. Cumplimiento del prompt

Verificar que el modelo haya seguido las instrucciones definidas para la operación.

---

### VLLM-007. Reglas del proyecto

Verificar que la respuesta no contradiga las reglas funcionales, el modelo de decisiones, el flujo de datos ni los estándares oficiales del proyecto.

---

## Estrategias de recuperación permitidas

Los errores del modelo de lenguaje podrán utilizar únicamente las siguientes estrategias oficiales:

- REC-001 Reintento automático.
- REC-002 Espera y reanudación.
- REC-004 Reprocesamiento.
- REC-007 Escalamiento.
- REC-009 Solicitud de intervención del usuario.

La estrategia seleccionada dependerá del tipo de error, su severidad y la probabilidad de recuperación.

---

## Reglas generales

- Ninguna respuesta del modelo podrá utilizarse sin validación previa.
- Toda interacción con el modelo deberá registrarse para auditoría.
- Las respuestas inválidas nunca deberán almacenarse como información oficial del sistema.
- Las respuestas parcialmente válidas únicamente podrán utilizarse cuando exista una regla oficial que lo autorice.
- Los errores repetitivos del modelo deberán escalarse conforme a las políticas oficiales de recuperación.
- La incorporación de nuevos tipos de errores del modelo requerirá la actualización oficial de este documento.
- Ningún componente podrá implementar mecanismos de validación incompatibles con los definidos en esta sección.

---

# 14. Manejo de errores de datos

El manejo de errores de datos establece las reglas oficiales para detectar, validar, registrar, recuperar y corregir cualquier condición que pueda comprometer la calidad, integridad, consistencia o disponibilidad de la información utilizada por la automatización.

Su propósito es garantizar que todas las decisiones, evaluaciones y procesos de la automatización se ejecuten utilizando información confiable, completa y consistente durante todo el ciclo de vida de los datos.

Las reglas definidas en este capítulo serán aplicables a toda información capturada, generada, transformada, almacenada, actualizada o recuperada por cualquier componente del sistema.

---

## Principios

### MED-001. Integridad de los datos

Toda operación deberá preservar la integridad lógica y estructural de la información.

---

### MED-002. Consistencia

Los datos deberán mantenerse consistentes entre todos los componentes de la automatización.

---

### MED-003. Validación obligatoria

Toda información deberá validarse antes de ser utilizada o almacenada.

---

### MED-004. Trazabilidad

Toda modificación realizada sobre los datos deberá poder rastrearse posteriormente.

---

### MED-005. Recuperabilidad

Siempre que sea técnicamente posible, la automatización deberá intentar recuperar la información afectada antes de descartarla.

---

## Tipos oficiales de errores de datos

### EDATA-001. Datos incompletos

Información obligatoria ausente o insuficiente para continuar correctamente el procesamiento.

---

### EDATA-002. Datos inválidos

Información cuyo contenido incumple las reglas de validación definidas por el proyecto.

Ejemplos:

- Formatos incorrectos.
- Valores fuera de rango.
- Tipos incompatibles.

---

### EDATA-003. Datos duplicados

Existencia de múltiples registros que representan la misma entidad.

---

### EDATA-004. Datos inconsistentes

Información que presenta contradicciones internas o incompatibilidades con otros registros.

---

### EDATA-005. Datos obsoletos

Información que ya no representa el estado actual del elemento correspondiente.

---

### EDATA-006. Relaciones inválidas

Referencias entre entidades que no pueden resolverse correctamente.

---

### EDATA-007. Conflictos de actualización

Situaciones en las que múltiples operaciones intentan modificar simultáneamente la misma información.

---

### EDATA-008. Corrupción de datos

Alteración de la información que impide su utilización confiable.

---

### EDATA-009. Pérdida parcial de información

Desaparición de una parte del contenido necesario para completar el procesamiento.

---

### EDATA-010. Error de transformación

Alteración incorrecta de los datos durante procesos de limpieza, normalización o conversión.

---

## Validaciones obligatorias

Toda información deberá superar, como mínimo, las siguientes validaciones.

### VDAT-001. Existencia

Verificar que toda información obligatoria esté presente.

---

### VDAT-002. Integridad

Verificar que los datos permanezcan completos durante todo el procesamiento.

---

### VDAT-003. Consistencia

Verificar la coherencia entre todos los campos relacionados.

---

### VDAT-004. Formato

Verificar que los datos respeten los formatos oficiales definidos por el proyecto.

---

### VDAT-005. Unicidad

Verificar la inexistencia de registros duplicados cuando corresponda.

---

### VDAT-006. Relaciones

Verificar la validez de las relaciones entre entidades.

---

### VDAT-007. Estados

Verificar que las transiciones de estado respeten el flujo oficial de la automatización.

---

### VDAT-008. Persistencia

Verificar que la información almacenada corresponda exactamente con la información validada.

---

## Estrategias de recuperación permitidas

Los errores relacionados con los datos podrán utilizar las siguientes estrategias oficiales:

- REC-003 Reinicio controlado.
- REC-004 Reprocesamiento.
- REC-005 Continuación segura (cuando exista autorización).
- REC-006 Omisión controlada (únicamente sobre información no obligatoria).
- REC-007 Escalamiento.
- REC-008 Finalización controlada.
- REC-009 Solicitud de intervención del usuario.

La estrategia seleccionada dependerá de la naturaleza del error, del impacto sobre la información y de la posibilidad de recuperación sin comprometer la integridad de los datos.

---

## Reglas generales

- Ningún dato podrá almacenarse sin haber sido validado.
- Ningún dato inválido podrá utilizarse para alimentar el modelo de decisiones.
- Toda modificación sobre la información deberá conservar su trazabilidad.
- Los datos corruptos nunca deberán sobrescribir información previamente validada.
- Las operaciones de recuperación deberán preservar la integridad de toda la información relacionada.
- Toda pérdida de información deberá registrarse como un incidente oficial.
- Ningún componente podrá implementar reglas de validación incompatibles con las definidas en este documento.

---

# 15. Notificaciones y alertas

Las notificaciones y alertas establecen el modelo oficial mediante el cual la automatización comunica eventos relevantes relacionados con la ocurrencia, tratamiento, recuperación y resolución de errores.

Su propósito es garantizar que toda la información importante llegue oportunamente al destinatario adecuado, evitando tanto la ausencia de información como la generación excesiva de mensajes que dificulten el seguimiento de la operación.

Las reglas definidas en este capítulo serán aplicables a todos los módulos y componentes de la automatización.

---

## Principios

### NAL-001. Relevancia

Toda notificación o alerta deberá comunicar únicamente información útil para el seguimiento del sistema.

---

### NAL-002. Oportunidad

La comunicación deberá emitirse tan pronto como ocurra el evento que la origine.

---

### NAL-003. Claridad

Toda comunicación deberá ser objetiva, precisa y suficiente para comprender el incidente.

---

### NAL-004. No duplicidad

La automatización deberá evitar la emisión repetitiva de mensajes correspondientes al mismo incidente, salvo que exista un cambio relevante en su estado.

---

### NAL-005. Trazabilidad

Toda notificación o alerta emitida deberá conservarse como parte del historial del incidente correspondiente.

---

## Clasificación

### Notificación

Una notificación informa un evento operativo que no requiere atención inmediata del usuario.

Su finalidad es mantener el historial operativo y facilitar el seguimiento del comportamiento del sistema.

Ejemplos:

- Inicio de una recuperación automática.
- Recuperación completada correctamente.
- Reintento ejecutado.
- Finalización normal del tratamiento del error.
- Registro de un incidente de baja severidad.

---

### Alerta

Una alerta comunica una condición que requiere atención, seguimiento o intervención debido al impacto potencial sobre la automatización.

Las alertas deberán priorizarse según la severidad del incidente.

Ejemplos:

- Error crítico.
- Recuperación fallida.
- Agotamiento de los reintentos.
- Intervención obligatoria del usuario.
- Fallo repetitivo.
- Corrupción de datos.
- Indisponibilidad prolongada de un servicio externo.

---

## Niveles oficiales de alerta

### ALT-001. Informativa

Comunica eventos relevantes sin impacto operativo.

No requiere acciones adicionales.

---

### ALT-002. Preventiva

Comunica situaciones que podrían evolucionar hacia un incidente de mayor impacto.

Permite realizar seguimiento preventivo.

---

### ALT-003. Operativa

Comunica incidentes que afectan parcialmente el funcionamiento de la automatización.

Puede requerir supervisión.

---

### ALT-004. Crítica

Comunica incidentes que comprometen procesos importantes o requieren intervención inmediata.

---

## Eventos que generan notificaciones

Como mínimo, la automatización deberá emitir notificaciones cuando ocurra alguno de los siguientes eventos:

- Inicio de una estrategia de recuperación.
- Finalización satisfactoria de una recuperación.
- Ejecución de un reintento.
- Cambio de estado de un incidente.
- Cierre de un incidente.
- Recuperación automática exitosa.

---

## Eventos que generan alertas

Como mínimo, la automatización deberá generar alertas cuando ocurra alguno de los siguientes eventos:

- Error clasificado como SV-1.
- Error clasificado como SV-2.
- Agotamiento del número máximo de reintentos.
- Error no recuperable.
- Escalamiento del incidente.
- Solicitud de intervención del usuario.
- Corrupción de datos.
- Fallo repetitivo sobre un mismo componente.
- Indisponibilidad prolongada de un recurso externo.

---

## Destinatarios

Las comunicaciones podrán dirigirse a uno o varios de los siguientes destinatarios:

- Sistema de auditoría.
- Sistema de registros.
- Componentes internos de la automatización.
- Usuario.
- Procesos de recuperación.
- Procesos de monitoreo.

La selección del destinatario dependerá del tipo de evento y de su severidad.

---

## Contenido mínimo

Toda notificación o alerta deberá incluir, como mínimo:

- Identificador del incidente.
- Fecha y hora.
- Módulo afectado.
- Categoría del error.
- Nivel de severidad.
- Descripción resumida.
- Acción ejecutada.
- Estado actual del incidente.

Cuando corresponda, también podrá incluir:

- Estrategia de recuperación aplicada.
- Número de reintentos ejecutados.
- Recomendaciones para el usuario.
- Información adicional para auditoría.

---

## Cierre de alertas

Una alerta podrá cerrarse únicamente cuando:

- El incidente haya sido resuelto.
- La recuperación haya finalizado correctamente.
- El proceso haya concluido de forma controlada.
- El usuario haya tomado la decisión correspondiente cuando sea requerida.

El cierre deberá registrarse como parte del historial del incidente.

---

## Reglas generales

- Toda alerta deberá estar asociada a un incidente registrado.
- Toda notificación deberá corresponder a un evento verificable.
- Las alertas no podrán emitirse sin una condición objetiva que las justifique.
- La automatización deberá evitar la generación masiva de alertas repetitivas sobre un mismo incidente.
- Toda comunicación deberá conservarse para fines de auditoría y trazabilidad.
- La incorporación de nuevos tipos de notificaciones o alertas requerirá la actualización oficial de este documento.

---

# 16. Escalamiento de errores

El escalamiento de errores establece el modelo oficial mediante el cual un incidente es transferido a un nivel superior de tratamiento cuando las estrategias de recuperación disponibles resultan insuficientes para resolver la condición de error.

Su propósito es garantizar que ningún incidente permanezca indefinidamente sin resolución y que toda condición de error continúe siendo tratada mediante mecanismos progresivos, controlados y completamente trazables.

El escalamiento deberá ejecutarse únicamente después de haber aplicado las estrategias de recuperación autorizadas para el tipo de error correspondiente, salvo que la severidad del incidente justifique un escalamiento inmediato.

---

## Principios

### ESC-001. Escalamiento progresivo

Todo incidente deberá escalar únicamente al siguiente nivel disponible de tratamiento.

No se permitirán saltos injustificados entre niveles de escalamiento.

---

### ESC-002. Escalamiento justificado

Todo escalamiento deberá fundamentarse en evidencia objetiva obtenida durante el tratamiento del incidente.

---

### ESC-003. Escalamiento registrado

Cada evento de escalamiento deberá registrarse como parte del historial oficial del incidente.

---

### ESC-004. Escalamiento proporcional

El nivel de escalamiento deberá corresponder a la severidad, impacto y recuperabilidad del error.

---

### ESC-005. Continuidad operacional

Siempre que sea posible, el escalamiento deberá preservar la continuidad del resto de procesos independientes de la automatización.

---

## Niveles oficiales de escalamiento

### Nivel 1. Recuperación automática

El incidente continúa siendo tratado por los mecanismos automáticos de recuperación definidos para el proceso correspondiente.

Este nivel constituye el mecanismo inicial de tratamiento.

---

### Nivel 2. Recuperación especializada

Cuando la recuperación inicial no resulte suficiente, el incidente será transferido a mecanismos especializados del propio sistema.

Ejemplos:

- Cambio de estrategia de recuperación.
- Reprocesamiento.
- Reinicio controlado.
- Recuperación alternativa.

---

### Nivel 3. Escalamiento funcional

Cuando el incidente continúe sin resolverse, el tratamiento será transferido a otro componente funcional de la automatización.

Ejemplos:

- Procesos de recuperación.
- Componentes de supervisión.
- Procesos de validación adicionales.

---

### Nivel 4. Intervención del usuario

Cuando el sistema no disponga de información suficiente para resolver automáticamente el incidente o la decisión corresponda exclusivamente al usuario, el tratamiento deberá escalarse para solicitar su intervención.

La automatización deberá proporcionar toda la información necesaria para facilitar la decisión.

---

### Nivel 5. Finalización controlada

Cuando ninguna estrategia resulte viable, el proceso deberá finalizar de forma controlada, preservando toda la información generada durante el tratamiento del incidente.

---

## Condiciones de escalamiento

El incidente deberá escalarse cuando ocurra cualquiera de las siguientes condiciones:

### CES-001

Se agoten todas las estrategias de recuperación autorizadas.

---

### CES-002

Se alcance el número máximo permitido de reintentos.

---

### CES-003

El error sea clasificado como no recuperable.

---

### CES-004

La severidad del incidente aumente durante su tratamiento.

---

### CES-005

Se detecte riesgo para la integridad de la información.

---

### CES-006

El modelo de decisiones determine que el sistema no puede continuar automáticamente.

---

### CES-007

Sea necesaria una decisión reservada exclusivamente al usuario.

---

## Información obligatoria del escalamiento

Todo evento de escalamiento deberá registrar, como mínimo:

- Identificador del incidente.
- Fecha y hora.
- Nivel de escalamiento.
- Motivo del escalamiento.
- Estrategias ejecutadas previamente.
- Resultado de dichas estrategias.
- Estado actual del incidente.
- Destinatario del escalamiento.

---

## Reglas generales

- Todo escalamiento deberá conservar su trazabilidad completa.
- Ningún incidente podrá permanecer indefinidamente en un mismo nivel de escalamiento.
- El escalamiento nunca deberá eliminar información previamente registrada.
- La finalización controlada constituirá el último nivel oficial de tratamiento.
- La incorporación de nuevos niveles de escalamiento requerirá la actualización oficial de este documento.
- Ningún componente podrá implementar mecanismos de escalamiento incompatibles con las reglas aquí definidas.

---

# 17. Trazabilidad y auditoría de errores

La trazabilidad y auditoría de errores establece el conjunto de reglas oficiales para registrar, conservar y reconstruir el ciclo de vida completo de cualquier incidente ocurrido durante la ejecución de la automatización.

Su propósito es garantizar que toda condición de error pueda analizarse posteriormente, identificando su origen, evolución, tratamiento, recuperación y resultado final, preservando la integridad de la evidencia generada durante todo el proceso.

Las disposiciones de este capítulo complementan las reglas generales de trazabilidad definidas en el Documento 4 — Flujo de Datos y las convenciones establecidas en el Documento 5 — Estándares del Proyecto, especializándolas para el manejo de incidentes.

---

## Principios

### TAE-001. Trazabilidad completa

Todo incidente deberá conservar un historial continuo desde su detección hasta su cierre definitivo.

---

### TAE-002. Inmutabilidad del historial

Los registros históricos de un incidente no podrán eliminarse ni modificarse de forma que alteren la evidencia original.

Las correcciones deberán registrarse como nuevos eventos.

---

### TAE-003. Evidencia objetiva

Toda acción realizada sobre un incidente deberá sustentarse mediante información verificable.

---

### TAE-004. Auditoría permanente

Toda la información relacionada con un incidente deberá permanecer disponible durante el período de conservación definido por el proyecto.

---

### TAE-005. Integridad del historial

Las relaciones entre incidentes, procesos, ofertas y componentes deberán mantenerse completas durante todo el ciclo de vida del sistema.

---

## Información trazable

Como mínimo, la automatización deberá conservar la siguiente información para cada incidente.

### TRA-001. Identificación

- Identificador del incidente.
- Identificador del error.
- Identificador de la ejecución.

---

### TRA-002. Contexto

- Fecha y hora.
- Módulo.
- Proceso.
- Componente.
- Estado del proceso.

---

### TRA-003. Clasificación

- Categoría.
- Severidad.
- Fuente.
- Recuperabilidad.

---

### TRA-004. Evidencia

- Información disponible.
- Mensajes generados.
- Valores relevantes.
- Resultado de las validaciones.

---

### TRA-005. Tratamiento

- Estrategias de recuperación ejecutadas.
- Reintentos realizados.
- Escalamientos efectuados.
- Intervenciones del usuario.

---

### TRA-006. Resultado

- Estado final.
- Resultado de la recuperación.
- Motivo del cierre.
- Fecha de finalización.

---

## Eventos auditables

Como mínimo, deberán registrarse los siguientes eventos.

### AUD-001

Detección del incidente.

---

### AUD-002

Clasificación del error.

---

### AUD-003

Registro oficial.

---

### AUD-004

Cambio de severidad.

---

### AUD-005

Inicio de recuperación.

---

### AUD-006

Resultado de la recuperación.

---

### AUD-007

Cada reintento ejecutado.

---

### AUD-008

Cada escalamiento.

---

### AUD-009

Intervención del usuario.

---

### AUD-010

Cambio de estado del incidente.

---

### AUD-011

Cierre definitivo.

---

## Relaciones auditables

Todo incidente deberá poder relacionarse, cuando corresponda, con:

- La oferta afectada.
- La ejecución donde ocurrió.
- El módulo responsable.
- El componente involucrado.
- El proceso correspondiente.
- Las decisiones tomadas.
- Las estrategias de recuperación aplicadas.
- Los registros asociados.
- Las notificaciones emitidas.
- Las alertas generadas.

---

## Conservación del historial

La información histórica de los incidentes deberá conservarse conforme a las políticas oficiales de almacenamiento definidas para el proyecto.

La eliminación, consolidación o archivado de registros únicamente podrá realizarse mediante procedimientos oficialmente documentados.

---

## Reglas generales

- Todo incidente deberá poder reconstruirse completamente a partir de su historial.
- Ninguna acción realizada sobre un incidente podrá quedar sin registrar.
- Toda modificación del estado de un incidente deberá conservar evidencia.
- La auditoría deberá mantenerse independiente de la tecnología utilizada para implementar la automatización.
- Los mecanismos de auditoría no podrán alterar el comportamiento operativo del sistema.
- Ningún componente podrá implementar reglas de trazabilidad incompatibles con las definidas en este documento.

---

# 18. Restricciones del manejo de errores

Las restricciones definidas en este capítulo establecen los límites operativos que deberán respetar todos los mecanismos de detección, clasificación, recuperación, registro, auditoría y tratamiento de errores de la automatización.

Su propósito es preservar la consistencia del modelo de manejo de errores, evitar comportamientos no autorizados y garantizar que todos los componentes de la automatización operen bajo un conjunto único de reglas.

Las siguientes restricciones serán de cumplimiento obligatorio para todos los módulos presentes y futuros del proyecto.

---

## Restricciones generales

### RME-001

Ningún error podrá permanecer sin detectar cuando existan mecanismos técnicos razonables para identificarlo.

---

### RME-002

Ningún error detectado podrá omitirse del registro oficial de incidentes.

---

### RME-003

No se permitirá eliminar registros históricos de incidentes.

Toda modificación deberá conservar la trazabilidad correspondiente.

---

### RME-004

Ningún componente podrá implementar mecanismos propios de clasificación que contradigan las categorías oficiales definidas en este documento.

---

### RME-005

Los niveles oficiales de severidad no podrán modificarse dinámicamente por criterios subjetivos.

Toda modificación deberá estar respaldada por evidencia objetiva.

---

### RME-006

No podrán ejecutarse estrategias de recuperación no autorizadas por este documento.

---

### RME-007

No se permitirán ciclos infinitos de recuperación o reintentos.

Todo proceso deberá poseer una condición oficial de finalización o escalamiento.

---

### RME-008

Ningún mecanismo de recuperación podrá comprometer la integridad, consistencia o trazabilidad de la información.

---

### RME-009

Los errores no podrán utilizarse como mecanismo de control normal del flujo funcional.

Las excepciones deberán representar únicamente condiciones anómalas.

---

### RME-010

Las respuestas del modelo de lenguaje no podrán utilizarse sin superar las validaciones oficiales definidas para dicho componente.

---

### RME-011

Los errores provenientes de servicios externos no deberán asumirse como permanentes sin haber ejecutado las políticas oficiales de recuperación autorizadas.

---

### RME-012

Las validaciones de datos no podrán deshabilitarse para acelerar el procesamiento de la automatización.

---

### RME-013

Ningún incidente podrá permanecer indefinidamente en estado abierto.

Todo incidente deberá finalizar mediante recuperación, escalamiento o cierre controlado.

---

### RME-014

Las notificaciones y alertas no podrán generarse sin una condición objetiva previamente registrada.

---

### RME-015

Las acciones ejecutadas durante el tratamiento de un incidente deberán poder reconstruirse completamente mediante la información registrada.

---

### RME-016

La incorporación de nuevos tipos de errores, estrategias de recuperación, políticas de reintento o mecanismos de auditoría únicamente podrá realizarse mediante una actualización oficial de este documento.

---

### RME-017

Ningún módulo podrá implementar reglas particulares de manejo de errores que contradigan las disposiciones establecidas en este documento.

---

### RME-018

El modelo de manejo de errores deberá mantenerse independiente del lenguaje de programación, herramientas, plataformas o tecnologías utilizadas para implementar la automatización.

---

## Reglas generales

- Todas las restricciones definidas en este capítulo serán obligatorias para cualquier implementación del proyecto.
- Las excepciones únicamente podrán aprobarse mediante una actualización oficial de la documentación.
- Toda desviación respecto a estas restricciones deberá documentarse, justificarse y conservar su trazabilidad.
- Ningún componente podrá operar fuera de las restricciones establecidas en este documento.

---

# 19. Criterios de aceptación

Los criterios de aceptación definen las condiciones mínimas que deberá cumplir cualquier implementación del modelo de manejo de errores para considerarse conforme con las disposiciones establecidas en este documento.

Su propósito es proporcionar un conjunto de verificaciones objetivas que permitan validar que el sistema implementa correctamente los mecanismos de detección, clasificación, recuperación, registro, auditoría y tratamiento de incidentes.

Todos los criterios definidos en este capítulo serán de cumplimiento obligatorio.

---

## Criterios generales

### CAE-001

La automatización deberá implementar un mecanismo oficial para detectar errores en todos los módulos del sistema.

---

### CAE-002

Todo error detectado deberá clasificarse utilizando exclusivamente las categorías oficiales definidas en este documento.

---

### CAE-003

Todo incidente deberá registrarse antes de ejecutar cualquier estrategia de recuperación.

---

### CAE-004

Todo registro de incidente deberá contener la información mínima obligatoria definida para el modelo de registro de errores.

---

### CAE-005

Todo error deberá recibir un nivel oficial de severidad antes de iniciar su tratamiento.

---

### CAE-006

Toda estrategia de recuperación deberá corresponder a una estrategia oficial del catálogo definido en este documento.

---

### CAE-007

Toda política de reintento deberá cumplir las restricciones establecidas para los reintentos oficiales.

---

### CAE-008

La automatización deberá impedir la ejecución de ciclos infinitos de recuperación o reintentos.

---

### CAE-009

Toda interacción con recursos externos deberá aplicar las reglas oficiales para el manejo de errores externos.

---

### CAE-010

Toda respuesta proveniente del modelo de lenguaje deberá superar las validaciones oficiales antes de utilizarse dentro del sistema.

---

### CAE-011

Toda información utilizada durante el procesamiento deberá cumplir las validaciones oficiales de calidad de datos.

---

### CAE-012

Toda notificación y toda alerta deberán estar asociadas a un incidente oficialmente registrado.

---

### CAE-013

Todo evento de escalamiento deberá conservar su historial completo.

---

### CAE-014

La trazabilidad deberá permitir reconstruir completamente el ciclo de vida de cualquier incidente.

---

### CAE-015

Toda modificación realizada sobre un incidente deberá conservar evidencia suficiente para auditoría.

---

### CAE-016

Ningún mecanismo implementado podrá contradecir las restricciones establecidas en este documento.

---

### CAE-017

Todos los módulos de la automatización deberán utilizar el modelo oficial de manejo de errores definido en este documento.

---

### CAE-018

Las implementaciones deberán mantener independencia respecto al lenguaje de programación, plataforma o tecnología utilizada.

---

### CAE-019

Las pruebas funcionales deberán demostrar que cada estrategia oficial de recuperación puede ejecutarse correctamente cuando corresponda.

---

### CAE-020

Las pruebas de integración deberán verificar que el manejo de errores preserve la integridad del flujo de datos y la consistencia de la información durante todo el ciclo de vida del incidente.

---

## Validación del documento

Se considerará que la implementación cumple este documento únicamente cuando:

- Todos los criterios anteriores hayan sido verificados satisfactoriamente.
- No existan incumplimientos respecto a las reglas oficiales del manejo de errores.
- Las evidencias de validación se encuentren disponibles para auditoría.
- La documentación de implementación mantenga consistencia con el presente documento.

---

# 20. Índice de reglas de manejo de errores

El presente índice consolida todos los identificadores oficiales definidos en este documento.

Su propósito es facilitar la consulta, referencia cruzada, implementación y mantenimiento del modelo de manejo de errores, proporcionando un punto único de acceso a todas las reglas oficiales.

---

# 2. Principios del manejo de errores

| Prefijo | Descripción |
|----------|-------------|
| PME | Principios del manejo de errores |

---

# 3. Arquitectura del manejo de errores

| Prefijo | Descripción |
|----------|-------------|
| AME | Arquitectura del manejo de errores |

---

# 4. Clasificación de errores

| Prefijo | Descripción |
|----------|-------------|
| CE | Criterios de clasificación |
| CER | Categorías oficiales de errores |
| ER | Identificador oficial de errores |

---

# 5. Fuentes de error

| Prefijo | Descripción |
|----------|-------------|
| FDE | Fuentes de error |

---

# 6. Detección de errores

| Prefijo | Descripción |
|----------|-------------|
| PDE | Principios de detección |
| MDE | Mecanismos oficiales de detección |

---

# 7. Registro de errores

| Prefijo | Descripción |
|----------|-------------|
| RER | Registro oficial de errores |

---

# 8. Niveles de severidad

| Prefijo | Descripción |
|----------|-------------|
| NSE | Criterios de evaluación de severidad |
| SV | Niveles oficiales de severidad |
| RSE | Reglas de asignación de severidad |

---

# 9. Estrategias de recuperación

| Prefijo | Descripción |
|----------|-------------|
| PRE | Principios de recuperación |
| REC | Estrategias oficiales de recuperación |
| SRE | Criterios de selección de estrategias |

---

# 10. Políticas de reintento

| Prefijo | Descripción |
|----------|-------------|
| PRT | Principios de reintento |
| POL-RET | Políticas oficiales de reintento |

---

# 11. Manejo de errores por módulo

No se definieron prefijos específicos para este capítulo, ya que reutiliza las categorías, estrategias y políticas oficiales establecidas previamente.

---

# 12. Manejo de errores externos

| Prefijo | Descripción |
|----------|-------------|
| MEE | Principios del manejo de errores externos |
| EEX | Tipos oficiales de errores externos |

---

# 13. Manejo de errores del modelo de lenguaje (LLM)

| Prefijo | Descripción |
|----------|-------------|
| MLLM | Principios del manejo de errores del modelo de lenguaje |
| ELLM | Tipos oficiales de errores del modelo de lenguaje |
| VLLM | Validaciones oficiales del modelo de lenguaje |

---

# 14. Manejo de errores de datos

| Prefijo | Descripción |
|----------|-------------|
| MED | Principios del manejo de errores de datos |
| EDATA | Tipos oficiales de errores de datos |
| VDAT | Validaciones oficiales de datos |

---

# 15. Notificaciones y alertas

| Prefijo | Descripción |
|----------|-------------|
| NAL | Principios de notificaciones y alertas |
| ALT | Niveles oficiales de alerta |

---

# 16. Escalamiento de errores

| Prefijo | Descripción |
|----------|-------------|
| ESC | Principios de escalamiento |
| CES | Condiciones oficiales de escalamiento |

---

# 17. Trazabilidad y auditoría de errores

| Prefijo | Descripción |
|----------|-------------|
| TAE | Principios de trazabilidad y auditoría |
| TRA | Información trazable |
| AUD | Eventos auditables |

---

# 18. Restricciones del manejo de errores

| Prefijo | Descripción |
|----------|-------------|
| RME | Restricciones del manejo de errores |

---

# 19. Criterios de aceptación

| Prefijo | Descripción |
|----------|-------------|
| CAE | Criterios de aceptación |

---

# Resumen general de prefijos oficiales

| Prefijo | Significado |
|----------|-------------|
| PME | Principios del manejo de errores |
| AME | Arquitectura del manejo de errores |
| CE | Criterios de clasificación |
| CER | Categorías oficiales de errores |
| ER | Identificador oficial de errores |
| FDE | Fuentes de error |
| PDE | Principios de detección |
| MDE | Mecanismos de detección |
| RER | Registro de errores |
| NSE | Criterios de severidad |
| SV | Niveles de severidad |
| RSE | Reglas de severidad |
| PRE | Principios de recuperación |
| REC | Estrategias de recuperación |
| SRE | Selección de estrategias |
| PRT | Principios de reintento |
| POL-RET | Políticas de reintento |
| MEE | Manejo de errores externos |
| EEX | Errores externos |
| MLLM | Principios del LLM |
| ELLM | Errores del LLM |
| VLLM | Validaciones del LLM |
| MED | Principios de datos |
| EDATA | Errores de datos |
| VDAT | Validaciones de datos |
| NAL | Notificaciones y alertas |
| ALT | Niveles de alerta |
| ESC | Principios de escalamiento |
| CES | Condiciones de escalamiento |
| TAE | Principios de trazabilidad y auditoría |
| TRA | Información trazable |
| AUD | Eventos auditables |
| RME | Restricciones |
| CAE | Criterios de aceptación |
