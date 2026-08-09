# Documento 12 – Arquitectura General del Sistema (Optimizado)

---

## 1. Propósito y Alcance

Define la **arquitectura general oficial** de la automatización de búsqueda laboral: organización estructural del sistema, módulos, componentes, capas, servicios, mecanismos de integración y principios arquitectónicos.

**Función:** referencia oficial para diseño e implementación. Toda solución del proyecto debe respetar esta arquitectura, preservando consistencia, modularidad, mantenibilidad y escalabilidad.

**Coherencia obligatoria:** las decisiones arquitectónicas deben alinearse con los Documentos 0–11 (glosario, requisitos funcionales/no funcionales, modelo de decisión, flujo de datos, estándares, manejo de errores, arquitectura de carpetas, decisiones estratégicas, investigación y stack tecnológico aprobado).

**Base para:** Documento 13 (Modelo de Datos) y todas las fases posteriores. Provee una estructura técnica uniforme para implementar los módulos.

**Control de cambios:** toda modificación debe documentarse, justificarse y aprobarse formalmente antes de incorporarse, preservando trazabilidad, compatibilidad documental y evolución controlada.

---

## 2. Objetivos Arquitectónicos (OA)

Criterios guía obligatorios durante diseño, implementación, mantenimiento y evolución. Toda decisión debe contribuir a uno o más.

| ID | Objetivo | Definición |
|---|---|---|
| OA-001 | Modularidad | Organizar en módulos con responsabilidades específicas y límites funcionales definidos |
| OA-002 | Separación de responsabilidades | Cada componente cumple una única responsabilidad identificable; sin mezclar procesos de negocio distintos |
| OA-003 | Bajo acoplamiento | Minimizar dependencias entre módulos para evolución independiente |
| OA-004 | Alta cohesión | Los elementos de un módulo se relacionan estrechamente con su responsabilidad |
| OA-005 | Escalabilidad | Incorporar módulos, funcionalidades y fuentes sin rediseño significativo |
| OA-006 | Mantenibilidad | Facilitar comprensión, actualización, corrección y mejora continua |
| OA-007 | Reusabilidad | Componentes reutilizables por distintos módulos cuando corresponda |
| OA-008 | Extensibilidad | Añadir capacidades agregando componentes, evitando modificar los existentes |
| OA-009 | Consistencia | Todos los módulos siguen organización uniforme y respetan los principios de este documento |
| OA-010 | Trazabilidad | Seguimiento completo de información, decisiones y procesos entre componentes |
| OA-011 | Observabilidad | Monitoreo mediante logs, métricas y mecanismos de diagnóstico |
| OA-012 | Robustez | Minimizar impacto de errores individuales; una falla no compromete el sistema completo |
| OA-013 | Testeabilidad | Validación y verificación de componentes aislados y del sistema completo |
| OA-014 | Configurabilidad | Comportamiento ajustable mediante configuraciones controladas, sin modificar código |
| OA-015 | Compatibilidad tecnológica | Total compatibilidad con el stack oficial del Documento 11 |
| OA-016 | Independencia tecnológica | Minimizar dependencias innecesarias de tecnologías, plataformas o proveedores específicos |
| OA-017 | Evolución controlada | Facilitar cambios futuros preservando estabilidad y coherencia |
| OA-018 | Compatibilidad documental | Alineación con requisitos, estándares, modelos y restricciones de los Documentos 0–11 |
| OA-019 | Simplicidad | Evitar complejidad innecesaria; soluciones claras y proporcionadas a las necesidades reales |
| OA-020 | Sostenibilidad arquitectónica | Favorecer mantenimiento y evolución a largo plazo, preservando la calidad |

---

## 3. Principios Arquitectónicos (PA)

Reglas oficiales de diseño, obligatorias en definición, implementación, mantenimiento y evolución. Toda decisión debe justificar su conformidad.

| ID | Principio | Definición |
|---|---|---|
| PA-001 | Arquitectura modular | Módulos delimitados con responsabilidades específicas y límites funcionales definidos |
| PA-002 | Responsabilidad única | Cada módulo/componente/servicio cumple una responsabilidad principal; sin concentrar funciones de procesos distintos |
| PA-003 | Separación por capas | Separación clara entre capas; sin dependencias impropias entre ellas |
| PA-004 | Bajo acoplamiento | Minimizar dependencias para independencia funcional y evolución |
| PA-005 | Alta cohesión | Elementos de un componente estrechamente relacionados con su responsabilidad |
| PA-006 | Comunicación por interfaces definidas | Interacción entre módulos solo por interfaces claras; sin dependencias implícitas ni acceso a implementaciones internas |
| PA-007 | Centralización de servicios compartidos | Funcionalidades reutilizables como servicios compartidos; sin duplicar lógica |
| PA-008 | Configuración desacoplada | Configuración separada del código; comportamiento modificable por mecanismos controlados |
| PA-009 | Flujo de dependencias controlado | Dependencias con dirección arquitectónica definida; sin dependencias circulares |
| PA-010 | Independencia entre módulos | Módulos capaces de evolucionar, mantenerse y probarse independientemente |
| PA-011 | Tolerancia a fallos | Aislar errores para reducir propagación e impacto global |
| PA-012 | Observabilidad integrada | Componentes facilitan registro de eventos, métricas y evidencia para monitoreo, diagnóstico y auditoría |
| PA-013 | Escalabilidad por composición | Nuevas capacidades agregando componentes, evitando modificar la estructura existente |
| PA-014 | Extensibilidad | Extender funcionalidad sin alterar innecesariamente módulos implementados |
| PA-015 | Consistencia estructural | Organización homogénea respetando convenciones oficiales |
| PA-016 | Reutilización de componentes | Componentes reutilizables por distintos procesos/módulos cuando sea viable |
| PA-017 | Evolución incremental | Incorporación progresiva de mejoras sin comprometer estabilidad ni compatibilidad |
| PA-018 | Compatibilidad tecnológica | Alineación con el stack oficial del Documento 11 |
| PA-019 | Trazabilidad arquitectónica | Identificación clara del flujo de información, responsabilidades y relaciones entre componentes |
| PA-020 | Simplicidad de diseño | Evitar complejidad innecesaria; soluciones claras y proporcionadas |

---

## 4. Vista General de la Arquitectura

Organizada en **tres niveles complementarios** que separan lógica de negocio, servicios compartidos e infraestructura.

### 4.1 Nivel Funcional
Procesos principales (núcleo de negocio). Módulos:
- Descubrimiento de oportunidades.
- Preparación inicial de ofertas.
- Evaluación inicial.
- Procesamiento de ofertas.
- Gestión de resultados.

Cada módulo tiene responsabilidades definidas y se comunica solo por los mecanismos de la arquitectura. **No** implementa servicios transversales ni accede directamente a infraestructura: usa los componentes compartidos.

### 4.2 Nivel de Servicios Transversales
Servicios reutilizables que proveen capacidades comunes. Incluyen: gestión de configuración, motor de decisión, IA, persistencia, logging/auditoría, observabilidad, seguridad, manejo de errores, servicios compartidos de soporte.

Diseñados como componentes independientes y desacoplados de los módulos funcionales. **Ningún módulo reimplementa** funcionalidades ya disponibles en estos servicios.

### 4.3 Nivel de Infraestructura
Recursos tecnológicos externos: plataforma de búsqueda, navegador automatizado, modelos de IA, base de datos, sistema de archivos, servicios externos autorizados.

Aislada de la lógica de negocio mediante mecanismos de abstracción para reducir dependencias tecnológicas y facilitar evolución.

### 4.4 Relación entre Niveles
Separación estricta entre los tres niveles:
- Módulos funcionales usan exclusivamente los servicios transversales necesarios.
- Servicios transversales son los únicos responsables de interactuar con infraestructura cuando aplica.

Resultado: arquitectura modular, reutilizable, mantenible y escalable; menor impacto de cambios tecnológicos en la lógica de negocio; incorporación facilitada de nuevas capacidades.

---

## 5. Componentes Principales (CMP)

Unidades arquitectónicas con responsabilidades definidas, independencia funcional, interfaces explícitas y compatibilidad con los principios.

| ID | Componente | Responsabilidad |
|---|---|---|
| CMP-001 | Descubrimiento de oportunidades | Localizar, recolectar y registrar nuevas oportunidades desde las fuentes oficiales |
| CMP-002 | Preparación inicial de ofertas | Normalizar, estructurar y preparar la información del descubrimiento para evaluación |
| CMP-003 | Evaluación inicial | Análisis preliminar aplicando los criterios de evaluación del proyecto |
| CMP-004 | Procesamiento de ofertas | Análisis detallado de oportunidades aprobadas en evaluación inicial; integra información para la decisión del usuario |
| CMP-005 | Gestión de resultados | Consolidar, almacenar y presentar el resultado final del procesamiento |
| CMP-006 | Motor de decisión | Ejecuta el modelo de decisión oficial y determina el comportamiento según las reglas aprobadas |
| CMP-007 | Motor de automatización web | Controla interacción automatizada con plataformas: navegación, extracción, acciones autorizadas |
| CMP-008 | Motor de IA | Coordina modelos de IA; provee análisis, clasificación, generación y procesamiento de información |
| CMP-009 | Persistencia | Gestiona almacenamiento, recuperación y actualización de información |
| CMP-010 | Gestión de configuración | Administra parámetros que controlan el comportamiento del sistema |
| CMP-011 | Observabilidad | Recolecta logs, métricas y evidencia para monitoreo, diagnóstico y auditoría |
| CMP-012 | Seguridad | Protege información, controla acceso a recursos y preserva integridad |
| CMP-013 | Manejo de errores | Detecta, clasifica, registra y coordina el tratamiento de errores según el modelo oficial |
| CMP-014 | Servicios compartidos | Provee funcionalidades reutilizables sin duplicar lógica de implementación |

### 5.1 Estructura Interna de CMP-001
Organizada en elementos derivados uno a uno en el paquete `modules/discovery/`:

- **`run_context.py`:** mantiene el contexto de la ejecución actual (Run): identificador, snapshot de configuración, sesión activa y estado acumulado.
- **Nodos de descubrimiento:** los trece nodos del flujo oficial de Discovery definidos en el MVP Execution Plan (Fase 4) y modelados en DOC-04 (Sección 15). Cada nodo es responsable de una etapa y se comunica con los siguientes exclusivamente por los contratos de la hoja técnica.
- **`adapters/`:** adaptadores de plataforma que implementan la interfaz **INT-001** y usan la integración **INT-003** para interactuar con cada fuente oficial.

**Uso de servicios transversales por CMP-001:**

| Elemento interno | Servicios compartidos de los que depende |
|---|---|
| Run manager | SRV-004 (Persistencia), SRV-005 (Configuración) |
| Lock manager | SRV-004 (Persistencia) |
| Adaptadores de plataforma | SRV-003 (Automatización web), SRV-006 (Logging) |

- **Run manager:** orquesta la ejecución del flujo oficial de Discovery.
- **Lock manager:** garantiza mediante el lock store que no haya más de una ejecución en curso concurrente por fuente.
- **Credenciales oficiales** usadas por los adaptadores deben almacenarse en el repositorio seguro del servicio de Gestión de Configuración (SRV-005), accedidas exclusivamente por sus interfaces públicas y **nunca** persistidas en base de datos de aplicación, logs ni registros de ejecución (ver Sección 14, Credenciales y secretos).

### 5.2 Principios de Organización de Componentes
Todos los componentes deben: responsabilidades claramente definidas; comunicación solo por mecanismos de la arquitectura; evitar dependencias innecesarias; favorecer reutilización; permitir evolución independiente cuando sea técnicamente viable; compatibilidad con el stack oficial y demás documentación del proyecto.

---

## 6. Organización por Módulos

Organización en módulos independientes con responsabilidades definidas para reducir acoplamiento, favorecer reutilización y permitir incorporar capacidades sin afectar estabilidad.

### 6.1 Módulos de Negocio
Implementan el flujo funcional principal (gestión de oportunidades): descubrimiento, preparación inicial, evaluación inicial, procesamiento, gestión de resultados. Cada uno ejecuta solo las responsabilidades de su proceso de negocio.

### 6.2 Módulos de Plataforma
Capacidades técnicas reutilizables para soportar procesos de negocio: motor de decisión, motor de automatización web, motor de IA, persistencia. Ofrecen servicios reutilizables **sin** incorporar lógica de procesos de negocio específicos.

### 6.3 Módulos de Infraestructura
Capacidades para operación, administración y supervisión: gestión de configuración, observabilidad, seguridad, manejo de errores, servicios compartidos. Desacoplados de la lógica funcional; proveen servicios comunes.

### 6.4 Relaciones entre Módulos
Reglas de interacción:
- Cada módulo mantiene responsabilidad claramente definida.
- Módulos de negocio pueden usar servicios de módulos de plataforma e infraestructura.
- Módulos de plataforma **no** deben depender de procesos de negocio específicos.
- Módulos de infraestructura **no** deben incorporar lógica funcional de negocio.
- Toda comunicación por los mecanismos definidos por la arquitectura.

### 6.5 Evolución Modular
Nuevos módulos preservan la organización de este capítulo. Se clasifican dentro de un grupo existente o, si es estrictamente necesario, se crea un nuevo grupo formalmente justificado sin afectar la coherencia global.

---

## 7. Arquitectura por Capas

Todos los módulos mantienen organización interna uniforme basada en **capas funcionales** (comportamiento de negocio) y **capas técnicas** (operación sin lógica de negocio). Obligatoria para todos los módulos del proyecto.

### 7.1 Capas Funcionales

| Capa | Responsabilidad | Restricción |
|---|---|---|
| Interfaz | Recibir solicitudes, entregar resultados; punto de entrada/salida del módulo | No implementa lógica de negocio |
| Orquestación | Coordinar el flujo de ejecución interno; organizar secuencia de operaciones y delegar a servicios | — |
| Servicio | Implementar lógica funcional mediante servicios especializados | Cada servicio con responsabilidad definida |
| Dominio | Reglas de negocio, entidades conceptuales y modelos propios del módulo | Independiente de tecnología e infraestructura |

### 7.2 Capas Técnicas

| Capa | Responsabilidad |
|---|---|
| Integraciones | Comunicación con otros módulos, servicios internos y recursos externos autorizados |
| Persistencia | Almacenar, recuperar y actualizar información requerida por el módulo |
| Configuración | Administrar parámetros específicos del módulo |
| Observabilidad | Generar logs, métricas y evidencia para monitoreo y diagnóstico |
| Manejo de errores | Detectar, clasificar, registrar y gestionar errores según el modelo oficial |

### 7.3 Dependencias entre Capas
Reglas:
- Cada capa cumple una única responsabilidad definida.
- Capas funcionales **no** dependen directamente de tecnologías específicas.
- Capas técnicas **no** contienen reglas de negocio.
- Comunicación entre capas por interfaces claramente definidas.
- Evitar dependencias circulares entre capas.

### 7.4 Uniformidad Arquitectónica
Todos los módulos implementan la misma organización por capas. Solo pueden omitirse capas cuya responsabilidad no sea necesaria para un módulo específico, si la omisión no afecta la coherencia general. Nuevas capas requieren justificación formal y compatibilidad con los principios.

---

## 8. Flujo General de Interacción entre Módulos

Interacción controlada, explícita y consistente con los principios, para garantizar arquitectura desacoplada, mantenible y preparada para evolucionar.

### 8.1 Flujo de Ejecución General
Secuencia funcional principal:
1. Descubrimiento de oportunidades.
2. Preparación inicial de ofertas.
3. Evaluación inicial.
4. Procesamiento de ofertas.
5. Gestión de resultados.

Cada módulo es exclusivamente responsable de su etapa.

### 8.2 Uso de Servicios Transversales
Los módulos funcionales pueden usar servicios de plataforma e infraestructura cuando sea necesario. Su uso no altera el flujo funcional principal.

### 8.3 Reglas Oficiales de Comunicación (RCM)

| ID | Regla | Definición |
|---|---|---|
| RCM-001 | Comunicación por interfaces públicas | Interacción entre módulos exclusivamente por interfaces oficiales |
| RCM-002 | Prohibición de acceso interno | Ningún módulo accede directamente a componentes internos de otro |
| RCM-003 | Dependencias unidireccionales | Dependencias en una sola dirección; prohibidas las circulares |
| RCM-004 | Uso de servicios compartidos | Funcionalidad reutilizable se obtiene de servicios compartidos; sin duplicar lógica existente |
| RCM-005 | Independencia funcional | Módulos funcionales no dependen del funcionamiento interno de los servicios técnicos que usan |
| RCM-006 | Comunicación explícita | Toda interacción definida, documentada y controlada; sin dependencias implícitas |
| RCM-007 | Aislamiento de errores | Cada módulo gestiona sus propios errores antes de propagar resultados |
| RCM-008 | Respeto al flujo oficial | Interacciones respetan el flujo oficial; excepciones solo si las reglas del proyecto las autorizan expresamente |

### 8.4 Principios de Interacción
Comunicaciones deben permanentemente: bajo acoplamiento; favorecer reutilización; preservar independencia funcional; facilitar trazabilidad; minimizar impacto de cambios arquitectónicos; coherencia con el modelo de decisión y flujo de datos oficiales.

---

## 9. Servicios Compartidos (SRV)

Capacidades reutilizables usadas por múltiples módulos sin duplicar lógica. Centralizan funcionalidades comunes, mantienen consistencia y reducen acoplamiento. Cada servicio: responsabilidad definida, interfaz pública de uso, compatibilidad con los principios.

### 9.1 Servicios de Dominio

| ID | Servicio | Propósito | Responsabilidad |
|---|---|---|---|
| SRV-001 | Motor de decisión | Ejecutar el modelo de decisión oficial | Aplicar reglas de decisión aprobadas para determinar el comportamiento |
| SRV-002 | Motor de IA | Proveer análisis, clasificación, generación y procesamiento vía modelos de IA | Centralizar toda interacción con los modelos de IA |
| SRV-003 | Motor de automatización web | Gestionar interacción automatizada con plataformas | Controlar navegación, extracción y acciones autorizadas |

### 9.2 Servicios de Infraestructura

| ID | Servicio | Propósito | Responsabilidad |
|---|---|---|---|
| SRV-004 | Persistencia | Gestionar almacenamiento y recuperación de información | Garantizar disponibilidad e integridad de datos |
| SRV-005 | Gestión de configuración | Gestionar parámetros del sistema | Ajustar comportamiento sin modificar implementación |
| SRV-006 | Logging y auditoría | Centralizar generación de logs y evidencia | Facilitar trazabilidad, auditoría y diagnóstico |
| SRV-007 | Observabilidad | Proveer métricas, indicadores y monitoreo | Facilitar supervisión continua del comportamiento |
| SRV-008 | Seguridad | Proteger información y controlar acceso | Implementar mecanismos de protección definidos |
| SRV-009 | Manejo de errores | Gestionar centralmente errores y excepciones | Aplicar el modelo oficial de manejo de errores |
| SRV-010 | Gestión de sistema de archivos | Gestionar acceso a recursos en el sistema de archivos | Centralizar lectura, escritura y organización de archivos |

**Almacenamiento de credenciales (SRV-005):** credenciales y secretos de integraciones se almacenan en un repositorio seguro gestionado por este servicio. En el MVP, el repositorio es un archivo de variables de entorno (`.env`) cargado exclusivamente por un cargador de entorno oficial; sus valores se referencian en la configuración del sistema sin incrustarse en ella. Las credenciales **nunca** se incluyen en archivos bajo control de versiones, base de datos de aplicación, logs ni registros de ejecución.

### 9.3 Reglas Generales de Servicios Compartidos
Todos los servicios deben: responsabilidad única definida; reutilizables por múltiples módulos; exponer solo interfaces públicas documentadas; desacoplados de procesos de negocio específicos cuando aplique; sin dependencias circulares; compatibilidad con el stack oficial; facilitar evolución independiente de su implementación.

---

## 10. Arquitectura de Integración con Sistemas Externos

Separación estricta entre componentes internos y recursos externos. Toda integración mediante mecanismos de abstracción que aíslen la lógica de negocio de las particularidades tecnológicas. **Ningún módulo funcional se comunica directamente** con un sistema externo.

### 10.1 Modelo de Integración
Toda integración se implementa mediante un **adaptador arquitectónico** responsable de:
- Recibir solicitudes de módulos internos.
- Validar la información intercambiada.
- Traducir datos al formato requerido por el sistema externo.
- Normalizar respuestas recibidas.
- Gestionar errores de comunicación.
- Registrar eventos relevantes de integración.
- Aislar cambios producidos por modificaciones en el sistema externo.

Aplicado uniformemente a todas las integraciones del proyecto.

### 10.2 Catálogo Oficial de Integraciones (INT)

| ID | Integración | Propósito | Responsabilidad |
|---|---|---|---|
| INT-001 | Plataforma de búsqueda laboral | Acceso a oportunidades publicadas en la plataforma objetivo | Obtener información y ejecutar acciones autorizadas durante la automatización |
| INT-002 | Proveedor de modelos de IA | Acceso a los modelos de IA usados | Ejecutar solicitudes del Motor de IA sin exponer detalles de implementación a los consumidores |
| INT-003 | Navegador automatizado | Entorno de ejecución para automatizar interacción con plataformas web | Navegación automatizada y ejecución controlada de acciones según políticas del proyecto |

### 10.3 Reglas Generales de Integración
Toda integración debe: interfaces claramente definidas; desacoplada de lógica de negocio; centralizar gestión de errores de comunicación; normalizar información intercambiada; facilitar sustitución del recurso externo; registrar eventos para auditoría y diagnóstico; compatibilidad con los principios.

### 10.4 Recursos Tecnológicos Internos
Recursos usados exclusivamente por la arquitectura interna (base de datos, sistema de archivos) **no** forman parte del catálogo de integración externa. Su uso se realiza mediante los servicios compartidos correspondientes y se documenta en los capítulos específicos de persistencia e infraestructura.

---

## 11. Arquitectura de Persistencia

Principios y reglas para gestionar toda la información durante el ciclo de vida, preservando integridad, trazabilidad y disponibilidad. La implementación es responsabilidad del servicio compartido de Persistencia (SRV-004); este capítulo establece las reglas de organización.

### 11.1 Organización de la Información

| Categoría | Definición | Ejemplos |
|---|---|---|
| Operacional | Generada durante la ejecución normal | Oportunidades descubiertas, información preparada, resultados de evaluación, información procesada, estados de ejecución |
| Configuración | Parámetros que determinan el comportamiento | Parámetros generales, configuración de módulos, umbrales, variables de operación, preferencias del sistema |
| Evidencia operacional | Monitoreo, auditoría y diagnóstico | Logs de eventos, errores, auditorías, métricas, evidencia de ejecución |
| Recursos documentales | Documentos usados por la automatización | Currículum, portafolio, plantillas, documentación oficial del proyecto |

### 11.2 Reglas Oficiales de Persistencia (RP)

| ID | Regla | Definición |
|---|---|---|
| RP-001 | Organización por tipo | Toda información persistida se clasifica según las categorías de este capítulo |
| RP-002 | Acceso por servicio de Persistencia | Módulos acceden a información persistida solo vía SRV-004 |
| RP-003 | Prohibición de acceso directo | Ningún módulo funcional interactúa directamente con mecanismos físicos de almacenamiento |
| RP-004 | Integridad | Preservar consistencia e integridad en todas las operaciones de almacenamiento y recuperación |
| RP-005 | Trazabilidad | Toda modificación relevante es identificable y trazable según políticas del proyecto |
| RP-006 | Desacoplamiento de negocio | Reglas de persistencia independientes de la lógica funcional |
| RP-007 | Compatibilidad con el modelo de datos | Organización alineada con el Modelo de Datos oficial |
| RP-008 | Evolución controlada | Nuevos tipos de información o mecanismos de almacenamiento preservan compatibilidad |

### 11.3 Principios de Persistencia
Garantizar: separación clara entre lógica de negocio y almacenamiento; organización consistente; trazabilidad; reutilización del servicio de Persistencia por todos los módulos; compatibilidad con el stack oficial; preparación para evolución futura.

---

## 12. Arquitectura de Inteligencia Artificial

Reglas que gobiernan el uso de modelos de IA: uso consistente, controlado y desacoplado de la lógica de negocio. El uso es responsabilidad exclusiva del Motor de IA (SRV-002); este capítulo establece las reglas.

### 12.1 Rol de la IA
Mecanismo especializado de procesamiento de información. Ejecuta análisis, extracción, clasificación, transformación y generación de contenido cuando los procesos de negocio lo requieren. **No** controla el flujo de ejecución ni implementa reglas de negocio.

### 12.2 Responsabilidades Autorizadas
Extracción estructurada de información; clasificación de contenido; resumen; análisis de texto; generación de contenido cuando el proceso lo requiera; transformación de información entre formatos compatibles. Todo uso alineado con las responsabilidades oficiales de cada módulo.

### 12.3 Responsabilidades No Autorizadas
La IA **no debe:** implementar reglas de negocio; reemplazar al Motor de Decisión (SRV-001); controlar el flujo de ejecución; modificar directamente información persistida; alterar configuraciones; ejecutar acciones fuera del alcance autorizado.

### 12.4 Reglas Oficiales de Uso de IA (RAI)

| ID | Regla | Definición |
|---|---|---|
| RAI-001 | Acceso por servicio oficial | Todo uso de modelos de IA exclusivamente vía SRV-002 |
| RAI-002 | Separación de responsabilidades | IA solo procesa información; decisiones funcionales a cargo de SRV-001 |
| RAI-003 | Independencia de negocio | Modelos de IA no contienen conocimiento específico de reglas de negocio |
| RAI-004 | Gestión centralizada de instrucciones | Instrucciones para interactuar con modelos gestionadas centralmente para evolución controlada |
| RAI-005 | Validación de entrada | Toda información enviada a modelos se valida previamente |
| RAI-006 | Normalización de respuesta | Respuestas transformadas a formatos compatibles antes de ser usadas por otros módulos |
| RAI-007 | Trazabilidad | Toda interacción con modelos registrable y auditable cuando aplique |
| RAI-008 | Manejo uniforme de errores | Errores de IA gestionados por los mecanismos oficiales |
| RAI-009 | Independencia de proveedor | Minimizar dependencias de un proveedor o modelo específico; facilitar reemplazo |
| RAI-010 | Evolución controlada | Nuevos modelos, capacidades o estrategias preservan compatibilidad con la arquitectura |

### 12.5 Principios de IA
Garantizar: separación entre procesamiento inteligente y lógica de negocio; uso consistente; independencia de proveedor; trazabilidad de solicitudes; compatibilidad con el Motor de Decisión; evolución controlada.

---

## 13. Gestión de Configuración

Reglas para administrar todos los parámetros, permitiendo ajustar comportamiento de forma controlada y mantenible sin modificar componentes. Responsabilidad exclusiva del servicio de Gestión de Configuración (SRV-005).

### 13.1 Organización de la Configuración

| Alcance | Definición | Ejemplos |
|---|---|---|
| Global | Afecta la operación general | Parámetros generales, configuración de entorno de ejecución, directorios principales, opciones globales |
| Por módulo | Parámetros específicos de cada módulo | Parámetros de Descubrimiento, Preparación Inicial, Evaluación Inicial, Procesamiento, Gestión de Resultados |
| Integración | Interacción con recursos externos | Navegador automatizado, plataforma objetivo, proveedor de IA |
| Operacional | Servicios técnicos de la arquitectura | Observabilidad, logging/auditoría, persistencia, seguridad, manejo de errores |

### 13.2 Reglas Oficiales de Configuración (RCF)

| ID | Regla | Definición |
|---|---|---|
| RCF-001 | Configuración centralizada | Toda configuración gestionada vía SRV-005 |
| RCF-002 | Prohibición de configuración incrustada | Parámetros configurables no codificados directamente en la implementación |
| RCF-003 | Validación | Toda configuración se valida antes de ser usada |
| RCF-004 | Acceso por servicio oficial | Módulos acceden a configuración solo por interfaces públicas de SRV-005 |
| RCF-005 | Versionado | Modificaciones relevantes identificables y controlables según estrategia del proyecto |
| RCF-006 | Separación configuración–datos | Configuración separada de la información operacional de persistencia |
| RCF-007 | Reutilización | Parámetros comunes centralizados; sin duplicación; comportamiento uniforme |
| RCF-008 | Evolución controlada | Nuevos parámetros preservan compatibilidad y alineación documental |

### 13.3 Restricciones de Configuración
La configuración **no debe:** implementar reglas de negocio; controlar el flujo funcional; reemplazar responsabilidades del Motor de Decisión; contener lógica de procesamiento; modificar la estructura arquitectónica. Su propósito es exclusivamente parametrizar el comportamiento de componentes ya definidos.

### 13.4 Principios de Configuración
Garantizar: centralización; separación configuración–lógica de negocio; consistencia entre módulos; facilidad de mantenimiento; trazabilidad de cambios; compatibilidad con el stack; evolución controlada.

---

## 14. Arquitectura de Seguridad

Reglas para proteger información, componentes y recursos, preservando confidencialidad, integridad y disponibilidad. La seguridad es parte del diseño arquitectónico, no solo de la implementación tecnológica. Capacidades provistas por Seguridad (SRV-008).

### 14.1 Activos Protegidos
Mínimo:
- **Información:** datos operacionales, configuraciones, documentos, resultados de procesamiento.
- **Configuración:** parámetros que controlan comportamiento del sistema y módulos.
- **Credenciales y secretos:** información de autenticación, autorización o acceso a recursos protegidos.
- **Integraciones externas:** comunicaciones con recursos externos autorizados.
- **Ejecución del sistema:** operación normal de módulos, servicios y procesos.

### 14.2 Clasificación de Sensibilidad de la Información

| Nivel | Definición |
|---|---|
| Público | Su divulgación no representa riesgo para el proyecto |
| Interno | Exclusivo para la operación interna de la automatización |
| Confidencial | Información personal, operacional o estratégica cuya divulgación no autorizada puede afectar la operación o privacidad del usuario |
| Secreto | Acceso restringido al máximo nivel permitido. Incluye: credenciales, tokens, claves de acceso, secretos de integraciones |

### 14.3 Reglas Oficiales de Seguridad (RSA)

| ID | Regla | Definición |
|---|---|---|
| RSA-001 | Menor privilegio | Cada componente accede solo a recursos estrictamente necesarios |
| RSA-002 | Validación obligatoria de entrada | Toda información recibida se valida antes de procesarse |
| RSA-003 | Protección de credenciales | Credenciales y secretos no almacenados ni expuestos fuera de mecanismos autorizados |
| RSA-004 | Gestión segura de secretos | Secretos gestionados mediante mecanismos centralizados y controlados |
| RSA-005 | Aislamiento de información sensible | Información confidencial o secreta aislada cuando sea necesario |
| RSA-006 | Auditoría de acciones críticas | Toda operación crítica de seguridad registrable y auditable |
| RSA-007 | Protección de integraciones externas | Comunicación con recursos externos solo por mecanismos de integración definidos |
| RSA-008 | Integridad de información | Preservar integridad durante todo el ciclo de vida |
| RSA-009 | Recuperación controlada | Incidentes de seguridad gestionados controladamente para minimizar impacto |
| RSA-010 | Evolución controlada | Nuevos mecanismos de seguridad preservan compatibilidad |

### 14.4 Principios de Seguridad
Garantizar: protección proporcional a la sensibilidad; separación lógica de negocio–mecanismos de seguridad; protección de credenciales y secretos; integridad; trazabilidad de acciones críticas; compatibilidad con el stack; evolución controlada.

---

## 15. Arquitectura de Observabilidad

Reglas para monitorear, entender y diagnosticar el comportamiento durante todo el ciclo de ejecución. Provee información para evaluar operación, detectar anomalías, diagnosticar incidentes y soportar evolución. Capacidades provistas por Observabilidad (SRV-007).

### 15.1 Organización de la Observabilidad

| Categoría | Definición | Ejemplos |
|---|---|---|
| Evidencia operacional | Eventos durante la ejecución | Inicio/fin de procesos, cambios de estado, eventos relevantes, advertencias, errores |
| Métricas operacionales | Indicadores para evaluar comportamiento | Tiempo de ejecución, oportunidades procesadas, tiempo de respuesta de integraciones, uso de servicios compartidos, solicitudes a IA |
| Trazabilidad de procesos | Reconstruir el camino completo de una operación | Flujo seguido, componentes involucrados, servicios usados, integraciones invocadas, decisiones ejecutadas |

### 15.2 Reglas Oficiales de Observabilidad (ROA)

| ID | Regla | Definición |
|---|---|---|
| ROA-001 | Registro uniforme de eventos | Componentes generan eventos en formato consistente definido por la arquitectura |
| ROA-002 | Generación de métricas | Componentes producen métricas para evaluar comportamiento y desempeño |
| ROA-003 | Trazabilidad de procesos | Reconstruir el camino completo de operaciones relevantes |
| ROA-004 | Observabilidad desacoplada | La generación de evidencia no modifica ni interfiere con la lógica funcional |
| ROA-005 | Identificación de componente | Toda evidencia permite identificar el componente que la originó |
| ROA-006 | Correlación de eventos | Evidencia de una misma operación asociable entre sí |
| ROA-007 | Registro de errores | Errores registrados según el modelo oficial de manejo de errores |
| ROA-008 | Evolución controlada | Nueva evidencia, métricas o mecanismos preservan compatibilidad |

### 15.3 Principios de Observabilidad
Garantizar: comprensión del comportamiento; diagnóstico de incidentes; medición objetiva de desempeño; trazabilidad; compatibilidad con el modelo de manejo de errores; separación observabilidad–lógica de negocio; evolución controlada.

---

## 16. Estrategia de Escalabilidad

Reglas para expandir capacidades progresivamente preservando estabilidad, coherencia y mantenibilidad. La escalabilidad se logra principalmente por evolución de la arquitectura, no solo por aumento de recursos tecnológicos.

### 16.1 Dimensiones de Escalabilidad

| Dimensión | Definición |
|---|---|
| Funcional | Incorporar nuevos procesos de negocio sin afectar módulos existentes: nuevos módulos, etapas de flujo, criterios de análisis, procesos de automatización |
| Servicios | Incorporar nuevos servicios compartidos reutilizables sin modificar los existentes, respetando los principios |
| Integración | Incorporar nuevas integraciones externas manteniendo el modelo oficial del Capítulo 10; sin afectar módulos consumidores |
| Información | Gestionar crecimiento progresivo del volumen persistido sin modificar la organización; evolución del modelo de datos compatible con la arquitectura de persistencia |
| Operacional | Aumentar frecuencia de ejecución, número de procesos automatizados y volumen de procesamiento preservando estabilidad |

### 16.2 Reglas Oficiales de Escalabilidad (REA)

| ID | Regla | Definición |
|---|---|---|
| REA-001 | Escalabilidad por composición | Evolución preferiblemente incorporando nuevos componentes, evitando modificar existentes |
| REA-002 | Evolución compatible | Toda expansión mantiene compatibilidad con la arquitectura general |
| REA-003 | Reutilización de servicios | Nuevas capacidades reutilizan servicios compartidos existentes cuando sea posible |
| REA-004 | Incorporación controlada de integraciones | Nueva integración conforme al modelo oficial |
| REA-005 | Independencia de módulos | Nuevos módulos no crean dependencias innecesarias con existentes |
| REA-006 | Compatibilidad documental | Toda expansión alineada con la documentación oficial |
| REA-007 | Escalabilidad progresiva | Incorporación incremental de capacidades, evitando rediseños estructurales |
| REA-008 | Evolución documentada | Toda modificación de escalabilidad documentada y justificada formalmente |

### 16.3 Principios de Escalabilidad
Garantizar: crecimiento progresivo; incorporación controlada de capacidades; preservación de modularidad; reutilización de componentes y servicios; compatibilidad con el stack; evolución sostenible.

---

## 17. Estrategia de Extensibilidad

Reglas para incorporar nuevas capacidades sin alterar innecesariamente componentes existentes. Evolución controlada manteniendo estabilidad, compatibilidad y coherencia. Se logra incorporando elementos que respeten interfaces, principios y reglas.

### 17.1 Dimensiones de Extensibilidad

| Dimensión | Definición |
|---|---|
| Funcional | Incorporar nuevos procesos de negocio sin modificar comportamiento de módulos existentes; vía nuevos módulos o extensiones compatibles |
| Componentes | Incorporar nuevos componentes para expandir capacidades; cumpliendo principios, organización modular y arquitectura por capas |
| Servicios | Incorporar nuevos servicios compartidos preservando independencia de los existentes; integración por interfaces públicas y compatibilidad con el catálogo oficial |
| Integración | Incorporar nuevas plataformas, proveedores o recursos externos respetando el modelo oficial; sin requerir modificaciones en módulos consumidores |
| IA | Incorporar nuevos modelos, estrategias de procesamiento, instrucciones o capacidades de IA sin afectar módulos que usan el servicio oficial; desacoplado de lógica de negocio |

### 17.2 Reglas Oficiales de Extensibilidad (REX)

| ID | Regla | Definición |
|---|---|---|
| REX-001 | Extensión por incorporación | Nueva capacidad preferiblemente vía nuevos componentes/módulos/servicios |
| REX-002 | Preservación de componentes existentes | Extensiones no requieren modificar componentes estabilizados cuando sea técnicamente viable |
| REX-003 | Compatibilidad con interfaces públicas | Nuevas capacidades usan exclusivamente interfaces públicas |
| REX-004 | Reutilización de servicios compartidos | Extensiones reutilizan servicios existentes cuando satisfacen la necesidad |
| REX-005 | Compatibilidad documental | Toda expansión alineada con la documentación oficial |
| REX-006 | Desacoplamiento de extensiones | Nuevas capacidades minimizan dependencias con componentes existentes |
| REX-007 | Evolución incremental | Extensiones incorporables progresivamente sin afectar estabilidad |
| REX-008 | Documentación obligatoria | Nueva extensión documentada y justificada formalmente antes de incorporarse |

### 17.3 Principios de Extensibilidad
Garantizar: incorporación controlada; preservación de estabilidad; reutilización de componentes y servicios; bajo acoplamiento entre extensiones y componentes existentes; compatibilidad con el stack; evolución sostenible.

---

## 18. Restricciones Arquitectónicas (RAR)

Condiciones obligatorias en diseño, implementación, mantenimiento y evolución. Preservan coherencia evitando desviaciones que comprometan modularidad, mantenibilidad, escalabilidad o compatibilidad. Consolidan principios, objetivos y reglas previos; **no** introducen nuevos requisitos.

### 18.1 Restricciones Estructurales

| ID | Restricción | Definición |
|---|---|---|
| RAR-001 | Uso obligatorio de la arquitectura oficial | Toda implementación respeta la organización arquitectónica de este documento |
| RAR-002 | Respeto a la organización modular | Componentes organizados según la estructura modular |
| RAR-003 | Respeto a la arquitectura por capas | Todo módulo implementa la organización por capas del Capítulo 7 |
| RAR-004 | Comunicación por interfaces públicas | Componentes se comunican solo por interfaces oficiales |
| RAR-005 | Prohibición de dependencias circulares | No se permiten dependencias circulares entre módulos, componentes o servicios |

### 18.2 Restricciones Funcionales

| ID | Restricción | Definición |
|---|---|---|
| RAR-006 | Respeto al flujo oficial | La implementación mantiene el flujo funcional definido |
| RAR-007 | Separación procesamiento inteligente–lógica de negocio | La IA no reemplaza al Motor de Decisión ni implementa reglas de negocio |
| RAR-008 | Uso de servicios compartidos | Funcionalidad reutilizable implementada vía servicios compartidos |
| RAR-009 | Separación negocio–infraestructura | Lógica funcional desacoplada de infraestructura tecnológica e integraciones |

### 18.3 Restricciones Tecnológicas

| ID | Restricción | Definición |
|---|---|---|
| RAR-010 | Compatibilidad con el stack | Toda implementación usa el stack oficial aprobado |
| RAR-011 | Integraciones controladas | Comunicación con recursos externos solo por el modelo oficial |
| RAR-012 | Persistencia desacoplada | Módulos funcionales no acceden directamente a almacenamiento; interacción solo vía servicio de Persistencia |
| RAR-013 | Configuración centralizada | Configuración gestionada exclusivamente vía SRV-005 |

### 18.4 Restricciones Documentales

| ID | Restricción | Definición |
|---|---|---|
| RAR-014 | Compatibilidad documental | Toda implementación alineada con Documentos 0–12 y decisiones oficiales aprobadas |
| RAR-015 | Trazabilidad de cambios | Toda modificación arquitectónica documentada, justificada y trazable respecto a la versión anterior |
| RAR-016 | Evolución controlada | Toda expansión preserva compatibilidad con objetivos, principios y restricciones de este documento |

### 18.5 Principios de Cumplimiento
Toda implementación debe demostrar cumplimiento de estas restricciones antes de considerarse compatible con la arquitectura oficial. El incumplimiento se trata como **desviación arquitectónica** y requiere análisis, justificación y aprobación formal antes de incorporarse.

---

## 19. Criterios de Aceptación (CA)

Mecanismo oficial para verificar que una implementación, modificación o expansión cumple la arquitectura. Proceso de validación objetivo, uniforme y trazable. Consolidan objetivos, principios, reglas y restricciones previos; **no** introducen nuevos requisitos.

### 19.1 Alcance de Validación
Aplicar mínimo en: implementación de nuevos módulos; incorporación de nuevos componentes; desarrollo de nuevos servicios compartidos; incorporación de nuevas integraciones; modificaciones arquitectónicas; refactorizaciones con impacto estructural; validación del MVP; validación de versiones posteriores.

### 19.2 Matriz de Conformidad Arquitectónica

| ID | Criterio | Verificación |
|---|---|---|
| CA-001 | Objetivos arquitectónicos | Cumplimiento de OA |
| CA-002 | Principios arquitectónicos | Respeto de PA |
| CA-003 | Componentes oficiales | Uso correcto de CMP |
| CA-004 | Servicios compartidos | Uso de SRV según responsabilidades oficiales |
| CA-005 | Comunicación entre módulos | Respeto de RCM |
| CA-006 | Arquitectura de persistencia | Cumplimiento de RP |
| CA-007 | Arquitectura de IA | Cumplimiento de RAI |
| CA-008 | Gestión de configuración | Respeto de RCF |
| CA-009 | Arquitectura de seguridad | Cumplimiento de RSA |
| CA-010 | Arquitectura de observabilidad | Cumplimiento de ROA |
| CA-011 | Estrategia de escalabilidad | Respeto de REA |
| CA-012 | Estrategia de extensibilidad | Cumplimiento de REX |
| CA-013 | Restricciones arquitectónicas | Cumplimiento de todos los RAR |

### 19.3 Resultado de Validación
Cada criterio se evalúa exclusivamente con uno de estos resultados:
- **Cumple:** criterio totalmente satisfecho.
- **No cumple:** criterio no satisfecho.
- **No aplica:** criterio no aplicable al elemento evaluado.

Sin estados intermedios ni interpretaciones subjetivas.

### 19.4 Criterios de Aprobación
Una implementación es compatible con la arquitectura oficial solo cuando:
- Cumple todos los criterios aplicables.
- No viola ninguna restricción arquitectónica.
- Mantiene compatibilidad con la documentación oficial.
- Preserva la coherencia estructural.

Toda desviación identificada debe documentarse, justificarse y resolverse antes de aprobar su incorporación.

### 19.5 Principios de Validación
Garantizar: objetividad; trazabilidad de resultados; uniformidad de criterios; repetibilidad del proceso; compatibilidad con toda la documentación oficial; evolución controlada de la arquitectura.

---

## 20. Vista Arquitectónica Consolidada

Representación oficial de la arquitectura general. Integra en una sola representación coherente todos los elementos definidos en este documento, proveyendo una vista de alto nivel que facilita comprender la organización del sistema y las relaciones entre componentes principales.

**Sintetiza:** organización general; módulos de negocio; componentes principales; servicios compartidos; integraciones externas; arquitectura por capas; flujo general de interacción; arquitecturas especializadas (persistencia, IA, configuración, seguridad, observabilidad); estrategias de escalabilidad y extensibilidad; restricciones y criterios de aceptación.

**Reglas de sincronización:** constituye el punto de referencia principal para entender la organización estructural y debe permanecer permanentemente sincronizada con las decisiones arquitectónicas oficialmente aprobadas. Toda modificación que afecte la arquitectura general debe reflejarse tanto en los capítulos correspondientes como en la representación consolidada, preservando coherencia entre documentación y arquitectura actual.

**Representación gráfica:** el diagrama oficial de la Vista Arquitectónica Consolidada es parte integral de este documento y constituye la referencia visual autorizada para interpretar la estructura general. Se crea y mantiene como parte de la documentación arquitectónica del proyecto y debe reflejar fielmente todas las decisiones aprobadas.
