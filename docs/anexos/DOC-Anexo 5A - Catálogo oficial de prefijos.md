# Anexo 5A. Catálogo oficial de prefijos

El presente anexo establece el catálogo oficial de prefijos utilizados por la documentación de la automatización de búsqueda de empleo.

Su propósito es garantizar una identificación uniforme de los documentos, capítulos, principios, reglas, convenciones y demás elementos normativos del proyecto.

Este catálogo constituye la única referencia oficial para la asignación de nuevos prefijos.

---

# A.1. Principios generales

* Todo prefijo deberá ser único dentro del proyecto.
* Un prefijo únicamente podrá representar un único concepto.
* Los prefijos deberán mantenerse estables durante toda la vida del proyecto.
* Ningún documento podrá reutilizar un prefijo ya asignado a otra categoría.
* Toda incorporación de un nuevo prefijo deberá actualizar este catálogo antes de considerarse oficial.

---

# A.2. Prefijos de documentos

| Prefijo | Documento                 |
| ------- | ------------------------- |
| DOC-00  | Glosario del Proyecto     |
| DOC-01  | Requisitos Funcionales    |
| DOC-02  | Requisitos No Funcionales |
| DOC-03  | Modelo de Decisiones      |
| DOC-04  | Flujo de Datos            |
| DOC-05  | Estándares del Proyecto   |

---

# A.3. Prefijos de capítulos

| Prefijo | Significado                                        |
| ------- | -------------------------------------------------- |
| PEP     | Principios de los estándares del proyecto          |
| CEG     | Convenciones generales                             |
| CNP     | Convenciones de nomenclatura                       |
| CID     | Convenciones para identificadores                  |
| CED     | Convenciones para estados                          |
| CFH     | Convenciones para fechas y horas                   |
| CFDT    | Convenciones para formatos de datos                |
| CJS     | Convenciones para estructuras JSON                 |
| CDO     | Convenciones para documentación                    |
| CPR     | Convenciones para prompts                          |
| CNA     | Convenciones para nombres de archivos y documentos |
| COC     | Convenciones para organización de carpetas         |
| CVE     | Convenciones para versionado                       |
| CLR     | Convenciones para registros (Logs)                 |
| CAT     | Convenciones para auditoría y trazabilidad         |
| CEM     | Convenciones para entidades y modelos de datos     |
| CMC     | Convenciones para módulos y componentes            |
| CCS     | Convenciones para configuración del sistema        |
| RES     | Restricciones de los estándares                    |
| CAE     | Criterios de aceptación                            |

---

# A.4. Prefijos de requisitos

| Prefijo | Significado            |
| ------- | ---------------------- |
| RF      | Requisito Funcional    |
| RNF     | Requisito No Funcional |

---

# A.5. Prefijos de decisiones

| Prefijo | Significado                    |
| ------- | ------------------------------ |
| MD      | Regla del Modelo de Decisiones |

---

# A.6. Prefijos de flujo de datos

| Prefijo | Significado              |
| ------- | ------------------------ |
| FD      | Regla del Flujo de Datos |

---

# A.7. Prefijos de procesos

| Prefijo | Significado |
| ------- | ----------- |
| PRC     | Proceso     |
| ETP     | Etapa       |
| SUB     | Subproceso  |

---

# A.8. Prefijos de módulos

| Prefijo | Significado |
| ------- | ----------- |
| MOD     | Módulo      |
| CMP     | Componente  |
| SRV     | Servicio    |
| INT     | Integración |

---

# A.9. Prefijos de entidades

| Prefijo | Significado |
| ------- | ----------- |
| ENT     | Entidad     |
| ATR     | Atributo    |
| REL     | Relación    |

---

# A.9b. Prefijos de IDs de datos persistentes

| Prefijo | Tabla SQLite       | Significado                  |
| ------- | ------------------ | ---------------------------- |
| FNT     | fuentes            | Fuente de oferta (LinkedIn)  |
| EMP     | empresas           | Empresa empleadora           |
| UBI     | ubicaciones        | Ubicación geográfica         |
| OFE     | ofertas            | Oferta de empleo cruda       |
| OFP     | ofertas_procesadas | Oferta procesada y limpia    |
| EVL     | evaluaciones       | Evaluación de compatibilidad |
| RSP     | resultados_procesamiento | Resultado de procesamiento profundo |

---

# A.10. Prefijos de configuración

| Prefijo | Significado         |
| ------- | ------------------- |
| CFG     | Configuración       |
| ENV     | Variable de entorno |
| PAR     | Parámetro           |

---

# A.11. Prefijos de registros

| Prefijo | Significado        |
| ------- | ------------------ |
| LOG     | Registro operativo |
| EVT     | Evento             |
| ERR     | Error              |
| WRN     | Advertencia        |
| INF     | Información        |

---

# A.12. Prefijos de prompts

| Prefijo | Significado            |
| ------- | ---------------------- |
| PRM     | Prompt                 |
| SYS     | Instrucción de sistema |
| TMP     | Plantilla de prompt    |

---

# A.13. Prefijos de archivos

| Prefijo | Significado          |
| ------- | -------------------- |
| DOC     | Documento            |
| IMG     | Imagen               |
| CFG     | Configuración        |
| DB      | Base de datos        |
| JSON    | Archivo JSON         |
| LOG     | Archivo de registros |

---

# A.14. Administración del catálogo

Toda incorporación, modificación o eliminación de un prefijo deberá cumplir las siguientes condiciones:

* No generar conflictos con prefijos existentes.
* Mantener la unicidad del catálogo.
* Actualizar este anexo antes de utilizar el nuevo prefijo.
* Documentar la justificación de la modificación correspondiente.

---

# A.15. Fuente oficial

El presente anexo constituye la única referencia oficial para la asignación y administración de prefijos utilizados por la automatización de búsqueda de empleo.

Ningún documento del proyecto podrá definir prefijos diferentes o incompatibles con los establecidos en este catálogo.
