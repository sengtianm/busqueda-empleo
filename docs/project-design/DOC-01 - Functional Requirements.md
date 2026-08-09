# Requisitos Funcionales (DOC-01)

## 1. Propósito y Objetivos

**Propósito:** Automatización modular, escalable y mantenible que gestiona integralmente la búsqueda de empleo: descubre, recopila, prepara, evalúa y administra ofertas de trabajo; automatiza tareas repetitivas y operativas; genera información estructurada y recursos de postulación; mantiene las decisiones estratégicas bajo control del usuario.

**Objetivos específicos:**

1. Descubrir oportunidades desde fuentes configuradas.
2. Centralizar ofertas en un repositorio único estructurado, sin duplicados, con historial.
3. Preparar cada oferta (limpieza, normalización, validación).
4. Evaluar automáticamente compatibilidad con el perfil profesional usando criterios predefinidos.
5. Clasificar por prioridad y estado de procesamiento.
6. Analizar en profundidad ofertas que superan la evaluación inicial.
7. Generar automáticamente recursos de apoyo a la postulación según características de cada oferta.
8. Mantener registro completo del ciclo de vida (cambios de estado, decisiones, resultados).
9. Proveer información clara, organizada y suficiente para decisiones del usuario en cada etapa.
10. Reducir tiempo/esfuerzo en tareas repetitivas mediante automatización.
11. Permitir incorporar nuevas fuentes, reglas y funcionalidades sin afectar componentes existentes.

---

## 2. Alcance Funcional

### 2.1 Capacidades incluidas

| Área | Capacidades |
|------|-------------|
| **Descubrimiento** | Consultar fuentes configuradas · Detectar nuevas ofertas · Extraer información disponible · Registrar ofertas descubiertas |
| **Preparación** | Limpiar y normalizar información extraída · Validar integridad de datos · Detectar y eliminar duplicados · Asignar estado inicial de procesamiento |
| **Evaluación inicial** | Analizar cada oferta según criterios definidos · Calcular puntuación de compatibilidad · Clasificar por prioridad · Descartar automáticamente ofertas que violan reglas predefinidas |
| **Procesamiento profundo** | Analizar en detalle ofertas seleccionadas · Identificar requisitos, responsabilidades, beneficios y otra información relevante · Generar información estructurada para preparación de postulación · Preparar recursos definidos para el proceso de postulación |
| **Gestión de procesos** | Mantener historial completo de cada oferta · Gestionar estados del flujo de trabajo · Registrar decisiones y resultados · Permitir seguimiento del ciclo de vida completo |
| **Administración** | Configurar fuentes de empleo · Actualizar criterios de evaluación · Incorporar nuevas reglas y funcionalidades sin afectar componentes existentes |

### 2.2 Funciones principales (F1–F10)

| Código | Función | Detalle |
|--------|---------|---------|
| **F1** | Descubrimiento de oportunidades | Consultar fuentes configuradas · Detectar ofertas nuevas · Extraer información relevante · Registrar fecha, hora y fuente del descubrimiento |
| **F2** | Gestión de ofertas | Crear registro único por oferta · Detectar y prevenir duplicados · Actualizar información cuando la oferta cambia · Mantener historial de modificaciones |
| **F3** | Preparación de información | Limpiar datos extraídos · Normalizar formatos y estructuras · Completar información derivada cuando sea posible · Validar calidad de datos obtenidos |
| **F4** | Evaluación automatizada | Analizar ofertas con criterios predefinidos · Calcular puntuación de compatibilidad · Clasificar por prioridad · Identificar automáticamente ofertas a descartar |
| **F5** | Procesamiento profundo | Analizar contenido completo de la oferta · Identificar requisitos técnicos y funcionales · Extraer responsabilidades, beneficios y condiciones laborales · Generar información estructurada para apoyar la postulación |
| **F6** | Generación de recursos | Generar documentos, análisis o recursos definidos para cada postulación · Organizar por oferta · Mantener trazabilidad entre recurso generado y oferta correspondiente |
| **F7** | Gestión del flujo de trabajo | Controlar estados de cada oferta durante todo su ciclo de vida · Registrar cada transición de estado · Registrar decisiones automatizadas y del usuario · Permitir reanudar procesos interrumpidos |
| **F8** | Administración | Gestionar fuentes de empleo · Gestionar criterios de evaluación · Gestionar configuración general del sistema · Gestionar catálogos, reglas y parámetros |
| **F9** | Consulta y seguimiento | Ver historial completo de ofertas · Ver estado actual de cada oferta · Ver resultados de evaluación · Acceder a información generada durante el procesamiento |
| **F10** | Registro y auditoría | Registrar eventos relevantes del sistema · Registrar errores y excepciones · Registrar decisiones automatizadas · Mantener trazabilidad completa del procesamiento de cada oferta |

### 2.3 Fuera de alcance

**Principio general:** La automatización no realiza decisiones estratégicas, no modifica el perfil profesional sin autorización, no envía postulaciones automáticamente salvo aprobación explícita, no reemplaza el juicio del usuario en decisiones de alto impacto, y no ejecuta actividades ajenas al proceso de búsqueda y preparación de oportunidades laborales.

| Código | Función excluida | Detalle |
|--------|------------------|---------|
| **FNA-1** | Postulación automática | No enviar postulaciones sin aprobación explícita del usuario |
| **FNA-2** | Decisiones estratégicas | No reemplazar el juicio del usuario en decisiones de alto impacto: elegir empresa, decidir si una oportunidad vale la pena personalmente, modificar criterios profesionales sin autorización |
| **FNA-3** | Modificación del perfil profesional | No modificar automáticamente: currículum, perfil profesional, portafolio, información personal, preferencias laborales |
| **FNA-4** | Comunicación con terceros | No enviar correos, mensajes ni comunicación externa en nombre del usuario salvo funcionalidad explícitamente diseñada, implementada y aprobada |
| **FNA-5** | Gestión de entrevistas | No programar entrevistas, aceptar invitaciones ni responder automáticamente a procesos de reclutamiento |
| **FNA-6** | Actividades fuera del alcance | No ejecutar tareas no directamente relacionadas con descubrimiento, análisis, evaluación, preparación y gestión de oportunidades laborales |
| **FNA-7** | Aprendizaje autónomo | No modificar reglas de negocio, criterios de evaluación ni configuraciones del sistema por sí mismo sin intervención del usuario |

---

## 3. Actores del Sistema

| Código | Actor | Descripción | Responsabilidades / Ejemplos |
|--------|-------|-------------|------------------------------|
| **A1** | Usuario | Propietario y operador de la automatización | Configurar el sistema · Definir criterios de evaluación · Autorizar decisiones que requieren intervención humana · Revisar resultados generados · Actualizar información profesional cuando sea necesario |
| **A2** | Plataformas de empleo | Fuentes de las cuales la automatización obtiene oportunidades | Publicar ofertas · Proveer información disponible para procesamiento · *Ejemplos:* LinkedIn, Indeed, Computrabajo, Magneto, sitios corporativos de carreras, otras fuentes configuradas por el usuario |
| **A3** | Modelo de IA | Servicio de IA usado para analizar y generar información | Analizar ofertas · Extraer información relevante · Clasificar contenido · Generar análisis · Apoyar generación de recursos de postulación |
| **A4** | Servicios externos | Cualquier servicio de apoyo a la operación de la automatización | Almacenar información · Facilitar comunicación entre componentes · Proveer servicios de soporte · *Ejemplos:* servicios de almacenamiento, bases de datos, servicios de archivos, herramientas de automatización, APIs auxiliares |

**Dependencias externas:** Plataformas de empleo · Modelo de IA · Base de datos · Navegador · Sistema de archivos · APIs.

---

## 4. Entradas del Sistema (E-001 a E-007)

| Código | Entrada | Contenido |
|--------|---------|-----------|
| **E-001** | Configuración del usuario | Fuentes de empleo · Frecuencia de ejecución · Preferencias generales · Parámetros de configuración |
| **E-002** | Perfil profesional | Currículum · Perfil profesional · Experiencia laboral · Habilidades · Tecnologías · Idiomas · Certificaciones · Formación académica · Preferencias laborales · Expectativas salariales · Modalidad de trabajo · Ubicación · Empresas objetivo · Empresas restringidas |
| **E-003** | Ofertas de trabajo | Título · Empresa · Descripción · Requisitos · Responsabilidades · Beneficios · Salario · Modalidad de trabajo · Ubicación · Fecha de publicación · URL · Identificador de la oferta · Plataforma de origen |
| **E-004** | Reglas de negocio | Reglas de evaluación · Reglas de rechazo · Reglas de aceptación · Prioridades · Umbrales · Excepciones |
| **E-005** | Prompts y configuraciones de IA | Prompts · Plantillas · Parámetros de ejecución · Configuraciones de procesamiento |
| **E-006** | Información histórica | Historial de ofertas · Estados anteriores · Resultados de evaluación · Documentos generados · Logs de ejecución · Decisiones del usuario |
| **E-007** | Decisiones del usuario | Aprobar una oferta · Rechazar una oferta · Solicitar nuevo análisis · Modificar criterios de evaluación · Reanudar un proceso |

---

## 5. Datos Internos (DI-001 a DI-007)

| Código | Dato interno | Contenido |
|--------|--------------|-----------|
| **DI-001** | Identificadores internos | ID interno de oferta · ID de procesamiento · ID de ejecución · ID de análisis · ID de documento generado |
| **DI-002** | Estados de procesamiento | Estado actual · Estado anterior · Fecha de cambio · Motivo del cambio · Responsable del cambio (usuario o sistema) |
| **DI-003** | Resultados intermedios | Puntuaciones parciales · Clasificaciones temporales · Información extraída · Datos normalizados · Resultados de validación |
| **DI-004** | Configuración operativa | Parámetros internos · Variables de ejecución · Configuración de módulos · Configuración del flujo de trabajo · Umbrales internos |
| **DI-005** | Historial del sistema | Historial de cambios · Historial de evaluaciones · Historial de decisiones · Historial de reprocesamiento |
| **DI-006** | Métricas de ejecución | Tiempo de ejecución · Duración por módulo · Número de ofertas procesadas · Número de errores · Número de reintentos · Indicadores de rendimiento |
| **DI-007** | Relaciones internas | Oferta ↔ Evaluaciones · Oferta ↔ Documentos · Oferta ↔ Historial · Oferta ↔ Decisiones · Oferta ↔ Ejecuciones |

---

## 6. Salidas del Sistema (S-001 a S-007)

| Código | Salida | Contenido |
|--------|--------|-----------|
| **S-001** | Ofertas estructuradas | Información normalizada de cada oferta, lista para ser usada por los procesos de la automatización: información limpia · campos normalizados · datos validados · identificadores internos |
| **S-002** | Resultados de evaluación inicial | Puntuación · Nivel de compatibilidad · Prioridad · Motivos de aceptación · Motivos de rechazo · Recomendaciones |
| **S-003** | Análisis profundo de la oferta | Resumen ejecutivo · Requisitos identificados · Competencias técnicas · Habilidades blandas · Responsabilidades · Beneficios · Riesgos · Observaciones relevantes |
| **S-004** | Recursos de postulación | Análisis estratégicos · Información organizada · Documentos definidos para cada oferta · Otros recursos aprobados durante el desarrollo del proyecto |
| **S-005** | Estado de la oferta | Estado actual · Fecha de última actualización · Historial de estados · Persona o sistema responsable de la última decisión |
| **S-006** | Informes | Número de ofertas descubiertas · Número de ofertas descartadas · Número de ofertas priorizadas · Tiempo de procesamiento · Métricas de ejecución · Estadísticas generales |
| **S-007** | Logs del sistema | Eventos · Errores · Advertencias · Decisiones automatizadas · Decisiones del usuario · Historial de ejecución |

---

## 7. Flujo de Trabajo Funcional (FF-01 a FF-09)

| Etapa | Código | Proceso | Acciones |
|-------|--------|---------|----------|
| **1. Descubrimiento** | FF-01 | FP-01 | Consultar fuentes configuradas · Detectar nuevas ofertas · Extraer información disponible · Registrar la oferta en el sistema |
| **2. Preparación** | FF-02 | FP-02 | Limpiar información · Normalizar datos · Validar integridad de la oferta · Detectar duplicados · Asignar estado inicial |
| **3. Evaluación inicial** | FF-03 | FP-03 | Analizar compatibilidad con el perfil profesional · Aplicar reglas de rechazo · Calcular puntuación inicial · Clasificar prioridad |
| **4. Decisión inicial** | FF-04 | — | Si la oferta no cumple criterios mínimos → fin del procesamiento. Si cumple → continuar a procesamiento profundo |
| **5. Procesamiento profundo** | FF-05 | FP-05 | Analizar la oferta en detalle · Identificar requisitos y competencias · Analizar responsabilidades y beneficios · Generar información estructurada |
| **6. Generación de recursos** | FF-06 | FP-06 | Preparar recursos definidos para apoyar la postulación · Organizar resultados generados · Asociar recursos con la oferta correspondiente |
| **7. Revisión del usuario** | FF-07 | FP-07 | Cuando el flujo requiere decisión estratégica: presentar información al usuario · esperar decisión · registrar decisión tomada |
| **8. Gestión y seguimiento** | FF-08 | FP-08 | Actualizar estado de la oferta · Registrar historial · Preservar trazabilidad completa · Mantener disponible toda la información generada |
| **9. Finalización** | FF-09 | — | Marcar procesamiento como completado · Registrar fecha de finalización · Preservar toda la información para referencia futura |

---

## 8. Ciclo de Vida y Catálogo de Estados

**Nota (decisión 2026-07-30):** Los 7 estados siguientes son la única fuente de verdad para el ciclo de vida de la oferta, alineados con `shared/state_machine.py`. Versiones anteriores del catálogo (EST-001..010, EST-999 Error) quedan obsoletas.

| Código | Estado | Descripción | Proceso funcional | Asignado por | Estados anteriores | Estados siguientes | Estado final |
|--------|--------|-------------|-------------------|--------------|--------------------|--------------------|--------------|
| **EST-001** | Descubierto | La oferta fue identificada en una fuente y registrada por primera vez | FP-01 Descubrimiento | Sistema | Ninguno | EST-002 | No |
| **EST-002** | Preparado | La información fue limpiada, normalizada y validada | FP-02 Preparación | Sistema | EST-001 | EST-003 | No |
| **EST-003** | Evaluado | La oferta fue evaluada según las reglas de negocio | FP-03 Evaluación inicial | Sistema | EST-002 | EST-004 · EST-005 | No |
| **EST-004** | Aceptado | La oferta superó la evaluación inicial y está aprobada para continuar | FP-03 Evaluación inicial | Sistema | EST-003 | EST-006 | No |
| **EST-005** | Descartado | La oferta ya no se procesa porque no cumplió las reglas definidas o porque el usuario decidió descartarla | FP-03 Evaluación inicial · FP-07 Revisión del usuario | Sistema · Usuario | EST-003 | EST-007 | **Sí** |
| **EST-006** | Procesado | La oferta fue analizada en profundidad y toda la información requerida para apoyar la postulación fue generada | FP-05 Procesamiento profundo | Sistema | EST-004 | EST-007 | No |
| **EST-007** | Finalizado | La oferta completó su ciclo de vida dentro de la automatización y toda la información relacionada fue almacenada para referencia futura | FP-08 Gestión y seguimiento | Sistema | EST-005 · EST-006 | — | **Sí** |

**Etapas del ciclo de vida (LC-01 a LC-07):** Corresponden directamente a los estados EST-001 a EST-007 respectivamente: LC-01 Descubierto · LC-02 Preparado · LC-03 Evaluado · LC-04 Aceptado · LC-05 Descartado · LC-06 Procesado · LC-07 Finalizado.

---

## 9. Decisiones Automatizadas (DA-001 a DA-008)

**Principio general:** Toda decisión automatizada debe ser: reproducible · trazable · auditable · basada en reglas documentadas · reversible cuando sea técnicamente posible.

| Código | Decisión | Acciones |
|--------|----------|----------|
| **DA-001** | Descubrimiento de ofertas | Detectar nuevas ofertas · Identificar si una oferta ya existe · Registrar nuevas oportunidades |
| **DA-002** | Preparación de información | Limpiar datos · Normalizar formatos · Validar campos requeridos · Detectar información inconsistente |
| **DA-003** | Gestión de duplicados | Identificar ofertas duplicadas · Asociar registros equivalentes · Prevenir procesamiento duplicado |
| **DA-004** | Evaluación inicial | Calcular puntuación de compatibilidad · Aplicar reglas de rechazo · Asignar prioridad · Clasificar la oferta |
| **DA-005** | Procesamiento profundo | Analizar contenido de la oferta · Extraer requisitos · Identificar competencias · Generar información estructurada · Producir los análisis definidos por el sistema |
| **DA-006** | Generación de recursos | Generar recursos definidos para apoyar la postulación · Organizar la información generada · Asociar cada recurso con su oferta correspondiente |
| **DA-007** | Gestión del flujo de trabajo | Cambiar estado del ciclo de vida cuando se cumplen las condiciones definidas · Actualizar estado operativo · Registrar eventos, métricas e historial |
| **DA-008** | Recuperación operativa | Reintentar procesos cuando existe estrategia de recuperación definida · Reanudar procesos interrumpidos · Marcar procesos que requieren intervención del usuario |

---

## 10. Decisiones que Requieren Intervención del Usuario (DU-001 a DU-008)

**Principio general:** Toda decisión con consecuencias estratégicas, legales, personales o de representación del usuario requiere aprobación explícita del usuario antes de su ejecución.

| Código | Decisión | Detalle |
|--------|----------|---------|
| **DU-001** | Aprobación de oportunidad | Decidir si una oferta debe seguir siendo considerada una oportunidad valiosa |
| **DU-002** | Rechazo manual | Descartar una oferta por motivos personales o estratégicos que no pueden determinarse automáticamente: preferencias personales, cultura organizacional, interés en la empresa, información externa no disponible para el sistema |
| **DU-003** | Priorización excepcional | Modificar manualmente la prioridad asignada automáticamente por el sistema |
| **DU-004** | Aprobación de postulación | Autorizar la preparación final de una postulación para una oferta específica |
| **DU-005** | Envío de postulación | Autorizar cualquier acción que implique enviar información del usuario a terceros: enviar currículum, completar formulario de postulación, enviar correo, compartir documentos |
| **DU-006** | Modificación del perfil profesional | Autorizar cambios en: currículum, perfil profesional, portafolio, información personal, preferencias laborales |
| **DU-007** | Modificación de reglas del sistema | Aprobar cambios en: reglas de evaluación, reglas de rechazo, umbrales, configuraciones críticas, criterios de decisión |
| **DU-008** | Reprocesamiento excepcional | Autorizar reprocesamiento de ofertas cuando el sistema detecta situaciones que no pueden resolverse automáticamente |

---

## 11. Reglas Funcionales Generales (GFR-001 a GFR-015)

| Código | Regla | Definición |
|--------|-------|------------|
| **GFR-001** | Trazabilidad | Toda acción, decisión, recomendación y cambio de estado debe ser registrado |
| **GFR-002** | Identificación única | Toda oferta debe tener un identificador único e inmutable dentro del sistema |
| **GFR-003** | No duplicación | La misma oferta nunca debe ser procesada simultáneamente más de una vez |
| **GFR-004** | Integridad de la información | La automatización no debe eliminar ni modificar la información original obtenida de las fuentes. Cualquier transformación se realiza sobre datos derivados o normalizados |
| **GFR-005** | Separación de datos | Entradas, datos internos y salidas deben permanecer como entidades conceptualmente independientes |
| **GFR-006** | Trazabilidad documental | Todo documento, análisis o recurso generado debe ser trazable hasta la oferta que lo originó |
| **GFR-007** | Control de estados | Toda oferta debe tener siempre exactamente un estado de ciclo de vida y un estado operativo. Nunca deben existir estados conflictivos simultáneamente |
| **GFR-008** | Pre-validación | Ningún proceso debe ejecutarse a menos que la oferta cumpla los requisitos mínimos definidos para esa etapa |
| **GFR-009** | Recuperación controlada | Ante un error recuperable, el sistema debe intentar resolverlo según la estrategia de recuperación definida antes de solicitar intervención del usuario |
| **GFR-010** | Intervención del usuario | Las decisiones estratégicas solo se ejecutan tras autorización explícita del usuario |
| **GFR-011** | Consistencia del procesamiento | Toda oferta debe avanzar por el flujo de trabajo funcional según las transiciones de ciclo de vida definidas |
| **GFR-012** | Auditabilidad | Toda decisión automatizada debe ser justificable mediante reglas documentadas |
| **GFR-013** | Configuración centralizada | Reglas de negocio, parámetros y configuraciones se gestionan desde un único punto de configuración |
| **GFR-014** | Modularidad | Los componentes deben diseñarse para minimizar dependencias y facilitar mantenimiento, reemplazo y expansión futura |
| **GFR-015** | Escalabilidad | La adición de nuevas fuentes, reglas de negocio, módulos o funcionalidades no debe requerir modificaciones significativas de componentes existentes |

---

## 12. Catálogo de Casos de Uso (UC-001 a UC-025)

| Área | Casos de uso |
|------|--------------|
| **Gestión de configuración** | UC-001 Configurar el sistema · UC-002 Configurar fuentes de empleo · UC-003 Configurar reglas de evaluación · UC-004 Configurar preferencias del usuario |
| **Descubrimiento** | UC-005 Descubrir nuevas ofertas · UC-006 Registrar una oferta · UC-007 Detectar ofertas duplicadas |
| **Preparación** | UC-008 Preparar una oferta · UC-009 Normalizar información · UC-010 Validar información |
| **Evaluación** | UC-011 Evaluar una oferta · UC-012 Clasificar una oferta · UC-013 Descartar una oferta |
| **Procesamiento profundo** | UC-014 Analizar una oferta · UC-015 Extraer requisitos · UC-016 Generar análisis · UC-017 Generar recursos de postulación |
| **Gestión** | UC-018 Ver una oferta · UC-019 Ver historial · UC-020 Ver estado de una oferta · UC-021 Reprocesar una oferta · UC-022 Registrar decisión del usuario |
| **Administración** | UC-023 Ver métricas · UC-024 Ver logs · UC-025 Gestionar configuraciones del sistema |

*Nota: La especificación detallada de cada caso de uso se documenta por separado.*

---

## 13. Restricciones Funcionales (FC-001 a FC-010)

| Código | Restricción |
|--------|-------------|
| **FC-001** | El sistema solo procesa ofertas originadas en fuentes previamente configuradas |
| **FC-002** | Toda oferta debe tener un identificador único antes de iniciar el procesamiento |
| **FC-003** | No debe existir más de una instancia activa de procesamiento para la misma oferta |
| **FC-004** | Ninguna oferta avanza a la siguiente etapa del flujo sin haber completado exitosamente la etapa anterior, salvo regla documentada que lo permita explícitamente |
| **FC-005** | Las decisiones estratégicas siempre requieren autorización explícita del usuario |
| **FC-006** | Toda decisión automatizada debe estar respaldada por una regla documentada |
| **FC-007** | Toda información generada debe mantener trazabilidad hasta la oferta que la originó |
| **FC-008** | La automatización debe preservar el historial completo de cada oferta |
| **FC-009** | Los errores deben registrarse antes de iniciar cualquier proceso de recuperación |
| **FC-010** | El sistema debe mantener consistencia entre el estado de ciclo de vida y el estado operativo de cada oferta |

---

## 14. Criterios de Aceptación (AC-001 a AC-010)

| Código | Criterio |
|--------|----------|
| **AC-001** | Es capaz de descubrir ofertas desde las fuentes configuradas |
| **AC-002** | Registra cada oferta con un identificador único |
| **AC-003** | Prepara y valida correctamente la información obtenida |
| **AC-004** | Evalúa automáticamente las ofertas usando las reglas definidas |
| **AC-005** | Genera la información requerida para apoyar el proceso de postulación |
| **AC-006** | Mantiene actualizados tanto el estado de ciclo de vida como el estado operativo de cada oferta |
| **AC-007** | Registra toda acción, decisión y recomendación realizada durante el procesamiento |
| **AC-008** | Solicita intervención del usuario cuando se requiere una decisión estratégica |
| **AC-009** | Mantiene trazabilidad completa de cada oferta durante todo su ciclo de vida |
| **AC-010** | Permite extender el sistema con nuevas fuentes, reglas de negocio y funcionalidades sin afectar el comportamiento de componentes existentes |

---

## 15. Módulo 1: Descubrimiento de Oportunidades — Requisitos Funcionales Específicos

Los siguientes requisitos complementan los generales de este documento para el Módulo 1. Derivan del análisis comparativo de la ficha técnica (M1, 2026-08-07, §7c — conjunto imprescindible) y las decisiones D1–D4.

| Código | Requisito | Detalle |
|--------|-----------|---------|
| **RF-M1-001** | Corrida única | El módulo ejecuta una sola corrida por invocación (`corrida`), identificada unívocamente por `run_id`; todo registro generado por el módulo (ofertas, eventos, sesiones) se ancla a su `run_id` (trazabilidad en todo registro; RN-01) |
| **RF-M1-002** | Bloqueo de concurrencia | El módulo no permite una segunda corrida mientras otra está activa; el control de concurrencia es un bloqueo persistente (`bloqueo` con `run_id` y timestamp) con umbral de obsolescencia configurable (D3; ERR-06/07/08/09) |
| **RF-M1-003** | Sesión de plataforma reutilizable | Cuando la entrada a la fuente tiene éxito, el módulo crea una sesión (`session_id`), la mantiene disponible para nodos subsiguientes durante la corrida, y la cierra al salir; la sesión es auditable (auditoría T2, D3: `session_id`, `run_id`, `source_id`, `set_indice`, `timestamp`, `total_declarado`, `conteo`, `estado`) |
| **RF-M1-004** | Almacén seguro de credenciales | El módulo resuelve credenciales solo desde un almacén seguro (referencia en configuración, valores en `.env` vía dotenv — D4); las credenciales nunca se registran en logs, eventos ni base de datos |
| **RF-M1-005** | Políticas de captura | El módulo aplica políticas de captura por fuente y por corrida (`max_paginas`, `max_ofertas_por_corrida`, `pausa_entre_lotes`, estrategia anti-bloqueo), resolviendo valores efectivos fusionando políticas por fuente con defaults globales (RN-11) |
| **RF-M1-006** | Sets de filtros | El módulo itera los sets de filtros básicos configurados (`sets_de_filtros`) de la fuente actual en orden de configuración (set vacío = búsqueda base) y expone el índice del set en curso (`set_indice`) |
| **RF-M1-007** | Adaptador de plataforma | El módulo interactúa con cada plataforma mediante un adaptador que encapsula: parámetros de acceso (ficha de acceso), resolución de credenciales, búsqueda, parseo y captura de ofertas; el adaptador preserva la integridad de la información original (C2) y soporta el mecanismo masivo/incremental de la plataforma (RN-10) |
| **RF-M1-008** | Reintentos condicionales | El módulo reintenta solo los motivos `fuente_inalcanzable` y `timeout_*` (entrada/consulta/captura), con backoff exponencial y desde canal cerrado; los demás códigos producen fallo inmediato y nunca se reintentan (REC-003, DOC-06 §11) |
| **RF-M1-009** | Códigos de error por nodo | Todo nodo identifica su fallo con el código de negocio oficial del catálogo (`ERR-XX`/`EVT-01`) y un `codigo_motivo`, mapeando a la categoría técnica `ER-<CAT>-<n>` (DOC-06, C7); no se permiten códigos locales de nodo sin mapeo técnico |

**Nota — Asignación de estado (C5):** En compatibilidad con los requisitos generales de este documento (catálogo de estados EST-001), el Módulo 1 inserta las ofertas descubiertas en el almacén "Ofertas Totales" con `estado='discovered'` (asignación por defecto, sin deduplicación; la normalización y deduplicación pertenecen al Módulo 2).

**Nota — Resolución de D1 (`fuentes.activa`):** El atributo `active` de cada fuente permanece en el modelo de datos como atributo de catálogo (decisión D1, 2026-08-07): su valor se gestiona manualmente y se ignora en tiempo de ejecución — la ausencia de `active` establecido en true no filtra fuentes, excluidas o incluidas durante la ejecución.

---

## 16. Módulo 1 — Conjunto Imprescindible (§7c del análisis)

El alcance funcional obligatorio del Módulo 1, sin el cual el módulo no cumple los requisitos generales (FF-01) ni el flujo de datos (DFT), es el siguiente conjunto:

| Imprescindible (§7c) | Requisito que lo cubre |
|----------------------|------------------------|
| Trazabilidad en todo registro | RF-M1-001 (corrida), más `source_id` / `session_id` / `set_indice` por registro |
| Ficha de acceso a la fuente | Cubierto por "Entrar a la fuente" (validación de acceso) |
| Bloqueo persistente | RF-M1-002 (D3, concurrencia) |
| `sets_de_filtros` | RF-M1-006 |
| `politicas_de_captura` | RF-M1-005 |
| Almacén seguro de credenciales | RF-M1-004 |
| Adaptador de plataforma | RF-M1-007 |
| Reintentos condicionales | RF-M1-008 |
| Códigos de error por nodo | RF-M1-009 |

Estos nueve puntos constituyen el alcance funcional mínimo del Módulo 1; su trazabilidad es obligatoria en todo registro (`run_id` + `source_id` + `session_id` + `set_indice` cuando aplique).
**Reducción estimada:** ~65-70 % del volumen original, 0 % de pérdida informativa.
