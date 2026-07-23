# Documento 1
# Requisitos funcionales

## 1. Propósito del sistema

Desarrollar una automatización integral que descubra, recopile, procese, evalúe y gestione ofertas de empleo de forma autónoma en todas las tareas repetitivas del proceso.

El sistema deberá transformar las ofertas encontradas en información estructurada, evaluarlas según criterios previamente definidos y generar todos los insumos necesarios para facilitar y acelerar el proceso de postulación.

La automatización actuará como un asistente inteligente especializado en la búsqueda de empleo, automatizando las actividades repetitivas y operativas, mientras que las decisiones estratégicas o de mayor impacto permanecerán bajo el control del usuario.

---

## 2. Objetivo general

Diseñar e implementar una automatización modular, escalable y mantenible que permita gestionar de manera integral el proceso de búsqueda de empleo, desde el descubrimiento de oportunidades hasta la generación de los insumos necesarios para la postulación, automatizando las tareas repetitivas y proporcionando al usuario información estructurada y análisis que faciliten la toma de decisiones.

---

## 3. Objetivos específicos

1. Descubrir automáticamente oportunidades de empleo desde las fuentes de información definidas.

2. Centralizar todas las ofertas encontradas en un único repositorio estructurado, evitando duplicados y manteniendo su historial.

3. Preparar cada oferta mediante procesos de limpieza, normalización y validación de la información extraída.

4. Evaluar automáticamente las ofertas utilizando criterios previamente definidos para identificar su nivel de compatibilidad con el perfil del usuario.

5. Clasificar las ofertas según su prioridad y estado dentro del flujo de procesamiento.

6. Analizar en profundidad las ofertas que superen la evaluación inicial para generar información útil para la postulación.

7. Generar automáticamente los insumos necesarios para apoyar el proceso de candidatura, de acuerdo con las características de cada oferta.

8. Mantener un registro completo del ciclo de vida de cada oferta, incluyendo cambios de estado, decisiones y resultados obtenidos.

9. Proporcionar al usuario información clara, organizada y suficiente para apoyar la toma de decisiones en cada etapa del proceso.

10. Reducir el tiempo y el esfuerzo dedicados a las tareas repetitivas de la búsqueda de empleo mediante procesos automatizados.

11. Permitir la incorporación de nuevas fuentes de empleo, reglas de evaluación y funcionalidades sin afectar el funcionamiento de los componentes existentes.

---

## 4. Alcance funcional

La automatización abarcará las siguientes capacidades funcionales:

### 4.1 Descubrimiento de oportunidades

- Consultar las fuentes de empleo previamente configuradas.
- Detectar nuevas ofertas de empleo.
- Extraer la información disponible de cada oferta.
- Registrar las ofertas encontradas.

### 4.2 Preparación de ofertas

- Limpiar y normalizar la información extraída.
- Validar la integridad de los datos.
- Detectar y eliminar ofertas duplicadas.
- Asignar el estado inicial de procesamiento.

### 4.3 Evaluación inicial

- Analizar automáticamente cada oferta según los criterios definidos.
- Calcular una puntuación de compatibilidad.
- Clasificar las ofertas por prioridad.
- Descartar automáticamente las ofertas que incumplan reglas previamente establecidas.

### 4.4 Procesamiento profundo

- Analizar detalladamente las ofertas seleccionadas.
- Identificar requisitos, responsabilidades, beneficios y demás información relevante.
- Generar información estructurada para apoyar la preparación de la candidatura.
- Preparar los insumos definidos para el proceso de postulación.

### 4.5 Gestión del proceso

- Mantener el historial completo de cada oferta.
- Administrar los estados del flujo de procesamiento.
- Registrar decisiones y resultados.
- Permitir el seguimiento de cada oferta durante su ciclo de vida.

### 4.6 Administración

- Permitir la configuración de fuentes de empleo.
- Permitir la actualización de criterios de evaluación.
- Permitir la incorporación de nuevas reglas y funcionalidades sin afectar los componentes existentes.

## Fuera del alcance

La automatización no tendrá como responsabilidad:

- Tomar decisiones estratégicas que deban ser aprobadas por el usuario.
- Modificar el perfil profesional del usuario sin autorización.
- Enviar postulaciones automáticamente sin que dicha funcionalidad haya sido aprobada e implementada explícitamente.
- Sustituir el criterio del usuario en decisiones de alto impacto.
- Realizar actividades ajenas al proceso de búsqueda y preparación de oportunidades laborales.

---

## 5. Funciones principales del sistema

El sistema deberá proporcionar las siguientes funciones principales:

### F1. Descubrimiento de oportunidades

- Consultar automáticamente las fuentes de empleo configuradas.
- Detectar nuevas ofertas disponibles.
- Extraer la información relevante de cada oferta.
- Registrar la fecha, hora y fuente de descubrimiento.

---

### F2. Gestión de ofertas

- Crear un registro único para cada oferta.
- Detectar y evitar registros duplicados.
- Actualizar la información cuando una oferta cambie.
- Mantener el historial de modificaciones.

---

### F3. Preparación de la información

- Limpiar los datos extraídos.
- Normalizar formatos y estructuras.
- Completar información derivada cuando sea posible.
- Validar la calidad de los datos obtenidos.

---

### F4. Evaluación automática

- Analizar las ofertas utilizando criterios previamente definidos.
- Calcular una puntuación de compatibilidad.
- Clasificar las ofertas según su prioridad.
- Identificar automáticamente ofertas descartables.

---

### F5. Procesamiento profundo

- Analizar el contenido completo de las ofertas.
- Identificar requisitos técnicos y funcionales.
- Extraer responsabilidades, beneficios y condiciones.
- Generar información estructurada para apoyar la postulación.

---

### F6. Generación de insumos

- Generar los documentos, análisis o recursos definidos para apoyar cada candidatura.
- Organizar los insumos generados por oferta.
- Mantener la trazabilidad entre cada insumo y su oferta correspondiente.

---

### F7. Gestión del flujo

- Controlar el estado de cada oferta durante todo su ciclo de vida.
- Registrar cada transición de estado.
- Registrar decisiones automáticas y decisiones del usuario.
- Permitir reanudar procesos interrumpidos.

---

### F8. Administración

- Gestionar las fuentes de empleo.
- Gestionar los criterios de evaluación.
- Gestionar configuraciones generales del sistema.
- Gestionar catálogos, reglas y parámetros.

---

### F9. Consulta y seguimiento

- Permitir consultar el historial completo de las ofertas.
- Visualizar el estado actual de cada oferta.
- Consultar resultados de evaluaciones.
- Consultar información generada durante el procesamiento.

---

### F10. Registro y auditoría

- Registrar los eventos relevantes del sistema.
- Registrar errores y excepciones.
- Registrar decisiones automáticas.
- Mantener trazabilidad completa del procesamiento de cada oferta.

---

## 6. Funciones fuera del alcance

La automatización no tendrá como responsabilidad las siguientes funciones, salvo que en futuras versiones del proyecto se apruebe expresamente su incorporación:

### FNA-1. Postulación automática

No enviará postulaciones automáticamente a ofertas de empleo sin la aprobación explícita del usuario.

---

### FNA-2. Toma de decisiones estratégicas

No reemplazará el criterio del usuario en decisiones de alto impacto, incluyendo, entre otras:

- Elegir a qué empresa postularse.
- Decidir si una oportunidad es conveniente por motivos personales.
- Modificar criterios profesionales sin autorización.

---

### FNA-3. Modificación del perfil profesional

No realizará cambios automáticos sobre la información profesional del usuario, tales como:

- Hoja de vida.
- Portafolio.
- Perfil profesional.
- Información personal.
- Preferencias laborales.

---

### FNA-4. Comunicación con terceros

No enviará correos electrónicos, mensajes o cualquier otro tipo de comunicación externa en nombre del usuario, excepto cuando dicha funcionalidad haya sido diseñada, implementada y autorizada explícitamente.

---

### FNA-5. Gestión de entrevistas

No programará entrevistas, aceptará invitaciones ni responderá procesos de selección de forma automática.

---

### FNA-6. Actividades ajenas al proceso

No ejecutará tareas que no estén directamente relacionadas con el descubrimiento, análisis, evaluación, preparación y gestión de oportunidades laborales.

---

### FNA-7. Aprendizaje autónomo

No modificará por sí mismo las reglas de negocio, criterios de evaluación o configuraciones del sistema sin intervención del usuario.

---

## 7. Actores del sistema

Los actores representan las personas o sistemas que interactúan directa o indirectamente con la automatización.

Actores y dependencias externas:

- Usuario

Dependencias externas

- Plataformas de empleo
- Modelo de IA
- Base de datos
- Navegador
- Sistema de archivos
- APIs
---

### A1. Usuario

Es el propietario y operador de la automatización.

Responsabilidades:

- Configurar el sistema.
- Definir criterios de evaluación.
- Autorizar las decisiones que requieran intervención humana.
- Revisar los resultados generados.
- Actualizar su información profesional cuando sea necesario.

---

### A2. Plataformas de empleo

Corresponde a las fuentes desde las cuales la automatización obtiene las oportunidades laborales.

Ejemplos:

- LinkedIn
- Indeed
- Computrabajo
- Magneto
- Sitios de empleo corporativos
- Otras fuentes configuradas por el usuario.

Responsabilidades:

- Publicar ofertas de empleo.
- Proporcionar la información disponible para su procesamiento.

---

### A3. Modelo de Inteligencia Artificial

Corresponde al servicio de IA utilizado por la automatización para analizar y generar información.

Responsabilidades:

- Analizar ofertas.
- Extraer información relevante.
- Clasificar contenido.
- Generar análisis.
- Apoyar la generación de insumos para la candidatura.

---

### A4. Servicios externos

Corresponde a cualquier servicio utilizado como apoyo durante el funcionamiento de la automatización.

Ejemplos:

- Almacenamiento.
- Bases de datos.
- Servicios de archivos.
- Herramientas de automatización.
- APIs auxiliares.

Responsabilidades:

- Almacenar información.
- Facilitar la comunicación entre componentes.
- Proporcionar servicios de apoyo al sistema.

---

## 8. Entradas del sistema

Las entradas del sistema corresponden a toda la información necesaria para ejecutar los procesos de descubrimiento, evaluación, procesamiento y gestión de oportunidades laborales.

### E-001. Configuración del usuario

Información definida por el usuario para personalizar el funcionamiento de la automatización.

Incluye, entre otros:

- Fuentes de empleo.
- Frecuencia de ejecución.
- Preferencias generales.
- Parámetros de configuración.

---

### E-002. Perfil profesional

Información utilizada para evaluar la compatibilidad entre el usuario y las ofertas de empleo.

Incluye:

- Hoja de vida.
- Perfil profesional.
- Experiencia laboral.
- Habilidades.
- Tecnologías.
- Idiomas.
- Certificaciones.
- Formación académica.
- Preferencias laborales.
- Expectativa salarial.
- Modalidad de trabajo.
- Ubicación.
- Empresas objetivo.
- Empresas restringidas.

---

### E-003. Ofertas de empleo

Información obtenida desde las diferentes plataformas de empleo.

Puede incluir:

- Título.
- Empresa.
- Descripción.
- Requisitos.
- Responsabilidades.
- Beneficios.
- Salario.
- Modalidad.
- Ubicación.
- Fecha de publicación.
- URL.
- Identificador de la oferta.
- Plataforma de origen.

---

### E-004. Reglas de negocio

Conjunto de criterios definidos para controlar el comportamiento de la automatización.

Incluye:

- Reglas de evaluación.
- Reglas de descarte.
- Reglas de aceptación.
- Prioridades.
- Umbrales.
- Excepciones.

---

### E-005. Prompts y configuraciones de IA

Conjunto de instrucciones utilizadas para solicitar análisis y generación de información al modelo de inteligencia artificial.

Incluye:

- Prompts.
- Plantillas.
- Parámetros de ejecución.
- Configuraciones de procesamiento.

---

### E-006. Información histórica

Información generada por ejecuciones anteriores.

Incluye:

- Historial de ofertas.
- Estados anteriores.
- Resultados de evaluaciones.
- Documentos generados.
- Registros de ejecución.
- Decisiones del usuario.

---

### E-007. Decisiones del usuario

Información ingresada por el usuario durante el proceso cuando una decisión no puede ser tomada automáticamente.

Ejemplos:

- Aprobar una oferta.
- Rechazar una oferta.
- Solicitar un nuevo análisis.
- Modificar criterios.
- Reanudar un proceso.

---

## 9. Datos internos del sistema

Los datos internos corresponden a toda la información generada, transformada y mantenida por la automatización para controlar el procesamiento de las ofertas y garantizar la consistencia del sistema.

### DI-001. Identificadores internos

Información utilizada para identificar de forma única los elementos del sistema.

Incluye:

- ID interno de la oferta.
- ID de procesamiento.
- ID de ejecución.
- ID de análisis.
- ID de documentos generados.

---

### DI-002. Estado del procesamiento

Información utilizada para controlar el avance de cada oferta dentro del flujo de trabajo.

Incluye:

- Estado actual.
- Estado anterior.
- Fecha de cambio.
- Motivo del cambio.
- Responsable del cambio (usuario o sistema).

---

### DI-003. Resultados intermedios

Información generada durante las diferentes etapas del procesamiento.

Ejemplos:

- Puntuaciones parciales.
- Clasificaciones temporales.
- Información extraída.
- Datos normalizados.
- Resultados de validaciones.

---

### DI-004. Configuración operativa

Información utilizada por la automatización durante su ejecución.

Incluye:

- Parámetros internos.
- Variables de ejecución.
- Configuración de módulos.
- Configuración de flujos.
- Umbrales internos.

---

### DI-005. Historial del sistema

Información utilizada para garantizar la trazabilidad del procesamiento.

Incluye:

- Historial de cambios.
- Historial de evaluaciones.
- Historial de decisiones.
- Historial de reprocesamientos.

---

### DI-006. Métricas de ejecución

Información utilizada para medir el funcionamiento de la automatización.

Incluye:

- Tiempo de ejecución.
- Duración por módulo.
- Número de ofertas procesadas.
- Número de errores.
- Número de reintentos.
- Indicadores de rendimiento.

---

### DI-007. Relaciones internas

Información utilizada para relacionar los diferentes elementos del sistema.

Ejemplos:

- Oferta ↔ Evaluaciones.
- Oferta ↔ Documentos.
- Oferta ↔ Historial.
- Oferta ↔ Decisiones.
- Oferta ↔ Ejecuciones.

---

## 10. Salidas del sistema

Las salidas del sistema corresponden a toda la información generada por la automatización como resultado del procesamiento de las ofertas de empleo.

### S-001. Ofertas estructuradas

Información normalizada de cada oferta, lista para ser utilizada por los diferentes procesos de la automatización.

Incluye, entre otros:

- Información limpia.
- Campos normalizados.
- Datos validados.
- Identificadores internos.

---

### S-002. Resultado de la evaluación inicial

Información obtenida durante el análisis automático de compatibilidad.

Incluye:

- Puntuación.
- Nivel de compatibilidad.
- Prioridad.
- Motivos de aceptación.
- Motivos de descarte.
- Recomendaciones.

---

### S-003. Análisis profundo de la oferta

Información obtenida durante el procesamiento detallado de la vacante.

Incluye:

- Resumen ejecutivo.
- Requisitos identificados.
- Competencias técnicas.
- Competencias blandas.
- Responsabilidades.
- Beneficios.
- Riesgos.
- Observaciones relevantes.

---

### S-004. Insumos para la candidatura

Recursos generados para facilitar la preparación de una postulación.

Podrán incluir:

- Análisis estratégicos.
- Información organizada.
- Documentos definidos para cada oferta.
- Otros recursos aprobados durante el desarrollo del proyecto.

---

### S-005. Estado de la oferta

Información actualizada sobre la situación de cada oferta dentro del flujo de procesamiento.

Incluye:

- Estado actual.
- Fecha de actualización.
- Historial de cambios.
- Responsable de la última decisión.

---

### S-006. Reportes

Información consolidada sobre el funcionamiento de la automatización.

Puede incluir:

- Número de ofertas encontradas.
- Número de ofertas descartadas.
- Número de ofertas priorizadas.
- Tiempo de procesamiento.
- Indicadores de ejecución.
- Estadísticas generales.

---

### S-007. Registros del sistema

Información utilizada para auditoría y seguimiento.

Incluye:

- Eventos.
- Errores.
- Advertencias.
- Decisiones automáticas.
- Decisiones del usuario.
- Historial de ejecución.

---

## 11. Flujo funcional general

El sistema gestionará cada oferta de empleo siguiendo un flujo funcional compuesto por las siguientes etapas:

### FF-01. Descubrimiento

- Consultar las fuentes de empleo configuradas.
- Detectar nuevas ofertas.
- Extraer la información disponible.
- Registrar la oferta en el sistema.

↓

### FF-02. Preparación

- Limpiar la información.
- Normalizar los datos.
- Validar la integridad de la oferta.
- Detectar duplicados.
- Asignar el estado inicial.

↓

### FF-03. Evaluación inicial

- Analizar la compatibilidad con el perfil profesional.
- Aplicar reglas de descarte.
- Calcular la puntuación inicial.
- Clasificar la prioridad.

↓

### FF-04. Decisión inicial

Si la oferta no cumple los criterios mínimos:

→ Finaliza el procesamiento.

Si cumple los criterios:

→ Continúa al procesamiento profundo.

↓

### FF-05. Procesamiento profundo

- Analizar detalladamente la vacante.
- Identificar requisitos.
- Identificar competencias.
- Analizar responsabilidades.
- Analizar beneficios.
- Generar información estructurada.

↓

### FF-06. Generación de insumos

- Preparar los recursos definidos para apoyar la candidatura.
- Organizar los resultados obtenidos.
- Asociar los insumos con la oferta correspondiente.

↓

### FF-07. Revisión del usuario

Cuando el flujo requiera una decisión estratégica:

- Presentar la información al usuario.
- Esperar la decisión correspondiente.
- Registrar la decisión tomada.

↓

### FF-08. Gestión y seguimiento

- Actualizar el estado de la oferta.
- Registrar el historial.
- Conservar la trazabilidad completa.
- Mantener disponible toda la información generada.

↓

### FF-09. Finalización

- Marcar el procesamiento como finalizado.
- Registrar la fecha de cierre.
- Conservar toda la información para consultas futuras.

---

## 12. Ciclo de vida de una oferta

Cada oferta de empleo seguirá un ciclo de vida compuesto por las siguientes etapas:

### CV-01. Descubierta

La oferta es localizada en una fuente de empleo y registrada por primera vez en el sistema.

---

### CV-02. Preparada

La información ha sido limpiada, normalizada, validada y está lista para ser evaluada.

---

### CV-03. Evaluada

La oferta ha sido analizada mediante las reglas de evaluación inicial y cuenta con una puntuación de compatibilidad.

---

### CV-04. Clasificada

La oferta ha sido categorizada según su prioridad y el resultado de la evaluación.

---

### CV-05. Procesada

La oferta ha sido analizada en profundidad y se ha generado toda la información necesaria para apoyar la candidatura.

---

### CV-06. Pendiente de decisión

La automatización ha finalizado las tareas que puede realizar de forma autónoma y requiere una decisión del usuario para continuar o finalizar el proceso.

---

### CV-07. Finalizada

La oferta ha completado su ciclo dentro de la automatización y toda la información relacionada ha sido registrada para futuras consultas.

---

## 13. Catálogo de estados de una oferta

El sistema controlará el ciclo de vida de cada oferta mediante un conjunto de estados predefinidos.

### EST-001. Descubierta

**Descripción**

La oferta ha sido identificada en una fuente de empleo y registrada por primera vez.

**Proceso funcional**

PF-01 — Descubrimiento

**Asignado por**

Sistema

**Estados anteriores**

Ninguno

**Estados siguientes**

- EST-002 Preparada
- EST-999 Error

---

### EST-002. Preparada

**Descripción**

La información fue limpiada, normalizada y validada.

**Proceso funcional**

PF-02 — Preparación

**Asignado por**

Sistema

**Estados anteriores**

- EST-001

**Estados siguientes**

- EST-003 Evaluada
- EST-999 Error

---

### EST-003. Evaluada

**Descripción**

La oferta fue evaluada mediante las reglas de negocio.

**Proceso funcional**

PF-03 — Evaluación inicial

**Asignado por**

Sistema

**Estados anteriores**

- EST-002

**Estados siguientes**

- EST-004 Clasificada
- EST-010 Descartada
- EST-999 Error

---

### EST-004. Clasificada

**Descripción**

La oferta fue priorizada según los resultados de la evaluación.

**Proceso funcional**

PF-03 — Evaluación inicial

**Asignado por**

Sistema

**Estados anteriores**

- EST-003

**Estados siguientes**

- EST-005 Procesamiento profundo
- EST-010 Descartada

---

### EST-005. Procesamiento profundo

**Descripción**

La oferta está siendo analizada en detalle.

**Proceso funcional**

PF-05

**Asignado por**

Sistema

**Estados siguientes**

- EST-006 Procesada
- EST-999 Error

---

### EST-006. Procesada

**Descripción**

El análisis profundo terminó correctamente.

**Proceso funcional**

PF-05

**Estados siguientes**

- EST-007 Insumos generados

---

### EST-007. Insumos generados

**Descripción**

Todos los recursos definidos para apoyar la candidatura fueron generados.

**Proceso funcional**

PF-06

**Estados siguientes**

- EST-008 Pendiente de decisión

---

### EST-008. Pendiente de decisión

**Descripción**

La automatización requiere una decisión del usuario.

**Proceso funcional**

PF-07

**Asignado por**

Sistema

**Estados siguientes**

- EST-009 Finalizada
- EST-010 Descartada

---

### EST-009. Finalizada

**Descripción**

La oferta terminó completamente su procesamiento.

**Proceso funcional**

PF-09

**Estado final**

Sí

---

### EST-010. Descartada

**Descripción**

La oferta dejó de procesarse porque no cumplió las reglas definidas o el usuario decidió descartarla.

**Estado final**

Sí

---

### EST-999. Error

**Descripción**

El procesamiento fue interrumpido por un error y requiere reintento o intervención.

**Estado final**

No

---

## 14. Decisiones automáticas

La automatización podrá tomar decisiones de manera autónoma únicamente cuando existan reglas previamente definidas y documentadas.

### DA-001. Descubrimiento de ofertas

- Detectar nuevas ofertas.
- Identificar si una oferta ya existe.
- Registrar nuevas oportunidades.

---

### DA-002. Preparación de la información

- Limpiar datos.
- Normalizar formatos.
- Validar campos obligatorios.
- Detectar información inconsistente.

---

### DA-003. Gestión de duplicados

- Identificar ofertas duplicadas.
- Relacionar registros equivalentes.
- Evitar el procesamiento repetido.

---

### DA-004. Evaluación inicial

- Calcular la puntuación de compatibilidad.
- Aplicar reglas de descarte.
- Asignar una prioridad.
- Clasificar la oferta.

---

### DA-005. Procesamiento profundo

- Analizar el contenido de la oferta.
- Extraer requisitos.
- Identificar competencias.
- Generar información estructurada.
- Elaborar análisis definidos por el sistema.

---

### DA-006. Generación de insumos

- Generar los recursos definidos para apoyar la candidatura.
- Organizar la información generada.
- Asociar cada recurso con la oferta correspondiente.

---

### DA-007. Gestión del flujo

- Cambiar el estado del ciclo de vida cuando se cumplan las condiciones establecidas.
- Actualizar el estado operativo.
- Registrar eventos.
- Registrar métricas.
- Registrar historial.

---

### DA-008. Recuperación operativa

- Reintentar procesos cuando exista una estrategia de recuperación definida.
- Continuar procesos interrumpidos.
- Marcar procesos que requieran intervención.

---

### Principio general

Toda decisión automática deberá ser:

- Reproducible.
- Trazable.
- Auditable.
- Basada en reglas documentadas.
- Reversible cuando sea técnicamente posible.

---

## 15. Decisiones que requieren intervención del usuario

Las siguientes decisiones deberán ser tomadas exclusivamente por el usuario, salvo que en una versión futura del proyecto se apruebe expresamente su automatización.

### DU-001. Aprobación de una oportunidad

Decidir si una oferta debe continuar siendo considerada como una oportunidad de interés.

---

### DU-002. Descarte manual

Descartar una oferta por motivos personales o estratégicos que no puedan ser determinados automáticamente.

Ejemplos:

- Preferencias personales.
- Cultura organizacional.
- Interés en la empresa.
- Información externa no disponible para el sistema.

---

### DU-003. Priorización excepcional

Modificar manualmente la prioridad asignada automáticamente por el sistema.

---

### DU-004. Aprobación de la candidatura

Autorizar la preparación final de una candidatura para una oferta específica.

---

### DU-005. Envío de postulaciones

Autorizar cualquier acción que implique enviar información del usuario a terceros.

Ejemplos:

- Enviar una hoja de vida.
- Completar un formulario de aplicación.
- Enviar un correo electrónico.
- Compartir documentos.

---

### DU-006. Modificación del perfil profesional

Autorizar cambios en:

- Hoja de vida.
- Perfil profesional.
- Portafolio.
- Información personal.
- Preferencias laborales.

---

### DU-007. Modificación de reglas del sistema

Aprobar cambios en:

- Reglas de evaluación.
- Reglas de descarte.
- Umbrales.
- Configuraciones críticas.
- Criterios de decisión.

---

### DU-008. Reprocesamiento excepcional

Autorizar el reprocesamiento de ofertas cuando el sistema detecte situaciones que no puedan resolverse automáticamente.

---

### Principio general

Toda decisión que implique consecuencias estratégicas, legales, personales o de representación del usuario deberá requerir su aprobación explícita antes de ejecutarse.

---

## 16. Reglas funcionales generales

Las siguientes reglas deberán cumplirse durante toda la operación de la automatización.

### RFG-001. Trazabilidad

Toda acción, decisión, recomendación y cambio de estado deberá quedar registrado.

---

### RFG-002. Identificación única

Toda oferta deberá contar con un identificador único e inmutable dentro del sistema.

---

### RFG-003. No duplicidad

Una misma oferta no podrá procesarse simultáneamente más de una vez.

---

### RFG-004. Integridad de la información

La automatización no deberá eliminar ni modificar información original obtenida de las fuentes de empleo.

Las transformaciones deberán realizarse sobre datos derivados o normalizados.

---

### RFG-005. Separación entre datos

Las entradas, los datos internos y las salidas deberán mantenerse como entidades conceptualmente independientes.

---

### RFG-006. Trazabilidad de documentos

Todo documento, análisis o recurso generado deberá poder relacionarse con la oferta que le dio origen.

---

### RFG-007. Control de estados

Toda oferta deberá encontrarse siempre en un único estado del ciclo de vida y en un único estado operativo.

No podrán existir estados incompatibles simultáneamente.

---

### RFG-008. Validación previa

Ningún proceso podrá ejecutarse si la oferta no cumple los requisitos mínimos definidos para esa etapa.

---

### RFG-009. Recuperación controlada

Cuando ocurra un error recuperable, el sistema deberá intentar resolverlo siguiendo la estrategia definida antes de solicitar intervención del usuario.

---

### RFG-010. Intervención del usuario

Las decisiones estratégicas únicamente podrán ejecutarse después de la autorización explícita del usuario.

---

### RFG-011. Consistencia del procesamiento

Cada oferta deberá recorrer el flujo funcional respetando las transiciones definidas para el ciclo de vida.

---

### RFG-012. Auditoría

Toda decisión automática deberá ser justificable mediante reglas documentadas.

---

### RFG-013. Configuración centralizada

Las reglas de negocio, parámetros y configuraciones deberán administrarse desde un único punto de configuración.

---

### RFG-014. Modularidad

Los componentes deberán diseñarse para minimizar dependencias entre sí y facilitar su mantenimiento, sustitución y ampliación.

---

### RFG-015. Escalabilidad

La incorporación de nuevas fuentes de empleo, reglas, módulos o funcionalidades no deberá requerir modificaciones significativas en los componentes existentes.

---

## 17. Catálogo de casos de uso

Los siguientes casos de uso representan las principales funcionalidades del sistema. La especificación detallada de cada uno se documentará en un documento independiente.

### Gestión de configuración

- CU-001 Configurar el sistema.
- CU-002 Configurar fuentes de empleo.
- CU-003 Configurar reglas de evaluación.
- CU-004 Configurar preferencias del usuario.

---

### Descubrimiento

- CU-005 Descubrir nuevas ofertas.
- CU-006 Registrar una oferta.
- CU-007 Detectar ofertas duplicadas.

---

### Preparación

- CU-008 Preparar una oferta.
- CU-009 Normalizar información.
- CU-010 Validar información.

---

### Evaluación

- CU-011 Evaluar una oferta.
- CU-012 Clasificar una oferta.
- CU-013 Descartar una oferta.

---

### Procesamiento profundo

- CU-014 Analizar una oferta.
- CU-015 Extraer requisitos.
- CU-016 Generar análisis.
- CU-017 Generar insumos para la candidatura.

---

### Gestión

- CU-018 Consultar una oferta.
- CU-019 Consultar el historial.
- CU-020 Consultar el estado de una oferta.
- CU-021 Reprocesar una oferta.
- CU-022 Registrar una decisión del usuario.

---

### Administración

- CU-023 Consultar métricas.
- CU-024 Consultar registros.
- CU-025 Gestionar configuraciones del sistema.

---

## 18. Restricciones funcionales

### RST-001

El sistema únicamente procesará ofertas provenientes de fuentes previamente configuradas.

---

### RST-002

Toda oferta deberá poseer un identificador único antes de iniciar su procesamiento.

---

### RST-003

No podrá existir más de un procesamiento activo para la misma oferta.

---

### RST-004

Ninguna oferta podrá avanzar a una etapa del flujo si no ha completado correctamente la etapa anterior, salvo que exista una regla documentada que lo permita.

---

### RST-005

Las decisiones estratégicas requerirán siempre autorización explícita del usuario.

---

### RST-006

Toda decisión automática deberá estar respaldada por una regla documentada.

---

### RST-007

Toda información generada deberá mantener trazabilidad con la oferta que la originó.

---

### RST-008

La automatización deberá preservar el historial completo de cada oferta.

---

### RST-009

Los errores deberán registrarse antes de iniciar cualquier proceso de recuperación.

---

### RST-010

El sistema deberá mantener la consistencia entre el estado del ciclo de vida y el estado operativo de cada oferta.

---

## 19. Criterios de aceptación

El sistema cumplirá los requisitos funcionales cuando se verifique que:

### CA-001

Es capaz de descubrir ofertas desde las fuentes configuradas.

---

### CA-002

Registra cada oferta con un identificador único.

---

### CA-003

Prepara y valida correctamente la información obtenida.

---

### CA-004

Evalúa automáticamente las ofertas utilizando las reglas definidas.

---

### CA-005

Genera la información necesaria para apoyar la candidatura.

---

### CA-006

Mantiene actualizado el estado del ciclo de vida y el estado operativo de cada oferta.

---

### CA-007

Registra todas las acciones, decisiones y recomendaciones realizadas durante el procesamiento.

---

### CA-008

Solicita la intervención del usuario cuando una decisión estratégica lo requiera.

---

### CA-009

Mantiene la trazabilidad completa de cada oferta durante todo su ciclo de vida.

---

### CA-010

Permite ampliar el sistema con nuevas fuentes, reglas y funcionalidades sin afectar el comportamiento de los componentes existentes.
