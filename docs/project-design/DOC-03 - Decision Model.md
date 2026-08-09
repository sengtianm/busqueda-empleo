# Documento 3 – Modelo de Decisión (Optimizado)

---

## 1. Propósito

Define el modelo de decisión de la automatización de búsqueda de empleo: principios, reglas, criterios, mecanismos y restricciones que gobiernan toda decisión durante el procesamiento de ofertas laborales.

**Alcance obligatorio:** todo módulo que evalúe, clasifique, priorice, rechace, recomiende o decida dentro de la automatización.

**Funciones:**
- Establecer cómo se evalúa la información, se aplican reglas de negocio, se asignan prioridades, se resuelven situaciones previstas y se determina si una decisión es automática o requiere intervención del usuario.
- Servir como referencia oficial para diseño, implementación, validación y evolución del motor de decisiones.
- Garantizar alineación con Requisitos Funcionales, No Funcionales y Principios Generales del proyecto.

---

## 2. Principios del Modelo de Decisión

| ID | Principio | Definición |
|---|---|---|
| DMP-001 | Basado en reglas | Toda decisión se fundamenta exclusivamente en reglas de negocio documentadas y aprobadas. Prohibido usar criterios implícitos, aleatorios o no documentados. |
| DMP-002 | Consistencia | Mismos inputs + configuración + reglas → misma decisión. Comportamiento determinista. |
| DMP-003 | Reproducibilidad | Toda decisión es reproducible con la misma información, configuración y versión de reglas vigentes al momento de ejecución. |
| DMP-004 | Trazabilidad | Toda decisión preserva: datos evaluados, reglas aplicadas, resultado generado y responsable. |
| DMP-005 | Auditabilidad | Toda decisión respaldada por evidencia objetiva registrada: qué, cuándo, por qué y qué reglas la sustentaron. |
| DMP-006 | Separación evaluación/decisión | La evaluación produce información objetiva; la decisión usa esa información para determinar la acción. Son conceptualmente independientes. |
| DMP-007 | Intervención controlada del usuario | Decisiones estratégicas, personales, legales o de representación del usuario requieren aprobación explícita. La automatización no sustituye el juicio del usuario. |
| DMP-008 | Integridad primero | Ante incertidumbre, información insuficiente o conflicto de reglas: priorizar integridad del procesamiento. Solicitar intervención del usuario o aplicar estrategias definidas. |
| DMP-009 | Independencia tecnológica | Reglas y criterios definidos independientemente de lenguaje, herramienta, proveedor o modelo de IA. |
| DMP-010 | Evolución controlada | Toda adición, modificación o eliminación de reglas se documenta previamente y preserva compatibilidad con el modelo. |
| DMP-011 | Transparencia | Decisiones comprensibles para el usuario. El sistema proporciona justificación con criterios y reglas principales. |
| DMP-012 | Jerarquía de reglas | Ante resultados incompatibles entre reglas, se resuelve por orden de prioridad definido. Prohibida la ejecución simultánea de decisiones contradictorias para la misma oferta. |
| DMP-013 | Preservación de contexto | Solo se usa información relevante al estado actual de la oferta y al contexto del proceso. No se usa información obsoleta, inconsistente o de etapas incompatibles. |
| DMP-014 | Sin aprendizaje autónomo | La automatización no modifica autónomamente reglas, criterios, umbrales ni ningún elemento del modelo. Toda modificación requiere aprobación explícita del usuario y documentación. |
| DMP-015 | Consistencia con flujo funcional | Toda decisión respeta el flujo funcional, ciclo de vida de la oferta y transiciones de estado. Ninguna decisión provoca transiciones incompatibles, omite etapas obligatorias o altera el comportamiento esperado sin regla documentada que lo autorice. |

---

## 3. Arquitectura del Modelo de Decisión

Componente transversal utilizado por distintos módulos, sin depender de implementación tecnológica específica. Opera como flujo secuencial: inputs → evaluación → aplicación de reglas → decisión → registro.

### 3.1 Componentes

| ID | Componente | Responsabilidad |
|---|---|---|
| DMA-001 | **Inputs** | Conjunto de información para evaluar y decidir (ver §5). |
| DMA-002 | **Motor de Evaluación** | Analiza criterios, calcula scores, detecta violaciones, identifica condiciones especiales, genera resultados intermedios. **No decide**; solo produce información objetiva. |
| DMA-003 | **Motor de Reglas** | Aplica reglas de aceptación, rechazo, resolución de conflictos, prioridades, excepciones. Determina si la decisión es automática o requiere intervención. |
| DMA-004 | **Motor de Decisión** | Emite la decisión final por oferta, cumpliendo principios y alineada al flujo funcional. |
| DMA-005 | **Registro y Auditoría** | Almacena: datos evaluados, resultados, reglas aplicadas, decisión, justificación, fecha/hora, responsable, estado resultante. |

### 3.2 Flujo conceptual

1. Recibir inputs.
2. Validar información disponible.
3. Evaluar criterios.
4. Aplicar reglas de negocio.
5. Resolver conflictos entre reglas (si aplica).
6. Determinar decisión.
7. Asignar estado resultante.
8. Registrar completamente para trazabilidad y auditoría.

### 3.3 Responsabilidades del modelo

- Evaluar objetivamente la información.
- Aplicar reglas aprobadas.
- Emitir decisiones consistentes y reproducibles.
- Priorizar ofertas.
- Determinar si una oferta continúa, se detiene o requiere intervención.
- Garantizar trazabilidad.
- Preservar consistencia con flujo funcional y ciclo de vida.

### 3.4 Fuera de alcance

- Modificar autónomamente reglas de negocio.
- Alterar el perfil profesional del usuario.
- Sustituir decisiones estratégicas del usuario.
- Ejecutar acciones operativas ajenas al proceso de decisión.
- Implementar lógica técnica de módulos consumidores.
- Depender de un modelo de IA, lenguaje o herramienta específica.

---

## 4. Tipos de Decisiones

### 4.1 Decisiones Automatizadas (TD-001)

Ejecutables sin intervención del usuario, respaldadas por reglas documentadas.

**Ejemplos:** detectar duplicados, validar información obligatoria, clasificar, asignar prioridad, rechazar por violación objetiva de reglas, actualizar estados del flujo.

**Características:** basadas en reglas, deterministas, reproducibles, auditables, reversibles cuando la arquitectura lo permita.

### 4.2 Recomendaciones (TD-002)

Conclusiones generadas para apoyar la decisión del usuario. No modifican estado ni ejecutan acciones estratégicas.

**Ejemplos:** recomendar continuar con una aplicación, revisión manual, rechazo por baja compatibilidad, actualización de información antes de proceder.

**Características:** basadas en información verificable, justificadas con reglas documentadas, trazables, independientes de la decisión final del usuario.

### 4.3 Decisiones Estratégicas (TD-003)

Impacto excede las responsabilidades de la automatización. Requieren autorización explícita del usuario. No se ejecutan automáticamente.

**Ejemplos:** aprobar una aplicación, decidir aplicar a una empresa, modificar criterios profesionales, autorizar compartir información con terceros.

**Características:** tomadas exclusivamente por el usuario, registradas en historial, con justificación y trazabilidad completa.

### 4.4 Decisiones Operativas (TD-004)

Controlan el funcionamiento interno de la automatización. Afectan comportamiento técnico pero no decisiones estratégicas.

**Ejemplos:** reintentar proceso, pausar/reanudar ejecución, marcar oferta para revisión, cambiar estado operativo.

**Características:** respetan estrategias de recuperación, preservan integridad del procesamiento, mantienen consistencia del flujo funcional.

### 4.5 Decisiones de Excepción (TD-005)

Situaciones fuera del flujo normal que requieren reglas especiales. Objetivo: preservar estabilidad y continuidad ante condiciones anormales.

**Ejemplos:** información insuficiente, reglas en conflicto, datos inconsistentes, dependencias externas no disponibles, resultados no concluyentes.

**Características:** aplicadas solo con condición documentada que las justifique, trazabilidad completa, priorizan integridad, solicitan intervención del usuario si no existe resolución automática permitida.

### 4.6 Jerarquía de decisiones

Cuando una oferta está sujeta a múltiples tipos simultáneamente, se resuelve en este orden (de mayor a menor prioridad):

1. Decisiones de excepción
2. Decisiones estratégicas del usuario
3. Decisiones automatizadas
4. Decisiones operativas
5. Recomendaciones

Ningún tipo puede contradecir a otro de nivel superior.

### 4.7 Unicidad de decisión

Por proceso funcional y por oferta: una sola decisión activa como resultado final. Resultados intermedios múltiples se resuelven con reglas antes de emitir la decisión final. Toda decisión reemplazada, descartada o modificada se preserva en el historial.

---

## 5. Inputs del Modelo de Decisión

**Condiciones generales para todo input:**
- Identificable unívocamente.
- Proveniente de fuente autorizada.
- Validado exitosamente.
- Consistente con el estado actual del procesamiento.
- Trazable durante todo el ciclo de vida.
- Disponible para auditorías y reprocesamiento.
- Cumple reglas de integridad del proyecto.

| ID | Input | Contenido |
|---|---|---|
| DMI-001 | **Información de la oferta** | Título, empresa, descripción, responsabilidades, requisitos, habilidades, salario, modalidad, ubicación, tipo de empleo, idioma, fecha de publicación, plataforma fuente, URL, identificadores. Input primario de la evaluación. |
| DMI-002 | **Perfil profesional del usuario** | Experiencia, habilidades técnicas y profesionales, formación académica, certificaciones, idiomas, preferencias laborales, expectativas salariales, modalidad preferida, ubicación, empresas objetivo, empresas restringidas. Sincronizado con la versión aprobada por el usuario. |
| DMI-003 | **Reglas de negocio** | Reglas de aceptación, rechazo, priorización, clasificación, umbrales, excepciones, restricciones. Fundamento de toda decisión automatizada. |
| DMI-004 | **Configuración del sistema** | Parámetros generales, de evaluación, umbrales configurables, preferencias de procesamiento, configuraciones de módulos. Gestión centralizada. |
| DMI-005 | **Información histórica** | Historial de ofertas, resultados previos, decisiones previas, eventos de reprocesamiento, cambios de estado, métricas. Su uso nunca compromete la reproducibilidad. |
| DMI-006 | **Resultados intermedios** | Scores parciales, validaciones completadas, clasificaciones temporales, indicadores de compatibilidad, observaciones. Solo utilizables dentro del contexto de la oferta evaluada. |
| DMI-007 | **Decisiones del usuario** | Aprobaciones, rechazos manuales, modificaciones de prioridad, autorizaciones, reprocesamientos solicitados, cambios aprobados de criterios. Prevalecen sobre recomendaciones de la automatización cuando las reglas lo establecen. |
| DMI-008 | **Estado de la oferta** | Estado de ciclo de vida y operativo actual. Determina qué reglas aplican y qué decisiones están permitidas. No se ejecutan decisiones incompatibles con el estado actual. |

---

## 6. Criterios de Evaluación

Cada criterio es una dimensión independiente de evaluación. La definición no establece pesos, importancia relativa ni umbrales (se definen en reglas de negocio correspondientes).

**Principios aplicables a todos los criterios:**
- Evaluados independientemente.
- Basados exclusivamente en información validada.
- Objetivos y reproducibles.
- Trazabilidad completa.
- Reglas documentadas.
- Extensibles sin afectar criterios existentes.
- Independientes de tecnología.
- Consistentes con perfil del usuario y estado actual de la oferta.

| ID | Criterio | Evalúa | Aspectos considerados |
|---|---|---|---|
| EC-001 | Compatibilidad profesional | Alineación perfil usuario vs. perfil requerido | Cargo, campo profesional, nivel de experiencia, seniority, especialización, responsabilidades primarias |
| EC-002 | Habilidades técnicas | Alineación de habilidades técnicas | Tecnologías, herramientas, lenguajes, frameworks, plataformas, metodologías, conocimiento especializado |
| EC-003 | Habilidades profesionales | Alineación de habilidades blandas | Liderazgo, comunicación, trabajo en equipo, organización, resolución de problemas, adaptabilidad, otras relevantes |
| EC-004 | Experiencia laboral | Correspondencia de experiencia | Años, experiencia específica, industrias, responsabilidades, nivel de responsabilidad, trayectoria |
| EC-005 | Formación académica | Compatibilidad educativa | Nivel, títulos, programas, especializaciones, certificaciones, estudios adicionales |
| EC-006 | Idiomas | Alineación de idiomas | Idioma, nivel requerido, nivel demostrado, certificaciones |
| EC-007 | Condiciones laborales | Compatibilidad de condiciones | Modalidad, tipo de empleo, horario, jornada, disponibilidad requerida |
| EC-008 | Ubicación geográfica | Compatibilidad geográfica | Ciudad, país, remoto, híbrido, reubicación, restricciones geográficas |
| EC-009 | Compensación | Compatibilidad salarial | Salario, rango, moneda, beneficios financieros. Sin información salarial → aplicar reglas de información incompleta. |
| EC-010 | Empresa | Aspectos de la organización | Empresas objetivo, empresas restringidas, sector industrial, preferencias del usuario |
| EC-011 | Calidad de la oferta | Calidad y suficiencia de la información | Completitud, claridad, consistencia, disponibilidad de información obligatoria, nivel de detalle. Baja calidad reduce confiabilidad sin necesariamente implicar rechazo. |
| EC-012 | Restricciones del usuario | Cumplimiento de restricciones explícitas | Empresas excluidas, tecnologías no deseadas, modalidades inaceptables, ubicaciones restringidas, condiciones inaceptables, otras configuradas. **Prevalecen sobre cualquier criterio de compatibilidad.** |

---

## 7. Sistema de Puntuación

Mecanismo que transforma resultados de evaluación en medida cuantitativa de compatibilidad. No constituye decisión por sí mismo; es input para reglas de aceptación, rechazo y priorización.

| ID | Regla | Contenido |
|---|---|---|
| SS-001 | Objetivo | Medir compatibilidad, facilitar comparación entre ofertas, servir de input a reglas de decisión, mantener criterios consistentes, reducir subjetividad. |
| SS-002 | Estructura | Score = combinación de resultados de criterios. Cada criterio contribuye independientemente según ponderación. Pesos específicos se documentan con las reglas de negocio. |
| SS-003 | Independencia | Cada criterio se calcula independientemente. Un resultado no modifica otro salvo regla documentada que lo autorice. |
| SS-004 | Ponderación | Peso relativo distinto por criterio. Documentada, configurable, gestión centralizada, modificable sin alterar lógica general. |
| SS-005 | Penalizaciones | Aplicables cuando la oferta incumple condiciones específicas. Documentadas, objetivas, reproducibles, trazables. No implican rechazo automático necesariamente. |
| SS-006 | Bonificaciones | Aplicables por características especialmente favorables. Basadas en reglas documentadas, objetivas, trazables, consistentes. |
| SS-007 | Información insuficiente | Se aplica tratamiento definido para información incompleta. La ausencia no se interpreta automática como favorable ni desfavorable salvo regla específica. |
| SS-008 | Normalización | Score final en escala uniforme para todas las ofertas. Permite comparación objetiva. |
| SS-009 | Clasificación del resultado | Score → nivel de compatibilidad. Rangos específicos se definen con reglas de negocio. Sirve de input a reglas de aceptación/rechazo/priorización. |
| SS-010 | Reproducibilidad | Mismo resultado si no cambian: inputs, reglas, configuración, versión del modelo. |
| SS-011 | Trazabilidad | Registrar: criterios evaluados, resultados individuales, penalizaciones, bonificaciones, score final, nivel de compatibilidad, fecha/hora, versión de reglas. |

---

## 8. Reglas de Aceptación

Condiciones para que una oferta avance en el flujo funcional. Se aplican tras completar la evaluación y antes del procesamiento profundo.

| ID | Regla |
|---|---|
| AR-001 | Cumplir criterios mínimos definidos por reglas de negocio. Incumplir uno o más criterios obligatorios impide aceptación, independientemente del score. |
| AR-002 | Alcanzar nivel mínimo de compatibilidad establecido. Umbrales definidos en reglas de negocio. |
| AR-003 | Información suficiente para evaluación confiable. Si es insuficiente → aplicar reglas de información incompleta antes de aceptar o rechazar. |
| AR-004 | Cumplir toda restricción obligatoria del usuario. Ninguna oferta se acepta si viola una restricción obligatoria. |
| AR-005 | Información libre de inconsistencias que impidan interpretación correcta. Inconsistencias significativas → aplicar reglas de validación o excepción antes de continuar. |
| AR-006 | Estado de ciclo de vida compatible con evaluación. No se aceptan ofertas ya completadas, rechazadas o en estados incompatibles. |
| AR-007 | Ausencia de conflictos entre reglas aplicadas. Conflictos detectados → resolver según mecanismo definido antes de emitir decisión final. |
| AR-008 | Evaluación completada exitosamente con todos los resultados requeridos disponibles. No se aceptan ofertas con evaluación incompleta o interrumpida. |
| AR-009 | **Registro obligatorio:** ID de oferta, fecha/hora, resultado de evaluación, nivel de compatibilidad, reglas aplicadas, justificación, estado asignado, responsable. |
| AR-010 | La aceptación autoriza únicamente la transición a la siguiente etapa del flujo funcional. No implica aprobación automática de aplicación, transmisión de información a terceros ni ninguna decisión estratégica del usuario. |

---

## 9. Reglas de Rechazo

Condiciones bajo las cuales una oferta termina su procesamiento sin avanzar. Aplicadas objetiva, consistentemente y solo con regla documentada.

| ID | Regla |
|---|---|
| RD-001 | Incumplimiento de uno o más criterios obligatorios → rechazo. |
| RD-002 | Compatibilidad inferior al umbral mínimo → rechazo. Umbrales definidos por reglas de negocio. |
| RD-003 | Violación de restricción obligatoria del usuario (empresas restringidas, modalidad, ubicación, condiciones, tecnologías, otras) → rechazo. |
| RD-004 | Información inconsistente, corrupta o insuficiente para evaluación confiable sin estrategia documentada de resolución → rechazo. |
| RD-005 | Duplicado de oferta previamente registrada sin regla de reprocesamiento → rechazo del nuevo registro, preservando historial existente. No se elimina información previa. |
| RD-006 | Estado de ciclo de vida incompatible con procesamiento posterior → rechazo. Solo reprocesable con regla autorizada. |
| RD-007 | Conflictos entre reglas irresolubles por mecanismos definidos → no continúa automáticamente. Se aplica estrategia definida (rechazo o intervención del usuario). |
| RD-008 | **Validación previa al rechazo:** evaluación completada, regla válida, ninguna regla de mayor prioridad impide el rechazo, resultado consistente con estado actual. |
| RD-009 | **Registro obligatorio:** ID de oferta, fecha/hora, regla aplicada, motivo, resultados de evaluación, estado asignado, responsable. |
| RD-010 | Oferta rechazada no avanza a etapas posteriores. Solo reprocesable con regla documentada o autorización explícita del usuario. |

---

## 10. Priorización de Ofertas

Mecanismo para ordenar ofertas aceptadas según nivel de interés. Solo aplica a ofertas que pasaron aceptación.

| ID | Regla |
|---|---|
| JP-001 | **Objetivo:** determinar orden de procesamiento, identificar oportunidades de mayor potencial, optimizar recursos, facilitar revisión del usuario, establecer criterio de clasificación consistente. |
| JP-002 | **Criterios:** resultado del scoring, nivel de compatibilidad, cumplimiento de criterios clave, restricciones del usuario, calidad de información, reglas aplicables, otros definidos por el proyecto. Importancia relativa definida por reglas de negocio. |
| JP-003 | **Niveles:** Alta, Media, Baja. Toda oferta aceptada recibe exactamente un nivel. Criterios de asignación documentados en reglas de negocio. |
| JP-004 | **Unicidad:** una sola prioridad activa por oferta. Nueva evaluación que modifique prioridad preserva la anterior en historial. |
| JP-005 | **Repriorización** cuando: información de la oferta se actualiza, perfil del usuario se modifica, reglas de negocio cambian, se realiza reprocesamiento autorizado, nueva información relevante disponible. Todo evento registrado en historial. |
| JP-006 | **Independencia del procesamiento:** prioridad determina orden recomendado pero no modifica resultado de evaluación ni sustituye reglas de aceptación/rechazo. Oferta de alta prioridad cumple todas las reglas del flujo. |
| JP-007 | **Resolución de empates:** mecanismos objetivos, reproducibles, documentados y consistentes definidos por reglas de negocio. Hasta su definición, ofertas con mismo nivel se consideran equivalentes. |
| JP-008 | **Validación previa:** evaluación completada, score válido, reglas aplicadas, sin conflictos pendientes, oferta elegible. |
| JP-009 | **Registro:** ID de oferta, fecha/hora, nivel asignado, resultado de evaluación, reglas aplicadas, justificación, responsable. |
| JP-010 | **Uso de la prioridad:** orden de procesamiento profundo, organización de presentación al usuario, programación de ejecuciones futuras, optimización de recursos, reportes y estadísticas. No autoriza automáticamente ninguna acción estratégica. |

---

## 11. Reglas de Transición de Decisiones

Condiciones bajo las cuales una decisión modifica el estado de una oferta en el flujo funcional. Ninguna decisión produce cambios de estado no documentados y autorizados.

| ID | Regla |
|---|---|
| DTR-001 | Solo transiciones previamente definidas en el flujo funcional. Prohibidas transiciones implícitas, arbitrarias o no documentadas. |
| DTR-002 | **Validación previa:** evaluación completada, decisión determinada, sin conflictos pendientes, estado compatible con la transición solicitada. |
| DTR-003 | Solo entre estados de ciclo de vida y operativos compatibles. Prohibidas transiciones que contradigan el flujo aprobado. |
| DTR-004 | **Aceptación →** transición a la siguiente etapa del flujo. No autoriza acciones estratégicas. |
| DTR-005 | **Rechazo →** terminación del procesamiento según flujo. Se preserva toda información para auditorías y reprocesamiento futuro. |
| DTR-006 | **Intervención del usuario →** suspensión de transición automática hasta recibir decisión del usuario. Luego se continúa según reglas del escenario. |
| DTR-007 | **Reprocesamiento →** retorno solo a etapas definidas por reglas. No elimina ni sobreescribe historial previo. |
| DTR-008 | **Recuperación →** continuación desde el estado más apropiado, evitando repetir etapas completadas. Cumple estrategias de recuperación ante fallos. |
| DTR-009 | **Transiciones prohibidas:** omitir etapas obligatorias, retroceder arbitrariamente, ejecutar etapas fuera de secuencia, mantener estados incompatibles simultáneamente, modificar estados finales sin autorización. Excepciones solo con regla documentada. |
| DTR-010 | **Registro:** estado previo, estado resultante, decisión que disparó la transición, regla aplicada, fecha/hora, responsable, justificación. |

**Flujo conceptual de transición:**
1. Verificar estado actual de la oferta.
2. Validar información requerida disponible.
3. Aplicar reglas de evaluación.
4. Determinar decisión.
5. Verificar compatibilidad de transición.
6. Actualizar estado.
7. Registrar en historial.
8. Continuar con siguiente proceso o terminar.

---

## 12. Casos Especiales

Situaciones anticipadas que requieren tratamiento diferente al flujo normal sin ser error ni excepción. Todo caso especial tiene estrategia de manejo definida antes de incorporarse.

**Principios aplicables:** documentado previamente, criterios objetivos de identificación, estrategia definida, trazabilidad completa, preserva consistencia del modelo, evita decisiones ambiguas, no altera flujo funcional salvo regla documentada, facilita adición de nuevos casos sin afectar existentes.

| ID | Caso | Manejo |
|---|---|---|
| SC-001 | **Información incompleta** | Aplicar reglas definidas según importancia de la información faltante. No implica aceptación ni rechazo automático. |
| SC-002 | **Información en conflicto** | Identificar conflicto, aplicar reglas de validación. Sin resolución → no se genera decisión final. |
| SC-003 | **Información actualizada** | Determinar si requiere nueva evaluación o solo actualización de historial. Toda reevaluación preserva trazabilidad de decisiones previas. |
| SC-004 | **Oferta previamente procesada** | Determinar: mantener decisión existente, actualizar evaluación, repriorizar, reprocesar o preservar solo historial. Según reglas de reprocesamiento. |
| SC-005 | **Múltiples ubicaciones** | Evaluar cada ubicación/modalidad según preferencias y restricciones del usuario antes de decidir. |
| SC-006 | **Salario ausente** | Aplicar reglas de información incompleta para el criterio de compensación. No implica rechazo automático. |
| SC-007 | **Reglas parcialmente aplicables** | Excluir criterios no aplicables según reglas definidas, preservando consistencia del resultado global. |
| SC-008 | **Cambio en reglas de negocio post-evaluación** | Determinar: preservar decisión actual o iniciar reevaluación. Toda reevaluación registrada como nuevo evento. |
| SC-009 | **Intervención del usuario durante evaluación** | Registrar intervención y adaptar flujo según reglas. Decisiones del usuario prevalecen sobre recomendaciones automatizadas cuando el modelo lo establece. |
| SC-010 | **Casos especiales futuros** | Incorporación mediante reglas documentadas, preservando compatibilidad. Ningún caso modifica principios generales del documento. |

---

## 13. Manejo de Excepciones

Reglas aplicables cuando una situación impide continuar el proceso normal de evaluación y no puede resolverse por el flujo estándar. Objetivo: preservar integridad, consistencia y minimizar impacto operativo.

**Principios aplicables:** detección oportuna, preservar integridad de información, mantener continuidad cuando sea posible, escalar solo lo no resoluble automáticamente, trazabilidad completa, reproducibilidad de estrategias, sin decisiones improvisadas o no documentadas, independencia tecnológica.

| ID | Regla |
|---|---|
| EH-001 | **Identificación:** detectar toda situación que impida determinar una decisión válida con reglas normales. No implica necesariamente error del sistema. |
| EH-002 | **Clasificación por naturaleza:** información insuficiente, inconsistente, conflictos entre reglas, estados incompatibles, dependencias externas, errores de evaluación, configuraciones inválidas. Clasificación específica documentada en el documento de Manejo de Errores. |
| EH-003 | **Evaluación de recuperabilidad:** determinar si se resuelve automáticamente o requiere intervención del usuario. Estrategia cumple reglas de negocio y preserva consistencia. |
| EH-004 | **Resolución automática:** solo con estrategia documentada. Debe: cumplir reglas, preservar información existente, mantener trazabilidad, evitar efectos secundarios en otras ofertas. |
| EH-005 | **Escalamiento al usuario:** cuando no hay resolución automática o involucra decisión estratégica. La oferta permanece en estado compatible con espera. |
| EH-006 | **Preservación de contexto:** estado de la oferta, información evaluada, reglas aplicadas, resultados obtenidos, momento de la excepción. Disponible para análisis, auditoría y reprocesamiento. |
| EH-007 | **Continuidad post-resolución:** continuar desde la etapa más apropiada sin repetir etapas completadas. Si no es posible → flujo de terminación o intervención del usuario. |
| EH-008 | **Protección de integridad:** ninguna excepción produce: pérdida de información, corrupción de datos, estados incompatibles, decisiones contradictorias, omisión de registros obligatorios. Integridad prevalece sobre continuidad. |
| EH-009 | **Registro obligatorio:** ID de oferta, tipo de excepción, descripción, fecha/hora, estado al momento, regla involucrada (si aplica), estrategia aplicada, resultado, responsable de la resolución. |
| EH-010 | **Mejora continua:** información de excepciones identifica oportunidades de mejora. Nuevas estrategias requieren actualización de documentación oficial antes de implementación. |

---

## 14. Decisiones Reservadas al Usuario

Decisiones que por su naturaleza estratégica, personal, profesional o legal no se ejecutan automáticamente. La automatización actúa como soporte, no como sustituto del juicio humano.

**Principios aplicables:** requieren autorización explícita, trazabilidad completa, historial preservado, prevalecen sobre recomendaciones automatizadas en caso de conflicto, no automatizables sin modificación formal de documentación, preservan autonomía del usuario, independencia tecnológica.

Ninguna regla, proceso o componente puede modificar este principio sin aprobación explícita del usuario y actualización de documentación oficial.

| ID | Decisión |
|---|---|
| URD-001 | **Aprobación de oportunidad laboral:** exclusiva del usuario. La automatización genera recomendaciones, análisis y scores, pero no decide si una oferta representa una oportunidad profesional. |
| URD-002 | **Rechazo por criterios personales:** el usuario puede rechazar por motivos no determinables objetivamente (interés personal, cultura organizacional, reputación, experiencias previas, preferencias, información externa). |
| URD-003 | **Modificación de prioridad:** el usuario puede modificar la prioridad asignada automáticamente. Se preserva el valor original calculado en el historial. |
| URD-004 | **Aprobación de aplicación laboral:** exclusiva del usuario. La automatización genera toda la información necesaria pero nunca decide automáticamente. |
| URD-005 | **Autorización para compartir información:** toda transmisión, publicación o compartir información personal/profesional con terceros requiere autorización explícita. Incluye: envío de CV, portafolio, formularios, emails, documentos. |
| URD-006 | **Modificación del perfil profesional:** toda modificación (CV, perfil, portafolio, experiencia, habilidades, certificaciones, preferencias) requiere aprobación explícita. La automatización puede proponer pero nunca aplicar automáticamente. |
| URD-007 | **Modificación de reglas de negocio:** toda modificación al modelo (criterios, reglas de aceptación/rechazo, scoring, umbrales, priorización, casos especiales, excepciones) requiere autorización del usuario. Ningún componente las modifica autónomamente. |
| URD-008 | **Reprocesamiento excepcional:** cuando no se justifica por reglas automatizadas existentes, la decisión es del usuario. Se registra con justificación. |
| URD-009 | **Adición de nuevas fuentes de empleo:** exclusiva del usuario. La automatización no integra nuevas plataformas, APIs o sitios por iniciativa propia. |
| URD-010 | **Adición de nuevas funcionalidades:** toda expansión funcional requiere aprobación previa del usuario. Incluye cualquier modificación que cambie el alcance funcional originalmente aprobado. |

---

## 15. Trazabilidad y Auditoría

Mecanismos para preservar evidencia que permita reconstruir, verificar, analizar y validar toda decisión. Garantiza transparencia, reproducibilidad, rendición de cuentas y mejora continua.

**Principios aplicables:** historial completo de toda decisión, integridad de información, reconstrucción total, facilita auditorías internas y externas, reproducibilidad de decisiones históricas, transparencia, independencia tecnológica, soporta evolución a largo plazo sin comprometer consistencia histórica.

| ID | Regla |
|---|---|
| TA-001 | **Trazabilidad completa:** toda decisión preserva información suficiente para reconstruir el proceso completo: evaluación, aplicación de reglas, transición y resultado final. |
| TA-002 | **Información mínima de auditoría:** ID de oferta, ID de ejecución, ID de decisión, fecha/hora, estado actual, estado previo, estado resultante, resultados de evaluación, reglas aplicadas, score generado, nivel de compatibilidad, prioridad asignada, justificación, responsable, versión de reglas de negocio, versión del modelo de decisión. Información adicional incorporable si no compromete consistencia. |
| TA-003 | **Inmutabilidad de registros históricos:** registros inmutables. Cambio de decisión → nuevo registro sin modificar ni eliminar el previo. |
| TA-004 | **Historial de decisiones:** toda oferta mantiene historial completo: evaluaciones, decisiones, transiciones, reprocesamientos, intervenciones del usuario, excepciones, cambios de prioridad, actualizaciones de reglas, recuperaciones. |
| TA-005 | **Trazabilidad de reglas:** toda decisión preserva las reglas exactas usadas. Si las reglas evolucionan, la versión registrada permite reproducir la decisión bajo las mismas condiciones históricas. |
| TA-006 | **Trazabilidad de evaluación:** preservar resultados intermedios necesarios para reconstruir la decisión final: scores parciales, resultados por criterio, validaciones, penalizaciones, bonificaciones, cálculos de compatibilidad. |
| TA-007 | **Trazabilidad de acciones del usuario:** toda intervención registrada: aprobaciones, rechazos manuales, cambios de prioridad, modificaciones de reglas, autorizaciones de reprocesamiento, actualizaciones de perfil. Prevalecen sobre recomendaciones automatizadas cuando las reglas lo establecen. |
| TA-008 | **Disponibilidad para auditoría:** información disponible durante el ciclo de vida definido por políticas de retención de datos. Almacenamiento garantiza integridad, accesibilidad y consistencia. |
| TA-009 | **Reproducibilidad:** información registrada permite reproducir cualquier decisión si no cambian: inputs, configuración, reglas, versión del modelo. Resultado reproducido ≡ decisión original. |
| TA-010 | **Mejora continua:** información de trazabilidad y auditoría soporta: análisis de procesos, detección de oportunidades de mejora, validación de nuevas reglas, identificación de situaciones recurrentes, optimización continua. Toda mejora se documenta antes de implementar. |
