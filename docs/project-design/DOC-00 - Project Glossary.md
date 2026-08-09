# Glosario del Proyecto (DOC-00)

**Objetivo:** Definición oficial única de todos los conceptos del proyecto. Garantiza consistencia terminológica en documentación, desarrollo y mantenimiento.

## Principios de gobernanza

1. Un término = una definición oficial. Ningún documento redefine términos existentes.
2. Todo concepto nuevo se incorpora aquí.
3. Definiciones independientes de la tecnología.
4. Códigos de identificación permanentes; nunca se reutilizan.

---

## 1. Conceptos Generales

| Código | Término | Definición |
|--------|---------|------------|
| GLO-001 | Automatización | Sistema que ejecuta autónomamente tareas repetitivas de búsqueda de empleo; el usuario mantiene todas las decisiones estratégicas. |
| GLO-002 | Oferta de trabajo (Job Posting) | Oportunidad laboral publicada por una fuente y registrada en el sistema para su procesamiento. |
| GLO-003 | Fuente de empleo (Job Source) | Plataforma, sitio web, API u otro origen del cual la automatización obtiene ofertas. |
| GLO-004 | Perfil profesional | Conjunto de información profesional usada para evaluar la compatibilidad del usuario con una oferta. |
| GLO-005 | Compatibilidad | Grado de alineación entre el perfil profesional y los requisitos de una oferta. |
| GLO-006 | Prioridad | Nivel asignado a una oferta según los criterios de evaluación establecidos. |
| GLO-007 | Paquete de postulación (Application Package) | Conjunto de recursos preparados para respaldar una postulación a una oferta. |
| GLO-008 | Material de apoyo (Supporting Material) | Documento, análisis u otro recurso generado por la automatización para respaldar una postulación. |

## 2. Actores

| Código | Término | Definición |
|--------|---------|------------|
| GLO-009 | Usuario | Propietario de la automatización; responsable exclusivo de todas las decisiones estratégicas. |
| GLO-010 | Dependencia externa | Sistema, servicio o plataforma con el que la automatización interactúa para obtener información o ejecutar procesos. |

## 3. Flujo de Trabajo Funcional

| Código | Término | Definición |
|--------|---------|------------|
| GLO-011 | Flujo de trabajo funcional (Functional Workflow) | Secuencia ordenada de procesos que una oferta sigue desde su descubrimiento hasta completar su procesamiento. |
| GLO-012 | Proceso funcional (FP) | Etapa específica dentro del flujo de trabajo funcional. |
| GLO-013 | Ciclo de vida (Lifecycle) | Conjunto de etapas funcionales que una oferta puede atravesar mientras permanezca en el sistema. |
| GLO-014 | Estado de ciclo de vida (Lifecycle Status) | Etapa funcional actual de una oferta. |
| GLO-015 | Estado operativo (Operational Status) | Condición técnica/operativa de una oferta durante el procesamiento. Valores: *Running, Waiting, Retrying, Paused, Error*. |

## 4. Procesamiento

| Código | Término | Definición |
|--------|---------|------------|
| GLO-016 | Descubrimiento (Discovery) | Proceso de identificación de nuevas ofertas. |
| GLO-017 | Preparación (Preparation) | Limpieza, normalización y validación de la información recuperada. |
| GLO-018 | Evaluación inicial (Initial Evaluation) | Cálculo del nivel de compatibilidad de una oferta aplicando las reglas definidas. |
| GLO-019 | Procesamiento profundo (Deep Processing) | Análisis detallado de una oferta para generar información estratégica y materiales de apoyo para la postulación. |
| GLO-020 | Normalización (Normalization) | Transformación de información a formatos estandarizados para facilitar el procesamiento. |
| GLO-021 | Validación (Validation) | Verificación de que una oferta cumple las condiciones necesarias para continuar en el flujo funcional. |
| GLO-022 | Reprocesamiento (Reprocessing) | Re-ejecución de una o más etapas del flujo funcional sobre una oferta previamente procesada. |
| GLO-023 | Duplicado (Duplicate) | Oferta que representa la misma oportunidad laboral que otra ya registrada en el sistema. |

## 5. Datos

| Código | Término | Definición |
|--------|---------|------------|
| GLO-024 | Entrada (Input) | Información recibida por la automatización desde una fuente externa. |
| GLO-025 | Dato interno (Internal Data) | Información generada y mantenida por la automatización para controlar su operación. |
| GLO-026 | Salida (Output) | Información entregada por la automatización como resultado de su procesamiento. |
| GLO-027 | Historial (History) | Registro cronológico de todos los eventos relacionados con una oferta. |
| GLO-028 | Trazabilidad (Traceability) | Capacidad de reconstruir el recorrido completo de una oferta: acciones, decisiones, estados y resultados. |

## 6. Decisiones

| Código | Término | Definición |
|--------|---------|------------|
| GLO-029 | Acción automatizada (Automated Action) | Actividad operativa ejecutada automáticamente sin requerir decisión. |
| GLO-030 | Decisión automatizada (Automated Decision) | Decisión tomada por la automatización usando reglas previamente documentadas. |
| GLO-031 | Recomendación (Recommendation) | Sugerencia generada por la automatización para apoyar la toma de decisiones del usuario. |
| GLO-032 | Decisión estratégica (Strategic Decision) | Decisión reservada exclusivamente al usuario por su impacto personal, profesional o legal. |
| GLO-033 | Regla de negocio (Business Rule) | Condición documentada que determina cómo debe comportarse la automatización en una situación específica. |
| GLO-034 | Regla funcional (Functional Rule) | Regla permanente que define el comportamiento global del sistema. |

## 7. Arquitectura

| Código | Término | Definición |
|--------|---------|------------|
| GLO-035 | Motor de procesos (Process Engine) | Componente que ejecuta y coordina el flujo de trabajo funcional. |
| GLO-036 | Motor de decisiones (Decision Engine) | Componente que aplica reglas de negocio para producir decisiones automatizadas y recomendaciones. |
| GLO-037 | Módulo (Module) | Componente funcional independiente que implementa una parte específica de la automatización. |
| GLO-038 | Configuración (Configuration) | Conjunto de parámetros que determinan el comportamiento de la automatización. |

## 8. Gestión

| Código | Término | Definición |
|--------|---------|------------|
| GLO-039 | Auditoría (Audit) | Capacidad del sistema de justificar toda acción, decisión y cambio de estado mediante registros verificables. |
| GLO-040 | Métrica (Metric) | Indicador para medir rendimiento, operación o calidad de la automatización. |
| GLO-041 | Log | Evento almacenado para documentar ejecución de procesos, decisiones, errores u otras acciones relevantes. |
| GLO-042 | Error | Situación que impide la ejecución normal de un proceso y requiere estrategia de recuperación o intervención humana. |
| GLO-043 | Excepción (Exception) | Situación infrecuente anticipada por las reglas del sistema que modifica el flujo normal sin representar necesariamente un error. |

## 9. Descubrimiento de Oportunidades (Módulo 1)

| Código | Término | Definición |
|--------|---------|------------|
| GLO-044 | Corrida (Run) | Instancia de ejecución del Módulo 1, identificada por `run_id`. Todo registro generado durante una corrida se ancla a su `run_id` (RN-01). |
| GLO-045 | `run_id` | Identificador único de una corrida; campo de trazabilidad obligatorio en todo registro del Módulo 1 (eventos, sesiones, ofertas). |
| GLO-046 | `session_id` | Identificador de la sesión de plataforma abierta por el Módulo 1 al acceder exitosamente a la fuente; reutilizable por nodos subsiguientes; registrado en auditoría de sesión. |
| GLO-047 | Lote (Batch) | Grupo de ofertas capturadas conjuntamente por el nodo de captura; materializado por el contrato `capture_batch`. |
| GLO-048 | `set_indice` | Índice (0-based, en orden configurado) del conjunto de filtros actualmente aplicado a una fuente; parte de la trazabilidad de todo registro de búsqueda y captura. |
| GLO-049 | Políticas de captura (Capture Policies) | Parámetros que gobiernan la captura: `max_paginas`, `max_ofertas_por_corrida`, `pausa_entre_lotes`, estrategia anti-bloqueo. Valores efectivos por fuente se fusionan con defaults globales (RN-11). |
| GLO-050 | Bloqueo de concurrencia | Registro persistente (con `run_id` y `timestamp`) que garantiza una sola corrida activa a la vez; su umbral de obsolescencia permite sobrescribir un lock stale. |
| GLO-051 | Almacenes lógicos (Logical Stores) | Almacenes conceptuales del Módulo 1 (Ofertas Totales, errores/sucesos, control de sesiones, corridas, bloqueo) persistidos como tablas de una única base SQLite (D2). |
| GLO-052 | `entry_result` | Contrato del nodo "Entrar a la fuente": `{estado, codigo_motivo, evidencia_acotada, numero_de_intentos}`. Sin datos sensibles. |
| GLO-053 | `search_result` | Contrato del nodo "Aplicar los filtros", por set de filtros: `{estado, codigo_motivo, evidencia_acotada, ofertas_primera_pagina, estado_paginacion, total_declarado, set_indice, numero_de_intentos}`. |
| GLO-054 | `capture_batch` | Contrato del nodo "Capturar ofertas": lote capturado y su contabilidad de captura. |
| GLO-055 | `estado_captura` | Contrato del estado de captura: página procesada, capturas acumuladas, si se alcanzó el límite. Consume el estado de paginación de `search_result`. |
| GLO-056 | Grupo A / Grupo B de códigos | Clasificación de códigos de fallo: **Grupo A** compromete la fuente actual (se cierra o la corrida aborta). **Grupo B** es inherente al set de filtros (el set se cierra y se itera al siguiente). |
| GLO-057 | Adaptador (Adapter) | Componente que encapsula la lógica específica de acceso, búsqueda y captura de cada plataforma fuente, conforme a las interfaces oficiales (INT-001 / INT-003). |
