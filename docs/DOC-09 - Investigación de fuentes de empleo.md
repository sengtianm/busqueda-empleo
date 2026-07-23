# Documento 9 - Investigación de Fuentes de Empleo

## 1. Propósito del documento

El presente documento tiene como propósito investigar, analizar y documentar de manera objetiva las características de las fuentes de empleo que podrán ser utilizadas por la automatización de búsqueda de empleo.

Su finalidad es proporcionar una base técnica, funcional y estratégica que permita determinar la viabilidad de utilizar una plataforma como fuente oficial de información para el proyecto, considerando sus mecanismos de acceso, restricciones, riesgos, estabilidad, posibilidades de automatización y compatibilidad con los objetivos definidos en la documentación oficial.

Las conclusiones contenidas en este documento servirán como fundamento para las decisiones de arquitectura, implementación y evolución de la automatización, evitando que dichas decisiones se basen en suposiciones o información no verificada.

Para la presente versión del proyecto, el alcance de este documento se limita exclusivamente al análisis de la plataforma **LinkedIn**, la cual constituye la única fuente de empleo que será evaluada y documentada para la primera versión (MVP) de la automatización.

Toda conclusión, decisión o recomendación incluida en este documento deberá estar respaldada por un análisis previo y, cuando corresponda, por la investigación de la información técnica, funcional o legal necesaria para garantizar su validez.

Las decisiones adoptadas en este documento serán de cumplimiento obligatorio para los documentos posteriores relacionados con la arquitectura, el desarrollo y la operación de la automatización, salvo que sean modificadas mediante una actualización formal de la documentación del proyecto.

---

## 2. Principios de la investigación de fuentes

Los siguientes principios establecen las reglas que deberán regir la investigación, evaluación, selección y documentación de las fuentes de empleo utilizadas por la automatización de búsqueda de empleo.

Su propósito es garantizar que todas las decisiones relacionadas con una fuente de información se fundamenten en criterios objetivos, verificables y alineados con la documentación oficial del proyecto.

---

### PIF-001. Investigación basada en evidencia

Toda conclusión incorporada al presente documento deberá estar respaldada por información previamente investigada y verificada.

No se documentarán suposiciones ni afirmaciones sin sustento.

---

### PIF-002. Objetividad

La evaluación de una fuente de empleo deberá realizarse utilizando criterios técnicos, funcionales y operativos, evitando decisiones basadas en preferencias personales.

---

### PIF-003. Cumplimiento legal

Toda fuente de empleo deberá analizarse considerando sus términos de uso, políticas aplicables y restricciones legales relacionadas con la obtención de información.

---

### PIF-004. Protección de la cuenta del usuario

Las decisiones adoptadas deberán priorizar la seguridad y preservación de la cuenta utilizada por el usuario durante la interacción con la plataforma.

No se aceptarán estrategias que incrementen injustificadamente el riesgo de restricciones, bloqueos o suspensión de la cuenta.

---

### PIF-005. Compatibilidad con el proyecto

La fuente evaluada deberá ser compatible con los objetivos, el alcance, los requisitos funcionales, los requisitos no funcionales y el modelo de decisiones definidos para la automatización.

---

### PIF-006. Independencia tecnológica

La evaluación de una fuente deberá realizarse sin depender de una herramienta, lenguaje de programación o tecnología específica.

---

### PIF-007. Trazabilidad

Toda decisión tomada durante la investigación deberá poder relacionarse con la evidencia, el análisis y la justificación correspondiente.

---

### PIF-008. Reproducibilidad

La información documentada deberá ser suficiente para que una futura revisión pueda reproducir el análisis y llegar a las mismas conclusiones, salvo que la plataforma haya cambiado.

---

### PIF-009. Actualización controlada

Cuando una plataforma modifique su funcionamiento, políticas o mecanismos de acceso, la investigación deberá revisarse y actualizarse antes de modificar la automatización.

---

### PIF-010. Prioridad de la estabilidad

Entre varias alternativas técnicamente viables, deberá priorizarse aquella que ofrezca mayor estabilidad, mantenibilidad y menor riesgo operativo para la automatización.

---

### PIF-011. Alcance controlado

El presente documento únicamente documentará la plataforma LinkedIn para la primera versión de la automatización.

La incorporación de nuevas fuentes requerirá una actualización formal del documento.

---

### PIF-012. Consistencia documental

Toda la información documentada deberá mantenerse coherente con el resto de la documentación oficial del proyecto.

---

## Principios generales de la investigación de fuentes

La investigación de fuentes deberá garantizar:

- Decisiones fundamentadas en evidencia.
- Evaluaciones objetivas y verificables.
- Cumplimiento de las restricciones legales y de uso.
- Protección de la cuenta del usuario.
- Compatibilidad con los objetivos del proyecto.
- Trazabilidad de todas las decisiones.
- Facilidad para actualizar la investigación.
- Evolución controlada de las fuentes oficiales del proyecto.

---

## 3. Criterios para seleccionar fuentes de empleo

La selección de una fuente de empleo para la automatización deberá fundamentarse en criterios objetivos, verificables y alineados con los objetivos generales del proyecto. La incorporación de una plataforma no dependerá únicamente de su popularidad o del volumen de ofertas disponibles, sino de su capacidad para integrarse de manera sostenible dentro de la arquitectura de la automatización.

Los criterios definidos en este capítulo deberán aplicarse a cualquier plataforma que sea evaluada en el futuro, garantizando que todas las decisiones relacionadas con la incorporación de nuevas fuentes mantengan un mismo estándar de calidad, seguridad, mantenibilidad y trazabilidad.

### 3.1 Cobertura de oportunidades

La plataforma deberá ofrecer una cantidad suficiente de oportunidades laborales compatibles con el perfil profesional objetivo del usuario.

El objetivo no consiste en obtener el mayor número posible de ofertas, sino en maximizar la disponibilidad de oportunidades potencialmente relevantes.

### 3.2 Calidad de la información

Las ofertas publicadas deberán proporcionar información suficiente para permitir una evaluación objetiva de su pertinencia.

Una oferta será considerada apta para continuar en el proceso únicamente cuando su contenido permita comprender, como mínimo, las responsabilidades del cargo, los conocimientos requeridos y los elementos necesarios para compararla con el perfil profesional del usuario.

Las ofertas cuya información resulte insuficiente deberán descartarse durante las etapas iniciales del proceso.

### 3.3 Compatibilidad con la estrategia de consultas

La plataforma deberá permitir construir estrategias de consultas suficientemente específicas para reducir el volumen de ofertas irrelevantes antes del proceso de evaluación.

La automatización diseñará y ejecutará dichas consultas utilizando filtros y criterios configurables orientados al perfil profesional del usuario.

### 3.4 Independencia del sistema de evaluación

La plataforma será utilizada exclusivamente como fuente de recuperación de oportunidades laborales.

La determinación de la relevancia de cada oferta será responsabilidad exclusiva del sistema de evaluación de la automatización, el cual aplicará criterios propios para clasificar, priorizar y decidir la continuidad de cada oportunidad.

### 3.5 Viabilidad técnica

Deberá existir un mecanismo técnicamente viable para obtener la información necesaria para la automatización.

La plataforma deberá permitir una integración que resulte compatible con los objetivos funcionales y técnicos del proyecto.

### 3.6 Seguridad de la interacción

La interacción con la plataforma deberá realizarse mediante mecanismos que minimicen el riesgo operativo para la cuenta del usuario.

Cuando la plataforma requiera autenticación para acceder a las funcionalidades necesarias, esta deberá implementarse de forma controlada, limitándose a las operaciones estrictamente requeridas y procurando reproducir el comportamiento esperado de un usuario legítimo.

### 3.7 Mantenibilidad

La plataforma deberá permitir una integración cuyo mantenimiento resulte razonable durante el ciclo de vida del proyecto.

Las modificaciones que la plataforma pueda sufrir a lo largo del tiempo deberán poder gestionarse sin comprometer la evolución general de la automatización.

### 3.8 Relación costo-beneficio

El esfuerzo requerido para integrar y mantener una plataforma deberá justificarse por el valor que aporta al proceso de búsqueda de oportunidades laborales.

No se incorporarán plataformas cuyo costo de mantenimiento resulte desproporcionado frente al incremento real de oportunidades relevantes.

### 3.9 Principios de aprobación

Una plataforma podrá aprobarse como fuente oficial del proyecto únicamente cuando cumpla simultáneamente los siguientes principios:

- Proporciona oportunidades laborales relevantes para el perfil profesional objetivo.
- Las ofertas contienen información suficiente para ser evaluadas objetivamente.
- Existe un mecanismo técnicamente viable para obtener la información requerida.
- Permite una interacción segura con un riesgo operativo aceptable para la cuenta del usuario.
- Su mantenimiento resulta sostenible durante el ciclo de vida del proyecto.
- El beneficio obtenido justifica el esfuerzo de integración y mantenimiento.

### 3.10 Aplicación al MVP

Como resultado del proceso de investigación realizado para la primera versión del proyecto, se determina que LinkedIn cumple los criterios establecidos en este capítulo y se aprueba como la única fuente oficial de oportunidades laborales para el MVP de la automatización.

Las futuras incorporaciones de nuevas plataformas deberán someterse al mismo proceso de investigación, análisis y evaluación antes de ser aprobadas como fuentes oficiales del proyecto.

---

## 4. Recomendaciones generales

Las siguientes recomendaciones deberán considerarse durante el análisis, selección e integración de cualquier plataforma de empleo dentro del proyecto.

### 4.1 Validar siempre mediante pruebas reales

Las decisiones relacionadas con una plataforma no deberán fundamentarse únicamente en documentación, investigaciones de terceros o información publicada por la comunidad.

Siempre que sea posible, deberán realizarse pruebas prácticas para verificar el comportamiento real de la plataforma antes de adoptar una decisión que afecte el diseño o funcionamiento de la automatización.

### 4.2 Priorizar evidencia sobre suposiciones

Cuando exista contradicción entre una investigación y el comportamiento observado durante las pruebas realizadas por el proyecto, prevalecerá la evidencia obtenida mediante validación práctica.

Toda modificación derivada de nuevas evidencias deberá documentarse y justificar la actualización de las decisiones previamente adoptadas.

### 4.3 Mantener independencia respecto a la plataforma

Las decisiones tomadas durante el análisis de una plataforma no deberán condicionar innecesariamente la evolución futura del proyecto.

Siempre que sea posible, las características particulares de una plataforma deberán tratarse como decisiones específicas de dicha plataforma y no como reglas generales de la automatización.

### 4.4 Minimizar el riesgo operativo

La interacción con cualquier plataforma deberá diseñarse procurando reducir el riesgo para la cuenta del usuario.

La automatización deberá limitar sus acciones a aquellas estrictamente necesarias para cumplir los objetivos definidos por el proyecto y evitar comportamientos que puedan incrementar el riesgo de restricciones o suspensiones.

### 4.5 Revisar periódicamente las decisiones adoptadas

Las plataformas de empleo evolucionan constantemente.

Por esta razón, las decisiones documentadas deberán revisarse cuando existan cambios relevantes en el funcionamiento de la plataforma, en sus mecanismos de acceso, en sus políticas o en cualquier otro aspecto que pueda afectar la automatización.

### 4.6 Mantener trazabilidad

Toda decisión relevante deberá poder relacionarse con la investigación, evidencia o prueba práctica que la originó.

La trazabilidad facilitará la actualización del proyecto cuando una plataforma modifique su comportamiento o cuando se incorporen nuevas fuentes de empleo.

### 4.7 Favorecer la evolución incremental

La incorporación de nuevas plataformas deberá realizarse de forma gradual.

Cada nueva fuente deberá investigarse, documentarse, evaluarse e integrarse individualmente antes de ampliar el alcance de la automatización.

---

## 5. Criterios de aceptación

El proceso de investigación y análisis de una plataforma de empleo se considerará finalizado únicamente cuando se hayan cumplido los siguientes criterios.

### 5.1 Investigación completada

Se habrá recopilado y analizado la información necesaria para comprender el funcionamiento de la plataforma en los aspectos relevantes para la automatización.

### 5.2 Validación práctica realizada

Las conclusiones más relevantes deberán haber sido verificadas mediante pruebas prácticas siempre que resulte posible.

Cuando no sea posible realizar una validación experimental, dicha limitación deberá quedar documentada.

### 5.3 Riesgos identificados

Deberán haberse identificado los principales riesgos técnicos, operativos y funcionales asociados con la utilización de la plataforma.

Cada riesgo deberá contar con una descripción clara y, cuando corresponda, con una estrategia de mitigación.

### 5.4 Mecanismos de acceso documentados

Deberán documentarse los mecanismos disponibles para acceder a la información necesaria para la automatización, incluyendo sus principales características, limitaciones y restricciones conocidas.

### 5.5 Restricciones documentadas

Deberán documentarse las restricciones técnicas, funcionales y de uso identificadas durante el proceso de investigación.

### 5.6 Viabilidad determinada

La investigación deberá concluir de forma explícita si la plataforma resulta viable o no para formar parte de la automatización, justificando dicha decisión con base en la evidencia recopilada.

### 5.7 Decisiones documentadas

Todas las decisiones relevantes derivadas del análisis deberán quedar documentadas y justificadas, permitiendo comprender las razones que sustentan la incorporación, descarte o tratamiento particular de la plataforma.

### 5.8 Trazabilidad garantizada

Las conclusiones, decisiones y recomendaciones deberán poder relacionarse con la evidencia, investigaciones o pruebas que las respaldan.

La documentación deberá permitir revisar o actualizar las decisiones cuando la plataforma modifique su funcionamiento o se obtenga nueva evidencia.

### 5.9 Documentación completa

El análisis de la plataforma se considerará aceptado únicamente cuando todos los capítulos definidos en el presente documento hayan sido completados, revisados y aprobados conforme a los objetivos del proyecto.

---

## 6. Índice del documento

### Estructura del documento

1. Propósito del documento.
2. Principios de la investigación de fuentes.
3. Criterios para seleccionar fuentes de empleo.
4. Recomendaciones generales.
5. Criterios de aceptación.
6. Índice del documento.

---

### Anexos

Los siguientes anexos forman parte de la documentación de soporte del presente documento y tienen como objetivo conservar la trazabilidad del proceso de investigación, análisis y toma de decisiones realizado durante la selección de plataformas de empleo.

**Anexo A.** Decisiones derivadas del análisis de la plataforma.

Contendrá las decisiones estratégicas adoptadas específicamente para la plataforma analizada, incluyendo las justificaciones que dieron origen a cada una de ellas.

**Anexo B.** Investigaciones realizadas.

Contendrá las investigaciones, análisis comparativos, resultados experimentales y demás evidencia recopilada durante el proceso de evaluación de la plataforma.

Cada nueva plataforma incorporada al proyecto deberá contar con sus propios anexos de decisiones e investigaciones, manteniendo independencia entre la documentación específica de cada fuente de empleo.
