# DOC-06 — Manejo de errores (versión optimizada)

## 1. Propósito y alcance
Este documento define el modelo oficial para detectar, clasificar, registrar, tratar, recuperar y rastrear errores en la automatización de búsqueda de empleo.

Establece principios, reglas y procedimientos uniformes para controlar fallas y minimizar su impacto sobre continuidad, integridad de información y experiencia de usuario.

Es la referencia oficial obligatoria para todos los módulos, procesos, componentes, servicios, integraciones, flujos de datos y recursos de la automatización, independiente de la tecnología usada.

Aplica también a cualquier desarrollo, modificación o extensión que introduzca nuevas condiciones de error o mecanismos de recuperación.

Objetivos operativos:
- Detectar errores oportunamente.
- Registrarlos consistentemente.
- Clasificarlos por severidad.
- Tratarlos con estrategias de recuperación predefinidas.
- Preservarlos para auditoría, trazabilidad y mejora continua.

---

## 2. Principios de manejo de errores (PME)
Estos principios complementan el Project Glossary, Functional Requirements, Non-Functional Requirements, Decision Model, Data Flow y Project Standards.

| ID | Principio |
|---|---|
| PME-001 | Detectar cada error tan pronto como sea posible y evitar su propagación. |
| PME-002 | Registrar todo error según convenciones oficiales de auditoría y trazabilidad. Prohibido errores silenciosos no verificables. |
| PME-003 | Clasificar cada error con criterios oficiales de severidad, origen e impacto. No usar clasificaciones alternativas. |
| PME-004 | Intentar recuperación automática autorizada; si no es viable, terminar controladamente. |
| PME-005 | Nunca comprometer integridad, consistencia ni trazabilidad de la información. |
| PME-006 | Aislar errores para no interrumpir innecesariamente procesos independientes. |
| PME-007 | Incluir información suficiente para análisis, reproducción e investigación. |
| PME-008 | Relacionar cada error con proceso, módulo, componente, oferta, operación o recurso afectado. |
| PME-009 | Mantener independencia de lenguaje, herramienta, proveedor o plataforma. |
| PME-010 | Ninguna recuperación puede causar pérdida de información, duplicación de registros ni alteración del flujo lógico. |
| PME-011 | Permitir incorporar nuevos errores, mecanismos y fuentes sin modificar la estructura general. |
| PME-012 | Mantener alineación con documentación oficial; ningún procedimiento puede contradecir documentos aprobados. |
| PME-013 | Minimizar intervención del usuario; si es necesaria, suministrar información suficiente para decidir. |
| PME-014 | Todo el ciclo de vida del error debe ser auditable mediante logs. |
| PME-015 | Toda modificación al modelo debe documentarse, justificarse y preservar compatibilidad cuando sea posible. |

---

## 3. Arquitectura de manejo de errores (AME)
Modelo obligatorio para todos los procesos: descubrimiento de oportunidades, preparación inicial, evaluación inicial, procesamiento de ofertas, almacenamiento y cualquier componente futuro.

| Etapa | Definición |
|---|---|
| AME-01 Detección | Identificar condición anómala o comportamiento inesperado. |
| AME-02 Clasificación | Determinar tipo, origen, severidad e impacto según reglas oficiales. |
| AME-03 Registro | Registrar información necesaria para trazabilidad y auditoría antes de ejecutar recuperación. |
| AME-04 Evaluación | Determinar si procede recuperación automática o intervención de otro proceso/usuario, usando políticas oficiales. |
| AME-05 Recuperación | Ejecutar estrategia autorizada: reintento, reinicio controlado, re-ejecución, omisión controlada, continuación segura o terminación controlada. |
| AME-06 Validación | Verificar que la recuperación resolvió el error; si no, escalar. |
| AME-07 Escalamiento | Si la recuperación no es posible o es insuficiente, escalar según severidad: nuevos intentos, otro componente, usuario o terminación controlada. |
| AME-08 Cierre | Finalizar formalmente la gestión preservando el histórico. |
| AME-09 Auditoría | Conservar información disponible para auditoría, análisis estadístico, investigación y mejora. |

Flujo obligatorio:
1. Detectar.
2. Clasificar.
3. Registrar.
4. Evaluar estrategia.
5. Recuperar si aplica.
6. Validar recuperación.
7. Escalar si falla.
8. Cerrar incidente.
9. Preservar información para auditoría y trazabilidad.

Ningún componente puede implementar un flujo alternativo que contradiga estas etapas, salvo excepción expresamente documentada y aprobada.

---

## 4. Clasificación de errores

### 4.1 Criterios de clasificación (CE)
| ID | Criterio |
|---|---|
| CE-001 | Origen: componente o recurso donde ocurrió. |
| CE-002 | Naturaleza: tipo de falla. |
| CE-003 | Severidad: impacto operativo. |
| CE-004 | Recuperabilidad: si puede resolverse automáticamente o requiere intervención adicional. |
| CE-005 | Persistencia: temporal o permanente. |
| CE-006 | Alcance: afecta solo una operación o procesos adicionales. |

Cada error pertenece a una única categoría principal y la conserva durante todo su ciclo de vida.

### 4.2 Categorías oficiales (CER)
| ID | Prefijo | Categoría | Ejemplos |
|---|---|---|---|
| CER-001 | ER-RED | Red | Pérdida de conexión; timeout; DNS no disponible; servicio remoto inaccesible. |
| CER-002 | ER-NAV | Navegador | Página no cargada; elemento inexistente; captcha; cambio inesperado de DOM; sesión expirada. |
| CER-003 | ER-EXT | Extracción | Información incompleta; selectores inválidos; dato no encontrado; contenido inaccesible. |
| CER-004 | ER-VAL | Validación | Campos requeridos ausentes; formatos inválidos; datos inconsistentes; valores fuera de rango. |
| CER-005 | ER-LLM | Modelo de lenguaje | Respuesta vacía; inválida; formato incorrecto; tiempo excedido; incapacidad de interpretar contenido. |
| CER-006 | ER-DAT | Datos | Datos corruptos; duplicados; incompatibles; relaciones inconsistentes. |
| CER-007 | ER-DB | Persistencia | Falla de escritura; falla de lectura; archivo inaccesible; recurso bloqueado. |
| CER-008 | ER-CFG | Configuración | Parámetros inexistentes; variables requeridas ausentes; configuración incompatible. |
| CER-009 | ER-INT | Interno | Excepciones no manejadas; estados inválidos; flujo inconsistente; dependencias insatisfechas. |
| CER-010 | ER-EXTS | Externo | API fuera de servicio; cambios en plataformas; restricciones temporales de proveedor; mantenimiento. |

### 4.3 Identificador oficial
Formato obligatorio:
```text
ER-<CATEGORIA>-<SECUENCIAL>
```
Ejemplos: `ER-RED-001`, `ER-NAV-003`, `ER-EXT-015`, `ER-VAL-002`, `ER-LLM-004`, `ER-DAT-007`, `ER-DB-001`, `ER-CFG-002`, `ER-INT-009`, `ER-EXTS-003`.

Cada identificador es único, inmutable y reutilizable solo como referencia histórica.

### 4.4 Reglas de clasificación
- Todo error debe pertenecer a una única categoría principal.
- Todo error debe tener identificador oficial.
- La categoría no puede modificarse después de registrada.
- Nuevas categorías solo por actualización oficial de este documento.
- Ningún componente puede usar clasificaciones distintas.

---

## 5. Fuentes de error (FDE)
| ID | Fuente | Orígenes incluidos |
|---|---|---|
| FDE-001 | Internas | Lógica de negocio; flujos; reglas de decisión; procesos internos; estados inconsistentes; errores de programación; excepciones no manejadas. |
| FDE-002 | Infraestructura | Sistema operativo; recursos de equipo; permisos; espacio de almacenamiento; procesos del sistema; fallas del entorno de ejecución. |
| FDE-003 | Red | Pérdida de conectividad; latencia alta; timeout; DNS; interrupciones; restricciones temporales de acceso. |
| FDE-004 | Navegador | Cambios de interfaz; elementos inexistentes; captchas; ventanas inesperadas; sesiones expiradas; recursos bloqueados. |
| FDE-005 | Extracción | Información incompleta; estructuras modificadas; contenido dinámico; datos inaccesibles; cambios de selectores; información inconsistente. |
| FDE-006 | Modelo de lenguaje | Respuestas inválidas; información insuficiente; formatos inesperados; errores de interpretación; tiempo excedido; fallas de comunicación con el servicio. |
| FDE-007 | Datos | Datos incompletos; duplicados; inconsistencias; formatos incompatibles; relaciones inválidas; información corrupta. |
| FDE-008 | Persistencia | Fallas de escritura/lectura; archivos inexistentes; recursos bloqueados; fallas de sincronización; problemas de acceso. |
| FDE-009 | Configuración | Parámetros inexistentes; configuración incompleta; variables requeridas ausentes; configuraciones incompatibles; valores inválidos. |
| FDE-010 | Usuario | Configuración incorrecta; información incompleta; parámetros inconsistentes; interrupción manual; decisiones incompatibles con el estado actual. |
| FDE-011 | Externas | Plataformas de empleo; APIs externas; servicios de autenticación; servicios de IA; cambios de proveedor; mantenimiento; restricciones de terceros. |
| FDE-012 | Desconocidas | Origen no determinable inmediatamente. Registrar toda la información disponible y observar hasta identificar causa raíz. |

Reglas:
- Todo error debe asociarse al menos a una fuente.
- Una fuente puede originar múltiples categorías.
- Un error puede asociarse a múltiples fuentes si hay evidencia suficiente.
- Las fuentes son independientes de la tecnología.
- Incorporar nuevas fuentes requiere actualización oficial.
- Ningún componente puede definir fuentes incompatibles.

---

## 6. Detección de errores

### 6.1 Principios de detección (PDE)
| ID | Principio |
|---|---|
| PDE-001 | Detectar lo más cerca posible del origen para evitar efectos secundarios. |
| PDE-002 | La detección debe ser automática cuando sea técnicamente posible. |
| PDE-003 | Todo error detectado debe ser demostrable con evidencia objetiva. |
| PDE-004 | La detección debe permanecer activa durante todo el ciclo del proceso. |
| PDE-005 | Detectar un error no implica automáticamente terminar el proceso; la continuidad depende de políticas de recuperación. |

### 6.2 Mecanismos oficiales de detección (MDE)
| ID | Mecanismo | Alcance / ejemplos |
|---|---|---|
| MDE-001 | Validaciones preventivas | Antes de operar: configuraciones obligatorias, recursos disponibles, parámetros válidos, dependencias disponibles. |
| MDE-002 | Validaciones en ejecución | Durante la ejecución: verificación de respuesta, confirmación de operación, elementos esperados, estados válidos. |
| MDE-003 | Validaciones post-ejecución | Tras completar: confirmación de escritura, verificación de almacenamiento, validación de resultados, cambios de estado. |
| MDE-004 | Monitoreo continuo | Supervisar procesos críticos: interrupciones inesperadas, procesos detenidos, consumo anormal, comportamientos inconsistentes. |
| MDE-005 | Timeout | Si una operación excede el tiempo máximo permitido, genera error. Aplica a procesos internos y externos. |
| MDE-006 | Integridad de datos | Verificar información recibida, transformada, almacenada o recuperada. |
| MDE-007 | Respuesta del LLM | Validar como mínimo: existencia de respuesta, estructura esperada, formato requerido e información suficiente para continuar. |
| MDE-008 | Recursos externos | Confirmar que la interacción con plataforma/API/servicio fue correcta antes de continuar. |
| MDE-009 | Reglas de negocio | Verificar cumplimiento de reglas funcionales y modelo de decisión; cualquier incumplimiento es error. |
| MDE-010 | Consistencia de flujo | Verificar que transiciones de estado, decisiones y operaciones respeten el flujo oficial. |

Reglas:
- Detectar antes de propagar cuando sea técnicamente posible.
- Toda detección debe generar evidencia suficiente.
- La ausencia de detección no implica inexistencia del error.
- Los mecanismos deben ser reutilizables por todos los módulos.
- Nuevos mecanismos deben documentarse oficialmente antes de usarse.
- Ningún módulo puede implementar mecanismos incompatibles.

---

## 7. Registro de errores

Objetivos del registro:
- Preservar histórico completo del incidente.
- Facilitar recuperación y diagnóstico.
- Proveer evidencia para auditoría.
- Soportar monitoreo operacional.
- Identificar tendencias y errores recurrentes.
- Generar indicadores de confiabilidad.
- Facilitar mejora continua.

### 7.1 Información mínima obligatoria (RER)
| ID | Campo | Requisito |
|---|---|---|
| RER-001 | Identificador de error | Según convención oficial. |
| RER-002 | Identificador de incidente | Único por evento; distingue múltiples ocurrencias del mismo tipo. |
| RER-003 | Fecha y hora | Exactas, en formato oficial. |
| RER-004 | Módulo | Nombre oficial del módulo afectado. |
| RER-005 | Proceso | Proceso activo al momento del incidente. |
| RER-006 | Componente | Componente responsable de detectar o generar el error. |
| RER-007 | Categoría | Categoría oficial del error. |
| RER-008 | Severidad | Nivel oficial asignado. |
| RER-009 | Fuente | Origen oficialmente identificado. |
| RER-010 | Descripción | Clara, objetiva y sin interpretaciones subjetivas. |
| RER-011 | Evidencia | Mensajes, respuestas, valores, recursos afectados, capturas o referencias si existen. |
| RER-012 | Acción ejecutada | Reintento, recuperación, escalamiento, terminación controlada o notificación. |
| RER-013 | Resultado de acción | Recuperado, parcialmente recuperado, no recuperado, escalado o terminado. |
| RER-014 | Estado del incidente | Detectado, en recuperación, escalado, resuelto o cerrado. |
| RER-015 | Identificador de oferta | Si el error está asociado a una oferta específica. |
| RER-016 | Identificador de ejecución | Relaciona errores ocurridos en la misma ejecución. |
| RER-017 | Referencias de auditoría | Enlaces/identificadores a registros, decisiones, procesos o documentos relacionados. |

### 7.2 Reglas de registro
- Registrar todo error antes de ejecutar cualquier estrategia de recuperación.
- Ningún error puede eliminarse del histórico una vez registrado.
- Toda modificación debe preservar trazabilidad.
- El formato debe ser uniforme en toda la automatización.
- La información debe ser suficiente para reproducir y analizar el incidente.
- Los logs deben conservarse según políticas de retención.
- Ningún módulo puede registrar errores con estructuras distintas.

---

## 8. Niveles de severidad

### 8.1 Criterios de evaluación (NSE)
| ID | Criterio |
|---|---|
| NSE-001 | Impacto operacional: efecto sobre continuidad. |
| NSE-002 | Impacto en datos: efecto sobre integridad, consistencia o disponibilidad. |
| NSE-003 | Alcance: número de módulos/procesos/componentes afectados. |
| NSE-004 | Recuperabilidad: capacidad de resolución automática. |
| NSE-005 | Intervención requerida: nivel de participación de usuario u otro componente. |

### 8.2 Niveles oficiales (SV)
| Nivel | Impacto | Características | Ejemplos | Recuperación automática | Intervención usuario |
|---|---|---|---|---|---|
| SV-1 | Crítico | Impide continuidad o compromete integridad; no puede continuar; sin recuperación automática viable; puede comprometer información crítica; atención inmediata. | Corrupción de información; falla general de persistencia; inconsistencia crítica de flujo; error interno irreparable. | No | Obligatoria |
| SV-2 | Alto | Impide completar correctamente un proceso importante; el resto puede seguir funcionando. | Imposibilidad de procesar oferta; error persistente de LLM; error permanente de plataforma externa; falla repetitiva de extracción. | Parcial o limitada | Probable |
| SV-3 | Medio | Afecta parcialmente un proceso; recuperación automática posible en la mayoría de casos. | Timeout temporal; error transitorio de red; recurso temporalmente no disponible; respuesta incompleta recuperable. | Sí, normalmente | Infrecuente |
| SV-4 | Bajo | Impacto reducido; el proceso puede continuar; no requiere intervención inmediata. | Advertencias de validación; información opcional ausente; retrasos menores; reintento exitoso en primer intento. | Sí | No requerida |
| SV-5 | Informativo | Eventos registrados para auditoría/monitoreo; no son falla operacional. | Recuperación automática exitosa; reintentos exitosos; cambios de estado relevantes; eventos de seguimiento. | No aplica | No requerida |

### 8.3 Reglas de asignación (RSE)
| ID | Regla |
|---|---|
| RSE-001 | Cada error recibe un único nivel oficial. |
| RSE-002 | Asignar severidad inmediatamente después de clasificar. |
| RSE-003 | Solo puede actualizarse con evidencia objetiva de cambio de impacto real; registrar cambios. |
| RSE-004 | No asignar solo por causa; evaluar impacto real. |
| RSE-005 | Dos errores de la misma categoría pueden tener distinta severidad si su impacto difiere. |
| RSE-006 | Recuperación, reintentos, notificación y escalamiento se basan en la severidad asignada. |

---

## 9. Estrategias de recuperación

### 9.1 Principios (PRE)
| ID | Principio |
|---|---|
| PRE-001 | Preservar integridad, consistencia y trazabilidad. |
| PRE-002 | Solo ejecutar estrategias oficiales aprobadas. |
| PRE-003 | Proporcionalidad: no usar mecanismos excesivos para errores menores. |
| PRE-004 | Validar la recuperación antes de continuar. |
| PRE-005 | Registrar toda estrategia ejecutada. |

### 9.2 Catálogo oficial (REC)
| ID | Estrategia | Definición / aplicación |
|---|---|---|
| REC-001 | Reintento automático | Repetir la misma operación sin cambiar contexto. Aplica a errores temporales: timeout, red transitoria, servicio temporalmente no disponible. |
| REC-002 | Esperar y reanudar | Suspender temporalmente hasta que desaparezca la condición. Aplica cuando hay alta probabilidad de recuperación espontánea. |
| REC-003 | Reinicio controlado de operación | Reiniciar solo la operación afectada, conservando el resto del proceso. |
| REC-004 | Reprocesamiento | Reejecutar una etapa completada usando información disponible cuando el resultado pudo afectarse por error recuperable. |
| REC-005 | Continuación segura del flujo | Continuar omitiendo operaciones cuya ausencia no compromete el resultado final. Solo con autorización explícita del modelo de decisión. |
| REC-006 | Omisión controlada | Excluir una operación opcional; registrar la omisión. |
| REC-007 | Escalamiento | Transferir el tratamiento a otro mecanismo, componente o usuario cuando la estrategia actual es insuficiente. |
| REC-008 | Terminación controlada | Detener ordenadamente el proceso cuando no existe estrategia segura; preservar información generada. |
| REC-009 | Solicitud de intervención de usuario | Pedir decisión cuando falta información suficiente; suministrar toda la información necesaria. |

### 9.3 Criterios de selección (SRE)
| ID | Criterio |
|---|---|
| SRE-001 | Severidad. |
| SRE-002 | Recuperabilidad. |
| SRE-003 | Riesgo para integridad de información o proceso. |
| SRE-004 | Continuidad operacional sin comprometer resultados. |
| SRE-005 | Dependencias necesarias para ejecutar la recuperación. |

Reglas:
- Usar solo estrategias oficiales.
- Ninguna estrategia puede comprometer integridad.
- Validar siempre antes de continuar.
- Registrar cada estrategia en el histórico.
- Un mismo error puede requerir varias estrategias secuenciales.
- Si ninguna es efectiva, escalar.
- Nuevas estrategias requieren actualización formal.

---

## 10. Políticas de reintento

### 10.1 Principios (PRT)
| ID | Principio |
|---|---|
| PRT-001 | Solo reintentar si una política oficial lo autoriza; prohibido reintento ilimitado. |
| PRT-002 | Ningún reintento puede causar duplicación, inconsistencias o alteración del flujo oficial. |
| PRT-003 | Solo reintentar operaciones cuya probabilidad de éxito aumente con nueva ejecución. |
| PRT-004 | Registrar cada intento en el histórico del incidente. |
| PRT-005 | Evaluar cada intento independientemente. |

### 10.2 Políticas oficiales (POL-RET)
| ID | Política |
|---|---|
| POL-RET-001 | Definir número máximo de intentos; al alcanzarlo, aplicar otra estrategia o escalar. |
| POL-RET-002 | Establecer intervalo de espera entre reintentos para minimizar repetir inmediatamente la condición. |
| POL-RET-003 | Permitir aumento progresivo de espera si fallas repetidas, según política del proceso, para reducir carga interna/externa. |
| POL-RET-004 | Antes de reintentar, verificar que la condición cambió o existen posibilidades razonables de éxito. |
| POL-RET-005 | Cancelar reintentos si: máximo alcanzado; error no recuperable; riesgo de integridad; sin posibilidad objetiva de éxito; regla del modelo de decisión lo ordena. |
| POL-RET-006 | No reintentar errores no recuperables por naturaleza: configuración inválida, parámetros requeridos ausentes, datos inconsistentes, errores lógicos, restricciones permanentes externas. |
| POL-RET-007 | Registrar como mínimo: número de intento, fecha/hora, resultado, espera aplicada, estrategia usada y estado posterior. |
| POL-RET-008 | Si los reintentos no resuelven, abandonar la política y aplicar la siguiente estrategia; prohibido reiniciar ciclos indefinidamente. |
| POL-RET-009 | El fallo de una política no debe afectar procesos independientes. |
| POL-RET-010 | Proteger servicios externos: evitar comportamiento abusivo y respetar límites operacionales. |

Reglas:
- Toda política debe asociarse a estrategia oficial.
- Ningún reintento compromete integridad.
- Todo intento debe registrarse.
- El máximo de reintentos debe definirse antes de ejecutar el proceso.
- Ninguna operación puede quedar indefinidamente en reintento.
- Agotada la política, continuar con estrategia oficial correspondiente.
- Ningún módulo puede implementar políticas incompatibles.

---

## 11. Manejo de errores por módulo

### 11.1 Reglas comunes
- Todos los módulos cumplen las reglas generales de este documento.
- Solo pueden aplicar estrategias adicionales si no contradicen políticas oficiales.
- Usan exclusivamente categorías oficiales.
- Las estrategias deben corresponder a las autorizadas por módulo.
- Todo incidente se registra antes de recuperar.
- Ningún módulo puede implementar mecanismos incompatibles.
- Modificaciones futuras no deben afectar reglas generales.
- Incorporar nuevos módulos requiere actualización oficial de esta sección.

### 11.2 Módulos funcionales
| Módulo | Objetivo | Errores frecuentes | Categorías | Estrategias permitidas | Reintentos | Terminación |
|---|---|---|---|---|---|---|
| 1. Descubrimiento de oportunidades | Gestionar localización y recuperación inicial de ofertas. | Conectividad; timeout; cambios de estructura; captchas; restricciones temporales; autenticación; información inaccesible. | ER-RED, ER-NAV, ER-EXT, ER-EXTS | REC-001, REC-002, REC-003, REC-007, REC-008 | Políticas oficiales para servicios externos. | Solo si: extracción exitosa; estrategias agotadas; modelo de decisión determina terminar. |
| 2. Preparación inicial de oferta | Gestionar limpieza, normalización y validación inicial. | Campos requeridos ausentes; formatos inválidos; información inconsistente; duplicados; errores de transformación. | ER-VAL, ER-DAT, ER-INT | REC-003, REC-004, REC-006, REC-008 | Solo si el origen es recuperable; errores permanentes de datos no se reintentan. | Cuando la oferta alcanza estado consistente o se determina que no puede recuperarse. |
| 3. Evaluación inicial | Gestionar evaluación automática de compatibilidad. | Reglas inconsistentes; información insuficiente; errores de scoring; estados inválidos. | ER-DAT, ER-VAL, ER-INT | REC-004, REC-005, REC-007, REC-009 | Solo si existe nueva información que permita repetir evaluación con expectativa razonable. | Cuando: resultado válido; oferta descartada definitivamente; usuario interviene si se requiere. |
| 4. Procesamiento de oferta | Gestionar análisis profundo de ofertas seleccionadas. | Respuestas inválidas del LLM; información insuficiente; fallas de análisis; errores de generación de resultado. | ER-LLM, ER-DAT, ER-INT, ER-EXTS | REC-001, REC-004, REC-007, REC-009 | Respetar políticas oficiales para servicios de IA y recursos externos. | Cuando: análisis completo; estrategias agotadas; usuario decide continuación/terminación. |
| 5. Gestión y seguimiento | Gestionar almacenamiento, actualización y seguimiento. | Fallas de escritura/lectura; histórico inconsistente; actualización incompleta; errores de persistencia. | ER-DB, ER-DAT, ER-INT | REC-003, REC-004, REC-007, REC-008 | Deben garantizar que nunca ocurran duplicados o inconsistencias. | Solo si: información almacenada correctamente; histórico consistente; incidente tratado según reglas. |

---

### 11.3 Módulo 1: catálogo de negocio y política de reintento

El Módulo 1 define códigos de negocio por nodo (`ERR-nn` / `EVT-01`) que complementan, nunca reemplazan, las categorías técnicas oficiales `ER-*` (CER-001..010). Doble denominación (ver análisis comparativo C7): los códigos de negocio son de alcance local por nodo; `ER-<CATEGORIA>-<n>` permanece como capa técnica.

#### 11.3.1 Códigos por nodo
| Nodo | Códigos | Motivos / condiciones |
|---|---|---|
| INICIO | ERR-01..ERR-12 | Arranque local, oracle, configuración, BD, lock, identificadores duplicados, fuente descartada. |
| ¿Existe al menos una fuente configurada? | ERR-01 | Aborto por violación de contrato de contexto. |
| ¿Quedan fuentes por procesar...? | ERR-01 | Aborto por violación de contrato de iterador. |
| Seleccionar la siguiente fuente pendiente | ERR-01..03 | Fallas internas de contexto. |
| Entrar a la fuente seleccionada | ERR-01..09 | `fuente_inalcanzable`, `timeout_ingreso`, `autenticacion_rechazada`, `bloqueo_plataforma`, `criterio_no_cumplido`, `error_interno_fuente`, corrupción de contexto. |
| ¿El ingreso fue exitoso? | ERR-01..02 | `entry_result` ausente/corrupto. |
| Aplicar los filtros... | ERR-01..08 | `filtros_no_aplicables`, `fuente_inalcanzable`, `timeout_consulta`, `sesion_expirada`, `respuesta_invalida`, `error_interno_consulta`. |
| ¿Se encontraron ofertas? | ERR-01..02 | `search_result` ausente/corrupto. |
| Capturar ofertas | ERR-01..09 + EVT-01 | `fuente_inalcanzable`, `timeout_captura`, `sesion_expirada`, `bloqueo_plataforma`, `respuesta_invalida`, `error_interno_captura`; `oferta_no_capturada` (EVT-01). |
| Registrar ofertas capturadas | ERR-01..02 | `capture_batch` ausente/corrupto; falla de escritura/transacción. |
| ¿Quedan ofertas por capturar? | ERR-01..02 | `estado_captura` ausente/inválido. |
| ¿Quedan sets de filtros...? | ERR-01..02 | Iteradores inconsistentes. |
| Finalizar Proceso | — | Best-effort; el umbral de obsolescencia protege un lock atascado (ERR-07). |

#### 11.3.2 Catálogo oficial de códigos de negocio
| Código | `codigo_motivo` | Categoría técnica | ¿Reintenta? |
|---|---|---|---|
| ERR-01 | `colision_run_id` | ER-INT | No |
| ERR-02 | `config_ausente` | ER-CFG | No |
| ERR-03 | `config_ilegible` | ER-CFG | No |
| ERR-04 | `config_corrupta` | ER-CFG | No |
| ERR-05 | `bd_indisponible` | ER-DB | No |
| ERR-06 | `concurrencia_activa` | ER-DB | No |
| ERR-07 | `bloqueo_obsoleto` | ER-DB | No |
| ERR-08 | `bloqueo_no_decidible` | ER-DB | No |
| ERR-09 | `contienda_bloqueo` | ER-DB | No |
| ERR-10 | `fallo_estado_interno` | ER-INT | No |
| ERR-11 | `identificadores_duplicados` | ER-CFG | No |
| ERR-12 | `ficha_incompleta` | ER-CFG | No |

Violaciones de contrato en nodos de decisión:
- Contrato de sucesor ausente/corrupto se registra con códigos locales `ERR-01..02` del nodo de decisión.
- Se clasifica como `ER-INT`.
- Aborta la ejecución con estado `error`.

#### 11.3.3 Mapeo de motivos a categoría técnica
| Motivo (`codigo_motivo`) | Categoría técnica | ¿Reintenta? |
|---|---|---|
| `fuente_inalcanzable` | ER-RED / ER-EXT | Sí |
| `timeout_ingreso` | ER-RED | Sí |
| `autenticacion_rechazada` | ER-NAV | No |
| `bloqueo_plataforma` | ER-NAV | No |
| `criterio_no_cumplido` | ER-NAV | No |
| `credenciales_no_disponibles` | ER-CFG | No |
| `error_interno_fuente` | ER-INT | No |
| `filtros_no_aplicables` | ER-EXT | No |
| `timeout_consulta` / `timeout_captura` | ER-RED | Sí |
| `sesion_expirada` | ER-NAV | No |
| `respuesta_invalida` | ER-EXT | No |
| `error_interno_consulta` / `error_interno_captura` | ER-INT | No |
| `oferta_no_capturada` | ER-EXT | No (EVT-01) |

#### 11.3.4 Política de reintento condicional
Solo se reintentan:
- `fuente_inalcanzable`
- `timeout_*` (`timeout_ingreso`, `timeout_consulta`, `timeout_captura`)

Condiciones:
- Reintento con backoff y desde un canal cerrado.
- Límites de reintento por configuración de corrida.
- Todos los demás códigos son inmediatamente no reintentables.
- Producen falla inmediata con registro por nodo, sin reingresar ni continuar según RN-03/RN-06 de la ficha técnica.

| Motivo | ¿Reintenta? | Notas |
|---|---|---|
| `fuente_inalcanzable` | Sí | Con backoff; si se agota → evidencia de falla y continuar con sets/fuentes restantes. |
| `timeout_ingreso`, `timeout_consulta`, `timeout_captura` | Sí | Backoff; si se agota → continuación según política del nodo. |
| Todos los demás | No | Falla inmediata; registro por nodo. |

#### 11.3.5 Clasificación Grupo A / Grupo B
| Grupo | Significado | Motivos aplicables |
|---|---|---|
| A — Compromiso de la fuente | La fuente queda comprometida y no puede continuar en esta corrida; se cierra nodo/fuente o termina la ejecución (aborto). | `autenticacion_rechazada`, `bloqueo_plataforma`, `criterio_no_cumplido`, `sesion_expirada` cuando implica pérdida de credenciales, `error_interno_fuente`, `bloqueo_plataforma` durante captura, códigos de contrato/aborto. |
| B — Propio del set | La falla pertenece al set de filtros actual; se cierra el set y continúa con el siguiente. | `filtros_no_aplicables`, `respuesta_invalida`, `timeout_*` agotado, `error_interno_consulta`, `error_interno_captura`, EVT-01 `oferta_no_capturada`. |

Reglas de cierre:
- Grupo A: se cierra nodo/fuente.
- Grupo B: la corrida continúa con el siguiente set de filtros.
- `credenciales_no_disponibles` no pertenece a A ni B: ocurre antes de entrar a la fuente, durante resolución de credenciales; es falla determinística de configuración (`ER-CFG`) y no se reintenta (RN-03 de “Entrar” v1.1).

#### 11.3.6 Estados de terminación
| Estado | Motivos | Tipo de evento |
|---|---|---|
| `normal` | `corrida_completada`, `sin_fuentes` | suceso |
| `concurrencia` | `concurrencia` (lock sostenido por otra corrida) | suceso |
| `error` | Cualquier aborto: corrupción de contexto, violaciones de contrato, falla fatal no reintentable | error |

Registro:
- Todo evento se registra en “errores o sucesos” con `run_id`, `timestamp`, `tipo`, `codigo`, `evidencia`.
- Si el almacén no está disponible, el log crítico local (Loguru) actúa como fallback (ficha técnica, INICIO §1.11).

---

## 12. Manejo de errores externos

### 12.1 Principios (MEE)
| ID | Principio |
|---|---|
| MEE-001 | Cualquier servicio externo puede fallar en cualquier momento; ningún flujo crítico debe depender de disponibilidad permanente. |
| MEE-002 | Validar toda respuesta externa antes de continuar. |
| MEE-003 | La recuperación debe respetar estrategias y políticas oficiales. |
| MEE-004 | Evitar sobrecarga, bloqueos o incumplimiento de políticas de terceros. |
| MEE-005 | Registrar toda falla externa para auditoría y análisis. |

### 12.2 Tipos y estrategias (EEX)
| ID | Tipo | Ejemplos | Estrategias permitidas |
|---|---|---|---|
| EEX-001 | Plataformas de empleo | Plataforma no disponible; cambios de estructura; captchas; restricciones de acceso; autenticación fallida; información inaccesible. | REC-001, REC-002, REC-003, REC-007, REC-008 |
| EEX-002 | APIs externas | Timeout; respuesta inválida; código de error; servicio no disponible; límite de solicitudes excedido. | REC-001, REC-002, REC-007 |
| EEX-003 | Servicios de LLM | Servicio no disponible; tiempo de respuesta excedido; respuesta inválida; error de autenticación; restricción temporal. | REC-001, REC-002, REC-004, REC-007, REC-009 |
| EEX-004 | Servicios de autenticación | Credenciales inválidas; token expirado; acceso denegado; sesión inválida. | REC-003, REC-007, REC-009 |
| EEX-005 | Servicios de red | DNS no disponible; conectividad interrumpida; latencia alta; timeout; rutas inaccesibles. | REC-001, REC-002, REC-007 |
| EEX-006 | Cambios estructurales | Cambio de HTML; cambio de selectores; nuevos flujos de navegación; eliminación de funcionalidades. | REC-007, REC-008, REC-009 |
| EEX-007 | Restricciones operacionales | Rate limiting; restricción geográfica; restricción temporal; límite de uso alcanzado. | REC-002, REC-007, REC-009 |
| EEX-008 | Mantenimiento de terceros | Ventanas de mantenimiento; actualizaciones; interrupciones temporales. | REC-002, REC-007, REC-008 |

Reglas:
- Todo recurso externo se considera potencialmente no disponible.
- Ninguna respuesta externa se asume válida sin verificación previa.
- Las estrategias respetan políticas oficiales de reintento.
- Minimizar impacto externo en otros módulos.
- Los errores externos nunca comprometen integridad de información ya procesada.
- Toda interacción externa debe ser completamente trazable.
- Incorporar nuevos recursos externos requiere actualización oficial.

---

## 13. Manejo de errores del modelo de lenguaje (LLM)

### 13.1 Principios (MLLM)
| ID | Principio |
|---|---|
| MLLM-001 | Desconfianza por defecto: toda respuesta es potencialmente incorrecta hasta validar. |
| MLLM-002 | Ninguna respuesta puede usarse para decidir o modificar información sin validación previa. |
| MLLM-003 | La automatización no depende exclusivamente del LLM; la información crítica debe ser verificable por reglas adicionales cuando aplique. |
| MLLM-004 | Recuperación solo mediante estrategias oficiales autorizadas. |
| MLLM-005 | Toda interacción con el LLM debe conservar información suficiente para auditoría. |

### 13.2 Tipos oficiales de error (ELLM)
| ID | Tipo | Definición |
|---|---|---|
| ELLM-001 | Respuesta vacía | No devuelve contenido utilizable. |
| ELLM-002 | Respuesta incompleta | Contiene solo parte de la información esperada. |
| ELLM-003 | Respuesta truncada | Termina antes de completar el contenido requerido. |
| ELLM-004 | Formato inválido | No cumple formato requerido: JSON inválido, Markdown incorrecto, campos requeridos ausentes, estructura inesperada. |
| ELLM-005 | Información inconsistente | Contradicciones internas o resultados incompatibles con la información suministrada. |
| ELLM-006 | Interpretación incorrecta | Interpreta mal la información suministrada. |
| ELLM-007 | Incumplimiento de prompt | No sigue instrucciones del prompt. |
| ELLM-008 | Alucinación | Genera información no justificable por datos de entrada o reglas oficiales. |
| ELLM-009 | Tiempo excedido | No responde dentro del tiempo máximo permitido. |
| ELLM-010 | Error de servicio | El servicio devuelve condición de error que impide completar la operación. |

### 13.3 Validaciones obligatorias (VLLM)
| ID | Validación |
|---|---|
| VLLM-001 | Existencia de respuesta. |
| VLLM-002 | Integridad: respuesta completa. |
| VLLM-003 | Formato: estructura esperada. |
| VLLM-004 | Consistencia: sin contradicciones internas. |
| VLLM-005 | Coherencia con la información suministrada. |
| VLLM-006 | Cumplimiento del prompt. |
| VLLM-007 | Cumplimiento de reglas del proyecto: no contradecir reglas funcionales, modelo de decisión, flujo de datos ni estándares oficiales. |

### 13.4 Estrategias permitidas
- REC-001, REC-002, REC-004, REC-007, REC-009.
- La selección depende del tipo de error, severidad y probabilidad de recuperación.

Reglas:
- Ninguna respuesta se usa sin validación previa.
- Registrar toda interacción.
- Respuestas inválidas nunca se almacenan como información oficial.
- Respuestas parcialmente válidas solo si una regla oficial lo autoriza.
- Errores repetitivos se escalan según políticas oficiales.
- Nuevos tipos requieren actualización oficial.
- Ningún componente puede implementar validaciones incompatibles.

---

## 14. Manejo de errores de datos

### 14.1 Principios (MED)
| ID | Principio |
|---|---|
| MED-001 | Preservar integridad lógica y estructural. |
| MED-002 | Mantener consistencia entre componentes. |
| MED-003 | Validar toda información antes de usarla o almacenarla. |
| MED-004 | Hacer trazable toda modificación de datos. |
| MED-005 | Intentar recuperar información afectada antes de descartarla cuando sea técnicamente posible. |

### 14.2 Tipos oficiales de error (EDATA)
| ID | Tipo | Definición / ejemplos |
|---|---|---|
| EDATA-001 | Datos incompletos | Falta información obligatoria para continuar. |
| EDATA-002 | Datos inválidos | Viola reglas de validación: formatos incorrectos, valores fuera de rango, tipos incompatibles. |
| EDATA-003 | Datos duplicados | Múltiples registros representan la misma entidad. |
| EDATA-004 | Datos inconsistentes | Contradicciones internas o incompatibilidad con otros registros. |
| EDATA-005 | Datos desactualizados | Ya no representan el estado actual. |
| EDATA-006 | Relaciones inválidas | Referencias entre entidades que no pueden resolverse. |
| EDATA-007 | Conflictos de actualización | Múltiples operaciones intentan modificar simultáneamente la misma información. |
| EDATA-008 | Corrupción de datos | Alteración que impide uso confiable. |
| EDATA-009 | Pérdida parcial | Desaparición de parte del contenido necesario. |
| EDATA-010 | Error de transformación | Alteración incorrecta durante limpieza, normalización o conversión. |

### 14.3 Validaciones obligatorias (VDAT)
| ID | Validación |
|---|---|
| VDAT-001 | Existencia de información obligatoria. |
| VDAT-002 | Integridad durante todo el procesamiento. |
| VDAT-003 | Consistencia entre campos relacionados. |
| VDAT-004 | Formato oficial. |
| VDAT-005 | Unicidad, cuando aplique. |
| VDAT-006 | Validez de relaciones entre entidades. |
| VDAT-007 | Transiciones de estado conformes al flujo oficial. |
| VDAT-008 | La información almacenada corresponde exactamente a la validada. |

### 14.4 Estrategias permitidas
- REC-003, REC-004, REC-005 cuando esté autorizado.
- REC-006 solo para información no obligatoria.
- REC-007, REC-008, REC-009.
- Selección según naturaleza, impacto y posibilidad de recuperación sin comprometer integridad.

Reglas:
- Ningún dato se almacena sin validación.
- Ningún dato inválido puede alimentar el modelo de decisión.
- Toda modificación conserva trazabilidad.
- Datos corruptos nunca sobrescriben información previamente validada.
- Las recuperaciones preservan integridad de información relacionada.
- Toda pérdida de información se registra como incidente oficial.
- Ningún componente puede implementar validaciones incompatibles.

---

## 15. Notificaciones y alertas

### 15.1 Principios (NAL)
| ID | Principio |
|---|---|
| NAL-001 | Comunicar solo información útil para seguimiento. |
| NAL-002 | Emitir tan pronto ocurre el evento. |
| NAL-003 | Mensaje objetivo, preciso y suficiente. |
| NAL-004 | Evitar duplicados salvo cambio relevante de estado. |
| NAL-005 | Conservar cada comunicación como parte del histórico del incidente. |

El modelo evita tanto la ausencia de información como la emisión excesiva de mensajes.

### 15.2 Clasificación
| Tipo | Definición | Ejemplos |
|---|---|---|
| Notificación | Evento operacional que no requiere atención inmediata. | Inicio de recuperación automática; recuperación exitosa; reintento ejecutado; cierre normal; registro de incidente de baja severidad. |
| Alerta | Condición que requiere atención, seguimiento o intervención por impacto potencial. | Error crítico; recuperación fallida; reintentos agotados; intervención obligatoria; falla repetitiva; corrupción de datos; indisponibilidad prolongada externa. |

### 15.3 Niveles oficiales de alerta (ALT)
| ID | Nivel | Definición |
|---|---|---|
| ALT-001 | Informativa | Evento relevante sin impacto operacional; no requiere acción. |
| ALT-002 | Preventiva | Situación que puede evolucionar a incidente mayor; permite seguimiento preventivo. |
| ALT-003 | Operacional | Afecta parcialmente el funcionamiento; puede requerir supervisión. |
| ALT-004 | Crítica | Compromete procesos importantes o requiere intervención inmediata. |

### 15.4 Eventos que generan comunicación
Notificaciones, como mínimo:
- Inicio de estrategia de recuperación.
- Recuperación exitosa.
- Ejecución de reintento.
- Cambio de estado del incidente.
- Cierre del incidente.
- Recuperación automática exitosa.

Alertas, como mínimo:
- Error SV-1.
- Error SV-2.
- Máximo de reintentos agotado.
- Error no recuperable.
- Escalamiento del incidente.
- Solicitud de intervención de usuario.
- Corrupción de datos.
- Falla repetitiva en el mismo componente.
- Indisponibilidad prolongada de recurso externo.

### 15.5 Destinatarios
- Sistema de auditoría.
- Sistema de logs.
- Componentes internos.
- Usuario.
- Procesos de recuperación.
- Procesos de monitoreo.

La selección depende del tipo de evento y severidad.

### 15.6 Contenido mínimo
Obligatorio:
- Identificador de incidente.
- Fecha y hora.
- Módulo afectado.
- Categoría de error.
- Nivel de severidad.
- Descripción resumida.
- Acción ejecutada.
- Estado actual del incidente.

Opcional, cuando aplique:
- Estrategia aplicada.
- Número de reintentos.
- Recomendaciones para usuario.
- Información adicional de auditoría.

### 15.7 Cierre de alerta
Una alerta solo se cierra si:
- El incidente está resuelto.
- La recuperación terminó correctamente.
- El proceso concluyó controladamente.
- El usuario tomó la decisión requerida, si aplica.

El cierre se registra en el histórico.

Reglas:
- Toda alerta debe estar asociada a incidente registrado.
- Toda notificación debe corresponder a evento verificable.
- No emitir alertas sin condición objetiva.
- Evitar alertas masivas repetitivas sobre el mismo incidente.
- Conservar toda comunicación para auditoría.
- Nuevos tipos requieren actualización oficial.

---

## 16. Escalamiento de errores

El escalamiento transfiere el incidente a niveles superiores cuando las estrategias disponibles son insuficientes.

Se ejecuta solo después de aplicar estrategias autorizadas, salvo que la severidad justifique escalamiento inmediato.

### 16.1 Principios (ESC)
| ID | Principio |
|---|---|
| ESC-001 | Escalar solo al siguiente nivel disponible; prohibido saltos injustificados. |
| ESC-002 | Basar cada escalamiento en evidencia objetiva. |
| ESC-003 | Registrar cada evento de escalamiento en el histórico. |
| ESC-004 | El nivel debe ser proporcional a severidad, impacto y recuperabilidad. |
| ESC-005 | Preservar continuidad de procesos independientes cuando sea posible. |

### 16.2 Niveles oficiales
| Nivel | Tratamiento |
|---|---|
| 1. Recuperación automática | Mecanismos automáticos definidos para el proceso; nivel inicial. |
| 2. Recuperación especializada | Cambio de estrategia, reprocesamiento, reinicio controlado o recuperación alternativa. |
| 3. Escalamiento funcional | Transferencia a otro componente funcional: recuperación, supervisión o validación adicional. |
| 4. Intervención de usuario | Cuando falta información suficiente o la decisión es exclusiva del usuario; suministrar información necesaria. |
| 5. Terminación controlada | Sin estrategia viable; terminar preservando información del tratamiento. |

### 16.3 Condiciones oficiales de escalamiento (CES)
| ID | Condición |
|---|---|
| CES-001 | Estrategias autorizadas agotadas. |
| CES-002 | Máximo de reintentos alcanzado. |
| CES-003 | Error clasificado como no recuperable. |
| CES-004 | La severidad aumenta durante el tratamiento. |
| CES-005 | Riesgo para integridad de información detectado. |
| CES-006 | El modelo de decisión determina que no puede continuar automáticamente. |
| CES-007 | Se requiere decisión reservada exclusivamente al usuario. |

### 16.4 Información mínima de escalamiento
- Identificador de incidente.
- Fecha y hora.
- Nivel de escalamiento.
- Motivo.
- Estrategias ejecutadas previamente.
- Resultado de esas estrategias.
- Estado actual.
- Destinatario del escalamiento.

Reglas:
- Trazabilidad completa.
- Ningún incidente puede permanecer indefinidamente en el mismo nivel.
- El escalamiento nunca elimina información previa.
- La terminación controlada es el último nivel oficial.
- Nuevos niveles requieren actualización oficial.
- Ningún componente puede implementar mecanismos incompatibles.

---

## 17. Trazabilidad y auditoría de errores
Este capítulo complementa DOC-04 — Data Flow y DOC-05 — Project Standards.

### 17.1 Principios (TAE)
| ID | Principio |
|---|---|
| TAE-001 | Histórico continuo desde detección hasta cierre definitivo. |
| TAE-002 | Inmutabilidad del histórico; no borrar ni alterar evidencia original; correcciones como nuevos eventos. |
| TAE-003 | Toda acción debe estar soportada por evidencia verificable. |
| TAE-004 | Información disponible durante el período de retención definido. |
| TAE-005 | Relaciones entre incidentes, procesos, ofertas y componentes permanecen completas. |

### 17.2 Información trazable mínima (TRA)
| ID | Información |
|---|---|
| TRA-001 | Identificación: incidente, error y ejecución. |
| TRA-002 | Contexto: fecha/hora, módulo, proceso, componente y estado del proceso. |
| TRA-003 | Clasificación: categoría, severidad, fuente y recuperabilidad. |
| TRA-004 | Evidencia: información disponible, mensajes, valores y resultados de validación. |
| TRA-005 | Tratamiento: estrategias, reintentos, escalamientos e intervenciones de usuario. |
| TRA-006 | Resultado: estado final, resultado de recuperación, motivo de cierre y fecha de finalización. |

### 17.3 Eventos auditables (AUD)
| ID | Evento |
|---|---|
| AUD-001 | Detección del incidente. |
| AUD-002 | Clasificación del error. |
| AUD-003 | Registro oficial. |
| AUD-004 | Cambio de severidad. |
| AUD-005 | Inicio de recuperación. |
| AUD-006 | Resultado de recuperación. |
| AUD-007 | Cada reintento ejecutado. |
| AUD-008 | Cada escalamiento. |
| AUD-009 | Intervención de usuario. |
| AUD-010 | Cambio de estado del incidente. |
| AUD-011 | Cierre definitivo. |

### 17.4 Relaciones auditables
Cada incidente debe poder relacionarse, cuando aplique, con:
- Oferta afectada.
- Ejecución donde ocurrió.
- Módulo responsable.
- Componente involucrado.
- Proceso correspondiente.
- Decisiones tomadas.
- Estrategias aplicadas.
- Logs asociados.
- Notificaciones emitidas.
- Alertas generadas.

### 17.5 Preservación
- Conservar histórico según políticas oficiales de almacenamiento.
- Borrar, consolidar o archivar solo mediante procedimientos oficialmente documentados.

Reglas:
- Todo incidente debe ser totalmente reconstructible.
- Ninguna acción puede quedar sin registro.
- Cada cambio de estado preserva evidencia.
- Auditoría independiente de tecnología.
- Los mecanismos de auditoría no alteran comportamiento operacional.
- Ningún componente puede implementar reglas incompatibles.

---

## 18. Restricciones de manejo de errores (RME)
Estas restricciones preservan consistencia del modelo, evitan comportamientos no autorizados y aseguran reglas únicas para todos los componentes.

| ID | Restricción |
|---|---|
| RME-001 | Ningún error puede quedar sin detectar si existen mecanismos técnicos razonables para identificarlo. |
| RME-002 | Ningún error detectado puede omitirse del registro oficial. |
| RME-003 | Prohibido borrar registros históricos; toda modificación conserva trazabilidad. |
| RME-004 | Ningún componente puede implementar clasificación propia que contradiga categorías oficiales. |
| RME-005 | La severidad no puede modificarse dinámicamente por criterios subjetivos; requiere evidencia objetiva. |
| RME-006 | Prohibido ejecutar estrategias de recuperación no autorizadas. |
| RME-007 | Prohibido ciclos infinitos de recuperación o reintento; todo proceso debe tener terminación o escalamiento oficial. |
| RME-008 | Ninguna recuperación puede comprometer integridad, consistencia o trazabilidad. |
| RME-009 | Los errores no pueden usarse como mecanismo normal de control de flujo; solo representan condiciones anómalas. |
| RME-010 | Las respuestas del LLM no pueden usarse sin pasar validaciones oficiales. |
| RME-011 | Los errores externos no pueden asumirse permanentes sin ejecutar políticas oficiales autorizadas. |
| RME-012 | Prohibido desactivar validaciones de datos para acelerar procesamiento. |
| RME-013 | Ningún incidente puede permanecer indefinidamente abierto; termina por recuperación, escalamiento o cierre controlado. |
| RME-014 | Prohibido generar notificaciones/alertas sin condición objetiva previamente registrada. |
| RME-015 | Toda acción durante tratamiento debe ser completamente reconstructible. |
| RME-016 | Nuevos tipos de error, estrategias, políticas o mecanismos de auditoría solo por actualización oficial. |
| RME-017 | Ningún módulo puede tener reglas particulares que contradigan este documento. |
| RME-018 | El modelo debe permanecer independiente de lenguaje, herramientas, plataformas o tecnologías. |

Reglas generales:
- Las restricciones son obligatorias para toda implementación.
- Excepciones solo mediante actualización oficial.
- Toda desviación debe documentarse, justificarse y conservar trazabilidad.
- Ningún componente puede operar fuera de estas restricciones.

---

## 19. Criterios de aceptación (CAE)
Todos los criterios son obligatorios.

| ID | Criterio |
|---|---|
| CAE-001 | Existe mecanismo oficial de detección en todos los módulos. |
| CAE-002 | Todo error detectado se clasifica exclusivamente con categorías oficiales. |
| CAE-003 | Todo incidente se registra antes de ejecutar recuperación. |
| CAE-004 | Cada registro contiene la información mínima obligatoria. |
| CAE-005 | Todo error recibe nivel oficial de severidad antes del tratamiento. |
| CAE-006 | Toda recuperación corresponde al catálogo oficial. |
| CAE-007 | Toda política de reintento cumple restricciones oficiales. |
| CAE-008 | Se impiden ciclos infinitos de recuperación o reintento. |
| CAE-009 | Toda interacción externa aplica reglas oficiales de manejo externo. |
| CAE-010 | Toda respuesta del LLM pasa validaciones oficiales antes de usarse. |
| CAE-011 | Toda información usada cumple validaciones oficiales de calidad de datos. |
| CAE-012 | Toda notificación/alerta está asociada a incidente registrado. |
| CAE-013 | Todo escalamiento conserva histórico completo. |
| CAE-014 | La trazabilidad permite reconstruir completamente el ciclo de vida de cualquier incidente. |
| CAE-015 | Toda modificación de incidente preserva evidencia suficiente. |
| CAE-016 | Ningún mecanismo implementado contradice restricciones oficiales. |
| CAE-017 | Todos los módulos usan el modelo oficial. |
| CAE-018 | Las implementaciones son independientes de lenguaje, plataforma o tecnología. |
| CAE-019 | Pruebas funcionales demuestran que cada estrategia oficial puede ejecutarse correctamente cuando aplique. |
| CAE-020 | Pruebas de integración verifican que el manejo de errores preserva integridad del flujo de datos y consistencia durante todo el ciclo del incidente. |

Validación de cumplimiento:
- Todos los criterios verificados satisfactoriamente.
- Sin incumplimientos de reglas oficiales.
- Evidencia disponible para auditoría.
- Documentación de implementación consistente con este documento.

---

## 20. Índice de prefijos
Punto único de consulta para implementación y mantenimiento.

| Prefijo | Dominio |
|---|---|
| PME | Principios de manejo de errores |
| AME | Arquitectura de manejo de errores |
| CE | Criterios de clasificación |
| CER | Categorías oficiales de error |
| ER | Identificador oficial de error |
| FDE | Fuentes de error |
| PDE | Principios de detección |
| MDE | Mecanismos de detección |
| RER | Registro oficial de errores |
| NSE | Criterios de evaluación de severidad |
| SV | Niveles oficiales de severidad |
| RSE | Reglas de asignación de severidad |
| PRE | Principios de recuperación |
| REC | Estrategias oficiales de recuperación |
| SRE | Criterios de selección de estrategia |
| PRT | Principios de reintentos |
| POL-RET | Políticas oficiales de reintentos |
| MEE | Principios de manejo externo |
| EEX | Tipos oficiales de errores externos |
| MLLM | Principios del modelo de lenguaje |
| ELLM | Tipos oficiales de errores del LLM |
| VLLM | Validaciones oficiales del LLM |
| MED | Principios de datos |
| EDATA | Tipos oficiales de errores de datos |
| VDAT | Validaciones oficiales de datos |
| NAL | Principios de notificaciones y alertas |
| ALT | Niveles oficiales de alerta |
| ESC | Principios de escalamiento |
| CES | Condiciones oficiales de escalamiento |
| TAE | Principios de trazabilidad y auditoría |
| TRA | Información trazable |
| AUD | Eventos auditables |
| RME | Restricciones de manejo de errores |
| CAE | Criterios de aceptación |
| ERR / EVT | Códigos de negocio por nodo del Módulo 1; complementan, no reemplazan, `ER-*` |
