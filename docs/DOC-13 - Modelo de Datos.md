# Documento 13 - Modelo de Datos

## 1. Propósito del documento

El presente documento define el modelo de datos oficial de la automatización de búsqueda de empleo.

Su propósito es establecer, organizar y documentar la estructura lógica de la información utilizada por la automatización, garantizando que todas las entidades, atributos, relaciones, restricciones, reglas de integridad y mecanismos de persistencia sean consistentes con los objetivos, el alcance, los requisitos y la arquitectura definida para el proyecto.

Este documento constituye la referencia oficial para el diseño, implementación, mantenimiento y evolución del modelo de datos. Ningún elemento relacionado con la gestión de la información deberá incorporarse, modificarse o eliminarse sin haber sido previamente analizado y documentado conforme a los criterios establecidos en este documento.

Las decisiones aquí documentadas deberán mantener coherencia con los Documentos 0 al 12, incluyendo los requisitos funcionales y no funcionales, el modelo de decisiones, el flujo de datos, los estándares del proyecto, el modelo de manejo de errores, la arquitectura de carpetas, el alcance y objetivos, el stack tecnológico y la arquitectura general del sistema.

El modelo de datos deberá garantizar la integridad, consistencia, trazabilidad, mantenibilidad y escalabilidad de la información durante todo el ciclo de vida de las ofertas de empleo y de los procesos ejecutados por la automatización.

Asimismo, este documento servirá como fundamento para la implementación de la capa de persistencia, el acceso a los datos y el desarrollo del MVP, garantizando que todas las decisiones de implementación se apoyen sobre un modelo de datos previamente analizado, justificado y aprobado.

Toda modificación al modelo de datos deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al proyecto, preservando la trazabilidad histórica y la coherencia con el resto de la documentación oficial.

---

## 2. Principios del modelo de datos

El diseño, implementación, mantenimiento y evolución del modelo de datos de la automatización deberá realizarse conforme a los principios definidos en este capítulo.

Estos principios constituyen las reglas oficiales que deberán respetarse durante la definición de entidades, atributos, relaciones, restricciones, reglas de validación y cualquier otro componente del modelo de datos.

Toda decisión relacionada con el modelo de datos deberá estar debidamente justificada y mantener coherencia con la documentación oficial previamente aprobada.

Se establecen los siguientes principios oficiales:

### PMD-001. Integridad de los datos

El modelo de datos deberá preservar permanentemente la integridad de la información, evitando estados inconsistentes o relaciones inválidas.

### PMD-002. Consistencia

Toda la información almacenada deberá mantenerse consistente entre los distintos módulos, procesos y componentes de la automatización.

### PMD-003. Unicidad

Cada entidad deberá disponer de mecanismos que permitan identificar inequívocamente cada uno de sus registros cuando corresponda.

### PMD-004. Normalización

El modelo de datos deberá minimizar la redundancia innecesaria de información mediante una organización lógica y estructurada de las entidades y sus relaciones.

### PMD-005. No duplicidad de información

La misma información no deberá almacenarse múltiples veces cuando pueda mantenerse mediante relaciones correctamente definidas.

### PMD-006. Modularidad

El modelo de datos deberá organizarse de forma modular, facilitando su comprensión, mantenimiento y evolución.

### PMD-007. Escalabilidad

La estructura del modelo deberá permitir la incorporación de nuevas entidades, atributos y relaciones sin requerir una reorganización significativa del modelo existente.

### PMD-008. Trazabilidad

El modelo de datos deberá permitir reconstruir el historial de los procesos, decisiones y cambios relevantes realizados durante el ciclo de vida de cada oferta de empleo.

### PMD-009. Auditabilidad

La información necesaria para auditoría y diagnóstico deberá poder conservarse sin afectar la integridad del modelo.

### PMD-010. Persistencia controlada

Toda la información persistente deberá almacenarse conforme a reglas claramente definidas, evitando datos huérfanos, inconsistentes o innecesarios.

### PMD-011. Independencia tecnológica

El modelo de datos deberá definirse de forma independiente del motor de base de datos o de cualquier tecnología específica de almacenamiento.

### PMD-012. Validación de los datos

El modelo deberá facilitar la validación de los datos antes de su incorporación, modificación o utilización dentro de la automatización.

### PMD-013. Mantenibilidad

La estructura del modelo deberá facilitar su actualización, corrección y comprensión durante toda la vida útil del proyecto.

### PMD-014. Extensibilidad

El modelo deberá permitir incorporar nuevos requisitos funcionales mediante ampliaciones controladas, preservando la compatibilidad con la información existente.

### PMD-015. Seguridad de la información

El modelo de datos deberá facilitar la protección de la integridad, disponibilidad y confidencialidad de la información conforme a los requisitos del proyecto.

### PMD-016. Separación entre modelo lógico y modelo físico

La definición conceptual y lógica de los datos deberá mantenerse independiente de su implementación física en la base de datos.

### PMD-017. Compatibilidad con la arquitectura general

El modelo de datos deberá ser completamente compatible con la arquitectura general del sistema aprobada para el proyecto.

### PMD-018. Compatibilidad con el flujo de datos

La estructura de la información deberá soportar correctamente todas las transformaciones y movimientos definidos en el Flujo de Datos oficial.

### PMD-019. Compatibilidad con el modelo de decisiones

El modelo deberá almacenar toda la información necesaria para soportar el Modelo de Decisiones aprobado, preservando la trazabilidad de cada decisión.

### PMD-020. Evolución controlada

Toda modificación del modelo de datos deberá documentarse, justificarse y aprobarse formalmente antes de su incorporación al proyecto.

---

## Principios generales del modelo de datos

El modelo de datos deberá garantizar:

- Integridad y consistencia de la información.
- Eliminación de redundancias innecesarias.
- Modularidad y mantenibilidad.
- Escalabilidad y extensibilidad.
- Trazabilidad y auditabilidad.
- Independencia tecnológica.
- Compatibilidad con la arquitectura general del sistema.
- Compatibilidad con el flujo de datos y el modelo de decisiones.
- Evolución controlada del modelo.
- Coherencia con toda la documentación oficial del proyecto.

---

## 3. Objetivos del modelo de datos

Los objetivos del modelo de datos definen los resultados que deberá alcanzar la estructura de información de la automatización para soportar de manera eficiente, consistente y trazable todos los procesos del proyecto.

Cada objetivo representa una capacidad que deberá preservarse durante el diseño, implementación, mantenimiento y evolución del modelo de datos.

---

### OMD-001. Centralizar la información oficial

Establecer un modelo de datos que actúe como la fuente oficial de información para todos los módulos, procesos y componentes de la automatización.

---

### OMD-002. Representar el dominio del proyecto

Modelar de forma estructurada todas las entidades, relaciones y atributos necesarios para representar el proceso completo de búsqueda y procesamiento de oportunidades laborales.

---

### OMD-003. Garantizar la integridad de la información

Asegurar que toda la información almacenada mantenga su consistencia, validez y coherencia durante todo su ciclo de vida.

---

### OMD-004. Soportar el ciclo de vida de las ofertas

Permitir el almacenamiento y seguimiento de toda la información generada desde el descubrimiento de una oferta de empleo hasta la finalización de su procesamiento.

---

### OMD-005. Garantizar la trazabilidad

Conservar la información necesaria para reconstruir el historial de estados, decisiones, transformaciones y operaciones realizadas sobre cada oferta de empleo.

---

### OMD-006. Facilitar el intercambio de información

Proporcionar una estructura uniforme que permita el intercambio consistente de información entre todos los módulos de la automatización.

---

### OMD-007. Minimizar la redundancia

Organizar la información de forma que se evite el almacenamiento innecesario de datos duplicados, favoreciendo la reutilización mediante relaciones adecuadas.

---

### OMD-008. Facilitar la auditoría

Permitir el registro y consulta de la información necesaria para auditoría, diagnóstico y seguimiento operativo del sistema.

---

### OMD-009. Favorecer la escalabilidad

Diseñar un modelo que permita incorporar nuevas entidades, relaciones y atributos sin afectar significativamente la estructura existente.

---

### OMD-010. Favorecer la mantenibilidad

Mantener una organización clara, modular y consistente que facilite la evolución y comprensión del modelo de datos.

---

### OMD-011. Optimizar el acceso a la información

Proporcionar una estructura que facilite las consultas, búsquedas y operaciones requeridas por los distintos módulos del sistema.

---

### OMD-012. Preservar la independencia tecnológica

Definir el modelo de datos de forma independiente del motor de base de datos y de cualquier tecnología específica de almacenamiento.

---

### OMD-013. Soportar la evolución del proyecto

Permitir la incorporación controlada de nuevos requisitos funcionales sin comprometer la compatibilidad con la información previamente almacenada.

---

## Principios generales de los objetivos del modelo de datos

Los objetivos del modelo de datos deberán:

- Contribuir directamente al cumplimiento de los objetivos generales del proyecto.
- Mantener coherencia con toda la documentación oficial.
- Garantizar la integridad, consistencia y trazabilidad de la información.
- Facilitar la integración entre los módulos de la automatización.
- Favorecer la escalabilidad y mantenibilidad del modelo.
- Permanecer independientes de tecnologías específicas.
- Servir como referencia para el diseño, validación y evolución del modelo de datos.

---

## 4. Arquitectura general del modelo de datos

La arquitectura general del modelo de datos define la organización conceptual de la información utilizada por la automatización de búsqueda de empleo.

Su propósito es estructurar el modelo de datos de forma modular, coherente y alineada con la arquitectura general del sistema, el flujo de datos y los procesos funcionales previamente definidos.

La organización establecida en este capítulo constituye el modelo oficial que deberá respetarse durante el diseño de todas las entidades, relaciones, atributos y demás componentes del modelo de datos.

---

### 4.1. Modelo arquitectónico

El modelo de datos adopta una arquitectura organizada por dominios funcionales, donde cada conjunto de entidades representa una responsabilidad específica dentro de la automatización.

Esta organización facilita la comprensión del dominio, reduce el acoplamiento entre entidades y favorece la evolución independiente de cada área funcional del sistema.

---

### 4.2. Dominio de descubrimiento de oportunidades

Agrupa las entidades responsables de representar la información obtenida durante el proceso de identificación y recopilación de ofertas de empleo.

Las entidades pertenecientes a este dominio deberán almacenar únicamente la información correspondiente a esta etapa del flujo operativo.

---

### 4.3. Dominio de preparación inicial

Agrupa las entidades relacionadas con la normalización, validación inicial y preparación de la información antes de su evaluación.

Este dominio será responsable de representar los datos generados durante la etapa de preparación de las ofertas.

---

### 4.4. Dominio de evaluación inicial

Agrupa las entidades encargadas de representar los resultados obtenidos durante la evaluación automática de las ofertas de empleo.

Incluye la información necesaria para soportar el modelo de decisiones y la clasificación inicial de las oportunidades.

---

### 4.5. Dominio de procesamiento de la oferta

Agrupa las entidades que representan la información generada durante el procesamiento profundo de las ofertas seleccionadas.

Este dominio contendrá los datos relacionados con diagnósticos, análisis, generación de documentos, resultados y demás procesos especializados.

---

### 4.6. Dominio de servicios compartidos

Agrupa las entidades reutilizadas por varios módulos de la automatización.

Su finalidad es evitar duplicidad de información y centralizar los datos comunes utilizados por distintos procesos del sistema.

---

### 4.7. Dominio de configuración

Agrupa las entidades responsables de almacenar parámetros, configuraciones, preferencias y demás información utilizada para controlar el comportamiento de la automatización.

---

### 4.8. Dominio de auditoría y operación

Agrupa las entidades destinadas al seguimiento operativo del sistema.

Incluye la información necesaria para auditoría, trazabilidad, manejo de errores, registros de ejecución, eventos relevantes y monitoreo de la automatización.

---

### 4.9. Relaciones entre dominios

Cada dominio deberá mantener relaciones únicamente cuando exista una necesidad funcional claramente identificada.

Las relaciones deberán minimizar el acoplamiento entre dominios y preservar la independencia funcional de cada uno de ellos.

Toda interacción entre dominios deberá respetar el flujo oficial de datos definido para la automatización.

---

### 4.10. Principios de la arquitectura del modelo de datos

La arquitectura general del modelo de datos deberá preservar permanentemente los siguientes principios:

- Organización por dominios funcionales.
- Bajo acoplamiento entre dominios.
- Alta cohesión dentro de cada dominio.
- Modularidad.
- Escalabilidad.
- Reutilización de información.
- Integridad y consistencia de los datos.
- Trazabilidad completa de la información.
- Compatibilidad con la arquitectura general del sistema.
- Evolución controlada del modelo.

---

### 4.11. Evolución de la arquitectura

Toda incorporación, modificación o eliminación de entidades deberá respetar la arquitectura general definida en este documento.

Cualquier cambio estructural deberá documentarse, justificarse y aprobarse formalmente antes de su implementación, garantizando la compatibilidad con el resto del modelo de datos y con la documentación oficial del proyecto.

---

## 5. Entidades del sistema

Las entidades del sistema representan los elementos fundamentales que conforman el modelo de datos oficial de la automatización de búsqueda de empleo.

Cada entidad deberá modelar un concepto único del dominio del proyecto, poseer una responsabilidad claramente definida y mantener coherencia con los principios del modelo de datos, la arquitectura general del sistema, el flujo de datos y el modelo de decisiones.

Las entidades oficiales se clasifican en las siguientes categorías:

---

### 5.1. Entidades principales

Corresponden a los elementos centrales del dominio de negocio de la automatización.

Estas entidades representan la información principal sobre la cual se ejecutan los procesos funcionales del sistema.

Toda entidad principal deberá:

- Representar un concepto propio del dominio del proyecto.
- Tener un ciclo de vida claramente definido.
- Poder relacionarse con otras entidades mediante reglas explícitas.
- Mantener independencia respecto de su implementación física.

---

### 5.2. Entidades de soporte

Corresponden a las entidades utilizadas para complementar, parametrizar o enriquecer la información de las entidades principales.

Su propósito es evitar redundancia, favorecer la reutilización de información y facilitar la evolución del modelo.

Las entidades de soporte podrán ser compartidas por múltiples módulos de la automatización.

---

### 5.3. Entidades operativas

Corresponden a las entidades utilizadas para representar el funcionamiento interno de la automatización.

Incluyen la información necesaria para:

- Gestión de estados.
- Procesamiento interno.
- Auditoría.
- Manejo de errores.
- Registros operativos.
- Ejecuciones.
- Eventos.
- Configuración.
- Trazabilidad.

Estas entidades no representan conceptos del negocio, sino aspectos propios de la operación del sistema.

---

### 5.4. Inventario oficial de entidades

El inventario oficial de entidades del proyecto deberá derivarse exclusivamente de la documentación oficial previamente aprobada.

Cada entidad incorporada al modelo de datos deberá cumplir, como mínimo, las siguientes condiciones:

- Tener una necesidad funcional claramente identificada.
- Estar respaldada por uno o más requisitos funcionales.
- Ser compatible con el flujo oficial de datos.
- Mantener coherencia con el modelo de decisiones.
- Respetar la arquitectura general del sistema.
- No duplicar responsabilidades de otra entidad existente.
- Poder integrarse con el resto del modelo de datos sin generar inconsistencias.

No se permitirá incorporar entidades que no se encuentren debidamente justificadas desde el punto de vista funcional o arquitectónico.

---

### 5.5. Evolución del inventario de entidades

Toda incorporación, modificación, unificación o eliminación de entidades deberá documentarse y justificarse formalmente antes de formar parte del modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la trazabilidad histórica y la coherencia con el resto de la documentación oficial del proyecto.

---

## 6. Relaciones entre entidades

Las relaciones entre entidades definen la forma en que los distintos elementos del modelo de datos interactúan entre sí para representar de manera coherente el dominio funcional de la automatización.

Toda relación deberá responder a una necesidad funcional claramente identificada, respetar la arquitectura general del sistema y mantener la integridad del modelo de datos.

Las relaciones definidas en este documento constituyen el marco normativo que deberá respetarse durante la construcción del modelo lógico y la implementación física de la base de datos.

---

### 6.1. Principios generales de las relaciones

Toda relación entre entidades deberá cumplir los siguientes principios:

- Responder a un requisito funcional del proyecto.
- Mantener la integridad referencial.
- Evitar redundancias innecesarias.
- Minimizar el acoplamiento entre dominios.
- Facilitar la trazabilidad de la información.
- Mantener coherencia con el flujo oficial de datos.
- Respetar la arquitectura modular del sistema.
- Permitir la evolución controlada del modelo de datos.

---

### 6.2. Relaciones intra-dominio

Las entidades pertenecientes a un mismo dominio funcional podrán establecer relaciones cuando dichas relaciones sean necesarias para representar correctamente el comportamiento de ese dominio.

Estas relaciones deberán mantener una alta cohesión y evitar dependencias innecesarias con otros dominios.

---

### 6.3. Relaciones inter-dominio

Las relaciones entre entidades pertenecientes a dominios diferentes únicamente podrán establecerse cuando exista una necesidad funcional claramente documentada.

Estas relaciones deberán diseñarse procurando el menor nivel posible de acoplamiento entre dominios.

---

### 6.4. Cardinalidad de las relaciones

Toda relación deberá definir explícitamente su cardinalidad durante la construcción del modelo lógico de datos.

Como mínimo, deberán identificarse los siguientes tipos de relación cuando correspondan:

- Uno a uno (1:1).
- Uno a muchos (1:N).
- Muchos a muchos (N:M).

La selección de la cardinalidad deberá justificarse de acuerdo con las necesidades funcionales del proyecto.

---

### 6.5. Integridad referencial

Las relaciones deberán preservar permanentemente la integridad referencial de la información.

No se permitirán relaciones que generen registros huérfanos, inconsistencias o dependencias inválidas entre entidades.

Las reglas específicas de actualización y eliminación serán definidas durante el diseño del modelo lógico y la implementación física.

---

### 6.6. Dependencias entre entidades

Las dependencias entre entidades deberán mantenerse al mínimo necesario para representar correctamente el dominio del proyecto.

Toda dependencia deberá encontrarse debidamente justificada y documentada.

---

### 6.7. Prevención de relaciones innecesarias

No se permitirá establecer relaciones que:

- Dupliquen información ya representada por otras relaciones.
- Introduzcan dependencias circulares injustificadas.
- Incrementen innecesariamente la complejidad del modelo.
- Contradigan la arquitectura general del sistema o el flujo oficial de datos.

---

### 6.8. Compatibilidad con el flujo de datos

Las relaciones entre entidades deberán facilitar el intercambio de información entre los distintos módulos de la automatización conforme al flujo oficial de procesamiento.

La estructura relacional no deberá obstaculizar la ejecución de ninguna etapa del proceso.

---

### 6.9. Evolución de las relaciones

Toda incorporación, modificación o eliminación de relaciones deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la integridad del modelo y la coherencia con el resto de la documentación oficial del proyecto.

---

## 7. Atributos de las entidades

Los atributos de las entidades representan las propiedades que describen la información almacenada por cada elemento del modelo de datos.

Todo atributo deberá aportar un significado funcional claro, mantener coherencia con el dominio que representa y cumplir los principios establecidos para el modelo de datos.

La definición detallada de los atributos individuales se realizará en el Diccionario Oficial de Datos. El presente capítulo establece únicamente las reglas generales que deberán cumplir todos los atributos del modelo.

---

### 7.1. Principios generales de los atributos

Todo atributo deberá cumplir los siguientes principios:

- Representar una única propiedad del dominio.
- Tener un significado claro e inequívoco.
- Estar respaldado por una necesidad funcional.
- Mantener coherencia con la entidad a la que pertenece.
- Cumplir los estándares oficiales de nomenclatura del proyecto.
- Poder validarse conforme a reglas objetivas.
- Evitar redundancias innecesarias.
- Mantener independencia de la implementación física.

---

### 7.2. Clasificación de los atributos

Los atributos del modelo de datos se clasifican oficialmente en las siguientes categorías:

#### Atributos de identificación

Permiten identificar de forma única una instancia de una entidad.

Estos atributos constituyen la base para la identificación lógica de los registros dentro del modelo.

---

#### Atributos de negocio

Representan la información propia del dominio funcional de la entidad.

Describen las características principales del concepto modelado y constituyen la mayor parte de la información utilizada por la automatización.

---

#### Atributos de relación

Permiten establecer vínculos entre entidades y representar las asociaciones definidas por el modelo de datos.

Su utilización deberá preservar la integridad referencial y minimizar el acoplamiento entre entidades.

---

#### Atributos de control

Representan información utilizada para gestionar el ciclo de vida de los registros.

Incluyen, entre otros, estados, indicadores de versión, fechas operativas y demás elementos necesarios para controlar el comportamiento de la información.

---

#### Atributos de auditoría

Permiten registrar la información necesaria para garantizar la trazabilidad y el seguimiento histórico de los registros.

Su utilización deberá facilitar el diagnóstico, la auditoría y el análisis de la evolución de la información.

---

### 7.3. Tipificación de los atributos

Todo atributo deberá definir un tipo de dato compatible con la naturaleza de la información que representa.

La selección del tipo de dato deberá priorizar:

- Precisión.
- Consistencia.
- Eficiencia.
- Facilidad de validación.
- Compatibilidad con el modelo lógico.

Los tipos de datos específicos serán definidos durante el diseño del modelo lógico y documentados en el Diccionario Oficial de Datos.

---

### 7.4. Obligatoriedad de los atributos

Cada atributo deberá clasificarse como obligatorio u opcional de acuerdo con los requisitos funcionales del proyecto.

La obligatoriedad deberá justificarse funcionalmente y mantenerse consistente durante toda la evolución del modelo.

---

### 7.5. Validación de los atributos

Todo atributo deberá disponer de reglas de validación que garanticen la calidad e integridad de la información.

Las reglas de validación podrán incluir, cuando corresponda:

- Longitud.
- Formato.
- Dominio de valores.
- Rangos permitidos.
- Unicidad.
- Obligatoriedad.
- Consistencia con otros atributos.

Las reglas específicas serán documentadas en el Diccionario Oficial de Datos.

---

### 7.6. Atributos derivados

No se permitirá almacenar información que pueda obtenerse de forma determinística a partir de otros atributos, salvo que exista una justificación técnica o funcional debidamente documentada.

Cuando un atributo derivado sea persistido, deberán establecerse mecanismos que garanticen permanentemente su consistencia con la información de origen.

---

### 7.7. Evolución de los atributos

Toda incorporación, modificación o eliminación de atributos deberá documentarse, justificarse y aprobarse formalmente antes de formar parte del modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la integridad del modelo y la coherencia con el resto de la documentación oficial del proyecto.

---

## 8. Reglas de integridad de los datos

Las reglas de integridad de los datos establecen los criterios oficiales que deberán garantizar la consistencia, validez, confiabilidad y coherencia de toda la información administrada por la automatización.

Estas reglas serán de aplicación obligatoria durante el diseño del modelo de datos, la implementación de la base de datos, los procesos de validación, el intercambio de información entre módulos y cualquier operación de creación, modificación, eliminación o consulta de datos.

---

### 8.1. Integridad de entidad

Toda entidad deberá disponer de un mecanismo que permita identificar de forma única cada uno de sus registros.

No se permitirá la existencia de registros ambiguos o imposibles de identificar de manera inequívoca dentro del modelo de datos.

---

### 8.2. Integridad referencial

Toda relación entre entidades deberá preservar la coherencia entre los registros relacionados.

No podrán existir referencias a entidades inexistentes ni relaciones que generen registros huérfanos o inconsistentes.

Las reglas específicas de actualización y eliminación serán definidas durante el diseño del modelo lógico.

---

### 8.3. Integridad de dominio

Cada atributo deberá admitir únicamente valores compatibles con su naturaleza, significado y propósito funcional.

Los dominios válidos deberán definirse mediante reglas de validación claramente documentadas.

---

### 8.4. Integridad funcional

Toda la información almacenada deberá cumplir las reglas funcionales establecidas en los requisitos del proyecto, el modelo de decisiones y el flujo oficial de procesamiento.

No se permitirá almacenar información que contradiga el comportamiento esperado de la automatización.

---

### 8.5. Integridad temporal

La evolución de la información deberá respetar el orden lógico y cronológico definido para el ciclo de vida de cada oferta de empleo y de los procesos asociados.

No podrán producirse transiciones, estados o secuencias temporales incompatibles con el flujo oficial de la automatización.

---

### 8.6. Integridad de auditoría

Toda operación relevante que modifique información deberá poder reconstruirse mediante los mecanismos oficiales de auditoría y trazabilidad del proyecto.

La eliminación o modificación de información no deberá comprometer la reconstrucción del historial cuando este deba conservarse.

---

### 8.7. Integridad operacional

La automatización deberá impedir que errores de ejecución, interrupciones del procesamiento o fallos recuperables generen estados inconsistentes dentro del modelo de datos.

Los mecanismos de recuperación deberán preservar la coherencia de la información durante todo el ciclo de procesamiento.

---

### 8.8. Integridad semántica

La información generada por procesos automáticos o mediante inteligencia artificial deberá validarse antes de incorporarse al modelo de datos cuando corresponda.

La validación deberá garantizar que dicha información sea coherente con el contexto funcional, las reglas del proyecto y el resto de la información previamente almacenada.

La incorporación de información generada automáticamente no deberá comprometer la consistencia ni la confiabilidad del modelo de datos.

---

### 8.9. Validación de la integridad

Los mecanismos de validación deberán ejecutarse antes, durante o después de las operaciones sobre los datos, según corresponda a la naturaleza de cada regla de integridad.

Toda violación de una regla de integridad deberá gestionarse conforme al Modelo de Manejo de Errores aprobado para el proyecto.

---

### 8.10. Evolución de las reglas de integridad

Toda incorporación, modificación o eliminación de reglas de integridad deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la coherencia del modelo y el cumplimiento de toda la documentación oficial del proyecto.

---

## 9. Catálogos y tablas de referencia

Los catálogos y tablas de referencia constituyen el mecanismo oficial para centralizar la información reutilizable utilizada por la automatización de búsqueda de empleo.

Su propósito es garantizar la consistencia de los datos, reducir la duplicidad de información y facilitar la administración de los valores compartidos por los distintos módulos del sistema.

La incorporación de un catálogo deberá responder siempre a una necesidad funcional claramente identificada y respetar los principios del modelo de datos definidos en este documento.

---

### 9.1. Objetivo de los catálogos

Los catálogos deberán proporcionar una fuente única de información para aquellos conjuntos de valores utilizados de manera recurrente dentro de la automatización.

Su utilización deberá favorecer:

- La normalización de la información.
- La reutilización de datos.
- La consistencia entre módulos.
- La simplificación del mantenimiento.
- La evolución controlada del modelo de datos.

---

### 9.2. Criterios para la creación de un catálogo

Un conjunto de valores únicamente podrá modelarse como catálogo cuando cumpla uno o más de los siguientes criterios:

- Sea reutilizado por múltiples entidades.
- Sea utilizado por distintos módulos de la automatización.
- Requiera administración centralizada.
- Pueda modificarse sin alterar la lógica del sistema.
- Represente un concepto estable del dominio del proyecto.
- Sea necesario para procesos de validación o normalización.
- Contribuya a reducir la redundancia de información.

La creación de catálogos que no aporten un beneficio funcional o arquitectónico deberá evitarse.

---

### 9.3. Clasificación de los catálogos

Los catálogos oficiales del proyecto podrán clasificarse en las siguientes categorías:

#### Catálogos funcionales

Representan conceptos propios del dominio de negocio utilizados durante el procesamiento de las ofertas de empleo.

---

#### Catálogos geográficos

Representan información relacionada con ubicaciones geográficas utilizadas por la automatización.

---

#### Catálogos técnicos

Representan información utilizada para el funcionamiento interno del sistema, incluyendo estados, tipos, clasificaciones y demás elementos de carácter técnico.

---

#### Catálogos de configuración

Representan valores utilizados para parametrizar el comportamiento de la automatización sin requerir modificaciones sobre la lógica del sistema.

---

### 9.4. Reutilización de los catálogos

Toda entidad que requiera información representada por un catálogo oficial deberá reutilizar dicho catálogo en lugar de almacenar nuevamente la misma información.

No se permitirá la existencia de catálogos duplicados que representen el mismo concepto funcional.

---

### 9.5. Integridad de los catálogos

Los valores contenidos en los catálogos deberán mantenerse consistentes, completos y compatibles con el resto del modelo de datos.

Toda modificación sobre un catálogo deberá preservar la integridad referencial de las entidades que dependan de él.

---

### 9.6. Administración de los catálogos

La incorporación, modificación, desactivación o eliminación de valores pertenecientes a un catálogo deberá realizarse mediante procedimientos controlados que garanticen la consistencia del modelo de datos.

Las reglas específicas para la administración de cada catálogo serán definidas durante el diseño del modelo lógico y documentadas en el Diccionario Oficial de Datos.

---

### 9.7. Alternativas a los catálogos

Cuando un conjunto de valores no cumpla los criterios establecidos para convertirse en un catálogo oficial, podrá representarse mediante otros mecanismos de implementación, siempre que dicha decisión esté técnicamente justificada y no comprometa la mantenibilidad, la consistencia ni la evolución del modelo de datos.

La selección del mecanismo más adecuado deberá realizarse durante el diseño del modelo lógico y mantenerse documentada conforme a la arquitectura del proyecto.

---

### 9.8. Evolución de los catálogos

Toda incorporación, modificación o eliminación de un catálogo oficial deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos.

Las modificaciones deberán preservar la compatibilidad con la información existente, la integridad del modelo y la coherencia con el resto de la documentación oficial del proyecto.

---

## 10. Estados del sistema

Los estados del sistema representan la situación funcional u operativa de las entidades que conforman el modelo de datos durante su ciclo de vida dentro de la automatización.

Su propósito es controlar la evolución de la información, garantizar la consistencia del procesamiento y permitir el seguimiento completo de cada entidad desde su creación hasta la finalización de su participación en el sistema.

Toda entidad cuyo comportamiento evolucione a través de distintas etapas deberá gestionar su ciclo de vida mediante estados claramente definidos.

---

### 10.1. Principios generales de los estados

Los estados del sistema deberán cumplir los siguientes principios:

- Representar situaciones reales del dominio o del funcionamiento interno del sistema.
- Mantener coherencia con el flujo oficial de datos.
- Respetar el Modelo de Decisiones del proyecto.
- Facilitar la trazabilidad del procesamiento.
- Permitir la auditoría de las transiciones.
- Favorecer la recuperación controlada ante errores.
- Mantener independencia de la implementación tecnológica.

---

### 10.2. Clasificación de los estados

Los estados oficiales del modelo de datos podrán clasificarse en las siguientes categorías:

#### Estados de negocio

Representan el avance funcional de las entidades dentro del proceso de búsqueda y procesamiento de oportunidades laborales.

---

#### Estados operativos

Representan la situación de ejecución de los procesos internos de la automatización.

---

#### Estados de control

Representan condiciones administrativas, técnicas o temporales necesarias para controlar el comportamiento del sistema.

---

### 10.3. Modelo basado en máquinas de estados

Toda entidad que disponga de un ciclo de vida deberá modelarse conceptualmente como una máquina de estados.

Cada máquina de estados deberá definir, como mínimo:

- El estado inicial.
- Los estados permitidos.
- Las transiciones válidas.
- Las condiciones necesarias para cada transición.
- Los estados finales, cuando correspondan.

No se permitirán transiciones que no hayan sido definidas como válidas para la entidad correspondiente.

---

### 10.4. Transiciones entre estados

Toda transición deberá responder a un evento funcional u operativo claramente identificado.

Las transiciones deberán:

- Mantener coherencia con el flujo oficial de procesamiento.
- Respetar las reglas del Modelo de Decisiones.
- Preservar la integridad de la información.
- Impedir secuencias incompatibles con el ciclo de vida de la entidad.

---

### 10.5. Registro de las transiciones

Toda transición relevante entre estados deberá registrarse mediante los mecanismos oficiales de trazabilidad y auditoría definidos para el proyecto.

El registro deberá permitir reconstruir el historial completo de evolución de la entidad cuando resulte necesario.

---

### 10.6. Validación de los estados

Antes de realizar una transición, el sistema deberá verificar que:

- La entidad se encuentra en un estado válido.
- La transición solicitada está permitida.
- Se cumplen las condiciones funcionales necesarias.
- No se compromete la integridad del modelo de datos.

Las validaciones específicas serán definidas durante el diseño del modelo lógico y la implementación del sistema.

---

### 10.7. Recuperación ante estados inconsistentes

Cuando un proceso de la automatización detecte una transición inválida o un estado inconsistente, deberá aplicar las estrategias definidas en el Modelo de Manejo de Errores.

La recuperación no deberá comprometer la integridad, trazabilidad ni consistencia de la información almacenada.

---

### 10.8. Evolución del modelo de estados

Toda incorporación, modificación o eliminación de estados o transiciones deberá documentarse, justificarse y aprobarse formalmente antes de formar parte del modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, el historial de las entidades y la coherencia con el resto de la documentación oficial del proyecto.

---

## 11. Identificadores y claves

Los identificadores y las claves constituyen los mecanismos oficiales para garantizar la identificación única de las entidades y la correcta representación de las relaciones dentro del modelo de datos.

Su propósito es preservar la integridad referencial, facilitar la trazabilidad de la información y mantener la estabilidad del modelo durante toda la evolución de la automatización.

Toda entidad del modelo de datos deberá disponer de mecanismos de identificación definidos conforme a los principios establecidos en este capítulo.

---

### 11.1. Principios generales

Los identificadores y las claves deberán cumplir los siguientes principios:

- Garantizar la identificación única de cada registro.
- Mantener estabilidad durante todo el ciclo de vida de la entidad.
- Preservar la integridad referencial del modelo de datos.
- Mantener independencia respecto a cambios en la información de negocio.
- Facilitar la evolución y mantenibilidad del sistema.
- Evitar ambigüedades en las relaciones entre entidades.

---

### 11.2. Identificadores técnicos

Toda entidad persistente deberá disponer de un identificador técnico estable que represente su identidad dentro del sistema.

Los identificadores técnicos deberán:

- Ser únicos.
- Permanecer inmutables durante toda la existencia del registro.
- No depender de información susceptible de modificación.
- No reutilizarse una vez asignados.
- Ser utilizados como mecanismo principal de identificación dentro del modelo de datos.

La estrategia específica para la generación de estos identificadores será definida durante el diseño del modelo lógico.

---

### 11.3. Claves primarias

Toda entidad deberá disponer de una clave primaria que permita identificar de forma inequívoca cada uno de sus registros.

La clave primaria deberá construirse utilizando el identificador técnico oficial de la entidad, salvo que exista una justificación arquitectónica documentada para adoptar una estrategia diferente.

---

### 11.4. Claves alternativas

Cuando una entidad posea uno o varios identificadores propios del dominio funcional, estos podrán definirse como claves alternativas.

Las claves alternativas deberán:

- Mantener unicidad cuando corresponda.
- No sustituir la clave primaria.
- Poder modificarse cuando la naturaleza del negocio así lo requiera.
- Mantener consistencia con las reglas funcionales del proyecto.

---

### 11.5. Claves foráneas

Las relaciones entre entidades deberán implementarse mediante claves foráneas que preserven la integridad referencial del modelo de datos.

Toda clave foránea deberá:

- Referenciar una entidad existente.
- Mantener coherencia con las relaciones definidas en el modelo lógico.
- Cumplir las reglas de actualización y eliminación establecidas para cada relación.

---

### 11.6. Restricciones de unicidad

Cuando la naturaleza funcional de la información lo requiera, el modelo de datos deberá establecer restricciones de unicidad adicionales sobre uno o varios atributos.

Estas restricciones complementarán la identificación técnica de las entidades y garantizarán la consistencia de la información de negocio.

---

### 11.7. Reutilización de identificadores

No se permitirá reutilizar identificadores técnicos pertenecientes a registros previamente existentes, incluso cuando dichos registros hayan sido eliminados, archivados o desactivados.

Este principio garantiza la preservación de la trazabilidad histórica y evita ambigüedades durante la evolución del sistema.

---

### 11.8. Evolución de identificadores y claves

Toda modificación relacionada con los mecanismos de identificación o con las claves del modelo de datos deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo oficial.

Las modificaciones deberán preservar la integridad referencial, la compatibilidad con la información existente y la coherencia con el resto de la documentación oficial del proyecto.

---

## 12. Modelo lógico de datos

El modelo lógico de datos constituye la representación oficial de la estructura lógica de la información administrada por la automatización de búsqueda de empleo.

Su propósito es consolidar la organización de las entidades, sus relaciones, mecanismos de identificación y reglas estructurales, proporcionando una representación independiente de cualquier tecnología específica de almacenamiento.

El modelo lógico servirá como referencia directa para la implementación del modelo físico de datos y deberá mantener coherencia con la totalidad de la documentación oficial del proyecto.

---

### 12.1. Objetivo del modelo lógico

El modelo lógico deberá representar de forma completa, consistente y estructurada todos los componentes que conforman el modelo de datos de la automatización.

Su diseño deberá garantizar:

- Coherencia estructural.
- Integridad de la información.
- Independencia tecnológica.
- Escalabilidad.
- Trazabilidad.
- Compatibilidad con la arquitectura general del sistema.

---

### 12.2. Alcance del modelo lógico

El modelo lógico deberá integrar, como mínimo:

- Las entidades oficiales del sistema.
- Las relaciones entre entidades.
- Las cardinalidades.
- Los mecanismos de identificación.
- Las claves primarias.
- Las claves alternativas.
- Las claves foráneas.
- Los catálogos relacionados.
- Las máquinas de estados aplicables.
- Las restricciones lógicas necesarias para preservar la integridad del modelo.

El detalle completo de los atributos individuales permanecerá documentado exclusivamente en el Diccionario Oficial de Datos.

---

### 12.3. Estructura uniforme de las entidades

Toda entidad incorporada al modelo lógico deberá documentarse utilizando una estructura uniforme que facilite su comprensión, mantenimiento y evolución.

Como mínimo, cada entidad deberá incluir:

- Nombre oficial.
- Dominio funcional.
- Tipo de entidad.
- Descripción funcional.
- Responsabilidad principal.
- Relaciones relevantes.
- Cardinalidades.
- Identificador técnico.
- Claves alternativas, cuando existan.
- Claves foráneas, cuando correspondan.
- Catálogos asociados.
- Máquina de estados, cuando aplique.
- Observaciones arquitectónicas relevantes.

---

### 12.4. Coherencia estructural

Toda entidad y relación incorporada al modelo lógico deberá mantener coherencia con:

- Los requisitos funcionales y no funcionales.
- El flujo oficial de datos.
- El Modelo de Decisiones.
- La Arquitectura General del Sistema.
- Los principios del modelo de datos.
- Las reglas de integridad.
- Los mecanismos oficiales de identificación.

No se permitirá incorporar elementos que contradigan la arquitectura aprobada del proyecto.

---

### 12.5. Independencia del modelo físico

El modelo lógico deberá mantenerse independiente de cualquier motor de base de datos, tecnología de persistencia o decisión específica de implementación.

Las decisiones relacionadas con tipos de datos físicos, índices, optimizaciones de almacenamiento o configuraciones propias del gestor de base de datos formarán parte del modelo físico y no del modelo lógico.

---

### 12.6. Validación del modelo lógico

Antes de aprobar el modelo lógico, deberá verificarse que:

- Todas las entidades oficiales se encuentren representadas.
- Todas las relaciones sean consistentes.
- Las cardinalidades estén correctamente definidas.
- Los mecanismos de identificación sean coherentes.
- Las reglas de integridad puedan aplicarse correctamente.
- El modelo soporte completamente el flujo funcional de la automatización.

---

### 12.7. Evolución del modelo lógico

Toda modificación del modelo lógico deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la arquitectura general del sistema y el resto de la documentación oficial del proyecto.


---

## 13. Persistencia y almacenamiento

La persistencia y el almacenamiento definen los principios oficiales para la conservación, administración y disponibilidad de la información utilizada por la automatización de búsqueda de empleo.

Su propósito es garantizar que toda la información administrada por el sistema mantenga su integridad, consistencia, trazabilidad y disponibilidad durante el tiempo que resulte necesario, independientemente de la tecnología utilizada para su almacenamiento.

Las decisiones relacionadas con la implementación física de la persistencia deberán respetar los principios establecidos en este capítulo y mantenerse alineadas con el Stack Tecnológico aprobado para el proyecto.

---

### 13.1. Principios generales de la persistencia

Toda información persistida por la automatización deberá cumplir los siguientes principios:

- Mantener integridad y consistencia durante todo su ciclo de vida.
- Preservar la trazabilidad de la información cuando corresponda.
- Evitar redundancias innecesarias.
- Favorecer la recuperación ante errores.
- Mantener independencia respecto al mecanismo físico de almacenamiento.
- Garantizar compatibilidad con el modelo de datos oficial.
- Facilitar la evolución futura del sistema.

---

### 13.2. Clasificación de la información según su persistencia

La información administrada por el sistema se clasificará oficialmente de acuerdo con su ciclo de vida.

#### Información permanente

Corresponde a la información que constituye el conocimiento principal del sistema y cuya conservación resulta necesaria durante toda la vida útil del proyecto.

Su eliminación únicamente podrá realizarse mediante procedimientos formalmente autorizados.

---

#### Información histórica

Corresponde a la información utilizada para preservar la trazabilidad, auditoría y reconstrucción del historial de los procesos ejecutados por la automatización.

Su conservación deberá garantizar la posibilidad de realizar análisis históricos cuando resulte necesario.

---

#### Información temporal

Corresponde a la información utilizada únicamente durante determinadas etapas del procesamiento y cuya permanencia deja de ser necesaria una vez finalizada su función.

Su ciclo de vida deberá administrarse mediante políticas controladas de limpieza y eliminación.

---

#### Información de configuración

Corresponde a la información utilizada para controlar el comportamiento de la automatización.

Su persistencia deberá garantizar la reproducibilidad de las ejecuciones y la estabilidad operativa del sistema.

---

### 13.3. Conservación de la información

Toda política de conservación deberá establecerse considerando:

- La naturaleza funcional de la información.
- Los requisitos de auditoría y trazabilidad.
- Las necesidades operativas del sistema.
- Los criterios de mantenimiento del proyecto.

No deberá eliminarse información cuya conservación resulte necesaria para garantizar la integridad o trazabilidad del sistema.

---

### 13.4. Eliminación de información

La eliminación de información deberá realizarse únicamente mediante procedimientos controlados que preserven la consistencia del modelo de datos.

Toda eliminación deberá respetar:

- Las reglas de integridad referencial.
- Las dependencias existentes entre entidades.
- Las necesidades de auditoría.
- Las políticas oficiales de conservación.

---

### 13.5. Disponibilidad de la información

La persistencia deberá garantizar que la información permanezca disponible para los procesos autorizados de la automatización cuando resulte necesaria.

Los mecanismos específicos de acceso serán definidos durante la implementación física del sistema.

---

### 13.6. Independencia tecnológica

Las reglas de persistencia establecidas en este documento deberán mantenerse independientes del motor de base de datos, del mecanismo de almacenamiento o de cualquier tecnología específica utilizada durante la implementación.

Las decisiones tecnológicas correspondientes se regirán por el Stack Tecnológico oficial del proyecto.

---

### 13.7. Evolución de la estrategia de persistencia

Toda modificación relacionada con la persistencia o el almacenamiento de la información deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la integridad, compatibilidad y coherencia con el resto de la documentación oficial del proyecto.


---

## 14. Versionado y evolución del modelo de datos

El modelo de datos constituye un componente estratégico de la arquitectura de la automatización y deberá evolucionar de forma controlada durante todo el ciclo de vida del proyecto.

Toda modificación deberá preservar la integridad del modelo, garantizar la compatibilidad con la información existente y mantener la coherencia con la documentación oficial del proyecto.

El proceso de evolución del modelo de datos deberá encontrarse completamente documentado, justificado y trazable.

---

### 14.1. Principios generales de evolución

Toda evolución del modelo de datos deberá cumplir los siguientes principios:

- Mantener la integridad estructural del modelo.
- Preservar la consistencia de la información existente.
- Minimizar el impacto sobre los módulos del sistema.
- Mantener compatibilidad con la arquitectura general.
- Favorecer la escalabilidad del proyecto.
- Garantizar la trazabilidad de todas las modificaciones.
- Permitir la recuperación de versiones anteriores cuando resulte necesario.

---

### 14.2. Versionado del modelo de datos

El modelo de datos deberá mantener un esquema formal de versionado que permita identificar claramente cada una de sus revisiones oficiales.

Cada versión deberá encontrarse asociada, como mínimo, a:

- Un identificador de versión.
- La fecha de aprobación.
- La descripción de los cambios realizados.
- La justificación funcional o arquitectónica correspondiente.
- El análisis de impacto efectuado.
- La aprobación formal del cambio.

---

### 14.3. Clasificación de los cambios

Las modificaciones realizadas sobre el modelo de datos podrán clasificarse oficialmente como:

#### Cambios evolutivos

Incorporan nuevas capacidades o amplían el modelo existente sin alterar su propósito general.

---

#### Cambios correctivos

Corrigen errores, inconsistencias o mejoras identificadas durante la evolución del proyecto.

---

#### Cambios estructurales

Modifican la organización general del modelo de datos y requieren un análisis de impacto exhaustivo antes de su incorporación.

---

### 14.4. Compatibilidad de los cambios

Toda modificación deberá clasificarse además según su impacto sobre el modelo existente.

#### Cambios compatibles

Son aquellos que preservan la compatibilidad con la información existente y no requieren modificaciones significativas en los componentes que utilizan el modelo de datos.

Como criterio general, este tipo de cambios podrán incluir:

- Incorporación de nuevas entidades independientes.
- Adición de atributos opcionales.
- Incorporación de nuevos catálogos.
- Ampliaciones compatibles con la arquitectura existente.

---

#### Cambios incompatibles

Son aquellos que pueden afectar la estructura del modelo, la información almacenada o el funcionamiento de los módulos de la automatización.

Como criterio general, este tipo de cambios podrán incluir:

- Eliminación de entidades.
- Modificación de mecanismos de identificación.
- Cambios en las cardinalidades.
- Eliminación de atributos utilizados por otros componentes.
- Alteraciones que comprometan la compatibilidad con versiones anteriores.

Todo cambio incompatible deberá estar respaldado por un análisis de impacto específico antes de su aprobación.

---

### 14.5. Gestión del historial de cambios

El historial de evolución del modelo de datos deberá mantenerse disponible durante toda la vida útil del proyecto.

Cada modificación deberá registrar:

- La versión afectada.
- Los elementos modificados.
- La naturaleza del cambio.
- La justificación correspondiente.
- Las decisiones arquitectónicas relacionadas.

---

### 14.6. Evaluación del impacto

Antes de aprobar cualquier modificación del modelo de datos deberá realizarse una evaluación de impacto que considere, como mínimo:

- La compatibilidad con la información existente.
- La integridad del modelo.
- La arquitectura general del sistema.
- El flujo oficial de datos.
- El Modelo de Decisiones.
- Los mecanismos de persistencia.
- Los procesos de auditoría y trazabilidad.

---

### 14.7. Aprobación de cambios

Toda modificación del modelo de datos deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse a una nueva versión oficial.

No se permitirá la incorporación de cambios cuya necesidad funcional o arquitectónica no haya sido debidamente demostrada.

---

### 14.8. Evolución controlada

La evolución del modelo de datos deberá realizarse de forma planificada, garantizando en todo momento la estabilidad del sistema, la mantenibilidad del proyecto y la coherencia con el resto de la documentación oficial.

Toda nueva versión deberá preservar los principios arquitectónicos establecidos en este documento.


---

## 15. Trazabilidad y auditoría

La trazabilidad y la auditoría constituyen los mecanismos oficiales para garantizar el seguimiento completo de la información administrada por la automatización y de las operaciones realizadas durante todo su ciclo de vida.

Su propósito es permitir la reconstrucción de procesos, facilitar el diagnóstico de incidentes, respaldar el modelo de decisiones y preservar la confiabilidad de la información almacenada.

Toda la arquitectura del modelo de datos deberá diseñarse de manera que la información relevante pueda ser trazada, auditada y analizada cuando resulte necesario.

---

### 15.1. Principios generales de trazabilidad y auditoría

La trazabilidad y la auditoría deberán cumplir los siguientes principios:

- Preservar la integridad histórica de la información.
- Permitir la reconstrucción de los procesos relevantes.
- Mantener coherencia con el flujo oficial de datos.
- Favorecer el diagnóstico de incidentes.
- Respaldar el Modelo de Decisiones.
- Facilitar la evolución y mantenimiento del sistema.
- Mantener independencia respecto a la implementación tecnológica.

---

### 15.2. Alcance de la trazabilidad

La trazabilidad deberá abarcar, como mínimo:

- El ciclo de vida de las entidades principales.
- Las transiciones entre estados.
- Las operaciones relevantes realizadas sobre la información.
- Las decisiones funcionales que afecten el procesamiento.
- Los eventos operativos necesarios para comprender la evolución del sistema.

La información registrada deberá ser suficiente para reconstruir los procesos cuando resulte necesario.

---

### 15.3. Clasificación de la auditoría

La auditoría oficial del proyecto podrá clasificarse en las siguientes categorías.

#### Auditoría funcional

Registra los eventos relacionados con el comportamiento funcional de la automatización y con el procesamiento de las ofertas de empleo.

---

#### Auditoría técnica

Registra los eventos relacionados con la operación interna del sistema, la ejecución de procesos y el funcionamiento de los componentes técnicos.

---

#### Auditoría de cambios

Registra las modificaciones realizadas sobre la información persistente y sobre los elementos relevantes del modelo de datos.

---

### 15.4. Trazabilidad del contexto de las decisiones

Toda decisión relevante generada durante la automatización deberá poder contextualizarse cuando resulte necesario.

La información de trazabilidad deberá permitir identificar, como mínimo:

- El proceso que originó la decisión.
- El momento en que fue tomada.
- La información utilizada como entrada.
- El resultado obtenido.
- El componente responsable de la ejecución.
- La versión de las reglas, configuraciones o modelos aplicables cuando corresponda.

El nivel de detalle registrado deberá ser suficiente para explicar el contexto funcional de la decisión sin comprometer la eficiencia ni la mantenibilidad del sistema.

---

### 15.5. Integridad de la auditoría

Los registros de auditoría deberán mantenerse protegidos contra modificaciones no autorizadas que comprometan la confiabilidad de la información histórica.

Toda alteración sobre la información de auditoría deberá encontrarse debidamente documentada y autorizada.

---

### 15.6. Conservación de la información de auditoría

La información de auditoría deberá conservarse conforme a las políticas oficiales de persistencia definidas para el proyecto.

Su eliminación únicamente podrá realizarse mediante procedimientos controlados que no comprometan la trazabilidad de los procesos relevantes.

---

### 15.7. Acceso a la información de auditoría

El acceso a la información de auditoría deberá realizarse únicamente para fines funcionales, operativos, de diagnóstico, mantenimiento o análisis autorizados por la arquitectura del sistema.

La organización de la información deberá facilitar su consulta sin afectar la integridad del modelo de datos.

---

### 15.8. Evolución de los mecanismos de trazabilidad

Toda modificación relacionada con la trazabilidad o la auditoría deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la integridad histórica y la coherencia con el resto de la documentación oficial del proyecto.

---

## 16. Seguridad y protección de los datos

La seguridad y la protección de los datos establecen los principios oficiales para preservar la confidencialidad, integridad, disponibilidad y uso adecuado de la información administrada por la automatización de búsqueda de empleo.

Su propósito es garantizar que la información sea gestionada de forma segura durante todo su ciclo de vida, manteniendo coherencia con la arquitectura general del sistema, el modelo de datos y los principios establecidos para el proyecto.

Las decisiones relacionadas con mecanismos tecnológicos específicos de protección deberán regirse por el Stack Tecnológico y por la implementación del sistema, sin alterar los principios definidos en este documento.

---

### 16.1. Principios generales de seguridad

La gestión de la información deberá cumplir, como mínimo, los siguientes principios:

- Preservar la confidencialidad de la información.
- Garantizar la integridad de los datos.
- Mantener la disponibilidad de la información cuando resulte necesaria.
- Favorecer la trazabilidad de las operaciones relevantes.
- Proteger la información frente a modificaciones no autorizadas.
- Mantener coherencia con el Modelo de Manejo de Errores.
- Preservar la estabilidad del modelo de datos.

---

### 16.2. Clasificación de la información según su sensibilidad

Toda la información administrada por la automatización deberá clasificarse de acuerdo con el nivel de protección que requiera.

#### Información pública

Corresponde a información cuya divulgación no representa un impacto significativo para el proyecto o para el usuario.

Su utilización no requiere medidas especiales de protección distintas de las definidas por la arquitectura general.

---

#### Información de uso interno

Corresponde a información utilizada exclusivamente por la automatización para el funcionamiento de sus procesos internos.

Su acceso deberá limitarse a los componentes autorizados de la arquitectura del sistema.

---

#### Información sensible

Corresponde a información cuya divulgación, modificación, pérdida o utilización indebida podría afectar al usuario, al funcionamiento de la automatización o a la integridad del proyecto.

Este tipo de información deberá recibir un nivel de protección acorde con su criticidad durante la implementación del sistema.

---

### 16.3. Protección de la integridad de los datos

Toda operación sobre la información deberá preservar la consistencia del modelo de datos y respetar las reglas oficiales de integridad definidas para el proyecto.

No se permitirá la incorporación de mecanismos que comprometan la confiabilidad de la información almacenada.

---

### 16.4. Protección durante el ciclo de vida de la información

Las medidas de protección deberán contemplar todas las etapas del ciclo de vida de la información, incluyendo:

- Creación.
- Procesamiento.
- Almacenamiento.
- Consulta.
- Modificación.
- Archivado.
- Eliminación.

La estrategia de protección deberá mantenerse consistente durante todas estas etapas.

---

### 16.5. Acceso a la información

El acceso a la información deberá limitarse exclusivamente a los procesos, componentes y mecanismos autorizados por la arquitectura del sistema.

La organización del modelo de datos deberá facilitar la aplicación de controles de acceso durante la implementación, sin depender de un mecanismo tecnológico específico.

---

### 16.6. Protección de la información histórica

La información utilizada para auditoría, trazabilidad e historial deberá protegerse de forma que preserve permanentemente su integridad y confiabilidad.

Toda modificación sobre información histórica deberá encontrarse debidamente justificada, documentada y autorizada.

---

### 16.7. Compatibilidad con la arquitectura de seguridad

Las reglas establecidas en este capítulo deberán mantenerse compatibles con:

- La Arquitectura General del Sistema.
- El Stack Tecnológico oficial.
- El Modelo de Manejo de Errores.
- Las políticas oficiales de persistencia.
- Los mecanismos de auditoría y trazabilidad.

---

### 16.8. Evolución de las políticas de protección

Toda modificación relacionada con la seguridad o protección de la información deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la integridad del modelo, la compatibilidad con la información existente y la coherencia con el resto de la documentación oficial del proyecto.

---

## 17. Reglas de validación de datos

Las reglas de validación de datos establecen los principios oficiales que deberán garantizar que toda la información incorporada al modelo de datos sea consistente, completa, válida y compatible con la arquitectura de la automatización.

Su propósito es prevenir la incorporación de información incorrecta, preservar la integridad del modelo de datos y asegurar que toda la información utilizada por la automatización cumpla las reglas funcionales y arquitectónicas del proyecto.

Las validaciones deberán aplicarse durante todo el ciclo de vida de la información, independientemente del mecanismo tecnológico utilizado para su implementación.

---

### 17.1. Principios generales de validación

Toda validación de datos deberá cumplir los siguientes principios:

- Verificar la consistencia de la información antes de su incorporación al modelo de datos.
- Mantener coherencia con las reglas de integridad definidas para el proyecto.
- Ser objetiva, reproducible y verificable.
- Mantener independencia respecto a la tecnología utilizada para su implementación.
- Favorecer la calidad de la información.
- Reducir la incorporación de datos inconsistentes.
- Mantener compatibilidad con el Modelo de Decisiones y el flujo oficial de procesamiento.

---

### 17.2. Validaciones estructurales

Las validaciones estructurales verificarán que la información cumpla los requisitos básicos definidos para cada elemento del modelo de datos.

Podrán incluir, entre otros:

- Obligatoriedad.
- Tipo de dato.
- Longitud.
- Formato.
- Dominio de valores.
- Restricciones de unicidad.

Las reglas específicas serán documentadas en el Diccionario Oficial de Datos.

---

### 17.3. Validaciones funcionales

Las validaciones funcionales verificarán que la información cumpla las reglas de negocio establecidas para la automatización.

Su propósito será garantizar que la información represente correctamente el comportamiento esperado del dominio funcional del proyecto.

---

### 17.4. Validaciones relacionales

Las validaciones relacionales verificarán la coherencia existente entre entidades relacionadas.

Estas validaciones deberán preservar la integridad referencial y garantizar la consistencia de las relaciones definidas por el modelo de datos.

---

### 17.5. Validaciones temporales

Las validaciones temporales verificarán la coherencia cronológica de la información durante todo el ciclo de vida de las entidades.

No se permitirá registrar secuencias temporales incompatibles con el flujo oficial de procesamiento.

---

### 17.6. Validaciones semánticas

Las validaciones semánticas verificarán, cuando corresponda, que la información generada automáticamente o mediante inteligencia artificial sea coherente con el contexto funcional del proyecto antes de incorporarse al modelo de datos.

Estas validaciones deberán garantizar que la información:

- Sea consistente con el dominio representado.
- Respete las reglas funcionales del proyecto.
- Mantenga coherencia con la información previamente almacenada.
- No comprometa la integridad semántica del modelo de datos.

Las validaciones semánticas complementan las reglas de integridad semántica definidas para el proyecto y deberán aplicarse cuando la naturaleza de la información así lo requiera.

---

### 17.7. Gestión de errores de validación

Toda validación fallida deberá gestionarse conforme al Modelo de Manejo de Errores aprobado para el proyecto.

La incorporación de información al modelo de datos no deberá continuar cuando el incumplimiento de una regla de validación comprometa la integridad, consistencia o confiabilidad de la información.

---

### 17.8. Evolución de las reglas de validación

Toda incorporación, modificación o eliminación de reglas de validación deberá documentarse, justificarse y aprobarse formalmente antes de formar parte del modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la información existente, la coherencia con el resto de la arquitectura y el cumplimiento de toda la documentación oficial del proyecto.

---

## 18. Estrategia de migraciones

La estrategia de migraciones establece los principios oficiales para gestionar la evolución estructural del modelo de datos durante todo el ciclo de vida de la automatización.

Su propósito es garantizar que toda modificación realizada sobre la estructura persistente del sistema preserve la integridad de la información, mantenga la compatibilidad con la arquitectura aprobada y permita una evolución controlada del proyecto.

Las decisiones relacionadas con herramientas específicas de migración deberán regirse por el Stack Tecnológico oficial y no forman parte del presente documento.

---

### 18.1. Principios generales de las migraciones

Toda migración del modelo de datos deberá cumplir los siguientes principios:

- Mantener la integridad de la información.
- Preservar la consistencia del modelo de datos.
- Garantizar la trazabilidad de las modificaciones.
- Mantener compatibilidad con la arquitectura general del sistema.
- Ser reproducible y verificable.
- Favorecer la evolución controlada del proyecto.
- Minimizar el riesgo de pérdida o corrupción de información.

---

### 18.2. Alcance de las migraciones

Las migraciones deberán utilizarse para gestionar cualquier modificación estructural que afecte el modelo persistente de datos, incluyendo, cuando corresponda:

- Incorporación de nuevas entidades.
- Modificación de entidades existentes.
- Cambios en relaciones.
- Actualización de restricciones.
- Incorporación o modificación de catálogos.
- Ajustes derivados de la evolución del modelo de datos.

---

### 18.3. Clasificación de las migraciones

Las migraciones oficiales podrán clasificarse como:

#### Migraciones evolutivas

Incorporan nuevas capacidades al modelo de datos preservando la compatibilidad con la estructura existente.

---

#### Migraciones correctivas

Corrigen errores, inconsistencias o deficiencias identificadas durante la evolución del proyecto.

---

#### Migraciones estructurales

Introducen modificaciones significativas sobre la organización del modelo de datos y requieren un análisis de impacto previo a su ejecución.

---

### 18.4. Versionado de las migraciones

Toda migración deberá encontrarse asociada a una versión oficial del modelo de datos.

Cada migración deberá registrar, como mínimo:

- Identificador de la migración.
- Versión del modelo de datos.
- Descripción de la modificación.
- Justificación funcional o arquitectónica.
- Fecha de incorporación.
- Resultado de la ejecución.

---

### 18.5. Validación previa a la migración

Antes de ejecutar una migración deberá verificarse, como mínimo:

- La consistencia del modelo de datos.
- La compatibilidad con la versión anterior.
- El impacto sobre la información existente.
- El cumplimiento de las reglas de integridad.
- La compatibilidad con la arquitectura general del sistema.

Toda migración deberá contar con un análisis de impacto documentado antes de su aprobación.

---

### 18.6. Reversibilidad de las migraciones

Siempre que sea técnicamente viable, toda migración deberá diseñarse de forma que permita revertir los cambios realizados y restaurar el estado anterior del modelo de datos.

Cuando una migración no pueda revertirse debido a limitaciones técnicas o a la naturaleza de la transformación realizada, esta condición deberá documentarse previamente junto con su justificación.

En tales casos deberán establecerse medidas que minimicen el riesgo para la integridad y disponibilidad de la información.

---

### 18.7. Trazabilidad de las migraciones

Toda migración deberá formar parte del historial oficial de evolución del modelo de datos.

La documentación correspondiente deberá permitir reconstruir:

- La versión de origen.
- La versión de destino.
- Los cambios efectuados.
- La justificación de la modificación.
- El impacto identificado.
- La evidencia de aprobación.

---

### 18.8. Evolución de la estrategia de migraciones

Toda modificación relacionada con la estrategia oficial de migraciones deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al modelo de datos oficial.

Las modificaciones deberán preservar la compatibilidad con la arquitectura general, el historial de evolución del proyecto y el resto de la documentación oficial.

---

## 19. Criterios de aceptación

Los criterios de aceptación establecen las condiciones oficiales que deberá cumplir el modelo de datos para considerarse completo, consistente y conforme con la arquitectura aprobada del proyecto.

Su propósito es proporcionar un conjunto de criterios objetivos que permitan verificar la calidad del modelo de datos antes de su aprobación oficial o de la incorporación de nuevas versiones.

El cumplimiento de estos criterios será obligatorio para toda versión oficial del modelo de datos.

---

### 19.1. Integridad estructural

El modelo de datos deberá cumplir, como mínimo, las siguientes condiciones:

- Todas las entidades oficiales deberán encontrarse representadas.
- Todas las relaciones deberán estar debidamente definidas y justificadas.
- Los mecanismos oficiales de identificación deberán encontrarse documentados.
- Las reglas de integridad deberán poder aplicarse correctamente.
- No deberán existir inconsistencias estructurales dentro del modelo.

---

### 19.2. Coherencia funcional

El modelo de datos deberá representar correctamente el dominio funcional de la automatización.

Como mínimo deberá verificarse que:

- El modelo soporte completamente el flujo oficial de procesamiento.
- Las entidades representen correctamente los conceptos del dominio.
- Las relaciones reflejen las necesidades funcionales del proyecto.
- Las máquinas de estados sean compatibles con el ciclo de vida de las entidades correspondientes.

---

### 19.3. Calidad del modelo de datos

El modelo deberá demostrar que:

- La información puede mantenerse consistente.
- Se minimiza la redundancia innecesaria.
- La organización de las entidades favorece la mantenibilidad.
- La arquitectura permite la evolución controlada del sistema.
- El modelo es escalable y extensible.

---

### 19.4. Cumplimiento de las reglas del modelo

Antes de su aprobación deberá verificarse que el modelo cumple:

- Los principios del modelo de datos.
- Los objetivos del modelo.
- Las reglas de integridad.
- Las reglas de validación.
- Las políticas de persistencia.
- Los principios de seguridad.
- Los mecanismos de trazabilidad y auditoría.

---

### 19.5. Coherencia documental

El modelo de datos deberá mantenerse completamente alineado con la documentación oficial del proyecto.

Como mínimo deberá verificarse la compatibilidad con:

- Los requisitos funcionales y no funcionales.
- La documentación estratégica del proyecto.
- El flujo oficial de datos.
- El Modelo de Decisiones.
- La Arquitectura General del Sistema.
- El Stack Tecnológico aprobado.
- El Modelo de Manejo de Errores.
- El resto de los documentos oficiales relacionados con la arquitectura del proyecto.

No deberán existir contradicciones entre el modelo de datos y la documentación oficial vigente.

---

### 19.6. Completitud de la documentación

Antes de aprobar una versión oficial del modelo de datos deberá verificarse que toda la documentación asociada se encuentra completa.

Como mínimo deberán encontrarse disponibles:

- El Modelo Lógico de Datos.
- El Diccionario Oficial de Datos.
- El Diagrama Oficial del Modelo de Datos.
- El historial de versiones correspondiente.
- La documentación de cambios aprobados.

---

### 19.7. Aprobación del modelo

El modelo de datos únicamente podrá considerarse oficialmente aprobado cuando todos los criterios definidos en este capítulo hayan sido verificados satisfactoriamente.

Toda excepción deberá documentarse, justificarse y aprobarse formalmente antes de la liberación de una nueva versión oficial.

---

### 19.8. Revalidación del modelo

Toda modificación realizada sobre el modelo de datos deberá dar lugar a una nueva evaluación de los criterios de aceptación definidos en este capítulo.

No podrá aprobarse una nueva versión del modelo mientras exista algún criterio de aceptación pendiente de cumplimiento.

---

## 20. Diccionario Oficial de Datos

El Diccionario Oficial de Datos constituye la especificación técnica oficial del modelo de datos de la automatización de búsqueda de empleo.

Su propósito es documentar de manera completa, uniforme y trazable todos los elementos que conforman el modelo de datos, proporcionando una única fuente oficial de información para el diseño, implementación, mantenimiento y evolución del sistema.

Toda entidad, atributo, relación, catálogo y componente del modelo de datos deberá encontrarse documentado conforme a la estructura establecida en este capítulo.

---

### 20.1. Objetivos del Diccionario Oficial de Datos

El diccionario deberá:

- Centralizar la documentación técnica del modelo de datos.
- Garantizar la uniformidad en la definición de los elementos del modelo.
- Facilitar la implementación de la base de datos.
- Favorecer la mantenibilidad del sistema.
- Servir como referencia oficial para el desarrollo y evolución del proyecto.
- Mantener la trazabilidad con el resto de la documentación oficial.

---

### 20.2. Alcance del diccionario

El Diccionario Oficial de Datos deberá documentar, como mínimo:

- Entidades.
- Atributos.
- Relaciones.
- Claves primarias.
- Claves alternativas.
- Claves foráneas.
- Catálogos.
- Restricciones.
- Reglas de validación.
- Máquinas de estados cuando correspondan.
- Observaciones arquitectónicas relevantes.

No deberá existir ningún elemento persistente del modelo de datos que no se encuentre documentado en este diccionario.

---

### 20.3. Plantilla oficial para las entidades

Toda entidad deberá documentarse utilizando una estructura uniforme.

Como mínimo deberá incluir:

#### Información general

- Nombre oficial.
- Dominio funcional.
- Tipo de entidad.
- Descripción funcional.
- Responsabilidad principal.

---

#### Identificación

- Identificador técnico.
- Clave primaria.
- Claves alternativas.

---

#### Relaciones

- Entidades relacionadas.
- Cardinalidades.
- Claves foráneas.
- Dependencias relevantes.

---

#### Ciclo de vida

- Máquina de estados, cuando aplique.
- Estados principales.
- Observaciones relacionadas con el ciclo de vida.

---

#### Catálogos asociados

Relación de los catálogos utilizados por la entidad.

---

#### Observaciones arquitectónicas

Información relevante para comprender el papel de la entidad dentro del modelo de datos.

---

### 20.4. Plantilla oficial para los atributos

Todo atributo deberá documentarse utilizando una estructura uniforme.

Como mínimo deberá incluir:

- Nombre oficial.
- Descripción funcional.
- Tipo lógico.
- Tipo físico, cuando corresponda durante la implementación.
- Categoría del atributo.
- Obligatoriedad.
- Valor por defecto, cuando aplique.
- Dominio de valores.
- Restricciones.
- Reglas de validación.
- Restricciones de unicidad, cuando existan.
- Nivel de sensibilidad.
- Clasificación según persistencia.
- Observaciones relevantes.

---

### 20.5. Trazabilidad documental

El Diccionario Oficial de Datos deberá mantener la trazabilidad con el resto de la documentación oficial del proyecto.

Cuando corresponda, cada entidad deberá indicar su relación con:

- Los requisitos funcionales asociados.
- El dominio arquitectónico al que pertenece.
- El flujo oficial de datos.
- El Modelo de Decisiones.
- Las máquinas de estados correspondientes.
- Los catálogos utilizados.
- Las reglas de integridad aplicables.
- Las reglas de validación relacionadas.

Asimismo, cuando resulte pertinente, cada atributo podrá documentar:

- La regla de validación correspondiente.
- La regla de integridad asociada.
- Su clasificación según sensibilidad.
- Su clasificación según persistencia.
- Observaciones arquitectónicas relevantes.

---

### 20.6. Consistencia del diccionario

Toda la información documentada en el Diccionario Oficial de Datos deberá mantenerse consistente con:

- El Modelo Lógico de Datos.
- El Diagrama Oficial del Modelo de Datos.
- Los principios del modelo de datos.
- La arquitectura general del sistema.
- El resto de la documentación oficial del proyecto.

No se permitirá la existencia de contradicciones entre el diccionario y los demás artefactos oficiales.

---

### 20.7. Mantenimiento del diccionario

Toda incorporación, modificación o eliminación de información documentada en el Diccionario Oficial de Datos deberá realizarse de manera controlada.

Las modificaciones deberán:

- Mantener la trazabilidad documental.
- Preservar la consistencia del modelo.
- Actualizar la documentación relacionada cuando corresponda.
- Mantener sincronizados el Modelo Lógico de Datos y el Diagrama Oficial del Modelo de Datos.

---

### 20.8. Evolución del diccionario

El Diccionario Oficial de Datos deberá evolucionar conjuntamente con el modelo de datos.

Toda modificación deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse a una nueva versión oficial del proyecto.

El diccionario constituye la fuente oficial de referencia para la definición detallada de los elementos del modelo de datos y deberá mantenerse permanentemente actualizado.


---

## 21. Diagrama Oficial del Modelo de Datos

El Diagrama Oficial del Modelo de Datos constituye la representación gráfica oficial de la estructura lógica de la información utilizada por la automatización de búsqueda de empleo.

Su propósito es facilitar la comprensión de la organización general del modelo de datos, mostrando de forma visual las entidades, sus relaciones y la estructura general del sistema, manteniendo coherencia con el Modelo Lógico de Datos y el Diccionario Oficial de Datos.

El diagrama deberá mantenerse permanentemente sincronizado con dichos artefactos y no constituirá la fuente oficial de definición del modelo de datos.

---

### 21.1. Objetivo del diagrama

El Diagrama Oficial del Modelo de Datos deberá:

- Representar gráficamente la estructura lógica del modelo de datos.
- Facilitar la comprensión de las relaciones entre entidades.
- Favorecer el análisis arquitectónico del sistema.
- Servir como apoyo para el desarrollo y mantenimiento del proyecto.
- Mantener coherencia con toda la documentación oficial.

---

### 21.2. Alcance del diagrama

El diagrama deberá representar, como mínimo:

- Las entidades oficiales del modelo de datos.
- Las relaciones existentes entre entidades.
- Las cardinalidades correspondientes.
- Los dominios funcionales cuando resulte conveniente para la comprensión del modelo.
- La clasificación de las entidades conforme a la arquitectura del proyecto.
- Los catálogos oficiales cuando formen parte del modelo lógico.
- Las dependencias estructurales relevantes.

La inclusión de información adicional deberá justificarse por su utilidad para comprender la arquitectura del modelo.

---

### 21.3. Representación gráfica

La representación gráfica deberá facilitar la comprensión del modelo de datos evitando complejidad innecesaria.

El diagrama deberá:

- Mantener una organización clara y uniforme.
- Minimizar cruces innecesarios entre relaciones.
- Favorecer la legibilidad.
- Mantener consistencia en la simbología utilizada.
- Facilitar su evolución conforme crezca el modelo de datos.

La notación gráfica específica será definida durante la fase de implementación y deberá mantenerse uniforme en todas las versiones del diagrama.

---

### 21.4. Relación con el Modelo Lógico de Datos

El Diagrama Oficial del Modelo de Datos deberá derivarse directamente del Modelo Lógico de Datos.

Toda modificación estructural realizada sobre el modelo lógico deberá reflejarse posteriormente en el diagrama oficial.

No se permitirá que el diagrama contenga elementos inexistentes en el Modelo Lógico de Datos.

---

### 21.5. Relación con el Diccionario Oficial de Datos

Toda entidad representada en el diagrama deberá encontrarse documentada en el Diccionario Oficial de Datos.

Las relaciones, mecanismos de identificación y demás elementos representados gráficamente deberán mantener coherencia con la documentación técnica correspondiente.

El diagrama constituye una representación visual del modelo y no sustituye la especificación detallada contenida en el diccionario.

---

### 21.6. Versionado del diagrama

El Diagrama Oficial del Modelo de Datos deberá mantenerse versionado de forma consistente con las versiones oficiales del modelo de datos.

Cada versión deberá encontrarse asociada al correspondiente Modelo Lógico de Datos y al Diccionario Oficial de Datos.

Toda modificación deberá quedar documentada dentro del historial oficial de evolución del modelo.

---

### 21.7. Mantenimiento del diagrama

Toda modificación incorporada al modelo de datos deberá reflejarse oportunamente en el Diagrama Oficial del Modelo de Datos.

La sincronización entre el diagrama, el modelo lógico y el diccionario deberá preservarse permanentemente.

No se permitirá mantener versiones inconsistentes entre estos artefactos.

---

### 21.8. Naturaleza del diagrama

El Diagrama Oficial del Modelo de Datos constituye un artefacto gráfico de apoyo para la comprensión de la arquitectura del sistema.

La fuente oficial para la definición del modelo de datos estará conformada por:

- El Modelo Lógico de Datos.
- El Diccionario Oficial de Datos.

En caso de discrepancia entre el diagrama y dichos artefactos, prevalecerá siempre la información documentada en el Modelo Lógico de Datos y en el Diccionario Oficial de Datos.

El diagrama deberá considerarse una representación visual derivada de estos documentos y mantenerse permanentemente actualizado respecto de ellos.

