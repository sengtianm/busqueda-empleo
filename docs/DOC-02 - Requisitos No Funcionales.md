# Documento 2

# Requisitos No Funcionales

## 1. Propósito del documento

Este documento define los requisitos no funcionales de la automatización de búsqueda de empleo.

Su propósito es establecer las características de calidad, restricciones y criterios técnicos que deberán cumplir todos los componentes del sistema durante su diseño, implementación, operación y evolución.

A diferencia de los requisitos funcionales, que describen **qué hace** la automatización, los requisitos no funcionales establecen **cómo debe hacerlo**, garantizando atributos como rendimiento, confiabilidad, mantenibilidad, escalabilidad, seguridad y portabilidad.

Los requisitos definidos en este documento serán de cumplimiento obligatorio para todos los módulos y componentes del proyecto, y servirán como referencia para las decisiones de arquitectura, selección de herramientas, implementación y validación del sistema.

---

## 2. Principios de calidad del sistema

Los siguientes principios establecen los atributos de calidad que deberán cumplir todos los componentes de la automatización durante su diseño, desarrollo, implementación, operación y mantenimiento.

Estos principios complementan los requisitos funcionales y servirán como criterio para evaluar cualquier decisión de arquitectura, implementación o incorporación de nuevas funcionalidades.

---

### PC-001. Confiabilidad

La automatización deberá ejecutar sus procesos de forma consistente y predecible, produciendo resultados reproducibles bajo las mismas condiciones de entrada.

Las fallas deberán ser detectadas, registradas y tratadas mediante los mecanismos de recuperación definidos por el sistema.

---

### PC-002. Escalabilidad

La arquitectura deberá permitir incorporar nuevas fuentes de empleo, módulos, reglas de negocio y funcionalidades con un impacto mínimo sobre los componentes existentes.

La ampliación del sistema no deberá requerir rediseños significativos de la arquitectura.

---

### PC-003. Modularidad

Cada componente deberá tener una responsabilidad claramente definida y mantener el menor nivel posible de dependencia respecto a otros componentes.

La modificación o sustitución de un módulo no deberá afectar el funcionamiento de los demás, salvo en las interfaces previamente definidas.

---

### PC-004. Mantenibilidad

La automatización deberá diseñarse para facilitar la corrección de errores, la incorporación de mejoras y la actualización de componentes, minimizando el esfuerzo de mantenimiento.

Toda modificación deberá poder realizarse sin comprometer la estabilidad general del sistema.

---

### PC-005. Trazabilidad

Toda acción, decisión, cambio de estado, procesamiento y generación de información deberá poder reconstruirse mediante registros verificables.

La trazabilidad deberá mantenerse durante todo el ciclo de vida de cada oferta de empleo.

---

### PC-006. Consistencia

Los datos generados, almacenados y procesados deberán mantenerse coherentes entre todos los módulos del sistema.

No podrán existir estados, registros o resultados incompatibles entre sí.

---

### PC-007. Disponibilidad

La automatización deberá estar preparada para ejecutarse cada vez que el usuario o la planificación definida lo requieran, siempre que las dependencias externas se encuentren disponibles.

Las interrupciones temporales deberán gestionarse mediante estrategias de recuperación definidas.

---

### PC-008. Eficiencia

Los recursos computacionales deberán utilizarse de manera racional, evitando procesamiento innecesario, consultas redundantes y consumo excesivo de memoria, almacenamiento o tiempo de ejecución.

---

### PC-009. Seguridad

La información utilizada por la automatización deberá protegerse frente a accesos, modificaciones o divulgaciones no autorizadas.

Las credenciales, configuraciones sensibles y datos personales deberán almacenarse utilizando mecanismos adecuados de protección.

---

### PC-010. Portabilidad

La automatización deberá diseñarse de forma que pueda trasladarse a diferentes entornos de ejecución con el menor número posible de cambios.

Las dependencias específicas de una plataforma deberán mantenerse aisladas siempre que sea técnicamente posible.

---

### PC-011. Extensibilidad

El sistema deberá permitir incorporar nuevas capacidades sin alterar el comportamiento esperado de las funcionalidades existentes.

Toda ampliación deberá respetar las interfaces, estándares y reglas definidas por el proyecto.

---

### PC-012. Auditabilidad

Toda decisión automática deberá poder justificarse mediante evidencia objetiva registrada por el sistema.

Los registros deberán ser suficientes para comprender qué ocurrió, cuándo ocurrió, por qué ocurrió y cuál fue el resultado obtenido.

---

### PC-013. Simplicidad

Las soluciones implementadas deberán privilegiar la simplicidad sobre la complejidad innecesaria.

Cuando existan varias alternativas técnicamente viables, se priorizará aquella que facilite la comprensión, el mantenimiento y la evolución del sistema.

---

### PC-014. Uso de tecnologías gratuitas

La selección de herramientas, servicios y componentes deberá priorizar alternativas gratuitas que satisfagan los requisitos funcionales y no funcionales del proyecto.

Solo se considerarán tecnologías o servicios de pago cuando exista una justificación técnica documentada y su incorporación haya sido aprobada explícitamente por el usuario.

---

### PC-015. Documentación permanente

Toda decisión relevante relacionada con la arquitectura, las reglas de negocio, el funcionamiento, la implementación o la evolución del sistema deberá quedar documentada antes de su incorporación al proyecto.

Ningún componente crítico podrá depender exclusivamente de conocimiento implícito o no documentado.

---

## 3. Rendimiento

Los siguientes requisitos establecen el comportamiento esperado de la automatización en términos de eficiencia, tiempos de respuesta y utilización de recursos durante su operación.

El objetivo es garantizar que el sistema procese las ofertas de empleo de forma oportuna, consistente y eficiente, sin comprometer la estabilidad del resto de los componentes.

---

### RNF-001. Rendimiento general

La automatización deberá ejecutar cada proceso utilizando únicamente los recursos necesarios para completar sus tareas, evitando operaciones redundantes o innecesarias.

---

### RNF-002. Tiempo de respuesta por módulo

Cada módulo deberá completar su procesamiento dentro de un tiempo razonable para el volumen de información recibido.

Los tiempos máximos específicos se definirán en los documentos técnicos correspondientes, una vez se conozca la implementación de cada módulo.

---

### RNF-003. Procesamiento incremental

La automatización deberá procesar únicamente las nuevas ofertas o aquellas que requieran reprocesamiento, evitando ejecutar nuevamente procesos sobre información que ya se encuentre vigente y validada.

---

### RNF-004. Optimización de consultas

Las consultas realizadas a fuentes de empleo, bases de datos y demás dependencias externas deberán minimizar solicitudes repetidas e innecesarias.

Siempre que sea posible, deberá reutilizarse la información previamente obtenida.

---

### RNF-005. Optimización del procesamiento

Los módulos deberán ejecutar únicamente las tareas requeridas para el estado actual de cada oferta.

No deberán ejecutarse procesos que no aporten información adicional al flujo funcional.

---

### RNF-006. Uso eficiente de recursos

La automatización deberá optimizar el consumo de memoria, almacenamiento, procesamiento y ancho de banda durante toda su ejecución.

---

### RNF-007. Ejecución independiente

La ejecución de un módulo no deberá degradar significativamente el rendimiento de los demás módulos.

Cada componente deberá administrar sus propios recursos de forma controlada.

---

### RNF-008. Escalabilidad del rendimiento

El incremento en el número de ofertas procesadas deberá producir un crecimiento controlado en los tiempos de ejecución, evitando degradaciones desproporcionadas del rendimiento.

---

### RNF-009. Monitoreo del rendimiento

La automatización deberá registrar métricas que permitan medir, al menos:

- Tiempo de ejecución por módulo.
- Tiempo total de cada ejecución.
- Número de ofertas procesadas.
- Número de ofertas descartadas.
- Número de errores.
- Número de reintentos.
- Consumo aproximado de recursos cuando sea posible.

Estas métricas servirán para identificar oportunidades de optimización y verificar el cumplimiento de los requisitos de rendimiento.

---

### RNF-010. Degradación controlada

Cuando una dependencia externa presente lentitud o indisponibilidad parcial, la automatización deberá degradar su rendimiento de forma controlada, priorizando la continuidad del procesamiento sobre la interrupción completa del sistema, siempre que las reglas de negocio lo permitan.

---

## 4. Escalabilidad

Los siguientes requisitos establecen la capacidad de la automatización para crecer de forma controlada, permitiendo la incorporación de nuevas funcionalidades, fuentes de empleo, reglas de negocio y componentes sin comprometer la estabilidad, el rendimiento o la mantenibilidad del sistema.

La escalabilidad deberá considerarse como un principio transversal durante todo el ciclo de vida del proyecto.

---

### RNF-011. Escalabilidad modular

La automatización deberá estar compuesta por módulos independientes con responsabilidades claramente definidas, permitiendo incorporar, reemplazar o ampliar componentes sin afectar el funcionamiento del resto del sistema.

---

### RNF-012. Incorporación de nuevas fuentes

El sistema deberá permitir agregar nuevas fuentes de empleo sin requerir modificaciones significativas en los módulos encargados del procesamiento, evaluación, gestión o generación de insumos.

Cada nueva fuente deberá integrarse mediante mecanismos estandarizados definidos por la arquitectura del proyecto.

---

### RNF-013. Escalabilidad de reglas de negocio

Las reglas de evaluación, descarte, clasificación y priorización deberán administrarse de forma centralizada, permitiendo su ampliación o modificación sin alterar la lógica general de los procesos.

---

### RNF-014. Escalabilidad funcional

La incorporación de nuevas funcionalidades deberá realizarse mediante componentes o módulos adicionales, evitando modificaciones innecesarias sobre funcionalidades ya implementadas y aprobadas.

---

### RNF-015. Escalabilidad del procesamiento

La automatización deberá mantener un comportamiento estable a medida que aumente el número de ofertas, fuentes de empleo, reglas de negocio o procesos ejecutados.

El crecimiento del volumen de procesamiento no deberá requerir rediseños estructurales de la solución.

---

### RNF-016. Escalabilidad de datos

La arquitectura deberá soportar el crecimiento progresivo de la información almacenada, preservando la integridad, la trazabilidad y el acceso eficiente a los datos históricos.

---

### RNF-017. Escalabilidad de configuraciones

Las configuraciones del sistema deberán administrarse de manera centralizada, permitiendo incorporar nuevos parámetros sin afectar las configuraciones existentes ni requerir modificaciones en múltiples componentes.

---

### RNF-018. Compatibilidad con futuras integraciones

La arquitectura deberá facilitar la integración futura de nuevos servicios, herramientas, modelos de inteligencia artificial o componentes externos mediante interfaces claramente definidas y desacopladas.

---

### RNF-019. Escalabilidad del mantenimiento

El incremento del tamaño del proyecto no deberá producir un aumento desproporcionado en la complejidad del mantenimiento.

La organización del código, la documentación y la arquitectura deberán favorecer una evolución progresiva y controlada del sistema.

---

### RNF-020. Evolución controlada

Toda ampliación del sistema deberá respetar la arquitectura, los estándares, las convenciones y las reglas documentadas del proyecto, garantizando la compatibilidad con los componentes existentes y evitando la introducción de dependencias innecesarias.

---

## 5. Disponibilidad

Los siguientes requisitos establecen las condiciones bajo las cuales la automatización deberá encontrarse preparada para ejecutar sus procesos y recuperarse ante interrupciones que puedan afectar su funcionamiento.

La disponibilidad deberá garantizar la continuidad operativa del sistema dentro de las limitaciones impuestas por las dependencias externas y la infraestructura utilizada.

---

### RNF-021. Disponibilidad operativa

La automatización deberá estar preparada para iniciar y ejecutar sus procesos siempre que el usuario o la planificación definida lo soliciten y las dependencias necesarias se encuentren disponibles.

---

### RNF-022. Tolerancia a indisponibilidad externa

La indisponibilidad temporal de una fuente de empleo, servicio externo, modelo de inteligencia artificial o cualquier otra dependencia no deberá comprometer el funcionamiento general de la automatización.

El sistema deberá aislar el componente afectado y continuar ejecutando, siempre que las reglas del proceso lo permitan.

---

### RNF-023. Reanudación del procesamiento

Cuando un proceso sea interrumpido por una causa recuperable, la automatización deberá ser capaz de reanudar la ejecución desde el punto más adecuado, evitando repetir innecesariamente las tareas ya completadas.

---

### RNF-024. Recuperación controlada

La recuperación ante fallos deberá seguir estrategias previamente definidas y documentadas, priorizando la integridad de la información y la consistencia del procesamiento.

---

### RNF-025. Conservación del estado

Ante una interrupción, la automatización deberá conservar el estado operativo y el estado del ciclo de vida de cada oferta, permitiendo continuar el procesamiento sin pérdida de trazabilidad.

---

### RNF-026. Independencia de módulos

La indisponibilidad de un módulo no deberá impedir el funcionamiento de los demás módulos, salvo cuando exista una dependencia funcional explícitamente documentada.

---

### RNF-027. Protección frente a interrupciones inesperadas

La automatización deberá minimizar el impacto de cierres inesperados, reinicios del sistema o interrupciones de ejecución, preservando la información necesaria para continuar el procesamiento posteriormente.

---

### RNF-028. Gestión de dependencias externas

La disponibilidad de cada dependencia externa deberá verificarse antes de iniciar las operaciones que la requieran.

Cuando una dependencia no se encuentre disponible, el sistema deberá aplicar la estrategia correspondiente antes de marcar el proceso como fallido.

---

### RNF-029. Continuidad del servicio

Siempre que sea técnicamente posible, los procesos no afectados por una falla deberán continuar ejecutándose normalmente, evitando interrupciones globales de la automatización.

---

### RNF-030. Registro de indisponibilidades

Toda interrupción, degradación del servicio o indisponibilidad detectada deberá registrarse para facilitar la auditoría, el diagnóstico y la mejora continua del sistema.

---

## 6. Seguridad

Los siguientes requisitos establecen las condiciones necesarias para proteger la información, las configuraciones y los recursos utilizados por la automatización durante todo su ciclo de vida.

La seguridad deberá aplicarse de forma transversal en todos los módulos del sistema, preservando la confidencialidad, la integridad y la disponibilidad de la información.

---

### RNF-031. Protección de la información

Toda la información gestionada por la automatización deberá almacenarse y procesarse utilizando mecanismos que reduzcan el riesgo de pérdida, alteración o acceso no autorizado.

---

### RNF-032. Protección de credenciales

Las credenciales, claves de acceso, tokens, secretos y cualquier otro dato sensible deberán mantenerse separados del código fuente y almacenarse mediante mecanismos adecuados de protección.

En ningún caso deberán incorporarse directamente dentro del código de la automatización.

---

### RNF-033. Protección de configuraciones sensibles

Las configuraciones que puedan afectar la seguridad o el funcionamiento del sistema deberán administrarse de forma centralizada y contar con mecanismos que eviten modificaciones accidentales o no autorizadas.

---

### RNF-034. Integridad de la información

La automatización deberá preservar la integridad de los datos originales obtenidos desde las fuentes de empleo.

Toda transformación realizada durante el procesamiento deberá efectuarse sobre información derivada o estructuras normalizadas, manteniendo disponible la información original cuando sea necesario.

---

### RNF-035. Protección de datos personales

La información personal del usuario deberá utilizarse únicamente para los fines definidos por la automatización y limitarse a los procesos que realmente la requieran.

El sistema deberá minimizar la exposición innecesaria de datos personales durante el procesamiento y almacenamiento.

---

### RNF-036. Validación de entradas

Toda información proveniente de fuentes externas, configuraciones del usuario o servicios integrados deberá ser validada antes de ser utilizada por la automatización.

Ningún dato externo deberá asumirse como válido sin una verificación previa.

---

### RNF-037. Principio de mínimo acceso

Cada componente de la automatización deberá acceder únicamente a la información y recursos estrictamente necesarios para cumplir su responsabilidad funcional.

---

### RNF-038. Registro de eventos de seguridad

Toda situación que pueda comprometer la seguridad de la automatización deberá registrarse para facilitar su análisis, auditoría y posterior corrección.

---

### RNF-039. Recuperación segura

Los procesos de recuperación ante errores no deberán comprometer la integridad de la información ni omitir las validaciones definidas por el sistema.

Toda recuperación deberá preservar la consistencia de los datos y la trazabilidad del procesamiento.

---

### RNF-040. Evolución segura

La incorporación de nuevos módulos, servicios, dependencias o funcionalidades no deberá reducir el nivel de seguridad previamente alcanzado por la automatización.

Toda modificación deberá respetar los requisitos de seguridad definidos en este documento.

---

## 7. Confiabilidad

Los siguientes requisitos establecen las condiciones necesarias para garantizar que la automatización opere de forma consistente, predecible y confiable durante todo su ciclo de vida.

La confiabilidad deberá asegurar que los resultados obtenidos sean reproducibles, que el procesamiento mantenga su integridad y que cualquier situación anómala pueda identificarse, registrarse y gestionarse adecuadamente.

---

### RNF-041. Consistencia de ejecución

La automatización deberá producir resultados consistentes cuando procese la misma información bajo las mismas condiciones de entrada y configuración.

---

### RNF-042. Integridad del procesamiento

Cada oferta deberá completar únicamente las etapas del flujo funcional que correspondan a su estado, evitando omisiones, duplicaciones o ejecuciones fuera de secuencia.

---

### RNF-043. Prevención de corrupción de datos

El sistema deberá proteger la información frente a modificaciones parciales, inconsistentes o incompletas que puedan comprometer la integridad del procesamiento.

---

### RNF-044. Detección de anomalías

La automatización deberá identificar comportamientos anómalos durante la ejecución de los procesos y registrarlos para su posterior análisis, independientemente de que generen o no un error.

---

### RNF-045. Tolerancia a fallos recuperables

Cuando ocurra un fallo recuperable, la automatización deberá aplicar los mecanismos definidos para continuar el procesamiento sin comprometer la consistencia de la información.

---

### RNF-046. Reproducibilidad

Las decisiones automáticas y los resultados obtenidos deberán poder reproducirse utilizando las mismas entradas, configuraciones y reglas de negocio vigentes al momento de la ejecución.

---

### RNF-047. Protección del flujo funcional

Ninguna oferta deberá omitir etapas obligatorias, retroceder a estados incompatibles o avanzar mediante transiciones no definidas por el sistema, salvo cuando exista una regla documentada que lo autorice.

---

### RNF-048. Estabilidad operativa

La automatización deberá mantener un comportamiento estable durante ejecuciones prolongadas o repetitivas, evitando degradaciones que afecten la confiabilidad del procesamiento.

---

### RNF-049. Verificación de resultados

Al finalizar cada proceso, la automatización deberá verificar que se hayan generado correctamente los resultados esperados antes de continuar con la siguiente etapa del flujo funcional.

---

### RNF-050. Preservación de la trazabilidad

Toda acción ejecutada por la automatización deberá conservar la información necesaria para reconstruir posteriormente el procesamiento realizado, garantizando la confiabilidad de auditorías, revisiones y reprocesamientos.

---

## 8. Mantenibilidad

Los siguientes requisitos establecen las condiciones necesarias para que la automatización pueda corregirse, actualizarse, ampliarse y mantenerse de forma sencilla durante todo su ciclo de vida.

La mantenibilidad deberá minimizar el esfuerzo requerido para incorporar mejoras, corregir errores, sustituir componentes o adaptar la automatización a nuevos requerimientos.

---

### RNF-051. Arquitectura modular

La automatización deberá organizarse en módulos con responsabilidades claramente definidas y bajo acoplamiento, facilitando su mantenimiento y evolución independiente.

---

### RNF-052. Separación de responsabilidades

Cada componente deberá cumplir una única responsabilidad funcional claramente identificada.

La lógica de negocio, la configuración, el acceso a datos y la integración con servicios externos deberán mantenerse desacoplados siempre que sea técnicamente posible.

---

### RNF-053. Configuración centralizada

Las reglas de negocio, parámetros operativos, configuraciones generales y demás elementos modificables deberán administrarse desde ubicaciones centralizadas, evitando configuraciones duplicadas.

---

### RNF-054. Documentación actualizada

Toda modificación funcional, técnica o arquitectónica deberá reflejarse en la documentación oficial del proyecto antes de considerarse finalizada.

La documentación deberá mantenerse sincronizada con el comportamiento real de la automatización.

---

### RNF-055. Facilidad de actualización

La incorporación de mejoras, correcciones o nuevas funcionalidades deberá realizarse con el menor impacto posible sobre los componentes existentes.

Las actualizaciones no deberán requerir modificaciones innecesarias en módulos no relacionados.

---

### RNF-056. Sustitución de componentes

La arquitectura deberá facilitar el reemplazo de herramientas, librerías, servicios externos o componentes internos sin afectar significativamente el funcionamiento general del sistema.

---

### RNF-057. Reutilización

Los componentes, funciones, reglas y recursos comunes deberán diseñarse para favorecer su reutilización y evitar la duplicación de lógica dentro del proyecto.

---

### RNF-058. Consistencia de implementación

Todos los módulos deberán respetar las convenciones, estándares y lineamientos definidos para el proyecto, garantizando uniformidad en su organización y funcionamiento.

---

### RNF-059. Facilidad de diagnóstico

La estructura de la automatización deberá facilitar la identificación del origen de errores, comportamientos inesperados o problemas de rendimiento mediante mecanismos de trazabilidad y registros adecuados.

---

### RNF-060. Evolución controlada

Toda modificación realizada sobre la automatización deberá preservar la compatibilidad con la arquitectura, los requisitos funcionales, los requisitos no funcionales y las reglas documentadas del proyecto, evitando introducir deuda técnica innecesaria.

---

## 9. Portabilidad

Los siguientes requisitos establecen las condiciones necesarias para que la automatización pueda trasladarse, instalarse y ejecutarse en diferentes entornos con el menor esfuerzo posible, preservando su funcionamiento y comportamiento esperado.

La portabilidad deberá reducir la dependencia de plataformas, herramientas e infraestructuras específicas, favoreciendo la evolución futura del proyecto.

---

### RNF-061. Independencia del entorno

La automatización deberá diseñarse de forma que su funcionamiento dependa lo menos posible de características específicas del entorno donde sea ejecutada.

Las diferencias entre entornos deberán resolverse mediante mecanismos de configuración y no mediante modificaciones en la lógica del sistema.

---

### RNF-062. Configuración desacoplada

Las rutas, variables de entorno, credenciales, parámetros de ejecución y demás configuraciones deberán mantenerse completamente separadas del código fuente.

La migración entre entornos no deberá requerir cambios en los componentes funcionales.

---

### RNF-063. Independencia de la infraestructura

La arquitectura deberá minimizar las dependencias con infraestructura, hardware o servicios específicos, siempre que existan alternativas técnicamente viables que permitan cumplir los requisitos del proyecto.

---

### RNF-064. Compatibilidad con múltiples entornos

La automatización deberá diseñarse para facilitar su ejecución en distintos entornos compatibles, tales como equipos de desarrollo, pruebas o producción, manteniendo un comportamiento consistente.

---

### RNF-065. Sustitución de dependencias

La sustitución de librerías, herramientas, servicios externos o componentes internos deberá realizarse con un impacto mínimo sobre el resto de la automatización.

---

### RNF-066. Gestión centralizada de dependencias

Las dependencias utilizadas por el sistema deberán encontrarse claramente identificadas, documentadas y administradas de forma centralizada para facilitar su instalación, actualización o sustitución.

---

### RNF-067. Portabilidad de la información

Los datos generados por la automatización deberán almacenarse utilizando formatos abiertos, ampliamente soportados y fáciles de migrar, evitando dependencias innecesarias con tecnologías propietarias.

---

### RNF-068. Portabilidad de la documentación

Toda la documentación funcional, técnica y de configuración deberá mantenerse en formatos abiertos y ampliamente compatibles, facilitando su consulta y mantenimiento con diferentes herramientas.

---

### RNF-069. Reproducibilidad del entorno

La documentación del proyecto deberá permitir recrear completamente un entorno funcional siguiendo únicamente los procedimientos documentados, sin depender de conocimiento no registrado.

---

### RNF-070. Evolución tecnológica

La arquitectura deberá facilitar la incorporación futura de nuevas tecnologías o el reemplazo de componentes existentes sin requerir una reconstrucción significativa de la automatización.

---

## 10. Compatibilidad

Los siguientes requisitos establecen las condiciones necesarias para garantizar que los diferentes componentes de la automatización puedan interactuar correctamente entre sí y con las dependencias externas previstas durante el desarrollo del proyecto.

La compatibilidad deberá facilitar la integración, la evolución tecnológica y la incorporación de nuevos componentes sin comprometer el funcionamiento general del sistema.

---

### RNF-071. Compatibilidad entre módulos

Todos los módulos de la automatización deberán comunicarse mediante interfaces claramente definidas y compatibles con la arquitectura del sistema.

Ningún módulo deberá depender de implementaciones internas de otros componentes.

---

### RNF-072. Compatibilidad con dependencias externas

La automatización deberá utilizar mecanismos de integración compatibles con las plataformas, servicios y herramientas aprobadas para el proyecto, respetando las restricciones técnicas y operativas de cada una.

---

### RNF-073. Compatibilidad de formatos de datos

La información intercambiada entre módulos y dependencias externas deberá utilizar formatos estandarizados, consistentes y ampliamente soportados.

Las transformaciones necesarias deberán realizarse sin afectar la integridad de la información.

---

### RNF-074. Compatibilidad de configuraciones

Las configuraciones del sistema deberán mantenerse compatibles entre los distintos entornos de ejecución, evitando diferencias que alteren el comportamiento esperado de la automatización.

---

### RNF-075. Compatibilidad con futuras ampliaciones

La incorporación de nuevos módulos, fuentes de empleo, modelos de inteligencia artificial o servicios externos no deberá requerir modificaciones significativas en las interfaces ya establecidas.

---

### RNF-076. Compatibilidad de versiones

Cuando un componente dependa de versiones específicas de herramientas, librerías o servicios externos, dichas dependencias deberán encontrarse documentadas para garantizar la estabilidad del sistema.

---

### RNF-077. Compatibilidad de la documentación

La documentación funcional, técnica y de arquitectura deberá mantenerse alineada con la versión vigente de la automatización, evitando inconsistencias entre el comportamiento implementado y la documentación oficial.

---

### RNF-078. Compatibilidad del modelo de datos

Las modificaciones realizadas sobre las estructuras de datos deberán preservar la compatibilidad con los componentes que las utilicen o incluir mecanismos de migración previamente definidos.

---

### RNF-079. Compatibilidad evolutiva

Las mejoras incorporadas al sistema deberán mantener la compatibilidad con las funcionalidades existentes, salvo cuando una modificación incompatible haya sido previamente documentada, justificada y aprobada.

---

### RNF-080. Compatibilidad arquitectónica

Todo nuevo componente deberá respetar los principios, estándares, convenciones e interfaces definidos por la arquitectura oficial del proyecto antes de integrarse a la automatización.

---

## 11. Usabilidad

Los siguientes requisitos establecen las condiciones necesarias para que la automatización resulte fácil de comprender, configurar, utilizar y supervisar por parte del usuario.

La usabilidad deberá reducir la complejidad operativa del sistema, facilitando su administración sin requerir conocimientos técnicos innecesarios para las actividades habituales.

---

### RNF-081. Configuración sencilla

Las configuraciones habituales de la automatización deberán organizarse de forma clara y estructurada, permitiendo su comprensión y modificación sin afectar el resto del sistema.

---

### RNF-082. Información comprensible

Toda la información presentada al usuario deberá utilizar una terminología consistente con la documentación oficial del proyecto y describir claramente el estado, resultado o acción correspondiente.

---

### RNF-083. Consistencia de la interfaz

Los mecanismos utilizados para consultar información, revisar resultados, gestionar configuraciones o tomar decisiones deberán mantener un comportamiento uniforme en toda la automatización.

---

### RNF-084. Trazabilidad para el usuario

El usuario deberá poder identificar fácilmente el estado actual de cada oferta, las acciones realizadas, las decisiones tomadas y el resultado de cada etapa del procesamiento.

---

### RNF-085. Facilidad de administración

Las tareas habituales de administración, como actualizar configuraciones, revisar resultados, consultar registros o modificar reglas, deberán realizarse mediante procedimientos claramente definidos y documentados.

---

### RNF-086. Mensajes informativos

La automatización deberá proporcionar mensajes claros durante la ejecución de los procesos, indicando el progreso, las advertencias, los errores y las acciones requeridas por el usuario cuando corresponda.

---

### RNF-087. Reducción de la intervención manual

La automatización deberá minimizar la cantidad de acciones repetitivas que requieran intervención del usuario, reservando su participación únicamente para las decisiones estratégicas previamente definidas.

---

### RNF-088. Facilidad de aprendizaje

La organización de la automatización, su documentación y sus configuraciones deberán facilitar que un nuevo usuario comprenda su funcionamiento progresivamente sin depender de conocimiento implícito.

---

### RNF-089. Acceso a la información

La información relevante sobre cada oferta, ejecución, análisis o decisión deberá encontrarse organizada y disponible para su consulta de manera rápida y estructurada.

---

### RNF-090. Coherencia documental

La terminología utilizada por la automatización deberá mantenerse alineada con el Glosario del Proyecto y con el resto de la documentación oficial, garantizando una experiencia consistente para el usuario durante la administración y el seguimiento del sistema.

---

## 12. Restricciones tecnológicas

Los siguientes requisitos establecen las limitaciones y criterios tecnológicos que deberán respetarse durante el diseño, desarrollo, implementación y evolución de la automatización.

Estas restricciones buscan garantizar la coherencia técnica del proyecto, reducir la complejidad de mantenimiento y cumplir los principios definidos desde su planificación.

---

### RNF-091. Prioridad de herramientas gratuitas

La automatización deberá construirse utilizando herramientas, librerías, servicios y tecnologías gratuitas siempre que permitan cumplir los requisitos funcionales y no funcionales del proyecto.

---

### RNF-092. Incorporación de tecnologías de pago

Ninguna tecnología, servicio o herramienta de pago podrá incorporarse al proyecto sin una justificación técnica documentada y la aprobación explícita del usuario.

---

### RNF-093. Tecnologías ampliamente soportadas

Se deberán priorizar tecnologías con documentación suficiente, mantenimiento activo, comunidades consolidadas y amplio soporte, reduciendo el riesgo de obsolescencia o abandono.

---

### RNF-094. Uso de estándares abiertos

Siempre que sea técnicamente posible, la automatización deberá utilizar estándares abiertos para formatos de datos, protocolos de comunicación e intercambio de información.

---

### RNF-095. Minimización de dependencias

Se deberá evitar la incorporación de dependencias externas innecesarias.

Toda nueva dependencia deberá aportar un beneficio claramente justificado respecto a su costo de mantenimiento y complejidad.

---

### RNF-096. Independencia de proveedores

La arquitectura deberá minimizar el acoplamiento con proveedores, plataformas o servicios específicos, facilitando su sustitución cuando sea necesario.

---

### RNF-097. Compatibilidad con la arquitectura

Toda tecnología incorporada al proyecto deberá respetar la arquitectura, los principios de diseño y los estándares definidos en la documentación oficial.

---

### RNF-098. Gestión de versiones

Las versiones de las herramientas, librerías y componentes utilizados deberán mantenerse documentadas para garantizar la reproducibilidad del entorno y facilitar futuras actualizaciones.

---

### RNF-099. Evaluación previa de nuevas tecnologías

Antes de incorporar una nueva herramienta, servicio o dependencia, deberá evaluarse su compatibilidad con la arquitectura, su impacto sobre el mantenimiento, su escalabilidad y su continuidad a largo plazo.

---

### RNF-100. Restricción de modificaciones tecnológicas

La sustitución de tecnologías principales durante el desarrollo del proyecto solo podrá realizarse cuando exista una justificación técnica documentada y dicha decisión haya sido aprobada por el usuario.

---

## 13. Consumo esperado de recursos

Los siguientes requisitos establecen los criterios para el uso eficiente de los recursos computacionales durante la ejecución de la automatización.

El objetivo es garantizar que el sistema mantenga un funcionamiento estable y eficiente, evitando el consumo innecesario de recursos y facilitando su operación en entornos con capacidades limitadas.

---

### RNF-101. Uso eficiente de recursos

La automatización deberá utilizar únicamente los recursos necesarios para ejecutar cada proceso, evitando consumo innecesario de memoria, procesamiento, almacenamiento y ancho de banda.

---

### RNF-102. Optimización del procesamiento

Los módulos deberán ejecutar únicamente las operaciones requeridas para el estado actual de cada oferta, evitando cálculos, consultas o análisis redundantes.

---

### RNF-103. Gestión de memoria

La automatización deberá liberar oportunamente los recursos de memoria utilizados durante cada proceso, evitando acumulaciones innecesarias que puedan degradar el rendimiento del sistema.

---

### RNF-104. Gestión del almacenamiento

La información almacenada deberá organizarse de forma eficiente, evitando duplicidad innecesaria y conservando únicamente los datos requeridos para garantizar la trazabilidad, auditoría y funcionamiento del sistema.

---

### RNF-105. Optimización de consultas

Las consultas realizadas a bases de datos, fuentes de empleo y demás dependencias externas deberán minimizar accesos repetitivos e innecesarios mediante estrategias adecuadas de organización y reutilización de la información.

---

### RNF-106. Uso responsable del ancho de banda

La automatización deberá minimizar la transferencia innecesaria de información hacia y desde servicios externos, descargando únicamente los datos requeridos para cada proceso.

---

### RNF-107. Control de procesos simultáneos

El número de procesos ejecutados simultáneamente deberá mantenerse dentro de los límites que garanticen la estabilidad del sistema y de las dependencias externas utilizadas.

---

### RNF-108. Optimización del almacenamiento histórico

El crecimiento del historial de ofertas, registros, métricas y documentos no deberá afectar significativamente el rendimiento general de la automatización.

La organización de la información deberá facilitar su consulta y administración a largo plazo.

---

### RNF-109. Monitoreo del consumo

La automatización deberá registrar métricas que permitan identificar el consumo aproximado de recursos durante las ejecuciones, facilitando la detección de oportunidades de optimización.

---

### RNF-110. Escalabilidad del consumo

El incremento en el volumen de ofertas procesadas deberá producir un crecimiento proporcional y controlado del consumo de recursos, evitando incrementos desproporcionados respecto al trabajo realizado.

---

## 14. Tiempos máximos de ejecución

Los siguientes requisitos establecen los criterios para controlar la duración de los procesos ejecutados por la automatización.

El objetivo es garantizar que la ejecución permanezca dentro de límites razonables, detectar oportunamente procesos anómalos y facilitar la recuperación cuando una operación exceda el tiempo esperado.

Los valores específicos de tiempo máximo se definirán durante el diseño de la arquitectura y la implementación de cada módulo, una vez se conozcan las tecnologías, dependencias y condiciones reales de ejecución.

---

### RNF-111. Tiempo máximo por proceso

Todo proceso ejecutado por la automatización deberá contar con un tiempo máximo de ejecución previamente definido.

Cuando dicho límite sea superado, el sistema deberá aplicar la estrategia de gestión correspondiente.

---

### RNF-112. Control de procesos prolongados

La automatización deberá identificar los procesos cuya duración exceda el comportamiento esperado y registrarlos para su posterior análisis.

---

### RNF-113. Interrupción controlada

Cuando un proceso supere el tiempo máximo permitido y no pueda completarse de forma segura, la automatización deberá finalizarlo de manera controlada, preservando la integridad de la información y la trazabilidad del procesamiento.

---

### RNF-114. Gestión de tiempos de espera

Las operaciones que dependan de servicios externos deberán utilizar tiempos de espera configurables para evitar bloqueos indefinidos durante la ejecución.

---

### RNF-115. Independencia temporal entre módulos

La demora de un módulo no deberá provocar el bloqueo permanente de otros procesos independientes, salvo cuando exista una dependencia funcional explícitamente documentada.

---

### RNF-116. Reanudación tras interrupciones

Cuando un proceso sea detenido por superar el tiempo máximo permitido y exista una estrategia de recuperación definida, la automatización deberá permitir su reanudación sin repetir innecesariamente las tareas ya completadas.

---

### RNF-117. Configuración centralizada de tiempos

Los límites de tiempo utilizados por la automatización deberán administrarse mediante configuraciones centralizadas, evitando valores distribuidos dentro de la lógica de los módulos.

---

### RNF-118. Registro de excedentes de tiempo

Toda ejecución que supere el tiempo esperado deberá registrarse indicando, como mínimo:

- Proceso afectado.
- Fecha y hora.
- Duración observada.
- Límite configurado.
- Acción ejecutada por la automatización.

---

### RNF-119. Optimización continua

La información recopilada sobre los tiempos de ejecución deberá utilizarse para identificar procesos susceptibles de optimización durante la evolución del proyecto.

---

### RNF-120. Adaptabilidad de los límites

Los tiempos máximos de ejecución deberán poder ajustarse conforme evolucionen la arquitectura, el volumen de procesamiento y las características de las dependencias externas, sin requerir modificaciones en la lógica funcional del sistema.

---

## 15. Recuperación ante fallos

Los siguientes requisitos establecen las condiciones necesarias para que la automatización pueda detectar, gestionar y recuperarse de fallos sin comprometer la integridad de la información, la trazabilidad del procesamiento ni la estabilidad del sistema.

La recuperación ante fallos deberá priorizar la continuidad operativa siempre que sea técnicamente posible y compatible con las reglas de negocio definidas.

---

### RNF-121. Detección de fallos

La automatización deberá identificar oportunamente cualquier fallo que impida o comprometa la ejecución normal de un proceso, iniciando la estrategia de recuperación correspondiente.

---

### RNF-122. Recuperación controlada

Toda recuperación deberá ejecutarse siguiendo procedimientos previamente definidos y documentados, evitando acciones improvisadas o comportamientos no determinísticos.

---

### RNF-123. Conservación del estado

Cuando ocurra un fallo, el sistema deberá preservar el estado operativo, el estado del ciclo de vida y la información necesaria para continuar posteriormente el procesamiento.

---

### RNF-124. Reintentos controlados

Los procesos que admitan recuperación automática deberán utilizar mecanismos de reintento previamente definidos, evitando ciclos infinitos o ejecuciones repetitivas innecesarias.

---

### RNF-125. Aislamiento de fallos

Un fallo ocurrido en un módulo no deberá propagarse automáticamente hacia otros componentes independientes, salvo cuando exista una dependencia funcional explícitamente documentada.

---

### RNF-126. Protección de la integridad

Ningún proceso de recuperación podrá comprometer la integridad de los datos, generar inconsistencias o alterar la trazabilidad del procesamiento realizado hasta el momento del fallo.

---

### RNF-127. Escalamiento de incidencias

Cuando un fallo no pueda resolverse mediante los mecanismos automáticos definidos, la automatización deberá registrar la situación y marcar el proceso para la intervención del usuario cuando corresponda.

---

### RNF-128. Registro de la recuperación

Toda estrategia de recuperación ejecutada deberá registrarse indicando, como mínimo:

- Proceso afectado.
- Causa del fallo.
- Estrategia aplicada.
- Número de reintentos realizados.
- Resultado obtenido.
- Estado final del proceso.

---

### RNF-129. Reanudación segura

Cuando la recuperación sea exitosa, la automatización deberá continuar el procesamiento desde el punto más adecuado, evitando repetir innecesariamente las tareas completadas correctamente.

---

### RNF-130. Recuperación reproducible

Los mecanismos de recuperación deberán producir un comportamiento consistente y predecible frente a fallos equivalentes, garantizando que la misma situación genere la misma estrategia de recuperación bajo las mismas condiciones.

---

## 16. Observabilidad (Logs y Métricas)

Los siguientes requisitos establecen las condiciones necesarias para que la automatización permita conocer, comprender y auditar su comportamiento durante la ejecución de todos sus procesos.

La observabilidad deberá proporcionar información suficiente para supervisar el funcionamiento del sistema, diagnosticar problemas, medir el rendimiento y facilitar la mejora continua de la automatización.

---

### RNF-131. Registro integral de eventos

La automatización deberá registrar todos los eventos relevantes ocurridos durante su ejecución, permitiendo reconstruir el comportamiento completo del sistema.

---

### RNF-132. Registro de procesos

Cada proceso ejecutado deberá generar registros que permitan identificar, como mínimo:

- Identificador de la ejecución.
- Módulo responsable.
- Fecha y hora de inicio.
- Fecha y hora de finalización.
- Resultado obtenido.
- Estado final.

---

### RNF-133. Registro de decisiones

Toda decisión automática deberá quedar registrada junto con la información necesaria para comprender:

- La regla aplicada.
- Los datos evaluados.
- La decisión tomada.
- El resultado obtenido.

---

### RNF-134. Registro de errores y excepciones

Todo error, excepción o comportamiento inesperado deberá registrarse indicando la información necesaria para facilitar su diagnóstico, recuperación y posterior análisis.

---

### RNF-135. Registro de cambios de estado

Cada transición del ciclo de vida y del estado operativo de una oferta deberá registrarse, incluyendo el momento del cambio y el responsable de la transición (sistema o usuario).

---

### RNF-136. Métricas de ejecución

La automatización deberá recopilar métricas que permitan evaluar su comportamiento operativo, incluyendo, como mínimo:

- Número de ofertas descubiertas.
- Número de ofertas procesadas.
- Número de ofertas descartadas.
- Número de procesos ejecutados.
- Número de errores.
- Número de reintentos.
- Duración de las ejecuciones.

---

### RNF-137. Métricas de rendimiento

El sistema deberá registrar indicadores que permitan analizar la eficiencia de cada módulo y detectar oportunidades de optimización durante la evolución del proyecto.

---

### RNF-138. Persistencia de registros

Los registros generados por la automatización deberán conservarse durante el tiempo definido por la estrategia de gestión del proyecto, permitiendo auditorías, análisis históricos y reprocesamientos cuando sean necesarios.

---

### RNF-139. Consulta de información operativa

La información registrada deberá organizarse de forma que facilite la consulta, búsqueda y análisis de procesos, ofertas, decisiones, errores y métricas sin afectar el funcionamiento de la automatización.

---

### RNF-140. Trazabilidad completa

La combinación de registros, métricas y eventos deberá permitir reconstruir completamente el recorrido de una oferta desde su descubrimiento hasta la finalización de su procesamiento, incluyendo todas las acciones, decisiones, estados y resultados generados durante su ciclo de vida.

---

## 17. Criterios de aceptación

La automatización cumplirá los requisitos no funcionales cuando se verifique que satisface los siguientes criterios de aceptación durante las pruebas, validaciones y operación del sistema.

---

### CNA-001. Rendimiento

La automatización ejecuta sus procesos dentro de los límites de rendimiento definidos para cada módulo, sin degradaciones significativas durante la operación normal.

---

### CNA-002. Escalabilidad

La incorporación de nuevas fuentes de empleo, reglas de negocio, módulos o funcionalidades puede realizarse sin requerir modificaciones significativas en los componentes existentes.

---

### CNA-003. Disponibilidad

La automatización puede iniciar y ejecutar sus procesos cuando las dependencias necesarias se encuentran disponibles y gestiona adecuadamente las interrupciones temporales de los servicios externos.

---

### CNA-004. Seguridad

Las credenciales, configuraciones sensibles y datos personales permanecen protegidos y separados de la lógica de la automatización, cumpliendo los mecanismos de seguridad definidos.

---

### CNA-005. Confiabilidad

La automatización produce resultados consistentes y reproducibles bajo las mismas condiciones de entrada, manteniendo la integridad del procesamiento durante todo el ciclo de vida de las ofertas.

---

### CNA-006. Mantenibilidad

Las modificaciones, correcciones y ampliaciones pueden realizarse sin afectar innecesariamente otros componentes y respetando la arquitectura y la documentación oficial del proyecto.

---

### CNA-007. Portabilidad

La automatización puede instalarse y ejecutarse en los entornos previstos utilizando únicamente los procedimientos y configuraciones documentados.

---

### CNA-008. Compatibilidad

Los módulos, servicios y dependencias externas interactúan correctamente mediante las interfaces definidas, preservando la consistencia del intercambio de información.

---

### CNA-009. Usabilidad

El usuario puede configurar, administrar, consultar resultados y supervisar el funcionamiento de la automatización utilizando la documentación y los mecanismos previstos por el sistema.

---

### CNA-010. Restricciones tecnológicas

Las tecnologías utilizadas cumplen las restricciones definidas para el proyecto, priorizando herramientas gratuitas, estándares abiertos y componentes compatibles con la arquitectura.

---

### CNA-011. Consumo de recursos

La automatización utiliza los recursos computacionales de manera eficiente y mantiene un comportamiento estable conforme aumenta el volumen de procesamiento.

---

### CNA-012. Tiempos de ejecución

Los procesos respetan los tiempos máximos configurados o aplican correctamente las estrategias definidas cuando dichos límites son superados.

---

### CNA-013. Recuperación ante fallos

La automatización detecta, registra y recupera los fallos conforme a las estrategias documentadas, preservando la integridad de la información y la continuidad del procesamiento cuando sea posible.

---

### CNA-014. Observabilidad

Los registros, métricas y eventos generados permiten supervisar, auditar y reconstruir completamente el comportamiento de la automatización durante cualquier ejecución.

---

### CNA-015. Cumplimiento integral

Todos los requisitos no funcionales definidos en este documento pueden verificarse mediante evidencia objetiva obtenida durante las pruebas, la operación o la revisión de la documentación oficial del proyecto.

---

## 18. Índice de requisitos no funcionales

El presente documento contiene los siguientes grupos de requisitos no funcionales:

| Rango | Categoría |
|--------|-----------|
| RNF-001 – RNF-010 | Rendimiento |
| RNF-011 – RNF-020 | Escalabilidad |
| RNF-021 – RNF-030 | Disponibilidad |
| RNF-031 – RNF-040 | Seguridad |
| RNF-041 – RNF-050 | Confiabilidad |
| RNF-051 – RNF-060 | Mantenibilidad |
| RNF-061 – RNF-070 | Portabilidad |
| RNF-071 – RNF-080 | Compatibilidad |
| RNF-081 – RNF-090 | Usabilidad |
| RNF-091 – RNF-100 | Restricciones tecnológicas |
| RNF-101 – RNF-110 | Consumo esperado de recursos |
| RNF-111 – RNF-120 | Tiempos máximos de ejecución |
| RNF-121 – RNF-130 | Recuperación ante fallos |
| RNF-131 – RNF-140 | Observabilidad (logs y métricas) |

Cada requisito posee un identificador único e inmutable que podrá utilizarse como referencia en la documentación, la implementación, las pruebas, la arquitectura y los futuros documentos del proyecto.

Los identificadores RNF no deberán reutilizarse ni modificarse una vez el documento haya sido aprobado.
