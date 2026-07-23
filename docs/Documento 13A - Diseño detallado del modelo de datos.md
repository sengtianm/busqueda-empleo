# Documento 13A - Diseño detallado del Modelo de Datos

# 1. Inventario oficial de entidades

El presente inventario constituye la relación oficial de todas las entidades persistentes que conformarán el modelo de datos de la automatización de búsqueda de empleo.

Cada entidad será desarrollada posteriormente en este documento mediante su especificación detallada.

| Entidad | Categoría | Dominio funcional | Descripción |
|---------|-----------|-------------------|-------------|
| Oferta | Principal | Descubrimiento de oportunidades | Representa cada oferta de empleo identificada por la automatización durante el proceso de búsqueda. |
| Fuente | Principal | Descubrimiento de oportunidades | Representa el origen desde el cual se obtiene una oferta de empleo. |
| Empresa | Principal | Descubrimiento de oportunidades | Representa la organización que publica la oferta de empleo. |
| Ubicación | Soporte | Descubrimiento de oportunidades | Representa la información geográfica asociada a una oferta de empleo. |
| Oferta Procesada | Principal | Procesamiento de la oferta | Representa la versión estructurada y normalizada de una oferta después de su procesamiento. |
| Evaluación Inicial | Principal | Evaluación inicial | Representa el resultado de la evaluación inicial realizada sobre una oferta de empleo. |
| Evaluación Detallada | Principal | Evaluación detallada | Representa el resultado de la evaluación completa de una oferta que superó la evaluación inicial. |
| Documento Generado | Operativa | Generación documental | Representa los documentos generados automáticamente por la automatización para una oferta determinada. |
| Postulación | Principal | Gestión de postulaciones | Representa cada proceso de postulación realizado sobre una oferta de empleo. |
| Evento | Operativa | Trazabilidad | Registra los eventos relevantes ocurridos durante el procesamiento de la automatización. |
| Decisión | Operativa | Modelo de decisiones | Registra las decisiones funcionales tomadas por la automatización durante el procesamiento de una oferta. |
| Configuración | Soporte | Configuración | Representa la configuración utilizada por la automatización durante su ejecución. |
| Catálogo | Soporte | Referencias | Representa los conjuntos de valores controlados utilizados por las diferentes entidades del modelo. |

---

# 2. Especificación detallada de las entidades

En este capítulo se documentará detalladamente cada una de las entidades que conforman el modelo de datos de la automatización.

Cada entidad será especificada utilizando una estructura uniforme con el fin de garantizar consistencia, facilitar la implementación de la base de datos y mantener la trazabilidad con el resto de la documentación del proyecto.

La especificación de cada entidad incluirá, como mínimo, la siguiente información:

- Nombre de la entidad.
- Descripción.
- Propósito dentro de la automatización.
- Atributos.
- Clave primaria.
- Claves alternativas (cuando existan).
- Claves foráneas (cuando existan).
- Relaciones con otras entidades.
- Cardinalidad de las relaciones.
- Restricciones.
- Máquina de estados (cuando aplique).
- Observaciones.

Las entidades serán documentadas en el siguiente orden:

1. Oferta.
2. Fuente.
3. Empresa.
4. Ubicación.
5. Oferta Procesada.
6. Evaluación Inicial.
7. Evaluación Detallada.
8. Documento Generado.
9. Postulación.
10. Evento.
11. Decisión.
12. Configuración.
13. Catálogo.

---

## 2.1. Entidad: Oferta

### Descripción

La entidad **Oferta** representa cada oportunidad laboral identificada por la automatización durante el proceso de descubrimiento de oportunidades.

Constituye la entidad principal del modelo de datos, ya que todo el procesamiento posterior de la automatización se realiza alrededor de una oferta de empleo.

Cada registro corresponde a una única oferta identificada en una fuente determinada.

---

### Propósito

Su propósito es almacenar la información original de cada oferta descubierta antes de cualquier proceso de normalización, evaluación o generación de documentos.

La entidad conserva la referencia oficial de la oferta durante todo su ciclo de vida dentro de la automatización.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la oferta. |
| fuente_id | UUID | Sí | Referencia a la fuente donde fue descubierta la oferta. |
| empresa_id | UUID | Sí | Referencia a la empresa que publica la oferta. |
| ubicacion_id | UUID | No | Referencia a la ubicación asociada a la oferta. |
| identificador_fuente | Texto | No | Identificador utilizado por la fuente de origen para la oferta. |
| url | Texto | Sí | Enlace original de la oferta. |
| titulo | Texto | Sí | Título original de la oferta. |
| descripcion_original | Texto largo | Sí | Contenido original de la oferta obtenido durante el descubrimiento. |
| fecha_publicacion | Fecha/Hora | No | Fecha de publicación indicada por la fuente. |
| fecha_descubrimiento | Fecha/Hora | Sí | Fecha y hora en que la automatización descubrió la oferta. |
| estado | Catálogo | Sí | Estado actual de la oferta dentro del flujo de procesamiento. |
| activa | Booleano | Sí | Indica si la oferta continúa vigente dentro del sistema. |
| observaciones | Texto largo | No | Información adicional relevante sobre la oferta. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- fuente_id → Fuente
- empresa_id → Empresa
- ubicacion_id → Ubicación
- estado → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Fuente | Pertenece a | N : 1 |
| Empresa | Es publicada por | N : 1 |
| Ubicación | Se localiza en | N : 1 |
| Oferta Procesada | Genera | 1 : 1 |
| Evaluación Inicial | Es evaluada mediante | 1 : 1 |
| Evaluación Detallada | Puede generar | 1 : 0..1 |
| Documento Generado | Puede generar | 1 : N |
| Postulación | Puede originar | 1 : 0..1 |
| Evento | Registra eventos | 1 : N |
| Decisión | Registra decisiones | 1 : N |

---

### Restricciones

- Toda oferta deberá pertenecer a una única fuente.
- Toda oferta deberá encontrarse asociada a una única empresa.
- La URL de la oferta deberá conservarse durante todo su ciclo de vida.
- El contenido original de la oferta no deberá sobrescribirse después de su descubrimiento.
- El estado de la oferta deberá seguir la máquina de estados definida para la entidad.

---

### Máquina de estados

La entidad seguirá la máquina de estados oficial definida para el procesamiento de ofertas de empleo.

La especificación detallada de dicha máquina de estados será documentada en el apartado correspondiente de este documento.

---

### Observaciones

La entidad **Oferta** constituye el punto de entrada del modelo de datos y sirve como referencia principal para todas las entidades derivadas del proceso de procesamiento, evaluación y postulación.


---

## 2.2. Entidad: Fuente

### Descripción

La entidad **Fuente** representa cada origen desde el cual la automatización descubre oportunidades de empleo.

Una fuente corresponde a una plataforma, sitio web, portal de empleo, página corporativa o cualquier otro medio autorizado para la obtención de ofertas laborales.

---

### Propósito

Su propósito es centralizar la información de cada origen de datos utilizado por la automatización, permitiendo identificar la procedencia de cada oferta y gestionar las características particulares de cada fuente.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la fuente. |
| nombre | Texto | Sí | Nombre oficial de la fuente. |
| tipo | Catálogo | Sí | Tipo de fuente utilizada por la automatización. |
| url_principal | Texto | Sí | URL principal de la fuente. |
| descripcion | Texto largo | No | Descripción general de la fuente. |
| activa | Booleano | Sí | Indica si la fuente se encuentra habilitada para el descubrimiento de ofertas. |
| frecuencia_consulta | Catálogo | No | Frecuencia configurada para consultar la fuente. |
| ultima_consulta | Fecha/Hora | No | Fecha y hora de la última consulta realizada. |
| ultima_actualizacion | Fecha/Hora | No | Fecha y hora de la última actualización detectada en la fuente, cuando sea posible determinarla. |
| observaciones | Texto largo | No | Información adicional relevante sobre la fuente. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- tipo → Catálogo
- frecuencia_consulta → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Publica | 1 : N |

---

### Restricciones

- Toda fuente deberá tener un nombre único dentro del sistema.
- La URL principal deberá identificar de forma unívoca la fuente.
- No podrán asociarse nuevas ofertas a una fuente inactiva.
- El tipo de fuente deberá corresponder a un valor válido del catálogo oficial.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Fuente** representa exclusivamente el origen de las ofertas de empleo.

No almacena información específica de una oferta individual, sino las características generales del origen desde el cual la automatización obtiene la información.

---

## 2.3. Entidad: Empresa

### Descripción

La entidad **Empresa** representa la organización responsable de publicar una o más ofertas de empleo procesadas por la automatización.

Cada registro corresponde a una empresa identificada a partir de la información obtenida desde las diferentes fuentes de empleo.

---

### Propósito

Su propósito es centralizar la información de las empresas, evitando duplicidad de datos cuando una misma organización publique múltiples ofertas o utilice diferentes fuentes de reclutamiento.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la empresa. |
| nombre | Texto | Sí | Nombre oficial de la empresa. |
| nombre_normalizado | Texto | Sí | Nombre estandarizado utilizado para evitar duplicidades. |
| sitio_web | Texto | No | Sitio web oficial de la empresa. |
| linkedin | Texto | No | URL del perfil oficial de LinkedIn de la empresa. |
| sector | Catálogo | No | Sector económico al que pertenece la empresa. |
| tamaño | Catálogo | No | Clasificación del tamaño de la empresa. |
| descripcion | Texto largo | No | Descripción general de la empresa. |
| observaciones | Texto largo | No | Información adicional relevante sobre la empresa. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- sector → Catálogo
- tamaño → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Publica | 1 : N |

---

### Restricciones

- El nombre normalizado deberá utilizarse para minimizar la creación de empresas duplicadas.
- Una empresa podrá estar asociada a múltiples ofertas.
- Una empresa podrá aparecer en múltiples fuentes diferentes sin generar registros duplicados.
- Los valores de sector y tamaño deberán corresponder a los catálogos oficiales cuando sean utilizados.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Empresa** representa únicamente la organización que ofrece la vacante.

No almacena información específica de una oferta de empleo, ya que esa información pertenece a la entidad **Oferta**.

Una misma empresa podrá publicar múltiples ofertas en diferentes momentos y a través de diferentes fuentes, manteniendo siempre un único registro dentro del modelo de datos.

---

## 2.4. Entidad: Ubicación

### Descripción

La entidad **Ubicación** representa la localización geográfica asociada a una oferta de empleo.

Su propósito es almacenar la información de ubicación de forma normalizada, evitando la duplicidad de datos cuando múltiples ofertas compartan el mismo lugar.

---

### Propósito

Centralizar la información geográfica de las ofertas de empleo para facilitar su consulta, filtrado, análisis y reutilización dentro de la automatización.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la ubicación. |
| pais | Texto | Sí | País donde se ofrece la vacante. |
| estado_provincia | Texto | No | Estado, provincia o departamento. |
| ciudad | Texto | No | Ciudad de la vacante. |
| direccion | Texto | No | Dirección específica cuando esté disponible. |
| modalidad | Catálogo | Sí | Modalidad de trabajo asociada a la ubicación (presencial, remoto, híbrido, etc.). |
| tipo_ubicacion | Catálogo | Sí | Clasificación de la ubicación de la oferta. |
| observaciones | Texto largo | No | Información adicional relacionada con la ubicación. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- modalidad → Catálogo
- tipo_ubicacion → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Es utilizada por | 1 : N |

---

### Restricciones

- Toda ubicación deberá indicar al menos el país.
- La modalidad deberá corresponder a un valor definido en el catálogo oficial.
- El tipo de ubicación deberá corresponder a un valor definido en el catálogo oficial.
- Las coordenadas geográficas solo podrán almacenarse cuando la información esté disponible y sea consistente con la ubicación registrada.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Ubicación** representa únicamente la localización asociada a una oferta de empleo.

La modalidad de trabajo se incorpora en esta entidad por estar directamente relacionada con la forma en que se desempeña la vacante (presencial, remoto, híbrido, etc.), permitiendo reutilizar ubicaciones comunes entre diferentes ofertas y evitando duplicidad de información.

---

## 2.5. Entidad: Oferta Procesada

### Descripción

La entidad **Oferta Procesada** representa la versión estructurada, normalizada y enriquecida de una oferta de empleo después de haber sido procesada por la automatización.

Su contenido es el resultado de interpretar la información original de la entidad **Oferta**, permitiendo que las etapas posteriores trabajen con datos organizados y consistentes.

---

### Propósito

Almacenar la información procesada de una oferta para facilitar su evaluación, comparación, generación de documentos y toma de decisiones, preservando al mismo tiempo la oferta original sin modificaciones.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la oferta procesada. |
| oferta_id | UUID | Sí | Referencia a la oferta original. |
| cargo_normalizado | Texto | Sí | Nombre normalizado del cargo identificado. |
| descripcion_procesada | Texto largo | Sí | Descripción estructurada de la oferta. |
| resumen | Texto largo | No | Resumen generado del contenido de la oferta. |
| habilidades_tecnicas | Texto largo | No | Relación de habilidades técnicas identificadas. |
| habilidades_blandas | Texto largo | No | Relación de habilidades blandas identificadas. |
| tecnologias | Texto largo | No | Tecnologías identificadas durante el procesamiento. |
| nivel_experiencia | Catálogo | No | Nivel de experiencia requerido. |
| nivel_educativo | Catálogo | No | Nivel educativo identificado. |
| tipo_contrato | Catálogo | No | Tipo de contratación identificado. |
| modalidad_trabajo | Catálogo | No | Modalidad de trabajo identificada. |
| rango_salarial | Texto | No | Información salarial normalizada cuando exista. |
| idiomas | Texto largo | No | Idiomas requeridos o deseables identificados. |
| beneficios | Texto largo | No | Beneficios identificados en la oferta. |
| requisitos | Texto largo | No | Requisitos principales extraídos de la oferta. |
| responsabilidades | Texto largo | No | Responsabilidades principales identificadas. |
| fecha_procesamiento | Fecha/Hora | Sí | Fecha y hora en que finalizó el procesamiento. |
| version_procesamiento | Texto | Sí | Versión del proceso de procesamiento utilizada. |
| observaciones | Texto largo | No | Información adicional relevante sobre el procesamiento. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- oferta_id

---

### Claves foráneas

- oferta_id → Oferta
- nivel_experiencia → Catálogo
- nivel_educativo → Catálogo
- tipo_contrato → Catálogo
- modalidad_trabajo → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Es generada a partir de | 1 : 1 |
| Evaluación Inicial | Es utilizada por | 1 : 1 |
| Evaluación Detallada | Es utilizada por | 1 : 0..1 |
| Documento Generado | Sirve como insumo para | 1 : N |

---

### Restricciones

- Toda oferta procesada deberá estar asociada a una única oferta original.
- No podrá existir más de una oferta procesada para la misma oferta.
- La información procesada no deberá reemplazar ni modificar el contenido original almacenado en la entidad **Oferta**.
- Los valores clasificados mediante catálogos deberán corresponder a los valores oficiales definidos para el proyecto.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Oferta Procesada** constituye la representación estructurada de una oferta de empleo y actúa como base para las etapas posteriores de evaluación y generación documental.

Su existencia permite preservar la información original obtenida durante el descubrimiento mientras se dispone de una versión optimizada para el procesamiento interno de la automatización.

---

## 2.6. Entidad: Evaluación Inicial

### Descripción

La entidad **Evaluación Inicial** representa el resultado de la primera evaluación realizada sobre una oferta procesada.

Su finalidad es determinar, mediante criterios previamente definidos por el proyecto, si una oferta debe continuar hacia la evaluación detallada o ser descartada.

---

### Propósito

Registrar el resultado de la evaluación inicial de cada oferta, preservando la información utilizada para la toma de decisiones y permitiendo la trazabilidad del proceso de filtrado.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la evaluación inicial. |
| oferta_procesada_id | UUID | Sí | Referencia a la oferta procesada evaluada. |
| resultado | Catálogo | Sí | Resultado obtenido en la evaluación inicial. |
| puntaje | Decimal | Sí | Puntaje total obtenido durante la evaluación inicial. |
| umbral_aprobacion | Decimal | Sí | Puntaje mínimo requerido para superar la evaluación. |
| decision | Catálogo | Sí | Decisión generada a partir del resultado de la evaluación. |
| justificacion | Texto largo | Sí | Justificación de la decisión tomada. |
| criterios_evaluados | Texto largo | Sí | Resumen de los criterios aplicados durante la evaluación. |
| observaciones | Texto largo | No | Información adicional relevante sobre la evaluación. |
| fecha_evaluacion | Fecha/Hora | Sí | Fecha y hora en que se realizó la evaluación. |
| version_modelo | Texto | Sí | Versión del modelo, reglas o configuración utilizada para realizar la evaluación. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- oferta_procesada_id

---

### Claves foráneas

- oferta_procesada_id → Oferta Procesada
- resultado → Catálogo
- decision → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta Procesada | Evalúa | 1 : 1 |
| Evaluación Detallada | Puede generar | 1 : 0..1 |
| Decisión | Registra | 1 : N |
| Evento | Registra | 1 : N |

---

### Restricciones

- Toda evaluación inicial deberá estar asociada a una única oferta procesada.
- No podrá existir más de una evaluación inicial para la misma oferta procesada.
- El resultado deberá corresponder a un valor definido en el catálogo oficial.
- La decisión deberá corresponder al resultado obtenido durante la evaluación.
- La evaluación deberá conservar el puntaje, el umbral y la justificación utilizados para la toma de decisión.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Evaluación Inicial** representa el primer filtro objetivo de la automatización.

Su resultado determina si una oferta continúa hacia la etapa de evaluación detallada o finaliza su procesamiento, manteniendo siempre la trazabilidad de la decisión tomada y de la información utilizada para respaldarla.

---

## 2.7. Entidad: Evaluación Detallada

### Descripción

La entidad **Evaluación Detallada** representa el resultado del diagnóstico profundo realizado sobre una oferta de empleo que superó la evaluación inicial.

Su contenido corresponde a la información generada durante la **Fase 1 – Diagnóstico de la vacante para la construcción de la cover letter**, documentando de manera estructurada el análisis realizado sobre la oferta y el nivel de ajuste entre las necesidades de la organización y el perfil profesional del usuario. :contentReference[oaicite:0]{index=0}

---

### Propósito

Registrar de forma estructurada todos los resultados obtenidos durante el diagnóstico profundo de una oferta de empleo, permitiendo conservar la trazabilidad del análisis y proporcionando los insumos necesarios para las fases posteriores de generación documental y postulación. :contentReference[oaicite:1]{index=1}

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la evaluación detallada. |
| oferta_procesada_id | UUID | Sí | Referencia a la oferta procesada evaluada. |
| resultado_organizacional | Texto largo | Sí | Resultado organizacional principal y resultados secundarios identificados durante el diagnóstico. |
| problema_organizacional | Texto largo | Sí | Problema organizacional principal, problemas explícitos, problemas inferidos y aspectos no determinables identificados. |
| perfil_profesional_requerido | Texto largo | Sí | Capacidades críticas, forma de pensar, experiencias y competencias requeridas para la posición. |
| coincidencias_perfil | Texto largo | Sí | Evidencias principales y complementarias que demuestran la coincidencia entre el perfil del usuario y la vacante. |
| logica_xyz | Texto largo | Sí | Lógica X → Y → Z construida durante el diagnóstico. |
| hipotesis_valor | Texto largo | Sí | Hipótesis de valor formulada para sustentar la candidatura. |
| informacion_descartada | Texto largo | No | Información del perfil profesional que se determinó que no aporta valor para esta vacante. |
| ajuste_tecnico | Decimal | Sí | Calificación del ajuste técnico (0 a 10). |
| justificacion_ajuste_tecnico | Texto largo | Sí | Justificación del ajuste técnico obtenida durante la evaluación. |
| ajuste_funcional | Decimal | Sí | Calificación del ajuste funcional (0 a 10). |
| justificacion_ajuste_funcional | Texto largo | Sí | Justificación del ajuste funcional obtenida durante la evaluación. |
| ajuste_estrategico | Decimal | Sí | Calificación del ajuste estratégico (0 a 10). |
| justificacion_ajuste_estrategico | Texto largo | Sí | Justificación del ajuste estratégico obtenida durante la evaluación. |
| riesgo_sobrecalificacion | Catálogo | Sí | Nivel de riesgo de sobrecalificación (Bajo, Medio o Alto). |
| justificacion_riesgo | Texto largo | Sí | Justificación del nivel de riesgo de sobrecalificación asignado. |
| recomendacion_final | Catálogo | Sí | Recomendación final sobre la conveniencia de aplicar (Aplicar, Aplicar con reservas o No aplicar). |
| justificacion_recomendacion | Texto largo | Sí | Justificación de la recomendación final. |
| insumos_cover_letter | Texto largo | Sí | Resumen de los insumos estratégicos que servirán como entrada para la siguiente fase de construcción de la cover letter. |
| fecha_evaluacion | Fecha/Hora | Sí | Fecha y hora en que finalizó la evaluación. |
| version_metodologia | Texto | Sí | Versión de la metodología utilizada para realizar el diagnóstico. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- oferta_procesada_id

---

### Claves foráneas

- oferta_procesada_id → Oferta Procesada
- riesgo_sobrecalificacion → Catálogo
- recomendacion_final → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta Procesada | Evalúa | 1 : 1 |
| Documento Generado | Proporciona los insumos para | 1 : N |
| Postulación | Puede originar | 1 : 0..1 |
| Decisión | Registra | 1 : N |
| Evento | Registra | 1 : N |

---

### Restricciones

- Toda evaluación detallada deberá estar asociada a una única oferta procesada.
- No podrá existir más de una evaluación detallada para la misma oferta procesada.
- Solo podrán someterse a evaluación detallada las ofertas que hayan superado la evaluación inicial.
- Las calificaciones de ajuste deberán utilizar una escala de 0 a 10.
- El riesgo de sobrecalificación deberá corresponder a uno de los valores definidos en el catálogo oficial.
- La recomendación final deberá corresponder a uno de los valores definidos en el catálogo oficial.
- Toda conclusión registrada deberá mantener trazabilidad con la evidencia obtenida de la oferta laboral, la hoja de vida y el portafolio profesional. :contentReference[oaicite:2]{index=2}

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Evaluación Detallada** almacena el resultado completo del diagnóstico profundo de una oferta de empleo.

Su estructura reproduce los entregables definidos para la **Fase 1 – Diagnóstico de la vacante para la construcción de la cover letter**, permitiendo que las fases posteriores de la automatización consuman directamente esta información sin necesidad de reconstruir el análisis realizado. :contentReference[oaicite:3]{index=3}

---

## 2.8. Entidad: Documento Generado

### Descripción

La entidad **Documento Generado** representa cada documento producido automáticamente por la automatización como resultado del procesamiento y evaluación de una oferta de empleo.

Cada registro corresponde a un documento específico generado para una oferta determinada, conservando la información necesaria para su trazabilidad, gestión y reutilización.

---

### Propósito

Almacenar la información de todos los documentos generados por la automatización, permitiendo controlar su ciclo de vida, mantener el historial de versiones y facilitar su consulta posterior.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único del documento generado. |
| oferta_id | UUID | Sí | Referencia a la oferta para la cual fue generado el documento. |
| evaluacion_detallada_id | UUID | Sí | Referencia a la evaluación detallada utilizada como base para la generación del documento. |
| tipo_documento | Catálogo | Sí | Tipo de documento generado (Cover Letter, Hoja de Vida, etc.). |
| nombre_documento | Texto | Sí | Nombre asignado al documento. |
| version | Texto | Sí | Versión del documento generado. |
| contenido | Texto largo | Sí | Contenido completo del documento generado. |
| formato | Catálogo | Sí | Formato del documento (Markdown, PDF, DOCX, etc.). |
| estado | Catálogo | Sí | Estado actual del documento. |
| fecha_generacion | Fecha/Hora | Sí | Fecha y hora de generación del documento. |
| fecha_ultima_modificacion | Fecha/Hora | No | Fecha y hora de la última modificación del documento, cuando aplique. |
| observaciones | Texto largo | No | Información adicional relevante sobre el documento. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- oferta_id → Oferta
- evaluacion_detallada_id → Evaluación Detallada
- tipo_documento → Catálogo
- formato → Catálogo
- estado → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Es generado para | N : 1 |
| Evaluación Detallada | Se basa en | N : 1 |
| Postulación | Puede ser utilizado en | 1 : N |

---

### Restricciones

- Todo documento generado deberá estar asociado a una única oferta.
- Todo documento generado deberá basarse en una evaluación detallada previamente finalizada.
- El tipo de documento deberá corresponder a un valor definido en el catálogo oficial.
- El formato deberá corresponder a un valor definido en el catálogo oficial.
- El estado deberá corresponder a un valor definido en el catálogo oficial.
- Cada versión del documento deberá conservar su trazabilidad.

---

### Máquina de estados

La entidad seguirá la máquina de estados oficial definida para la gestión documental de la automatización.

La especificación detallada de dicha máquina de estados será documentada en el apartado correspondiente de este documento.

---

### Observaciones

La entidad **Documento Generado** permite gestionar todos los documentos producidos por la automatización de forma independiente de su tipo.

Esta aproximación facilita incorporar nuevos tipos de documentos en el futuro sin necesidad de modificar la estructura del modelo de datos, preservando la escalabilidad y la mantenibilidad del sistema.

---

## 2.9. Entidad: Postulación

### Descripción

La entidad **Postulación** representa el proceso mediante el cual el usuario aplica a una oferta de empleo utilizando los documentos generados por la automatización.

Cada registro corresponde a una única postulación realizada o planificada para una oferta específica.

---

### Propósito

Registrar y gestionar el ciclo de vida completo de cada postulación, permitiendo mantener la trazabilidad desde la oferta de empleo hasta el resultado final del proceso de selección.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la postulación. |
| oferta_id | UUID | Sí | Referencia a la oferta a la cual se realiza la postulación. |
| documento_principal_id | UUID | Sí | Documento principal utilizado para la postulación. |
| fecha_postulacion | Fecha/Hora | No | Fecha y hora en que se realizó la postulación. |
| canal_postulacion | Catálogo | Sí | Medio utilizado para realizar la postulación. |
| estado | Catálogo | Sí | Estado actual de la postulación. |
| respuesta_empresa | Texto largo | No | Respuesta recibida por parte de la empresa, cuando exista. |
| fecha_respuesta | Fecha/Hora | No | Fecha y hora de la respuesta de la empresa. |
| siguiente_accion | Texto | No | Próxima acción prevista dentro del proceso de selección. |
| fecha_siguiente_accion | Fecha/Hora | No | Fecha programada para la siguiente acción. |
| observaciones | Texto largo | No | Información adicional relevante sobre la postulación. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- oferta_id → Oferta
- documento_principal_id → Documento Generado
- canal_postulacion → Catálogo
- estado → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Corresponde a | N : 1 |
| Documento Generado | Utiliza | N : 1 |
| Evento | Registra | 1 : N |
| Decisión | Puede registrar | 1 : N |

---

### Restricciones

- Toda postulación deberá estar asociada a una única oferta.
- Toda postulación deberá utilizar al menos un documento generado por la automatización.
- El canal de postulación deberá corresponder a un valor definido en el catálogo oficial.
- El estado deberá corresponder a un valor definido en el catálogo oficial.
- Toda modificación del estado de la postulación deberá conservar su trazabilidad.

---

### Máquina de estados

La entidad seguirá la máquina de estados oficial definida para el proceso de postulación.

La especificación detallada de dicha máquina de estados será documentada en el apartado correspondiente de este documento.

---

### Observaciones

La entidad **Postulación** representa el seguimiento completo del proceso de aplicación a una oferta de empleo.

Su objetivo no es almacenar únicamente la fecha de envío de la candidatura, sino registrar la evolución completa de la postulación hasta su cierre, permitiendo mantener la trazabilidad de todas las acciones y decisiones relacionadas con el proceso de selección.

---

## 2.10. Entidad: Evento

### Descripción

La entidad **Evento** representa cada hecho relevante ocurrido durante la ejecución de la automatización.

Un evento corresponde a una acción, cambio de estado, ejecución de un proceso o cualquier otra ocurrencia que deba conservarse para efectos de trazabilidad, auditoría y diagnóstico del sistema.

---

### Propósito

Registrar cronológicamente los eventos generados por la automatización, permitiendo reconstruir el historial completo de procesamiento de una oferta y facilitar el análisis de incidentes, errores y decisiones.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único del evento. |
| oferta_id | UUID | Sí | Referencia a la oferta relacionada con el evento. |
| tipo_evento | Catálogo | Sí | Tipo de evento registrado. |
| entidad_afectada | Texto | Sí | Nombre de la entidad sobre la cual ocurrió el evento. |
| entidad_id | UUID | Sí | Identificador del registro afectado por el evento. |
| accion | Catálogo | Sí | Acción ejecutada (creación, actualización, eliminación, evaluación, generación, etc.). |
| descripcion | Texto largo | Sí | Descripción detallada del evento. |
| resultado | Catálogo | Sí | Resultado de la operación asociada al evento. |
| origen | Catálogo | Sí | Componente de la automatización que generó el evento. |
| contexto | Texto largo | No | Información adicional útil para comprender el evento. |
| fecha_evento | Fecha/Hora | Sí | Fecha y hora en que ocurrió el evento. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- oferta_id → Oferta
- tipo_evento → Catálogo
- accion → Catálogo
- resultado → Catálogo
- origen → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Registra eventos de | N : 1 |
| Decisión | Puede estar asociado a | N : 0..1 |
| Postulación | Puede registrar eventos de | N : 0..1 |

---

### Restricciones

- Todo evento deberá estar asociado a una oferta.
- Todo evento deberá registrar el momento exacto en que ocurrió.
- El tipo de evento, la acción, el resultado y el origen deberán corresponder a valores definidos en los catálogos oficiales.
- Los eventos no podrán eliminarse una vez registrados.
- Los eventos deberán conservarse para garantizar la trazabilidad del sistema.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Evento** constituye el historial cronológico de la automatización.

Su finalidad es proporcionar trazabilidad completa sobre el funcionamiento del sistema, permitiendo reconstruir qué ocurrió, cuándo ocurrió, sobre qué elemento ocurrió y cuál fue el resultado de cada proceso ejecutado.

---

## 2.11. Entidad: Decisión

### Descripción

La entidad **Decisión** representa cada decisión tomada por la automatización durante el procesamiento de una oferta de empleo.

Una decisión corresponde a la conclusión obtenida después de aplicar reglas de negocio, criterios de evaluación o procesos de análisis, determinando el curso de acción que seguirá la automatización.

---

### Propósito

Registrar de forma estructurada todas las decisiones relevantes tomadas por la automatización, preservando la trazabilidad del razonamiento utilizado y permitiendo reconstruir posteriormente por qué una determinada acción fue ejecutada.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único de la decisión. |
| oferta_id | UUID | Sí | Referencia a la oferta relacionada con la decisión. |
| etapa | Catálogo | Sí | Etapa del proceso en la que se tomó la decisión. |
| tipo_decision | Catálogo | Sí | Clasificación de la decisión tomada. |
| decision | Texto | Sí | Decisión adoptada por la automatización. |
| justificacion | Texto largo | Sí | Explicación que sustenta la decisión tomada. |
| evidencia | Texto largo | Sí | Evidencia utilizada para respaldar la decisión. |
| confianza | Decimal | No | Nivel de confianza asociado a la decisión, cuando aplique. |
| componente_origen | Catálogo | Sí | Componente de la automatización que generó la decisión. |
| fecha_decision | Fecha/Hora | Sí | Fecha y hora en que se tomó la decisión. |
| observaciones | Texto largo | No | Información adicional relevante sobre la decisión. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- Ninguna.

---

### Claves foráneas

- oferta_id → Oferta
- etapa → Catálogo
- tipo_decision → Catálogo
- componente_origen → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Registra decisiones de | N : 1 |
| Evento | Puede originar | 1 : N |
| Evaluación Inicial | Puede estar asociada a | N : 0..1 |
| Evaluación Detallada | Puede estar asociada a | N : 0..1 |
| Postulación | Puede influir en | N : 0..1 |

---

### Restricciones

- Toda decisión deberá estar asociada a una oferta.
- Toda decisión deberá registrar la justificación correspondiente.
- Toda decisión deberá conservar la evidencia utilizada para respaldarla.
- La etapa, el tipo de decisión y el componente de origen deberán corresponder a valores definidos en los catálogos oficiales.
- Las decisiones no podrán eliminarse una vez registradas, con el fin de preservar la trazabilidad del proceso.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Decisión** constituye el registro formal de las decisiones tomadas por la automatización.

Su objetivo es preservar el razonamiento utilizado durante el procesamiento de una oferta, permitiendo comprender posteriormente qué decisión se tomó, por qué se tomó, con qué evidencia se sustentó y en qué etapa del proceso ocurrió.

---

## 2.12. Entidad: Configuración

### Descripción

La entidad **Configuración** representa los parámetros utilizados por la automatización para controlar su comportamiento durante la ejecución.

Cada registro corresponde a un parámetro configurable que influye en el funcionamiento del sistema sin requerir modificaciones en la implementación.

---

### Propósito

Centralizar la configuración operativa de la automatización, permitiendo administrar de forma controlada los valores utilizados por los diferentes procesos del sistema.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único del parámetro de configuración. |
| categoria | Catálogo | Sí | Categoría a la que pertenece el parámetro. |
| nombre | Texto | Sí | Nombre único del parámetro de configuración. |
| descripcion | Texto largo | Sí | Descripción del propósito del parámetro. |
| valor | Texto largo | Sí | Valor asignado al parámetro. |
| tipo_dato | Catálogo | Sí | Tipo de dato esperado para el valor del parámetro. |
| valor_defecto | Texto largo | No | Valor por defecto del parámetro. |
| obligatorio | Booleano | Sí | Indica si el parámetro es obligatorio para el funcionamiento del sistema. |
| editable | Booleano | Sí | Indica si el parámetro puede modificarse sin alterar la implementación. |
| activo | Booleano | Sí | Indica si el parámetro se encuentra habilitado. |
| observaciones | Texto largo | No | Información adicional relevante sobre el parámetro. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- nombre

---

### Claves foráneas

- categoria → Catálogo
- tipo_dato → Catálogo

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Catálogo | Utiliza valores de | N : 1 |

---

### Restricciones

- El nombre del parámetro deberá ser único dentro del sistema.
- Todo parámetro deberá pertenecer a una categoría definida en el catálogo oficial.
- El tipo de dato deberá corresponder a un valor definido en el catálogo oficial.
- El valor almacenado deberá ser compatible con el tipo de dato definido.
- Los parámetros marcados como obligatorios deberán tener siempre un valor válido.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Configuración** permite desacoplar la lógica de la automatización de los valores operativos utilizados durante su ejecución.

Su utilización facilita la adaptación del sistema a nuevos escenarios sin necesidad de modificar la estructura del modelo de datos ni el código de implementación.


---


## 2.13. Entidad: Catálogo

### Descripción

La entidad **Catálogo** representa los conjuntos de valores controlados utilizados por las diferentes entidades del modelo de datos.

Su propósito es normalizar la información, evitar valores inconsistentes y facilitar el mantenimiento de listas de referencia utilizadas por la automatización.

---

### Propósito

Centralizar todos los valores de referencia utilizados por el modelo de datos, garantizando uniformidad, consistencia y reutilización entre las diferentes entidades.

---

### Atributos

| Atributo | Tipo lógico | Obligatorio | Descripción |
|----------|-------------|-------------|-------------|
| id | UUID | Sí | Identificador único del registro del catálogo. |
| nombre_catalogo | Texto | Sí | Nombre del catálogo al que pertenece el registro. |
| codigo | Texto | Sí | Código único del valor dentro del catálogo. |
| nombre | Texto | Sí | Nombre visible del valor. |
| descripcion | Texto largo | No | Descripción del valor del catálogo. |
| orden | Entero | No | Orden de presentación del valor dentro del catálogo. |
| activo | Booleano | Sí | Indica si el valor puede utilizarse en la automatización. |
| observaciones | Texto largo | No | Información adicional relevante sobre el valor. |
| fecha_creacion | Fecha/Hora | Sí | Fecha y hora de creación del registro. |
| fecha_actualizacion | Fecha/Hora | Sí | Fecha y hora de la última actualización del registro. |

---

### Clave primaria

- id

---

### Claves alternativas

- nombre_catalogo + codigo

---

### Claves foráneas

No aplica.

---

### Relaciones

| Entidad relacionada | Relación | Cardinalidad |
|----------------------|----------|--------------|
| Oferta | Es utilizado por | 1 : N |
| Fuente | Es utilizado por | 1 : N |
| Empresa | Es utilizado por | 1 : N |
| Ubicación | Es utilizado por | 1 : N |
| Oferta Procesada | Es utilizado por | 1 : N |
| Evaluación Inicial | Es utilizado por | 1 : N |
| Evaluación Detallada | Es utilizado por | 1 : N |
| Documento Generado | Es utilizado por | 1 : N |
| Postulación | Es utilizado por | 1 : N |
| Evento | Es utilizado por | 1 : N |
| Decisión | Es utilizado por | 1 : N |
| Configuración | Es utilizado por | 1 : N |

---

### Restricciones

- Cada combinación **nombre_catalogo + codigo** deberá ser única.
- Un valor inactivo no podrá utilizarse en nuevos registros.
- Los códigos deberán mantenerse estables para preservar la compatibilidad del modelo de datos.
- La eliminación física de valores utilizados por otras entidades no estará permitida.

---

### Máquina de estados

No aplica.

---

### Observaciones

La entidad **Catálogo** actúa como repositorio central de todos los valores controlados utilizados por la automatización.

Entre los catálogos que podrán administrarse mediante esta entidad se encuentran, entre otros:

- Estados de las ofertas.
- Tipos de fuente.
- Modalidades de trabajo.
- Tipos de contrato.
- Niveles de experiencia.
- Niveles educativos.
- Sectores empresariales.
- Tamaños de empresa.
- Tipos de documento.
- Estados de documentos.
- Estados de postulación.
- Tipos de evento.
- Tipos de decisión.
- Categorías de configuración.
- Cualquier otro conjunto de valores controlados incorporado durante la evolución del proyecto.

---

# 3. Catálogos y tablas de referencia

Los catálogos constituyen los conjuntos de valores controlados utilizados por el modelo de datos para garantizar la consistencia, integridad y normalización de la información almacenada.

Cada catálogo deberá administrarse de forma independiente y será utilizado mediante claves foráneas por las entidades que lo requieran.

---

## 3.1. Catálogo: Estados de la oferta

**Propósito**

Definir los estados que puede atravesar una oferta durante su ciclo de vida.

**Valores iniciales**

- Descubierta
- Preparada
- Evaluación inicial
- Aprobada para evaluación detallada
- Rechazada en evaluación inicial
- Evaluación detallada
- Aprobada para postulación
- Rechazada en evaluación detallada
- Documentación generada
- Postulada
- Cerrada
- Archivada

---

## 3.2. Catálogo: Tipos de fuente

**Propósito**

Clasificar el origen de las ofertas de empleo.

**Valores iniciales**

- Portal de empleo
- Página corporativa
- LinkedIn
- Agencia de reclutamiento
- Referido
- Otro

---

## 3.3. Catálogo: Modalidades de trabajo

**Propósito**

Clasificar la modalidad bajo la cual se desarrolla la vacante.

**Valores iniciales**

- Presencial
- Remota
- Híbrida

---

## 3.4. Catálogo: Tipos de contrato

**Propósito**

Clasificar la modalidad contractual de la vacante.

**Valores iniciales**

- Indefinido
- Término fijo
- Temporal
- Prestación de servicios
- Freelance
- Práctica
- No especificado

---

## 3.5. Catálogo: Nivel de experiencia

**Propósito**

Clasificar el nivel de experiencia requerido por la vacante.

**Valores iniciales**

- Sin experiencia
- Junior
- Semi Senior
- Senior
- Líder
- Gerencial
- No especificado

---

## 3.6. Catálogo: Nivel educativo

**Propósito**

Clasificar el nivel académico requerido por la vacante.

**Valores iniciales**

- Bachiller
- Técnico
- Tecnólogo
- Profesional
- Especialización
- Maestría
- Doctorado
- No especificado

---

## 3.7. Catálogo: Sectores empresariales

**Propósito**

Clasificar el sector económico de las empresas.

**Valores iniciales**

- Tecnología
- Manufactura
- Salud
- Educación
- Financiero
- Retail
- Consultoría
- Gobierno
- Otro

---

## 3.8. Catálogo: Tamaño de empresa

**Propósito**

Clasificar el tamaño de la organización.

**Valores iniciales**

- Microempresa
- Pequeña
- Mediana
- Grande
- Multinacional
- No especificado

---

## 3.9. Catálogo: Tipos de documento

**Propósito**

Clasificar los documentos generados por la automatización.

**Valores iniciales**

- Cover Letter
- Hoja de Vida
- Correo de postulación
- Documento de apoyo
- Otro

---

## 3.10. Catálogo: Estados del documento

**Propósito**

Controlar el ciclo de vida de los documentos generados.

**Valores iniciales**

- Generado
- Revisado
- Aprobado
- Utilizado
- Archivado

---

## 3.11. Catálogo: Canales de postulación

**Propósito**

Clasificar el medio utilizado para realizar una postulación.

**Valores iniciales**

- Portal de empleo
- Página corporativa
- LinkedIn
- Correo electrónico
- Otro

---

## 3.12. Catálogo: Estados de la postulación

**Propósito**

Registrar la evolución del proceso de postulación.

**Valores iniciales**

- Pendiente
- Enviada
- En revisión
- Entrevista
- Prueba técnica
- Oferta recibida
- Rechazada
- Retirada
- Finalizada

---

## 3.13. Catálogo: Tipos de evento

**Propósito**

Clasificar los eventos registrados por la automatización.

**Valores iniciales**

- Descubrimiento
- Procesamiento
- Evaluación
- Generación documental
- Postulación
- Actualización
- Error
- Advertencia
- Información

---

## 3.14. Catálogo: Tipos de decisión

**Propósito**

Clasificar las decisiones tomadas durante la ejecución de la automatización.

**Valores iniciales**

- Aprobación
- Rechazo
- Continuar procesamiento
- Detener procesamiento
- Generar documento
- Postular
- Archivar

---

## 3.15. Catálogo: Riesgo de sobrecalificación

**Propósito**

Clasificar el riesgo de sobrecalificación identificado durante la evaluación detallada.

**Valores iniciales**

- Bajo
- Medio
- Alto

---

## 3.16. Catálogo: Recomendación final

**Propósito**

Registrar la recomendación final obtenida durante la evaluación detallada.

**Valores iniciales**

- Aplicar
- Aplicar con reservas
- No aplicar

---

# 4. Modelo Lógico de Datos

El Modelo Lógico de Datos define la estructura lógica de la información administrada por la automatización, estableciendo las entidades, sus relaciones y las reglas de organización de los datos, independientemente de la tecnología utilizada para su implementación.

---

## 4.1. Entidades principales

Las entidades principales del modelo son:

- Oferta
- Fuente
- Empresa
- Ubicación
- Oferta Procesada
- Evaluación Inicial
- Evaluación Detallada
- Documento Generado
- Postulación
- Evento
- Decisión
- Configuración
- Catálogo

---

## 4.2. Relaciones principales

### Oferta

- Una **Fuente** puede contener muchas **Ofertas**.
- Una **Empresa** puede publicar muchas **Ofertas**.
- Una **Ubicación** puede estar asociada a muchas **Ofertas**.
- Una **Oferta** genera una única **Oferta Procesada**.
- Una **Oferta** puede generar muchos **Eventos**.
- Una **Oferta** puede generar muchas **Decisiones**.
- Una **Oferta** puede tener una única **Postulación**.

---

### Oferta Procesada

- Una **Oferta Procesada** posee una única **Evaluación Inicial**.
- Una **Oferta Procesada** puede poseer una única **Evaluación Detallada**.

---

### Evaluación Detallada

- Una **Evaluación Detallada** puede generar múltiples **Documentos Generados**.

---

### Documento Generado

- Una **Postulación** utiliza uno o más **Documentos Generados**.

---

### Catálogo

La entidad **Catálogo** proporciona valores controlados para las diferentes entidades del modelo.

---

## 4.3. Cardinalidades

| Relación | Cardinalidad |
|----------|--------------|
| Fuente → Oferta | 1 : N |
| Empresa → Oferta | 1 : N |
| Ubicación → Oferta | 1 : N |
| Oferta → Oferta Procesada | 1 : 1 |
| Oferta Procesada → Evaluación Inicial | 1 : 1 |
| Oferta Procesada → Evaluación Detallada | 1 : 0..1 |
| Evaluación Detallada → Documento Generado | 1 : N |
| Oferta → Evento | 1 : N |
| Oferta → Decisión | 1 : N |
| Oferta → Postulación | 1 : 0..1 |
| Documento Generado → Postulación | 1 : N |

---

## 4.4. Flujo lógico del modelo

El flujo principal de la información dentro del modelo de datos sigue la siguiente secuencia:

**Fuente**
→ **Oferta**
→ **Oferta Procesada**
→ **Evaluación Inicial**
→ **Evaluación Detallada**
→ **Documento Generado**
→ **Postulación**

Durante todo el proceso, las entidades **Evento** y **Decisión** registran la trazabilidad de las operaciones realizadas, mientras que **Catálogo** y **Configuración** proporcionan la información de soporte necesaria para el funcionamiento de la automatización.

---

## 4.5. Integridad del modelo

El Modelo Lógico de Datos deberá garantizar que:

- Todas las relaciones mantengan integridad referencial.
- No existan entidades huérfanas.
- Toda entidad principal pueda trazarse hasta la oferta que le dio origen.
- La información original de la oferta permanezca inalterada durante todo el procesamiento.
- La trazabilidad del procesamiento pueda reconstruirse completamente a partir de las relaciones entre entidades.

---

## 4.6. Evolución del modelo

Toda modificación del Modelo Lógico de Datos deberá:

- Mantener compatibilidad con las versiones oficiales del proyecto.
- Actualizar el Diccionario Oficial de Datos.
- Actualizar el Diagrama Entidad–Relación (ERD).
- Mantener la consistencia con la arquitectura definida en el Documento 13.

---

# 5. Diccionario Oficial de Datos

El Diccionario Oficial de Datos constituye la referencia técnica oficial del modelo de datos de la automatización.

Su propósito es documentar de forma estructurada todos los atributos definidos para cada entidad, proporcionando una especificación única, consistente y trazable de la información administrada por el sistema.

Cada atributo deberá documentarse utilizando la siguiente estructura.

---

## 5.1. Estructura del diccionario

Cada atributo deberá registrar, como mínimo, la siguiente información:

| Campo | Descripción |
|--------|-------------|
| Entidad | Entidad a la que pertenece el atributo. |
| Atributo | Nombre oficial del atributo. |
| Descripción | Propósito del atributo dentro del modelo de datos. |
| Tipo lógico | Tipo de dato definido para el modelo lógico. |
| Obligatorio | Indica si el atributo admite valores nulos. |
| Clave primaria | Indica si el atributo forma parte de la clave primaria. |
| Clave alternativa | Indica si el atributo pertenece a una clave alternativa. |
| Clave foránea | Indica la entidad referenciada cuando corresponda. |
| Valor por defecto | Valor asignado automáticamente cuando aplique. |
| Dominio | Conjunto de valores permitidos o catálogo asociado. |
| Restricciones | Reglas de integridad aplicables al atributo. |
| Sensibilidad | Clasificación de sensibilidad de la información. |
| Persistencia | Indica si el dato es permanente, histórico o temporal. |
| Observaciones | Información adicional relevante para la implementación. |

---

## 5.2. Cobertura

El Diccionario Oficial de Datos deberá incluir la totalidad de los atributos pertenecientes a las siguientes entidades:

- Oferta.
- Fuente.
- Empresa.
- Ubicación.
- Oferta Procesada.
- Evaluación Inicial.
- Evaluación Detallada.
- Documento Generado.
- Postulación.
- Evento.
- Decisión.
- Configuración.
- Catálogo.

No se permitirá la existencia de atributos implementados que no se encuentren documentados en este diccionario.

---

## 5.3. Consistencia

Toda modificación realizada sobre un atributo deberá reflejarse de manera consistente en:

- La especificación de la entidad correspondiente.
- El Modelo Lógico de Datos.
- El Diagrama Entidad–Relación (ERD), cuando la modificación afecte la estructura del modelo.

El Diccionario Oficial de Datos constituirá la referencia técnica para la implementación de la base de datos.

---

## 5.4. Control de cambios

Toda incorporación, modificación o eliminación de atributos deberá actualizar el Diccionario Oficial de Datos antes de ser considerada una versión oficial del modelo de datos.

La información documentada deberá mantenerse sincronizada con el resto de la documentación técnica del proyecto.

---

# 6. Diagrama Entidad–Relación (ERD)

El Diagrama Entidad–Relación (ERD) constituye la representación gráfica oficial del Modelo Lógico de Datos definido en el presente documento.

Su propósito es visualizar de forma clara las entidades que conforman el modelo, las relaciones existentes entre ellas y las cardinalidades correspondientes, facilitando la comprensión, implementación y mantenimiento de la estructura de datos de la automatización.

---

## 6.1. Objetivo

El Diagrama Entidad–Relación deberá:

- Representar todas las entidades oficiales del modelo de datos.
- Mostrar las relaciones entre entidades.
- Representar las cardinalidades correspondientes.
- Facilitar la comprensión de la arquitectura de datos.
- Servir como apoyo para la implementación de la base de datos.

---

## 6.2. Entidades representadas

El diagrama deberá incluir, como mínimo, las siguientes entidades:

- Oferta
- Fuente
- Empresa
- Ubicación
- Oferta Procesada
- Evaluación Inicial
- Evaluación Detallada
- Documento Generado
- Postulación
- Evento
- Decisión
- Configuración
- Catálogo

---

## 6.3. Relaciones representadas

El diagrama deberá representar las relaciones oficiales definidas en el Modelo Lógico de Datos, incluyendo sus respectivas cardinalidades.

Como mínimo deberán visualizarse las relaciones entre:

- Fuente ↔ Oferta
- Empresa ↔ Oferta
- Ubicación ↔ Oferta
- Oferta ↔ Oferta Procesada
- Oferta Procesada ↔ Evaluación Inicial
- Oferta Procesada ↔ Evaluación Detallada
- Evaluación Detallada ↔ Documento Generado
- Documento Generado ↔ Postulación
- Oferta ↔ Evento
- Oferta ↔ Decisión
- Oferta ↔ Postulación
- Catálogo ↔ Entidades que utilizan valores controlados
- Configuración ↔ Componentes de la automatización

---

## 6.4. Reglas de representación

El diagrama deberá cumplir las siguientes reglas:

- Representar únicamente entidades oficiales.
- Mantener coherencia con el Modelo Lógico de Datos.
- Mantener coherencia con el Diccionario Oficial de Datos.
- Mostrar claramente las cardinalidades.
- Evitar relaciones ambiguas o duplicadas.
- Mantener una distribución que favorezca la legibilidad.

---

## 6.5. Consistencia documental

Toda modificación realizada sobre el modelo de datos deberá reflejarse de forma consistente en el Diagrama Entidad–Relación.

No se permitirá la existencia de diferencias entre:

- La especificación de las entidades.
- El Modelo Lógico de Datos.
- El Diccionario Oficial de Datos.
- El Diagrama Entidad–Relación.

Estos cuatro artefactos deberán mantenerse permanentemente sincronizados y constituirán la documentación oficial del modelo de datos del proyecto.

---

# 7. Historial de versiones

El presente documento deberá mantener un historial oficial de versiones con el fin de garantizar la trazabilidad de su evolución durante el ciclo de vida del proyecto.

Toda modificación realizada sobre el modelo de datos deberá quedar registrada antes de ser considerada una versión oficial.

---

## Historial de versiones

| Versión | Fecha | Autor | Descripción del cambio |
|----------|-------|--------|------------------------|
| 1.0 | Pendiente | Pendiente | Creación inicial del Documento 13A – Diseño Detallado del Modelo de Datos. |

---

## Reglas de versionado

Toda nueva versión deberá registrar, como mínimo:

- Número de versión.
- Fecha de publicación.
- Autor o responsable del cambio.
- Descripción resumida de las modificaciones realizadas.

Cuando una modificación afecte la estructura del modelo de datos, deberá verificarse la actualización de los siguientes artefactos:

- Inventario oficial de entidades.
- Especificación detallada de las entidades.
- Catálogos y tablas de referencia.
- Modelo Lógico de Datos.
- Diccionario Oficial de Datos.
- Diagrama Entidad–Relación (ERD).

No se considerará oficial ninguna versión del documento que presente inconsistencias entre estos componentes.
