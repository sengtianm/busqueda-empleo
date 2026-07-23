# Documento 4

# Flujo de Datos

# 1. Propósito del documento

El presente documento define el modelo oficial del flujo de datos de la automatización de búsqueda de empleo.

Su propósito es establecer cómo deberá ingresar, transformarse, validarse, almacenarse, consultarse y conservarse toda la información utilizada por la automatización durante el procesamiento de las ofertas de empleo, garantizando la consistencia, integridad, trazabilidad y disponibilidad de los datos en cada etapa del flujo funcional.

Este documento determina el recorrido completo de la información desde el momento en que una oferta es descubierta en una fuente de empleo hasta que finaliza completamente su ciclo de vida dentro del sistema, incluyendo todas las transformaciones, validaciones, estados, persistencia y relaciones entre los distintos componentes de la automatización.

Asimismo, constituye la referencia oficial para el diseño, implementación, validación y evolución de la arquitectura de datos del proyecto, asegurando que todos los módulos intercambien información de manera uniforme, controlada y compatible con los Requisitos Funcionales, los Requisitos No Funcionales, el Modelo de Decisiones y el Glosario del Proyecto.

Las disposiciones contenidas en este documento serán de cumplimiento obligatorio para todos los componentes que generen, consuman, transformen, almacenen, consulten o actualicen información dentro de la automatización.

---

# 2. Principios del flujo de datos

Los siguientes principios establecen las condiciones que deberán cumplir todos los flujos de información utilizados por la automatización durante el descubrimiento, preparación, evaluación, procesamiento, gestión y seguimiento de las ofertas de empleo.

Estos principios complementan los Requisitos Funcionales, los Requisitos No Funcionales y el Modelo de Decisiones, constituyendo los lineamientos obligatorios para el diseño, implementación, validación y evolución del flujo de datos del sistema.

---

### PFD-001. Integridad de los datos

Toda información deberá conservar su integridad durante el procesamiento.

Ninguna transformación podrá alterar, eliminar o corromper la información original obtenida desde las fuentes de empleo, salvo cuando exista una regla de negocio previamente documentada que lo autorice.

---

### PFD-002. Trazabilidad completa

Todo dato deberá poder rastrearse desde su origen hasta su estado final dentro de la automatización.

La trazabilidad deberá permitir reconstruir el recorrido completo de la información, incluyendo transformaciones, validaciones, decisiones, cambios de estado y persistencia.

---

### PFD-003. Flujo controlado

Toda información deberá recorrer únicamente los procesos definidos por el flujo funcional del proyecto.

No se permitirán movimientos, transformaciones o accesos a datos que no se encuentren previamente documentados.

---

### PFD-004. Consistencia

Los datos deberán mantenerse coherentes entre todos los módulos de la automatización.

No podrán existir versiones incompatibles, registros contradictorios ni diferencias injustificadas entre la información utilizada por los distintos componentes del sistema.

---

### PFD-005. Validación previa

Todo dato recibido desde una fuente externa o generado durante el procesamiento deberá superar las validaciones correspondientes antes de ser utilizado por procesos posteriores.

Ningún componente podrá asumir que una entrada es válida sin verificarla previamente.

---

### PFD-006. Separación de responsabilidades

Cada etapa del flujo de datos deberá realizar únicamente las transformaciones y operaciones que correspondan a su responsabilidad funcional.

Las actividades de captura, transformación, validación, evaluación, almacenamiento y consulta deberán permanecer conceptualmente independientes.

---

### PFD-007. Persistencia controlada

Toda información que deba conservarse para garantizar la operación, la trazabilidad, la auditoría o el reprocesamiento deberá almacenarse mediante los mecanismos definidos por la arquitectura del proyecto.

La persistencia deberá preservar tanto la información original como la información derivada cuando corresponda.

---

### PFD-008. Reproducibilidad

Las mismas entradas, procesadas bajo las mismas reglas y configuraciones, deberán producir los mismos datos de salida.

El flujo de datos deberá ser determinístico y evitar comportamientos inconsistentes.

---

### PFD-009. Independencia tecnológica

La definición del flujo de datos deberá mantenerse independiente de la tecnología utilizada para implementarlo.

Su funcionamiento no dependerá de un lenguaje de programación, base de datos, proveedor o herramienta específica.

---

### PFD-010. Evolución controlada

Toda modificación al flujo de datos deberá documentarse previamente y preservar la compatibilidad con el resto de la documentación oficial del proyecto.

La incorporación de nuevos datos, transformaciones o procesos no deberá alterar el comportamiento esperado de los componentes existentes sin una justificación documentada.

---

### PFD-011. Disponibilidad de la información

La información deberá permanecer disponible para los procesos que la requieran durante todo su ciclo de vida, respetando las reglas de acceso, persistencia y conservación definidas por el proyecto.

---

### PFD-012. Unicidad de la información

Cada dato deberá tener una única fuente de verdad dentro de la automatización.

No se permitirá mantener copias inconsistentes de la misma información cuando exista un mecanismo oficial para consultarla o reconstruirla.

---

### PFD-013. Minimización de duplicidad

El flujo de datos deberá evitar la generación de información duplicada siempre que sea posible.

Cuando por razones funcionales existan datos redundantes, deberá mantenerse la sincronización y trazabilidad entre ellos.

---

### PFD-014. Protección del dato original

La información obtenida directamente desde las fuentes de empleo deberá conservarse sin modificaciones.

Las normalizaciones, enriquecimientos y transformaciones deberán realizarse sobre estructuras derivadas, preservando siempre el dato original para futuras auditorías o reprocesamientos.

---

### PFD-015. Coherencia con el flujo funcional

Todo movimiento de información deberá respetar el flujo funcional, el ciclo de vida de las ofertas, el modelo de decisiones y los estados definidos para la automatización.

Ningún dato podrá utilizarse en procesos incompatibles con su estado o nivel de procesamiento.

---

# 3. Arquitectura del flujo de datos

La arquitectura del flujo de datos define la estructura conceptual mediante la cual la información circula, se transforma, se valida, se almacena y se consulta dentro de la automatización de búsqueda de empleo.

Su propósito es establecer un recorrido uniforme, controlado y trazable para todos los datos gestionados por el sistema, garantizando que cada componente interactúe con la información de forma consistente y respetando las responsabilidades definidas para cada etapa del procesamiento.

La arquitectura del flujo de datos constituye un componente transversal de la automatización y será utilizada por todos los módulos del sistema sin depender de una implementación tecnológica específica.

Su funcionamiento se basa en un flujo secuencial compuesto por la recepción de datos, validación, transformación, persistencia, consumo, actualización y conservación de la información.

---

## 3.1 Componentes del flujo de datos

El flujo de datos estará conformado por los siguientes componentes conceptuales:

### AFD-001. Origen de los datos

Corresponde a todas las fuentes autorizadas desde las cuales la automatización obtiene información.

Entre otras, podrán incluirse:

- Plataformas de empleo.
- Configuración del usuario.
- Perfil profesional.
- Reglas de negocio.
- Configuraciones del sistema.
- Información histórica.
- Decisiones del usuario.

Todo dato deberá identificar claramente su origen antes de incorporarse al flujo de procesamiento.

---

### AFD-002. Recepción de datos

Componente encargado de incorporar la información proveniente de las fuentes autorizadas.

Entre sus responsabilidades se encuentran:

- Recibir la información.
- Identificar el origen.
- Asociar metadatos básicos.
- Preparar los datos para su validación.

La recepción no modifica el contenido de la información obtenida.

---

### AFD-003. Validación de datos

Componente responsable de verificar que la información recibida cumple las condiciones necesarias para continuar el procesamiento.

Entre sus responsabilidades se encuentran:

- Verificar integridad.
- Validar estructura.
- Detectar inconsistencias.
- Identificar información incompleta.
- Confirmar compatibilidad con el proceso correspondiente.

La validación no transforma la información; únicamente determina su aptitud para continuar el flujo.

---

### AFD-004. Transformación de datos

Componente encargado de convertir la información validada a las estructuras utilizadas internamente por la automatización.

Entre sus responsabilidades se encuentran:

- Normalizar formatos.
- Completar información derivada cuando corresponda.
- Estructurar los datos.
- Generar información intermedia.
- Preparar la información para los procesos funcionales.

Las transformaciones deberán preservar siempre el dato original.

---

### AFD-005. Persistencia de datos

Componente encargado de almacenar la información necesaria para garantizar la operación, la trazabilidad, el historial y los reprocesamientos del sistema.

Entre sus responsabilidades se encuentran:

- Almacenar datos originales.
- Almacenar datos transformados.
- Registrar estados.
- Registrar decisiones.
- Registrar eventos.
- Conservar el historial.

---

### AFD-006. Consumo de datos

Componente responsable de suministrar la información requerida por los diferentes módulos de la automatización.

Entre sus responsabilidades se encuentran:

- Recuperar información.
- Verificar disponibilidad.
- Entregar únicamente los datos necesarios para cada proceso.
- Garantizar la consistencia de la información consultada.

---

### AFD-007. Actualización de datos

Componente encargado de registrar los cambios producidos durante el procesamiento de una oferta.

Entre sus responsabilidades se encuentran:

- Actualizar estados.
- Incorporar nuevos resultados.
- Registrar nuevas evaluaciones.
- Asociar documentos generados.
- Mantener sincronizadas las estructuras de información.

Toda actualización deberá conservar el historial correspondiente.

---

### AFD-008. Registro y trazabilidad

Componente encargado de conservar toda la información necesaria para reconstruir posteriormente el recorrido completo de los datos.

Como mínimo deberá registrar:

- Origen de la información.
- Transformaciones realizadas.
- Validaciones ejecutadas.
- Procesos que utilizaron los datos.
- Cambios de estado.
- Decisiones relacionadas.
- Fecha y hora de cada evento.
- Responsable del cambio cuando corresponda.

---

## 3.2 Flujo conceptual de los datos

Toda información gestionada por la automatización seguirá el siguiente flujo conceptual:

1. Recepción de información desde una fuente autorizada.
2. Identificación del origen de los datos.
3. Validación de la información recibida.
4. Transformación y normalización cuando corresponda.
5. Almacenamiento de la información.
6. Consumo por los módulos funcionales autorizados.
7. Actualización de la información durante el procesamiento.
8. Registro completo de todas las operaciones para garantizar la trazabilidad y la auditoría.

---

## 3.3 Responsabilidades del flujo de datos

El flujo de datos será responsable de:

- Incorporar información desde fuentes autorizadas.
- Validar la calidad de los datos.
- Transformar la información conforme a las reglas definidas.
- Garantizar la disponibilidad de los datos para cada proceso.
- Mantener la consistencia entre módulos.
- Registrar el historial completo de la información.
- Preservar la trazabilidad durante todo el ciclo de vida de las ofertas.
- Facilitar los reprocesamientos cuando sean autorizados.

---

## 3.4 Responsabilidades fuera del alcance

El flujo de datos no tendrá como responsabilidad:

- Tomar decisiones funcionales o estratégicas.
- Aplicar reglas de negocio propias del modelo de decisiones.
- Modificar el perfil profesional del usuario.
- Determinar prioridades o clasificaciones.
- Ejecutar procesos funcionales distintos de la gestión de la información.

---

# 4. Entradas del flujo de datos

Las entradas del flujo de datos corresponden al conjunto de información que puede incorporarse a la automatización para iniciar o apoyar el procesamiento de las ofertas de empleo.

Toda entrada deberá provenir de una fuente autorizada, encontrarse correctamente identificada y superar las validaciones correspondientes antes de incorporarse al flujo de información.

El flujo de datos no podrá utilizar información cuyo origen no pueda determinarse, que no haya sido validada o que sea incompatible con el estado actual del procesamiento.

---

## EFD-001. Información de ofertas de empleo

Corresponde a la información obtenida desde las fuentes de empleo durante el proceso de descubrimiento.

Podrá incluir, entre otros:

- Título del cargo.
- Empresa.
- Descripción.
- Responsabilidades.
- Requisitos.
- Beneficios.
- Salario.
- Modalidad.
- Ubicación.
- Tipo de contrato.
- Fecha de publicación.
- Plataforma de origen.
- URL.
- Identificadores asociados.

Esta información constituye la principal entrada del flujo de datos.

---

## EFD-002. Perfil profesional del usuario

Corresponde a la información profesional utilizada durante la evaluación de compatibilidad y la generación de insumos.

Podrá incluir:

- Experiencia laboral.
- Competencias técnicas.
- Competencias profesionales.
- Formación académica.
- Certificaciones.
- Idiomas.
- Preferencias laborales.
- Expectativa salarial.
- Modalidad de trabajo preferida.
- Ubicación.
- Empresas objetivo.
- Empresas restringidas.

---

## EFD-003. Configuración del sistema

Corresponde a los parámetros operativos que determinan el comportamiento de la automatización.

Podrá incluir:

- Configuraciones generales.
- Parámetros de ejecución.
- Configuración de módulos.
- Frecuencias de procesamiento.
- Configuración de flujos.
- Variables de operación.

---

## EFD-004. Reglas de negocio

Corresponde al conjunto de reglas utilizadas por la automatización para controlar el procesamiento de la información.

Podrá incluir:

- Reglas de evaluación.
- Reglas de aceptación.
- Reglas de descarte.
- Reglas de priorización.
- Umbrales.
- Restricciones.
- Casos especiales.
- Excepciones.

---

## EFD-005. Información histórica

Corresponde a la información generada durante ejecuciones anteriores y que resulte necesaria para continuar el procesamiento.

Podrá incluir:

- Historial de ofertas.
- Historial de evaluaciones.
- Historial de decisiones.
- Historial de estados.
- Documentos generados.
- Registros de ejecución.
- Métricas relevantes.

---

## EFD-006. Decisiones del usuario

Corresponde a las decisiones estratégicas registradas por el usuario que puedan afectar el flujo de datos.

Podrá incluir:

- Aprobaciones.
- Descartes manuales.
- Reprocesamientos autorizados.
- Cambios de prioridad.
- Actualizaciones del perfil profesional.
- Modificaciones autorizadas sobre configuraciones o reglas.

---

## EFD-007. Datos generados por la automatización

Corresponde a toda la información producida internamente durante el procesamiento de una oferta.

Podrá incluir:

- Resultados intermedios.
- Datos normalizados.
- Clasificaciones.
- Puntuaciones.
- Análisis.
- Documentos generados.
- Estados del procesamiento.
- Estados operativos.

Estos datos podrán convertirse en entradas para procesos posteriores dentro del mismo flujo de información.

---

## Principios generales de las entradas

Toda entrada incorporada al flujo de datos deberá cumplir las siguientes condiciones:

- Provenir de una fuente autorizada.
- Ser identificable de forma única.
- Mantener información sobre su origen.
- Superar las validaciones correspondientes antes de ser utilizada.
- Conservar su integridad durante todo el procesamiento.
- Mantener compatibilidad con el estado actual del flujo funcional.
- Permanecer disponible para auditorías y reprocesamientos cuando sea necesario.
- Respetar las reglas de seguridad, trazabilidad y persistencia definidas para el proyecto.

---

# 5. Transformaciones de datos

Las transformaciones de datos corresponden al conjunto de operaciones mediante las cuales la automatización convierte la información recibida desde las fuentes autorizadas en estructuras consistentes, normalizadas y aptas para ser utilizadas durante los diferentes procesos funcionales.

Su propósito es garantizar que todos los módulos trabajen sobre información uniforme, preservando siempre la integridad del dato original y manteniendo la trazabilidad completa de cada transformación realizada.

Toda transformación deberá ejecutarse únicamente después de que la información haya superado las validaciones correspondientes.

---

## TFD-001. Conservación del dato original

Toda transformación deberá preservar íntegramente la información original obtenida desde la fuente de empleo.

Las modificaciones, normalizaciones o enriquecimientos deberán realizarse sobre estructuras derivadas, sin alterar el contenido original.

---

## TFD-002. Normalización de formatos

La automatización deberá convertir los datos recibidos a formatos internos estandarizados.

Podrán normalizarse, entre otros:

- Fechas.
- Horas.
- Ubicaciones.
- Modalidades de trabajo.
- Tipos de contrato.
- Salarios.
- Monedas.
- Identificadores.
- Estructuras de texto.

---

## TFD-003. Estandarización de estructuras

La información deberá organizarse utilizando estructuras uniformes que faciliten su utilización por todos los módulos de la automatización.

La estructura interna deberá mantenerse consistente independientemente de la fuente de origen.

---

## TFD-004. Enriquecimiento de información

Cuando las reglas del proyecto lo permitan, la automatización podrá generar información derivada a partir de los datos disponibles.

Entre otros ejemplos:

- Cálculo de campos derivados.
- Clasificaciones preliminares.
- Identificadores internos.
- Metadatos de procesamiento.
- Relaciones entre entidades.

El enriquecimiento nunca sustituirá la información original.

---

## TFD-005. Eliminación de redundancias funcionales

Durante las transformaciones podrán eliminarse duplicidades que no aporten valor al procesamiento interno, siempre que dicha operación no implique pérdida de información relevante ni afecte la trazabilidad.

---

## TFD-006. Asociación de metadatos

Durante el proceso de transformación podrán incorporarse metadatos necesarios para controlar el procesamiento de la información.

Entre otros:

- Fecha y hora de incorporación.
- Fuente de origen.
- Identificador interno.
- Versión del procesamiento.
- Estado inicial.
- Información de trazabilidad.

---

## TFD-007. Generación de estructuras derivadas

La automatización podrá generar nuevas estructuras de datos destinadas exclusivamente al funcionamiento interno del sistema.

Estas estructuras podrán utilizarse para:

- Evaluaciones.
- Análisis.
- Reportes.
- Historial.
- Auditoría.
- Gestión del procesamiento.

Toda estructura derivada deberá mantener relación con la información que le dio origen.

---

## TFD-008. Compatibilidad entre transformaciones

Las transformaciones deberán producir resultados compatibles con los módulos que consumirán posteriormente la información.

Ninguna transformación podrá generar estructuras incompatibles con las interfaces oficiales definidas por la automatización.

---

## TFD-009. Reproducibilidad de las transformaciones

Las mismas entradas, procesadas bajo las mismas reglas y configuraciones, deberán generar exactamente las mismas transformaciones.

Las operaciones deberán ser determinísticas y completamente reproducibles.

---

## TFD-010. Registro de transformaciones

Toda transformación realizada sobre la información deberá registrarse como parte del historial del flujo de datos.

Como mínimo deberá conservarse la siguiente información:

- Identificador del dato.
- Transformación aplicada.
- Fecha y hora.
- Responsable de la transformación (sistema).
- Resultado obtenido.
- Relación con la información original.

---

## Principios generales de las transformaciones

Todas las transformaciones de datos deberán cumplir los siguientes principios:

- Preservar la información original.
- Mantener consistencia entre módulos.
- Ser completamente trazables.
- Ser reproducibles.
- Basarse en reglas documentadas.
- Mantener independencia tecnológica.
- Evitar pérdida de información.
- Facilitar futuras ampliaciones del flujo de datos.
- Depender de una tecnología, base de datos o herramienta específica para su funcionamiento.

---

# 6. Validaciones de datos

Las validaciones de datos corresponden al conjunto de verificaciones que la automatización deberá realizar sobre toda la información incorporada al flujo de datos antes de permitir su utilización por los procesos funcionales del sistema.

Su propósito es garantizar que la información utilizada durante el procesamiento sea íntegra, consistente, suficiente y compatible con el estado actual de la oferta, reduciendo el riesgo de errores, inconsistencias y decisiones incorrectas.

Ningún dato podrá avanzar a la siguiente etapa del flujo si no ha superado las validaciones correspondientes o si no existe una regla documentada que autorice su tratamiento como caso especial o excepción.

---

## VFD-001. Validación del origen

Toda información deberá provenir de una fuente previamente autorizada por la automatización.

No podrán incorporarse datos cuyo origen no pueda identificarse o verificarse.

---

## VFD-002. Validación de integridad

La automatización deberá verificar que la información recibida conserve su integridad durante todo el proceso de incorporación al flujo de datos.

No deberán detectarse pérdidas, alteraciones o corrupciones de la información.

---

## VFD-003. Validación de estructura

Los datos deberán cumplir la estructura esperada para cada tipo de información antes de continuar el procesamiento.

Las estructuras incompatibles deberán tratarse conforme a las reglas de manejo de excepciones.

---

## VFD-004. Validación de obligatoriedad

La automatización deberá comprobar que los campos clasificados como obligatorios se encuentren disponibles cuando sean requeridos por el proceso correspondiente.

La ausencia de información obligatoria deberá gestionarse mediante las reglas de negocio definidas para estos casos.

---

## VFD-005. Validación de consistencia

La información deberá mantenerse coherente entre sus diferentes elementos.

No deberán existir datos contradictorios que impidan una interpretación confiable de la oferta o del proceso en ejecución.

---

## VFD-006. Validación de compatibilidad

La información deberá ser compatible con el estado actual del ciclo de vida de la oferta y con el proceso funcional que pretende utilizarla.

No podrán emplearse datos pertenecientes a etapas incompatibles del flujo funcional.

---

## VFD-007. Validación de duplicidad

La automatización deberá identificar información duplicada cuando dicha duplicidad pueda afectar el procesamiento.

La detección de duplicados deberá seguir las reglas definidas para la gestión de ofertas equivalentes.

---

## VFD-008. Validación de relaciones

La automatización deberá verificar que las relaciones entre los diferentes datos del sistema permanezcan válidas y consistentes.

Entre otras:

- Oferta ↔ Historial.
- Oferta ↔ Evaluaciones.
- Oferta ↔ Estados.
- Oferta ↔ Documentos.
- Oferta ↔ Decisiones.

---

## VFD-009. Validación previa al consumo

Antes de que un módulo utilice información almacenada, deberá verificarse que dicha información continúe siendo válida para el proceso correspondiente.

Cuando exista información obsoleta, incompleta o incompatible, deberán aplicarse las reglas definidas antes de continuar.

---

## VFD-010. Registro de validaciones

Toda validación realizada deberá registrarse como parte del historial del flujo de datos.

Como mínimo deberá conservarse la siguiente información:

- Identificador del dato.
- Validación ejecutada.
- Resultado obtenido.
- Fecha y hora.
- Responsable de la validación (sistema).
- Acción realizada cuando la validación no sea satisfactoria.

---

## Principios generales de las validaciones

Todas las validaciones de datos deberán cumplir los siguientes principios:

- Ejecutarse antes del consumo de la información.
- Basarse en reglas previamente documentadas.
- Ser objetivas y reproducibles.
- Mantener trazabilidad completa.
- Preservar la integridad de los datos.
- Detectar inconsistencias oportunamente.
- Mantener independencia tecnológica.
- Permitir la incorporación de nuevas validaciones sin afectar las existentes.

---

# 7. Salidas del flujo de datos

Las salidas del flujo de datos corresponden al conjunto de información generada por la automatización como resultado de los procesos de validación, transformación, evaluación, procesamiento, gestión y seguimiento de las ofertas de empleo.

Su propósito es proporcionar información estructurada, consistente y trazable para apoyar el funcionamiento de los diferentes módulos de la automatización, facilitar la toma de decisiones del usuario y garantizar la conservación del conocimiento generado durante el procesamiento.

Toda salida deberá mantener relación con la información que le dio origen y cumplir las reglas de integridad, trazabilidad y persistencia definidas por el proyecto.

---

## SFD-001. Información estructurada de la oferta

Corresponde a la versión normalizada y preparada de la oferta de empleo, lista para ser utilizada por los diferentes procesos de la automatización.

Podrá incluir, entre otros:

- Información validada.
- Campos normalizados.
- Identificadores internos.
- Metadatos de procesamiento.
- Relaciones internas.

Esta estructura constituirá la principal fuente de información para los procesos posteriores.

---

## SFD-002. Resultados de la evaluación

Corresponde a la información generada durante la evaluación inicial y el procesamiento profundo de la oferta.

Podrá incluir:

- Puntuaciones.
- Niveles de compatibilidad.
- Prioridades.
- Clasificaciones.
- Resultados parciales.
- Resultados finales.
- Justificaciones.

---

## SFD-003. Información derivada

Corresponde a toda información generada por la automatización a partir de los datos originales.

Entre otros ejemplos:

- Datos enriquecidos.
- Campos calculados.
- Relaciones generadas.
- Indicadores internos.
- Metadatos adicionales.

La información derivada deberá mantener siempre su relación con el dato original.

---

## SFD-004. Estados del procesamiento

Corresponde a la información utilizada para controlar el avance de cada oferta dentro del flujo funcional.

Podrá incluir:

- Estado del ciclo de vida.
- Estado operativo.
- Fecha de actualización.
- Responsable del cambio.
- Historial de transiciones.

---

## SFD-005. Recursos para la candidatura

Corresponde a los documentos, análisis e insumos generados por la automatización para apoyar la preparación de una candidatura.

Podrán incluir:

- Análisis estratégicos.
- Información organizada.
- Documentos asociados.
- Recursos definidos durante el desarrollo del proyecto.

Cada recurso deberá mantener su relación con la oferta correspondiente.

---

## SFD-006. Información para consulta

Corresponde a la información organizada para facilitar la consulta por parte del usuario y de los módulos de gestión.

Podrá incluir:

- Historial completo.
- Estado actual.
- Resultados de evaluaciones.
- Documentos generados.
- Decisiones registradas.
- Métricas relevantes.

---

## SFD-007. Registros operativos

Corresponde a la información utilizada para garantizar la observabilidad, auditoría y seguimiento del funcionamiento de la automatización.

Podrá incluir:

- Eventos.
- Registros de ejecución.
- Validaciones realizadas.
- Transformaciones ejecutadas.
- Errores.
- Advertencias.
- Métricas.
- Decisiones automáticas.
- Decisiones del usuario.

---

## Principios generales de las salidas

Toda salida generada por el flujo de datos deberá cumplir las siguientes condiciones:

- Mantener relación con la información que le dio origen.
- Conservar trazabilidad completa.
- Mantener consistencia con el estado actual del procesamiento.
- Encontrarse disponible para los procesos autorizados.
- Preservar la integridad de la información.
- Cumplir las reglas de persistencia definidas para el proyecto.
- Mantener compatibilidad con los demás módulos de la automatización.
- Poder utilizarse en auditorías, consultas y reprocesamientos cuando sea necesario.

---

# 8. Persistencia de datos

La persistencia de datos define las reglas mediante las cuales la automatización conservará la información generada y utilizada durante el procesamiento de las ofertas de empleo.

Su propósito es garantizar la disponibilidad, integridad, consistencia y trazabilidad de la información durante todo el ciclo de vida de cada oferta, permitiendo su consulta, auditoría, reprocesamiento y utilización por los diferentes componentes del sistema.

Toda información cuya conservación resulte necesaria para el funcionamiento de la automatización deberá almacenarse conforme a las reglas establecidas en este documento.

---

## PDD-001. Persistencia de la información original

Toda información obtenida desde una fuente de empleo deberá conservarse íntegramente como registro original.

La información original no podrá eliminarse ni sobrescribirse como consecuencia de las transformaciones realizadas por la automatización.

---

## PDD-002. Persistencia de la información derivada

Toda información generada durante las diferentes etapas del procesamiento podrá almacenarse cuando sea necesaria para el funcionamiento del sistema, la trazabilidad, la auditoría o futuros reprocesamientos.

La información derivada deberá mantener siempre su relación con los datos que le dieron origen.

---

## PDD-003. Persistencia del historial

La automatización deberá conservar el historial completo de cada oferta durante todo su ciclo de vida.

El historial deberá incluir, como mínimo:

- Cambios de estado.
- Validaciones.
- Transformaciones.
- Evaluaciones.
- Decisiones.
- Reprocesamientos.
- Eventos relevantes.

---

## PDD-004. Persistencia de configuraciones

Las configuraciones utilizadas por la automatización deberán mantenerse almacenadas de forma que permitan reproducir el comportamiento del sistema bajo las mismas condiciones.

Las modificaciones realizadas sobre configuraciones críticas deberán conservar su correspondiente historial.

---

## PDD-005. Persistencia de documentos

Todo documento, análisis o recurso generado durante el procesamiento deberá conservar su relación con la oferta correspondiente.

La persistencia deberá permitir identificar fácilmente el origen, la versión y el momento de generación de cada recurso.

---

## PDD-006. Persistencia de registros operativos

Los registros utilizados para auditoría, observabilidad y diagnóstico deberán almacenarse de forma que permitan reconstruir completamente la ejecución de los procesos.

Entre otros podrán conservarse:

- Eventos.
- Errores.
- Advertencias.
- Métricas.
- Validaciones.
- Transformaciones.
- Decisiones.

---

## PDD-007. Conservación de relaciones

La persistencia deberá preservar las relaciones existentes entre los diferentes elementos del sistema.

Entre otras:

- Oferta ↔ Historial.
- Oferta ↔ Evaluaciones.
- Oferta ↔ Estados.
- Oferta ↔ Documentos.
- Oferta ↔ Decisiones.
- Oferta ↔ Registros.

Ninguna relación podrá perderse durante el almacenamiento de la información.

---

## PDD-008. Disponibilidad de la información persistida

La información almacenada deberá permanecer disponible para los procesos autorizados durante todo el tiempo definido por las políticas de conservación del proyecto.

Su consulta no deberá alterar el contenido almacenado.

---

## PDD-009. Reutilización de la información

Cuando una información previamente persistida continúe siendo válida, la automatización deberá reutilizarla antes de generar nuevamente datos equivalentes.

Este principio busca reducir procesamiento innecesario y evitar duplicidad de información.

---

## PDD-010. Registro de operaciones de persistencia

Toda operación relevante de almacenamiento o actualización deberá registrarse como parte del historial del sistema.

Como mínimo deberá conservarse la siguiente información:

- Identificador del dato.
- Operación realizada.
- Fecha y hora.
- Responsable de la operación (sistema o usuario).
- Resultado obtenido.
- Estado final del almacenamiento.

---

## Principios generales de la persistencia

La persistencia de datos deberá cumplir los siguientes principios:

- Preservar la integridad de la información.
- Mantener la trazabilidad completa.
- Conservar el historial de las ofertas.
- Evitar pérdida de información.
- Mantener consistencia entre los datos almacenados.
- Facilitar auditorías y reprocesamientos.
- Mantener independencia respecto de la tecnología utilizada para el almacenamiento.
- Favorecer la reutilización de información previamente validada.

---

# 9. Estados de los datos durante el procesamiento

Los estados de los datos representan la condición en la que se encuentra la información durante su recorrido por el flujo de datos de la automatización.

Su propósito es controlar el nivel de procesamiento, disponibilidad y confiabilidad de la información en cada etapa del flujo funcional, garantizando que los diferentes módulos utilicen únicamente datos compatibles con el proceso que ejecutan.

Los estados definidos en este capítulo corresponden al estado de la información y no sustituyen el ciclo de vida ni el estado operativo de las ofertas de empleo definidos en otros documentos del proyecto.

---

## EPD-001. Recibido

Corresponde a la información que ha sido incorporada desde una fuente autorizada y se encuentra pendiente de validación.

Características:

- Origen identificado.
- Información original preservada.
- Pendiente de validaciones.
- No disponible para procesos funcionales.

---

## EPD-002. Validado

Corresponde a la información que ha superado satisfactoriamente las validaciones definidas para su incorporación al flujo de datos.

Características:

- Integridad verificada.
- Estructura validada.
- Consistencia comprobada.
- Disponible para transformación.

---

## EPD-003. Transformado

Corresponde a la información que ha sido normalizada y adaptada a las estructuras internas utilizadas por la automatización.

Características:

- Formato estandarizado.
- Información derivada generada cuando corresponda.
- Dato original preservado.
- Disponible para los procesos funcionales.

---

## EPD-004. Persistido

Corresponde a la información almacenada conforme a las reglas de persistencia del sistema.

Características:

- Disponible para consultas.
- Disponible para auditorías.
- Disponible para reprocesamientos.
- Conserva su historial.

---

## EPD-005. En uso

Corresponde a la información que está siendo utilizada activamente por uno o más procesos autorizados de la automatización.

Características:

- Asociada a un proceso funcional.
- Disponible para consumo controlado.
- Protegida frente a modificaciones incompatibles durante su utilización.

---

## EPD-006. Actualizado

Corresponde a la información que ha incorporado nuevos resultados o modificaciones derivadas del procesamiento autorizado.

Características:

- Historial actualizado.
- Relaciones preservadas.
- Nueva versión registrada cuando corresponda.
- Disponible para los siguientes procesos del flujo funcional.

---

## EPD-007. Histórico

Corresponde a la información que ya no representa la versión vigente, pero debe conservarse para garantizar la trazabilidad y la auditoría.

Características:

- No se elimina.
- Mantiene relación con la versión vigente.
- Disponible para consultas históricas.
- Disponible para reprocesamientos autorizados.

---

## EPD-008. Archivado

Corresponde a la información cuyo procesamiento ha finalizado y que se conserva únicamente conforme a las políticas de conservación definidas por el proyecto.

Características:

- Procesamiento finalizado.
- Consulta permitida.
- Sin modificaciones operativas.
- Conservación para auditoría e historial.

---

## EPD-009. Inconsistente

Corresponde a la información que presenta problemas de integridad, estructura, consistencia o compatibilidad y que no puede continuar el flujo normal hasta que se aplique la estrategia correspondiente.

Características:

- Procesamiento suspendido.
- Pendiente de resolución.
- No disponible para consumo funcional.
- Sujeta a validación, corrección o manejo de excepciones.

---

## EPD-010. Obsoleto

Corresponde a la información que ha sido reemplazada por una versión más reciente y que ya no debe utilizarse durante el procesamiento normal.

Características:

- Conservación obligatoria para trazabilidad.
- No utilizada como fuente vigente.
- Disponible para auditorías.
- Relacionada con la versión que la reemplazó.

---

## Principios generales de los estados de los datos

Los estados de los datos deberán cumplir los siguientes principios:

- Un dato únicamente podrá encontrarse en un estado vigente a la vez.
- Todo cambio de estado deberá registrarse como parte del historial del sistema.
- Los estados deberán ser consistentes con el flujo funcional y el procesamiento realizado.
- Ningún dato podrá utilizarse en un proceso incompatible con su estado.
- Las transiciones entre estados deberán respetar las reglas documentadas del flujo de datos.
- Los estados históricos deberán conservarse para garantizar la trazabilidad y la auditoría.
- Los estados deberán mantenerse independientes de la tecnología utilizada para implementar la automatización.

---

# 10. Trazabilidad del flujo de datos

La trazabilidad del flujo de datos establece los mecanismos mediante los cuales la automatización registrará, conservará y podrá reconstruir el recorrido completo de la información durante todo el ciclo de vida de una oferta de empleo.

Su propósito es garantizar la transparencia del procesamiento, facilitar auditorías, permitir reprocesamientos y demostrar cómo cada dato fue incorporado, validado, transformado, utilizado, actualizado y conservado por la automatización.

Toda información gestionada por el flujo de datos deberá mantener la evidencia necesaria para reconstruir completamente su historial.

---

## TRD-001. Identificación única de los datos

Todo dato incorporado al flujo deberá contar con un identificador único e inmutable que permita seguir su recorrido durante todo el procesamiento.

Este identificador deberá mantenerse independientemente de las transformaciones, actualizaciones o reprocesamientos realizados.

---

## TRD-002. Registro del origen

La automatización deberá conservar el origen de toda la información incorporada al flujo de datos.

Como mínimo deberá registrarse:

- Fuente de origen.
- Fecha y hora de incorporación.
- Identificador de la fuente cuando exista.
- Proceso responsable de la incorporación.

---

## TRD-003. Registro de transformaciones

Toda transformación realizada sobre la información deberá quedar registrada como un evento trazable.

El registro deberá permitir identificar:

- Información original.
- Transformación aplicada.
- Resultado obtenido.
- Fecha y hora.
- Responsable de la transformación.

---

## TRD-004. Registro de validaciones

Toda validación ejecutada sobre los datos deberá conservar su resultado como parte del historial del procesamiento.

Entre otros elementos podrán registrarse:

- Validación aplicada.
- Resultado obtenido.
- Regla utilizada.
- Acción ejecutada cuando corresponda.
- Fecha y hora.

---

## TRD-005. Registro del consumo de datos

La automatización deberá conservar evidencia de los procesos que utilicen información persistida durante la ejecución de los diferentes módulos.

Este registro permitirá identificar qué componentes consumieron determinada información y con qué propósito.

---

## TRD-006. Registro de actualizaciones

Toda actualización realizada sobre la información deberá generar un nuevo evento dentro del historial.

Como mínimo deberá registrarse:

- Estado anterior.
- Estado resultante.
- Información modificada.
- Fecha y hora.
- Responsable de la actualización.
- Justificación cuando corresponda.

---

## TRD-007. Conservación del historial

La automatización deberá conservar el historial completo del recorrido de cada dato.

El historial no podrá eliminarse ni sobrescribirse durante el ciclo de vida de la oferta.

---

## TRD-008. Reconstrucción del flujo

La información registrada deberá ser suficiente para reconstruir completamente el recorrido seguido por cualquier dato dentro de la automatización.

La reconstrucción deberá permitir identificar:

- Cómo ingresó la información.
- Qué validaciones superó.
- Qué transformaciones recibió.
- Qué procesos la utilizaron.
- Qué actualizaciones experimentó.
- Cuál fue su estado final.

---

## TRD-009. Disponibilidad para auditoría

La información utilizada para garantizar la trazabilidad deberá permanecer disponible durante el periodo de conservación definido por el proyecto.

Las consultas de auditoría no deberán modificar el estado de los datos ni afectar el funcionamiento de la automatización.

---

## TRD-010. Versionado del flujo de datos

Toda información relevante deberá asociarse a la versión vigente de las reglas, configuraciones y procesos utilizados durante su tratamiento.

Esto permitirá reproducir el comportamiento histórico del flujo de datos aun cuando el sistema evolucione posteriormente.

---

## Principios generales de la trazabilidad

La trazabilidad del flujo de datos deberá cumplir los siguientes principios:

- Registrar todo el recorrido de la información.
- Mantener identificadores únicos e inmutables.
- Preservar el historial completo.
- Permitir la reconstrucción del procesamiento.
- Facilitar auditorías y reprocesamientos.
- Garantizar la reproducibilidad del flujo de datos.
- Mantener independencia respecto de la tecnología utilizada para su implementación.
- Preservar la integridad de la información histórica.

---

# 11. Integridad y consistencia de los datos

La integridad y la consistencia de los datos establecen las reglas que deberá cumplir toda la información gestionada por la automatización para garantizar que permanezca correcta, completa, coherente y confiable durante todo el ciclo de vida de las ofertas de empleo.

Su propósito es asegurar que todos los módulos de la automatización trabajen sobre información válida, evitando inconsistencias, pérdidas de datos, contradicciones o alteraciones que puedan afectar el procesamiento, las decisiones o la trazabilidad del sistema.

La integridad y la consistencia deberán preservarse desde la incorporación de los datos hasta su conservación final.

---

## ICD-001. Conservación de la integridad

Toda información deberá mantener su contenido íntegro durante todas las etapas del flujo de datos.

Ningún proceso podrá alterar, eliminar o corromper información sin que exista una regla previamente documentada que lo autorice.

---

## ICD-002. Consistencia entre módulos

La información utilizada por los diferentes módulos de la automatización deberá mantenerse coherente y sincronizada.

No podrán existir diferencias incompatibles entre los datos utilizados por distintos procesos para representar una misma información.

---

## ICD-003. Unicidad de la información

Cada dato deberá tener una única representación oficial dentro del sistema.

Cuando existan estructuras derivadas o copias funcionales, deberá mantenerse la relación con la fuente oficial para evitar inconsistencias.

---

## ICD-004. Conservación de relaciones

Las relaciones existentes entre los diferentes elementos de información deberán mantenerse durante todo el procesamiento.

Entre otras:

- Oferta ↔ Información original.
- Oferta ↔ Información transformada.
- Oferta ↔ Historial.
- Oferta ↔ Evaluaciones.
- Oferta ↔ Decisiones.
- Oferta ↔ Documentos.
- Oferta ↔ Registros operativos.

---

## ICD-005. Consistencia temporal

La información deberá mantener coherencia respecto al momento en que fue generada, modificada o utilizada.

Toda actualización deberá registrarse cronológicamente para preservar la secuencia real de los acontecimientos.

---

## ICD-006. Protección frente a inconsistencias

Cuando se detecte información inconsistente, la automatización deberá impedir que continúe el procesamiento hasta aplicar las reglas correspondientes de validación, caso especial o manejo de excepciones.

No deberán generarse resultados basados en información cuya consistencia no haya sido verificada.

---

## ICD-007. Conservación durante actualizaciones

Las actualizaciones realizadas sobre la información no deberán provocar pérdida del historial ni afectar la consistencia de los datos previamente registrados.

Toda modificación deberá preservar las versiones necesarias para garantizar la trazabilidad.

---

## ICD-008. Consistencia durante reprocesamientos

Cuando una oferta sea reprocesada, la automatización deberá garantizar que la nueva información permanezca consistente con el historial existente.

El reprocesamiento no deberá generar contradicciones entre las diferentes versiones registradas.

---

## ICD-009. Verificación permanente

La automatización podrá ejecutar verificaciones de integridad y consistencia durante cualquier etapa del flujo de datos cuando resulte necesario para garantizar la calidad de la información.

Estas verificaciones deberán ejecutarse sin alterar el contenido de los datos.

---

## ICD-010. Registro de incidencias

Toda incidencia relacionada con la integridad o consistencia de los datos deberá registrarse como parte del historial del sistema.

Como mínimo deberá conservarse:

- Identificador del dato.
- Tipo de incidencia.
- Descripción.
- Fecha y hora.
- Acción aplicada.
- Resultado obtenido.
- Responsable de la resolución cuando corresponda.

---

## Principios generales de la integridad y consistencia

La integridad y consistencia de los datos deberán cumplir los siguientes principios:

- Preservar la información durante todo su ciclo de vida.
- Mantener coherencia entre todos los módulos de la automatización.
- Evitar contradicciones y pérdidas de información.
- Mantener trazabilidad completa.
- Facilitar auditorías y reprocesamientos.
- Basarse en reglas previamente documentadas.
- Mantener independencia respecto de la tecnología utilizada para su implementación.
- Garantizar la confiabilidad de la información utilizada por el sistema.

---

# 12. Manejo de reprocesamientos

El manejo de reprocesamientos establece las reglas mediante las cuales la automatización podrá volver a procesar total o parcialmente la información asociada a una oferta de empleo previamente registrada.

Su propósito es garantizar que los reprocesamientos se ejecuten de forma controlada, preservando la integridad de la información, la trazabilidad del historial y la consistencia del flujo de datos, evitando duplicidades, pérdidas de información o resultados contradictorios.

Todo reprocesamiento deberá ejecutarse únicamente cuando exista una condición previamente documentada que lo justifique.

---

## MRD-001. Autorización del reprocesamiento

Todo reprocesamiento deberá estar respaldado por una regla de negocio documentada o por una decisión explícita del usuario cuando así lo requiera el modelo de decisiones.

No podrán ejecutarse reprocesamientos arbitrarios.

---

## MRD-002. Conservación de la información existente

El reprocesamiento no deberá eliminar, sobrescribir ni alterar la información previamente registrada.

Toda nueva información deberá incorporarse preservando el historial existente.

---

## MRD-003. Reutilización de información válida

Antes de generar nuevamente información, la automatización deberá determinar si existen datos previamente persistidos que continúen siendo válidos para el nuevo procesamiento.

Cuando sea posible, dichos datos deberán reutilizarse para evitar operaciones innecesarias y mantener la consistencia del sistema.

---

## MRD-004. Revalidación de la información

Durante un reprocesamiento, la automatización deberá ejecutar nuevamente las validaciones que resulten necesarias para garantizar que la información continúe siendo válida bajo las condiciones actuales del sistema.

---

## MRD-005. Regeneración de información derivada

Cuando el reprocesamiento modifique información utilizada para generar datos derivados, la automatización deberá recalcular únicamente los elementos afectados, preservando aquellos que continúen siendo válidos.

---

## MRD-006. Actualización de relaciones

Toda modificación producida durante el reprocesamiento deberá mantener actualizadas las relaciones entre la información original, la información derivada, los documentos generados, las evaluaciones y el historial correspondiente.

---

## MRD-007. Conservación del historial

Cada reprocesamiento deberá registrarse como un nuevo evento dentro del historial de la oferta.

Las ejecuciones anteriores deberán conservarse íntegramente para permitir auditorías y reconstrucciones posteriores.

---

## MRD-008. Consistencia posterior al reprocesamiento

Finalizado el reprocesamiento, la automatización deberá verificar que toda la información resultante permanezca consistente con:

- El flujo funcional.
- El modelo de decisiones.
- Las reglas de negocio.
- El estado actual de la oferta.
- La información previamente registrada.

---

## MRD-009. Registro del reprocesamiento

Toda ejecución de un reprocesamiento deberá registrar, como mínimo:

- Identificador de la oferta.
- Motivo del reprocesamiento.
- Información reutilizada.
- Información recalculada.
- Fecha y hora.
- Responsable del reprocesamiento (sistema o usuario).
- Resultado obtenido.

---

## MRD-010. Finalización del reprocesamiento

Una vez concluido el reprocesamiento, la información resultante deberá incorporarse nuevamente al flujo de datos respetando las reglas de validación, persistencia, trazabilidad y consistencia definidas en este documento.

---

## Principios generales del manejo de reprocesamientos

El manejo de reprocesamientos deberá cumplir los siguientes principios:

- Basarse exclusivamente en reglas documentadas o autorizaciones válidas.
- Preservar toda la información histórica.
- Evitar duplicidad innecesaria de información.
- Reutilizar los datos válidos siempre que sea posible.
- Mantener la integridad y consistencia del flujo de datos.
- Garantizar la trazabilidad completa de cada reprocesamiento.
- Mantener independencia respecto de la tecnología utilizada para su implementación.
- Facilitar futuras reevaluaciones y evoluciones del sistema.

---

# 13. Restricciones del flujo de datos

Las restricciones del flujo de datos establecen los límites que deberán respetarse durante el diseño, implementación, operación y evolución de todos los procesos relacionados con la gestión de la información dentro de la automatización.

Su propósito es garantizar que el flujo de datos permanezca alineado con los objetivos del proyecto, preservando la integridad de la información, la consistencia del procesamiento, la trazabilidad y la compatibilidad con el resto de la documentación oficial.

Estas restricciones serán de cumplimiento obligatorio para todos los componentes que generen, transformen, validen, consuman, almacenen o actualicen información dentro del sistema.

---

## RFD-001. Origen autorizado de los datos

La automatización únicamente podrá incorporar información proveniente de fuentes previamente autorizadas por el proyecto.

No podrán procesarse datos cuyo origen no pueda identificarse o verificarse.

---

## RFD-002. Protección del dato original

La información obtenida desde las fuentes de empleo no podrá modificarse, eliminarse ni sobrescribirse durante el procesamiento.

Toda transformación deberá realizarse sobre estructuras derivadas que mantengan la relación con la información original.

---

## RFD-003. Prohibición de pérdida de información

Ningún proceso del flujo de datos podrá provocar la pérdida de información necesaria para garantizar la operación, la trazabilidad, la auditoría o los reprocesamientos.

Toda eliminación autorizada deberá encontrarse documentada y preservar el historial correspondiente.

---

## RFD-004. Consumo exclusivo de información validada

Los módulos de la automatización únicamente podrán utilizar información que haya superado las validaciones correspondientes o cuyo tratamiento haya sido autorizado mediante las reglas de casos especiales o manejo de excepciones.

---

## RFD-005. Respeto por el flujo funcional

Toda circulación de información deberá respetar el flujo funcional oficial de la automatización.

No podrán utilizarse datos pertenecientes a etapas incompatibles ni ejecutarse procesos fuera de la secuencia definida por el proyecto.

---

## RFD-006. Conservación de la trazabilidad

Toda operación realizada sobre la información deberá conservar la evidencia necesaria para reconstruir posteriormente el recorrido completo de los datos.

No podrán ejecutarse operaciones que impidan la reconstrucción del historial.

---

## RFD-007. Restricción de duplicidad

La automatización deberá evitar la generación innecesaria de información duplicada.

Cuando existan copias funcionales o estructuras derivadas, deberá mantenerse la sincronización y la relación con la fuente oficial de la información.

---

## RFD-008. Configuración centralizada

Las reglas relacionadas con el flujo de datos deberán administrarse mediante mecanismos centralizados.

No deberán existir configuraciones incompatibles o distribuidas que alteren el comportamiento uniforme del sistema.

---

## RFD-009. Independencia tecnológica

El comportamiento del flujo de datos no deberá depender de un lenguaje de programación, una base de datos, un proveedor, un servicio o una herramienta específica.

La implementación tecnológica no podrá modificar el significado ni las reglas del flujo de información.

---

## RFD-010. Compatibilidad documental

Toda modificación realizada sobre el flujo de datos deberá preservar la compatibilidad con:

- El Glosario del Proyecto.
- Los Requisitos Funcionales.
- Los Requisitos No Funcionales.
- El Modelo de Decisiones.
- El Flujo Funcional.
- El Ciclo de Vida de las Ofertas.
- La documentación oficial vigente del proyecto.

Cuando una modificación rompa dicha compatibilidad, deberá documentarse y aprobarse antes de su implementación.

---

## Principios generales de las restricciones

Las restricciones del flujo de datos deberán cumplir los siguientes principios:

- Preservar la integridad de la información.
- Mantener la consistencia del flujo de datos.
- Garantizar la trazabilidad completa.
- Evitar comportamientos no documentados.
- Favorecer la mantenibilidad y escalabilidad del sistema.
- Mantener independencia respecto de la tecnología utilizada para su implementación.
- Garantizar la compatibilidad con toda la documentación oficial del proyecto.

---

# 14. Criterios de aceptación

El flujo de datos se considerará aprobado cuando se verifique, mediante evidencia objetiva, que cumple los principios, reglas, restricciones y comportamientos definidos en el presente documento.

Los siguientes criterios de aceptación servirán como referencia para validar el diseño, la implementación, las pruebas y la evolución del flujo de datos de la automatización.

---

### CFD-001. Incorporación de datos

Toda información deberá incorporarse únicamente desde fuentes autorizadas y correctamente identificadas.

No deberán procesarse datos cuyo origen no pueda verificarse.

---

### CFD-002. Validación correcta de la información

Toda información utilizada por la automatización deberá haber superado las validaciones definidas para el proceso correspondiente o haber sido tratada conforme a las reglas documentadas para casos especiales o excepciones.

---

### CFD-003. Correcta transformación de los datos

Las transformaciones deberán producir estructuras consistentes, reproducibles y compatibles con los módulos que consumen la información.

El dato original deberá permanecer íntegro.

---

### CFD-004. Persistencia adecuada

Toda información cuya conservación sea necesaria para la operación, trazabilidad, auditoría o reprocesamiento deberá almacenarse conforme a las reglas definidas en este documento.

---

### CFD-005. Correcta gestión de estados

Los datos deberán transitar únicamente por estados compatibles con el flujo funcional y las reglas del proyecto.

No deberán existir estados inconsistentes o incompatibles.

---

### CFD-006. Conservación de la integridad

La información deberá mantener su integridad durante todo el ciclo de vida del procesamiento.

No deberán producirse pérdidas, alteraciones no autorizadas ni corrupciones de datos.

---

### CFD-007. Consistencia entre módulos

Los diferentes componentes de la automatización deberán utilizar información consistente y sincronizada.

No deberán existir diferencias incompatibles entre los datos compartidos por distintos módulos.

---

### CFD-008. Correcta gestión de reprocesamientos

Los reprocesamientos deberán preservar el historial, reutilizar la información válida cuando corresponda y mantener la consistencia del flujo de datos.

---

### CFD-009. Trazabilidad completa

La automatización deberá conservar la información necesaria para reconstruir completamente el recorrido de cualquier dato.

La reconstrucción deberá permitir identificar:

- Su origen.
- Las validaciones realizadas.
- Las transformaciones aplicadas.
- Los procesos que utilizaron la información.
- Las actualizaciones realizadas.
- Su estado final.

---

### CFD-010. Auditabilidad

Toda operación relevante realizada sobre los datos deberá poder justificarse mediante evidencia objetiva registrada durante el procesamiento.

La información almacenada deberá ser suficiente para realizar auditorías técnicas y funcionales.

---

### CFD-011. Reproducibilidad

El flujo de datos deberá producir los mismos resultados cuando procese las mismas entradas utilizando las mismas reglas, configuraciones y versión del sistema.

---

### CFD-012. Compatibilidad documental

El flujo de datos deberá mantenerse completamente alineado con:

- El Glosario del Proyecto.
- Los Requisitos Funcionales.
- Los Requisitos No Funcionales.
- El Modelo de Decisiones.
- El Flujo Funcional.
- El Ciclo de Vida de las Ofertas.
- La documentación oficial vigente del proyecto.

---

### CFD-013. Escalabilidad

La incorporación de nuevas fuentes de datos, transformaciones, validaciones o procesos deberá realizarse sin afectar el comportamiento de los componentes existentes, salvo cuando dicha modificación haya sido previamente documentada y aprobada.

---

### CFD-014. Independencia tecnológica

El comportamiento del flujo de datos deberá mantenerse independiente de la tecnología utilizada para su implementación.

La sustitución de herramientas, servicios o componentes tecnológicos no deberá modificar las reglas definidas en este documento.

---

### CFD-015. Cumplimiento integral

El flujo de datos cumplirá este documento cuando todos los criterios anteriores puedan verificarse mediante pruebas, revisiones documentales o evidencias obtenidas durante la operación de la automatización.

---

## Principio general de aceptación

La aprobación del flujo de datos requerirá demostrar que toda la información gestionada por la automatización es:

- Íntegra.
- Consistente.
- Reproducible.
- Trazable.
- Auditable.
- Basada en fuentes autorizadas.
- Compatible con el resto de la documentación oficial del proyecto.

---

# 15. Índice del flujo de datos

El presente documento organiza sus elementos mediante identificadores únicos e inmutables, con el fin de facilitar su consulta, implementación, trazabilidad, auditoría y mantenimiento.

Cada identificador constituye una referencia oficial del flujo de datos y podrá utilizarse en la documentación, la arquitectura, el desarrollo, las pruebas y la operación de la automatización.

Los identificadores definidos en este documento no deberán reutilizarse, modificarse ni reasignarse una vez el documento haya sido aprobado.

---

## Índice de principios del flujo de datos

| Rango | Categoría |
|--------|-----------|
| PFD-001 – PFD-015 | Principios del flujo de datos |

---

## Índice de arquitectura del flujo de datos

| Rango | Categoría |
|--------|-----------|
| AFD-001 – AFD-008 | Componentes del flujo de datos |

---

## Índice de entradas del flujo de datos

| Rango | Categoría |
|--------|-----------|
| EFD-001 – EFD-007 | Entradas del flujo de datos |

---

## Índice de transformaciones de datos

| Rango | Categoría |
|--------|-----------|
| TFD-001 – TFD-010 | Transformaciones de datos |

---

## Índice de validaciones de datos

| Rango | Categoría |
|--------|-----------|
| VFD-001 – VFD-010 | Validaciones de datos |

---

## Índice de salidas del flujo de datos

| Rango | Categoría |
|--------|-----------|
| SFD-001 – SFD-007 | Salidas del flujo de datos |

---

## Índice de persistencia de datos

| Rango | Categoría |
|--------|-----------|
| PDD-001 – PDD-010 | Persistencia de datos |

---

## Índice de estados de los datos

| Rango | Categoría |
|--------|-----------|
| EPD-001 – EPD-010 | Estados de los datos durante el procesamiento |

---

## Índice de trazabilidad del flujo de datos

| Rango | Categoría |
|--------|-----------|
| TFD-001 – TFD-010 | Trazabilidad del flujo de datos |

> **Nota:** Aunque ambos grupos utilizan el prefijo **TFD**, pertenecen a capítulos distintos del documento. Durante la implementación se recomienda utilizar el identificador completo (capítulo + código) o adoptar un prefijo diferenciado (por ejemplo, **TRD** para Trazabilidad del Flujo de Datos) para evitar ambigüedades.

---

## Índice de integridad y consistencia de los datos

| Rango | Categoría |
|--------|-----------|
| ICD-001 – ICD-010 | Integridad y consistencia de los datos |

---

## Índice de manejo de reprocesamientos

| Rango | Categoría |
|--------|-----------|
| MRD-001 – MRD-010 | Manejo de reprocesamientos |

---

## Índice de restricciones del flujo de datos

| Rango | Categoría |
|--------|-----------|
| RFD-001 – RFD-010 | Restricciones del flujo de datos |

---

## Índice de criterios de aceptación

| Rango | Categoría |
|--------|-----------|
| CFD-001 – CFD-015 | Criterios de aceptación |

---

## Resumen del documento

| Capítulo | Contenido |
|----------|-----------|
| 1 | Propósito del documento |
| 2 | Principios del flujo de datos |
| 3 | Arquitectura del flujo de datos |
| 4 | Entradas del flujo de datos |
| 5 | Transformaciones de datos |
| 6 | Validaciones de datos |
| 7 | Salidas del flujo de datos |
| 8 | Persistencia de datos |
| 9 | Estados de los datos durante el procesamiento |
| 10 | Trazabilidad del flujo de datos |
| 11 | Integridad y consistencia de los datos |
| 12 | Manejo de reprocesamientos |
| 13 | Restricciones del flujo de datos |
| 14 | Criterios de aceptación |
| 15 | Índice del flujo de datos |

---

## Principios del índice

El índice del flujo de datos deberá cumplir los siguientes principios:

- Mantener identificadores únicos e inmutables.
- Facilitar la navegación y consulta del documento.
- Servir como referencia oficial para la implementación del flujo de datos.
- Permitir la trazabilidad entre documentación, arquitectura, desarrollo y pruebas.
- Facilitar la incorporación de nuevos elementos sin alterar los identificadores existentes.
- Mantener consistencia con el resto de la documentación oficial del proyecto.
