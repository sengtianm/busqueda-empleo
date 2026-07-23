# Anexo 5B - Estándares técnicos oficiales

El presente anexo establece los estándares técnicos oficiales que deberán utilizarse de forma uniforme durante el diseño, implementación y evolución de la automatización de búsqueda de empleo.

Su propósito es convertir en especificaciones concretas las convenciones generales definidas en el Documento 5.

Toda implementación del proyecto deberá respetar los estándares definidos en este anexo.

---

# B.1. Estándar para fechas

## Formato oficial

```text
YYYY-MM-DD
```

### Ejemplo

```text
2026-07-17
```

---

# B.2. Estándar para fecha y hora

## Formato oficial

```text
YYYY-MM-DDTHH:mm:ssZ
```

Compatible con ISO 8601.

### Ejemplo

```text
2026-07-17T14:30:45Z
```

---

# B.3. Zona horaria oficial

Durante el procesamiento interno:

* Todas las fechas deberán almacenarse en UTC.

Durante la presentación al usuario:

* Las fechas podrán convertirse a la zona horaria correspondiente.

---

# B.4. Estándar para duración

Formato recomendado:

```text
PT2H35M20S
```

Compatible con ISO 8601.

Cuando el proceso únicamente requiera cálculos internos también podrá utilizar segundos como unidad base.

---

# B.5. Formato oficial para identificadores

Estructura general:

```text
<PREFIJO>-<NÚMERO>
```

Ejemplos:

```text
RF-001
RNF-014
MD-032
FD-018
PRM-005
CFG-003
```

---

# B.6. Formato oficial para versiones

Se utilizará Versionado Semántico.

Estructura:

```text
vMayor.Menor.Corrección
```

Ejemplos:

```text
v1.0.0
v1.1.0
v2.3.4
```

---

# B.7. Convención oficial para nombres JSON

Todas las claves JSON deberán utilizar:

```text
camelCase
```

Ejemplos:

```json
{
  "jobTitle": "",
  "companyName": "",
  "publicationDate": "",
  "evaluationScore": 0
}
```

---

# B.8. Convención oficial para nombres de variables

Se utilizará:

```text
camelCase
```

Ejemplos:

```text
jobOffer
evaluationScore
candidateProfile
```

---

# B.9. Convención oficial para constantes

Se utilizará:

```text
UPPER_SNAKE_CASE
```

Ejemplos:

```text
MAX_RETRIES
DEFAULT_TIMEOUT
MIN_SCORE_REQUIRED
```

---

# B.10. Convención oficial para nombres de archivos

Formato recomendado:

```text
nombre-descriptivo.extension
```

Ejemplos:

```text
modelo-de-decisiones.md
config-general.json
flujo-datos.drawio
```

Cuando sea necesario incluir versiones:

```text
nombre-descriptivo_v1.0.0.extension
```

---

# B.11. Convención oficial para carpetas

Formato recomendado:

```text
kebab-case
```

Ejemplos:

```text
project-docs
job-offers
generated-files
prompt-library
```

---

# B.12. Convención oficial para nombres de prompts

Formato:

```text
PRM-XXX Nombre descriptivo
```

Ejemplos:

```text
PRM-001 Evaluación Inicial

PRM-002 Clasificación de Oferta

PRM-003 Generación de Estrategia
```

---

# B.13. Convención oficial para nombres de documentos

Formato:

```text
Documento N - Nombre del Documento
```

Ejemplos:

```text
Documento 3 - Modelo de Decisiones

Documento 5 - Estándares del Proyecto
```

---

# B.14. Convención para archivos generados automáticamente

Formato:

```text
YYYYMMDD_HHmmss_tipo-identificador.extension
```

Ejemplos:

```text
20260717_103015_reporte.md

20260717_121540_evaluacion.json

20260717_183250_log.txt
```

---

# B.15. Convención para registros (Logs)

Formato recomendado:

```text
YYYYMMDD_HHmmss_modulo.log
```

Ejemplo:

```text
20260717_103015_evaluacion.log
```

---

# B.16. Convención para codificación de archivos

Todos los archivos de texto del proyecto deberán utilizar:

```text
UTF-8
```

---

# B.17. Convención para finales de línea

Se utilizará:

```text
LF
```

para mantener compatibilidad entre plataformas.

---

# B.18. Convención para documentos Markdown

Todos los documentos oficiales deberán utilizar:

* Extensión `.md`
* Codificación UTF-8
* Encabezados Markdown (`#`)
* Tablas Markdown
* Bloques de código con lenguaje especificado cuando corresponda.

---

# B.19. Compatibilidad

Toda excepción a los estándares definidos en este anexo deberá encontrarse documentada y aprobada antes de su utilización.

---

# B.20. Fuente oficial

El presente anexo constituye la referencia técnica oficial para todos los estándares concretos utilizados por la automatización de búsqueda de empleo.
