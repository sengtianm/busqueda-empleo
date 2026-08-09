# Documento 13 – Modelo de Datos (Optimizado)

---

## 1. Propósito y Alcance

Define el **modelo de datos oficial** de la automatización de búsqueda laboral: estructura lógica de la información, incluyendo entidades, atributos, relaciones, restricciones, reglas de integridad y mecanismos de persistencia.

**Función:** referencia oficial para diseño, implementación, mantenimiento y evolución del modelo de datos. Ningún elemento de información se agrega, modifica o elimina sin análisis y documentación previa conforme a este documento.

**Coherencia obligatoria:** las decisiones deben alinearse con los Documentos 0–12 (requisitos funcionales/no funcionales, modelo de decisión, flujo de datos, estándares, manejo de errores, arquitectura de carpetas, alcance y objetivos, stack tecnológico, arquitectura general del sistema).

**Garantías del modelo:** integridad, consistencia, trazabilidad, mantenibilidad y escalabilidad de la información durante todo el ciclo de vida de las ofertas y procesos.

**Base para:** implementación de la capa de persistencia, acceso a datos y desarrollo del MVP. Toda decisión de implementación debe estar respaldada por este modelo previamente analizado, justificado y aprobado.

**Control de cambios:** toda modificación debe documentarse, justificarse y aprobarse formalmente antes de incorporarse, preservando trazabilidad histórica y coherencia documental.

---

## 2. Regla Transversal de Evolución Controlada (REC)

Para evitar repetición en cada capítulo, se establece una única regla aplicable a **todo** elemento del modelo de datos (entidades, relaciones, atributos, reglas de integridad, catálogos, estados, identificadores, modelo lógico, persistencia, validaciones, migraciones, mecanismos de trazabilidad, políticas de seguridad):

> **REC-001.** Toda incorporación, modificación o eliminación de un elemento del modelo de datos debe:
> 1. Documentarse, justificarse y aprobarse formalmente antes de incorporarse.
> 2. Preservar compatibilidad con la información existente.
> 3. Preservar integridad y coherencia del modelo.
> 4. Mantener alineación con el resto de la documentación oficial del proyecto.
> 5. Registrar trazabilidad histórica del cambio.

Cuando un capítulo específico añada condiciones adicionales a esta regla, se explicitarán en ese capítulo. En caso contrario, REC-001 aplica íntegramente.

---

## 3. Principios del Modelo de Datos (PMD)

Reglas oficiales obligatorias durante definición de entidades, atributos, relaciones, restricciones, validaciones y cualquier componente del modelo. Toda decisión debe justificarse y alinearse con la documentación oficial aprobada.

| ID | Principio | Definición |
|---|---|---|
| PMD-001 | Integridad | Preservar permanentemente la integridad de la información; evitar estados inconsistentes o relaciones inválidas |
| PMD-002 | Consistencia | Toda información almacenada permanece consistente entre módulos, procesos y componentes |
| PMD-003 | Unicidad | Cada entidad tiene mecanismos para identificar inequívocamente cada registro donde aplique |
| PMD-004 | Normalización | Minimizar redundancia innecesaria mediante organización lógica y estructurada de entidades y relaciones |
| PMD-005 | No duplicación | La misma información no se almacena múltiples veces cuando puede mantenerse mediante relaciones correctamente definidas |
| PMD-006 | Modularidad | Organización modular que facilite comprensión, mantenimiento y evolución |
| PMD-007 | Escalabilidad | Estructura permite incorporar nuevas entidades, atributos y relaciones sin reorganización significativa |
| PMD-008 | Trazabilidad | Permite reconstruir historia de procesos, decisiones y cambios relevantes durante el ciclo de vida de cada oferta |
| PMD-009 | Auditabilidad | Información necesaria para auditoría y diagnóstico es preservable sin afectar la integridad del modelo |
| PMD-010 | Persistencia controlada | Toda información persistente se almacena según reglas claramente definidas; evitar datos huérfanos, inconsistentes o innecesarios |
| PMD-011 | Independencia tecnológica | Modelo definido independientemente del motor de base de datos o tecnología de almacenamiento específica |
| PMD-012 | Validación | Modelo facilita la validación de datos antes de su incorporación, modificación o uso |
| PMD-013 | Mantenibilidad | Estructura facilita actualización, corrección y comprensión durante toda la vida útil del proyecto |
| PMD-014 | Extensibilidad | Incorporación de nuevos requisitos funcionales mediante extensiones controladas, preservando compatibilidad con información existente |
| PMD-015 | Seguridad | Facilita protección de integridad, disponibilidad y confidencialidad según requisitos del proyecto |
| PMD-016 | Separación lógico/físico | Definición conceptual y lógica independiente de la implementación física en la base de datos |
| PMD-017 | Compatibilidad arquitectónica | Plena compatibilidad con la arquitectura general del sistema aprobada |
| PMD-018 | Compatibilidad con flujo de datos | Estructura soporta correctamente todas las transformaciones y movimientos definidos en el Flujo de Datos oficial |
| PMD-019 | Compatibilidad con modelo de decisión | Almacena toda la información necesaria para soportar el Modelo de Decisión aprobado, preservando trazabilidad de cada decisión |
| PMD-020 | Evolución controlada | Toda modificación se documenta, justifica y aprueba formalmente antes de incorporarse (ver REC-001) |

---

## 4. Objetivos del Modelo de Datos (OMD)

Resultados que la estructura de información debe alcanzar para soportar eficientemente todos los procesos del proyecto. Cada objetivo representa una capacidad a preservar durante diseño, implementación, mantenimiento y evolución.

| ID | Objetivo | Definición |
|---|---|---|
| OMD-001 | Centralizar información oficial | Modelo como fuente oficial de información para todos los módulos, procesos y componentes |
| OMD-002 | Representar el dominio del proyecto | Modelar estructuradamente todas las entidades, relaciones y atributos necesarios para representar el proceso completo de búsqueda y procesamiento de oportunidades |
| OMD-003 | Garantizar integridad | Toda información almacenada mantiene consistencia, validez y coherencia durante todo su ciclo de vida |
| OMD-004 | Soportar ciclo de vida de ofertas | Almacenamiento y seguimiento de toda información generada desde el descubrimiento hasta la finalización del procesamiento |
| OMD-005 | Garantizar trazabilidad | Preservar información necesaria para reconstruir historia de estados, decisiones, transformaciones y operaciones sobre cada oferta |
| OMD-006 | Facilitar intercambio de información | Estructura uniforme para intercambio consistente entre todos los módulos |
| OMD-007 | Minimizar redundancia | Evitar almacenamiento innecesario de datos duplicados; favorecer reutilización mediante relaciones apropiadas |
| OMD-008 | Facilitar auditoría | Permitir registro y consulta de información para auditoría, diagnóstico y monitoreo operacional |
| OMD-009 | Promover escalabilidad | Incorporar nuevas entidades, relaciones y atributos sin afectar significativamente la estructura existente |
| OMD-010 | Promover mantenibilidad | Organización clara, modular y consistente que facilite evolución y comprensión |
| OMD-011 | Optimizar acceso a información | Estructura que facilite consultas, búsquedas y operaciones requeridas por los módulos |
| OMD-012 | Preservar independencia tecnológica | Modelo independiente del motor de base de datos y tecnología de almacenamiento |
| OMD-013 | Soportar evolución del proyecto | Incorporación controlada de nuevos requisitos funcionales sin comprometer compatibilidad con información previamente almacenada |

---

## 5. Arquitectura General del Modelo de Datos

Organización conceptual de la información, estructurada de forma modular y coherente con la arquitectura general del sistema, el flujo de datos y los procesos funcionales.

### 5.1 Modelo Arquitectónico
Arquitectura organizada por **dominios funcionales**: cada conjunto de entidades representa una responsabilidad específica dentro de la automatización. Facilita comprensión del dominio, reduce acoplamiento entre entidades y promueve evolución independiente de cada área funcional.

### 5.2 Dominios Funcionales

| Dominio | Responsabilidad | Contenido |
|---|---|---|
| **Descubrimiento de oportunidades** | Información obtenida durante identificación y recolección de ofertas | Solo información correspondiente a esta etapa del flujo operacional |
| **Preparación inicial** | Normalización, validación inicial y preparación de información antes de evaluación | Datos generados durante la etapa de preparación de ofertas |
| **Evaluación inicial** | Resultados de la evaluación automática de ofertas | Información necesaria para soportar el modelo de decisión y clasificación inicial de oportunidades |
| **Procesamiento de ofertas** | Información generada durante el procesamiento profundo de ofertas seleccionadas | Diagnósticos, análisis, generación de documentos, resultados y otros procesos especializados |
| **Servicios compartidos** | Entidades reutilizadas por varios módulos | Evitar duplicación de datos y centralizar información común usada por diferentes procesos |
| **Configuración** | Parámetros, configuraciones, preferencias e información de control | Información usada para controlar el comportamiento de la automatización |
| **Auditoría y operación** | Monitoreo operacional del sistema | Información para auditoría, trazabilidad, manejo de errores, logs de ejecución, eventos relevantes y monitoreo |

### 5.3 Relaciones entre Dominios
- Cada dominio mantiene relaciones solo cuando existe necesidad funcional claramente identificada.
- Relaciones minimizan acoplamiento entre dominios y preservan independencia funcional de cada uno.
- Toda interacción entre dominios respeta el flujo de datos oficial definido.

### 5.4 Principios de Arquitectura
Preservar permanentemente: organización por dominios funcionales; bajo acoplamiento entre dominios; alta cohesión dentro de cada dominio; modularidad; escalabilidad; reutilización de información; integridad y consistencia de datos; trazabilidad completa; compatibilidad con la arquitectura general del sistema; evolución controlada (REC-001).

### 5.5 Evolución de Arquitectura
Aplica REC-001. Toda incorporación, modificación o eliminación de entidades respeta la arquitectura general definida. Cambios estructurales garantizan compatibilidad con el resto del modelo y documentación oficial.

---

## 6. Entidades del Sistema

Elementos fundamentales del modelo. Cada entidad modela un concepto único del dominio, tiene responsabilidad claramente definida y mantiene coherencia con principios, arquitectura, flujo de datos y modelo de decisión.

### 6.1 Clasificación de Entidades

| Tipo | Definición | Requisitos |
|---|---|---|
| **Principales** | Elementos centrales del dominio de negocio; información principal sobre la que se ejecutan procesos funcionales | Representar concepto específico del dominio; tener ciclo de vida claramente definido; relacionarse con otras entidades mediante reglas explícitas; mantener independencia de implementación física |
| **De soporte** | Complementan, parametrizan o enriquecen información de entidades principales | Evitar redundancia, promover reutilización, facilitar evolución del modelo; pueden ser compartidas por múltiples módulos |
| **Operacionales** | Representan funcionamiento interno de la automatización (no conceptos de negocio) | Gestión de estados, procesamiento interno, auditoría, manejo de errores, logs operacionales, ejecuciones, eventos, configuración, trazabilidad |

### 6.2 Inventario Oficial de Entidades
Derivado exclusivamente de documentación oficial previamente aprobada. Cada entidad incorporada debe cumplir mínimo:
- Necesidad funcional claramente identificada.
- Respaldo por uno o más requisitos funcionales.
- Compatibilidad con el flujo de datos oficial.
- Coherencia con el modelo de decisión.
- Respeto a la arquitectura general del sistema.
- No duplicar responsabilidades de otra entidad existente.
- Integrable con el resto del modelo sin generar inconsistencias.

**Entidades sin justificación funcional o arquitectónica adecuada no pueden incorporarse.**

### 6.3 Evolución de Entidades
Aplica REC-001. Toda incorporación, modificación, unificación o eliminación preserva compatibilidad con información existente, trazabilidad histórica y coherencia documental.

---

## 7. Relaciones entre Entidades

Definen cómo interactúan los elementos del modelo para representar coherentemente el dominio funcional. Toda relación responde a necesidad funcional claramente identificada, respeta la arquitectura y mantiene integridad del modelo. Constituyen marco normativo para construcción del modelo lógico e implementación física.

### 7.1 Principios Generales
Toda relación debe:
- Responder a requisito funcional del proyecto.
- Mantener integridad referencial.
- Evitar redundancias innecesarias.
- Minimizar acoplamiento entre dominios.
- Facilitar trazabilidad de información.
- Mantener coherencia con el flujo de datos oficial.
- Respetar la arquitectura modular del sistema.
- Permitir evolución controlada del modelo (REC-001).

### 7.2 Tipos de Relación por Alcance

| Tipo | Definición | Regla |
|---|---|---|
| **Intra-dominio** | Entre entidades del mismo dominio funcional | Mantener alta cohesión; evitar dependencias innecesarias con otros dominios |
| **Inter-dominio** | Entre entidades de dominios diferentes | Solo con necesidad funcional claramente documentada; diseñar con mínimo acoplamiento posible entre dominios |

### 7.3 Cardinalidad
Toda relación define explícitamente su cardinalidad durante la construcción del modelo lógico. Tipos mínimos a identificar donde aplique:
- Uno a uno (1:1)
- Uno a muchos (1:N)
- Muchos a muchos (N:M)

La selección de cardinalidad se justifica según necesidades funcionales del proyecto.

### 7.4 Integridad Referencial
Relaciones preservan permanentemente la integridad referencial. **No se permiten** relaciones que generen registros huérfanos, inconsistencias o dependencias inválidas entre entidades. Reglas específicas de actualización y eliminación se definen durante diseño del modelo lógico e implementación física.

### 7.5 Dependencias entre Entidades
Mantener al mínimo necesario para representar correctamente el dominio. Toda dependencia se justifica y documenta adecuadamente.

### 7.6 Relaciones No Permitidas
Relaciones que:
- Dupliquen información ya representada por otras relaciones.
- Introduzcan dependencias circulares injustificadas.
- Aumenten innecesariamente la complejidad del modelo.
- Contradigan la arquitectura general del sistema o el flujo de datos oficial.

### 7.7 Compatibilidad con Flujo de Datos
Relaciones facilitan intercambio de información entre módulos según el flujo oficial de procesamiento. La estructura relacional no obstaculiza la ejecución de ninguna etapa del proceso.

### 7.8 Evolución de Relaciones
Aplica REC-001.

---

## 8. Atributos de Entidades

Propiedades que describen la información almacenada por cada elemento del modelo. Todo atributo aporta significado funcional claro, mantiene coherencia con su dominio y cumple los principios del modelo. La definición detallada de atributos individuales se realiza en el **Diccionario Oficial de Datos**; este capítulo establece solo reglas generales.

### 8.1 Principios Generales
Todo atributo debe:
- Representar una única propiedad del dominio.
- Tener significado claro y no ambiguo.
- Estar respaldado por necesidad funcional.
- Mantener coherencia con la entidad a la que pertenece.
- Cumplir estándares oficiales de nomenclatura del proyecto.
- Ser validable según reglas objetivas.
- Evitar redundancias innecesarias.
- Mantener independencia de implementación física.

### 8.2 Clasificación de Atributos

| Categoría | Definición | Ejemplos/Notas |
|---|---|---|
| **Identificación** | Identifican unívocamente una instancia de entidad | Base para identificación lógica de registros dentro del modelo |
| **De negocio** | Información específica del dominio funcional de la entidad | Describen características principales del concepto modelado; constituyen la mayor parte de la información usada por la automatización |
| **De relación** | Establecen vínculos entre entidades y representan asociaciones definidas por el modelo | Preservar integridad referencial; minimizar acoplamiento entre entidades |
| **De control** | Gestionan ciclo de vida de registros | Estados, indicadores de versión, fechas operacionales y otros elementos necesarios para controlar comportamiento de la información |
| **De auditoría** | Registran información necesaria para garantizar trazabilidad y seguimiento histórico | Facilitan diagnóstico, auditoría y análisis de evolución de información |

### 8.3 Tipado de Atributos
Todo atributo define un tipo de dato compatible con la naturaleza de la información que representa. La selección prioriza: precisión, consistencia, eficiencia, facilidad de validación, compatibilidad con el modelo lógico. Tipos específicos se definen durante diseño del modelo lógico y se documentan en el Diccionario Oficial de Datos.

### 8.4 Obligatoriedad
Cada atributo se clasifica como **obligatorio** u **opcional** según requisitos funcionales. La obligatoriedad se justifica funcionalmente y permanece consistente durante la evolución del modelo.

### 8.5 Validación
Todo atributo tiene reglas de validación que garantizan calidad e integridad. Reglas pueden incluir donde aplique: longitud, formato, dominio de valores, rangos permitidos, unicidad, obligatoriedad, consistencia con otros atributos. Reglas específicas se documentan en el Diccionario Oficial de Datos.

### 8.6 Atributos Derivados
Información obtenible determinísticamente de otros atributos **no se almacena**, salvo justificación técnica o funcional debidamente documentada. Cuando se persiste un atributo derivado, se establecen mecanismos que garanticen permanentemente su consistencia con la información fuente.

### 8.7 Evolución de Atributos
Aplica REC-001.

---

## 9. Reglas de Integridad de Datos

Criterios oficiales que garantizan consistencia, validez, confiabilidad y coherencia de toda la información gestionada. Obligatorias durante diseño del modelo, implementación de base de datos, procesos de validación, intercambio de información entre módulos, y cualquier operación de creación, modificación, eliminación o consulta de datos.

| ID | Tipo de Integridad | Definición |
|---|---|---|
| INT-001 | **Entidad** | Toda entidad tiene mecanismo para identificación única de cada registro. No se permiten registros ambiguos o no identificables inequívocamente |
| INT-002 | **Referencial** | Toda relación preserva coherencia entre registros relacionados. No se permiten referencias a entidades inexistentes ni relaciones que generen registros huérfanos o inconsistentes. Reglas específicas de actualización/eliminación se definen en diseño del modelo lógico |
| INT-003 | **Dominio** | Cada atributo solo admite valores compatibles con su naturaleza, significado y propósito funcional. Dominios válidos se definen mediante reglas de validación claramente documentadas |
| INT-004 | **Funcional** | Toda información almacenada cumple reglas funcionales establecidas en requisitos del proyecto, modelo de decisión y flujo oficial. No se almacena información que contradiga el comportamiento esperado de la automatización |
| INT-005 | **Temporal** | Evolución de información respeta orden lógico y cronológico definido para ciclo de vida de cada oferta y procesos asociados. No pueden ocurrir transiciones, estados o secuencias temporales incompatibles con el flujo oficial |
| INT-006 | **Auditoría** | Toda operación relevante que modifica información es reconstruible mediante mecanismos oficiales de auditoría y trazabilidad. Eliminación o modificación de información no compromete reconstrucción de historia cuando deba preservarse |
| INT-007 | **Operacional** | Errores de ejecución, interrupciones de procesamiento o fallas recuperables no generan estados inconsistentes en el modelo. Mecanismos de recuperación preservan coherencia durante todo el ciclo de procesamiento |
| INT-008 | **Semántica** | Información generada por procesos automáticos o IA se valida antes de incorporarse al modelo donde aplique. Validación garantiza coherencia con contexto funcional, reglas del proyecto e información previamente almacenada. Incorporación de información generada automáticamente no compromete consistencia ni confiabilidad del modelo |

### 9.1 Validación de Integridad
Mecanismos de validación se ejecutan antes, durante o después de operaciones de datos, según naturaleza de cada regla. Toda violación de regla de integridad se gestiona según el Modelo de Manejo de Errores aprobado.

### 9.2 Evolución de Reglas de Integridad
Aplica REC-001.

---

## 10. Catálogos y Tablas de Referencia

Mecanismo oficial para centralizar información reutilizable usada por la automatización. Garantizan consistencia de datos, reducen duplicación y facilitan administración de valores compartidos por diferentes módulos. La incorporación de un catálogo responde siempre a necesidad funcional claramente identificada y respeta los principios del modelo.

### 10.1 Propósito
Proveer fuente única de información para conjuntos de valores usados recurrentemente. Su uso promueve: normalización de información, reutilización de datos, consistencia entre módulos, mantenimiento simplificado, evolución controlada del modelo.

### 10.2 Criterios para Creación de Catálogos
Un conjunto de valores puede modelarse como catálogo solo cuando cumple **uno o más** de:
- Es reutilizado por múltiples entidades.
- Es usado por diferentes módulos de la automatización.
- Requiere administración centralizada.
- Puede modificarse sin alterar lógica del sistema.
- Representa concepto estable del dominio del proyecto.
- Es necesario para procesos de validación o normalización.
- Contribuye a reducir redundancia de información.

**Evitar creación de catálogos que no aporten beneficio funcional o arquitectónico.**

### 10.3 Clasificación de Catálogos

| Tipo | Definición |
|---|---|
| **Funcionales** | Conceptos específicos del dominio de negocio usados durante procesamiento de ofertas |
| **Geográficos** | Información relacionada con ubicaciones geográficas usadas por la automatización |
| **Técnicos** | Información para funcionamiento interno del sistema: estados, tipos, clasificaciones y otros elementos técnicos |
| **De configuración** | Valores para parametrizar comportamiento de la automatización sin requerir modificaciones a lógica del sistema |

### 10.4 Reglas de Uso
- **Reutilización:** Toda entidad que requiera información representada por un catálogo oficial debe reutilizarlo en lugar de almacenar la misma información nuevamente. **No se permiten catálogos duplicados** que representen el mismo concepto funcional.
- **Integridad:** Valores contenidos en catálogos permanecen consistentes, completos y compatibles con el resto del modelo. Toda modificación a un catálogo preserva integridad referencial de entidades que dependen de él.
- **Administración:** Incorporación, modificación, desactivación o eliminación de valores se realiza mediante procedimientos controlados que garanticen consistencia del modelo. Reglas específicas se definen durante diseño del modelo lógico y se documentan en el Diccionario Oficial de Datos.

### 10.5 Alternativas a Catálogos
Cuando un conjunto de valores no cumple criterios para catálogo oficial, puede representarse mediante otros mecanismos de implementación, siempre que la decisión esté técnicamente justificada y no comprometa mantenibilidad, consistencia ni evolución del modelo. Selección del mecanismo más apropiado se realiza durante diseño del modelo lógico y se documenta según arquitectura del proyecto.

### 10.6 Evolución de Catálogos
Aplica REC-001.

---

## 11. Estados del Sistema

Representan la situación funcional u operacional de las entidades durante su ciclo de vida dentro de la automatización. Controlan evolución de información, garantizan consistencia de procesamiento y permiten seguimiento completo de cada entidad desde su creación hasta el fin de su participación en el sistema. Toda entidad cuyo comportamiento evoluciona a través de diferentes etapas gestiona su ciclo de vida mediante estados claramente definidos.

### 11.1 Principios Generales
Estados deben:
- Representar situaciones reales del dominio o del funcionamiento interno del sistema.
- Mantener coherencia con el flujo de datos oficial.
- Respetar el Modelo de Decisión del proyecto.
- Facilitar trazabilidad de procesamiento.
- Permitir auditoría de transiciones.
- Promover recuperación controlada desde errores.
- Mantener independencia de implementación tecnológica.

### 11.2 Clasificación de Estados

| Tipo | Definición |
|---|---|
| **De negocio** | Progreso funcional de entidades dentro del proceso de búsqueda y procesamiento de oportunidades |
| **Operacionales** | Estado de ejecución de procesos internos de la automatización |
| **De control** | Condiciones administrativas, técnicas o temporales necesarias para controlar comportamiento del sistema |

### 11.3 Modelo Basado en Máquinas de Estado
Toda entidad con ciclo de vida se modela conceptualmente como **máquina de estados**. Cada máquina de estados define mínimo:
- Estado inicial.
- Estados permitidos.
- Transiciones válidas.
- Condiciones necesarias para cada transición.
- Estados finales, donde aplique.

**No se permiten transiciones que no hayan sido definidas como válidas** para la entidad correspondiente.

### 11.4 Transiciones de Estado
Toda transición responde a evento funcional u operacional claramente identificado. Transiciones deben:
- Mantener coherencia con el flujo oficial de procesamiento.
- Respetar reglas del Modelo de Decisión.
- Preservar integridad de la información.
- Prevenir secuencias incompatibles con el ciclo de vida de la entidad.

### 11.5 Registro de Transiciones
Toda transición relevante entre estados se registra mediante mecanismos oficiales de trazabilidad y auditoría. El registro permite reconstruir historia completa de evolución de la entidad cuando sea necesario.

### 11.6 Validación de Estados
Antes de realizar una transición, el sistema verifica:
- La entidad está en estado válido.
- La transición solicitada está permitida.
- Se cumplen las condiciones funcionales necesarias.
- No se compromete la integridad del modelo de datos.

Validaciones específicas se definen durante diseño del modelo lógico e implementación del sistema.

### 11.7 Recuperación desde Estados Inconsistentes
Cuando un proceso detecta transición inválida o estado inconsistente, aplica estrategias definidas en el Modelo de Manejo de Errores. La recuperación no compromete integridad, trazabilidad ni consistencia de la información almacenada.

### 11.8 Evolución de Estados
Aplica REC-001.

---

## 12. Identificadores y Claves

Mecanismos oficiales para garantizar identificación única de entidades y correcta representación de relaciones dentro del modelo. Preservan integridad referencial, facilitan trazabilidad y mantienen estabilidad del modelo durante la evolución. Toda entidad tiene mecanismos de identificación definidos según estos principios.

### 12.1 Principios Generales
Identificadores y claves deben:
- Garantizar identificación única de cada registro.
- Mantener estabilidad durante todo el ciclo de vida de la entidad.
- Preservar integridad referencial del modelo.
- Mantener independencia de cambios en información de negocio.
- Facilitar evolución y mantenibilidad del sistema.
- Evitar ambigüedades en relaciones entre entidades.

### 12.2 Tipos de Identificadores y Claves

| Tipo | Definición | Reglas |
|---|---|---|
| **Identificador técnico** | Identidad estable del registro dentro del sistema | Único; inmutable durante toda la existencia del registro; no depende de información sujeta a modificación; no se reutiliza una vez asignado; mecanismo principal de identificación dentro del modelo. Estrategia específica de generación se define durante diseño del modelo lógico |
| **Clave primaria** | Identificación inequívoca de cada registro | Construida usando el identificador técnico oficial de la entidad, salvo justificación arquitectónica documentada para estrategia diferente |
| **Claves alternas** | Identificadores específicos del dominio funcional | Mantener unicidad donde aplique; no reemplazan la clave primaria; pueden ser modificables cuando la naturaleza del negocio lo requiera; consistencia con reglas funcionales del proyecto |
| **Claves foráneas** | Implementan relaciones entre entidades | Referencian entidad existente; coherencia con relaciones definidas en modelo lógico; cumplimiento de reglas de actualización y eliminación establecidas para cada relación |

### 12.3 Restricciones de Unicidad
Cuando la naturaleza funcional de la información lo requiera, el modelo establece restricciones de unicidad adicionales sobre uno o más atributos. Complementan la identificación técnica y garantizan consistencia de información de negocio.

### 12.4 Reutilización de Identificadores
Identificadores técnicos pertenecientes a registros previamente existentes **no se reutilizan**, incluso cuando dichos registros hayan sido eliminados, archivados o desactivados. Garantiza preservación de trazabilidad histórica y evita ambigüedades durante evolución del sistema.

### 12.5 Evolución de Identificadores y Claves
Aplica REC-001. Modificaciones preservan integridad referencial, compatibilidad con información existente y coherencia documental.

---

## 13. Modelo Lógico de Datos

Representación oficial de la estructura lógica de la información gestionada. Consolida organización de entidades, relaciones, mecanismos de identificación y reglas estructurales, proporcionando representación independiente de cualquier tecnología de almacenamiento específica. Sirve como referencia directa para implementación del modelo físico y mantiene coherencia con toda la documentación oficial.

### 13.1 Propósito
Representar completa, consistente y estructuralmente todos los componentes del modelo de datos. Diseño garantiza: coherencia estructural, integridad de información, independencia tecnológica, escalabilidad, trazabilidad, compatibilidad con la arquitectura general del sistema.

### 13.2 Alcance
El modelo lógico integra mínimo:
- Entidades oficiales del sistema.
- Relaciones entre entidades.
- Cardinalidades.
- Mecanismos de identificación.
- Claves primarias.
- Claves alternas.
- Claves foráneas.
- Catálogos relacionados.
- Máquinas de estado aplicables.
- Restricciones lógicas necesarias para preservar integridad del modelo.

**El detalle completo de atributos individuales permanece documentado exclusivamente en el Diccionario Oficial de Datos.**

### 13.3 Estructura Uniforme de Entidades
Toda entidad incorporada al modelo lógico se documenta usando estructura uniforme que facilite comprensión, mantenimiento y evolución. Mínimo incluye:
- Nombre oficial.
- Dominio funcional.
- Tipo de entidad.
- Descripción funcional.
- Responsabilidad principal.
- Relaciones relevantes.
- Cardinalidades.
- Identificador técnico.
- Claves alternas, donde existan.
- Claves foráneas, donde aplique.
- Catálogos asociados.
- Máquina de estado, donde aplique.
- Observaciones arquitectónicas relevantes.

### 13.4 Coherencia Estructural
Toda entidad y relación incorporada al modelo lógico mantiene coherencia con: requisitos funcionales y no funcionales, flujo de datos oficial, Modelo de Decisión, Arquitectura General del Sistema, principios del modelo de datos, reglas de integridad, mecanismos oficiales de identificación. **No pueden incorporarse elementos que contradigan la arquitectura aprobada del proyecto.**

### 13.5 Independencia del Modelo Físico
El modelo lógico permanece independiente de cualquier motor de base de datos, tecnología de persistencia o decisión específica de implementación. Decisiones sobre tipos de datos físicos, índices, optimizaciones de almacenamiento o configuraciones específicas del sistema de gestión de bases de datos forman parte del modelo físico, no del modelo lógico.

### 13.6 Validación del Modelo Lógico
Antes de aprobar el modelo lógico, verificar:
- Todas las entidades oficiales están representadas.
- Todas las relaciones son consistentes.
- Cardinalidades correctamente definidas.
- Mecanismos de identificación coherentes.
- Reglas de integridad aplicables correctamente.
- Modelo soporta completamente el flujo funcional de la automatización.

### 13.7 Evolución del Modelo Lógico
Aplica REC-001.

---

## 14. Persistencia y Almacenamiento

Principios oficiales para conservación, administración y disponibilidad de información. Garantizan que toda información gestionada mantenga integridad, consistencia, trazabilidad y disponibilidad durante el tiempo necesario, independientemente de la tecnología de almacenamiento. Decisiones de implementación física respetan estos principios y se alinean con el Stack Tecnológico aprobado.

### 14.1 Principios Generales
Toda información persistida debe:
- Mantener integridad y consistencia durante todo su ciclo de vida.
- Preservar trazabilidad donde aplique.
- Evitar redundancias innecesarias.
- Promover recuperación desde errores.
- Mantener independencia del mecanismo físico de almacenamiento.
- Garantizar compatibilidad con el modelo oficial de datos.
- Facilitar evolución futura del sistema.

### 14.2 Clasificación de Información según Ciclo de Vida

| Tipo | Definición | Reglas |
|---|---|---|
| **Permanente** | Conocimiento principal del sistema; preservación necesaria durante toda la vida útil del proyecto | Eliminación solo mediante procedimientos formalmente autorizados |
| **Histórica** | Preserva trazabilidad, auditoría y reconstrucción de historia de procesos | Preservación debe garantizar posibilidad de análisis histórico cuando sea necesario |
| **Temporal** | Usada solo durante ciertas etapas de procesamiento; permanencia innecesaria una vez completada su función | Ciclo de vida gestionado mediante políticas controladas de limpieza y eliminación |
| **De configuración** | Controla comportamiento de la automatización | Persistencia garantiza reproducibilidad de ejecuciones y estabilidad operacional del sistema |

### 14.3 Retención de Información
Políticas de retención consideran: naturaleza funcional de la información, requisitos de auditoría y trazabilidad, necesidades operacionales del sistema, criterios de mantenimiento del proyecto. **No debe eliminarse información cuya preservación sea necesaria para garantizar integridad o trazabilidad del sistema.**

### 14.4 Eliminación de Información
Solo mediante procedimientos controlados que preserven consistencia del modelo. Toda eliminación respeta: reglas de integridad referencial, dependencias existentes entre entidades, necesidades de auditoría, políticas oficiales de retención.

### 14.5 Disponibilidad
Persistencia garantiza que información permanezca disponible para procesos autorizados cuando sea necesario. Mecanismos específicos de acceso se definen durante implementación física del sistema.

### 14.6 Independencia Tecnológica
Reglas de persistencia permanecen independientes del motor de base de datos, mecanismo de almacenamiento o tecnología específica. Decisiones tecnológicas correspondientes se rigen por el Stack Tecnológico oficial del proyecto.

### 14.7 Evolución de Estrategia de Persistencia
Aplica REC-001.

### 14.8 Módulo de Descubrimiento (módulo 1) — Decisiones Específicas

Decisiones de persistencia del módulo de Descubrimiento de Oportunidades, incorporadas oficialmente:

| ID | Fecha | Decisión | Detalle |
|---|---|---|---|
| **D1** | 2026-08-07 | `active` de entidad Source | Atributo de catálogo para administración externa (manual); el runtime del módulo **no** filtra fuentes por este atributo |
| **D2** | 2026-08-07 | Tienda única | Todas las tiendas lógicas del módulo —ofertas (`ofertas`), eventos (`eventos`), sesiones (`sesiones`), corridas (`corridas`), bloqueo (`bloqueo`)— persisten como tablas de la misma base de datos SQLite única (`job_search.db`), conforme a sección 14.6 (independencia tecnológica) y decisión del Stack Tecnológico que estableció SQLite como tienda única del MVP |
| **D3** | 2026-08-07 | Auditoría de sesiones (mínima viable) | Tabla de auditoría de sesiones registra **solo sesiones exitosas** y contiene campos esenciales: `session_id`, `run_id`, `source_id`, `set_indice`, `timestamp`, `total_declarado`, `conteo`, `estado`. Intentos fallidos se reportan como eventos, nunca como sesiones. **Credenciales, tokens y cookies nunca se almacenan** (según hoja técnica) |
| **D4** | 2026-08-09 | Registro de capturas sin FKs de catálogo (Sub-fase 4.4) | `ofertas` **no** declara restricciones FK; `empresa_id` y `ubicacion_id` son nullable y se almacenan como `NULL` en captura del MVP, mientras las cadenas crudas del adaptador se conservan en `empresa_nombre` y `ubicacion_nombre` (y `source_id` de la fuente en `fuente_id`). Registro es un upsert deduplicando por `id_externo_url` y refrescando `timestamp_ultima_verificacion`. **Justificación:** los catálogos no se resuelven en Módulo 1, por lo que restricciones FK rechazaban capturas válidas (FOREIGN KEY constraint failed) |

---

## 15. Versionado y Evolución del Modelo de Datos

El modelo de datos es componente estratégico de la arquitectura y evoluciona de manera controlada durante todo el ciclo de vida del proyecto. Toda modificación preserva integridad del modelo, garantiza compatibilidad con información existente y mantiene coherencia con documentación oficial. El proceso de evolución es completamente documentado, justificado y trazable.

### 15.1 Principios Generales de Evolución
Toda evolución debe:
- Mantener integridad estructural del modelo.
- Preservar consistencia de información existente.
- Minimizar impacto en módulos del sistema.
- Mantener compatibilidad con arquitectura general.
- Promover escalabilidad del proyecto.
- Garantizar trazabilidad de todas las modificaciones.
- Permitir recuperación de versiones anteriores cuando sea necesario.

### 15.2 Esquema de Versionado
Esquema formal que permita identificar claramente cada revisión oficial. Cada versión se asocia mínimo con:
- Identificador de versión.
- Fecha de aprobación.
- Descripción de cambios realizados.
- Justificación funcional o arquitectónica correspondiente.
- Análisis de impacto realizado.
- Aprobación formal del cambio.

### 15.3 Clasificación de Cambios

| Por naturaleza | Definición |
|---|---|
| **Evolutivos** | Incorporan nuevas capacidades o expanden el modelo existente sin alterar su propósito general |
| **Correctivos** | Corrigen errores, inconsistencias o mejoras identificadas durante evolución del proyecto |
| **Estructurales** | Modifican organización general del modelo y requieren análisis exhaustivo de impacto antes de incorporación |

| Por compatibilidad | Definición | Ejemplos |
|---|---|---|
| **Compatibles** | Preservan compatibilidad con información existente y no requieren modificaciones significativas en componentes que usan el modelo | Incorporación de nuevas entidades independientes; adición de atributos opcionales; incorporación de nuevos catálogos; extensiones compatibles con arquitectura existente |
| **Incompatibles** | Pueden afectar estructura del modelo, información almacenada u operación de módulos de la automatización | Eliminación de entidades; modificación de mecanismos de identificación; cambios en cardinalidades; eliminación de atributos usados por otros componentes; alteraciones que comprometan compatibilidad con versiones anteriores |

**Todo cambio incompatible debe estar respaldado por análisis de impacto específico antes de su aprobación.**

### 15.4 Gestión de Historial de Cambios
Historia de evolución permanece disponible durante toda la vida útil del proyecto. Cada modificación registra: versión afectada, elementos modificados, naturaleza del cambio, justificación correspondiente, decisiones arquitectónicas relacionadas.

### 15.5 Evaluación de Impacto
Antes de aprobar cualquier modificación, evaluación de impacto considera mínimo:
- Compatibilidad con información existente.
- Integridad del modelo.
- Arquitectura general del sistema.
- Flujo de datos oficial.
- Modelo de Decisión.
- Mecanismos de persistencia.
- Procesos de auditoría y trazabilidad.

### 15.6 Aprobación de Cambios
Toda modificación se documenta, justifica y aprueba formalmente antes de incorporarse a nueva versión oficial. **No pueden incorporarse cambios cuya necesidad funcional o arquitectónica no haya sido debidamente demostrada.**

### 15.7 Evolución Controlada
Evolución planificada garantizando estabilidad del sistema, mantenibilidad del proyecto y coherencia con documentación oficial. Toda nueva versión preserva principios arquitectónicos establecidos en este documento.

---

## 16. Trazabilidad y Auditoría

Mecanismos oficiales para garantizar seguimiento completo de información gestionada y operaciones realizadas durante todo su ciclo de vida. Permiten reconstrucción de procesos, facilitan diagnóstico de incidentes, soportan el modelo de decisión y preservan confiabilidad de información almacenada. Toda la arquitectura del modelo de datos se diseña para que información relevante pueda ser trazada, auditada y analizada cuando sea necesario.

### 16.1 Principios Generales
Trazabilidad y auditoría deben:
- Preservar integridad histórica de información.
- Permitir reconstrucción de procesos relevantes.
- Mantener coherencia con el flujo de datos oficial.
- Promover diagnóstico de incidentes.
- Soportar el Modelo de Decisión.
- Facilitar evolución y mantenimiento del sistema.
- Mantener independencia de implementación tecnológica.

### 16.2 Alcance de Trazabilidad
Cubre mínimo:
- Ciclo de vida de entidades principales.
- Transiciones entre estados.
- Operaciones relevantes realizadas sobre información.
- Decisiones funcionales que afectan procesamiento.
- Eventos operacionales necesarios para entender evolución del sistema.

Información registrada debe ser suficiente para reconstruir procesos cuando sea necesario.

### 16.3 Clasificación de Auditoría

| Tipo | Definición |
|---|---|
| **Funcional** | Eventos relacionados con comportamiento funcional de la automatización y procesamiento de ofertas |
| **Técnica** | Eventos relacionados con operación interna del sistema, ejecución de procesos y funcionamiento de componentes técnicos |
| **De cambios** | Modificaciones realizadas a información persistente y a elementos relevantes del modelo de datos |

### 16.4 Trazabilidad de Contexto de Decisión
Toda decisión relevante generada durante la automatización debe ser contextualizable cuando sea necesario. Información de trazabilidad permite identificar mínimo:
- Proceso que originó la decisión.
- Momento en que fue tomada.
- Información usada como entrada.
- Resultado obtenido.
- Componente responsable de la ejecución.
- Versión de reglas, configuraciones o modelos aplicables donde corresponda.

Nivel de detalle registrado debe ser suficiente para explicar contexto funcional de la decisión sin comprometer eficiencia ni mantenibilidad del sistema.

### 16.5 Integridad de Auditoría
Registros de auditoría permanecen protegidos contra modificaciones no autorizadas que comprometan confiabilidad de información histórica. Toda alteración a información de auditoría se documenta y autoriza debidamente.

### 16.6 Retención de Información de Auditoría
Preservada según políticas oficiales de persistencia definidas. Eliminación solo mediante procedimientos controlados que no comprometan trazabilidad de procesos relevantes.

### 16.7 Acceso a Información de Auditoría
Acceso solo para propósitos funcionales, operacionales, de diagnóstico, mantenimiento o análisis autorizados por la arquitectura del sistema. Organización de información facilita consulta sin afectar integridad del modelo.

### 16.8 Evolución de Mecanismos de Trazabilidad
Aplica REC-001.

---

## 17. Seguridad y Protección de Datos

Principios oficiales para preservar confidencialidad, integridad, disponibilidad y uso adecuado de información gestionada. Garantizan manejo seguro durante todo el ciclo de vida, manteniendo coherencia con arquitectura general, modelo de datos y principios del proyecto. Decisiones sobre mecanismos tecnológicos específicos de protección se rigen por el Stack Tecnológico y la implementación del sistema, sin alterar estos principios.

### 17.1 Principios Generales
Gestión de información cumple mínimo:
- Preservar confidencialidad de información.
- Garantizar integridad de datos.
- Mantener disponibilidad cuando sea necesario.
- Promover trazabilidad de operaciones relevantes.
- Proteger información contra modificaciones no autorizadas.
- Mantener coherencia con el Modelo de Manejo de Errores.
- Preservar estabilidad del modelo de datos.

### 17.2 Clasificación por Sensibilidad

| Nivel | Definición |
|---|---|
| **Pública** | Divulgación no representa impacto significativo para proyecto o usuario. Uso no requiere medidas especiales de protección más allá de las definidas por arquitectura general |
| **Uso interno** | Usada exclusivamente por la automatización para operación de procesos internos. Acceso limitado a componentes autorizados de la arquitectura |
| **Sensible** | Divulgación, modificación, pérdida o uso inadecuado podría afectar al usuario, operación de la automatización o integridad del proyecto. Recibe nivel de protección proporcional a su criticidad durante implementación |

### 17.3 Protección de Integridad
Toda operación sobre información preserva consistencia del modelo y respeta reglas oficiales de integridad. **No pueden incorporarse mecanismos que comprometan confiabilidad de información almacenada.**

### 17.4 Protección durante Ciclo de Vida
Medidas de protección cubren todas las etapas: creación, procesamiento, almacenamiento, consulta, modificación, archivado, eliminación. Estrategia de protección permanece consistente durante todas estas etapas.

### 17.5 Acceso a Información
Limitado exclusivamente a procesos, componentes y mecanismos autorizados por la arquitectura. Organización del modelo facilita aplicación de controles de acceso durante implementación, sin depender de mecanismo tecnológico específico.

### 17.6 Protección de Información Histórica
Información usada para auditoría, trazabilidad e historia se protege de manera que preserve permanentemente su integridad y confiabilidad. Toda modificación a información histórica se justifica, documenta y autoriza debidamente.

### 17.7 Compatibilidad con Arquitectura de Seguridad
Reglas de este capítulo permanecen compatibles con: Arquitectura General del Sistema, Stack Tecnológico oficial, Modelo de Manejo de Errores, políticas oficiales de persistencia, mecanismos de auditoría y trazabilidad.

### 17.8 Evolución de Políticas de Protección
Aplica REC-001.

---

## 18. Reglas de Validación de Datos

Principios oficiales que garantizan que toda información incorporada al modelo sea consistente, completa, válida y compatible con la arquitectura. Previenen incorporación de información incorrecta, preservan integridad del modelo y aseguran cumplimiento de reglas funcionales y arquitectónicas. Validaciones aplican durante todo el ciclo de vida de la información, independientemente del mecanismo tecnológico usado para su implementación.

### 18.1 Principios Generales
Toda validación debe:
- Verificar consistencia de información antes de su incorporación al modelo.
- Mantener coherencia con reglas de integridad definidas.
- Ser objetiva, reproducible y verificable.
- Mantener independencia de tecnología usada para implementación.
- Promover calidad de información.
- Reducir incorporación de datos inconsistentes.
- Mantener compatibilidad con Modelo de Decisión y flujo oficial de procesamiento.

### 18.2 Tipos de Validación

| Tipo | Definición | Contenido |
|---|---|---|
| **Estructurales** | Verifican requisitos básicos definidos para cada elemento del modelo | Obligatoriedad, tipo de dato, longitud, formato, dominio de valores, restricciones de unicidad. Reglas específicas se documentan en el Diccionario Oficial de Datos |
| **Funcionales** | Verifican cumplimiento de reglas de negocio establecidas para la automatización | Garantizan que información represente correctamente comportamiento esperado del dominio funcional |
| **Relacionales** | Verifican coherencia existente entre entidades relacionadas | Preservan integridad referencial y garantizan consistencia de relaciones definidas por el modelo |
| **Temporales** | Verifican coherencia cronológica de información durante ciclo de vida de entidades | No pueden registrarse secuencias temporales incompatibles con el flujo oficial |
| **Semánticas** | Verifican, donde aplique, que información generada automáticamente o mediante IA sea coherente con contexto funcional antes de incorporarse | Complementan reglas de integridad semántica; aplican cuando naturaleza de la información lo requiera. Garantizan: consistencia con dominio representado, respeto a reglas funcionales, coherencia con información previamente almacenada, no compromiso de integridad semántica |

### 18.3 Gestión de Errores de Validación
Toda validación fallida se gestiona según el Modelo de Manejo de Errores aprobado. **La incorporación de información al modelo no continúa cuando el incumplimiento de una regla de validación comprometa integridad, consistencia o confiabilidad de la información.**

### 18.4 Evolución de Reglas de Validación
Aplica REC-001.

---

## 19. Estrategia de Migración

Principios oficiales para gestionar evolución estructural del modelo de datos durante todo el ciclo de vida. Garantizan que cualquier modificación a la estructura persistente preserve integridad de información, mantenga compatibilidad con arquitectura aprobada y permita evolución controlada. Decisiones sobre herramientas específicas de migración se rigen por el Stack Tecnológico oficial y no forman parte de este documento.

### 19.1 Principios Generales
Toda migración debe:
- Mantener integridad de información.
- Preservar consistencia del modelo de datos.
- Garantizar trazabilidad de modificaciones.
- Mantener compatibilidad con arquitectura general.
- Ser reproducible y verificable.
- Promover evolución controlada del proyecto.
- Minimizar riesgo de pérdida o corrupción de información.

### 19.2 Alcance
Migraciones gestionan cualquier modificación estructural que afecte el modelo persistente, incluyendo donde aplique: incorporación de nuevas entidades, modificación de entidades existentes, cambios en relaciones, actualización de restricciones, incorporación o modificación de catálogos, ajustes derivados de evolución del modelo.

### 19.3 Clasificación de Migraciones

| Tipo | Definición |
|---|---|
| **Evolutivas** | Incorporan nuevas capacidades preservando compatibilidad con estructura existente |
| **Correctivas** | Corrigen errores, inconsistencias o deficiencias identificadas durante evolución |
| **Estructurales** | Introducen modificaciones significativas a organización del modelo y requieren análisis de impacto previo a ejecución |

### 19.4 Versionado de Migraciones
Toda migración se asocia con versión oficial del modelo de datos. Cada migración registra mínimo: identificador de migración, versión del modelo, descripción de la modificación, justificación funcional o arquitectónica, fecha de incorporación, resultado de ejecución.

### 19.5 Validación Previa a Migración
Antes de ejecutar, verificar mínimo:
- Consistencia del modelo de datos.
- Compatibilidad con versión anterior.
- Impacto sobre información existente.
- Cumplimiento de reglas de integridad.
- Compatibilidad con arquitectura general.

**Toda migración debe tener análisis de impacto documentado antes de su aprobación.**

### 19.6 Reversibilidad
Siempre que sea técnicamente factible, toda migración se diseña permitiendo revertir cambios y restaurar estado anterior. Cuando no pueda revertirse por limitaciones técnicas o naturaleza de la transformación, esta condición se documenta anticipadamente con justificación. En tales casos, se establecen medidas que minimicen riesgo a integridad y disponibilidad de información.

### 19.7 Trazabilidad de Migraciones
Toda migración forma parte de historia oficial de evolución del modelo. Documentación correspondiente permite reconstruir: versión origen, versión destino, cambios realizados, justificación de la modificación, impacto identificado, evidencia de aprobación.

### 19.8 Evolución de Estrategia de Migración
Aplica REC-001.

---

## 20. Criterios de Aceptación

Condiciones oficiales que el modelo de datos debe cumplir para considerarse completo, consistente y conforme con la arquitectura aprobada. Proveen conjunto de criterios objetivos para verificar calidad antes de aprobación oficial o incorporación de nuevas versiones. Cumplimiento obligatorio para toda versión oficial.

### 20.1 Integridad Estructural
Mínimo:
- Todas las entidades oficiales representadas.
- Todas las relaciones apropiadamente definidas y justificadas.
- Mecanismos oficiales de identificación documentados.
- Reglas de integridad correctamente aplicables.
- Sin inconsistencias estructurales dentro del modelo.

### 20.2 Coherencia Funcional
Modelo representa correctamente el dominio funcional. Mínimo verificar:
- Modelo soporta completamente el flujo oficial de procesamiento.
- Entidades representan correctamente conceptos del dominio.
- Relaciones reflejan necesidades funcionales del proyecto.
- Máquinas de estado compatibles con ciclo de vida de entidades correspondientes.

### 20.3 Calidad del Modelo
Demostrar que:
- Información puede mantenerse consistentemente.
- Redundancia innecesaria minimizada.
- Organización de entidades promueve mantenibilidad.
- Arquitectura permite evolución controlada del sistema.
- Modelo es escalable y extensible.

### 20.4 Cumplimiento de Reglas del Modelo
Antes de aprobación, verificar cumplimiento con: principios del modelo de datos, objetivos del modelo, reglas de integridad, reglas de validación, políticas de persistencia, principios de seguridad, mecanismos de trazabilidad y auditoría.

### 20.5 Coherencia Documental
Modelo completamente alineado con documentación oficial. Mínimo verificar compatibilidad con: requisitos funcionales y no funcionales, documentación estratégica del proyecto, flujo de datos oficial, Modelo de Decisión, Arquitectura General del Sistema, Stack Tecnológico aprobado, Modelo de Manejo de Errores, resto de documentos oficiales relacionados con arquitectura. **No deben existir contradicciones entre el modelo de datos y documentación oficial vigente.**

### 20.6 Completitud de Documentación
Antes de aprobar versión oficial, verificar disponibilidad mínima de:
- Modelo Lógico de Datos.
- Diccionario Oficial de Datos.
- Diagrama Oficial del Modelo de Datos.
- Historial de versiones correspondiente.
- Documentación de cambios aprobados.

### 20.7 Aprobación del Modelo
Modelo solo se considera oficialmente aprobado cuando todos los criterios de este capítulo han sido satisfactoriamente verificados. Toda excepción se documenta, justifica y aprueba formalmente antes de liberar nueva versión oficial.

### 20.8 Revalidación del Modelo
Toda modificación al modelo conduce a nueva evaluación de criterios de aceptación de este capítulo. **No puede aprobarse nueva versión mientras algún criterio de aceptación permanezca incumplido.**

---

## 21. Diccionario Oficial de Datos

Especificación técnica oficial del modelo de datos. Documenta completa, uniforme y trazablemente todos los elementos que componen el modelo, proporcionando fuente oficial única de información para diseño, implementación, mantenimiento y evolución. Toda entidad, atributo, relación, catálogo y componente del modelo se documenta según estructura establecida en este capítulo.

### 21.1 Objetivos
Centralizar documentación técnica del modelo; garantizar uniformidad en definición de elementos; facilitar implementación de base de datos; promover mantenibilidad; servir como referencia oficial para desarrollo y evolución; mantener trazabilidad con resto de documentación oficial.

### 21.2 Alcance
Documenta mínimo: entidades, atributos, relaciones, claves primarias, claves alternas, claves foráneas, catálogos, restricciones, reglas de validación, máquinas de estado donde aplique, observaciones arquitectónicas relevantes. **No debe existir elemento persistente del modelo de datos que no esté documentado en este diccionario.**

### 21.3 Plantilla Oficial para Entidades
Toda entidad documentada con estructura uniforme. Mínimo incluye:

| Sección | Contenido |
|---|---|
| **Información general** | Nombre oficial, dominio funcional, tipo de entidad, descripción funcional, responsabilidad principal |
| **Identificación** | Identificador técnico, clave primaria, claves alternas |
| **Relaciones** | Entidades relacionadas, cardinalidades, claves foráneas, dependencias relevantes |
| **Ciclo de vida** | Máquina de estado donde aplique, estados principales, observaciones relacionadas con ciclo de vida |
| **Catálogos asociados** | Lista de catálogos usados por la entidad |
| **Observaciones arquitectónicas** | Información relevante para entender rol de la entidad dentro del modelo |

### 21.4 Plantilla Oficial para Atributos
Todo atributo documentado con estructura uniforme. Mínimo incluye:
- Nombre oficial.
- Descripción funcional.
- Tipo lógico.
- Tipo físico, donde aplique durante implementación.
- Categoría de atributo.
- Obligatoriedad.
- Valor por defecto, donde aplique.
- Dominio de valores.
- Restricciones.
- Reglas de validación.
- Restricciones de unicidad, donde existan.
- Nivel de sensibilidad.
- Clasificación según persistencia.
- Observaciones relevantes.

### 21.5 Trazabilidad Documental
Mantener trazabilidad con resto de documentación oficial. Donde aplique, cada entidad indica relación con: requisitos funcionales asociados, dominio arquitectónico al que pertenece, flujo de datos oficial, Modelo de Decisión, máquinas de estado correspondientes, catálogos usados, reglas de integridad aplicables, reglas de validación relacionadas.

Donde pertinente, cada atributo puede documentar: regla de validación correspondiente, regla de integridad asociada, clasificación según sensibilidad, clasificación según persistencia, observaciones arquitectónicas relevantes.

### 21.6 Consistencia del Diccionario
Toda información documentada permanece consistente con: Modelo Lógico de Datos, Diagrama Oficial del Modelo de Datos, principios del modelo de datos, arquitectura general del sistema, resto de documentación oficial. **No se permiten contradicciones entre el diccionario y otros artefactos oficiales.**

### 21.7 Mantenimiento del Diccionario
Toda incorporación, modificación o eliminación se realiza de manera controlada. Modificaciones deben: mantener trazabilidad documental, preservar consistencia del modelo, actualizar documentación relacionada donde aplique, mantener sincronizados Modelo Lógico de Datos y Diagrama Oficial del Modelo de Datos.

### 21.8 Evolución del Diccionario
Evoluciona junto con el modelo de datos. Toda modificación se documenta, justifica y aprueba formalmente antes de incorporarse a nueva versión oficial. El diccionario constituye fuente oficial de referencia para definición detallada de elementos del modelo y debe permanecer permanentemente actualizado.

---

## 22. Diagrama Oficial del Modelo de Datos

Representación gráfica oficial de la estructura lógica de la información. Facilita comprensión de organización general del modelo mostrando visualmente entidades, relaciones y estructura general, manteniendo coherencia con Modelo Lógico de Datos y Diccionario Oficial. Debe permanecer permanentemente sincronizado con estos artefactos y **no constituye la fuente oficial para definición del modelo de datos**.

### 22.1 Propósito
Representar gráficamente estructura lógica del modelo; facilitar comprensión de relaciones entre entidades; promover análisis arquitectónico del sistema; servir como soporte para desarrollo y mantenimiento; mantener coherencia con toda la documentación oficial.

### 22.2 Alcance
Representa mínimo: entidades oficiales del modelo, relaciones existentes entre entidades, cardinalidades correspondientes, dominios funcionales cuando sea conveniente para comprensión, clasificación de entidades según arquitectura del proyecto, catálogos oficiales cuando formen parte del modelo lógico, dependencias estructurales relevantes. Inclusión de información adicional debe justificarse por su utilidad para comprensión de arquitectura del modelo.

### 22.3 Representación Gráfica
Facilitar comprensión evitando complejidad innecesaria. Debe:
- Mantener organización clara y uniforme.
- Minimizar cruces innecesarios entre relaciones.
- Promover legibilidad.
- Mantener consistencia en simbología usada.
- Facilitar evolución conforme crece el modelo.

Notación gráfica específica se define durante fase de implementación y debe permanecer uniforme en todas las versiones del diagrama.

### 22.4 Relación con Modelo Lógico
Derivado directamente del Modelo Lógico de Datos. Toda modificación estructural hecha al modelo lógico se refleja posteriormente en el diagrama oficial. **El diagrama no puede contener elementos que no existan en el Modelo Lógico de Datos.**

### 22.5 Relación con Diccionario Oficial
Toda entidad representada en el diagrama está documentada en el Diccionario Oficial. Relaciones, mecanismos de identificación y otros elementos representados gráficamente mantienen coherencia con documentación técnica correspondiente. El diagrama constituye representación visual del modelo y **no reemplaza** la especificación detallada contenida en el diccionario.

### 22.6 Versionado del Diagrama
Versionado consistentemente con versiones oficiales del modelo de datos. Cada versión se asocia con Modelo Lógico de Datos y Diccionario Oficial correspondientes. Toda modificación se documenta dentro de historia oficial de evolución del modelo.

### 22.7 Mantenimiento del Diagrama
Toda modificación incorporada al modelo se refleja prontamente en el diagrama. Sincronización entre diagrama, modelo lógico y diccionario se preserva permanentemente. **No se permiten versiones inconsistentes entre estos artefactos.**

### 22.8 Naturaleza del Diagrama
Constituye artefacto de soporte gráfico para comprensión de arquitectura del sistema. La fuente oficial para definición del modelo de datos está compuesta por: **Modelo Lógico de Datos** y **Diccionario Oficial de Datos**. En caso de discrepancia entre el diagrama y estos artefactos, **la información documentada en el Modelo Lógico de Datos y el Diccionario Oficial de Datos prevalece siempre**. El diagrama se considera representación visual derivada de estos documentos y debe permanecer permanentemente actualizado respecto a ellos.
