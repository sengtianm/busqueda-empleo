# Documento 3 - Modelo de Decisiones

# 1. Propósito del documento

El presente documento define el modelo de decisiones de la automatización de búsqueda de empleo.

Su propósito es establecer los principios, reglas, criterios, mecanismos y restricciones que gobernarán todas las decisiones tomadas durante el procesamiento de las ofertas de empleo, garantizando que dichas decisiones sean consistentes, reproducibles, trazables y auditables.

Este documento determina cómo la automatización evaluará la información disponible, aplicará las reglas de negocio, asignará prioridades, resolverá situaciones previstas y determinará cuándo una decisión podrá ejecutarse de forma automática o requerirá la intervención del usuario.

Asimismo, constituye la referencia oficial para el diseño, implementación, validación y evolución del motor de decisiones del sistema, asegurando que todas las decisiones se mantengan alineadas con los requisitos funcionales, los requisitos no funcionales y los principios generales definidos para el proyecto.

Las disposiciones contenidas en este documento serán de cumplimiento obligatorio para todos los módulos que realicen procesos de evaluación, clasificación, priorización, descarte, recomendación o cualquier otra actividad que implique la toma de decisiones dentro de la automatización.

---

# 2. Principios del modelo de decisiones

Los siguientes principios establecen las condiciones que deberán cumplir todas las decisiones tomadas por la automatización durante el procesamiento de las ofertas de empleo.

Estos principios complementan los requisitos funcionales y no funcionales del proyecto y constituyen los criterios obligatorios para el diseño, implementación, validación y evolución del motor de decisiones.

---

### PMD-001. Decisiones basadas en reglas

Toda decisión automática deberá fundamentarse exclusivamente en reglas de negocio previamente documentadas y aprobadas.

No se permitirá la ejecución de decisiones basadas en criterios implícitos, aleatorios o no documentados.

---

### PMD-002. Consistencia

Ante las mismas entradas, configuraciones y reglas de negocio, la automatización deberá producir la misma decisión.

Las decisiones deberán ser determinísticas y evitar comportamientos inconsistentes.

---

### PMD-003. Reproducibilidad

Toda decisión deberá poder reproducirse utilizando la misma información, configuración y versión de las reglas vigentes al momento de su ejecución.

---

### PMD-004. Trazabilidad

Cada decisión deberá conservar la información necesaria para reconstruir posteriormente el proceso que condujo al resultado obtenido.

La trazabilidad deberá abarcar los datos evaluados, las reglas aplicadas, el resultado generado y el responsable de la decisión.

---

### PMD-005. Auditabilidad

Toda decisión automática deberá poder justificarse mediante evidencia objetiva registrada por el sistema.

La automatización deberá permitir conocer qué decisión fue tomada, cuándo ocurrió, por qué ocurrió y qué reglas sustentaron dicho resultado.

---

### PMD-006. Separación entre evaluación y decisión

El proceso de evaluación de una oferta y la decisión derivada de dicha evaluación deberán mantenerse conceptualmente independientes.

La evaluación produce información objetiva; la decisión utiliza dicha información para determinar la acción correspondiente.

---

### PMD-007. Intervención controlada del usuario

Las decisiones estratégicas, personales, legales o de representación del usuario deberán requerir su aprobación explícita antes de ejecutarse.

La automatización no podrá sustituir el criterio del usuario en este tipo de decisiones.

---

### PMD-008. Prioridad de la integridad

Cuando exista incertidumbre, información insuficiente o conflicto entre reglas, la automatización deberá priorizar la integridad del procesamiento y evitar decisiones que puedan comprometer la calidad de los resultados.

Cuando corresponda, deberá solicitar la intervención del usuario o aplicar las estrategias definidas para dichos casos.

---

### PMD-009. Independencia tecnológica

Las reglas y criterios de decisión deberán definirse de forma independiente de la tecnología utilizada para implementarlos.

Su validez no dependerá de un lenguaje de programación, herramienta, proveedor o modelo de inteligencia artificial específico.

---

### PMD-010. Evolución controlada

Toda incorporación, modificación o eliminación de reglas de decisión deberá documentarse previamente y preservar la compatibilidad con el resto del modelo de decisiones, evitando comportamientos inconsistentes o contradictorios.

---

### PMD-011. Transparencia

Las decisiones generadas por la automatización deberán ser comprensibles para el usuario.

Siempre que sea posible, el sistema deberá proporcionar la justificación de la decisión, indicando los principales criterios y reglas que influyeron en el resultado.

---

### PMD-012. Jerarquía de reglas

Cuando dos o más reglas produzcan resultados incompatibles, la automatización deberá resolver el conflicto aplicando el orden de prioridad definido por el modelo de decisiones.

No se permitirá la ejecución simultánea de decisiones contradictorias sobre una misma oferta.

---

### PMD-013. Conservación del contexto

Toda decisión deberá considerar únicamente la información pertinente al estado actual de la oferta y el contexto definido para el proceso correspondiente.

No deberán utilizarse datos obsoletos, inconsistentes o pertenecientes a etapas incompatibles del flujo funcional.

---

### PMD-014. No aprendizaje autónomo

La automatización no podrá modificar de forma autónoma las reglas de negocio, los criterios de evaluación, los umbrales de decisión ni cualquier otro elemento del modelo de decisiones.

Toda modificación requerirá aprobación explícita del usuario y su correspondiente documentación.

---

### PMD-015. Coherencia con el flujo funcional

Toda decisión deberá respetar el flujo funcional, el ciclo de vida de las ofertas y las transiciones de estado definidas para la automatización.

Ninguna decisión podrá provocar transiciones incompatibles, omitir etapas obligatorias o alterar el comportamiento esperado del sistema, salvo cuando exista una regla documentada que lo autorice.

---

# 3. Arquitectura del modelo de decisiones

La arquitectura del modelo de decisiones define la estructura conceptual mediante la cual la automatización transforma la información disponible en decisiones consistentes, trazables y alineadas con las reglas del proyecto.

El modelo de decisiones constituye un componente transversal de la automatización y podrá ser utilizado por diferentes módulos del sistema sin depender de una implementación tecnológica específica.

Su funcionamiento se basa en un flujo secuencial compuesto por entradas, evaluación, aplicación de reglas, generación de decisiones y registro de resultados.

---

## 3.1 Componentes del modelo de decisiones

El modelo de decisiones estará conformado por los siguientes componentes conceptuales:

### AMD-001. Entradas

Corresponde al conjunto de información utilizada para evaluar una oferta de empleo y determinar la decisión correspondiente.

Las entradas se definen en el capítulo "Entradas del modelo de decisiones" del presente documento.

---

### AMD-002. Motor de evaluación

Componente encargado de analizar la información disponible y calcular los resultados necesarios para la toma de decisiones.

Entre sus responsabilidades se encuentran:

- Analizar los criterios de evaluación.
- Calcular puntuaciones.
- Detectar incumplimientos.
- Identificar condiciones especiales.
- Generar resultados intermedios.

El motor de evaluación no toma decisiones; únicamente produce información objetiva para el siguiente componente.

---

### AMD-003. Motor de reglas

Componente responsable de aplicar las reglas de negocio definidas para el proyecto utilizando los resultados generados por el motor de evaluación.

Entre sus responsabilidades se encuentran:

- Aplicar reglas de aceptación.
- Aplicar reglas de descarte.
- Resolver conflictos entre reglas.
- Determinar prioridades.
- Identificar excepciones.
- Determinar si una decisión puede ejecutarse automáticamente o requiere intervención del usuario.

---

### AMD-004. Motor de decisiones

Componente encargado de emitir la decisión final correspondiente para cada oferta.

Las decisiones generadas deberán respetar los principios definidos en este documento y mantenerse alineadas con el flujo funcional de la automatización.

---

### AMD-005. Registro y auditoría

Componente encargado de almacenar toda la información relacionada con las decisiones tomadas.

Como mínimo deberá registrar:

- Datos evaluados.
- Resultados de la evaluación.
- Reglas aplicadas.
- Decisión obtenida.
- Justificación.
- Fecha y hora.
- Responsable de la decisión.
- Estado resultante.

---

## 3.2 Flujo conceptual del modelo de decisiones

Toda decisión seguirá el siguiente flujo conceptual:

1. Recepción de las entradas necesarias para el proceso.
2. Validación de la información disponible.
3. Evaluación de los criterios definidos.
4. Aplicación de las reglas de negocio.
5. Resolución de conflictos entre reglas, cuando existan.
6. Determinación de la decisión correspondiente.
7. Asignación del estado resultante.
8. Registro completo de la decisión para garantizar su trazabilidad y auditoría.

---

## 3.3 Responsabilidades del modelo de decisiones

El modelo de decisiones será responsable de:

- Evaluar objetivamente la información disponible.
- Aplicar las reglas de negocio aprobadas.
- Emitir decisiones consistentes y reproducibles.
- Priorizar ofertas según los criterios establecidos.
- Determinar cuándo una oferta debe continuar, detenerse o requerir intervención del usuario.
- Garantizar la trazabilidad de todas las decisiones.
- Preservar la coherencia con el flujo funcional y el ciclo de vida de las ofertas.

---

## 3.4 Responsabilidades fuera del alcance

El modelo de decisiones no tendrá como responsabilidad:

- Modificar las reglas de negocio de forma autónoma.
- Alterar el perfil profesional del usuario.
- Sustituir decisiones estratégicas reservadas al usuario.
- Ejecutar acciones operativas ajenas al proceso de decisión.
- Implementar la lógica técnica de los módulos que consumen sus decisiones.
- Depender de un modelo de inteligencia artificial, lenguaje de programación o herramienta específica para producir sus resultados.

---

# 4. Tipos de decisiones

El modelo de decisiones clasifica las decisiones de la automatización según su finalidad, nivel de autonomía, impacto sobre el flujo funcional y grado de intervención del usuario.

Esta clasificación permite definir con claridad las responsabilidades del sistema y establecer los límites de actuación de la automatización.

---

## 4.1 Decisiones automáticas

Las decisiones automáticas son aquellas que la automatización puede ejecutar sin intervención del usuario, siempre que existan reglas de negocio previamente documentadas que respalden su ejecución.

Estas decisiones deberán cumplir todos los principios establecidos en el presente documento y mantener su trazabilidad completa.

Ejemplos:

- Detectar ofertas duplicadas.
- Validar información obligatoria.
- Clasificar una oferta.
- Asignar una prioridad.
- Descartar una oferta por incumplimiento de reglas objetivas.
- Actualizar estados del flujo funcional.

---

### TD-001. Características

Las decisiones automáticas deberán ser:

- Basadas en reglas.
- Determinísticas.
- Reproducibles.
- Auditables.
- Reversibles cuando la arquitectura lo permita.

---

## 4.2 Recomendaciones

Las recomendaciones corresponden a conclusiones generadas por la automatización para apoyar la toma de decisiones del usuario.

Una recomendación no modifica por sí misma el estado de una oferta ni ejecuta acciones estratégicas.

Su propósito es proporcionar información objetiva que facilite la decisión final del usuario.

Ejemplos:

- Recomendar continuar con una candidatura.
- Recomendar revisar una oferta manualmente.
- Recomendar descartar una oferta por bajo nivel de compatibilidad.
- Recomendar actualizar determinada información antes de continuar.

---

### TD-002. Características

Las recomendaciones deberán:

- Basarse en información verificable.
- Justificarse mediante reglas documentadas.
- Mantener trazabilidad.
- Ser independientes de la decisión final del usuario.

---

## 4.3 Decisiones estratégicas

Las decisiones estratégicas corresponden a aquellas cuyo impacto excede las responsabilidades de la automatización y, por tanto, requieren autorización explícita del usuario.

Estas decisiones no podrán ejecutarse automáticamente.

Ejemplos:

- Aprobar una candidatura.
- Decidir postularse a una empresa.
- Modificar criterios profesionales.
- Autorizar el envío de información a terceros.

---

### TD-003. Características

Las decisiones estratégicas deberán:

- Ser tomadas exclusivamente por el usuario.
- Registrarse como parte del historial de la oferta.
- Conservar la justificación correspondiente.
- Mantener trazabilidad completa.

---

## 4.4 Decisiones operativas

Las decisiones operativas controlan el funcionamiento interno de la automatización y permiten mantener la continuidad del procesamiento.

Estas decisiones afectan el comportamiento técnico del sistema, pero no modifican las decisiones estratégicas del usuario.

Ejemplos:

- Reintentar un proceso.
- Pausar una ejecución.
- Reanudar un procesamiento.
- Marcar una oferta para revisión.
- Cambiar el estado operativo de una oferta.

---

### TD-004. Características

Las decisiones operativas deberán:

- Respetar las estrategias de recuperación definidas.
- Preservar la integridad del procesamiento.
- Mantener la consistencia del flujo funcional.

---

## 4.5 Decisiones de excepción

Las decisiones de excepción corresponden a situaciones no previstas por el flujo normal de procesamiento que requieren la aplicación de reglas especiales.

Su objetivo es preservar la estabilidad y la continuidad de la automatización cuando ocurren condiciones anómalas.

Ejemplos:

- Información insuficiente.
- Reglas contradictorias.
- Datos inconsistentes.
- Dependencias externas indisponibles.
- Resultados no concluyentes.

---

### TD-005. Características

Las decisiones de excepción deberán:

- Aplicarse únicamente cuando exista una condición documentada que lo justifique.
- Mantener la trazabilidad completa.
- Priorizar la integridad del procesamiento.
- Solicitar intervención del usuario cuando no exista una resolución automática permitida.

---

## 4.6 Jerarquía de decisiones

Cuando una misma oferta se encuentre sujeta a varios tipos de decisiones simultáneamente, la automatización deberá resolverlas respetando el siguiente orden de prioridad:

1. Decisiones de excepción.
2. Decisiones estratégicas del usuario.
3. Decisiones automáticas.
4. Decisiones operativas.
5. Recomendaciones.

Ningún tipo de decisión podrá contradecir una decisión ubicada en un nivel superior de esta jerarquía.

---

## 4.7 Principio de unicidad de la decisión

Para un mismo proceso funcional y una misma oferta, únicamente podrá existir una decisión vigente como resultado final del proceso de decisión.

Si durante la evaluación se generan múltiples resultados parciales, el modelo de decisiones deberá resolverlos mediante las reglas definidas antes de emitir la decisión definitiva.

Toda decisión sustituida, descartada o modificada deberá conservarse en el historial para garantizar la trazabilidad y la auditoría del sistema.

---

# 5. Entradas del modelo de decisiones

Las entradas del modelo de decisiones corresponden al conjunto de información que la automatización podrá utilizar para evaluar una oferta de empleo y determinar la decisión que corresponda según las reglas de negocio definidas.

Todas las entradas deberán provenir de fuentes válidas, encontrarse debidamente identificadas y haber superado los procesos de validación definidos por la automatización antes de ser utilizadas para la toma de decisiones.

El modelo de decisiones no podrá utilizar información no validada, inconsistente o ajena al contexto del proceso evaluado.

---

## EDM-001. Información de la oferta

Corresponde a la información estructurada de la oferta de empleo obtenida durante los procesos de descubrimiento y preparación.

Podrá incluir, entre otros:

- Título del cargo.
- Empresa.
- Descripción.
- Responsabilidades.
- Requisitos.
- Competencias.
- Salario.
- Modalidad de trabajo.
- Ubicación.
- Tipo de contrato.
- Idioma requerido.
- Fecha de publicación.
- Plataforma de origen.
- URL.
- Identificadores asociados.

Esta información constituye la principal entrada para el proceso de evaluación.

---

## EDM-002. Perfil profesional del usuario

Corresponde al conjunto de información profesional utilizada para medir la compatibilidad entre el usuario y la oferta evaluada.

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

El perfil profesional deberá mantenerse sincronizado con la versión vigente aprobada por el usuario.

---

## EDM-003. Reglas de negocio

Corresponde al conjunto de reglas documentadas que gobiernan el comportamiento del modelo de decisiones.

Podrán incluir:

- Reglas de aceptación.
- Reglas de descarte.
- Reglas de priorización.
- Reglas de clasificación.
- Umbrales.
- Excepciones.
- Restricciones.

Las reglas de negocio constituyen la base para toda decisión automática.

---

## EDM-004. Configuración del sistema

Corresponde a los parámetros operativos que condicionan el funcionamiento del modelo de decisiones.

Podrán incluir:

- Configuraciones generales.
- Parámetros de evaluación.
- Umbrales configurables.
- Preferencias de procesamiento.
- Configuraciones de módulos.

Las configuraciones deberán administrarse de forma centralizada.

---

## EDM-005. Información histórica

Corresponde a la información generada durante ejecuciones anteriores que resulte pertinente para la decisión actual.

Podrá incluir:

- Historial de la oferta.
- Resultados de evaluaciones anteriores.
- Decisiones previas.
- Reprocesamientos.
- Cambios de estado.
- Métricas relevantes.

La utilización del historial nunca deberá comprometer la reproducibilidad de las decisiones.

---

## EDM-006. Resultados intermedios

Corresponde a la información producida por etapas previas del proceso de evaluación y utilizada como insumo para decisiones posteriores.

Podrá incluir:

- Puntuaciones parciales.
- Validaciones realizadas.
- Clasificaciones temporales.
- Indicadores de compatibilidad.
- Observaciones generadas durante la evaluación.

Estos resultados únicamente podrán utilizarse dentro del contexto de la oferta evaluada.

---

## EDM-007. Decisiones del usuario

Corresponde a las decisiones estratégicas previamente registradas por el usuario y que deban considerarse durante el procesamiento de una oferta.

Podrán incluir:

- Aprobaciones.
- Descartes manuales.
- Modificaciones de prioridad.
- Autorizaciones.
- Reprocesamientos solicitados.
- Cambios aprobados en criterios profesionales.

Estas decisiones tendrán prioridad sobre cualquier recomendación generada por la automatización cuando así lo establezcan las reglas del sistema.

---

## EDM-008. Estado de la oferta

Corresponde al estado actual del ciclo de vida y al estado operativo de la oferta al momento de iniciar la decisión.

El estado determinará qué reglas pueden aplicarse y qué decisiones están permitidas para esa etapa del flujo funcional.

No podrán ejecutarse decisiones incompatibles con el estado vigente de la oferta.

---

## Principios generales de las entradas

Toda entrada utilizada por el modelo de decisiones deberá cumplir las siguientes condiciones:

- Ser identificable de forma única.
- Provenir de una fuente autorizada por la automatización.
- Haber superado las validaciones correspondientes.
- Mantener consistencia con el estado actual del procesamiento.
- Ser trazable durante todo el ciclo de vida de la oferta.
- Permanecer disponible para auditorías y reprocesamientos cuando sea necesario.
- Respetar las reglas de integridad definidas para el proyecto.

---

# 6. Criterios de evaluación

Los criterios de evaluación representan los aspectos objetivos que el modelo de decisiones analizará para determinar el nivel de compatibilidad entre una oferta de empleo y el perfil profesional del usuario.

Cada criterio constituye una dimensión independiente de evaluación y será utilizado posteriormente por el sistema de puntuación y las reglas de decisión.

La definición de los criterios no establece su peso, importancia relativa ni los umbrales de aceptación. Dichos elementos serán definidos en los capítulos correspondientes de este documento.

---

## CE-001. Compatibilidad profesional

Evalúa el grado de correspondencia entre el perfil profesional del usuario y el perfil requerido por la oferta.

Podrá considerar, entre otros aspectos:

- Cargo.
- Área profesional.
- Nivel de experiencia.
- Seniority.
- Especialización.
- Responsabilidades principales.

---

## CE-002. Competencias técnicas

Evalúa el nivel de coincidencia entre las competencias técnicas requeridas por la oferta y las competencias registradas en el perfil profesional del usuario.

Podrá considerar:

- Tecnologías.
- Herramientas.
- Lenguajes.
- Frameworks.
- Plataformas.
- Metodologías.
- Conocimientos especializados.

---

## CE-003. Competencias profesionales

Evalúa la coincidencia entre las competencias profesionales solicitadas y las capacidades registradas en el perfil del usuario.

Podrá considerar:

- Liderazgo.
- Comunicación.
- Trabajo en equipo.
- Organización.
- Resolución de problemas.
- Adaptabilidad.
- Otras competencias relevantes.

---

## CE-004. Experiencia laboral

Evalúa la correspondencia entre la experiencia requerida por la oferta y la experiencia documentada del usuario.

Podrá considerar:

- Años de experiencia.
- Experiencia específica.
- Sectores.
- Funciones desempeñadas.
- Nivel de responsabilidad.
- Trayectoria profesional.

---

## CE-005. Formación académica

Evalúa la compatibilidad entre la formación solicitada y la formación registrada en el perfil profesional.

Podrá considerar:

- Nivel académico.
- Títulos.
- Programas de formación.
- Especializaciones.
- Certificaciones.
- Estudios complementarios.

---

## CE-006. Idiomas

Evalúa la coincidencia entre los idiomas requeridos por la oferta y los idiomas conocidos por el usuario.

Podrá considerar:

- Idioma.
- Nivel requerido.
- Nivel acreditado.
- Certificaciones lingüísticas.

---

## CE-007. Condiciones laborales

Evalúa la compatibilidad entre las condiciones ofrecidas y las preferencias laborales del usuario.

Podrá considerar:

- Modalidad de trabajo.
- Tipo de contrato.
- Jornada.
- Horario.
- Disponibilidad requerida.

---

## CE-008. Ubicación geográfica

Evalúa la compatibilidad entre la ubicación de la oferta y las preferencias geográficas del usuario.

Podrá considerar:

- Ciudad.
- País.
- Trabajo remoto.
- Trabajo híbrido.
- Reubicación.
- Restricciones geográficas.

---

## CE-009. Compensación económica

Evalúa la compatibilidad entre la compensación ofrecida y las expectativas salariales definidas por el usuario.

Podrá considerar:

- Salario.
- Rango salarial.
- Moneda.
- Beneficios económicos cuando sean relevantes.

Cuando la oferta no publique información salarial, este criterio deberá tratarse conforme a las reglas definidas para información incompleta.

---

## CE-010. Empresa

Evalúa aspectos relacionados con la organización que publica la oferta.

Podrá considerar:

- Empresas objetivo.
- Empresas restringidas.
- Sector económico.
- Preferencias previamente definidas por el usuario.

---

## CE-011. Calidad de la oferta

Evalúa la calidad y suficiencia de la información disponible para realizar una evaluación confiable.

Podrá considerar:

- Integridad de la información.
- Claridad de la descripción.
- Consistencia de los datos.
- Información obligatoria disponible.
- Nivel de detalle.

Una baja calidad de la información podrá afectar la confiabilidad de la evaluación sin implicar necesariamente el descarte de la oferta.

---

## CE-012. Restricciones del usuario

Evalúa el cumplimiento de las restricciones explícitamente definidas por el usuario para su búsqueda de empleo.

Podrá considerar, entre otras:

- Empresas excluidas.
- Tecnologías no deseadas.
- Modalidades no aceptadas.
- Ubicaciones restringidas.
- Condiciones laborales no aceptadas.
- Otras restricciones configuradas.

Las restricciones definidas por el usuario tendrán prioridad sobre cualquier criterio de compatibilidad.

---

## Principios generales de evaluación

Todos los criterios de evaluación deberán cumplir las siguientes condiciones:

- Evaluarse de forma independiente.
- Basarse únicamente en información validada.
- Ser objetivos y reproducibles.
- Mantener trazabilidad completa.
- Utilizar reglas documentadas.
- Poder ampliarse sin afectar los criterios existentes.
- No depender de una tecnología o herramienta específica.
- Mantener coherencia con el perfil profesional del usuario y el estado actual de la oferta.

---

# 7. Sistema de puntuación

El sistema de puntuación define el mecanismo mediante el cual el modelo de decisiones transformará los resultados de la evaluación en una medida cuantitativa de compatibilidad entre una oferta de empleo y el perfil profesional del usuario.

Su propósito es proporcionar una valoración objetiva, consistente y reproducible que sirva como insumo para las reglas de aceptación, descarte y priorización.

El sistema de puntuación no constituye una decisión por sí mismo; representa únicamente el resultado numérico obtenido durante el proceso de evaluación.

---

## SP-001. Objetivo

El sistema de puntuación deberá:

- Medir el nivel de compatibilidad de cada oferta.
- Facilitar la comparación entre múltiples ofertas.
- Servir como entrada para las reglas de decisión.
- Mantener criterios uniformes para todas las evaluaciones.
- Reducir la subjetividad en el proceso de análisis.

---

## SP-002. Estructura de la puntuación

La puntuación de una oferta estará compuesta por la combinación de los resultados obtenidos en los criterios de evaluación definidos en este documento.

Cada criterio podrá aportar una contribución independiente al resultado final de acuerdo con las reglas de ponderación establecidas.

La definición de los pesos específicos se documentará una vez se diseñen las reglas de negocio correspondientes.

---

## SP-003. Independencia de los criterios

Cada criterio de evaluación deberá calcularse de forma independiente antes de integrarse en la puntuación global.

El resultado obtenido en un criterio no deberá modificar directamente el cálculo de otro, salvo cuando exista una regla documentada que lo autorice.

---

## SP-004. Ponderación

Cada criterio podrá tener un peso relativo diferente dentro del cálculo de la puntuación total.

La ponderación deberá:

- Estar documentada.
- Ser configurable.
- Mantenerse centralizada.
- Poder modificarse sin alterar la lógica general del modelo de decisiones.

---

## SP-005. Penalizaciones

El sistema podrá aplicar penalizaciones cuando una oferta incumpla determinadas condiciones definidas por las reglas de negocio.

Las penalizaciones deberán:

- Encontrarse previamente documentadas.
- Ser objetivas.
- Ser reproducibles.
- Mantener trazabilidad.

Una penalización no implicará necesariamente el descarte automático de la oferta.

---

## SP-006. Bonificaciones

El sistema podrá otorgar bonificaciones cuando una oferta presente características especialmente favorables para el perfil del usuario.

Las bonificaciones deberán:

- Basarse en reglas documentadas.
- Ser objetivas.
- Ser trazables.
- Mantener consistencia entre evaluaciones.

---

## SP-007. Información insuficiente

Cuando uno o varios criterios no puedan evaluarse por falta de información, el sistema de puntuación deberá aplicar el tratamiento definido para información incompleta sin generar resultados inconsistentes.

La ausencia de información no deberá interpretarse automáticamente como un resultado favorable o desfavorable, salvo cuando exista una regla específica que así lo determine.

---

## SP-008. Normalización

La puntuación final deberá expresarse utilizando una escala uniforme para todas las ofertas evaluadas.

La escala utilizada deberá permitir comparar objetivamente los resultados obtenidos entre diferentes oportunidades laborales.

---

## SP-009. Clasificación del resultado

Una vez calculada la puntuación, el resultado deberá clasificarse en un nivel de compatibilidad.

La clasificación servirá como insumo para las reglas de aceptación, descarte y priorización.

Los rangos específicos de clasificación se definirán posteriormente junto con las reglas de negocio correspondientes.

---

## SP-010. Reproducibilidad

El cálculo de la puntuación deberá producir siempre el mismo resultado cuando se utilicen:

- Las mismas entradas.
- Las mismas reglas.
- La misma configuración.
- La misma versión del modelo de decisiones.

---

## SP-011. Trazabilidad

Toda puntuación generada deberá conservar la información necesaria para reconstruir completamente su cálculo.

Como mínimo deberá registrarse:

- Criterios evaluados.
- Resultados individuales.
- Penalizaciones aplicadas.
- Bonificaciones aplicadas.
- Puntuación final.
- Nivel de compatibilidad obtenido.
- Fecha y hora del cálculo.
- Versión de las reglas utilizadas.

---

## Principios generales del sistema de puntuación

El sistema de puntuación deberá cumplir los siguientes principios:

- Objetividad.
- Consistencia.
- Transparencia.
- Configuración centralizada.
- Independencia tecnológica.
- Escalabilidad.
- Auditabilidad.
- Reproducibilidad.
- Trazabilidad.
- Facilidad de mantenimiento.

---

# 8. Reglas de aceptación

Las reglas de aceptación establecen las condiciones que deberá cumplir una oferta de empleo para continuar avanzando dentro del flujo funcional de la automatización.

Su propósito es garantizar que únicamente las ofertas con un nivel suficiente de compatibilidad y calidad continúen hacia las etapas posteriores del procesamiento.

Las reglas de aceptación deberán aplicarse después de finalizar el proceso de evaluación y antes de iniciar el procesamiento profundo de la oferta.

---

## RA-001. Cumplimiento de criterios mínimos

Toda oferta deberá cumplir los criterios mínimos definidos por las reglas de negocio para poder ser aceptada.

El incumplimiento de uno o más criterios obligatorios impedirá su aceptación, independientemente de la puntuación obtenida.

---

## RA-002. Compatibilidad suficiente

La oferta deberá alcanzar el nivel mínimo de compatibilidad establecido por el sistema de puntuación.

Los umbrales específicos serán definidos en las reglas de negocio correspondientes.

---

## RA-003. Integridad de la información

La información disponible deberá ser suficiente para permitir una evaluación confiable.

Cuando la información resulte insuficiente, la automatización aplicará las reglas previstas para información incompleta antes de aceptar o descartar la oferta.

---

## RA-004. Cumplimiento de restricciones

La oferta deberá respetar todas las restricciones obligatorias definidas por el usuario.

Ninguna oferta podrá ser aceptada si incumple una restricción clasificada como excluyente.

---

## RA-005. Consistencia de la información

La información utilizada durante la evaluación deberá encontrarse libre de inconsistencias que impidan interpretar correctamente la oferta.

Cuando se detecten inconsistencias relevantes, la automatización deberá aplicar las reglas de validación o de excepción antes de continuar.

---

## RA-006. Estado válido

La oferta únicamente podrá ser aceptada si se encuentra en un estado del ciclo de vida compatible con el proceso de evaluación.

No podrán aceptarse ofertas que ya hayan finalizado su procesamiento, hayan sido descartadas o se encuentren en estados incompatibles con la evaluación.

---

## RA-007. Ausencia de conflictos

Antes de aceptar una oferta, el modelo de decisiones deberá verificar que no existan conflictos entre las reglas aplicadas.

Cuando se detecten conflictos, deberán resolverse conforme al mecanismo de resolución definido en este documento antes de emitir la decisión final.

---

## RA-008. Validación del resultado

La aceptación de una oferta únicamente podrá producirse después de verificar que la evaluación haya finalizado correctamente y que todos los resultados requeridos se encuentren disponibles.

No deberán aceptarse ofertas con evaluaciones incompletas o interrumpidas.

---

## RA-009. Registro obligatorio

Toda aceptación deberá registrarse como parte del historial de la oferta.

Como mínimo deberá conservarse la siguiente información:

- Identificador de la oferta.
- Fecha y hora.
- Resultado de la evaluación.
- Nivel de compatibilidad.
- Reglas aplicadas.
- Justificación de la aceptación.
- Estado asignado.
- Responsable de la decisión.

---

## RA-010. Continuidad del flujo funcional

La aceptación de una oferta autoriza exclusivamente su transición hacia la siguiente etapa definida en el flujo funcional.

La aceptación no implica la aprobación automática de una candidatura, el envío de información a terceros ni ninguna otra decisión estratégica reservada al usuario.

---

## Principios generales de aceptación

Todas las reglas de aceptación deberán cumplir los siguientes principios:

- Basarse exclusivamente en reglas documentadas.
- Aplicarse de manera uniforme para todas las ofertas.
- Ser objetivas y reproducibles.
- Mantener trazabilidad completa.
- Respetar las restricciones del usuario.
- Preservar la integridad del flujo funcional.
- Permitir auditorías posteriores.
- Mantener independencia respecto de la tecnología utilizada para su implementación.

---

# 9. Reglas de descarte

Las reglas de descarte establecen las condiciones bajo las cuales una oferta de empleo deberá finalizar su procesamiento sin continuar hacia las etapas posteriores del flujo funcional.

Su propósito es evitar el consumo innecesario de recursos sobre ofertas que no cumplen las condiciones mínimas definidas por el modelo de decisiones o que presentan restricciones incompatibles con el perfil profesional del usuario.

Las reglas de descarte deberán aplicarse de forma objetiva, consistente y únicamente cuando exista una regla de negocio que las respalde.

---

## RD-001. Incumplimiento de criterios obligatorios

Toda oferta que incumpla uno o más criterios clasificados como obligatorios deberá ser descartada.

Los criterios obligatorios serán definidos por las reglas de negocio correspondientes.

---

## RD-002. Compatibilidad insuficiente

La oferta deberá descartarse cuando el resultado de la evaluación indique un nivel de compatibilidad inferior al umbral mínimo establecido para continuar el procesamiento.

Los valores específicos de dichos umbrales serán definidos en las reglas de negocio.

---

## RD-003. Incumplimiento de restricciones excluyentes

La oferta deberá descartarse cuando incumpla alguna restricción definida por el usuario como excluyente.

Entre otras, podrán considerarse restricciones relacionadas con:

- Empresas restringidas.
- Modalidad laboral.
- Ubicación.
- Condiciones laborales.
- Tecnologías no aceptadas.
- Otras restricciones configuradas por el usuario.

---

## RD-004. Información inválida

La oferta deberá descartarse cuando la información disponible sea inconsistente, corrupta o insuficiente para permitir una evaluación confiable y no exista una estrategia documentada que permita resolver dicha situación.

---

## RD-005. Oferta duplicada

Cuando se determine que una oferta corresponde a una oportunidad previamente registrada y las reglas de negocio indiquen que no debe reprocesarse, el sistema deberá descartar el nuevo registro y conservar únicamente el historial correspondiente.

El descarte por duplicidad no implicará la eliminación de información previamente almacenada.

---

## RD-006. Estado incompatible

Una oferta deberá descartarse cuando se encuentre en un estado del ciclo de vida que impida continuar el procesamiento conforme al flujo funcional definido.

No podrán procesarse ofertas finalizadas, descartadas o en cualquier otro estado incompatible, salvo que exista una regla de reprocesamiento previamente autorizada.

---

## RD-007. Conflictos no resolubles

Cuando durante la evaluación se detecten conflictos entre reglas de negocio que no puedan resolverse mediante los mecanismos definidos por el modelo de decisiones, la oferta no deberá continuar automáticamente.

El sistema deberá aplicar la estrategia prevista para estos casos, que podrá incluir el descarte o la intervención del usuario, según corresponda.

---

## RD-008. Validación del descarte

Antes de emitir una decisión de descarte, la automatización deberá verificar que:

- La evaluación haya finalizado correctamente.
- La regla de descarte aplicada sea válida.
- No exista una regla de mayor prioridad que impida el descarte.
- El resultado sea consistente con el estado actual de la oferta.

---

## RD-009. Registro obligatorio

Toda decisión de descarte deberá registrarse como parte del historial de la oferta.

Como mínimo deberá conservarse la siguiente información:

- Identificador de la oferta.
- Fecha y hora.
- Regla aplicada.
- Motivo del descarte.
- Resultados de la evaluación.
- Estado asignado.
- Responsable de la decisión.

---

## RD-010. Finalización del procesamiento

Una oferta descartada no continuará hacia las etapas posteriores del flujo funcional.

Únicamente podrá volver a procesarse cuando exista una regla de reprocesamiento documentada o una decisión explícita del usuario que así lo autorice.

---

## Principios generales del descarte

Todas las reglas de descarte deberán cumplir los siguientes principios:

- Basarse exclusivamente en reglas documentadas.
- Aplicarse de forma uniforme para todas las ofertas.
- Ser objetivas y reproducibles.
- Mantener trazabilidad completa.
- Preservar la integridad del historial.
- Evitar descartes basados en información no validada.
- Permitir auditorías posteriores.
- Mantener independencia respecto de la tecnología utilizada para su implementación.

---

# 10. Priorización de ofertas

La priorización de ofertas define el mecanismo mediante el cual la automatización ordenará las oportunidades de empleo aceptadas según su nivel de interés para el usuario.

Su propósito es optimizar el uso de los recursos de procesamiento y facilitar la toma de decisiones, concentrando los esfuerzos sobre aquellas ofertas que representen una mayor oportunidad de éxito.

La priorización únicamente podrá aplicarse a ofertas que hayan superado satisfactoriamente las reglas de aceptación.

---

## PO-001. Objetivo de la priorización

La priorización deberá permitir:

- Determinar el orden de procesamiento de las ofertas.
- Identificar las oportunidades con mayor potencial.
- Optimizar la utilización de recursos de la automatización.
- Facilitar la revisión por parte del usuario.
- Establecer un criterio uniforme de clasificación.

---

## PO-002. Criterios de priorización

La prioridad de una oferta podrá determinarse utilizando, entre otros, los siguientes elementos:

- Resultado del sistema de puntuación.
- Nivel de compatibilidad.
- Cumplimiento de criterios clave.
- Restricciones del usuario.
- Calidad de la información disponible.
- Reglas de negocio aplicables.
- Otros criterios definidos por el proyecto.

La importancia relativa de cada criterio será definida en las reglas de negocio correspondientes.

---

## PO-003. Niveles de prioridad

Toda oferta aceptada deberá clasificarse en un único nivel de prioridad.

Los niveles oficiales del modelo de decisiones serán:

- Prioridad alta.
- Prioridad media.
- Prioridad baja.

Los criterios específicos para asignar cada nivel se documentarán en las reglas de negocio.

---

## PO-004. Unicidad de la prioridad

Una oferta únicamente podrá tener un nivel de prioridad vigente en un momento determinado.

Cuando una nueva evaluación modifique la prioridad, la clasificación anterior deberá conservarse en el historial para garantizar la trazabilidad.

---

## PO-005. Repriorización

La prioridad de una oferta podrá recalcularse cuando ocurra alguno de los siguientes eventos:

- Actualización de la información de la oferta.
- Modificación del perfil profesional del usuario.
- Cambio en las reglas de negocio.
- Reprocesamiento autorizado.
- Incorporación de nueva información relevante.

Toda repriorización deberá registrarse como un nuevo evento dentro del historial.

---

## PO-006. Independencia del procesamiento

La prioridad determina el orden recomendado para procesar o revisar una oferta, pero no modifica por sí misma el resultado de la evaluación ni sustituye las reglas de aceptación o descarte.

Una oferta de alta prioridad deberá seguir cumpliendo todas las reglas del flujo funcional.

---

## PO-007. Resolución de empates

Cuando dos o más ofertas obtengan el mismo nivel de prioridad, el modelo de decisiones deberá aplicar los mecanismos de desempate definidos por las reglas de negocio.

Los criterios de desempate deberán ser:

- Objetivos.
- Reproducibles.
- Documentados.
- Consistentes.

Mientras dichos criterios no se encuentren definidos, las ofertas se considerarán equivalentes dentro del mismo nivel de prioridad.

---

## PO-008. Validación de la prioridad

Antes de asignar una prioridad, la automatización deberá verificar que:

- La evaluación haya finalizado correctamente.
- Exista una puntuación válida.
- Se hayan aplicado todas las reglas correspondientes.
- No existan conflictos pendientes de resolver.
- La oferta continúe siendo elegible para el procesamiento.

---

## PO-009. Registro de la priorización

Toda asignación o modificación de prioridad deberá registrarse como parte del historial de la oferta.

Como mínimo deberá conservarse la siguiente información:

- Identificador de la oferta.
- Fecha y hora.
- Nivel de prioridad asignado.
- Resultado de la evaluación.
- Reglas aplicadas.
- Motivo de la clasificación.
- Responsable de la decisión.

---

## PO-010. Uso de la prioridad

La prioridad podrá utilizarse como criterio para:

- Determinar el orden de procesamiento profundo.
- Organizar las ofertas presentadas al usuario.
- Programar futuras ejecuciones.
- Optimizar la asignación de recursos.
- Generar reportes y estadísticas.

La prioridad no autoriza automáticamente ninguna acción estratégica reservada al usuario.

---

## Principios generales de la priorización

La priorización de ofertas deberá cumplir los siguientes principios:

- Basarse exclusivamente en reglas documentadas.
- Mantener consistencia entre evaluaciones equivalentes.
- Ser objetiva y reproducible.
- Conservar trazabilidad completa.
- Permitir recalcular la prioridad cuando cambie el contexto de evaluación.
- Mantener independencia respecto de la tecnología utilizada para su implementación.
- Facilitar la escalabilidad del modelo de decisiones.

---

# 11. Reglas de transición de decisiones

Las reglas de transición de decisiones establecen las condiciones bajo las cuales una decisión podrá modificar el estado de una oferta dentro del flujo funcional de la automatización.

Su propósito es garantizar que toda transición sea consistente con el modelo de decisiones, el ciclo de vida de las ofertas y las reglas de negocio definidas para el proyecto.

Ninguna decisión podrá provocar cambios de estado que no se encuentren previamente documentados y autorizados por este modelo.

---

## RTD-001. Transiciones autorizadas

Toda decisión deberá producir únicamente transiciones previamente definidas dentro del flujo funcional de la automatización.

No se permitirán cambios de estado implícitos, arbitrarios o no documentados.

---

## RTD-002. Validación previa

Antes de ejecutar una transición, la automatización deberá verificar que:

- La evaluación correspondiente haya finalizado correctamente.
- La decisión se encuentre completamente determinada.
- No existan conflictos pendientes de resolver.
- La oferta se encuentre en un estado compatible con la transición solicitada.

---

## RTD-003. Compatibilidad entre estados

Las transiciones únicamente podrán realizarse entre estados compatibles del ciclo de vida y del estado operativo de la oferta.

No podrán producirse transiciones que contradigan el flujo funcional aprobado para el proyecto.

---

## RTD-004. Transiciones por aceptación

Cuando una oferta cumpla las reglas de aceptación, la decisión emitida deberá permitir su avance hacia la siguiente etapa definida dentro del flujo funcional.

La aceptación de una oferta no autoriza automáticamente ninguna acción estratégica reservada al usuario.

---

## RTD-005. Transiciones por descarte

Cuando una oferta incumpla las reglas de aceptación o cumpla una regla de descarte, la automatización deberá finalizar su procesamiento conforme al flujo funcional definido.

El descarte deberá conservar toda la información necesaria para permitir auditorías y, cuando corresponda, futuros reprocesamientos.

---

## RTD-006. Transiciones por intervención del usuario

Cuando una decisión estratégica requiera aprobación del usuario, la automatización deberá suspender la transición automática hasta recibir la decisión correspondiente.

Una vez registrada la decisión del usuario, el flujo continuará conforme a las reglas definidas para dicho escenario.

---

## RTD-007. Transiciones por reprocesamiento

Cuando una oferta sea autorizada para reprocesamiento, la automatización únicamente podrá regresar a etapas previamente definidas por las reglas de negocio.

El reprocesamiento no deberá eliminar ni sobrescribir el historial de decisiones anteriores.

---

## RTD-008. Transiciones por recuperación

Cuando un proceso interrumpido sea recuperado satisfactoriamente, la automatización deberá continuar desde el estado más adecuado, evitando repetir etapas correctamente finalizadas.

Toda recuperación deberá respetar las estrategias definidas para el manejo de fallos.

---

## RTD-009. Restricción de transiciones incompatibles

No estarán permitidas transiciones que impliquen, entre otras situaciones:

- Omitir etapas obligatorias.
- Retroceder arbitrariamente en el flujo funcional.
- Ejecutar etapas fuera de secuencia.
- Mantener simultáneamente estados incompatibles.
- Modificar estados finales sin autorización explícita.

Cualquier excepción deberá estar respaldada por una regla de negocio previamente documentada.

---

## RTD-010. Registro de las transiciones

Toda transición deberá registrarse como parte del historial de la oferta.

Como mínimo deberá conservarse la siguiente información:

- Estado anterior.
- Estado resultante.
- Decisión que originó la transición.
- Regla aplicada.
- Fecha y hora.
- Responsable de la decisión.
- Justificación de la transición.

---

## Flujo general de transición de decisiones

El modelo de decisiones seguirá el siguiente flujo conceptual para determinar la transición correspondiente:

1. Verificar el estado actual de la oferta.
2. Validar que la información requerida esté disponible.
3. Aplicar las reglas de evaluación.
4. Determinar la decisión correspondiente.
5. Verificar la compatibilidad de la transición.
6. Actualizar el estado de la oferta.
7. Registrar la transición en el historial.
8. Continuar con el siguiente proceso funcional o finalizar el procesamiento, según corresponda.

---

## Principios generales de las transiciones

Todas las transiciones de decisión deberán cumplir los siguientes principios:

- Basarse exclusivamente en reglas documentadas.
- Mantener la coherencia con el flujo funcional.
- Preservar la integridad del ciclo de vida de la oferta.
- Ser objetivas y reproducibles.
- Mantener trazabilidad completa.
- Evitar estados inconsistentes.
- Permitir auditorías posteriores.
- Mantener independencia respecto de la tecnología utilizada para su implementación.

---

# 12. Manejo de casos especiales

Los casos especiales corresponden a situaciones previstas por el modelo de decisiones que, debido a sus características particulares, requieren un tratamiento diferente al flujo normal de evaluación sin constituir necesariamente un error o una excepción del sistema.

Su propósito es preservar la consistencia de las decisiones, reducir la intervención innecesaria del usuario y garantizar que las ofertas sean procesadas conforme a reglas previamente documentadas.

Todo caso especial deberá contar con una estrategia de tratamiento definida antes de su incorporación al modelo de decisiones.

---

## CEE-001. Información incompleta

Cuando una oferta no contenga toda la información necesaria para evaluar uno o varios criterios, la automatización deberá aplicar las reglas definidas para información incompleta.

El tratamiento dependerá de la importancia de la información ausente y de las reglas de negocio correspondientes.

La ausencia de información no implicará automáticamente la aceptación ni el descarte de la oferta.

---

## CEE-002. Información contradictoria

Cuando la información de una oferta presente inconsistencias entre sus diferentes campos o fuentes, la automatización deberá identificar el conflicto y aplicar las reglas de validación correspondientes antes de emitir una decisión.

Mientras el conflicto permanezca sin resolver, no deberá generarse una decisión definitiva.

---

## CEE-003. Información actualizada

Cuando una oferta previamente registrada incorpore nueva información relevante, el sistema deberá determinar si dicha actualización requiere una nueva evaluación o únicamente una actualización del historial.

Toda reevaluación deberá conservar la trazabilidad de las decisiones anteriores.

---

## CEE-004. Oferta previamente procesada

Cuando una oferta ya haya sido procesada anteriormente, el modelo de decisiones deberá determinar si corresponde:

- Mantener la decisión existente.
- Actualizar la evaluación.
- Repriorizar la oferta.
- Reprocesarla.
- Conservar únicamente el historial.

La decisión dependerá de las reglas de reprocesamiento definidas para el proyecto.

---

## CEE-005. Múltiples ubicaciones

Cuando una oferta contemple varias ubicaciones o modalidades de trabajo, la automatización deberá evaluarlas conforme a las preferencias y restricciones del usuario antes de emitir una decisión.

---

## CEE-006. Información salarial ausente

Cuando la oferta no publique información sobre la compensación económica, el criterio de evaluación correspondiente deberá tratarse según las reglas definidas para información incompleta.

La ausencia de salario no implicará automáticamente el descarte de la oferta.

---

## CEE-007. Reglas parcialmente aplicables

Cuando uno o varios criterios de evaluación no resulten aplicables a una oferta específica, el sistema deberá excluir dichos criterios del proceso conforme a las reglas de negocio definidas, preservando la consistencia del resultado global.

---

## CEE-008. Cambios en las reglas de negocio

Cuando las reglas de negocio sean modificadas después de evaluar una oferta, el modelo de decisiones deberá determinar si corresponde mantener la decisión vigente o iniciar un proceso de reevaluación.

Toda reevaluación deberá quedar registrada como un nuevo evento dentro del historial.

---

## CEE-009. Intervención del usuario durante la evaluación

Cuando el usuario intervenga antes de finalizar el proceso de decisión, la automatización deberá registrar dicha intervención y adaptar el flujo conforme a las reglas correspondientes.

Las decisiones del usuario prevalecerán sobre las recomendaciones automáticas cuando así lo establezca el modelo de decisiones.

---

## CEE-010. Casos especiales futuros

La incorporación de nuevos casos especiales deberá realizarse mediante reglas documentadas, preservando la compatibilidad con el modelo de decisiones existente.

Ningún caso especial podrá modificar los principios generales definidos en este documento.

---

## Principios generales para el manejo de casos especiales

Todo caso especial deberá cumplir los siguientes principios:

- Estar previamente documentado.
- Tener criterios objetivos de identificación.
- Contar con una estrategia de tratamiento definida.
- Mantener la trazabilidad completa del procesamiento.
- Preservar la consistencia del modelo de decisiones.
- Evitar decisiones ambiguas o contradictorias.
- No alterar el flujo funcional salvo cuando exista una regla que lo autorice.
- Facilitar la incorporación de nuevos casos especiales sin afectar los existentes.

---

# 13. Manejo de excepciones

El manejo de excepciones define las reglas que deberá aplicar el modelo de decisiones cuando ocurra una situación que impida continuar el proceso normal de evaluación y que no pueda resolverse mediante el flujo funcional estándar.

Su propósito es preservar la integridad del procesamiento, garantizar la consistencia de las decisiones y minimizar el impacto operativo de situaciones no previstas o anómalas.

Toda excepción deberá ser detectada, registrada, tratada y resuelta conforme a las estrategias definidas por este documento.

---

## MED-001. Identificación de excepciones

El modelo de decisiones deberá identificar cualquier situación que impida determinar una decisión válida utilizando las reglas normales del sistema.

La identificación de una excepción no implica necesariamente un error del sistema.

---

## MED-002. Clasificación de excepciones

Toda excepción deberá clasificarse según su naturaleza antes de aplicar una estrategia de resolución.

Las excepciones podrán originarse, entre otras causas, por:

- Información insuficiente.
- Información inconsistente.
- Conflictos entre reglas.
- Estados incompatibles.
- Dependencias externas.
- Errores de evaluación.
- Configuraciones inválidas.

La clasificación específica se documentará en el documento de Manejo de Errores del proyecto.

---

## MED-003. Evaluación de recuperabilidad

Una vez identificada la excepción, la automatización deberá determinar si puede resolverse automáticamente o si requiere intervención del usuario.

La estrategia seleccionada deberá respetar las reglas de negocio y preservar la consistencia del procesamiento.

---

## MED-004. Resolución automática

Cuando exista una estrategia documentada para resolver una excepción, la automatización podrá ejecutarla de forma autónoma.

La resolución automática deberá:

- Respetar las reglas del modelo de decisiones.
- Preservar la información existente.
- Mantener la trazabilidad completa.
- Evitar efectos secundarios sobre otras ofertas.

---

## MED-005. Escalamiento al usuario

Cuando la excepción no pueda resolverse automáticamente o implique una decisión estratégica, la automatización deberá solicitar la intervención del usuario antes de continuar.

Durante este periodo, la oferta permanecerá en un estado compatible con la espera de dicha decisión.

---

## MED-006. Conservación del contexto

Toda excepción deberá conservar el contexto completo en el que ocurrió.

Como mínimo deberá mantenerse disponible:

- Estado de la oferta.
- Información evaluada.
- Reglas aplicadas.
- Resultados obtenidos.
- Momento en que ocurrió la excepción.

Esta información permitirá su análisis, auditoría y eventual reprocesamiento.

---

## MED-007. Continuidad del procesamiento

Una vez resuelta la excepción, la automatización deberá continuar el procesamiento desde la etapa más adecuada, evitando repetir procesos correctamente finalizados.

Cuando no sea posible continuar, la oferta seguirá el flujo definido para finalización o intervención del usuario.

---

## MED-008. Protección de la integridad

Ninguna excepción podrá provocar:

- Pérdida de información.
- Corrupción de datos.
- Estados incompatibles.
- Decisiones contradictorias.
- Omisión de registros obligatorios.

La integridad de la información tendrá prioridad sobre la continuidad del procesamiento.

---

## MED-009. Registro obligatorio

Toda excepción deberá registrarse como parte del historial de la oferta.

Como mínimo deberá conservarse la siguiente información:

- Identificador de la oferta.
- Tipo de excepción.
- Descripción.
- Fecha y hora.
- Estado en que ocurrió.
- Regla involucrada, cuando aplique.
- Estrategia aplicada.
- Resultado obtenido.
- Responsable de la resolución.

---

## MED-010. Mejora continua

La información registrada sobre las excepciones deberá utilizarse para identificar oportunidades de mejora del modelo de decisiones.

La incorporación de nuevas estrategias de resolución requerirá la actualización de la documentación oficial del proyecto antes de su implementación.

---

## Principios generales para el manejo de excepciones

El manejo de excepciones deberá cumplir los siguientes principios:

- Detectar oportunamente las situaciones anómalas.
- Preservar la integridad de la información.
- Mantener la continuidad del procesamiento cuando sea posible.
- Escalar únicamente las decisiones que no puedan resolverse automáticamente.
- Mantener trazabilidad completa.
- Garantizar la reproducibilidad de las estrategias aplicadas.
- Evitar decisiones improvisadas o no documentadas.
- Mantener independencia respecto de la tecnología utilizada para su implementación.

---

# 14. Decisiones reservadas al usuario

Las decisiones reservadas al usuario corresponden a aquellas que, por su naturaleza estratégica, personal, profesional o legal, no podrán ser ejecutadas automáticamente por la automatización.

Su propósito es preservar el control del usuario sobre las decisiones de mayor impacto, garantizando que la automatización actúe como un sistema de apoyo y no como un sustituto del criterio humano.

Ninguna regla de negocio, proceso automatizado o componente del sistema podrá modificar este principio sin la aprobación explícita del usuario y la correspondiente actualización de la documentación oficial del proyecto.

---

## DRU-001. Aprobación de una oportunidad laboral

La decisión de considerar una oferta como una oportunidad de interés será responsabilidad exclusiva del usuario.

La automatización podrá generar recomendaciones, análisis y puntuaciones, pero no podrá decidir en nombre del usuario si una oferta representa una oportunidad profesional.

---

## DRU-002. Descarte por criterios personales

El usuario podrá descartar una oferta por razones personales, estratégicas o cualquier otro criterio que no pueda determinarse objetivamente mediante las reglas del sistema.

Entre otros motivos podrán incluirse:

- Interés personal.
- Cultura organizacional.
- Reputación de la empresa.
- Experiencias previas.
- Preferencias profesionales.
- Información obtenida fuera de la automatización.

---

## DRU-003. Modificación de prioridades

El usuario podrá modificar la prioridad asignada automáticamente a una oferta cuando considere que existen razones estratégicas para hacerlo.

Toda modificación deberá conservar el valor original calculado por la automatización como parte del historial.

---

## DRU-004. Aprobación de la candidatura

La decisión de preparar una candidatura definitiva para una oferta será responsabilidad exclusiva del usuario.

La automatización podrá generar todos los insumos necesarios para facilitar dicha decisión, pero no podrá asumirla automáticamente.

---

## DRU-005. Autorización para compartir información

Toda acción que implique enviar, publicar o compartir información personal o profesional del usuario con terceros requerirá autorización explícita.

Entre otras acciones se incluyen:

- Envío de hoja de vida.
- Envío de portafolio.
- Diligenciamiento de formularios.
- Envío de correos electrónicos.
- Compartición de documentos.

---

## DRU-006. Modificación del perfil profesional

Toda modificación relacionada con el perfil profesional del usuario deberá ser aprobada expresamente por este.

Entre otros elementos:

- Hoja de vida.
- Perfil profesional.
- Portafolio.
- Experiencia laboral.
- Competencias.
- Certificaciones.
- Preferencias laborales.

La automatización podrá proponer cambios, pero nunca aplicarlos automáticamente.

---

## DRU-007. Modificación de reglas de negocio

Toda modificación sobre el modelo de decisiones deberá ser autorizada por el usuario.

Esto incluye, entre otros:

- Criterios de evaluación.
- Reglas de aceptación.
- Reglas de descarte.
- Sistema de puntuación.
- Umbrales.
- Priorización.
- Casos especiales.
- Excepciones.

Ningún componente del sistema podrá alterar estas reglas de forma autónoma.

---

## DRU-008. Reprocesamiento excepcional

Cuando una oferta requiera un reprocesamiento que no pueda justificarse mediante las reglas automáticas existentes, la decisión deberá ser tomada por el usuario.

La autorización deberá quedar registrada junto con el motivo correspondiente.

---

## DRU-009. Incorporación de nuevas fuentes de empleo

La decisión de incorporar una nueva fuente de empleo al sistema corresponderá exclusivamente al usuario.

La automatización no podrá integrar nuevas plataformas, APIs o sitios web por iniciativa propia.

---

## DRU-010. Incorporación de nuevas funcionalidades

Toda ampliación funcional de la automatización requerirá aprobación previa del usuario antes de ser implementada.

Esto incluye modificaciones que alteren el alcance funcional originalmente aprobado para el proyecto.

---

## Principios generales de las decisiones reservadas al usuario

Todas las decisiones reservadas al usuario deberán cumplir los siguientes principios:

- Requerir autorización explícita antes de su ejecución.
- Mantener trazabilidad completa.
- Conservar el historial de las decisiones tomadas.
- Tener prioridad sobre las recomendaciones generadas por la automatización cuando exista conflicto.
- No podrán automatizarse sin una modificación formal de la documentación del proyecto.
- Preservar la autonomía del usuario sobre las decisiones estratégicas.
- Mantener independencia respecto de la tecnología utilizada para implementar la automatización.

---

# 15. Trazabilidad y auditoría

La trazabilidad y la auditoría del modelo de decisiones establecen los mecanismos necesarios para registrar, reconstruir, verificar y justificar todas las decisiones tomadas durante el procesamiento de una oferta de empleo.

Su propósito es garantizar la transparencia, reproducibilidad y verificabilidad del modelo de decisiones, permitiendo conocer en cualquier momento cómo, cuándo, por qué y con base en qué información se tomó una decisión.

Toda decisión emitida por la automatización o por el usuario deberá conservar la información necesaria para permitir auditorías, revisiones y reprocesamientos futuros.

---

## TA-001. Registro obligatorio de decisiones

Toda decisión deberá generar un registro permanente dentro del historial de la oferta.

No podrán existir decisiones que no se encuentren registradas.

---

## TA-002. Identificación única

Cada decisión deberá poseer un identificador único e inmutable que permita referenciarla durante todo el ciclo de vida de la oferta.

Dicho identificador deberá conservarse incluso cuando la decisión sea reemplazada por una decisión posterior.

---

## TA-003. Información mínima registrada

Como mínimo, toda decisión deberá registrar la siguiente información:

- Identificador de la decisión.
- Identificador de la oferta.
- Tipo de decisión.
- Estado anterior.
- Estado resultante.
- Fecha y hora.
- Responsable de la decisión.
- Resultado obtenido.
- Justificación.
- Reglas aplicadas.
- Versión del modelo de decisiones utilizada.

---

## TA-004. Trazabilidad de las reglas

Toda decisión deberá mantener la relación con las reglas de negocio utilizadas durante su evaluación.

Esto permitirá reconstruir posteriormente el razonamiento seguido por la automatización para llegar al resultado obtenido.

---

## TA-005. Trazabilidad de las entradas

La automatización deberá conservar la referencia a las entradas utilizadas durante el proceso de decisión.

Entre otras:

- Información de la oferta.
- Perfil profesional.
- Configuración vigente.
- Reglas de negocio.
- Resultados intermedios.
- Decisiones previas relevantes.

---

## TA-006. Versionado del modelo de decisiones

Toda decisión deberá asociarse a la versión vigente del modelo de decisiones y de las reglas de negocio utilizadas al momento de su ejecución.

Esto garantizará la reproducibilidad histórica de las decisiones.

---

## TA-007. Historial de decisiones

Cuando una oferta sea reevaluada, repriorizada o reprocesada, el sistema deberá conservar todas las decisiones anteriores.

Las decisiones históricas no podrán eliminarse ni sobrescribirse.

---

## TA-008. Auditoría de modificaciones

Toda modificación realizada sobre una decisión previamente registrada deberá generar un nuevo evento de auditoría.

Como mínimo deberá conservarse:

- Decisión anterior.
- Nueva decisión.
- Motivo del cambio.
- Responsable.
- Fecha y hora.

---

## TA-009. Reconstrucción del proceso

La información registrada deberá ser suficiente para reconstruir completamente el proceso de decisión de cualquier oferta.

La reconstrucción deberá permitir identificar:

- Qué información fue evaluada.
- Qué reglas fueron aplicadas.
- Qué resultados se obtuvieron.
- Qué decisión se tomó.
- Qué transición de estado se ejecutó.

---

## TA-010. Disponibilidad para auditoría

La información utilizada para la trazabilidad deberá permanecer disponible durante todo el tiempo definido por la política de conservación del proyecto.

Su consulta no deberá alterar el estado de las ofertas ni el funcionamiento del sistema.

---

## Principios generales de la trazabilidad y auditoría

La trazabilidad y la auditoría del modelo de decisiones deberán cumplir los siguientes principios:

- Integridad de los registros.
- Inmutabilidad de la información histórica.
- Reproducibilidad de las decisiones.
- Transparencia del proceso de decisión.
- Identificación única de cada decisión.
- Conservación del historial completo.
- Disponibilidad para auditorías futuras.
- Independencia respecto de la tecnología utilizada para su implementación.

---

# 16. Restricciones del modelo de decisiones

Las restricciones del modelo de decisiones establecen los límites que deberán respetarse durante el diseño, implementación, operación y evolución del motor de decisiones de la automatización.

Su propósito es garantizar que todas las decisiones permanezcan alineadas con los objetivos del proyecto, preservando la integridad del procesamiento, la autonomía del usuario y la consistencia del sistema.

Estas restricciones serán de cumplimiento obligatorio para todos los componentes que participen en la toma de decisiones.

---

## RMD-001. Decisiones basadas únicamente en reglas documentadas

El modelo de decisiones únicamente podrá emitir decisiones respaldadas por reglas de negocio previamente documentadas y aprobadas.

No se permitirá la utilización de reglas implícitas, comportamientos no documentados o criterios arbitrarios.

---

## RMD-002. Prohibición de aprendizaje autónomo

La automatización no podrá modificar por sí misma:

- Reglas de negocio.
- Criterios de evaluación.
- Sistema de puntuación.
- Umbrales.
- Prioridades.
- Restricciones.
- Estrategias de decisión.

Toda modificación requerirá aprobación explícita del usuario y la actualización de la documentación correspondiente.

---

## RMD-003. Prohibición de decisiones estratégicas automáticas

El modelo de decisiones no podrá ejecutar automáticamente decisiones reservadas al usuario.

Entre otras:

- Aprobar una candidatura.
- Enviar información a terceros.
- Modificar el perfil profesional.
- Alterar preferencias laborales.
- Incorporar nuevas funcionalidades.
- Incorporar nuevas fuentes de empleo.

---

## RMD-004. Respeto por el flujo funcional

Toda decisión deberá respetar el flujo funcional oficial de la automatización.

No estarán permitidas transiciones que:

- Omitan etapas obligatorias.
- Alteren el ciclo de vida de una oferta.
- Generen estados incompatibles.
- Contradigan las reglas funcionales del proyecto.

---

## RMD-005. Protección de la información

El modelo de decisiones no podrá modificar, eliminar o sobrescribir la información original obtenida de las fuentes de empleo.

Toda evaluación deberá realizarse sobre información validada o estructuras derivadas cuando corresponda.

---

## RMD-006. Prohibición de pérdida de trazabilidad

Ninguna decisión podrá ejecutarse si impide reconstruir posteriormente el proceso que condujo al resultado obtenido.

Toda decisión deberá conservar su historial y su justificación.

---

## RMD-007. Restricción de decisiones ambiguas

Cuando la información disponible no permita determinar una decisión objetiva, la automatización no deberá emitir decisiones basadas en suposiciones.

En estos casos deberá aplicar las reglas para información incompleta, casos especiales o manejo de excepciones, según corresponda.

---

## RMD-008. Independencia tecnológica

El comportamiento del modelo de decisiones no deberá depender de una herramienta, lenguaje de programación, proveedor o modelo de inteligencia artificial específico.

La implementación tecnológica no podrá alterar el significado de las reglas de negocio.

---

## RMD-009. Configuración centralizada

Toda configuración relacionada con el modelo de decisiones deberá administrarse desde mecanismos centralizados.

No deberán existir reglas, umbrales o parámetros distribuidos entre diferentes componentes de la automatización.

---

## RMD-010. Compatibilidad evolutiva

Toda modificación realizada sobre el modelo de decisiones deberá preservar la compatibilidad con:

- El Glosario del Proyecto.
- Los Requisitos Funcionales.
- Los Requisitos No Funcionales.
- El flujo funcional.
- El ciclo de vida de las ofertas.
- Las reglas previamente aprobadas.

Cuando una modificación rompa dicha compatibilidad, deberá documentarse y aprobarse antes de su implementación.

---

## Principios generales de las restricciones

Las restricciones del modelo de decisiones deberán cumplir los siguientes principios:

- Preservar la integridad del modelo.
- Limitar el comportamiento de la automatización a reglas previamente definidas.
- Garantizar la autonomía del usuario sobre las decisiones estratégicas.
- Mantener la coherencia con toda la documentación oficial del proyecto.
- Favorecer la mantenibilidad y la escalabilidad del sistema.
- Garantizar decisiones objetivas, reproducibles y auditables.
- Mantener independencia respecto de la tecnología utilizada para la implementación.

---

# 17. Criterios de aceptación

El modelo de decisiones se considerará aprobado cuando se verifique, mediante evidencia objetiva, que cumple los principios, reglas, restricciones y comportamientos definidos en el presente documento.

Los siguientes criterios de aceptación servirán como referencia para validar el diseño, la implementación, las pruebas y la evolución del modelo de decisiones.

---

### CAD-001. Consistencia de las decisiones

El modelo deberá producir la misma decisión cuando procese las mismas entradas utilizando las mismas reglas, configuraciones y versión del modelo de decisiones.

---

### CAD-002. Aplicación correcta de las reglas

Toda decisión deberá estar respaldada por una o más reglas de negocio previamente documentadas.

No deberán existir decisiones generadas sin una justificación verificable.

---

### CAD-003. Correcta clasificación de las ofertas

El modelo deberá clasificar correctamente las ofertas conforme a los criterios de evaluación, el sistema de puntuación y las reglas de priorización definidas.

---

### CAD-004. Aplicación de reglas de aceptación y descarte

Las ofertas deberán continuar o finalizar su procesamiento únicamente cuando cumplan las condiciones establecidas por las reglas de aceptación y descarte.

---

### CAD-005. Respeto por las decisiones del usuario

Toda decisión reservada al usuario deberá requerir su autorización explícita antes de ejecutarse.

La automatización no deberá sustituir ni modificar dichas decisiones.

---

### CAD-006. Correcta gestión de casos especiales

El modelo deberá identificar y tratar adecuadamente los casos especiales definidos, aplicando las estrategias correspondientes sin comprometer la consistencia del procesamiento.

---

### CAD-007. Correcto manejo de excepciones

Las excepciones deberán detectarse, registrarse y resolverse conforme a las estrategias documentadas, preservando la integridad de la información y la continuidad del procesamiento cuando sea posible.

---

### CAD-008. Correcta ejecución de las transiciones

Toda transición de estado deberá respetar el flujo funcional, el ciclo de vida de las ofertas y las reglas de transición definidas por el modelo de decisiones.

No deberán producirse transiciones incompatibles o no documentadas.

---

### CAD-009. Trazabilidad completa

Toda decisión deberá conservar la información necesaria para reconstruir posteriormente:

- La información evaluada.
- Las reglas aplicadas.
- La decisión obtenida.
- La transición ejecutada.
- El responsable de la decisión.

---

### CAD-010. Auditabilidad

El modelo deberá permitir justificar cualquier decisión mediante evidencia objetiva registrada durante el procesamiento.

La información almacenada deberá ser suficiente para realizar auditorías técnicas y funcionales.

---

### CAD-011. Reproducibilidad

Toda decisión deberá poder reproducirse utilizando la misma versión del modelo, las mismas reglas de negocio, la misma configuración y las mismas entradas.

---

### CAD-012. Compatibilidad documental

El modelo de decisiones deberá mantenerse completamente alineado con:

- El Glosario del Proyecto.
- Los Requisitos Funcionales.
- Los Requisitos No Funcionales.
- El Flujo Funcional.
- El Ciclo de Vida de las Ofertas.
- La documentación oficial vigente del proyecto.

---

### CAD-013. Escalabilidad

La incorporación de nuevos criterios, reglas, excepciones o casos especiales deberá realizarse sin alterar el comportamiento de las decisiones existentes, salvo cuando dicha modificación haya sido previamente documentada y aprobada.

---

### CAD-014. Independencia tecnológica

El comportamiento del modelo deberá mantenerse independiente de la tecnología utilizada para su implementación.

La sustitución de herramientas, servicios o componentes tecnológicos no deberá modificar las reglas de decisión.

---

### CAD-015. Cumplimiento integral

El modelo de decisiones cumplirá este documento cuando todos los criterios anteriores puedan verificarse mediante pruebas, revisiones documentales o evidencias obtenidas durante la operación de la automatización.

---

## Principio general de aceptación

La aprobación del modelo de decisiones requerirá demostrar que todas las decisiones emitidas por la automatización son:

- Objetivas.
- Consistentes.
- Reproducibles.
- Trazables.
- Auditables.
- Basadas en reglas documentadas.
- Compatibles con el resto de la documentación oficial del proyecto.

---

# 18. Índice de reglas de decisión

El presente documento organiza sus elementos mediante identificadores únicos e inmutables, con el fin de facilitar su consulta, implementación, trazabilidad, auditoría y mantenimiento.

Cada identificador constituye una referencia oficial del modelo de decisiones y podrá utilizarse en la documentación, la arquitectura, el desarrollo, las pruebas y la operación de la automatización.

Los identificadores definidos en este documento no deberán reutilizarse, modificarse ni reasignarse una vez el documento haya sido aprobado.

---

## Índice de principios del modelo de decisiones

| Rango | Categoría |
|--------|-----------|
| PMD-001 – PMD-015 | Principios del modelo de decisiones |

---

## Índice de arquitectura del modelo de decisiones

| Rango | Categoría |
|--------|-----------|
| AMD-001 – AMD-005 | Componentes del modelo de decisiones |

---

## Índice de entradas del modelo de decisiones

| Rango | Categoría |
|--------|-----------|
| EDM-001 – EDM-008 | Entradas del modelo de decisiones |

---

## Índice de criterios de evaluación

| Rango | Categoría |
|--------|-----------|
| CE-001 – CE-012 | Criterios de evaluación |

---

## Índice del sistema de puntuación

| Rango | Categoría |
|--------|-----------|
| SP-001 – SP-011 | Sistema de puntuación |

---

## Índice de reglas de aceptación

| Rango | Categoría |
|--------|-----------|
| RA-001 – RA-010 | Reglas de aceptación |

---

## Índice de reglas de descarte

| Rango | Categoría |
|--------|-----------|
| RD-001 – RD-010 | Reglas de descarte |

---

## Índice de priorización de ofertas

| Rango | Categoría |
|--------|-----------|
| PO-001 – PO-010 | Priorización de ofertas |

---

## Índice de reglas de transición de decisiones

| Rango | Categoría |
|--------|-----------|
| RTD-001 – RTD-010 | Reglas de transición de decisiones |

---

## Índice de casos especiales

| Rango | Categoría |
|--------|-----------|
| CEE-001 – CEE-010 | Casos especiales |

---

## Índice de manejo de excepciones

| Rango | Categoría |
|--------|-----------|
| MED-001 – MED-010 | Manejo de excepciones |

---

## Índice de decisiones reservadas al usuario

| Rango | Categoría |
|--------|-----------|
| DRU-001 – DRU-010 | Decisiones reservadas al usuario |

---

## Índice de trazabilidad y auditoría

| Rango | Categoría |
|--------|-----------|
| TA-001 – TA-010 | Trazabilidad y auditoría |

---

## Índice de restricciones del modelo de decisiones

| Rango | Categoría |
|--------|-----------|
| RMD-001 – RMD-010 | Restricciones del modelo de decisiones |

---

## Índice de criterios de aceptación

| Rango | Categoría |
|--------|-----------|
| CAD-001 – CAD-015 | Criterios de aceptación |

---

## Resumen del documento

| Capítulo | Contenido |
|----------|-----------|
| 1 | Propósito del documento |
| 2 | Principios del modelo de decisiones |
| 3 | Arquitectura del modelo de decisiones |
| 4 | Tipos de decisiones |
| 5 | Entradas del modelo de decisiones |
| 6 | Criterios de evaluación |
| 7 | Sistema de puntuación |
| 8 | Reglas de aceptación |
| 9 | Reglas de descarte |
| 10 | Priorización de ofertas |
| 11 | Reglas de transición de decisiones |
| 12 | Casos especiales |
| 13 | Manejo de excepciones |
| 14 | Decisiones reservadas al usuario |
| 15 | Trazabilidad y auditoría |
| 16 | Restricciones del modelo de decisiones |
| 17 | Criterios de aceptación |
| 18 | Índice de reglas de decisión |

---

## Principios del índice

El índice de reglas de decisión deberá cumplir los siguientes principios:

- Mantener identificadores únicos e inmutables.
- Facilitar la navegación y consulta del documento.
- Servir como referencia oficial para la implementación del motor de decisiones.
- Permitir la trazabilidad entre documentación, arquitectura, desarrollo y pruebas.
- Facilitar la incorporación de nuevas reglas sin alterar los identificadores existentes.
- Mantener consistencia con el resto de la documentación oficial del proyecto.
