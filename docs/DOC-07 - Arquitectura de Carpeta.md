# DOC-O7 - Arquitectura de Carpetas

## 1. Propósito del documento

El presente documento define la arquitectura oficial de carpetas y archivos de la automatización de búsqueda de empleo.

Su propósito es establecer una estructura uniforme para la organización física de todos los recursos que conforman el proyecto, garantizando consistencia, claridad, mantenibilidad, escalabilidad y facilidad de navegación durante todo su ciclo de vida.

Este documento constituye la referencia oficial para la ubicación, organización y distribución de los documentos, módulos, configuraciones, datos, prompts, registros, scripts, recursos auxiliares y demás elementos que integran la automatización, independientemente de la tecnología utilizada para su implementación.

Asimismo, define los lineamientos necesarios para asegurar que todos los componentes del proyecto se almacenen siguiendo una estructura predecible, evitando duplicidades, dependencias innecesarias y desorganización a medida que la automatización evolucione.

Las disposiciones contenidas en este documento serán de cumplimiento obligatorio para todos los módulos, procesos, componentes, recursos, archivos y directorios del proyecto, así como para cualquier ampliación, refactorización o incorporación futura de nuevos elementos a la arquitectura.

---

## 2. Principios de la arquitectura de carpetas

Los siguientes principios establecen las reglas generales que deberán regir el diseño, organización, mantenimiento y evolución de la arquitectura de carpetas de la automatización de búsqueda de empleo.

Estos principios complementan el Glosario del Proyecto, los Requisitos Funcionales, los Requisitos No Funcionales, el Modelo de Decisiones, el Flujo de Datos, los Estándares del Proyecto y el Modelo de Manejo de Errores, constituyendo la base normativa para garantizar una organización uniforme de todos los recursos del proyecto.

---

### PAC-001. Organización uniforme

Toda la estructura de carpetas deberá seguir un único modelo organizacional definido por este documento.

No se permitirán estructuras alternativas que generen inconsistencias dentro del proyecto.

---

### PAC-002. Responsabilidad única

Cada directorio deberá tener un único propósito claramente definido.

No se permitirá almacenar recursos de distinta naturaleza cuando exista un directorio específico para ellos.

---

### PAC-003. Jerarquía lógica

La estructura de carpetas deberá reflejar la organización funcional de la automatización, facilitando la comprensión del proyecto sin depender del conocimiento de su implementación técnica.

---

### PAC-004. Escalabilidad

La arquitectura deberá permitir la incorporación de nuevos módulos, recursos y componentes sin requerir reorganizaciones importantes de la estructura existente.

---

### PAC-005. Independencia tecnológica

La organización de carpetas no dependerá de un lenguaje de programación, framework, proveedor o herramienta específica.

La estructura deberá mantenerse válida aun cuando cambien las tecnologías utilizadas.

---

### PAC-006. Ubicación predecible

Todo recurso deberá almacenarse en una ubicación predefinida y fácilmente identificable conforme a las reglas establecidas en este documento.

---

### PAC-007. Evitar duplicidad

Un mismo recurso no deberá almacenarse en múltiples ubicaciones salvo que exista una justificación documentada y aprobada.

---

### PAC-008. Separación de responsabilidades

Los documentos, configuraciones, datos, prompts, registros, código fuente, recursos temporales y demás elementos deberán mantenerse separados en directorios independientes.

---

### PAC-009. Consistencia estructural

Todos los módulos de la automatización deberán respetar la misma organización interna de carpetas cuando la naturaleza de sus componentes sea equivalente.

---

### PAC-010. Facilidad de mantenimiento

La arquitectura deberá facilitar la localización, modificación, sustitución y eliminación de cualquier recurso sin afectar innecesariamente otros componentes del proyecto.

---

### PAC-011. Compatibilidad documental

La organización física del proyecto deberá mantenerse alineada con la documentación oficial y con las convenciones establecidas en el Documento de Estándares del Proyecto.

---

### PAC-012. Evolución controlada

Toda modificación a la arquitectura de carpetas deberá documentarse, justificarse y aprobarse antes de entrar en vigencia.

---

### PAC-013. Trazabilidad

La ubicación de cada recurso deberá permitir identificar fácilmente su función, su módulo de pertenencia y su relación con el resto de la automatización.

---

### PAC-014. Reutilización

La estructura deberá favorecer la reutilización de recursos comunes evitando la creación innecesaria de copias o estructuras redundantes.

---

### PAC-015. Cumplimiento obligatorio

Toda carpeta, archivo o recurso incorporado al proyecto deberá respetar las reglas definidas en este documento antes de considerarse parte oficial de la arquitectura.

---

## Principios generales de la arquitectura de carpetas

La arquitectura de carpetas deberá cumplir los siguientes principios:

- Mantener una organización uniforme en todo el proyecto.
- Facilitar la navegación y localización de recursos.
- Favorecer la escalabilidad de la automatización.
- Evitar duplicidades y dependencias innecesarias.
- Separar claramente las responsabilidades de cada directorio.
- Mantener independencia tecnológica.
- Garantizar la trazabilidad de los recursos.
- Facilitar el mantenimiento y la evolución del proyecto.
- Permanecer alineada con toda la documentación oficial.
- Servir como referencia única para la organización física del proyecto.

---

## 3. Estructura general del proyecto

La estructura general del proyecto define la organización de más alto nivel de la automatización de búsqueda de empleo.

Su propósito es establecer una arquitectura física uniforme que facilite la ubicación de los recursos, reduzca la complejidad del proyecto y permita incorporar nuevos componentes sin alterar la organización existente.

Toda la estructura deberá organizarse utilizando directorios de primer nivel claramente diferenciados según su responsabilidad dentro de la automatización.

---

### EGP-001. Organización por responsabilidad

Los directorios de primer nivel deberán agrupar recursos que compartan una misma responsabilidad funcional.

No se permitirá utilizar directorios genéricos para almacenar recursos de naturaleza diferente.

---

### EGP-002. Separación entre documentación e implementación

La documentación oficial del proyecto deberá mantenerse completamente separada de los recursos utilizados para la implementación de la automatización.

---

### EGP-003. Separación entre configuración y lógica

Los archivos de configuración deberán almacenarse en directorios independientes de aquellos que contengan lógica de ejecución.

---

### EGP-004. Separación entre datos y procesos

Los datos generados, procesados o almacenados por la automatización deberán mantenerse separados de los componentes responsables de su procesamiento.

---

### EGP-005. Separación entre recursos permanentes y temporales

Los recursos temporales deberán almacenarse en ubicaciones específicas que permitan su limpieza o regeneración sin afectar la información permanente del proyecto.

---

### EGP-006. Organización modular

Cada módulo funcional de la automatización deberá disponer de un espacio claramente delimitado dentro de la estructura general, evitando dependencias físicas innecesarias entre módulos.

---

### EGP-007. Recursos compartidos

Los recursos utilizados por múltiples módulos deberán ubicarse en directorios compartidos definidos oficialmente, evitando la duplicación de archivos.

---

### EGP-008. Centralización de configuraciones

Las configuraciones comunes de la automatización deberán almacenarse en un único lugar, facilitando su mantenimiento y control de versiones.

---

### EGP-009. Centralización de documentación

Toda la documentación oficial del proyecto deberá encontrarse organizada bajo una estructura documental única, respetando los estándares definidos en el Documento 5.

---

### EGP-010. Centralización de registros

Los registros operativos, auditorías y archivos de seguimiento deberán almacenarse en ubicaciones específicas destinadas exclusivamente para dicho propósito.

---

### EGP-011. Escalabilidad estructural

La incorporación de nuevos módulos, componentes o recursos no deberá requerir reorganizar la estructura principal del proyecto.

La arquitectura deberá admitir el crecimiento progresivo de la automatización.

---

### EGP-012. Independencia tecnológica

La estructura general no dependerá de herramientas, lenguajes de programación o tecnologías específicas.

La organización física deberá mantenerse válida aun cuando cambie la implementación técnica.

---

### EGP-013. Trazabilidad

La ubicación física de cualquier recurso deberá facilitar la identificación de su función, su módulo de pertenencia y su relación con el resto del proyecto.

---

### EGP-014. Consistencia

Todos los componentes deberán respetar la estructura oficial definida en este documento.

No podrán crearse directorios alternativos que contradigan la arquitectura aprobada.

---

### EGP-015. Fuente única de organización

La arquitectura definida en este documento constituirá la única referencia oficial para la organización física del proyecto.

Cualquier modificación a la estructura deberá documentarse y aprobarse previamente.

---

## Objetivos de la estructura general

La estructura general del proyecto deberá garantizar:

- Organización uniforme de todos los recursos.
- Separación clara de responsabilidades.
- Facilidad de navegación.
- Escalabilidad del proyecto.
- Independencia tecnológica.
- Reutilización de recursos comunes.
- Facilidad de mantenimiento.
- Compatibilidad con la documentación oficial.
- Trazabilidad de todos los componentes.
- Evolución controlada de la arquitectura.

---

## 4. Organización de directorios

La organización de directorios define la estructura oficial de carpetas de la automatización de búsqueda de empleo.

Su propósito es establecer una distribución uniforme de todos los recursos del proyecto, garantizando que cada directorio posea una única responsabilidad y una ubicación predecible dentro de la arquitectura general.

La estructura definida en este capítulo será de cumplimiento obligatorio para todos los módulos y recursos que formen parte de la automatización.

---

### ODR-001. Directorio raíz

Todo el proyecto deberá encontrarse contenido dentro de un único directorio raíz que actuará como punto de entrada de la arquitectura.

Ningún recurso perteneciente al proyecto deberá almacenarse fuera de esta estructura.

---

### ODR-002. Directorios de primer nivel

Únicamente podrán existir directorios de primer nivel oficialmente definidos por este documento.

Cada uno deberá representar una categoría funcional claramente diferenciada.

---

### ODR-003. Organización jerárquica

Los directorios deberán organizarse utilizando una jerarquía lógica, donde cada nivel represente una especialización del nivel superior.

La profundidad de la estructura deberá mantenerse razonable para facilitar la navegación.

---

### ODR-004. Responsabilidad exclusiva

Cada directorio deberá almacenar únicamente recursos relacionados con su propósito.

No se permitirá utilizar una carpeta como almacenamiento genérico de archivos sin clasificación.

---

### ODR-005. Directorios compartidos

Los recursos reutilizados por múltiples módulos deberán almacenarse en directorios compartidos definidos oficialmente.

Ningún módulo deberá mantener copias independientes de recursos comunes.

---

### ODR-006. Directorios específicos por módulo

Cada módulo funcional de la automatización deberá disponer de un espacio propio dentro de la estructura del proyecto.

Los recursos exclusivos de un módulo deberán permanecer dentro de su propio directorio.

---

### ODR-007. Separación entre recursos permanentes y temporales

Los recursos temporales, archivos intermedios y datos de ejecución deberán almacenarse en directorios independientes de los recursos permanentes.

Esto permitirá su limpieza sin afectar la información oficial del proyecto.

---

### ODR-008. Organización uniforme

Cuando varios módulos utilicen estructuras equivalentes, deberán mantener la misma organización interna de directorios.

---

### ODR-009. Nombres consistentes

Los nombres de los directorios deberán cumplir las convenciones oficiales definidas en el Documento de Estándares del Proyecto.

No se permitirán nombres ambiguos, duplicados ni dependientes de una tecnología específica.

---

### ODR-010. Crecimiento controlado

La incorporación de nuevos directorios deberá responder a una necesidad funcional claramente identificada.

No podrán crearse carpetas preventivas para funcionalidades aún inexistentes.

---

### ODR-011. Eliminación controlada

La eliminación o reorganización de un directorio deberá garantizar previamente que ningún componente activo dependa de los recursos contenidos en él.

---

### ODR-012. Compatibilidad con el versionado

La organización de directorios deberá facilitar el control de versiones, evitando almacenar recursos generados automáticamente cuando estos puedan reconstruirse durante la ejecución.

---

### ODR-013. Trazabilidad

La ubicación física de cualquier recurso deberá permitir identificar inmediatamente su función y el componente al que pertenece.

---

### ODR-014. Evolución controlada

Toda modificación a la estructura oficial de directorios deberá documentarse, justificarse y aprobarse antes de incorporarse al proyecto.

---

### ODR-015. Arquitectura única

La estructura de directorios definida por este documento constituirá la única arquitectura oficial del proyecto.

No se permitirán variantes paralelas ni estructuras alternativas.

---

## Objetivos de la organización de directorios

La organización oficial de directorios deberá garantizar:

- Navegación sencilla por el proyecto.
- Separación clara de responsabilidades.
- Uniformidad entre módulos.
- Reutilización de recursos comunes.
- Escalabilidad de la estructura.
- Facilidad de mantenimiento.
- Compatibilidad con el control de versiones.
- Independencia tecnológica.
- Evolución controlada.
- Trazabilidad completa de todos los recursos.

---

## 5. Organización de archivos

La organización de archivos define la estructura oficial de los archivos que conforman la automatización de búsqueda de empleo y su distribución dentro de los directorios definidos por la arquitectura del proyecto.

Su propósito es garantizar que cada archivo posea una ubicación única, una responsabilidad claramente definida y una organización uniforme que facilite la navegación, el mantenimiento y la evolución de la automatización.

---

### OAR-001. Ubicación única

Todo archivo deberá almacenarse en un único directorio oficial conforme a las reglas establecidas en este documento.

No se permitirá mantener múltiples copias de un mismo archivo salvo que exista una justificación documentada y aprobada.

---

### OAR-002. Responsabilidad única

Cada archivo deberá cumplir una única función claramente definida.

No se permitirá concentrar responsabilidades independientes dentro de un mismo archivo cuando puedan separarse de forma lógica.

---

### OAR-003. Organización por categoría

Los archivos deberán agruparse según su naturaleza.

Como mínimo deberán existir categorías independientes para:

- Documentación.
- Configuración.
- Prompts.
- Datos.
- Registros.
- Recursos compartidos.
- Recursos temporales.
- Scripts.
- Componentes del sistema.

---

### OAR-004. Convenciones de nombres

Todos los archivos deberán respetar las convenciones oficiales de nomenclatura definidas en el Documento de Estándares del Proyecto.

---

### OAR-005. Coherencia entre módulos

Los módulos equivalentes deberán mantener la misma organización interna de archivos para facilitar su mantenimiento y comprensión.

---

### OAR-006. Separación entre archivos editables y generados

Los archivos mantenidos manualmente deberán almacenarse separados de aquellos generados automáticamente por la automatización.

---

### OAR-007. Archivos compartidos

Los archivos utilizados por múltiples módulos deberán mantenerse en ubicaciones compartidas oficialmente definidas.

No deberán existir copias locales dentro de cada módulo.

---

### OAR-008. Archivos temporales

Los archivos temporales deberán almacenarse únicamente en los directorios destinados para dicho propósito.

Su permanencia será exclusivamente transitoria.

---

### OAR-009. Archivos de configuración

Toda configuración del sistema deberá encontrarse centralizada.

No se permitirá mantener configuraciones distribuidas innecesariamente entre distintos componentes.

---

### OAR-010. Archivos de documentación

Toda la documentación oficial del proyecto deberá mantenerse organizada conforme a la arquitectura documental definida por el proyecto.

---

### OAR-011. Archivos de datos

Los archivos que contengan información procesada por la automatización deberán mantenerse separados de los archivos utilizados para la implementación del sistema.

---

### OAR-012. Compatibilidad con el control de versiones

La organización de archivos deberá facilitar el control de versiones.

Los archivos generados automáticamente que puedan reconstruirse no deberán formar parte del contenido permanente del proyecto.

---

### OAR-013. Integridad

Ningún archivo deberá depender de rutas físicas ambiguas o cambiantes para su funcionamiento.

Las referencias entre archivos deberán mantenerse consistentes durante toda la evolución del proyecto.

---

### OAR-014. Evolución controlada

La creación, modificación, traslado o eliminación de archivos oficiales deberá respetar la arquitectura definida en este documento.

Toda modificación significativa deberá documentarse.

---

### OAR-015. Fuente oficial

La estructura definida en este documento constituirá la única organización oficial de archivos del proyecto.

No se permitirán estructuras paralelas que contradigan estas reglas.

---

## Estructura oficial del proyecto

La siguiente estructura representa la arquitectura oficial de directorios y archivos de la automatización:

```text
/
├── docs/                  # Documentación oficial del proyecto
│   ├── anexos/
│   ├── diagramas/
│   ├── planes/
│   └── historial/
│
├── config/                # Configuración del sistema
│
├── prompts/               # Prompts oficiales
│
├── modules/               # Módulos funcionales
│   ├── descubrimiento/
│   ├── preparacion/
│   ├── evaluacion/
│   ├── procesamiento/
│   └── gestion/
│
├── shared/                # Recursos reutilizables
│
├── data/                  # Datos persistentes
│   ├── entrada/
│   ├── procesamiento/
│   ├── salida/
│   └── respaldo/
│
├── logs/                  # Registros y auditoría
│
├── temp/                  # Archivos temporales
│
├── scripts/               # Scripts auxiliares
│
├── tests/                 # Pruebas
│
└── README.md              # Información general del proyecto
```

---

## Objetivos de la organización de archivos

La organización oficial de archivos deberá garantizar:

- Una ubicación única para cada archivo.
- Responsabilidad claramente definida.
- Uniformidad entre módulos.
- Facilidad de navegación.
- Separación entre archivos permanentes y temporales.
- Reutilización de recursos comunes.
- Compatibilidad con el control de versiones.
- Escalabilidad de la arquitectura.
- Facilidad de mantenimiento.
- Trazabilidad completa de todos los recursos.

---

## 6. Convenciones de ubicación de recursos

Las convenciones de ubicación de recursos establecen las reglas oficiales para determinar dónde deberá almacenarse cada recurso perteneciente a la automatización de búsqueda de empleo.

Su propósito es garantizar una organización uniforme, eliminar ambigüedades, facilitar la localización de los recursos y preservar la coherencia de la arquitectura del proyecto durante toda su evolución.

Todo recurso deberá poseer una ubicación única definida conforme a las reglas establecidas en este capítulo.

---

### CUR-001. Ubicación por responsabilidad

Todo recurso deberá almacenarse en el directorio cuya responsabilidad funcional corresponda a la naturaleza del recurso.

La ubicación nunca deberá definirse por conveniencia temporal.

---

### CUR-002. Recursos exclusivos

Los recursos utilizados únicamente por un módulo deberán permanecer dentro de la estructura correspondiente a dicho módulo.

No deberán almacenarse en ubicaciones compartidas.

---

### CUR-003. Recursos compartidos

Los recursos reutilizados por varios módulos deberán ubicarse exclusivamente en los directorios destinados para recursos compartidos.

Ningún módulo deberá mantener copias independientes.

---

### CUR-004. Separación documental

Toda la documentación oficial deberá mantenerse separada de los recursos utilizados durante la ejecución de la automatización.

---

### CUR-005. Separación de configuraciones

Los archivos de configuración deberán mantenerse agrupados en las ubicaciones oficiales definidas para este propósito.

No deberán distribuirse entre distintos módulos salvo que exista una justificación técnica documentada.

---

### CUR-006. Recursos temporales

Los recursos temporales deberán almacenarse únicamente en las ubicaciones destinadas para archivos transitorios.

No podrán considerarse parte permanente de la arquitectura.

---

### CUR-007. Recursos persistentes

Los recursos cuya información deba conservarse entre ejecuciones deberán ubicarse exclusivamente en directorios destinados para almacenamiento permanente.

---

### CUR-008. Recursos generados automáticamente

Todo recurso generado por la automatización deberá almacenarse conforme a su naturaleza, distinguiéndose claramente de los recursos mantenidos manualmente.

---

### CUR-009. Recursos de auditoría

Los registros, evidencias, métricas y demás recursos utilizados para auditoría y trazabilidad deberán mantenerse agrupados en ubicaciones específicas para facilitar su consulta.

---

### CUR-010. Recursos de pruebas

Los recursos utilizados para pruebas deberán mantenerse completamente separados de los utilizados por la operación normal de la automatización.

---

### CUR-011. Recursos externos

Los recursos obtenidos desde plataformas, servicios o fuentes externas deberán mantenerse identificados y organizados independientemente de los recursos propios del proyecto.

---

### CUR-012. Recursos obsoletos

Los recursos que dejen de utilizarse no deberán permanecer mezclados con los recursos activos.

Su tratamiento deberá seguir las políticas oficiales de mantenimiento, archivado o eliminación definidas por el proyecto.

---

### CUR-013. Consistencia

La ubicación asignada a un recurso deberá mantenerse estable durante todo su ciclo de vida, salvo que exista una reorganización oficialmente aprobada.

---

### CUR-014. Trazabilidad

La ubicación física de un recurso deberá permitir identificar fácilmente:

- Su propósito.
- El módulo al que pertenece.
- Su nivel de reutilización.
- Su relación con otros componentes del proyecto.

---

### CUR-015. Cumplimiento obligatorio

Todo nuevo recurso incorporado al proyecto deberá respetar estas convenciones antes de formar parte oficial de la arquitectura.

---

## Objetivos de las convenciones de ubicación

Las convenciones de ubicación deberán garantizar:

- Ubicación única para cada recurso.
- Organización uniforme.
- Separación clara de responsabilidades.
- Facilidad de navegación.
- Reutilización de recursos compartidos.
- Separación entre recursos permanentes y temporales.
- Compatibilidad con la arquitectura general.
- Facilidad de mantenimiento.
- Trazabilidad completa.
- Evolución controlada de la estructura del proyecto.

---

## 7. Organización de la documentación

La organización de la documentación define las reglas oficiales para la estructura, ubicación y administración de toda la documentación perteneciente a la automatización de búsqueda de empleo.

Su propósito es garantizar que la documentación permanezca organizada, accesible, consistente y alineada con la evolución del proyecto, facilitando su consulta, mantenimiento y trazabilidad.

Toda la documentación oficial deberá cumplir las disposiciones establecidas en este capítulo, independientemente de su naturaleza o formato.

---

### ORD-001. Repositorio documental único

Toda la documentación oficial del proyecto deberá mantenerse dentro de una estructura documental única.

No se permitirá mantener documentación oficial distribuida en múltiples ubicaciones sin una justificación aprobada.

---

### ORD-002. Clasificación documental

Los documentos deberán organizarse según su finalidad.

Como mínimo deberán diferenciarse las siguientes categorías:

- Documentación estratégica.
- Documentación funcional.
- Documentación técnica.
- Arquitectura.
- Estándares.
- Anexos.
- Diagramas.
- Manuales.
- Historiales.
- Referencias.

---

### ORD-003. Separación de documentación y operación

Los documentos oficiales deberán mantenerse completamente separados de los archivos utilizados durante la ejecución de la automatización.

---

### ORD-004. Ubicación predecible

Todo documento deberá almacenarse en una ubicación previamente definida por la arquitectura documental del proyecto.

Su ubicación no deberá depender del autor ni del momento de creación.

---

### ORD-005. Unicidad documental

Cada documento oficial deberá existir únicamente en una versión vigente dentro de la documentación activa.

No se permitirá mantener múltiples copias activas del mismo documento.

---

### ORD-006. Organización de anexos

Los anexos deberán mantenerse organizados de manera independiente de los documentos principales.

Cada anexo deberá referenciar explícitamente el documento al que complementa.

---

### ORD-007. Organización de diagramas

Los diagramas oficiales deberán almacenarse agrupados según el proceso, módulo o documento al que pertenecen.

---

### ORD-008. Historial documental

Las versiones históricas, registros de cambios y conversaciones utilizadas para construir la documentación deberán mantenerse separadas de la documentación vigente.

Su conservación tendrá fines de auditoría y trazabilidad.

---

### ORD-009. Documentación generada automáticamente

Los documentos generados por procesos automáticos deberán identificarse claramente para diferenciarlos de aquellos mantenidos manualmente.

---

### ORD-010. Referencias cruzadas

Cuando un documento dependa de otro, la relación deberá establecerse mediante referencias documentales oficiales, evitando la duplicación de contenido.

---

### ORD-011. Evolución controlada

Toda incorporación, reorganización o eliminación de documentación oficial deberá documentarse previamente conforme a las políticas del proyecto.

---

### ORD-012. Compatibilidad

La organización documental deberá mantenerse compatible con las convenciones establecidas en el Documento de Estándares del Proyecto.

---

### ORD-013. Trazabilidad

Todo documento deberá poder relacionarse con:

- El documento principal al que pertenece.
- Los anexos asociados.
- Las decisiones que documenta.
- Los módulos afectados.
- El historial de cambios correspondiente.

---

### ORD-014. Conservación

La documentación histórica no deberá eliminarse mientras pueda aportar valor para auditorías, reconstrucción de decisiones o evolución del proyecto.

---

### ORD-015. Fuente oficial

La documentación organizada conforme a este documento constituirá la única fuente oficial de información del proyecto.

Cualquier documentación externa tendrá únicamente carácter informativo mientras no sea incorporada oficialmente.

---

## Objetivos de la organización documental

La organización de la documentación deberá garantizar:

- Una única fuente oficial de información.
- Organización uniforme de todos los documentos.
- Separación entre documentación vigente e histórica.
- Clasificación clara por categorías.
- Facilidad de consulta.
- Compatibilidad con los estándares del proyecto.
- Reutilización mediante referencias cruzadas.
- Trazabilidad documental completa.
- Conservación del historial del proyecto.
- Evolución controlada de toda la documentación.

---

## 8. Organización de la configuración del sistema

La organización de la configuración del sistema establece las reglas oficiales para la administración, almacenamiento y organización de todas las configuraciones utilizadas por la automatización de búsqueda de empleo.

Su propósito es garantizar que la configuración permanezca centralizada, consistente, controlada y desacoplada de la lógica de implementación, facilitando su mantenimiento, evolución y reutilización.

Toda configuración utilizada por la automatización deberá cumplir las disposiciones establecidas en este capítulo.

---

### OCS-001. Centralización

Toda configuración del sistema deberá mantenerse centralizada dentro de la arquitectura oficial del proyecto.

No se permitirá distribuir configuraciones equivalentes entre distintos módulos sin una justificación técnica documentada.

---

### OCS-002. Separación de la lógica

La configuración deberá mantenerse completamente separada de la lógica de negocio y de la implementación de los módulos.

Los valores configurables no deberán encontrarse codificados directamente dentro de los componentes del sistema.

---

### OCS-003. Organización por responsabilidad

Las configuraciones deberán organizarse según el componente, proceso o ámbito funcional al que pertenezcan.

Cada configuración deberá poseer un propósito claramente definido.

---

### OCS-004. Reutilización

Las configuraciones utilizadas por múltiples módulos deberán definirse una única vez y compartirse mediante los mecanismos oficiales establecidos por la arquitectura.

---

### OCS-005. Consistencia

Toda configuración deberá mantener una estructura uniforme y compatible con las convenciones definidas en el Documento de Estándares del Proyecto.

---

### OCS-006. Identificación

Cada configuración deberá encontrarse claramente identificada mediante un nombre único y descriptivo que permita reconocer fácilmente su propósito.

---

### OCS-007. Independencia tecnológica

La organización de las configuraciones no dependerá de un formato, lenguaje o herramienta específica.

Las reglas establecidas en este documento deberán mantenerse válidas independientemente de la tecnología utilizada.

---

### OCS-008. Control de cambios

Toda modificación realizada sobre una configuración oficial deberá poder identificarse, documentarse y justificarse.

---

### OCS-009. Separación por entorno

Cuando la automatización requiera configuraciones específicas para distintos entornos de ejecución, estas deberán mantenerse claramente diferenciadas sin alterar la estructura general del proyecto.

---

### OCS-010. Valores sensibles

Las configuraciones que contengan información sensible deberán administrarse mediante mecanismos seguros definidos por la arquitectura del sistema.

Su tratamiento no podrá comprometer la seguridad ni la trazabilidad del proyecto.

---

### OCS-011. Eliminación controlada

Las configuraciones obsoletas no deberán eliminarse sin verificar previamente que ningún componente activo dependa de ellas.

---

### OCS-012. Compatibilidad

Toda nueva configuración incorporada al proyecto deberá mantener compatibilidad con la estructura organizacional definida por este documento.

---

### OCS-013. Trazabilidad

Cada configuración deberá poder relacionarse con:

- El módulo que la utiliza.
- El proceso al que pertenece.
- Los recursos afectados.
- Su historial de modificaciones.

---

### OCS-014. Evolución controlada

La incorporación de nuevas configuraciones deberá responder a necesidades funcionales claramente justificadas y documentadas.

---

### OCS-015. Fuente oficial

La arquitectura de configuración definida en este documento constituirá la única referencia oficial para la administración de configuraciones del proyecto.

No se permitirán mecanismos paralelos que contradigan estas reglas.

---

## Objetivos de la organización de la configuración

La organización de la configuración del sistema deberá garantizar:

- Centralización de todas las configuraciones.
- Separación entre configuración y lógica de negocio.
- Reutilización de configuraciones comunes.
- Consistencia estructural.
- Independencia tecnológica.
- Control de cambios.
- Facilidad de mantenimiento.
- Escalabilidad de la arquitectura.
- Trazabilidad completa.
- Evolución controlada del sistema.

---

## 9. Organización de prompts

La organización de prompts establece las reglas oficiales para la administración, ubicación, clasificación y mantenimiento de todos los prompts utilizados por la automatización de búsqueda de empleo.

Su propósito es garantizar que los prompts permanezcan organizados, reutilizables, versionables y desacoplados de la lógica de implementación, facilitando su evolución y asegurando un comportamiento consistente de los componentes que interactúan con modelos de lenguaje.

Todo prompt oficial del proyecto deberá cumplir las disposiciones establecidas en este capítulo.

---

### ORP-001. Repositorio único

Todos los prompts oficiales deberán almacenarse dentro de una estructura única destinada exclusivamente para su administración.

No se permitirá mantener prompts oficiales distribuidos entre distintos componentes del sistema.

---

### ORP-002. Separación de la lógica

Los prompts deberán mantenerse completamente separados de la lógica de implementación.

Los textos utilizados para interactuar con modelos de lenguaje no deberán encontrarse incrustados directamente en los componentes del sistema.

---

### ORP-003. Organización funcional

Los prompts deberán organizarse según el proceso, módulo o responsabilidad funcional para la cual fueron diseñados.

---

### ORP-004. Reutilización

Cuando un mismo prompt pueda ser utilizado por múltiples módulos, deberá existir una única versión oficial compartida.

No deberán mantenerse copias independientes.

---

### ORP-005. Identificación

Todo prompt deberá poseer un identificador único conforme a las convenciones establecidas en el Documento de Estándares del Proyecto.

---

### ORP-006. Versionado

Toda modificación realizada sobre un prompt oficial deberá permitir identificar claramente su versión y conservar el historial correspondiente.

---

### ORP-007. Independencia tecnológica

La organización de los prompts deberá mantenerse independiente del proveedor del modelo de lenguaje, API, herramienta o tecnología utilizada para ejecutarlos.

---

### ORP-008. Clasificación

Los prompts deberán clasificarse según su propósito operativo.

Como mínimo podrán diferenciarse entre:

- Clasificación.
- Extracción.
- Evaluación.
- Generación.
- Validación.
- Corrección.
- Verificación.
- Apoyo operativo.

---

### ORP-009. Variables

Las variables utilizadas por un prompt deberán mantenerse claramente definidas y documentadas.

Su incorporación deberá seguir las convenciones oficiales del proyecto.

---

### ORP-010. Compatibilidad

Todo prompt deberá diseñarse procurando mantener compatibilidad con futuras modificaciones de la automatización.

La incorporación de nuevos módulos no deberá requerir rediseñar los prompts existentes salvo que exista una justificación técnica.

---

### ORP-011. Trazabilidad

Cada prompt deberá poder relacionarse con:

- El módulo que lo utiliza.
- El proceso donde interviene.
- Las entradas requeridas.
- Las salidas esperadas.
- Su historial de modificaciones.

---

### ORP-012. Evolución controlada

La incorporación, modificación o eliminación de prompts deberá documentarse previamente y mantenerse alineada con la arquitectura general del proyecto.

---

### ORP-013. Consistencia

Todos los prompts oficiales deberán mantener una estructura uniforme conforme a las plantillas y estándares definidos por el proyecto.

---

### ORP-014. Auditoría

La utilización de los prompts deberá poder identificarse durante la ejecución de la automatización para facilitar la auditoría y el análisis posterior.

---

### ORP-015. Fuente oficial

La arquitectura definida en este documento constituirá la única referencia oficial para la organización de prompts del proyecto.

No se permitirá utilizar prompts oficiales almacenados fuera de la estructura autorizada.

---

## Objetivos de la organización de prompts

La organización de los prompts deberá garantizar:

- Centralización de todos los prompts oficiales.
- Separación entre prompts y lógica de implementación.
- Reutilización de prompts comunes.
- Versionado controlado.
- Clasificación uniforme.
- Independencia tecnológica.
- Compatibilidad con la evolución del proyecto.
- Trazabilidad completa.
- Facilidad de mantenimiento.
- Consistencia con los estándares oficiales del proyecto.

---

## 10. Organización de datos

La organización de datos establece las reglas oficiales para la administración, almacenamiento y organización de toda la información utilizada, generada o procesada por la automatización de búsqueda de empleo.

Su propósito es garantizar que los datos permanezcan organizados, íntegros, trazables y desacoplados de la lógica de implementación, facilitando su mantenimiento, evolución y reutilización durante todo el ciclo de vida del proyecto.

Todo dato administrado por la automatización deberá cumplir las disposiciones establecidas en este capítulo.

---

### ODT-001. Separación por finalidad

Los datos deberán organizarse según su propósito dentro de la automatización.

Como mínimo deberán diferenciarse entre:

- Datos de entrada.
- Datos en procesamiento.
- Datos persistentes.
- Datos históricos.
- Datos temporales.
- Datos de respaldo.

---

### ODT-002. Separación de la implementación

Los datos deberán mantenerse completamente separados de los componentes responsables de procesarlos.

La organización de los datos no dependerá de la implementación técnica utilizada.

---

### ODT-003. Organización por módulo

Cuando resulte necesario, los datos podrán organizarse por módulo funcional, manteniendo siempre una estructura uniforme en toda la automatización.

---

### ODT-004. Datos compartidos

Los datos utilizados por múltiples módulos deberán administrarse mediante mecanismos centralizados definidos por la arquitectura del sistema.

No deberán mantenerse copias independientes que comprometan su consistencia.

---

### ODT-005. Persistencia

Los datos cuya conservación sea necesaria entre distintas ejecuciones deberán almacenarse utilizando los mecanismos oficiales definidos por el proyecto.

---

### ODT-006. Datos temporales

Los datos temporales deberán mantenerse completamente separados de los datos persistentes.

Su permanencia estará limitada exclusivamente al tiempo necesario para la ejecución correspondiente.

---

### ODT-007. Datos históricos

La información utilizada para auditoría, análisis, trazabilidad o reconstrucción de procesos deberá mantenerse separada de los datos operativos.

---

### ODT-008. Integridad

La organización de los datos deberá preservar permanentemente la integridad, consistencia y confiabilidad de la información administrada por la automatización.

---

### ODT-009. Versionado

Cuando la evolución del proyecto lo requiera, los cambios sobre estructuras de datos deberán poder identificarse y mantenerse bajo control.

---

### ODT-010. Independencia tecnológica

Las reglas definidas en este documento deberán mantenerse independientes del motor de almacenamiento, formato o tecnología utilizada.

---

### ODT-011. Trazabilidad

Todo conjunto de datos deberá poder relacionarse con:

- El módulo que lo genera.
- El proceso que lo utiliza.
- Su origen.
- Su destino.
- Su historial de procesamiento.

---

### ODT-012. Compatibilidad

La organización de los datos deberá facilitar la incorporación de nuevos módulos y nuevos tipos de información sin requerir reorganizaciones significativas.

---

### ODT-013. Conservación

Los datos cuya conservación sea requerida por las políticas del proyecto deberán mantenerse disponibles conforme a las reglas oficiales de almacenamiento y auditoría.

---

### ODT-014. Evolución controlada

Toda modificación significativa en la organización de los datos deberá documentarse previamente y mantenerse alineada con el resto de la arquitectura del proyecto.

---

### ODT-015. Fuente oficial

La organización definida en este documento constituirá la única referencia oficial para la administración y organización de los datos del proyecto.

No se permitirán estructuras paralelas que contradigan estas disposiciones.

---

## Objetivos de la organización de datos

La organización de los datos deberá garantizar:

- Separación clara entre los distintos tipos de datos.
- Independencia respecto de la implementación técnica.
- Integridad y consistencia de la información.
- Reutilización de datos compartidos.
- Escalabilidad de la arquitectura.
- Compatibilidad con nuevos módulos.
- Trazabilidad completa del ciclo de vida de los datos.
- Facilidad de mantenimiento.
- Conservación adecuada de la información.
- Evolución controlada de la arquitectura de datos.

---

## 11. Organización de registros (Logs)

La organización de registros establece las reglas oficiales para la administración, almacenamiento y clasificación de todos los registros generados por la automatización de búsqueda de empleo.

Su propósito es garantizar que los registros permanezcan organizados, accesibles, trazables y consistentes, facilitando el monitoreo, la auditoría, el diagnóstico de errores, el análisis operativo y la evolución del sistema.

Todo registro generado por la automatización deberá cumplir las disposiciones establecidas en este capítulo.

---

### ORL-001. Centralización

Todos los registros oficiales de la automatización deberán almacenarse dentro de una estructura única destinada para dicho propósito.

No se permitirá distribuir registros operativos entre distintos módulos sin una justificación técnica documentada.

---

### ORL-002. Separación por finalidad

Los registros deberán organizarse según su propósito.

Como mínimo deberán diferenciarse entre:

- Registros operativos.
- Registros de auditoría.
- Registros de errores.
- Registros de eventos.
- Registros de ejecución.
- Registros de diagnóstico.

---

### ORL-003. Separación de la implementación

Los registros deberán mantenerse completamente separados de los componentes responsables de generarlos.

La lógica del sistema no dependerá de la ubicación física de los registros.

---

### ORL-004. Organización uniforme

Todos los módulos de la automatización deberán registrar la información siguiendo una estructura uniforme conforme a los estándares oficiales del proyecto.

---

### ORL-005. Trazabilidad

Todo registro deberá permitir identificar, como mínimo:

- Fecha y hora del evento.
- Módulo responsable.
- Proceso asociado.
- Tipo de evento.
- Resultado de la operación.
- Identificador relacionado cuando corresponda.

---

### ORL-006. Integridad

Los registros deberán conservarse íntegros una vez generados.

No podrán modificarse posteriormente salvo mediante procedimientos oficialmente autorizados.

---

### ORL-007. Separación entre registros activos e históricos

Los registros utilizados por la operación diaria deberán mantenerse separados de aquellos conservados exclusivamente para fines históricos o de auditoría.

---

### ORL-008. Compatibilidad

La organización de los registros deberá mantenerse compatible con el Documento 6 — Manejo de Errores y con las convenciones definidas en el Documento 5 — Estándares del Proyecto.

---

### ORL-009. Independencia tecnológica

Las reglas establecidas en este capítulo deberán mantenerse independientes de cualquier herramienta de monitoreo, motor de almacenamiento o tecnología utilizada para implementar los registros.

---

### ORL-010. Conservación

Los registros cuya conservación sea requerida para auditoría, diagnóstico o análisis histórico deberán mantenerse disponibles conforme a las políticas oficiales del proyecto.

---

### ORL-011. Accesibilidad

Los registros deberán organizarse de manera que faciliten su consulta, análisis y recuperación cuando sean requeridos para tareas operativas o de auditoría.

---

### ORL-012. Evolución controlada

Toda modificación en la organización de los registros deberá documentarse previamente y mantenerse alineada con el resto de la arquitectura del proyecto.

---

### ORL-013. Reutilización

Cuando múltiples componentes generen registros equivalentes, deberán utilizar la misma estructura organizacional definida oficialmente.

---

### ORL-014. Consistencia

La clasificación y organización de los registros deberá mantenerse uniforme durante toda la evolución del proyecto.

No podrán coexistir estructuras alternativas para un mismo tipo de registro.

---

### ORL-015. Fuente oficial

La organización definida en este documento constituirá la única referencia oficial para la administración de registros de la automatización.

No se permitirá mantener mecanismos paralelos que contradigan estas disposiciones.

---

## Objetivos de la organización de registros

La organización de los registros deberá garantizar:

- Centralización de todos los registros oficiales.
- Separación entre los distintos tipos de registros.
- Compatibilidad con la auditoría y el manejo de errores.
- Integridad de la información registrada.
- Facilidad de consulta y diagnóstico.
- Independencia tecnológica.
- Trazabilidad completa de la operación.
- Escalabilidad de la arquitectura.
- Facilidad de mantenimiento.
- Evolución controlada del sistema.

---

## 12. Organización de recursos temporales

La organización de recursos temporales establece las reglas oficiales para la administración, almacenamiento y tratamiento de todos los recursos transitorios generados durante la ejecución de la automatización de búsqueda de empleo.

Su propósito es garantizar que los recursos temporales permanezcan aislados de los recursos permanentes, evitando afectar la integridad, organización y mantenibilidad del proyecto.

Todo recurso temporal deberá cumplir las disposiciones establecidas en este capítulo.

---

### ORT-001. Separación física

Todos los recursos temporales deberán almacenarse exclusivamente en las ubicaciones destinadas para dicho propósito.

No podrán mezclarse con recursos permanentes del proyecto.

---

### ORT-002. Carácter transitorio

Todo recurso temporal deberá existir únicamente durante el tiempo necesario para la ejecución del proceso que lo requiera.

---

### ORT-003. Organización por proceso

Cuando resulte necesario conservar recursos temporales durante una ejecución, estos deberán organizarse conforme al proceso o módulo que los haya generado.

---

### ORT-004. Independencia

Los recursos temporales no deberán convertirse en dependencias permanentes de ningún componente de la automatización.

La ejecución normal del sistema no podrá depender de información temporal previamente almacenada.

---

### ORT-005. Regeneración

Todo recurso temporal deberá poder regenerarse automáticamente cuando sea necesario.

La pérdida de un recurso temporal no deberá comprometer la continuidad del proyecto.

---

### ORT-006. Limpieza controlada

Los recursos temporales deberán eliminarse o reutilizarse mediante mecanismos controlados definidos por la arquitectura del sistema.

No deberán acumularse indefinidamente.

---

### ORT-007. Separación de auditoría

Los recursos temporales no deberán utilizarse como mecanismo permanente de auditoría, trazabilidad o almacenamiento histórico.

---

### ORT-008. Compatibilidad

La organización de los recursos temporales deberá mantenerse compatible con las políticas de manejo de errores, recuperación y trazabilidad definidas por el proyecto.

---

### ORT-009. Integridad

La existencia, modificación o eliminación de recursos temporales no deberá afectar la integridad de los datos permanentes ni de la documentación oficial.

---

### ORT-010. Independencia tecnológica

Las reglas establecidas en este capítulo deberán mantenerse independientes de herramientas, formatos o tecnologías específicas.

---

### ORT-011. Identificación

Todo recurso temporal deberá poder relacionarse con:

- El proceso que lo generó.
- El módulo correspondiente.
- La ejecución asociada cuando aplique.
- Su propósito operativo.

---

### ORT-012. Recursos reutilizables

Cuando un recurso temporal pueda reutilizarse durante una misma ejecución sin comprometer la consistencia del sistema, la arquitectura podrá permitir su reutilización controlada.

---

### ORT-013. Evolución controlada

Toda modificación significativa en la organización de los recursos temporales deberá documentarse previamente y mantenerse alineada con el resto de la arquitectura del proyecto.

---

### ORT-014. Consistencia

Todos los módulos deberán seguir las mismas reglas para la generación, utilización y eliminación de recursos temporales.

---

### ORT-015. Fuente oficial

Las disposiciones establecidas en este documento constituirán la única referencia oficial para la organización de recursos temporales dentro de la automatización.

No podrán implementarse mecanismos alternativos que contradigan estas reglas.

---

## Objetivos de la organización de recursos temporales

La organización de los recursos temporales deberá garantizar:

- Separación completa entre recursos temporales y permanentes.
- Eliminación controlada de recursos transitorios.
- Independencia respecto de la implementación técnica.
- Facilidad de mantenimiento.
- Compatibilidad con la recuperación ante errores.
- Integridad de la información permanente.
- Escalabilidad de la arquitectura.
- Organización uniforme entre módulos.
- Trazabilidad de los recursos temporales cuando sea necesaria.
- Evolución controlada de la arquitectura del proyecto.

---

## 13. Organización de scripts y utilidades

La organización de scripts y utilidades establece las reglas oficiales para la administración, almacenamiento y mantenimiento de todos los recursos destinados a apoyar el desarrollo, operación, pruebas, mantenimiento y administración de la automatización de búsqueda de empleo.

Su propósito es garantizar que los scripts y utilidades permanezcan organizados, reutilizables, independientes de la lógica principal del sistema y alineados con la arquitectura oficial del proyecto.

Todo script o utilidad perteneciente al proyecto deberá cumplir las disposiciones establecidas en este capítulo.

---

### OSU-001. Separación funcional

Los scripts y utilidades deberán mantenerse completamente separados de los módulos funcionales de la automatización.

Su existencia no deberá alterar la organización de los componentes principales del sistema.

---

### OSU-002. Propósito específico

Cada script o utilidad deberá cumplir una única responsabilidad claramente definida.

No se permitirá agrupar funciones independientes dentro de un mismo recurso cuando puedan mantenerse de forma separada.

---

### OSU-003. Organización por finalidad

Los scripts y utilidades deberán organizarse según su propósito operativo.

Como mínimo podrán diferenciarse entre:

- Automatización.
- Mantenimiento.
- Migración.
- Conversión.
- Validación.
- Diagnóstico.
- Administración.
- Apoyo al desarrollo.

---

### OSU-004. Reutilización

Todo script que pueda ser utilizado por múltiples procesos deberá mantenerse como un recurso reutilizable.

No deberán existir copias independientes de una misma utilidad.

---

### OSU-005. Independencia de la operación

La automatización deberá poder ejecutar sus procesos principales sin depender obligatoriamente de scripts auxiliares destinados exclusivamente al mantenimiento o administración.

---

### OSU-006. Identificación

Todo script o utilidad deberá poseer una identificación clara que permita reconocer inmediatamente su propósito.

---

### OSU-007. Compatibilidad

Los scripts deberán mantenerse compatibles con las convenciones establecidas por el Documento de Estándares del Proyecto y con la arquitectura general definida en este documento.

---

### OSU-008. Independencia tecnológica

Las reglas de organización establecidas en este capítulo deberán mantenerse independientes del lenguaje de programación o herramienta utilizada para implementar los scripts.

---

### OSU-009. Control de cambios

Toda modificación significativa realizada sobre un script oficial deberá poder identificarse, documentarse y justificarse.

---

### OSU-010. Trazabilidad

Todo script o utilidad deberá poder relacionarse con:

- El proceso que apoya.
- El módulo correspondiente cuando aplique.
- Su propósito operativo.
- Su historial de modificaciones.

---

### OSU-011. Seguridad

Los scripts utilizados para tareas administrativas o de mantenimiento deberán diseñarse evitando afectar la integridad de la información o la estabilidad de la automatización.

---

### OSU-012. Evolución controlada

La incorporación de nuevos scripts deberá responder a una necesidad claramente identificada y documentada.

No se permitirá crear utilidades redundantes que dupliquen funcionalidades existentes.

---

### OSU-013. Consistencia

Todos los scripts oficiales deberán mantener una organización uniforme conforme a las convenciones establecidas por el proyecto.

---

### OSU-014. Eliminación controlada

Los scripts que dejen de utilizarse deberán retirarse de forma controlada, verificando previamente que ningún proceso activo dependa de ellos.

---

### OSU-015. Fuente oficial

La organización definida en este documento constituirá la única referencia oficial para la administración de scripts y utilidades del proyecto.

No podrán mantenerse estructuras paralelas que contradigan estas disposiciones.

---

## Objetivos de la organización de scripts y utilidades

La organización de scripts y utilidades deberá garantizar:

- Separación entre la lógica principal y los recursos auxiliares.
- Organización uniforme por finalidad.
- Reutilización de utilidades comunes.
- Independencia tecnológica.
- Compatibilidad con la arquitectura general.
- Facilidad de mantenimiento.
- Control de cambios.
- Trazabilidad completa.
- Escalabilidad de la arquitectura.
- Evolución controlada de los recursos auxiliares.

---

## 14. Reglas de dependencias entre directorios

Las reglas de dependencias entre directorios establecen el modelo oficial para controlar las relaciones permitidas entre los distintos directorios que conforman la arquitectura de la automatización de búsqueda de empleo.

Su propósito es evitar dependencias innecesarias, reducir el acoplamiento entre componentes y garantizar que la evolución de la estructura del proyecto pueda realizarse de forma controlada y mantenible.

Todo directorio perteneciente a la arquitectura oficial deberá cumplir las disposiciones establecidas en este capítulo.

---

### RDD-001. Dependencias justificadas

Toda dependencia entre directorios deberá responder a una necesidad funcional claramente identificada.

No se permitirán dependencias creadas únicamente por conveniencia de implementación.

---

### RDD-002. Bajo acoplamiento

La arquitectura deberá minimizar las dependencias entre directorios.

Cada componente deberá mantener el mayor nivel posible de independencia respecto de los demás.

---

### RDD-003. Responsabilidad independiente

La existencia de una dependencia no deberá modificar la responsabilidad principal de un directorio.

Cada directorio conservará una única función claramente definida.

---

### RDD-004. Dependencias unidireccionales

Siempre que sea posible, las dependencias deberán mantenerse en un único sentido.

Se evitarán dependencias circulares entre directorios.

---

### RDD-005. Recursos compartidos

Cuando varios directorios requieran utilizar un mismo recurso, este deberá ubicarse en una estructura compartida oficialmente definida.

No deberán establecerse dependencias mediante copias de recursos.

---

### RDD-006. Aislamiento modular

Cada módulo funcional deberá mantener independencia respecto de la estructura interna de los demás módulos.

La interacción entre módulos deberá producirse únicamente mediante los mecanismos definidos por la arquitectura del proyecto.

---

### RDD-007. Dependencias de configuración

Los directorios responsables de la configuración podrán ser utilizados por múltiples componentes, pero las configuraciones no deberán depender de los módulos consumidores.

---

### RDD-008. Dependencias documentales

La documentación podrá hacer referencia a cualquier componente del proyecto sin generar dependencias operativas entre directorios.

---

### RDD-009. Recursos temporales

Los recursos temporales no podrán convertirse en dependencias permanentes de ningún directorio del proyecto.

---

### RDD-010. Independencia tecnológica

Las reglas de dependencias deberán mantenerse independientes del lenguaje de programación, framework o herramienta utilizada para implementar la automatización.

---

### RDD-011. Evolución compatible

La incorporación de nuevos directorios no deberá romper las dependencias previamente definidas ni afectar innecesariamente los componentes existentes.

---

### RDD-012. Eliminación controlada

Antes de eliminar un directorio deberá verificarse que ningún otro componente mantenga dependencias activas hacia él.

---

### RDD-013. Trazabilidad

Toda dependencia entre directorios deberá poder identificarse, justificarse y documentarse.

---

### RDD-014. Consistencia

Las reglas de dependencias deberán aplicarse de manera uniforme en toda la arquitectura del proyecto.

No se permitirán excepciones no documentadas.

---

### RDD-015. Fuente oficial

Las reglas definidas en este documento constituirán la única referencia oficial para la administración de dependencias entre directorios del proyecto.

No podrán establecerse relaciones que contradigan estas disposiciones.

---

## Objetivos de las reglas de dependencias

Las reglas de dependencias entre directorios deberán garantizar:

- Bajo acoplamiento entre componentes.
- Independencia de responsabilidades.
- Eliminación de dependencias circulares.
- Reutilización adecuada de recursos compartidos.
- Escalabilidad de la arquitectura.
- Compatibilidad con nuevos módulos.
- Facilidad de mantenimiento.
- Evolución controlada del proyecto.
- Trazabilidad de las relaciones entre directorios.
- Consistencia estructural de toda la arquitectura.

---

## 15. Reglas para incorporación de nuevos módulos

Las reglas para incorporación de nuevos módulos establecen el procedimiento oficial que deberá seguir cualquier componente funcional que se agregue a la automatización de búsqueda de empleo.

Su propósito es garantizar que la evolución del proyecto conserve la coherencia de la arquitectura, evitando inconsistencias organizacionales, duplicidad de responsabilidades y dependencias innecesarias.

Todo nuevo módulo deberá cumplir las disposiciones establecidas en este capítulo antes de formar parte de la arquitectura oficial del proyecto.

---

### RIM-001. Justificación funcional

Todo nuevo módulo deberá responder a una necesidad funcional claramente identificada y documentada.

No podrán incorporarse módulos cuya responsabilidad ya se encuentre cubierta por otro componente existente.

---

### RIM-002. Responsabilidad única

Cada módulo deberá poseer un único propósito claramente definido.

No se permitirá incorporar módulos con responsabilidades múltiples o ambiguas.

---

### RIM-003. Compatibilidad arquitectónica

Todo nuevo módulo deberá integrarse respetando la arquitectura de carpetas, las convenciones organizacionales y los estándares definidos por el proyecto.

---

### RIM-004. Organización uniforme

Los nuevos módulos deberán adoptar la misma estructura organizacional utilizada por los módulos existentes cuando la naturaleza de sus componentes sea equivalente.

---

### RIM-005. Reutilización

Antes de crear nuevos recursos, deberá verificarse si existen componentes reutilizables dentro de la arquitectura.

No deberán duplicarse funcionalidades ya disponibles.

---

### RIM-006. Dependencias controladas

Las dependencias introducidas por un nuevo módulo deberán mantenerse al mínimo indispensable y respetar las reglas oficiales de dependencias definidas por este documento.

---

### RIM-007. Compatibilidad documental

Todo nuevo módulo deberá incorporarse junto con la actualización de la documentación oficial correspondiente.

La arquitectura física y la documentación deberán mantenerse sincronizadas.

---

### RIM-008. Compatibilidad con los estándares

La incorporación de un nuevo módulo deberá respetar las convenciones de nomenclatura, identificadores, documentación, configuración, registros y demás estándares oficiales del proyecto.

---

### RIM-009. Compatibilidad con el modelo de datos

La incorporación de nuevos recursos no deberá comprometer la integridad, consistencia ni trazabilidad de los datos administrados por la automatización.

---

### RIM-010. Compatibilidad con el manejo de errores

Todo nuevo módulo deberá implementar las políticas oficiales de detección, registro, recuperación y tratamiento de errores definidas en el Documento 6.

---

### RIM-011. Escalabilidad

La incorporación de nuevos módulos no deberá requerir reorganizar significativamente la arquitectura existente.

La estructura deberá permitir el crecimiento progresivo del proyecto.

---

### RIM-012. Validación previa

Antes de aprobar un nuevo módulo deberá verificarse que su incorporación cumple todas las reglas arquitectónicas definidas por la documentación oficial.

---

### RIM-013. Trazabilidad

Toda incorporación de un nuevo módulo deberá documentar:

- Su propósito.
- Su alcance.
- Sus responsabilidades.
- Sus dependencias.
- Los documentos afectados.
- La fecha de incorporación.

---

### RIM-014. Evolución controlada

Toda incorporación deberá aprobarse formalmente antes de integrarse a la arquitectura oficial del proyecto.

Las modificaciones posteriores deberán seguir el mismo procedimiento.

---

### RIM-015. Fuente oficial

Las reglas establecidas en este documento constituirán el único procedimiento oficial para incorporar nuevos módulos a la automatización.

No podrán añadirse componentes que contradigan estas disposiciones.

---

## Objetivos de la incorporación de nuevos módulos

Las reglas para incorporación de nuevos módulos deberán garantizar:

- Crecimiento ordenado de la arquitectura.
- Compatibilidad con toda la documentación oficial.
- Uniformidad organizacional.
- Reutilización de componentes existentes.
- Bajo acoplamiento entre módulos.
- Escalabilidad del proyecto.
- Facilidad de mantenimiento.
- Integridad de la arquitectura.
- Trazabilidad de las incorporaciones.
- Evolución controlada de la automatización.

---

## 16. Restricciones de la arquitectura de carpetas

Las siguientes restricciones establecen los límites oficiales que deberán respetarse durante el diseño, implementación, mantenimiento y evolución de la arquitectura de carpetas de la automatización de búsqueda de empleo.

Su propósito es preservar la consistencia de la organización del proyecto, evitar desviaciones arquitectónicas y garantizar que toda modificación futura mantenga compatibilidad con la documentación oficial.

Todas las restricciones definidas en este capítulo serán de cumplimiento obligatorio para cualquier componente, módulo, recurso o ampliación del proyecto.

---

### RAP-001. Arquitectura única

No podrá coexistir más de una arquitectura oficial de carpetas para un mismo proyecto.

Toda la organización deberá ajustarse a la estructura definida por este documento.

---

### RAP-002. Directorios sin propósito

No podrán crearse directorios cuya responsabilidad no se encuentre claramente definida y documentada.

---

### RAP-003. Duplicidad organizacional

No podrán existir múltiples directorios destinados a almacenar el mismo tipo de recurso cuando una única ubicación resulte suficiente.

---

### RAP-004. Mezcla de responsabilidades

No se permitirá almacenar recursos pertenecientes a categorías funcionales distintas dentro de un mismo directorio cuando existan ubicaciones específicas para cada una.

---

### RAP-005. Dependencias circulares

No podrán establecerse dependencias circulares entre módulos, directorios o componentes de la arquitectura.

---

### RAP-006. Dependencias implícitas

La arquitectura no podrá depender de estructuras de carpetas no documentadas o creadas dinámicamente sin formar parte de la organización oficial del proyecto.

---

### RAP-007. Modificaciones no documentadas

Ninguna modificación significativa de la arquitectura podrá realizarse sin la correspondiente actualización de la documentación oficial.

---

### RAP-008. Recursos fuera de la arquitectura

Los recursos pertenecientes al proyecto no podrán almacenarse fuera de la estructura oficial definida por esta arquitectura, salvo casos excepcionales previamente aprobados y documentados.

---

### RAP-009. Acoplamiento excesivo

La organización de la arquitectura no podrá obligar a que un módulo conozca la estructura interna de otros módulos para cumplir sus responsabilidades.

---

### RAP-010. Dependencia tecnológica

La organización de carpetas no podrá diseñarse en función de herramientas, frameworks, lenguajes o proveedores específicos.

La arquitectura deberá conservar su validez aun cuando la implementación tecnológica cambie.

---

### RAP-011. Configuración distribuida

No se permitirá mantener configuraciones equivalentes distribuidas innecesariamente entre distintos componentes del proyecto.

---

### RAP-012. Recursos temporales permanentes

Los recursos temporales no podrán convertirse en almacenamiento permanente ni formar parte de la estructura estable del proyecto.

---

### RAP-013. Eliminación sin validación

No podrá eliminarse ningún directorio, archivo o recurso oficial sin verificar previamente que no existan dependencias activas hacia él.

---

### RAP-014. Inconsistencia documental

La arquitectura física y la documentación oficial no podrán evolucionar de forma independiente.

Toda modificación deberá mantenerse sincronizada entre ambas.

---

### RAP-015. Incumplimiento de estándares

No podrá incorporarse ningún recurso, módulo o componente que incumpla las convenciones establecidas por el Documento de Estándares del Proyecto y las disposiciones definidas en este documento.

---

## Restricciones generales

La arquitectura de carpetas deberá respetar las siguientes restricciones generales:

- Existirá una única arquitectura oficial.
- No se permitirá duplicidad de responsabilidades.
- No existirán dependencias circulares.
- Toda modificación deberá documentarse.
- La arquitectura permanecerá independiente de la tecnología utilizada.
- Los recursos deberán mantenerse dentro de la estructura oficial.
- La documentación y la arquitectura deberán evolucionar conjuntamente.
- Los recursos temporales permanecerán separados de los permanentes.
- Todo nuevo componente deberá respetar las reglas arquitectónicas oficiales.
- Ninguna excepción podrá aplicarse sin la correspondiente justificación y aprobación documental.

---

## 17. Criterios de aceptación

Los presentes criterios de aceptación establecen las condiciones que deberá cumplir la arquitectura de carpetas para considerarse conforme con la documentación oficial del proyecto.

Su propósito es proporcionar un conjunto uniforme de verificaciones que permitan validar la correcta organización de la estructura física de la automatización antes de su aprobación, implementación o modificación.

El cumplimiento de estos criterios será obligatorio para todos los módulos, componentes y recursos incorporados al proyecto.

---

### CAP-001. Organización uniforme

La arquitectura deberá mantener una organización consistente en todos sus directorios y recursos, conforme a las reglas definidas en este documento.

---

### CAP-002. Responsabilidades claramente definidas

Cada directorio y recurso deberá poseer una única responsabilidad claramente identificable.

No deberán existir ambigüedades funcionales.

---

### CAP-003. Separación de responsabilidades

La arquitectura deberá mantener una separación clara entre:

- Documentación.
- Configuración.
- Prompts.
- Datos.
- Registros.
- Recursos temporales.
- Scripts y utilidades.
- Componentes funcionales.

---

### CAP-004. Cumplimiento de estándares

Toda la arquitectura deberá respetar las convenciones establecidas por el Documento de Estándares del Proyecto.

---

### CAP-005. Compatibilidad documental

La estructura física deberá mantenerse completamente alineada con la documentación oficial del proyecto.

No deberán existir diferencias entre ambas.

---

### CAP-006. Escalabilidad

La arquitectura deberá permitir incorporar nuevos módulos sin requerir reorganizaciones significativas de la estructura existente.

---

### CAP-007. Independencia tecnológica

La organización de la arquitectura no deberá depender de tecnologías, herramientas o proveedores específicos.

---

### CAP-008. Bajo acoplamiento

Las dependencias entre directorios deberán mantenerse al mínimo necesario y respetar las reglas oficiales de la arquitectura.

---

### CAP-009. Trazabilidad

La ubicación de cada recurso deberá permitir identificar fácilmente:

- Su propósito.
- El módulo correspondiente.
- Su relación con otros componentes.
- La documentación asociada.

---

### CAP-010. Integridad

La arquitectura deberá preservar la integridad organizacional del proyecto evitando duplicidades, inconsistencias o dependencias no autorizadas.

---

### CAP-011. Evolución controlada

Toda modificación deberá encontrarse previamente documentada, justificada y aprobada antes de incorporarse oficialmente a la arquitectura.

---

### CAP-012. Compatibilidad con nuevos componentes

Todo nuevo módulo, recurso o directorio deberá poder incorporarse respetando completamente las reglas establecidas en este documento.

---

### CAP-013. Consistencia global

La arquitectura deberá mantener uniformidad organizacional entre todos los módulos de la automatización.

---

### CAP-014. Auditabilidad

La organización de la arquitectura deberá facilitar la revisión, auditoría y verificación de cualquier recurso perteneciente al proyecto.

---

### CAP-015. Cumplimiento integral

La arquitectura únicamente podrá considerarse aprobada cuando cumpla simultáneamente todos los criterios establecidos en este capítulo.

---

## Verificación de aceptación

La arquitectura de carpetas será considerada conforme cuando:

- Mantenga una organización uniforme.
- Exista una única responsabilidad por directorio.
- Se respete la separación de recursos.
- Cumpla los estándares oficiales del proyecto.
- Mantenga independencia tecnológica.
- Permita el crecimiento ordenado de la automatización.
- Evite dependencias innecesarias.
- Facilite la trazabilidad de todos los recursos.
- Mantenga coherencia con la documentación oficial.
- Cumpla íntegramente las disposiciones definidas en este documento.

---

## 18. Índice de la arquitectura de carpetas

El presente índice constituye la estructura oficial del **Documento 7 – Arquitectura de Carpetas**.

Su propósito es facilitar la consulta, navegación, mantenimiento y trazabilidad de todos los apartados que conforman la arquitectura organizacional del proyecto.

---

# Índice

## 1. Propósito del documento

Define el objetivo, alcance y obligatoriedad de la arquitectura de carpetas.

---

## 2. Principios de la arquitectura de carpetas

Establece los principios generales que deberán regir toda la organización física del proyecto.

---

## 3. Estructura general del proyecto

Define la organización conceptual de la arquitectura y la separación de responsabilidades.

---

## 4. Organización de directorios

Establece las reglas oficiales para la organización jerárquica de los directorios del proyecto.

---

## 5. Organización de archivos

Define las reglas para la organización de los archivos y la arquitectura conceptual del proyecto.

---

## 6. Convenciones de ubicación de recursos

Establece los criterios oficiales para determinar la ubicación de todos los recursos de la automatización.

---

## 7. Organización de la documentación

Define la estructura oficial para la administración y organización de toda la documentación del proyecto.

---

## 8. Organización de la configuración del sistema

Establece las reglas para organizar y administrar todas las configuraciones de la automatización.

---

## 9. Organización de prompts

Define la arquitectura oficial para la organización, reutilización y mantenimiento de los prompts.

---

## 10. Organización de datos

Establece las reglas para organizar la información utilizada y generada por la automatización.

---

## 11. Organización de registros (Logs)

Define la arquitectura para la organización de registros operativos, auditoría, eventos y diagnóstico.

---

## 12. Organización de recursos temporales

Establece las reglas para la administración de recursos transitorios generados durante la ejecución.

---

## 13. Organización de scripts y utilidades

Define la organización oficial de los recursos auxiliares utilizados para el desarrollo, mantenimiento y administración del proyecto.

---

## 14. Reglas de dependencias entre directorios

Establece las reglas que controlan las relaciones permitidas entre los distintos directorios de la arquitectura.

---

## 15. Reglas para incorporación de nuevos módulos

Define el procedimiento oficial para incorporar nuevos módulos sin afectar la consistencia de la arquitectura.

---

## 16. Restricciones de la arquitectura de carpetas

Establece los límites y prohibiciones que deberán respetarse durante toda la evolución del proyecto.

---

## 17. Criterios de aceptación

Define las condiciones objetivas que deberá cumplir la arquitectura para considerarse conforme con la documentación oficial.

---

## 18. Índice de la arquitectura de carpetas

Presenta la estructura oficial del documento y facilita su consulta como referencia normativa.

---

# Referencias normativas

La arquitectura de carpetas deberá mantenerse permanentemente alineada con los siguientes documentos oficiales del proyecto:

- Documento 0 — Glosario del Proyecto.
- Documento 1 — Requisitos Funcionales.
- Documento 2 — Requisitos No Funcionales.
- Documento 3 — Modelo de Decisiones.
- Documento 4 — Flujo de Datos.
- Documento 5 — Estándares del Proyecto.
- Documento 6 — Manejo de Errores.

Toda modificación realizada sobre la arquitectura deberá conservar la compatibilidad con estos documentos y con cualquier actualización oficial aprobada posteriormente.
