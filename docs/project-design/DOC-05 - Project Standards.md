# Estándares del Proyecto (DOC-05)

## 1. Propósito

Define el conjunto único oficial de convenciones, criterios y reglas que gobiernan diseño, desarrollo, documentación, implementación, mantenimiento y evolución de la automatización. Garantiza uniformidad, consistencia, trazabilidad y compatibilidad entre todos los componentes, independientemente de la tecnología usada.

**Alcance obligatorio:** Todos los módulos, procesos, componentes, documentos, configuraciones, estructuras de datos, recursos y desarrollos del proyecto, así como cualquier extensión futura.

**Referencia oficial para:** Nombres, identificadores, formatos, estructuras, documentación, versionado, organización del proyecto, registros operativos, modelos de datos, prompts y cualquier otro elemento que requiera estandarización común.

---

## 2. Principios Transversales

Los siguientes principios aplican a **todas** las categorías de convenciones de este documento. Se listan una sola vez en lugar de repetirse en cada sección.

| Principio | Definición |
|-----------|------------|
| **Uniformidad** | Mismas convenciones, estructuras y criterios en todo el proyecto. Sin alternativas que generen comportamientos inconsistentes. |
| **Consistencia** | Coherencia entre documentos, módulos, procesos, configuraciones y recursos. Toda modificación preserva la consistencia. |
| **Unicidad** | Cada convención, identificador, formato o regla se define una sola vez. Sin duplicaciones ni contradicciones. |
| **Claridad** | Precisión, explicitud y ausencia de ambigüedad. Interpretación única por cualquier participante. |
| **Reusabilidad** | Convenciones diseñadas para reutilización por cualquier componente. Se evita crear reglas específicas cuando existe una general aplicable. |
| **Escalabilidad** | Incorporación de nuevos módulos, documentos, procesos o tecnologías sin modificaciones estructurales significativas. |
| **Independencia tecnológica** | No dependencia de lenguaje de programación, proveedor, herramienta, base de datos o servicio específico. |
| **Compatibilidad documental** | Alineación con Glosario, Requisitos Funcionales, Requisitos No Funcionales, Modelo de Decisiones, Flujo de Datos y demás documentos oficiales. Ninguna convención los contradice. |
| **Evolución controlada** | Toda modificación se documenta, justifica y preserva compatibilidad con elementos existentes cuando es posible. |
| **Trazabilidad** | Toda convención relevante es identificable, referenciable y mantenible durante la vida del proyecto. Se preserva historial de cambios. |
| **Mantenibilidad** | Facilitar mantenimiento, comprensión y evolución, reduciendo complejidad y promoviendo organización uniforme. |
| **Aplicación obligatoria** | Todo nuevo componente cumple estos estándares antes de considerarse compatible con la arquitectura oficial. |
| **Extensibilidad** | Nuevas convenciones se integran respetando la estructura existente, sin alterar el significado de estándares previos. |
| **Auditabilidad** | Cumplimiento verificable mediante revisiones documentales, inspecciones técnicas o pruebas en cualquier etapa. |
| **Fuente única de referencia** | Este documento es la referencia oficial. Ante conflicto, prevalecen estas reglas salvo excepción explícitamente documentada y aprobada. |

---

## 3. Convenciones Generales (CEG-001 a CEG-015)

Reglas base que todos los elementos del proyecto respetan, independientemente de su naturaleza o componente.

| Código | Convención | Definición |
|--------|------------|------------|
| **CEG-001** | Aplicación uniforme | Aplicación uniforme en toda la automatización. Sin excepciones salvo regla documentada y aprobada expresamente. |
| **CEG-002** | Cumplimiento obligatorio | Todo nuevo documento, módulo, componente, configuración, estructura de datos, recurso o desarrollo cumple los estándares antes de incorporarse oficialmente. |
| **CEG-003** | Consistencia terminológica | Todos los términos corresponden al significado definido en el Glosario del Proyecto. Sin sinónimos, abreviaturas o denominaciones alternativas cuando existe término oficial aprobado. |
| **CEG-004** | Unicidad de definiciones | Cada concepto, convención, estructura o regla se define una vez. Referencias subsiguientes reutilizan la definición oficial existente. |
| **CEG-005** | Identificación única | Todo elemento que requiera identificación posee un identificador único, estable e inequívoco según las reglas de este documento. |
| **CEG-006** | Independencia tecnológica | Convenciones independientes de lenguaje de programación, herramienta, proveedor, base de datos o plataforma tecnológica. Su significado no depende de la implementación técnica. |
| **CEG-007** | Compatibilidad de componentes | Garantiza interoperabilidad entre todos los módulos. Ningún componente define reglas incompatibles con los estándares oficiales. |
| **CEG-008** | Legibilidad | Toda documentación, estructura, configuración o recurso prioriza claridad y facilidad de comprensión para cualquier participante del proyecto. |
| **CEG-009** | Extensibilidad | Incorporación de nuevos documentos, módulos, procesos, entidades o recursos sin modificar reglas previamente establecidas. |
| **CEG-010** | Reusabilidad | Se favorece reutilización de estructuras, convenciones y componentes existentes antes de crear nuevas definiciones. |
| **CEG-011** | Trazabilidad | Toda convención relevante es relacionable con documentos, procesos o componentes que la usan, facilitando auditorías y modificaciones futuras. |
| **CEG-012** | Compatibilidad documental | Alineación con toda documentación oficial vigente. Cuando una modificación afecta múltiples documentos, se actualizan todas las referencias correspondientes. |
| **CEG-013** | Evolución controlada | Incorporación, modificación o eliminación de una convención se documenta, justifica y aprueba antes de entrar en vigor. |
| **CEG-014** | Prioridad de estándares | Ante conflicto entre convenciones, prevalecen las reglas de este documento salvo excepción explícitamente documentada y aprobada. |
| **CEG-015** | Revisión continua | Las convenciones pueden evolucionar con el crecimiento del proyecto, siempre que las modificaciones preserven coherencia, compatibilidad y mantenibilidad. |

---

## 4. Convenciones de Nombres (CNP-001 a CNP-015)

Reglas oficiales para asignar nombres a todos los elementos del proyecto: documentación, componentes funcionales, estructuras de datos, módulos, configuraciones, recursos, procesos y demás elementos definidos.

| Código | Convención | Definición |
|--------|------------|------------|
| **CNP-001** | Nombres descriptivos | Todo elemento usa un nombre que describe claramente su propósito o función. Sin nombres genéricos, ambiguos o que requieran contexto adicional. |
| **CNP-002** | Unicidad de nombres | Cada elemento posee un nombre único dentro de su ámbito de aplicación. No coexisten dos elementos con el mismo nombre si puede generar confusión. |
| **CNP-003** | Consistencia terminológica | Los nombres usan exclusivamente la terminología oficial del Glosario del Proyecto. Sin sinónimos cuando existe término aprobado. |
| **CNP-004** | Estabilidad de nombres | Una vez aprobado oficialmente, el nombre no se modifica salvo justificación documentada y actualización de todas las referencias correspondientes. |
| **CNP-005** | Uso de un solo idioma | Todos los nombres definidos por el proyecto usan un solo idioma consistentemente. No se mezclan idiomas dentro del nombre del mismo elemento. |
| **CNP-006** | Prohibición de abreviaturas no documentadas | Sin abreviaturas, acrónimos o siglas que no estén previamente definidos en el Glosario del Proyecto o documentación oficial. |
| **CNP-007** | Convención uniforme por categoría | Todos los elementos de la misma categoría siguen el mismo criterio de nombramiento. Aplica a: documentos, módulos, componentes, procesos, entidades, recursos, configuraciones y archivos. |
| **CNP-008** | Evitar información redundante | Los nombres contienen solo la información necesaria para identificar el elemento. No se repiten datos ya definidos por el contexto donde se usa el nombre. |
| **CNP-009** | Compatibilidad documental | La nomenclatura es consistente en toda la documentación oficial. Cualquier modificación actualiza las referencias correspondientes. |
| **CNP-010** | Escalabilidad | La convención permite incorporar nuevos elementos sin alterar la estructura de nombramiento existente. |
| **CNP-011** | Legibilidad | Los nombres facilitan lectura y comprensión para el usuario y procesos de mantenimiento futuros. Se evitan construcciones excesivamente largas o difíciles de interpretar. |
| **CNP-012** | Independencia tecnológica | Las reglas de nombramiento no dependen de lenguaje de programación, herramienta, base de datos o plataforma específica. |
| **CNP-013** | Reusabilidad | Cuando un elemento representa el mismo concepto en diferentes documentos o módulos, retiene el mismo nombre oficial. |
| **CNP-014** | Trazabilidad | Toda referencia a un elemento usa exactamente el nombre oficial definido, facilitando trazabilidad entre documentos, arquitectura, implementación y pruebas. |
| **CNP-015** | Evolución controlada | Cualquier modificación a las convenciones de nombres se documenta previamente y preserva compatibilidad con elementos existentes cuando es posible. |

**Propuesta de mejora:** En el siguiente capítulo (Convenciones para Identificadores) se pueden concretar estas reglas indicando exactamente cómo se nombrará cada tipo de elemento: documentos, diagramas, módulos, flujos, estados, prompts, carpetas, archivos, variables, funciones, clases (si las hay en el futuro), bases de datos, colecciones o tablas, campos JSON y logs. Esto dejaría una sola convención oficial para absolutamente todo el proyecto y evitaría tener que tomar decisiones de nombramiento durante el desarrollo, añadiendo valor significativo a la mantenibilidad.

---

## 5. Convenciones para Identificadores (CID-001 a CID-015)

Reglas para creación, asignación, uso y mantenimiento de todos los identificadores del proyecto. Aplican a documentos, componentes, entidades, procesos, registros, configuraciones, estructuras de datos y cualquier elemento que requiera identificación formal.

| Código | Convención | Definición |
|--------|------------|------------|
| **CID-001** | Identificador único | Todo elemento que requiera identificación posee un identificador único dentro de su ámbito. No existen identificadores duplicados representando elementos diferentes. |
| **CID-002** | Identificador inmutable | Una vez asignado oficialmente, el identificador no se modifica durante la vida útil del elemento. Cuando un elemento evoluciona, retiene su identificador original salvo que sea un elemento nuevo. |
| **CID-003** | Identificador independiente del nombre | El identificador oficial es independiente del nombre descriptivo. Modificar el nombre no implica modificar el identificador. |
| **CID-004** | Prefijos estandarizados | Cada categoría del proyecto usa un prefijo exclusivo que permite identificar rápidamente el tipo de elemento. Los prefijos oficiales se definen en este documento y no se reutilizan para categorías diferentes. |
| **CID-005** | Numeración secuencial | Los identificadores usan numeración secuencial dentro de cada categoría. La incorporación de nuevos elementos no altera la numeración previamente asignada. |
| **CID-006** | Prohibición de reutilización | Identificadores retirados, reemplazados o descontinuados no se reutilizan para representar nuevos elementos. Su preservación permite mantener la trazabilidad histórica del proyecto. |
| **CID-007** | Consistencia documental | El mismo identificador siempre representa el mismo elemento en toda la documentación oficial. No existen referencias incompatibles. |
| **CID-008** | Compatibilidad entre documentos | Los identificadores son utilizables como referencias cruzadas entre los diferentes documentos del proyecto sin generar ambigüedad. |
| **CID-009** | Trazabilidad | Todo identificador permite localizar fácilmente el elemento correspondiente dentro de documentación, arquitectura, desarrollo y pruebas. |
| **CID-010** | Escalabilidad | La estructura de identificadores permite incorporar nuevas categorías y nuevos elementos sin afectar identificadores existentes. |
| **CID-011** | Independencia tecnológica | Los identificadores no dependen del lenguaje de programación, herramienta, proveedor, base de datos o tecnología usada para implementar la automatización. |
| **CID-012** | Legibilidad | Los identificadores mantienen un formato uniforme que facilita su lectura y reconocimiento por cualquier participante del proyecto. |
| **CID-013** | Compatibilidad de versionado | La evolución de un elemento no implica la creación de un nuevo identificador cuando continúa representando el mismo concepto. Diferentes versiones retienen el mismo identificador oficial. |
| **CID-014** | Registro histórico | Toda incorporación, modificación o eliminación de identificadores se preserva como parte del historial documental del proyecto cuando aplique. |
| **CID-015** | Fuente oficial de identificadores | Este documento constituye la referencia oficial para la definición y administración de todos los identificadores usados por la automatización. Ningún documento posterior puede definir identificadores incompatibles con las reglas aquí establecidas. |

---

## 6. Convenciones para Estados (CED-001 a CED-015)

Reglas para definición, identificación, representación y evolución de todos los estados usados por la automatización. Aplican a estados funcionales, de proceso, de entidad, de componente y cualquier otro estado que requiera identificación formal.

| Código | Convención | Definición |
|--------|------------|------------|
| **CED-001** | Identificador único | Todo estado posee un identificador único que lo distingue de cualquier otro estado dentro de la misma categoría. |
| **CED-002** | Nombre descriptivo | Cada estado usa un nombre que describe claramente la situación o condición que representa. |
| **CED-003** | Estado inmutable | Una vez definido, el identificador de un estado no se modifica durante el ciclo de vida del proceso o entidad. |
| **CED-004** | Transiciones explícitas | Las transiciones de estado se definen y documentan explícitamente. No ocurren cambios de estado implícitos o no documentados. |
| **CED-005** | Consistencia documental | El mismo estado siempre se representa con el mismo identificador en toda la documentación oficial. |
| **CED-006** | Consistencia terminológica | Los nombres de estados usan exclusivamente la terminología oficial definida en el Glosario del Proyecto. |
| **CED-007** | Representación independiente | Los identificadores de estado son independientes del nombre descriptivo, permitiendo modificar el nombre sin alterar el identificador. |
| **CED-008** | Trazabilidad | Todo estado es relacionable con el proceso, entidad o componente que lo usa, así como con las posibles transiciones que origina. |
| **CED-009** | Compatibilidad entre componentes | Estados usados por múltiples componentes mantienen representación consistente en toda la automatización. |
| **CED-010** | Escalabilidad | La definición de estados permite incorporar nuevos estados sin afectar la estructura existente. |
| **CED-011** | Independencia tecnológica | La definición conceptual de estados no depende de ningún lenguaje de programación, herramienta o plataforma específica. |
| **CED-012** | Reusabilidad | Cuando diferentes procesos comparten el mismo estado, reutilizan la misma definición oficial. |
| **CED-013** | Evolución controlada | Cualquier modificación a un estado o sus transiciones se documenta previamente y preserva compatibilidad con procesos existentes cuando es posible. |
| **CED-014** | Auditabilidad | El historial de estados permite reconstruir la secuencia de transiciones ocurridas durante la ejecución de un proceso. |
| **CED-015** | Fuente oficial de estados | Este documento constituye la referencia oficial para la definición y administración de todos los estados usados por la automatización. |

---

## 7. Convenciones para Fechas y Horas (CFH-001 a CFH-015)

Reglas para representación, almacenamiento, intercambio, documentación y uso de fechas y horas. Aplican a toda fecha, hora, timestamp, período, duración, calendario, registro operativo y cualquier otro dato temporal usado por la automatización.

| Código | Convención | Definición |
|--------|------------|------------|
| **CFH-001** | Formato oficial de fecha | Toda fecha usa un único formato oficial definido para el proyecto. No coexisten múltiples formatos para representar la misma información. |
| **CFH-002** | Formato oficial de hora | Toda hora usa un único formato oficial definido para el proyecto. La representación de hora permanece uniforme en todos los componentes del sistema. |
| **CFH-003** | Representación uniforme | Toda información temporal se representa usando las mismas convenciones en documentación, configuraciones, estructuras de datos, registros operativos y procesos internos. |
| **CFH-004** | Precisión temporal | Cada registro temporal almacena solo el nivel de precisión requerido por el proceso correspondiente. No se incorporan niveles de precisión innecesarios. |
| **CFH-005** | Preservación de datos originales | Cuando una fecha u hora proviene de una fuente externa, la automatización preserva el valor original cuando sea necesario para auditoría, trazabilidad o reprocesamiento. Las conversiones se realizan sobre estructuras derivadas. |
| **CFH-006** | Consistencia cronológica | Las fechas y horas usadas durante el procesamiento mantienen coherencia con la secuencia real de eventos. No se registran eventos con relaciones temporales incompatibles. |
| **CFH-007** | Zona horaria controlada | Toda información temporal se interpreta usando una política uniforme de manejo de zona horaria definida por el proyecto. Las conversiones se realizan consistentemente en todos los componentes. |
| **CFH-008** | Compatibilidad documental | Las convenciones temporales permanecen consistentes en toda la documentación oficial. No se usan diferentes formatos para representar la misma información. |
| **CFH-009** | Independencia tecnológica | La representación conceptual de fechas y horas no depende del lenguaje de programación, base de datos, sistema operativo o herramienta usada para implementar la automatización. |
| **CFH-010** | Trazabilidad temporal | Toda operación relevante registra la información temporal necesaria para permitir reconstruir el historial completo de procesamiento. |
| **CFH-011** | Reusabilidad | Los mismos criterios de representación de fechas y horas se reutilizan en todos los módulos del proyecto. No se definen convenciones particulares para componentes individuales. |
| **CFH-012** | Evolución controlada | Cualquier modificación a las convenciones temporales se documenta previamente y preserva compatibilidad con la información histórica del proyecto. |
| **CFH-013** | Compatibilidad con auditoría | La representación de fechas y horas facilita la reconstrucción cronológica de eventos durante auditorías, diagnósticos y reprocesamientos. |
| **CFH-014** | Consistencia entre registros | Cuando el mismo evento es registrado por diferentes componentes, la información temporal permanece consistente entre todos ellos. |
| **CFH-015** | Fuente oficial de convenciones temporales | Este documento constituye la referencia oficial para todas las reglas relacionadas con representación y uso de fechas y horas dentro del proyecto. |

---

## 8. Convenciones para Formatos de Datos (CFDT-001 a CFDT-015)

Reglas para representación, intercambio, almacenamiento y manejo de formatos de datos. Aplican a toda información intercambiada entre procesos, módulos, componentes, documentos, configuraciones, archivos, registros y cualquier elemento que almacene o transmita datos.

| Código | Convención | Definición |
|--------|------------|------------|
| **CFDT-001** | Formato uniforme | Todo dato se representa usando un formato oficial previamente definido para el tipo de información correspondiente. No coexisten múltiples formatos para representar el mismo dato. |
| **CFDT-002** | Consistencia estructural | Las estructuras de datos mantienen organización uniforme en todos los componentes que las usan. La misma información siempre se representa de la misma manera. |
| **CFDT-003** | Compatibilidad de módulos | Los formatos de datos garantizan interoperabilidad entre todos los módulos de la automatización. No se definen estructuras incompatibles para intercambio de información. |
| **CFDT-004** | Claridad de representación | Los formatos facilitan la interpretación de información tanto por procesos automáticos como por tareas de mantenimiento futuro. Se evitan estructuras ambiguas o innecesariamente complejas. |
| **CFDT-005** | Preservación de información | La transformación de datos entre diferentes formatos no causa pérdida de información relevante. Toda conversión preserva la integridad del contenido original. |
| **CFDT-006** | Independencia tecnológica | Los formatos conceptuales definidos por el proyecto permanecen independientes del lenguaje de programación, base de datos, herramienta o plataforma usada para implementar la automatización. |
| **CFDT-007** | Extensibilidad | Los formatos de datos permiten incorporar nuevos campos o estructuras sin afectar compatibilidad con información previamente existente. |
| **CFDT-008** | Compatibilidad documental | Los formatos definidos permanecen consistentes con toda la documentación oficial del proyecto. Cualquier modificación actualiza las referencias correspondientes. |
| **CFDT-009** | Validación uniforme | Toda estructura de datos es validable usando criterios homogéneos antes de ser usada por otros procesos de la automatización. |
| **CFDT-010** | Reusabilidad | Cuando sea posible, el mismo formato se reutiliza para representar información equivalente en diferentes módulos del proyecto. No se crean estructuras distintas para datos con el mismo significado. |
| **CFDT-011** | Trazabilidad | Los formatos permiten mantener la relación entre la información original y cualquier estructura derivada generada durante el procesamiento. |
| **CFDT-012** | Evolución controlada | Cualquier modificación a un formato de datos se documenta previamente y preserva compatibilidad con versiones anteriores cuando sea técnicamente posible. |
| **CFDT-013** | Compatibilidad con flujo de datos | Los formatos definidos son compatibles con las reglas establecidas en el Flujo de Datos y con las estructuras usadas por el Modelo de Decisiones y los Requisitos Funcionales. |
| **CFDT-014** | Uniformidad entre documentos | Diferentes documentos del proyecto se refieren al mismo formato usando exactamente la misma definición y terminología. |
| **CFDT-015** | Fuente oficial de formatos | Este documento constituye la referencia oficial para convenciones relacionadas con formatos de datos usados por la automatización. |

---

## 9. Convenciones para Estructuras JSON (CJS-001 a CJS-015)

Reglas para diseño, organización, representación, intercambio y evolución de todas las estructuras JSON usadas por la automatización. Aplican a cualquier estructura JSON usada para almacenamiento, intercambio de información, configuración, comunicación entre componentes o cualquier otro proceso que requiera dicho formato.

| Código | Convención | Definición |
|--------|------------|------------|
| **CJS-001** | Estructura uniforme | Todas las estructuras JSON mantienen organización consistente en todo el proyecto. Elementos equivalentes se representan usando la misma estructura. |
| **CJS-002** | Nombres consistentes | Las claves usadas dentro de estructuras JSON mantienen nomenclatura uniforme según las convenciones oficiales del proyecto. El mismo concepto siempre usa el mismo nombre de propiedad. |
| **CJS-003** | Identificación única | Toda entidad representada mediante JSON que requiera identificación incluye el identificador oficial correspondiente cuando aplique. |
| **CJS-004** | Tipado consistente | Cada propiedad mantiene siempre el mismo tipo de dato para representar el mismo concepto. No se usan diferentes tipos para la misma propiedad en diferentes estructuras. |
| **CJS-005** | Separación de datos y metadatos | Información funcional y metadatos se mantienen claramente diferenciados dentro de las estructuras JSON. Esta separación facilita mantenimiento, trazabilidad y evolución del sistema. |
| **CJS-006** | Compatibilidad evolutiva | Modificaciones a estructuras JSON preservan compatibilidad con versiones anteriores cuando sea técnicamente posible. |
| **CJS-007** | Extensibilidad | Las estructuras permiten incorporar nuevos campos sin alterar el significado o comportamiento de propiedades existentes. |
| **CJS-008** | Reusabilidad | Cuando diferentes procesos requieren representar la misma información, reutilizan la misma estructura JSON oficial. No se definen estructuras equivalentes para representar el mismo concepto. |
| **CJS-009** | Validación estructural | Toda estructura JSON es validable antes de ser usada por otros componentes de la automatización. Estructuras inválidas no continúan el flujo de procesamiento. |
| **CJS-010** | Preservación de información | Transformaciones realizadas sobre estructuras JSON no causan pérdida de información relevante. Cuando es necesario generar estructuras derivadas, se mantiene la relación con la información original. |
| **CJS-011** | Compatibilidad documental | Las estructuras JSON permanecen alineadas con el Modelo de Datos, el Flujo de Datos, el Modelo de Decisiones y el resto de la documentación oficial del proyecto. |
| **CJS-012** | Independencia tecnológica | Las convenciones definidas para JSON permanecen independientes de cualquier lenguaje de programación o herramienta específica usada durante la implementación. |
| **CJS-013** | Trazabilidad | Las estructuras JSON permiten identificar el origen, versión y contexto de la información cuando sea necesario para garantizar trazabilidad del sistema. |
| **CJS-014** | Evolución controlada | Cualquier modificación a una estructura JSON se documenta previamente y se mantiene sincronizada con el resto de la documentación oficial. |
| **CJS-015** | Fuente oficial de estructuras JSON | Este documento constituye la referencia oficial para todas las convenciones relacionadas con estructuras JSON usadas por la automatización. |

---

## 10. Convenciones para Documentación (CDO-001 a CDO-015)

Reglas para creación, organización, mantenimiento y evolución de toda la documentación del proyecto. Aplican a documentos estratégicos, documentación técnica, especificaciones funcionales, diagramas, manuales, procedimientos, anexos, registros y cualquier otro documento oficial.

| Código | Convención | Definición |
|--------|------------|------------|
| **CDO-001** | Documento único por propósito | Cada documento tiene un único objetivo claramente definido. No coexisten diferentes documentos regulando el mismo aspecto del proyecto. |
| **CDO-002** | Estructura uniforme | Todos los documentos oficiales mantienen estructura homogénea que facilita lectura, navegación y mantenimiento. Cuando sea posible, preservan el mismo estilo organizativo usado por el resto de la documentación oficial. |
| **CDO-003** | Identificación oficial | Todo documento posee un nombre oficial, un identificador único y una versión documentada según las convenciones establecidas por el proyecto. |
| **CDO-004** | Consistencia terminológica | Toda la documentación usa exclusivamente la terminología oficial definida en el Glosario del Proyecto. No se usan términos alternativos que generen ambigüedad. |
| **CDO-005** | Referencias cruzadas | Cuando un documento depende de definiciones contenidas en otro documento oficial, hace la referencia correspondiente en lugar de duplicar su contenido. |
| **CDO-006** | Sin duplicación | La misma regla, definición o convención se documenta una vez dentro del proyecto. Otros documentos referencian la fuente oficial correspondiente. |
| **CDO-007** | Coherencia documental | Cualquier modificación realizada a un documento que afecte otros documentos del proyecto se refleja mediante las actualizaciones necesarias para mantener consistencia documental. |
| **CDO-008** | Evolución controlada | Toda modificación relevante se documenta y asocia con la versión correspondiente del documento. Las modificaciones preservan coherencia con el resto de la documentación oficial. |
| **CDO-009** | Claridad | La documentación se redacta usando lenguaje preciso, objetivo e inequívoco. Las reglas se formulan de manera que admitan una sola interpretación. |
| **CDO-010** | Independencia tecnológica | La documentación conceptual del proyecto no depende de una tecnología, herramienta o lenguaje de programación específico, salvo que el propósito del documento lo requiera. |
| **CDO-011** | Trazabilidad | Toda regla, decisión o convención documentada es relacionable con los procesos, componentes o documentos que la usan. |
| **CDO-012** | Compatibilidad documental | Toda nueva documentación permanece alineada con los Requisitos Funcionales, Requisitos No Funcionales, Modelo de Decisiones, Flujo de Datos y otros documentos oficiales vigentes. |
| **CDO-013** | Reusabilidad | Cuando sea posible, la información común se reutiliza mediante referencias a la documentación oficial correspondiente, evitando replicación de contenido. |
| **CDO-014** | Auditabilidad | La documentación permite identificar claramente el origen, propósito, alcance y vigencia de cada definición usada durante el desarrollo del proyecto. |
| **CDO-015** | Fuente oficial | La documentación aprobada del proyecto constituye la única fuente de referencia oficial para el diseño, desarrollo, pruebas, mantenimiento y evolución de la automatización. No se usan documentos externos o versiones no aprobadas como referencia normativa. |

---

## 11. Convenciones para Prompts (CPR-001 a CPR-015)

Reglas para diseño, organización, documentación, mantenimiento y evolución de todos los prompts usados por la automatización. Aplican a todos los prompts, incluyendo aquellos para análisis de ofertas, evaluación inicial, diagnósticos, generación de estrategia, preparación de documentos, validaciones, verificaciones, clasificación de información y cualquier otro proceso asistido por modelos de lenguaje.

| Código | Convención | Definición |
|--------|------------|------------|
| **CPR-001** | Propósito único | Cada prompt cumple un único objetivo claramente definido. No existen prompts que mezclen diferentes responsabilidades funcionales cuando estas pueden separarse razonablemente. |
| **CPR-002** | Identificación oficial | Todo prompt posee un identificador único y una designación oficial según las convenciones del proyecto. |
| **CPR-003** | Estructura uniforme | Todos los prompts mantienen estructura homogénea que facilita su comprensión, mantenimiento y reutilización. La organización interna sigue los estándares oficiales definidos por el proyecto. |
| **CPR-004** | Responsabilidad claramente definida | Cada prompt especifica inequívocamente la tarea que el modelo de lenguaje debe ejecutar. No se incluyen instrucciones contradictorias o ambiguas. |
| **CPR-005** | Independencia del modelo | Los prompts se diseñan buscando minimizar dependencia de un modelo de lenguaje específico. Su contenido facilita futuras migraciones a otros proveedores o versiones de modelo. |
| **CPR-006** | Reusabilidad | Cuando sea posible, el mismo prompt se reutiliza para tareas equivalentes en lugar de crear versiones duplicadas con diferencias mínimas. |
| **CPR-007** | Modularidad | Prompts complejos se dividen en componentes o etapas independientes cuando esto facilita su mantenimiento, validación y evolución. |
| **CPR-008** | Consistencia terminológica | Todos los prompts usan exclusivamente la terminología oficial definida por el Glosario del Proyecto y documentación vigente. |
| **CPR-009** | Compatibilidad documental | Todo prompt permanece alineado con los Requisitos Funcionales, el Modelo de Decisiones, el Flujo de Datos y el resto de la documentación oficial del proyecto. |
| **CPR-010** | Versionado | Toda modificación relevante a un prompt se registra mediante el mecanismo oficial de versionado definido por el proyecto. Versiones anteriores se preservan cuando sea necesario para garantizar trazabilidad. |
| **CPR-011** | Trazabilidad | Todo prompt es relacionable con el proceso funcional, módulo o componente que lo usa. Asimismo, es posible identificar la versión usada durante una ejecución dada. |
| **CPR-012** | Evolución controlada | Modificaciones realizadas a prompts se documentan y evalúan previamente antes de incorporarse a la versión oficial del proyecto. |
| **CPR-013** | Auditabilidad | La automatización permite identificar qué prompt participó en cada proceso relevante cuando sea necesario para auditorías, diagnósticos o reprocesamiento. |
| **CPR-014** | Compatibilidad futura | Los prompts se diseñan de manera que permitan incorporar nuevas capacidades, nuevas variables o nuevos criterios sin requerir un rediseño completo. |
| **CPR-015** | Fuente oficial de prompts | Este documento constituye la referencia oficial para todas las convenciones relacionadas con el diseño y administración de prompts usados por la automatización. |

---

## 12. Convenciones para Nombres de Archivos y Documentos (CNA-001 a CNA-015)

Reglas para creación, asignación y administración de nombres usados por todos los archivos y documentos del proyecto. Aplican a documentos oficiales, archivos de configuración, recursos de automatización, plantillas, diagramas, registros, reportes, documentos generados automáticamente y cualquier otro archivo usado por el proyecto.

| Código | Convención | Definición |
|--------|------------|------------|
| **CNA-001** | Nombre descriptivo | Todo archivo o documento usa un nombre que describe claramente su contenido o propósito. No se usan nombres genéricos que dificulten la identificación. |
| **CNA-002** | Unicidad | Dentro del mismo contexto, no existen diferentes archivos o documentos con el mismo nombre. La nomenclatura permite identificar inequívocamente cada recurso. |
| **CNA-003** | Consistencia | Los nombres siguen una convención uniforme en toda la automatización. Archivos pertenecientes a la misma categoría mantienen el mismo criterio de nombramiento. |
| **CNA-004** | Correspondencia con contenido | El nombre de un archivo representa el contenido principal que almacena. Cuando el contenido cambia sustancialmente, se evalúa si corresponde crear un nuevo recurso o actualizar el existente según reglas de versionado. |
| **CNA-005** | Independencia tecnológica | La convención de nombramiento no depende del sistema operativo, lenguaje de programación, editor o herramienta usada durante el desarrollo. |
| **CNA-006** | Compatibilidad documental | Los nombres usados permanecen consistentes con los definidos en la documentación oficial del proyecto. No se usan diferentes denominaciones para el mismo recurso. |
| **CNA-007** | Organización por categorías | Los archivos se nombran de manera que faciliten su clasificación dentro de la estructura oficial de carpetas del proyecto. |
| **CNA-008** | Evolución controlada | Modificaciones relevantes a nombres de archivos o documentos preservan trazabilidad y respetan las reglas oficiales de versionado. |
| **CNA-009** | Trazabilidad | Todo archivo es relacionable con el módulo, proceso, documento o componente al que pertenece. Cuando sea necesario, esta relación se mantiene mediante identificadores oficiales. |
| **CNA-010** | Reusabilidad | Cuando un recurso representa el mismo contenido oficial, se reutiliza el archivo correspondiente en lugar de generar duplicados innecesarios. |
| **CNA-011** | Compatibilidad con automatización | Los nombres facilitan su uso por procesos automáticos, evitando ambigüedades y manteniendo estructura estable. |
| **CNA-012** | Escalabilidad | La convención de nombramiento permite incorporar nuevos archivos y documentos sin alterar la organización existente. |
| **CNA-013** | Claridad | Los nombres facilitan identificación inmediata del recurso por cualquier persona participante en el proyecto. |
| **CNA-014** | Fuente oficial | Los documentos oficiales retienen el nombre aprobado por el proyecto y se usan como referencia única para su contenido correspondiente. |
| **CNA-015** | Administración centralizada | Cualquier nueva convención relacionada con nombres de archivos y documentos permanece alineada con este documento y con el resto de la documentación oficial del proyecto. |

---

## 13. Convenciones para Organización de Carpetas (COC-001 a COC-015)

Reglas para organización, estructura y administración de carpetas usadas por la automatización. Aplican a todas las carpetas del proyecto, incluyendo documentación, código fuente, configuraciones, bases de datos, recursos, registros operativos, plantillas, prompts, pruebas y cualquier otro componente que requiera organización mediante directorios.

| Código | Convención | Definición |
|--------|------------|------------|
| **COC-001** | Organización jerárquica | La estructura de carpetas se organiza usando una jerarquía lógica que refleja la arquitectura funcional del proyecto. No se crean estructuras arbitrarias o inconsistentes. |
| **COC-002** | Responsabilidad única | Cada carpeta agrupa solo recursos pertenecientes a la misma categoría funcional. No se mezclan recursos de diferente naturaleza cuando existe separación lógica. |
| **COC-003** | Nombres consistentes | Los nombres de carpetas siguen las convenciones oficiales de nombramiento establecidas por el proyecto. La misma categoría de recurso siempre usa el mismo criterio de nombramiento. |
| **COC-004** | Estructura estable | La organización general de carpetas permanece estable durante la evolución del proyecto. Modificaciones estructurales se justifican y documentan previamente. |
| **COC-005** | Evitar duplicación | El mismo recurso no se almacena simultáneamente en diferentes ubicaciones cuando existe una única ubicación oficial para ese tipo de información. |
| **COC-006** | Escalabilidad | La estructura de carpetas permite incorporar nuevos módulos, componentes y recursos sin requerir reorganizaciones mayores. |
| **COC-007** | Independencia tecnológica | La organización conceptual de carpetas no depende de un lenguaje de programación, framework, sistema operativo o herramienta específica. |
| **COC-008** | Compatibilidad documental | La estructura oficial de carpetas permanece alineada con la arquitectura, documentación y componentes definidos para el proyecto. |
| **COC-009** | Separación de responsabilidades | Las carpetas facilitan la separación entre documentación, implementación, configuraciones, datos, recursos temporales, registros y otros elementos del proyecto. |
| **COC-010** | Trazabilidad | La organización de carpetas facilita identificar el módulo, proceso o componente al que pertenece cada recurso almacenado. |
| **COC-011** | Reusabilidad | Cuando múltiples componentes usan recursos comunes, estos se almacenan en una ubicación compartida oficialmente definida, evitando duplicaciones innecesarias. |
| **COC-012** | Compatibilidad con automatización | La estructura de carpetas facilita el acceso automatizado a recursos usados durante la ejecución de la automatización. No se usan organizaciones que dificulten el procesamiento automático. |
| **COC-013** | Evolución controlada | Cualquier modificación a la estructura oficial de carpetas se documenta y mantiene compatible con el resto de la arquitectura del proyecto. |
| **COC-014** | Claridad organizativa | La estructura permite a cualquier participante del proyecto localizar un recurso fácilmente, sin requerir conocimiento previo de la implementación. |
| **COC-015** | Fuente oficial | Este documento constituye la referencia oficial para todas las convenciones relacionadas con la organización de carpetas usadas por la automatización. |

---

## 14. Convenciones para Versionado (CVE-001 a CVE-015)

Reglas para creación, identificación, administración y evolución de versiones usadas dentro del proyecto. Aplican a todos los documentos oficiales, componentes funcionales, configuraciones, estructuras de datos, prompts, recursos generados, módulos y cualquier otro elemento cuyo contenido pueda evolucionar durante el ciclo de vida del proyecto.

| Código | Convención | Definición |
|--------|------------|------------|
| **CVE-001** | Versionado obligatorio | Todo elemento cuya evolución pueda afectar la operación, mantenimiento o comprensión del proyecto tiene un mecanismo oficial de versionado. |
| **CVE-002** | Identificación única de versión | Cada versión posee un identificador único que permite distinguirla inequívocamente de otras versiones del mismo elemento. |
| **CVE-003** | Evolución secuencial | Las versiones evolucionan siguiendo un orden lógico y cronológico. No se generan versiones inconsistentes o retrocesos que dificulten la trazabilidad del proyecto. |
| **CVE-004** | Preservación de historial | Toda versión oficial preserva su historial de cambios cuando sea necesario para garantizar trazabilidad, auditoría o recuperación de información. |
| **CVE-005** | Compatibilidad documental | Modificaciones realizadas a un elemento permanecen sincronizadas con la documentación oficial correspondiente. Toda versión refleja correctamente el estado actual del proyecto. |
| **CVE-006** | Independencia tecnológica | Las reglas de versionado permanecen independientes del sistema de control de versiones, lenguaje de programación, plataforma o herramienta usada durante la implementación. |
| **CVE-007** | Trazabilidad | Toda versión es relacionable con los cambios que la originaron, los elementos afectados y la documentación correspondiente. |
| **CVE-008** | Consistencia | Todos los elementos pertenecientes a la misma categoría usan el mismo criterio de versionado. No coexisten múltiples esquemas de versionado para el mismo tipo de recurso. |
| **CVE-009** | Evolución controlada | Cada nueva versión se genera solo cuando existe una modificación justificada respecto a la versión anterior. No se crean versiones sin cambios significativos o debidamente documentados. |
| **CVE-010** | Reproducibilidad | El versionado permite identificar la configuración exacta usada durante una ejecución, facilitando la reproducción de resultados cuando sea necesario. |
| **CVE-011** | Compatibilidad de componentes | Versiones usadas por componentes relacionados permanecen compatibles según las reglas definidas por la arquitectura del proyecto. |
| **CVE-012** | Reusabilidad | Cuando un elemento permanece vigente sin modificaciones, retiene su versión oficial sin generar nuevas versiones innecesarias. |
| **CVE-013** | Auditoría | El historial de versiones facilita la realización de auditorías técnicas y funcionales, permitiendo identificar qué cambios se incorporaron en cada evolución del proyecto. |
| **CVE-014** | Fuente oficial | Toda versión oficial se registra según las convenciones establecidas en este documento. No se usan versiones paralelas, informales o no documentadas. |
| **CVE-015** | Administración centralizada | Las reglas de versionado se administran uniformemente para todos los elementos del proyecto, garantizando consistencia durante toda la vida de la automatización. |

---

## 15. Convenciones para Logs (CLR-001 a CLR-015)

Reglas para generación, organización, almacenamiento y administración de todos los logs operativos producidos por la automatización. Aplican a todos los logs generados por procesos automáticos, módulos funcionales, componentes internos, integraciones, validaciones, transformaciones, errores, advertencias y cualquier otro evento relevante para la operación del sistema.

| Código | Convención | Definición |
|--------|------------|------------|
| **CLR-001** | Logging obligatorio de eventos relevantes | Todo proceso cuya ejecución sea relevante para la operación, diagnóstico, auditoría o mantenimiento de la automatización genera los logs correspondientes. |
| **CLR-002** | Consistencia estructural | Todos los logs mantienen estructura uniforme que facilita su procesamiento, consulta y análisis. No coexisten formatos incompatibles para representar eventos equivalentes. |
| **CLR-003** | Integridad de información | Los logs reflejan fielmente los eventos ocurridos durante la ejecución del sistema. No se alteran, eliminan ni modifican de manera que comprometa la veracidad de la información registrada. |
| **CLR-004** | Identificación de eventos | Todo log permite identificar inequívocamente el evento, proceso o componente que lo originó. |
| **CLR-005** | Registro cronológico | Los eventos preservan su secuencia temporal, permitiendo reconstruir el orden real de ejecución de los procesos. |
| **CLR-006** | Nivel de detalle apropiado | Los logs contienen solo la información necesaria para cumplir su propósito, evitando tanto la omisión de datos relevantes como el almacenamiento innecesario de información. |
| **CLR-007** | Compatibilidad con trazabilidad | Los logs mantienen compatibilidad con las reglas de trazabilidad establecidas por el proyecto, permitiendo relacionar cada evento con los elementos involucrados. |
| **CLR-008** | Independencia tecnológica | Las convenciones de logs permanecen independientes de la tecnología, herramienta o mecanismo específico usado para generar o almacenar logs. |
| **CLR-009** | Reusabilidad | Todos los componentes del sistema usan la misma convención para generar logs operativos. No se implementan formatos particulares para módulos individuales salvo justificación documentada. |
| **CLR-010** | Preservación | Los logs se preservan por el período definido por las políticas oficiales del proyecto cuando sea necesario para auditoría, diagnóstico, reprocesamiento o mantenimiento. |
| **CLR-011** | Compatibilidad documental | Las convenciones usadas para logs permanecen alineadas con el Flujo de Datos, el Modelo de Decisiones, el Manejo de Errores y el resto de la documentación oficial. |
| **CLR-012** | Evolución controlada | Cualquier modificación a la estructura o contenido de logs se documenta previamente y preserva compatibilidad con procesos existentes cuando sea posible. |
| **CLR-013** | Auditabilidad | Los logs proporcionan evidencia suficiente para respaldar auditorías técnicas y funcionales sobre el comportamiento de la automatización. |
| **CLR-014** | Escalabilidad | La estructura de logs permite incorporar nuevos tipos de eventos sin afectar la compatibilidad de logs existentes. |
| **CLR-015** | Fuente oficial | Este documento constituye la referencia oficial para todas las convenciones relacionadas con la generación y administración de logs operativos dentro de la automatización. |

---

## 16. Convenciones para Auditoría y Trazabilidad (CAT-001 a CAT-015)

Reglas para garantizar la auditabilidad y trazabilidad de todos los procesos, datos, decisiones, transformaciones y operaciones realizadas por la automatización. Aplican a todos los módulos, procesos, componentes, logs, flujos de datos, decisiones automáticas, intervenciones del usuario y cualquier otra operación relevante realizada durante la operación de la automatización.

| Código | Convención | Definición |
|--------|------------|------------|
| **CAT-001** | Trazabilidad completa | Toda operación relevante ejecutada por la automatización es trazable desde su origen hasta su resultado final. No existen procesos cuya ejecución no pueda reconstruirse posteriormente. |
| **CAT-002** | Evidencia objetiva | Toda acción relevante genera evidencia suficiente para justificar su ejecución, resultado y contexto cuando sea necesario para auditorías o diagnósticos. |
| **CAT-003** | Identificación de elementos | Toda evidencia de auditoría permite identificar claramente los elementos involucrados, incluyendo procesos afectados, componentes, datos y recursos. |
| **CAT-004** | Registro cronológico | La información usada para auditoría preserva el orden temporal de eventos, permitiendo reconstruir el recorrido completo de cada proceso. |
| **CAT-005** | Integridad de evidencia | La información usada para garantizar auditoría y trazabilidad se preserva intacta durante todo el período de conservación definido por el proyecto. |
| **CAT-006** | Relación entre eventos | Los logs permiten establecer relaciones entre eventos consecutivos o relacionados pertenecientes al mismo flujo de procesamiento. |
| **CAT-007** | Compatibilidad documental | Las convenciones de auditoría permanecen alineadas con el Flujo de Datos, el Modelo de Decisiones, el Manejo de Errores, los Requisitos Funcionales y el resto de la documentación oficial. |
| **CAT-008** | Independencia tecnológica | Las reglas de auditoría y trazabilidad permanecen independientes de las herramientas, plataformas o tecnologías usadas durante la implementación. |
| **CAT-009** | Reproducibilidad | La información preservada permite reproducir el comportamiento del sistema cuando se dispone de las mismas entradas, reglas y configuraciones. |
| **CAT-010** | Consistencia | Los diferentes componentes de la automatización aplican criterios homogéneos para registrar la información necesaria para auditoría. No coexisten mecanismos incompatibles entre módulos. |
| **CAT-011** | Evolución controlada | Cualquier modificación a las convenciones de auditoría y trazabilidad se documenta previamente y preserva compatibilidad con el historial existente. |
| **CAT-012** | Disponibilidad | La información necesaria para auditoría permanece disponible para procesos autorizados durante todo el período de conservación establecido por el proyecto. |
| **CAT-013** | Escalabilidad | Las convenciones permiten incorporar nuevos procesos, componentes y tipos de evidencia sin afectar la consistencia del sistema de auditoría. |
| **CAT-014** | Reusabilidad | Los mecanismos de auditoría y trazabilidad reutilizan las estructuras oficiales definidas por el proyecto, evitando duplicaciones innecesarias. |
| **CAT-015** | Fuente oficial | Este documento constituye la referencia oficial para todas las convenciones relacionadas con auditoría y trazabilidad usadas por la automatización. |

---

## 16.1. Formatos de auditoría de eventos y sesiones para el Módulo 1 (Descubrimiento de Oportunidades)

Estas convenciones establecen los formatos oficiales para registrar eventos y sesiones de auditoría generados por el Módulo 1 de la automatización.

### Formato para eventos

Todo evento generado por el módulo de Descubrimiento registra, como mínimo, los siguientes elementos, alineados con la entidad Evento del modelo de datos oficial (DOC-13 / 13A):

| Atributo | Descripción |
|----------|-------------|
| `run_id` | Identificador de la corrida (Corrida) que generó el evento (RN-01). |
| `source_id` | Identificador de la fuente sobre la que ocurrió el evento (opcional). |
| `session_id` | Identificador de la sesión de plataforma en la que ocurrió el evento (opcional). |
| `set_indice` | Índice del conjunto de filtros en el que ocurrió el evento (opcional). |
| `timestamp` | Fecha y hora en que ocurrió el evento. |
| `tipo` | Clasificación del evento: `error` o `suceso`. |
| `codigo` | Código de negocio del evento (convención `ERR-nn` / `EVT-nn`, ver DOC-06, Sección 11). |
| `evidencia` | Evidencia del evento (capturas de pantalla, trazas o fragmentos sin procesar; nunca credenciales ni tokens de sesión). |

**Ejemplo de referencia** (cumple la plantilla oficial de eventos, Apéndice 5C, C.11):

```
Fecha y hora: 2026-08-07 10:23:45 (local)
Módulo: Descubrimiento (M1)
Proceso: Corrida 3f2a-11 (set_indice 0)
Evento: EVT-01 (oferta_no_capturada)
Nivel: suceso
Resultado: Éxito - lote procesado, una oferta no capturada
Observaciones: total_declarado=37, conteo=25, paginas_consumidas=1; evidencia adjunta (registro de la oferta)
```

### Formato de auditoría de sesión

La auditoría de cada sesión de plataforma registra, exclusivamente, los campos mínimos viables definidos por la decisión D3 y la entidad Sesión del modelo de datos oficial (DOC-13 / 13A):

`session_id`, `run_id`, `source_id`, `set_indice`, `timestamp`, `total_declarado`, `conteo`, `estado`.

Los registros de sesión se crean solo después de una entrada exitosa; los intentos fallidos se reportan como eventos, nunca como sesiones.

### Convención de códigos por nodo

Los códigos de negocio siguen la convención `ERR-nn` (errores) y `EVT-nn` (eventos) establecida en DOC-06 (Sección 11, Manejo de Errores por Módulo), preservando el catálogo completo definido para el módulo de Descubrimiento y su mapeo a las categorías oficiales de error.

---

## 17. Convenciones para Entidades y Modelos de Datos (CEM-001 a CEM-015)

Reglas para definición, organización, identificación y evolución de entidades y modelos de datos usados por la automatización. Aplican a todas las entidades conceptuales y estructuras de datos usadas por la automatización, independientemente de la tecnología empleada para su implementación.

| Código | Convención | Definición |
|--------|------------|------------|
| **CEM-001** | Definición única | Cada entidad representa un único concepto del dominio del proyecto. No existen diferentes entidades representando el mismo concepto funcional. |
| **CEM-002** | Responsabilidad única | Toda entidad agrupa solo la información necesaria para representar el concepto al que corresponde. No se incorporan datos pertenecientes a otras entidades cuando existe separación funcional clara. |
| **CEM-003** | Identificación única | Toda entidad posee un identificador oficial que permite distinguir inequívocamente cada instancia a lo largo de todo su ciclo de vida. |
| **CEM-004** | Consistencia estructural | Entidades que representan conceptos equivalentes mantienen estructura uniforme en todos los módulos que las usan. |
| **CEM-005** | Relaciones explícitas | Toda relación entre entidades se define y documenta claramente. No existen dependencias implícitas o ambiguas entre modelos de datos. |
| **CEM-006** | Integridad conceptual | Las entidades preservan la coherencia de la información que representan. No se permiten estructuras incompatibles con el significado funcional de la entidad. |
| **CEM-007** | Independencia tecnológica | La definición conceptual de entidades no depende de un lenguaje de programación, motor de base de datos, formato de almacenamiento o herramienta específica. |
| **CEM-008** | Compatibilidad documental | Las entidades permanecen alineadas con el Glosario del Proyecto, los Requisitos Funcionales, el Modelo de Decisiones, el Flujo de Datos y el resto de la documentación oficial. |
| **CEM-009** | Reusabilidad | Cuando diferentes componentes usan el mismo concepto, reutilizan la entidad oficial correspondiente en lugar de definir estructuras equivalentes. |
| **CEM-010** | Evolución controlada | Cualquier modificación a una entidad se documenta previamente y preserva compatibilidad con información existente cuando sea posible. |
| **CEM-011** | Trazabilidad | Las entidades permiten relacionar la información almacenada con los procesos, decisiones, transformaciones y recursos asociados a lo largo de todo su ciclo de vida. |
| **CEM-012** | Escalabilidad | El modelo conceptual permite incorporar nuevas entidades, relaciones y atributos sin afectar la estabilidad de estructuras existentes. |
| **CEM-013** | Compatibilidad con modelo de datos | Las entidades definidas sirven como base para el Modelo de Datos oficial del proyecto y permanecen compatibles con su evolución. |
| **CEM-014** | Consistencia terminológica | Los nombres y definiciones de entidades usan exclusivamente la terminología oficial aprobada para el proyecto. |
| **CEM-015** | Fuente oficial | Este documento constituye la referencia oficial para convenciones relacionadas con entidades y modelos conceptuales usados por la automatización. |

---

## 18. Convenciones para Módulos y Componentes (CMC-001 a CMC-015)

Reglas para definición, organización, responsabilidades y evolución de los módulos y componentes que conforman la automatización. Aplican a todos los módulos funcionales, componentes internos, servicios, procesos, utilidades, integraciones y cualquier otra unidad lógica que forme parte de la automatización.

| Código | Convención | Definición |
|--------|------------|------------|
| **CMC-001** | Responsabilidad única | Todo módulo o componente tiene un único propósito claramente definido. No se agrupan responsabilidades independientes dentro del mismo componente cuando pueden separarse razonablemente. |
| **CMC-002** | Independencia funcional | Los módulos se diseñan para que puedan evolucionar con el menor nivel posible de dependencia de otros módulos. Las dependencias permanecen explícitas y justificadas. |
| **CMC-003** | Comunicación controlada | Los componentes solo intercambian información a través de los mecanismos oficialmente definidos por la arquitectura del proyecto. No se establecen dependencias ocultas ni intercambios informales de información. |
| **CMC-004** | Cohesión | Las funciones agrupadas dentro del mismo componente están relacionadas con la misma responsabilidad funcional. |
| **CMC-005** | Bajo acoplamiento | La interacción entre módulos minimiza el nivel de dependencia entre componentes, favoreciendo mantenibilidad y reusabilidad. |
| **CMC-006** | Reusabilidad | Cuando sea posible, un componente se diseña para ser reutilizado por diferentes procesos de la automatización sin requerir modificaciones específicas. |
| **CMC-007** | Escalabilidad | La arquitectura de módulos permite incorporar nuevos componentes sin alterar significativamente la organización existente. |
| **CMC-008** | Compatibilidad documental | Los módulos y componentes permanecen alineados con los Requisitos Funcionales, Requisitos No Funcionales, Modelo de Decisiones, Flujo de Datos y el resto de la documentación oficial. |
| **CMC-009** | Independencia tecnológica | La definición conceptual de módulos y componentes no depende de un lenguaje de programación, framework, proveedor o tecnología específica. |
| **CMC-010** | Identificación | Todo módulo o componente tiene una identificación oficial que permite referenciarlo consistentemente dentro de la documentación del proyecto. |
| **CMC-011** | Evolución controlada | Cualquier modificación a un módulo o componente se documenta previamente y preserva compatibilidad con la arquitectura oficial cuando sea posible. |
| **CMC-012** | Trazabilidad | Todo módulo es relacionable con las funciones que ejecuta, los procesos en los que participa y los componentes con los que interactúa. |
| **CMC-013** | Compatibilidad arquitectónica | Ningún módulo puede incorporar responsabilidades o comportamientos incompatibles con la arquitectura oficial del proyecto. Toda extensión respeta la organización establecida. |
| **CMC-014** | Mantenibilidad | La organización modular facilita el mantenimiento independiente, reemplazo, extensión y prueba de cada componente. |
| **CMC-015** | Fuente oficial | Este documento constituye la referencia oficial para todas las convenciones relacionadas con la definición y organización de módulos y componentes usados por la automatización. |

---

## 19. Convenciones para Configuración del Sistema (CCS-001 a CCS-015)

Reglas para definición, organización, administración y evolución de todas las configuraciones usadas por la automatización. Aplican a todas las configuraciones, incluyendo parámetros generales, configuraciones de módulos, integraciones, procesamiento, modelos de lenguaje, almacenamiento, reglas operativas y cualquier otro elemento configurable del sistema.

| Código | Convención | Definición |
|--------|------------|------------|
| **CCS-001** | Separación entre configuración y lógica | Toda configuración se mantiene separada de la lógica funcional de la automatización. Los valores configurables no se incrustan directamente en la implementación cuando pueden gestionarse mediante mecanismos oficiales de configuración. |
| **CCS-002** | Configuración centralizada | Toda configuración oficial se gestiona a través de un mecanismo centralizado definido por la arquitectura del proyecto. No coexisten configuraciones duplicadas o contradictorias. |
| **CCS-003** | Identificación única | Todo parámetro de configuración posee una identificación única dentro de su ámbito correspondiente. |
| **CCS-004** | Consistencia | Los parámetros mantienen el mismo significado y comportamiento en todos los componentes que los usan. No se redefinen configuraciones equivalentes con comportamientos diferentes. |
| **CCS-005** | Documentación obligatoria | Todo parámetro de configuración se documenta indicando su propósito, ámbito y uso dentro del proyecto. |
| **CCS-006** | Valores controlados | Las configuraciones usan solo valores compatibles con las reglas definidas por la arquitectura del proyecto y la documentación oficial. |
| **CCS-007** | Independencia tecnológica | Las convenciones relacionadas con configuración permanecen independientes del lenguaje de programación, proveedor, plataforma o herramienta usada durante la implementación. |
| **CCS-008** | Compatibilidad documental | Toda configuración permanece alineada con los Requisitos Funcionales, Requisitos No Funcionales, Modelo de Decisiones, Flujo de Datos y el resto de la documentación oficial vigente. |
| **CCS-009** | Evolución controlada | Modificaciones a parámetros de configuración se documentan previamente y preservan compatibilidad con el comportamiento esperado del sistema. |
| **CCS-010** | Reusabilidad | Cuando sea posible, el mismo parámetro de configuración se reutiliza por todos los componentes que comparten la misma necesidad funcional. No se crean configuraciones redundantes. |
| **CCS-011** | Trazabilidad | Toda modificación a una configuración relevante es identificable y relacionable con la versión correspondiente del proyecto cuando sea necesario. |
| **CCS-012** | Escalabilidad | La estructura de configuración permite incorporar nuevos parámetros sin afectar la organización existente. |
| **CCS-013** | Compatibilidad de módulos | Parámetros compartidos por diferentes módulos mantienen comportamiento consistente en toda la automatización. |
| **CCS-014** | Auditabilidad | Configuraciones que afectan el comportamiento funcional de la automatización son verificables durante auditorías, diagnósticos y reprocesamiento. |
| **CCS-015** | Fuente oficial | Este documento constituye la referencia oficial para todas las convenciones relacionadas con configuración del sistema usadas por la automatización. |

---

## 20. Restricciones Estándar (RES-001 a RES-015)

Límites normativos que se respetan durante la definición, aplicación, modificación y evolución de todos los estándares usados por la automatización. Preservan coherencia, estabilidad, mantenibilidad y compatibilidad del proyecto, evitando que la incorporación de nuevos estándares o la modificación de existentes comprometa la integridad de la documentación o la operación de la automatización. Son obligatorias para todos los documentos, componentes, procesos, configuraciones, estructuras de datos, recursos y extensiones futuras del proyecto.

| Código | Restricción | Definición |
|--------|-------------|------------|
| **RES-001** | Cumplimiento obligatorio | Todos los estándares definidos en este documento se cumplen sin excepción, salvo autorización expresamente documentada y aprobada. |
| **RES-002** | Prohibición de contradicciones | Ningún estándar, documento, módulo o componente puede establecer reglas que contradigan las convenciones oficiales definidas en este documento. |
| **RES-003** | Prohibición de duplicación | La misma regla, convención o definición no se mantiene en múltiples documentos cuando existe una fuente de referencia oficial. Otros documentos usan referencias cruzadas. |
| **RES-004** | Preservación de compatibilidad | Cualquier modificación a un estándar preserva, cuando sea posible, compatibilidad con componentes y documentos existentes. |
| **RES-005** | Evolución documentada | Toda incorporación, modificación o eliminación de un estándar se documenta antes de entrar en vigor. |
| **RES-006** | Independencia tecnológica | Los estándares oficiales no dependen de tecnologías, herramientas, proveedores o plataformas específicas, salvo que un documento especializado lo justifique explícitamente. |
| **RES-007** | Terminología oficial | Todos los estándares usan exclusivamente la terminología oficial definida por el Glosario del Proyecto. |
| **RES-008** | Coherencia documental | Modificaciones que afectan múltiples documentos se reflejan en toda la documentación correspondiente para mantener consistencia global del proyecto. |
| **RES-009** | Unicidad normativa | Cada aspecto regulado por el proyecto tiene una única referencia normativa oficial. No coexisten estándares paralelos para el mismo propósito. |
| **RES-010** | Preservación de trazabilidad | Ninguna modificación a los estándares puede eliminar la capacidad de reconstruir el historial de decisiones, cambios o versiones del proyecto. |
| **RES-011** | Mantenibilidad | Nuevos estándares favorecen la simplicidad, claridad y facilidad de mantenimiento del proyecto. No se incorporan reglas innecesariamente complejas. |
| **RES-012** | Escalabilidad | Toda extensión de los estándares se diseña de manera que permita el crecimiento del proyecto sin alterar la estructura normativa existente. |
| **RES-013** | Compatibilidad arquitectónica | Los estándares permanecen compatibles con la arquitectura oficial de la automatización y con los principios definidos en la documentación del proyecto. |
| **RES-014** | Aplicación uniforme | Las mismas convenciones se aplican consistentemente en todos los componentes del proyecto. No existen excepciones implícitas ni tratamientos particulares no documentados. |
| **RES-015** | Fuente normativa oficial | Este documento constituye la única referencia oficial para todas las convenciones generales y estándares usados por la automatización. Toda nueva norma se alinea con las restricciones aquí establecidas. |

---

## 21. Criterios de Aceptación (CAE-001 a CAE-015)

Condiciones que el Documento de Estándares del Proyecto debe cumplir para considerarse completo, consistente y oficialmente aprobado como referencia normativa para la automatización. Garantizan que todas las convenciones definidas son suficientes para proporcionar un marco uniforme aplicable consistentemente durante diseño, desarrollo, implementación, mantenimiento y evolución del proyecto.

| Código | Criterio | Verificación |
|--------|----------|--------------|
| **CAE-001** | Cobertura completa | El documento cubre todas las categorías de estándares definidas para el proyecto, sin omitir aspectos relevantes para la organización, desarrollo y mantenimiento de la automatización. |
| **CAE-002** | Consistencia interna | Todas las convenciones definidas son compatibles entre sí. No existen contradicciones, duplicaciones ni ambigüedades dentro del documento. |
| **CAE-003** | Compatibilidad documental | El documento permanece alineado con el Glosario del Proyecto, los Requisitos Funcionales, los Requisitos No Funcionales, el Modelo de Decisiones, el Flujo de Datos y el resto de la documentación oficial vigente. |
| **CAE-004** | Claridad | Las reglas se redactan de manera precisa, objetiva y fácilmente interpretable. Cada convención admite una sola interpretación. |
| **CAE-005** | Independencia tecnológica | Las convenciones generales permanecen independientes de tecnologías, plataformas, lenguajes de programación o herramientas específicas, salvo justificación documental explícita. |
| **CAE-006** | Aplicabilidad | Todas las convenciones definidas son prácticamente aplicables durante la construcción y evolución de la automatización. No se incorporan estándares imposibles o innecesariamente complejos de implementar. |
| **CAE-007** | Escalabilidad | El documento permite la incorporación de nuevos estándares, módulos, componentes y procesos sin requerir modificaciones estructurales significativas. |
| **CAE-008** | Reusabilidad | Las convenciones favorecen la reutilización de reglas, estructuras y criterios comunes entre todos los documentos y componentes del proyecto. |
| **CAE-009** | Trazabilidad | Las convenciones facilitan identificación, seguimiento y auditoría de todos los elementos regulados por el proyecto. |
| **CAE-010** | Mantenibilidad | El documento facilita la actualización de estándares sin comprometer la coherencia global de la documentación. |
| **CAE-011** | Ausencia de duplicación | Las definiciones normativas se documentan una vez. Otros documentos usan referencias oficiales en lugar de duplicar información. |
| **CAE-012** | Compatibilidad futura | Las convenciones permanecen válidas durante la evolución del proyecto, permitiendo la incorporación de nuevas funcionalidades y tecnologías sin redefinir la base normativa. |
| **CAE-013** | Coherencia arquitectónica | Las convenciones son compatibles con la arquitectura general del proyecto y con todos los documentos especializados que las implementan. |
| **CAE-014** | Verificabilidad | El cumplimiento de las convenciones es comprobable mediante revisiones documentales, inspecciones técnicas o validaciones durante el desarrollo de la automatización. |
| **CAE-015** | Aprobación formal | El documento solo se considera aprobado cuando todos los criterios definidos en este capítulo están satisfechos y el contenido ha sido validado como referencia oficial de estándares del proyecto. |

**Condición de aceptación del documento:** El Documento 5 – Estándares del Proyecto se considera oficialmente aceptado cuando: (1) Todos sus capítulos han sido completados y aprobados. (2) No existen contradicciones con la documentación oficial vigente. (3) Todas las convenciones son consistentes entre sí. (4) El documento puede usarse como referencia normativa para el resto del proyecto. (5) Documentos posteriores pueden implementar estas convenciones sin redefinirlas. (6) Se garantizan mantenibilidad, escalabilidad, trazabilidad y coherencia normativa de toda la automatización.

---

## 22. Índice de Estándares

Este índice consolida todos los estándares definidos en el Documento 5, constituyendo la referencia oficial para consulta, mantenimiento y evolución de las convenciones usadas por la automatización. Facilita la localización de cada estándar, evita duplicaciones normativas y establece una única fuente de referencia para todos los documentos del proyecto.

### 22.1. Estándares Generales

| Código | Estándar |
|--------|----------|
| PEP | Principios de Estándares del Proyecto |
| CEG | Convenciones Generales |
| CNP | Convenciones de Nombres |
| CID | Convenciones para Identificadores |

### 22.2. Estándares Operativos

| Código | Estándar |
|--------|----------|
| CED | Convenciones para Estados |
| CFH | Convenciones para Fechas y Horas |
| CFDT | Convenciones para Formatos de Datos |
| CJS | Convenciones para Estructuras JSON |

### 22.3. Estándares Documentales

| Código | Estándar |
|--------|----------|
| CDO | Convenciones para Documentación |
| CPR | Convenciones para Prompts |
| CNA | Convenciones para Nombres de Archivos y Documentos |
| COC | Convenciones para Organización de Carpetas |
| CVE | Convenciones para Versionado |

### 22.4. Estándares de Operación y Control

| Código | Estándar |
|--------|----------|
| CLR | Convenciones para Logs |
| CAT | Convenciones para Auditoría y Trazabilidad |
| CEM | Convenciones para Entidades y Modelos de Datos |
| CMC | Convenciones para Módulos y Componentes |
| CCS | Convenciones para Configuración del Sistema |

### 22.5. Estándares Normativos

| Código | Estándar |
|--------|----------|
| RES | Restricciones Estándar |
| CAE | Criterios de Aceptación |

### 22.6. Uso del Índice

Este índice constituye la referencia oficial para identificar los estándares usados dentro del proyecto. Toda nueva convención incorporada al Documento 5 debe:

1. Incorporar un prefijo único según las convenciones para identificadores.
2. Mantener la estructura de codificación definida en este documento.
3. Actualizar este índice antes de considerarse oficialmente aprobada.
4. Preservar coherencia con el resto de los estándares existentes.

### 22.7. Mantenimiento del Índice

Toda incorporación, modificación o eliminación de un estándar se refleja en este índice para garantizar que continúe siendo la referencia oficial de las convenciones usadas por el proyecto. No existen estándares oficiales que no estén registrados en este índice.
