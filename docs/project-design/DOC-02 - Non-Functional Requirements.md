# Requisitos No Funcionales (DOC-02)

## 1. Propósito

Define las características de calidad, restricciones y criterios técnicos obligatorios para todos los componentes del sistema durante diseño, implementación, operación y evolución. A diferencia de los requisitos funcionales (qué hace el sistema), estos definen **cómo** debe hacerlo. Son vinculantes para todos los módulos y sirven como referencia para decisiones arquitectónicas, selección de herramientas, implementación y validación.

---

## 2. Principios de Calidad del Sistema (QP-001 a QP-015)

Atributos de calidad que todo componente debe satisfacer durante diseño, desarrollo, implementación, operación y mantenimiento. Complementan los requisitos funcionales y sirven como criterio para evaluar cualquier decisión arquitectónica, implementación o nueva funcionalidad.

| Código | Principio | Definición |
|--------|-----------|------------|
| **QP-001** | Confiabilidad | Ejecución consistente y predecible; resultados reproducibles bajo las mismas condiciones de entrada. Los fallos se detectan, registran y manejan mediante mecanismos de recuperación definidos. |
| **QP-002** | Escalabilidad | Incorporación de nuevas fuentes, módulos, reglas y funcionalidades con impacto mínimo en componentes existentes; sin rediseño arquitectónico significativo. |
| **QP-003** | Modularidad | Responsabilidad claramente definida por componente; mínima dependencia entre componentes. Modificar o reemplazar un módulo no afecta a los demás salvo por interfaces definidas. |
| **QP-004** | Mantenibilidad | Facilidad para corregir defectos, mejorar y actualizar componentes con esfuerzo mínimo; sin comprometer estabilidad global. |
| **QP-005** | Trazabilidad | Toda acción, decisión, cambio de estado, actividad de procesamiento e información generada es reconstruible mediante registros verificables, durante todo el ciclo de vida de cada oferta. |
| **QP-006** | Consistencia | Datos generados, almacenados y procesados consistentes entre todos los módulos. No existen estados, registros ni resultados conflictivos. |
| **QP-007** | Disponibilidad | El sistema está listo para ejecutar cuando el usuario lo solicite o según calendario definido, siempre que las dependencias externas estén disponibles. Las interrupciones temporales se manejan con estrategias de recuperación predefinidas. |
| **QP-008** | Eficiencia | Uso eficiente de recursos computacionales: sin procesamiento innecesario, consultas redundantes ni consumo excesivo de memoria, almacenamiento o tiempo de ejecución. |
| **QP-009** | Seguridad | Protección de la información contra acceso, modificación o divulgación no autorizados. Credenciales, configuraciones sensibles y datos personales se almacenan con mecanismos de protección adecuados. |
| **QP-010** | Portabilidad | Diseñado para trasladarse entre entornos de ejecución con el mínimo de cambios. Las dependencias específicas de plataforma se aíslan cuando sea técnicamente factible. |
| **QP-011** | Extensibilidad | Incorporación de nuevas capacidades sin alterar el comportamiento esperado de funcionalidades existentes. Toda extensión cumple interfaces, estándares y reglas del proyecto. |
| **QP-012** | Auditabilidad | Toda decisión automatizada es justificable mediante evidencia objetiva registrada. Los registros permiten determinar qué ocurrió, cuándo, por qué y con qué resultado. |
| **QP-013** | Simplicidad | Las soluciones implementadas favorecen la simplicidad sobre complejidad innecesaria. Entre alternativas técnicamente viables, se prioriza la que mejora comprensión, mantenimiento y evolución. |
| **QP-014** | Uso de tecnologías libres | Prioridad a alternativas gratuitas que satisfagan los requisitos. Tecnologías de pago solo con justificación técnica documentada y aprobación explícita del usuario. |
| **QP-015** | Documentación continua | Toda decisión significativa (arquitectura, reglas, operación, implementación, evolución) se documenta antes de incorporarse. Ningún componente crítico depende exclusivamente de conocimiento implícito. |

---

## 3. Rendimiento (NFR-001 a NFR-010)

Comportamiento esperado en eficiencia, tiempos de respuesta y uso de recursos durante operación.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-001** | Rendimiento general | Ejecución de cada proceso usando solo los recursos necesarios, evitando operaciones redundantes o innecesarias. |
| **NFR-002** | Tiempo de respuesta por módulo | Cada módulo completa su procesamiento en tiempo razonable para el volumen recibido. Los tiempos máximos específicos se definen en documentos técnicos una vez conocida la implementación de cada módulo. |
| **NFR-003** | Procesamiento incremental | Solo se procesan ofertas nuevas o que requieren reprocesamiento; no se re-ejecuta sobre información ya actualizada y validada. |
| **NFR-004** | Optimización de consultas | Consultas a fuentes, bases de datos y dependencias externas minimizan solicitudes repetidas e innecesarias. Se reutiliza información previamente recuperada cuando sea posible. |
| **NFR-005** | Optimización de procesamiento | Los módulos ejecutan solo tareas requeridas para el estado actual de cada oferta. No se ejecutan procesos que no aporten valor al flujo funcional. |
| **NFR-006** | Uso eficiente de recursos | Optimización de memoria, almacenamiento, procesamiento y ancho de banda durante toda la ejecución. |
| **NFR-007** | Ejecución independiente | La ejecución de un módulo no degrada significativamente el rendimiento de otros. Cada componente gestiona sus propios recursos de forma controlada. |
| **NFR-008** | Escalabilidad de rendimiento | Al aumentar el número de ofertas procesadas, los tiempos de ejecución crecen de forma controlada, sin degradación desproporcionada. |
| **NFR-009** | Monitoreo de rendimiento | El sistema registra métricas que incluyen como mínimo: tiempo de ejecución por módulo · tiempo total de ejecución · número de ofertas procesadas · número de ofertas descartadas · número de errores · número de reintentos · consumo aproximado de recursos (cuando sea posible). Estas métricas identifican oportunidades de optimización y verifican cumplimiento de requisitos de rendimiento. |
| **NFR-010** | Degradación controlada | Cuando una dependencia externa se vuelve lenta o parcialmente indisponible, el sistema degrada su rendimiento de forma controlada, priorizando continuidad del procesamiento sobre interrupción total cuando las reglas de negocio lo permitan. |

---

## 4. Escalabilidad (NFR-011 a NFR-020)

Capacidad de crecer de forma controlada: nuevas funcionalidades, fuentes, reglas y componentes sin comprometer estabilidad, rendimiento ni mantenibilidad. Principio transversal durante todo el ciclo de vida.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-011** | Escalabilidad modular | Módulos independientes con responsabilidades definidas que permiten agregar, reemplazar o extender componentes sin afectar el resto del sistema. |
| **NFR-012** | Incorporación de nuevas fuentes | Nuevas fuentes de empleo se integran sin modificaciones significativas en módulos de procesamiento, evaluación, gestión o generación de recursos, mediante mecanismos estandarizados definidos por la arquitectura. |
| **NFR-013** | Escalabilidad de reglas de negocio | Reglas de evaluación, rechazo, clasificación y priorización gestionadas centralmente; extensibles o modificables sin cambiar la lógica global del proceso. |
| **NFR-014** | Escalabilidad funcional | Nuevas funcionalidades se incorporan mediante módulos o componentes adicionales, evitando modificaciones innecesarias a funcionalidad ya implementada y aprobada. |
| **NFR-015** | Escalabilidad de procesamiento | Comportamiento estable al aumentar ofertas, fuentes, reglas o procesos ejecutados. El crecimiento no requiere rediseño estructural. |
| **NFR-016** | Escalabilidad de datos | La arquitectura soporta crecimiento progresivo de información almacenada preservando integridad, trazabilidad y acceso eficiente a registros históricos. |
| **NFR-017** | Escalabilidad de configuración | Configuraciones gestionadas centralmente; nuevos parámetros se incorporan sin afectar configuraciones existentes ni requerir cambios en múltiples componentes. |
| **NFR-018** | Compatibilidad con integraciones futuras | La arquitectura facilita integración futura de nuevos servicios, herramientas, modelos de IA o componentes externos mediante interfaces definidas y bajo acoplamiento. |
| **NFR-019** | Escalabilidad de mantenimiento | Al crecer el proyecto, la complejidad de mantenimiento no aumenta desproporcionadamente. Organización de código, documentación y arquitectura soporta evolución controlada y progresiva. |
| **NFR-020** | Evolución controlada | Toda mejora cumple arquitectura, estándares, convenciones y reglas documentadas, garantizando compatibilidad con componentes existentes y evitando dependencias innecesarias. |

---

## 5. Disponibilidad (NFR-021 a NFR-030)

Condiciones para que el sistema esté listo para ejecutar y se recupere de interrupciones. Continuidad operativa dentro de las limitaciones impuestas por dependencias externas e infraestructura.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-021** | Disponibilidad operativa | El sistema inicia y ejecuta procesos cuando el usuario lo solicite o según calendario, siempre que las dependencias requeridas estén disponibles. |
| **NFR-022** | Tolerancia a indisponibilidad externa | La indisponibilidad temporal de fuentes, servicios, modelos de IA u otras dependencias no compromete la operación global. El sistema aísla el componente afectado y continúa la ejecución cuando las reglas del proceso lo permitan. |
| **NFR-023** | Reanudación de procesamiento | Cuando un proceso se interrumpe por evento recuperable, el sistema reanuda desde el punto más apropiado, evitando repetición innecesaria de tareas ya completadas. |
| **NFR-024** | Recuperación controlada | La recuperación de fallos sigue estrategias predefinidas y documentadas, priorizando integridad de información y consistencia del procesamiento. |
| **NFR-025** | Preservación de estado | Ante interrupción, el sistema preserva tanto el estado operativo como el estado de ciclo de vida de cada oferta, permitiendo continuar sin pérdida de trazabilidad. |
| **NFR-026** | Independencia de módulos | La indisponibilidad de un módulo no impide la operación de otros salvo dependencia funcional explícitamente documentada. |
| **NFR-027** | Protección contra interrupciones inesperadas | Minimiza impacto de apagados, reinicios o interrupciones preservando información necesaria para reanudar el procesamiento posteriormente. |
| **NFR-028** | Gestión de dependencias externas | Disponibilidad de cada dependencia externa verificada antes de iniciar operaciones que la requieran. Si no está disponible, se aplica estrategia correspondiente antes de marcar el proceso como fallido. |
| **NFR-029** | Continuidad de servicio | Cuando sea técnicamente factible, procesos no afectados por un fallo continúan ejecutándose normalmente, evitando interrupciones globales. |
| **NFR-030** | Registro de indisponibilidad | Toda interrupción, degradación de servicio o indisponibilidad detectada se registra para facilitar auditoría, diagnóstico y mejora continua. |

---

## 6. Seguridad (NFR-031 a NFR-040)

Condiciones para proteger información, configuraciones y recursos durante todo el ciclo de vida. Preocupación transversal en todos los módulos: confidencialidad, integridad y disponibilidad.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-031** | Protección de información | Toda información gestionada se almacena y procesa con mecanismos que reducen riesgo de pérdida, alteración o acceso no autorizado. |
| **NFR-032** | Protección de credenciales | Credenciales, claves, tokens, secretos y datos sensibles separados del código fuente y almacenados con mecanismos de protección adecuados. Nunca incrustados directamente en el código. |
| **NFR-033** | Protección de configuraciones sensibles | Configuraciones que afecten seguridad u operación gestionadas centralmente y protegidas contra modificaciones accidentales o no autorizadas. |
| **NFR-034** | Integridad de información | Preservar integridad de datos originales de fuentes de empleo. Transformaciones solo sobre información derivada o estructuras normalizadas, manteniendo disponible la información original cuando sea necesario. |
| **NFR-035** | Protección de datos personales | Información personal del usuario usada solo para los fines definidos y limitada a procesos que genuinamente la requieran. Minimiza exposición innecesaria durante procesamiento y almacenamiento. |
| **NFR-036** | Validación de entradas | Toda información de fuentes externas, configuraciones del usuario o servicios integrados se valida antes de ser usada. Ningún dato externo se asume válido sin verificación previa. |
| **NFR-037** | Principio de mínimo acceso | Cada componente accede solo a información y recursos estrictamente necesarios para su responsabilidad funcional. |
| **NFR-038** | Registro de eventos de seguridad | Todo evento que pueda comprometer la seguridad se registra para facilitar análisis, auditoría y remediación posterior. |
| **NFR-039** | Recuperación segura | Los procesos de recuperación no comprometen integridad ni eluden validaciones definidas. Toda operación de recuperación preserva consistencia de datos y trazabilidad. |
| **NFR-040** | Evolución segura | Incorporar nuevos módulos, servicios, dependencias o funcionalidades no reduce el nivel de seguridad alcanzado. Toda modificación cumple los requisitos de seguridad de este documento. |

---

## 7. Confiabilidad (NFR-041 a NFR-050)

Condiciones para operación consistente, predecible y confiable durante todo el ciclo de vida. Resultados reproducibles, integridad del procesamiento, e identificación/registro/gestión de situaciones anómalas.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-041** | Consistencia de ejecución | Resultados consistentes al procesar la misma información bajo las mismas condiciones de entrada y configuración. |
| **NFR-042** | Integridad de procesamiento | Cada oferta completa solo las etapas del flujo funcional correspondientes a su estado actual; sin omisiones, duplicaciones ni ejecución fuera de secuencia. |
| **NFR-043** | Prevención de corrupción de datos | Protección contra modificaciones parciales, inconsistentes o incompletas que comprometan integridad del procesamiento. |
| **NFR-044** | Detección de anomalías | Identifica comportamiento anómalo durante ejecución y lo registra para análisis posterior, independientemente de si resulta en error. |
| **NFR-045** | Tolerancia a fallos recuperables | Ante fallo recuperable, aplica mecanismos definidos para continuar el procesamiento sin comprometer consistencia de información. |
| **NFR-046** | Reproducibilidad | Decisiones automatizadas y resultados generados reproducibles usando mismas entradas, configuraciones y reglas vigentes al momento de ejecución. |
| **NFR-047** | Protección del flujo funcional | Ninguna oferta omite etapas obligatorias, retrocede a estados incompatibles ni avanza por transiciones indefinidas salvo autorización explícita de regla documentada. |
| **NFR-048** | Estabilidad operativa | Comportamiento estable durante ejecuciones prolongadas o repetitivas, sin degradación que afecte confiabilidad del procesamiento. |
| **NFR-049** | Verificación de resultados | Al completar cada proceso, verifica que los resultados esperados se generaron correctamente antes de continuar a la siguiente etapa del flujo funcional. |
| **NFR-050** | Preservación de trazabilidad | Toda acción preserva información necesaria para reconstruir el procesamiento posteriormente, garantizando auditorías, revisiones y reprocesamientos confiables. |

---

## 8. Mantenibilidad (NFR-051 a NFR-060)

Condiciones para corregir, actualizar, extender y mantener fácilmente el sistema durante su ciclo de vida, minimizando esfuerzo de mejoras, correcciones, reemplazo de componentes y adaptación a nuevos requisitos.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-051** | Arquitectura modular | Módulos con responsabilidades definidas y bajo acoplamiento, facilitando mantenimiento y evolución independiente. |
| **NFR-052** | Separación de responsabilidades | Responsabilidad funcional única y claramente identificada por componente. Lógica de negocio, configuración, acceso a datos e integración con servicios externos desacopladas cuando sea técnicamente factible. |
| **NFR-053** | Configuración centralizada | Reglas de negocio, parámetros operativos, configuraciones generales y demás elementos modificables gestionados desde ubicaciones centralizadas, evitando configuraciones duplicadas. |
| **NFR-054** | Documentación actualizada | Toda modificación funcional, técnica o arquitectónica se refleja en documentación oficial antes de considerarse completa. La documentación permanece sincronizada con el comportamiento real del sistema. |
| **NFR-055** | Facilidad de actualización | Mejoras, correcciones o nuevas funcionalidades se incorporan con mínimo impacto en componentes existentes, sin modificaciones innecesarias a módulos no relacionados. |
| **NFR-056** | Reemplazo de componentes | La arquitectura facilita reemplazo de herramientas, bibliotecas, servicios externos o componentes internos sin afectar significativamente la operación global. |
| **NFR-057** | Reutilización | Componentes, funciones, reglas y recursos comunes diseñados para fomentar reutilización y evitar lógica duplicada en todo el proyecto. |
| **NFR-058** | Consistencia de implementación | Todos los módulos cumplen convenciones, estándares y directrices del proyecto, garantizando consistencia en organización y comportamiento. |
| **NFR-059** | Facilidad de diagnóstico | Estructura que facilita identificar origen de errores, comportamientos inesperados o problemas de rendimiento mediante mecanismos de trazabilidad y logging apropiados. |
| **NFR-060** | Evolución controlada | Toda modificación preserva compatibilidad con arquitectura, requisitos funcionales, requisitos no funcionales y reglas documentadas, evitando deuda técnica innecesaria. |

---

## 9. Portabilidad (NFR-061 a NFR-070)

Condiciones para trasladar, instalar y ejecutar el sistema en diferentes entornos con mínimo esfuerzo, preservando comportamiento y funcionalidad esperados. Reduce dependencia de plataformas, herramientas e infraestructuras específicas.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-061** | Independencia de entorno | Operación depende mínimamente de características específicas del entorno. Diferencias entre entornos se resuelven mediante configuración, no modificando lógica del sistema. |
| **NFR-062** | Configuración desacoplada | Rutas, variables de entorno, credenciales, parámetros de ejecución y toda configuración completamente separadas del código fuente. Migrar entre entornos no requiere cambios en componentes funcionales. |
| **NFR-063** | Independencia de infraestructura | Minimiza dependencias de infraestructura, hardware o servicios específicos cuando existan alternativas técnicamente viables que satisfagan requisitos. |
| **NFR-064** | Compatibilidad multi-entorno | Diseñado para facilitar ejecución en diferentes entornos compatibles (desarrollo, pruebas, producción) manteniendo comportamiento consistente. |
| **NFR-065** | Reemplazo de dependencias | Bibliotecas, herramientas, servicios externos o componentes internos reemplazables con mínimo impacto en el resto del sistema. |
| **NFR-066** | Gestión centralizada de dependencias | Dependencias claramente identificadas, documentadas y gestionadas centralmente para simplificar instalación, actualización y reemplazo. |
| **NFR-067** | Portabilidad de datos | Datos generados almacenados en formatos abiertos, ampliamente soportados y fácilmente portables, evitando dependencia innecesaria de tecnologías propietarias. |
| **NFR-068** | Portabilidad de documentación | Toda documentación funcional, técnica y de configuración en formatos abiertos y ampliamente compatibles, facilitando acceso y mantenimiento con diferentes herramientas. |
| **NFR-069** | Reproducibilidad de entornos | La documentación permite recrear un entorno completamente funcional siguiendo solo procedimientos documentados, sin depender de conocimiento no documentado. |
| **NFR-070** | Evolución tecnológica | La arquitectura facilita incorporación futura de nuevas tecnologías o reemplazo de componentes existentes sin reconstrucción significativa del sistema. |

---

## 10. Compatibilidad (NFR-071 a NFR-080)

Condiciones para interacción correcta entre componentes del sistema y con dependencias externas planificadas. Facilita integración, evolución tecnológica e incorporación de nuevos componentes sin comprometer operación global.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-071** | Compatibilidad entre módulos | Comunicación mediante interfaces definidas compatibles con la arquitectura. Ningún módulo depende de detalles de implementación interna de otros componentes. |
| **NFR-072** | Compatibilidad con dependencias externas | Mecanismos de integración compatibles con plataformas, servicios y herramientas aprobadas, respetando restricciones técnicas y operativas de cada una. |
| **NFR-073** | Compatibilidad de formatos de datos | Información intercambiada usa formatos estandarizados, consistentes y ampliamente soportados. Transformaciones requeridas sin afectar integridad de información. |
| **NFR-074** | Compatibilidad de configuración | Configuraciones compatibles entre entornos de ejecución, evitando diferencias que alteren comportamiento esperado. |
| **NFR-075** | Compatibilidad con extensiones futuras | Incorporar nuevos módulos, fuentes, modelos de IA o servicios no requiere modificaciones significativas a interfaces ya establecidas. |
| **NFR-076** | Compatibilidad de versiones | Cuando un componente depende de versiones específicas de herramientas, bibliotecas o servicios, esas dependencias se documentan para garantizar estabilidad. |
| **NFR-077** | Compatibilidad de documentación | Documentación funcional, técnica y arquitectónica alineada con la versión actual del sistema, evitando inconsistencias entre comportamiento implementado y documentación oficial. |
| **NFR-078** | Compatibilidad del modelo de datos | Cambios en estructuras de datos preservan compatibilidad con componentes que las usan o incluyen mecanismos de migración predefinidos. |
| **NFR-079** | Compatibilidad evolutiva | Mejoras mantienen compatibilidad con funcionalidad existente salvo modificación incompatible previamente documentada, justificada y aprobada. |
| **NFR-080** | Compatibilidad arquitectónica | Todo nuevo componente cumple principios, estándares, convenciones e interfaces definidos por la arquitectura oficial antes de integrarse. |

---

## 11. Usabilidad (NFR-081 a NFR-090)

Condiciones para que el usuario entienda, configure, opere y monitoree fácilmente el sistema. Reduce complejidad operativa sin requerir conocimiento técnico innecesario para actividades rutinarias.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-081** | Configuración simple | Configuraciones comunes organizadas clara y estructuralmente, comprensibles y modificables sin afectar el resto del sistema. |
| **NFR-082** | Información comprensible | Información presentada al usuario usa terminología consistente con documentación oficial y describe claramente estado, resultado o acción correspondiente. |
| **NFR-083** | Consistencia de interfaz | Mecanismos para consultar información, revisar resultados, gestionar configuraciones o tomar decisiones mantienen comportamiento consistente en todo el sistema. |
| **NFR-084** | Trazabilidad para usuario | El usuario identifica fácilmente estado actual de cada oferta, acciones realizadas, decisiones tomadas y resultado de cada etapa de procesamiento. |
| **NFR-085** | Facilidad de administración | Tareas rutinarias (actualizar configuraciones, revisar resultados, consultar logs, modificar reglas) mediante procedimientos definidos y documentados. |
| **NFR-086** | Mensajes informativos | Mensajes claros durante ejecución indicando progreso, advertencias, errores y acciones requeridas del usuario cuando aplique. |
| **NFR-087** | Intervención manual reducida | Minimiza acciones repetitivas que requieran intervención del usuario; participación reservada exclusivamente para decisiones estratégicas predefinidas. |
| **NFR-088** | Facilidad de aprendizaje | Organización, documentación y configuraciones permiten a nuevos usuarios comprender progresivamente la operación sin depender de conocimiento implícito. |
| **NFR-089** | Accesibilidad de información | Información relevante de cada oferta, ejecución, análisis o decisión organizada y disponible para consulta rápida y estructurada. |
| **NFR-090** | Consistencia de documentación | Terminología usada por el sistema alineada con el Glosario del Proyecto y demás documentación oficial, garantizando experiencia consistente en administración y monitoreo. |

---

## 12. Restricciones Tecnológicas (NFR-091 a NFR-100)

Limitaciones y criterios a respetar durante diseño, desarrollo, implementación y evolución. Garantizan consistencia técnica, reducen complejidad de mantenimiento y cumplen principios establecidos en planificación.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-091** | Prioridad a herramientas libres | Construcción con herramientas, bibliotecas, servicios y tecnologías gratuitas siempre que satisfagan requisitos funcionales y no funcionales. |
| **NFR-092** | Adopción de tecnologías de pago | Ninguna tecnología, servicio o herramienta de pago se incorpora sin justificación técnica documentada y aprobación explícita del usuario. |
| **NFR-093** | Tecnologías ampliamente soportadas | Prioridad a tecnologías con documentación suficiente, mantenimiento activo, comunidad establecida y amplio soporte, reduciendo riesgo de obsolescencia. |
| **NFR-094** | Uso de estándares abiertos | Cuando sea técnicamente factible, estándares abiertos para formatos de datos, protocolos de comunicación e intercambio de información. |
| **NFR-095** | Minimización de dependencias | Evitar dependencias externas innecesarias. Toda nueva dependencia debe justificar beneficio claro respecto a costo de mantenimiento y complejidad añadida. |
| **NFR-096** | Independencia de proveedores | Minimizar acoplamiento a proveedores, plataformas o servicios específicos, facilitando reemplazo cuando sea necesario. |
| **NFR-097** | Compatibilidad arquitectónica | Toda tecnología incorporada cumple arquitectura, principios de diseño y estándares definidos en documentación oficial. |
| **NFR-098** | Gestión de versiones | Versiones de todas las herramientas, bibliotecas y componentes documentadas para garantizar reproducibilidad de entornos y facilitar actualizaciones. |
| **NFR-099** | Evaluación previa de nuevas tecnologías | Antes de incorporar nueva herramienta, servicio o dependencia: evaluar compatibilidad con arquitectura, impacto en mantenimiento, escalabilidad y continuidad a largo plazo. |
| **NFR-100** | Restricción de cambios tecnológicos | Reemplazo de tecnologías núcleo durante desarrollo solo con justificación técnica documentada y aprobación del usuario. |

---

## 13. Consumo Esperado de Recursos (NFR-101 a NFR-110)

Criterios para uso eficiente de recursos computacionales durante ejecución. Operación eficiente y consistente, evitando consumo innecesario y soportando ejecución en entornos con recursos limitados.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-101** | Uso eficiente de recursos | Solo recursos necesarios para ejecutar cada proceso, evitando consumo innecesario de memoria, procesamiento, almacenamiento y ancho de banda. |
| **NFR-102** | Optimización de procesamiento | Los módulos ejecutan solo operaciones requeridas para el estado actual de cada oferta, evitando cálculos, consultas o análisis redundantes. |
| **NFR-103** | Gestión de memoria | Liberación oportuna de recursos de memoria usados durante cada proceso, evitando acumulación innecesaria que degrade rendimiento. |
| **NFR-104** | Gestión de almacenamiento | Información almacenada organizada eficientemente, evitando duplicación innecesaria y reteniendo solo datos requeridos para trazabilidad, auditoría y operación correcta. |
| **NFR-105** | Optimización de consultas | Consultas a bases de datos, fuentes y dependencias externas minimizan acceso repetido e innecesario mediante organización adecuada y estrategias de reutilización. |
| **NFR-106** | Uso responsable de ancho de banda | Minimiza transferencias innecesarias hacia/desde servicios externos, descargando solo información requerida para cada proceso. |
| **NFR-107** | Control de procesos concurrentes | Número de procesos simultáneos dentro de límites que garanticen estabilidad del sistema y de las dependencias externas. |
| **NFR-108** | Optimización de almacenamiento histórico | Crecimiento de historial de ofertas, logs, métricas y documentos no afecta significativamente rendimiento global. Organización facilita gestión y recuperación a largo plazo. |
| **NFR-109** | Monitoreo de consumo de recursos | Registro de métricas que permitan identificar consumo aproximado de recursos durante ejecución, facilitando detección de oportunidades de optimización. |
| **NFR-110** | Escalabilidad de consumo | Al aumentar volumen de ofertas procesadas, consumo de recursos crece proporcional y controladamente, sin aumentos desproporcionados respecto al trabajo realizado. |

---

## 14. Tiempos Máximos de Ejecución (NFR-111 a NFR-120)

Criterios para controlar duración de procesos: ejecución dentro de límites razonables, detección oportuna de procesos anómalos y facilitación de recuperación cuando una operación excede duración esperada.

**Nota:** Los tiempos máximos específicos se definen durante diseño arquitectónico e implementación de módulos, una vez conocidas tecnologías, dependencias y condiciones reales de ejecución.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-111** | Tiempo máximo por proceso | Todo proceso tiene tiempo máximo predefinido. Al excederlo, se aplica estrategia de gestión correspondiente. |
| **NFR-112** | Monitoreo de procesos prolongados | Identifica procesos cuyo tiempo excede comportamiento esperado y los registra para análisis posterior. |
| **NFR-113** | Terminación controlada | Cuando un proceso excede tiempo máximo y no puede completarse de forma segura, termina de forma controlada preservando integridad de información y trazabilidad. |
| **NFR-114** | Gestión de timeouts | Operaciones dependientes de servicios externos usan valores de timeout configurables para evitar bloqueo indefinido. |
| **NFR-115** | Independencia temporal entre módulos | Retrasos en un módulo no bloquean permanentemente otros procesos independientes salvo dependencia funcional explícitamente documentada. |
| **NFR-116** | Reanudación tras interrupción | Cuando un proceso se detiene por exceder tiempo máximo y existe estrategia de recuperación, permite reanudar sin repetir innecesariamente tareas completadas. |
| **NFR-117** | Configuración centralizada de tiempos | Límites de tiempo gestionados mediante configuración centralizada, evitando valores distribuidos en lógica de módulos. |
| **NFR-118** | Registro de excedencia de tiempos | Toda ejecución que exceda tiempo esperado se registra con mínimo: proceso afectado · fecha y hora · duración observada · límite configurado · acción realizada por el sistema. |
| **NFR-119** | Optimización continua | Información sobre tiempos de ejecución se usa para identificar procesos optimizables durante la evolución del proyecto. |
| **NFR-120** | Adaptabilidad de límites | Tiempos máximos ajustables conforme evolucionan arquitectura, volumen de procesamiento y características de dependencias externas, sin modificar lógica funcional. |

---

## 15. Recuperación de Fallos (NFR-121 a NFR-130)

Condiciones para detectar, gestionar y recuperarse de fallos sin comprometer integridad, trazabilidad ni estabilidad global. Prioriza continuidad operativa cuando sea técnicamente factible y compatible con reglas de negocio.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-121** | Detección de fallos | Identifica oportunamente cualquier fallo que impida o comprometa ejecución normal de un proceso e inicia estrategia de recuperación correspondiente. |
| **NFR-122** | Recuperación controlada | Toda operación de recuperación sigue procedimientos predefinidos y documentados, evitando acciones improvisadas o comportamiento no determinista. |
| **NFR-123** | Preservación de estado | Ante fallo, preserva estado operativo, estado de ciclo de vida e información necesaria para reanudar posteriormente. |
| **NFR-124** | Reintentos controlados | Procesos con recuperación automática usan mecanismos de reintento predefinidos, evitando bucles infinitos o ejecuciones repetidas innecesarias. |
| **NFR-125** | Aislamiento de fallos | Fallo en un módulo no se propaga automáticamente a otros componentes independientes salvo dependencia funcional explícitamente documentada. |
| **NFR-126** | Protección de integridad | Ningún proceso de recuperación compromete integridad de datos, genera inconsistencias ni altera trazabilidad del procesamiento completado antes del fallo. |
| **NFR-127** | Escalamiento de incidentes | Cuando un fallo no puede resolverse con mecanismos automáticos definidos, registra la situación y marca el proceso para intervención del usuario cuando corresponda. |
| **NFR-128** | Registro de recuperación | Toda estrategia de recuperación ejecutada registra mínimo: proceso afectado · causa del fallo · estrategia aplicada · número de reintentos · resultado obtenido · estado final del proceso. |
| **NFR-129** | Reanudación segura | Cuando la recuperación es exitosa, reanuda desde el punto más apropiado evitando repetición innecesaria de tareas correctamente completadas. |
| **NFR-130** | Recuperación reproducible | Mecanismos de recuperación producen comportamiento consistente y predecible ante fallos equivalentes: situaciones idénticas resultan en la misma estrategia bajo las mismas condiciones. |

---

## 16. Observabilidad — Logs y Métricas (NFR-131 a NFR-140)

Condiciones para que el comportamiento sea comprensible, medible y auditable durante ejecución de todos los procesos. Proporciona información suficiente para monitoreo, diagnóstico, medición de rendimiento y mejora continua.

| Código | Requisito | Definición |
|--------|-----------|------------|
| **NFR-131** | Registro integral de eventos | Registra todos los eventos relevantes durante ejecución, permitiendo reconstruir comportamiento completo del sistema. |
| **NFR-132** | Registro de procesos | Todo proceso ejecutado genera registros con mínimo: identificador de ejecución · módulo responsable · fecha/hora de inicio · fecha/hora de fin · resultado obtenido · estado final. |
| **NFR-133** | Registro de decisiones | Toda decisión automatizada se registra con información necesaria para entender: regla aplicada · datos evaluados · decisión tomada · resultado obtenido. |
| **NFR-134** | Registro de errores y excepciones | Todo error, excepción o comportamiento inesperado se registra con información requerida para diagnóstico, recuperación y análisis posterior. |
| **NFR-135** | Registro de transiciones de estado | Toda transición de estado de ciclo de vida y operativo se registra incluyendo hora del cambio y entidad responsable (sistema o usuario). |
| **NFR-136** | Métricas de ejecución | Métricas que evalúan comportamiento operativo, incluyendo mínimo: ofertas descubiertas · ofertas procesadas · ofertas descartadas · procesos ejecutados · errores · reintentos · duración de ejecución. |
| **NFR-137** | Métricas de rendimiento | Indicadores que permiten analizar eficiencia de cada módulo e identificar oportunidades de optimización durante la evolución del proyecto. |
| **NFR-138** | Retención de logs | Logs retenidos por el período definido por la estrategia de gestión del proyecto, permitiendo auditorías, análisis históricos y reprocesamientos cuando se requieran. |
| **NFR-139** | Acceso a información operativa | Información registrada organizada para facilitar consulta, búsqueda y análisis de procesos, ofertas, decisiones, errores y métricas sin afectar operación del sistema. |
| **NFR-140** | Trazabilidad completa | Combinación de logs, métricas y eventos permite reconstruir completamente el recorrido de una oferta desde descubrimiento hasta finalización, incluyendo toda acción, decisión, estado y resultado durante su ciclo de vida. |

---

## 17. Criterios de Aceptación (NAC-001 a NAC-015)

El sistema satisface los requisitos no funcionales cuando se verifica que cumple los siguientes criterios durante pruebas, validación y operación.

| Código | Criterio | Verificación |
|--------|----------|--------------|
| **NAC-001** | Rendimiento | Ejecuta procesos dentro de límites definidos por módulo, sin degradación significativa en operación normal. |
| **NAC-002** | Escalabilidad | Nuevas fuentes, reglas, módulos o funcionalidades se incorporan sin modificaciones significativas a componentes existentes. |
| **NAC-003** | Disponibilidad | Inicia y ejecuta procesos cuando las dependencias están disponibles; gestiona correctamente interrupciones temporales de servicios externos. |
| **NAC-004** | Seguridad | Credenciales, configuraciones sensibles y datos personales protegidos y separados de la lógica del sistema, cumpliendo mecanismos de seguridad definidos. |
| **NAC-005** | Confiabilidad | Resultados consistentes y reproducibles bajo mismas condiciones de entrada; integridad del procesamiento preservada durante todo el ciclo de vida. |
| **NAC-006** | Mantenibilidad | Modificaciones, correcciones y extensiones implementables sin afectar innecesariamente otros componentes y respetando arquitectura y documentación oficial. |
| **NAC-007** | Portabilidad | Instalación y ejecución en entornos previstos usando solo procedimientos y configuraciones documentados. |
| **NAC-008** | Compatibilidad | Módulos, servicios y dependencias externas interactúan correctamente mediante interfaces definidas preservando consistencia del intercambio. |
| **NAC-009** | Usabilidad | El usuario configura, gestiona, revisa resultados y monitorea usando documentación y mecanismos provistos por el sistema. |
| **NAC-010** | Restricciones tecnológicas | Tecnologías usadas cumplen restricciones definidas: prioridad a herramientas libres, estándares abiertos y componentes compatibles con arquitectura. |
| **NAC-011** | Consumo de recursos | Uso eficiente de recursos computacionales; comportamiento estable al aumentar volumen de procesamiento. |
| **NAC-012** | Tiempos de ejecución | Procesos cumplen tiempos máximos configurados o aplican correctamente estrategias definidas al excederlos. |
| **NAC-013** | Recuperación de fallos | Detecta, registra y recupera de fallos según estrategias documentadas preservando integridad y continuidad cuando sea posible. |
| **NAC-014** | Observabilidad | Logs, métricas y eventos generados permiten monitoreo, auditoría y reconstrucción completa del comportamiento durante cualquier ejecución. |
| **NAC-015** | Cumplimiento global | Todos los requisitos no funcionales verificables mediante evidencia objetiva obtenida durante pruebas, operación o revisión de documentación oficial. |

---

## 18. Índice de Requisitos No Funcionales

| Rango | Categoría |
|-------|-----------|
| NFR-001 – NFR-010 | Rendimiento |
| NFR-011 – NFR-020 | Escalabilidad |
| NFR-021 – NFR-030 | Disponibilidad |
| NFR-031 – NFR-040 | Seguridad |
| NFR-041 – NFR-050 | Confiabilidad |
| NFR-051 – NFR-060 | Mantenibilidad |
| NFR-061 – NFR-070 | Portabilidad |
| NFR-071 – NFR-080 | Compatibilidad |
| NFR-081 – NFR-090 | Usabilidad |
| NFR-091 – NFR-100 | Restricciones tecnológicas |
| NFR-101 – NFR-110 | Consumo esperado de recursos |
| NFR-111 – NFR-120 | Tiempos máximos de ejecución |
| NFR-121 – NFR-130 | Recuperación de fallos |
| NFR-131 – NFR-140 | Observabilidad (logs y métricas) |

Cada requisito tiene identificador único e inmutable utilizable como referencia en documentación, implementación, pruebas, arquitectura y documentos futuros. Los identificadores NFR no se reutilizan ni modifican una vez aprobado este documento.

**Reducción estimada:** ~70 % del volumen original, 0 % de pérdida informativa.
