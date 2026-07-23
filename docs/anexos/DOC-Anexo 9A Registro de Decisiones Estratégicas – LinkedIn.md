# Anexo A
# Registro de Decisiones Estratégicas – LinkedIn

## A.1 Objetivo

El presente anexo registra las decisiones estratégicas adoptadas durante el proceso de investigación, análisis y evaluación de LinkedIn como plataforma oficial de búsqueda de oportunidades laborales para la primera versión (MVP) de la automatización.

Cada decisión documenta una conclusión aprobada durante la elaboración del Documento 9 y constituye la posición oficial del proyecto respecto al uso de LinkedIn.

Este registro tiene como propósito mantener la trazabilidad entre la evidencia obtenida durante las investigaciones, las conclusiones alcanzadas y las decisiones que condicionarán el diseño y funcionamiento de la automatización.

Las decisiones incluidas en este anexo son específicas para LinkedIn. Si en el futuro se incorpora una nueva plataforma de empleo, deberá elaborarse un registro independiente de decisiones estratégicas para dicha plataforma.

---

# DE-LI-001. LinkedIn como plataforma oficial del MVP

## Capítulo relacionado

4. Plataformas objetivo.

## Decisión

LinkedIn queda establecida como la única plataforma oficial para la búsqueda de oportunidades laborales durante la primera versión (MVP) de la automatización.

La incorporación de otras plataformas queda fuera del alcance del MVP y será evaluada en futuras etapas del proyecto mediante el mismo proceso de investigación y análisis definido en el Documento 9.

## Justificación

La investigación realizada permitió concluir que LinkedIn ofrece el mejor equilibrio entre cobertura de oportunidades laborales, calidad de la información disponible, posibilidades técnicas de automatización y compatibilidad con los objetivos definidos para el proyecto.

Aunque presenta restricciones técnicas y operativas propias de la plataforma, los beneficios obtenidos superan las limitaciones identificadas.

## Implicaciones para el proyecto

- Todo el desarrollo del MVP se realizará exclusivamente sobre LinkedIn.
- El Documento 9 queda limitado al análisis de esta plataforma.
- La arquitectura del proyecto deberá permitir incorporar nuevas plataformas sin afectar las decisiones adoptadas para LinkedIn.

---

# DE-LI-002. Aprobación de LinkedIn como fuente oficial de oportunidades

## Capítulo relacionado

5. Análisis de cada plataforma.

## Decisión

LinkedIn queda aprobada como fuente oficial de oportunidades laborales para la automatización.

Las ofertas publicadas en la plataforma constituyen la fuente primaria de información que alimentará el proceso de descubrimiento de oportunidades del proyecto.

La plataforma será utilizada únicamente para recuperar ofertas de empleo y la evaluación de su pertinencia será responsabilidad exclusiva de la automatización.

## Justificación

El análisis funcional demostró que LinkedIn proporciona una cobertura amplia de oportunidades laborales, una estructura suficientemente consistente de las ofertas y un conjunto de filtros que permite construir estrategias de búsqueda alineadas con el perfil profesional del usuario.

La investigación también confirmó que la plataforma ofrece la información necesaria para realizar una evaluación inicial de la mayoría de las ofertas.

## Implicaciones para el proyecto

- LinkedIn se convierte en la fuente oficial de descubrimiento de oportunidades.
- La automatización utilizará la información recuperada como insumo para las etapas posteriores del proceso.
- Los algoritmos de recomendación de LinkedIn no determinarán qué ofertas continúan dentro del flujo de evaluación del proyecto.

---

# DE-LI-003. Mecanismo oficial de acceso a LinkedIn

## Capítulo relacionado

6. APIs y mecanismos de acceso.

## Decisión

La automatización accederá a LinkedIn mediante una sesión autenticada utilizando el mecanismo de interacción seleccionado durante la investigación.

No se utilizarán APIs oficiales de LinkedIn para la obtención de oportunidades laborales debido a que no proporcionan las funcionalidades requeridas por el proyecto.

La autenticación pasa a formar parte del funcionamiento normal de la automatización y deja de considerarse un mecanismo opcional.

## Justificación

Durante la investigación se analizaron los diferentes mecanismos disponibles para acceder a la información de LinkedIn Jobs.

Inicialmente se consideró viable trabajar sin autenticación; sin embargo, la validación práctica realizada posteriormente demostró que el buscador de empleos requiere iniciar sesión para acceder correctamente a las funcionalidades necesarias para el proyecto.

Con base en esta evidencia se descartó la estrategia de operación exclusivamente como visitante y se adoptó un modelo de acceso autenticado.

## Implicaciones para el proyecto

- La gestión de sesiones autenticadas pasa a formar parte del flujo operativo de la automatización.
- El diseño de la solución deberá contemplar mecanismos seguros para iniciar, mantener y finalizar la sesión del usuario.
- La protección de la cuenta utilizada por la automatización se convierte en un requisito prioritario del proyecto.

# DE-LI-004. Método oficial de extracción de información

## Capítulo relacionado

7. Métodos de extracción de información.

## Decisión

La obtención de oportunidades laborales se realizará mediante un proceso de extracción controlado, diseñado para recuperar únicamente la información necesaria para las etapas posteriores de la automatización.

La extracción se limitará a los datos requeridos para evaluar cada oferta y construir el registro interno de oportunidades, evitando recopilar información que no aporte valor al proceso.

La automatización obtendrá la información directamente desde las ofertas de empleo publicadas en LinkedIn, utilizando el mecanismo de acceso aprobado para el proyecto.

## Justificación

La investigación demostró que las ofertas publicadas en LinkedIn contienen, en la mayoría de los casos, la información necesaria para realizar una evaluación inicial de su pertinencia.

También evidenció que recopilar información adicional no aporta beneficios significativos y aumenta innecesariamente la complejidad, el tiempo de ejecución y el riesgo operativo.

Por esta razón, se adoptó un método de extracción orientado exclusivamente a la información relevante para el proceso de evaluación.

## Implicaciones para el proyecto

- La extracción se enfocará únicamente en la información necesaria para el proyecto.
- El proceso de descubrimiento evitará recopilar información irrelevante.
- Se reducirá el consumo de recursos durante la ejecución de la automatización.
- El proceso de mantenimiento será más simple al limitar la cantidad de información dependiente de la estructura de LinkedIn.

---

# DE-LI-005. Restricciones técnicas y legales

## Capítulo relacionado

8. Restricciones técnicas y legales.

## Decisión

El diseño de la automatización incorporará como restricciones del proyecto las limitaciones técnicas y operativas identificadas durante la investigación de LinkedIn.

Se reconoce que LinkedIn implementa mecanismos orientados a proteger la plataforma frente a comportamientos automatizados y que dichos mecanismos condicionan la forma en que la automatización deberá interactuar con el sitio.

En consecuencia, el proyecto adopta una estrategia de interacción conservadora, priorizando la estabilidad de la solución y la protección de la cuenta del usuario sobre la velocidad de ejecución o el volumen de información obtenida.

## Justificación

La investigación permitió identificar restricciones relacionadas con el acceso a la plataforma, la automatización de acciones, los mecanismos de detección de comportamiento no humano y las limitaciones propias del funcionamiento de LinkedIn Jobs.

Estas restricciones no impiden desarrollar la automatización, pero sí condicionan la forma en que deberá implementarse.

Incorporarlas desde la etapa de análisis reduce el riesgo de rediseños posteriores y permite construir una solución más estable y sostenible.

## Implicaciones para el proyecto

- Las restricciones identificadas pasan a formar parte de los requisitos del proyecto.
- La arquitectura deberá diseñarse considerando dichas limitaciones desde el inicio.
- Las decisiones técnicas futuras deberán respetar estas restricciones.
- La estabilidad y la sostenibilidad tendrán prioridad frente a la rapidez de implementación.

---

# DE-LI-006. Términos de uso y criterios de cumplimiento

## Capítulo relacionado

9. Términos de uso y consideraciones de cumplimiento.

## Decisión

El proyecto reconoce que LinkedIn establece condiciones de uso y restricciones relacionadas con la automatización de su plataforma.

Como consecuencia, la automatización se diseñará procurando minimizar el riesgo operativo asociado a su utilización mediante una interacción limitada, controlada y alineada con un comportamiento similar al de un usuario legítimo.

La protección de la cuenta utilizada por la automatización se adopta como uno de los principios operativos del proyecto.

## Justificación

La investigación permitió identificar que el principal riesgo para la continuidad del proyecto no es la obtención de la información, sino las posibles restricciones que LinkedIn podría aplicar sobre una cuenta cuando detecta comportamientos incompatibles con el uso normal de la plataforma.

Por esta razón, las decisiones técnicas posteriores deberán orientarse a reducir dicho riesgo sin comprometer los objetivos funcionales de la automatización.

## Implicaciones para el proyecto

- La protección de la cuenta tendrá prioridad durante el diseño de la solución.
- Se evitarán estrategias de interacción agresivas o innecesarias.
- Las decisiones relacionadas con la automatización deberán evaluar siempre su impacto sobre el riesgo operativo.
- La continuidad del funcionamiento de la automatización prevalecerá sobre la maximización del volumen de consultas.

# DE-LI-007. Riesgos asociados al uso de LinkedIn

## Capítulo relacionado

10. Riesgos por plataforma.

## Decisión

El principal riesgo identificado para la utilización de LinkedIn no corresponde a la disponibilidad de la información, sino a la posibilidad de que la plataforma detecte un comportamiento automatizado y aplique restricciones sobre la cuenta utilizada por la automatización.

Como consecuencia, el proyecto adopta como criterio de diseño la mitigación del riesgo operativo antes que la maximización del rendimiento o de la velocidad de ejecución.

Los riesgos identificados se clasifican de la siguiente manera:

- Riesgo de restricción temporal o permanente de la cuenta.
- Riesgo de cambios en la interfaz o en el funcionamiento de LinkedIn.
- Riesgo de modificaciones en las políticas de uso de la plataforma.
- Riesgo de fallos ocasionados por cambios técnicos en el proceso de búsqueda de empleo.
- Riesgo de pérdida de estabilidad de la automatización como consecuencia de cambios introducidos por LinkedIn.

## Justificación

La investigación demostró que la mayoría de los riesgos relevantes no afectan la capacidad técnica para desarrollar la automatización, sino su continuidad operativa.

También permitió concluir que dichos riesgos pueden reducirse significativamente mediante decisiones de diseño adoptadas desde las primeras etapas del proyecto.

Por este motivo, la gestión del riesgo deja de ser una actividad posterior al desarrollo y pasa a formar parte de los principios fundamentales del diseño de la automatización.

## Implicaciones para el proyecto

- Todas las decisiones técnicas deberán considerar su impacto sobre el riesgo operativo.
- La arquitectura deberá facilitar la adaptación a cambios futuros de la plataforma.
- El comportamiento de la automatización deberá aproximarse al de un usuario legítimo.
- La protección de la cuenta tendrá prioridad sobre la velocidad de ejecución y el volumen de consultas.

---

# DE-LI-008. Frecuencia oficial de consulta

## Capítulo relacionado

11. Frecuencia recomendada de consulta.

## Decisión

La automatización ejecutará las consultas a LinkedIn con una frecuencia moderada, suficiente para identificar nuevas oportunidades laborales sin generar un patrón de actividad que incremente innecesariamente el riesgo para la cuenta del usuario.

La frecuencia de ejecución no se establecerá buscando el mayor número posible de consultas, sino el mejor equilibrio entre cobertura de oportunidades, actualidad de la información y seguridad operativa.

Durante el MVP no se realizarán consultas continuas ni ejecuciones con intervalos excesivamente cortos.

## Justificación

La investigación permitió concluir que una mayor frecuencia de consulta no garantiza una mejora proporcional en la calidad de las oportunidades obtenidas.

Por el contrario, incrementar innecesariamente el número de consultas aumenta el riesgo operativo sin aportar beneficios significativos para los objetivos del proyecto.

Se determinó que una estrategia de ejecución controlada ofrece un equilibrio más adecuado entre eficiencia y sostenibilidad.

## Implicaciones para el proyecto

- La frecuencia de ejecución se definirá como un parámetro configurable de la automatización.
- El sistema evitará patrones repetitivos de consulta.
- La estrategia de ejecución priorizará la estabilidad del proyecto sobre la actualización permanente de los resultados.
- La planificación de las ejecuciones formará parte de la estrategia de mitigación del riesgo operativo.

---

# DE-LI-009. Estrategia oficial de priorización de oportunidades

## Capítulo relacionado

12. Estrategia de priorización de fuentes.

## Decisión

La automatización utilizará una estrategia de consultas diseñada para maximizar la recuperación de oportunidades compatibles con el perfil profesional del usuario, reduciendo simultáneamente el volumen de ofertas irrelevantes.

La priorización de oportunidades no dependerá del algoritmo de recomendación de LinkedIn.

La plataforma se utilizará exclusivamente para recuperar ofertas de empleo; la decisión sobre cuáles continúan dentro del proceso será tomada por el sistema de evaluación definido por el proyecto.

La estrategia de consultas aprovechará los filtros disponibles en LinkedIn para reducir el número de ofertas que ingresan al proceso de evaluación, incluyendo, entre otros:

- palabras clave relacionadas con el perfil profesional;
- ubicación geográfica;
- modalidad de trabajo;
- fecha de publicación;
- nivel de experiencia;
- demás filtros que aporten valor al proceso de descubrimiento.

## Justificación

Las investigaciones demostraron que LinkedIn personaliza parcialmente los resultados utilizando información del perfil y del historial del usuario.

Sin embargo, también evidenciaron que una estrategia de consultas correctamente diseñada permite controlar de manera más consistente la calidad del conjunto inicial de oportunidades que serán evaluadas por la automatización.

Delegar la priorización al algoritmo de LinkedIn reduciría la transparencia del proceso y limitaría el control del proyecto sobre los criterios de selección.

## Implicaciones para el proyecto

- La estrategia de consultas se convierte en el primer mecanismo de filtrado de oportunidades.
- El sistema de evaluación será el responsable exclusivo de determinar la relevancia de cada oferta.
- La calidad del proceso de descubrimiento dependerá principalmente del diseño de las consultas y no de las recomendaciones de LinkedIn.
- La estrategia de consultas podrá evolucionar con el tiempo sin modificar la arquitectura general de la automatización.

---

# A.2 Observaciones finales

El presente registro reúne las decisiones estratégicas adoptadas durante el análisis de LinkedIn realizado en el Documento 9.

Cada decisión está respaldada por las investigaciones desarrolladas durante esta etapa del proyecto y representa la posición oficial adoptada para la primera versión (MVP) de la automatización.

Estas decisiones constituyen el marco de referencia para el diseño de la arquitectura, la implementación de los componentes relacionados con LinkedIn y las futuras etapas del proyecto.

En caso de que LinkedIn modifique significativamente su funcionamiento, sus mecanismos de acceso o sus políticas de uso, las decisiones afectadas deberán revisarse utilizando la misma metodología de investigación aplicada durante la elaboración del Documento 9.

La incorporación de nuevas plataformas de empleo requerirá la elaboración de un registro independiente de decisiones estratégicas para cada plataforma, manteniendo la independencia entre los análisis y preservando la trazabilidad de las decisiones adoptadas.

