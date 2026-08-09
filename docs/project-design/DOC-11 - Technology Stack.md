# DOC-11 – Technology Stack (Optimizado)

**Nota de consistencia**: El documento original contiene dos conflictos internos. Para optimizar sin perder información, se conservan las decisiones vigentes y se deja constancia de los elementos sustituidos o auxiliares:

1. **IA**: la estrategia oficial vigente es **cloud-primary** con fallback local configurable, según la decisión `2026-07-30 (Phase 3)`. Esto sustituye el requisito anterior de IA exclusivamente local.
2. **Persistencia**: la decisión específica de base de datos establece **SQLite** como almacenamiento oficial tras la migración del MVP. Los elementos `.xlsx`, `openpyxl` y `ONLYOFFICE` se conservan como herramientas auxiliares para hojas de cálculo, no como repositorio oficial paralelo.

---

## 1. Propósito y alcance

Este documento define la pila tecnológica oficial del proyecto de automatización de búsqueda de empleo. Establece, justifica y documenta tecnologías, herramientas, librerías, frameworks, componentes y metodologías que sirven como base tecnológica para diseño, desarrollo, pruebas, mantenimiento y evolución.

Reglas principales:

- Es la referencia oficial para seleccionar tecnologías durante todo el ciclo de vida del proyecto.
- Ningún componente tecnológico puede incorporarse sin evaluación previa según los criterios de este documento.
- Las decisiones deben ser consistentes con los Documentos 0–10, incluyendo requisitos funcionales y no funcionales, modelo de decisión, flujo de datos, estándares, manejo de errores, arquitectura de carpetas, alcance, objetivos, investigación de fuentes de empleo y perfil profesional del usuario.
- La selección prioriza: herramientas gratuitas, arquitectura práctica, mantenible y escalable, e independencia tecnológica para facilitar evolución futura.
- Este documento sirve de base para documentos posteriores de Arquitectura General del Sistema, Modelo de Datos y Desarrollo del MVP.
- Toda modificación de la pila tecnológica debe documentarse, justificarse y aprobarse formalmente antes de incorporarse, preservando trazabilidad y consistencia documental.

---

## 2. Principios oficiales de selección tecnológica

Todos los principios siguientes son obligarios y rigen evaluación, comparación, selección, reemplazo o actualización de componentes.

| ID | Principio | Descripción | Etapa | Peso |
|---|---|---|---|---|
| PST-001 | Tecnologías gratuitas | Solo se priorizan tecnologías de uso gratuito dentro del alcance definido. | Eliminatorio | — |
| PST-002 | Licenciamiento compatible | Las licencias deben permitir uso, modificación y distribución conforme a los objetivos del proyecto. | Eliminatorio | — |
| PST-003 | Madurez tecnológica | Tecnologías consolidadas y estables para uso en entornos reales. | Puntuable | 8 |
| PST-004 | Estabilidad | Historial estable y bajo riesgo de cambios disruptivos frecuentes. | Puntuable | 8 |
| PST-005 | Comunidad y ecosistema | Comunidad activa que facilite soporte, evolución y recursos técnicos. | Puntuable | 8 |
| PST-006 | Calidad de documentación | Documentación oficial completa, actualizada y suficiente. | Puntuable | 8 |
| PST-007 | Compatibilidad | Integración correcta con el resto de la pila tecnológica. | Eliminatorio | — |
| PST-008 | Modularidad | Favorecer arquitectura modular, aislamiento de responsabilidades y reutilización. | Puntuable | 7 |
| PST-009 | Escalabilidad | Permitir crecimiento funcional y técnico sin rediseños significativos. | Puntuable | 10 |
| PST-010 | Mantenibilidad | Facilitar comprensión, actualización y mantenimiento a largo plazo. | Puntuable | 10 |
| PST-011 | Rendimiento | Rendimiento adecuado para las cargas previstas. | Puntuable | 7 |
| PST-012 | Seguridad | Mecanismos que favorezcan soluciones seguras y confiables. | Eliminatorio | — |
| PST-013 | Portabilidad | Ejecución en distintos ambientes con el menor esfuerzo posible. | Puntuable | 5 |
| PST-014 | Independencia tecnológica | Evitar dependencias innecesarias de proveedores, plataformas o servicios específicos. | Puntuable | 6 |
| PST-015 | Facilidad de integración | Integración fácil con componentes internos y externos. | Eliminatorio | — |
| PST-016 | Actualización sostenible | Ciclo de evolución que permita actualizar sin afectar significativamente la estabilidad. | Puntuable | 5 |
| PST-017 | Consumo eficiente de recursos | Uso eficiente de los recursos hardware disponibles. | Puntuable | 5 |
| PST-018 | Facilidad de pruebas | Facilitar pruebas automatizadas y procesos de validación. | Puntuable | 6 |
| PST-019 | Compatibilidad con IA | Integración adecuada con modelos de lenguaje y componentes de IA, cuando aplique. | Eliminatorio si aplica | — |
| PST-020 | Compatibilidad con automatización web | Permitir automatización robusta de navegación, extracción e interacción web, cuando aplique. | Eliminatorio si aplica | — |
| PST-021 | Curva de aprendizaje | Complejidad de adopción razonable para facilitar mantenimiento futuro. | Puntuable | 2 |
| PST-022 | Riesgo de obsolescencia | Perspectivas favorables de continuidad, mantenimiento y evolución. | Puntuable | 5 |

La suma de pesos puntables es **100%**.

---

## 3. Metodología oficial de evaluación tecnológica

La evaluación debe ser objetiva, uniforme, reproducible, documentada y sin preferencias personales.

### 3.1 Etapa eliminatoria

Una tecnología debe cumplir **todos** los criterios eliminatorios. El incumplimiento de cualquiera descarta la alternativa, sin importar ventajas en otros aspectos.

Criterios eliminatorios:

- PST-001: Uso de tecnologías gratuitas.
- PST-002: Licenciamiento compatible.
- PST-007: Compatibilidad con la pila tecnológica.
- PST-012: Seguridad.
- PST-015: Facilidad de integración.
- PST-019: Compatibilidad con IA, cuando aplique.
- PST-020: Compatibilidad con automatización web, cuando aplique.

### 3.2 Etapa de puntuación

Las tecnologías que superen la etapa eliminatoria se evalúan con puntuación ponderada según los principios PST-003, PST-004, PST-005, PST-006, PST-008, PST-009, PST-010, PST-011, PST-013, PST-014, PST-016, PST-017, PST-018, PST-021 y PST-022.

### 3.3 Escala oficial de puntuación

Única escala permitida:

| Puntaje | Interpretación |
|---:|---|
| 0 | No cumple el criterio. |
| 1 | Cumplimiento muy pobre. |
| 2 | Cumplimiento pobre. |
| 3 | Cumplimiento aceptable. |
| 4 | Cumplimiento alto. |
| 5 | Cumplimiento excelente. |

### 3.4 Matriz oficial de evaluación

Toda decisión tecnológica debe respaldarse por una matriz que documente, como mínimo:

- Tecnologías evaluadas.
- Criterios eliminatorios aplicados.
- Resultado de cada criterio eliminatorio.
- Criterios puntables considerados.
- Peso asignado a cada criterio.
- Puntaje obtenido por cada alternativa en cada criterio.
- Puntaje total obtenido.
- Justificación técnica de la decisión.

### 3.5 Reglas de decisión

Una tecnología puede seleccionarse solo si simultáneamente:

1. Supera todos los criterios eliminatorios.
2. Obtiene el mayor puntaje ponderado entre las alternativas evaluadas.
3. No contradice ningún documento oficial del proyecto.
4. No incumple requisitos funcionales ni no funcionales.
5. Mantiene consistencia con la arquitectura general definida.

La selección no depende exclusivamente del puntaje final; también deben cumplirse criterios eliminatorios y reglas de decisión.

### 3.6 Reevaluación

Toda incorporación, actualización o reemplazo tecnológico debe evaluarse nuevamente con esta misma metodología y documentarse formalmente para preservar trazabilidad histórica.

---

## 4. Arquitectura tecnológica general

La arquitectura oficial organiza los componentes técnicos para cumplir objetivos, requisitos y principios del proyecto. Debe ser coherente, mantenible, escalable y desacoplada. Todo componente incorporado debe respetarla.

### 4.1 Modelo arquitectónico híbrido

La automatización adopta una arquitectura híbrida compuesta por:

1. Arquitectura modular.
2. Organización interna por capas.
3. Flujo de procesamiento secuencial.
4. Servicios compartidos.
5. Persistencia centralizada.

### 4.2 Reglas arquitectónicas

- **Modularidad**: módulos funcionales independientes, cada uno con responsabilidad única. Pueden evolucionar independientemente si respetan interfaces y contratos definidos.
- **Capas internas**: separación entre lógica de negocio, acceso a datos, integración con servicios externos, configuración e infraestructura.
- **Flujo secuencial**: cada módulo recibe una oferta en un estado dado, ejecuta solo su responsabilidad y entrega el resultado al siguiente módulo. No se permiten dependencias que alteren el orden oficial de procesamiento.
- **Servicios compartidos**: funcionalidades comunes se implementan como servicios reutilizables. Incluyen, entre otros: configuración, persistencia, gestión de estado, registro de eventos, manejo de errores, inteligencia artificial, gestión de prompts y utilidades comunes.
- **Persistencia centralizada**: toda información oficial se mantiene en una única fuente de persistencia compartida por módulos autorizados. Debe garantizar consistencia, trazabilidad e integridad durante todo el ciclo de vida. No se permiten repositorios paralelos que comprometan datos.

### 4.3 Principios permanentes de arquitectura

Modularidad, bajo acoplamiento, alta cohesión, escalabilidad, mantenibilidad, reutilización de componentes, separación de responsabilidades, consistencia de datos, trazabilidad y evolución controlada.

### 4.4 Evolución arquitectónica

Toda incorporación, reemplazo o modificación de componentes debe respetar la arquitectura definida. Cualquier cambio estructural debe documentarse, justificarse y aprobarse antes de implementarse, asegurando compatibilidad con el sistema y con la documentación oficial.

---

## 5. Decisiones oficiales de la pila tecnológica

### 5.1 Lenguaje de programación

**Alternativas evaluadas**: Python, Node.js (JavaScript/TypeScript), C#, Java y Go. Otras alternativas se descartaron por no ofrecer ventajas técnicas relevantes para los objetivos del proyecto.

**Criterios considerados**: compatibilidad con automatización web, integración con modelos de IA, ecosistema de librerías, procesamiento de datos, madurez tecnológica, comunidad y documentación, facilidad de mantenimiento, escalabilidad y compatibilidad con la arquitectura.

**Decisión oficial**: **Python 3.12**.

**Alcance**: se usará para todos los módulos funcionales, componentes compartidos, procesos de automatización, integración con IA, procesamiento de datos y demás elementos de la solución.

**Justificación**: excelente compatibilidad con automatización web; ecosistema maduro para IA; amplia disponibilidad de librerías para procesamiento de datos; buena documentación y comunidad; alta mantenibilidad; estabilidad tecnológica; compatibilidad con arquitecturas modulares; bajo riesgo de obsolescencia; cumplimiento de los criterios tecnológicos del documento.

**Regla**: otros lenguajes solo podrán incorporarse con justificación técnica documentada y aprobada según la metodología oficial.

---

### 5.2 Librerías principales

Objetivo: definir librerías centrales que aporten funcionalidad esencial y no puedan ser reemplazadas adecuadamente por la librería estándar de Python o por otra tecnología ya adoptada.

Criterios mínimos para incorporar una librería:

- Resuelve una necesidad real del proyecto.
- Aporta beneficio técnico sobre la librería estándar.
- No duplica funcionalidad ya cubierta por otra tecnología del stack.
- Posee mantenimiento activo y comunidad consolidada.
- Es estable y ampliamente usada en producción.
- Se integra correctamente con las demás tecnologías.
- Mantiene la complejidad del proyecto al mínimo.

No se incorporan dependencias solo por conveniencia, popularidad o funcionalidades que el proyecto no usará.

| Librería | Responsabilidad oficial |
|---|---|
| BeautifulSoup4 | Procesamiento y análisis de HTML obtenido durante la automatización. Interpreta la estructura DOM y facilita extracción organizada. |
| lxml | Parser oficial usado por BeautifulSoup4. Mejora rendimiento sin modificar la interfaz de trabajo. |
| Pydantic v2 | Definición, validación, serialización y deserialización de todos los modelos de datos. Toda información intercambiada entre módulos debe usar modelos Pydantic. |
| Loguru | Registro de eventos, trazabilidad y auditoría. Todo logging operacional debe usar esta librería. |
| RapidFuzz | Comparaciones aproximadas de texto y similitud de cadenas cuando puedan resolverse con algoritmos deterministas. |
| Tenacity | Políticas de reintento en operaciones con recursos externos potencialmente inestables. Centraliza la recuperación ante errores temporales. |
| httpx | Solicitudes HTTP cuando no se requiere navegador automatizado. Compatible con arquitecturas síncronas y asíncronas. |

**Librería estándar**: se usarán componentes de la librería estándar cuando sean suficientes. Se mencionan explícitamente: `pathlib`, `re`, `json`, `hashlib`, `datetime`, `time` y `sqlite3`. Otras librerías estándar pueden usarse con necesidad técnica justificada, sin que ello modifique el stack oficial.

**Librerías descartadas**: `requests`, `spaCy`, `NLTK`, `Stanza` y `jsonschema`. Solo podrán reevaluarse si surge un requisito funcional futuro que justifique su incorporación.

**Principios de uso**:

- Cada librería tiene una única responsabilidad clara.
- No se permiten dependencias que dupliquen funcionalidad existente.
- La librería estándar se prioriza siempre que cubra adecuadamente la necesidad.
- Toda nueva dependencia debe evaluarse antes de incorporarse.

---

### 5.3 Frameworks

**Alternativas evaluadas**: frameworks de Python para automatización, desarrollo web y scraping.

**Decisión oficial**: el proyecto **no adopta ningún framework** como parte del stack oficial.

**Cobertura suficiente mediante**: Python, arquitectura modular propia, librerías oficiales definidas, Playwright para automatización de navegador y Ollama como motor de inferencia de IA.

**Justificación**:

- La arquitectura definida no requiere funcionalidades provistas por frameworks.
- Un framework aumentaría complejidad sin ventaja proporcional.
- Se mantiene mayor control sobre arquitectura y evolución.
- Se reducen dependencias externas.
- Se facilitan mantenimiento y comprensión del código.

**Alcance futuro**: si surge un requisito funcional que justifique un framework, deberá pasar nuevamente por el proceso oficial de evaluación tecnológica.

---

### 5.4 Automatización de navegador

**Necesidad**: interactuar con aplicaciones web modernas con contenido dinámico, autenticación, JavaScript y cargas asíncronas.

Operaciones requeridas:

- Acceder a portales de empleo.
- Realizar búsquedas.
- Aplicar filtros.
- Navegar por resultados.
- Gestionar sesiones de usuario cuando sea necesario.
- Extraer información de ofertas.
- Descargar archivos cuando aplique.
- Obtener HTML para procesamiento posterior.

**Alternativas evaluadas**: Selenium, Playwright y Puppeteer.

**Decisión oficial**: **Playwright**.

**Justificación**: excelente compatibilidad con aplicaciones web modernas; soporte nativo para Chromium, Firefox y WebKit; gestión automática de esperas durante navegación; API moderna y mantenida activamente; excelente integración con Python; alta estabilidad en procesos prolongados; excelente documentación y amplia adopción. Selenium y Puppeteer no presentaron ventajas técnicas suficientes.

**Responsabilidades de Playwright**:

- Control del navegador.
- Navegación entre páginas.
- Interacción con elementos de interfaz.
- Gestión de sesiones.
- Obtención de contenido HTML.
- Capturas de pantalla cuando sea necesario.
- Descarga de archivos.

El procesamiento del HTML obtenido corresponde a **BeautifulSoup4** usando **lxml** como parser.

**Restricciones**:

- Toda automatización de navegador debe realizarse con Playwright.
- No se incorporarán tecnologías adicionales mientras Playwright cubra los requisitos funcionales.
- Cualquier reemplazo futuro debe pasar por evaluación tecnológica oficial.

---

### 5.5 Inteligencia artificial (LLM)

**Necesidad**: el proyecto requiere razonamiento que no puede resolverse solo con reglas deterministas o algoritmos tradicionales.

Usos previstos:

- Análisis de ofertas laborales.
- Interpretación de requisitos técnicos y funcionales.
- Extracción de información relevante.
- Evaluación de compatibilidad entre ofertas y perfil profesional.
- Generación de diagnósticos y recomendaciones.
- Redacción de documentos profesionales.
- Respuestas siguiendo instrucciones definidas mediante prompts estructurados.

#### Estrategia oficial vigente

El proyecto adopta estrategia **cloud-primary**:

- Todos los propósitos de IA se enrutan al modelo en la nube mediante **Ollama Cloud**, plan gratuito.
- El acceso se realiza a través de un proxy local.
- Existe un modelo local como fallback opcional y configurable para desarrollo o cuando la nube no esté alcanzable.

Decisión oficial `2026-07-30 (Phase 3)`:

```yaml
ai_routing:
  evaluation: cloud
  processing: cloud
```

Esta configuración sustituye el requisito de operación exclusivamente local/offline de versiones anteriores mediante fallback configurable definido en `config.yaml`.

La decisión balancea:

- Mayor calidad donde más importa, usando nube.
- Costo recurrente cero mediante plan gratuito.
- Operación simple: un solo proveedor y sin requisitos de hardware local para la ruta principal.
- Fallback local configurable para mitigar límites del plan gratuito, disponibilidad o cambios de términos.

#### Motores de inferencia

| Motor | Tecnología | Rol |
|---|---|---|
| Local | Ollama | Ejecución local de modelos. Rol oficial vigente: fallback configurable y/o uso local si el enrutamiento lo asigna. La selección original lo orientaba a tareas de alto volumen. |
| Nube | Ollama Cloud | Acceso a modelos de mayor capacidad sin hardware local. Ruta oficial vigente para `evaluation` y `processing`. |

**Razones para Ollama local**: ejecución completamente local; instalación y administración simples; excelente integración con Python; amplio catálogo de modelos compatibles; mantenimiento activo; buena documentación.

**Razones para Ollama Cloud**: acceso a modelos de gran escala sin hardware local; plan gratuito con modelos de alta capacidad; misma interfaz API que Ollama local, facilitando integración; sin costos operativos en el plan gratuito.

#### Arquitectura de integración

La automatización **no accede directamente** al modelo. Toda comunicación con el LLM debe realizarse a través de un **AI Service** interno, punto único de acceso a los motores de inferencia.

Responsabilidades del AI Service:

- Gestionar comunicación con proveedores de IA, locales y nube.
- Enrutar cada solicitud al proveedor adecuado según propósito.
- Centralizar gestión de prompts.
- Validar solicitudes y respuestas.
- Gestionar errores y reintentos.
- Desacoplar el resto de la arquitectura del modelo usado.

El enrutamiento se define en la sección `ai_routing` de `config.yaml`, asignando cada propósito, `evaluation` o `processing`, a un proveedor, `cloud` o `local`.

Esta estrategia permite reemplazar o reequilibrar modelos y proveedores sin modificar módulos funcionales.

#### Uso de modelos

El LLM se usa solo para tareas que requieran comprensión, razonamiento o generación de contenido. Las operaciones deterministas deben resolverse con algoritmos tradicionales y librerías especializadas.

#### Modelos oficiales

| Tipo | Modelo | Proveedor / motor | Hardware / plan | Rol |
|---|---|---|---|---|
| Local | Qwen 3.5 4B (`qwen3.5:4b`) | Ollama | GPU con 4 GB VRAM, referencia NVIDIA GTX 1650 Mobile | Fallback opcional para desarrollo o indisponibilidad de la nube. |
| Nube | Gemma 4 31B | Ollama Cloud, plan gratuito | Sin hardware local | Modelo principal para análisis profundo y generación de contenido. |

**Razones del modelo local**: buen seguimiento de instrucciones; buen rendimiento en español e inglés; capacidad suficiente para clasificación y análisis básico; cabe completamente en 4 GB de VRAM, favoreciendo velocidad; compatible con Ollama.

**Razones del modelo nube**: alto rendimiento en razonamiento y generación de texto; excelente calidad en español e inglés; capacidad para análisis profundo y redacción profesional; acceso gratuito mediante Ollama Cloud.

#### Evolución de modelos

Los modelos definidos son la selección inicial. Podrán reemplazarse si:

- Existe evidencia técnica que justifique el cambio.
- El nuevo modelo cumple criterios de admisión del proyecto.
- Aprueba el proceso oficial de evaluación tecnológica.
- Su incorporación no afecta la arquitectura general.

La separación local/nube facilita evolución independiente de cada modelo.

#### Restricciones de IA

- Si se usa fallback local, el modelo local debe ejecutarse vía Ollama.
- El modelo nube debe ser accesible mediante plan gratuito, sin costos recurrentes.
- El enrutamiento entre modelos debe ser transparente para los módulos funcionales.
- Toda comunicación debe realizarse exclusivamente a través del AI Service.
- El flujo inicial de evaluación, módulo 3, debe poder operar con la ruta nube o, si no está alcanzable, mediante fallback local configurable.
- Los modelos deben ser reemplazables en el futuro sin modificar la lógica de negocio.

---

### 5.6 Base de datos

**Objetivo**: definir el sistema oficial de almacenamiento persistente, permitiendo almacenar, consultar, actualizar y mantener información de forma simple, robusta, consultable y completamente local.

**Datos a preservar**: ofertas laborales, empresas, fuentes de ofertas, ubicaciones, ofertas procesadas, resultados de evaluación, estados de procesamiento, historial de ejecución y demás información necesaria para operar la automatización.

El almacenamiento debe facilitar acceso automático del sistema y consulta/edición manual del usuario cuando sea necesario.

**Alternativas evaluadas**: SQLite, Google Sheets y hoja de cálculo local.

Inicialmente se seleccionó hoja de cálculo local. Durante el desarrollo del MVP se migró a **SQLite** para aprovechar consultas estructuradas, integridad referencial y mejor rendimiento.

**Decisión oficial**: **SQLite**, disponible mediante `sqlite3` en la librería estándar de Python. No requiere librerías externas ni instalación adicional.

**Justificación**:

- Forma parte de la librería estándar de Python.
- No requiere instalar ni administrar un DBMS externo.
- Toda la información queda almacenada localmente en un único archivo.
- Soporta integridad referencial, transacciones, consultas SQL y esquemas normalizados.
- Permite consultar y modificar información con herramientas gratuitas como DB Browser for SQLite.
- Ofrece mejor rendimiento que una hoja de cálculo para volúmenes medios.
- Permite consultas estructuradas —filtros, joins, búsquedas— sin cargar toda la base en memoria.
- El archivo `.db` es portable y mantenible sin depender de software de oficina.

#### Organización de información

La base de datos se organiza en tablas normalizadas. Cada tabla tiene identificador secuencial único y campos de auditoría:

- `fecha_creacion`
- `fecha_actualizacion`

Tablas oficiales:

| Tabla | Prefijo | Propósito |
|---|---:|---|
| `fuentes` | FNT | Fuentes de ofertas, por ejemplo LinkedIn. |
| `empresas` | EMP | Empresas empleadoras. |
| `ubicaciones` | UBI | Ubicaciones geográficas. |
| `ofertas` | OFE | Ofertas laborales crudas. |
| `ofertas_procesadas` | OFP | Ofertas procesadas y limpias. |
| `evaluaciones` | EVL | Resultados de evaluación. |
| `resultados_procesamiento` | RSP | Resultados de procesamiento profundo. |

Tabla interna `secuencia_ids`: gestiona contadores para generar identificadores secuenciales con formato:

```text
{PREFIX}-{NUMBER:04d}
```

Ejemplos: `EMP-0001`, `OFE-0042`.

#### Acceso a datos

Toda lectura y escritura a la base de datos debe realizarse exclusivamente mediante:

```text
shared/persistence.py
```

Los módulos funcionales no pueden ejecutar SQL directamente. Esto reduce acoplamiento y facilita cambios futuros del sistema de almacenamiento.

#### Compatibilidad

Archivo oficial:

```text
data/job_search.db
```

Compatible con:

- Python mediante `sqlite3`.
- DB Browser for SQLite, herramienta gráfica gratuita.

#### Restricciones de persistencia

- Persistencia completamente local.
- SQLite como motor oficial de base de datos.
- Acceso exclusivo mediante `shared/persistence.py`.
- Sin dependencia de servicios externos ni sistemas remotos de gestión.

---

### 5.7 Configuración y variables de entorno

**Objetivo**: separar configuración del sistema y código fuente, permitiendo modificar parámetros sin cambiar código.

**Parámetros configurables**: directorios de trabajo, ruta de base de datos principal, ubicación del currículum, ubicación del portafolio profesional, directorio de documentos generados, configuración de modelos de IA, configuración de navegador y parámetros generales de operación.

La configuración se divide en dos componentes:

| Componente | Archivo | Contenido |
|---|---|---|
| Configuración funcional | `config.yaml` | Comportamiento de la automatización. |
| Variables de entorno | `.env` | Información específica de la máquina. |

#### `config.yaml`

Contiene configuración funcional del proyecto. Puede almacenar, entre otros:

- Configuración general.
- Parámetros de procesamiento.
- Configuración de navegador.
- Configuración de modelos de IA.
- Límites de procesamiento.
- Parámetros de evaluación.
- Configuración de módulos.

Su contenido debe organizarse jerárquicamente para facilitar mantenimiento y lectura.

#### `.env`

Contiene solo información dependiente del entorno de ejecución. Puede almacenar, entre otros:

- Rutas locales.
- Directorios de trabajo.
- Ubicación de Ollama.
- Ruta de base de datos.
- Variables específicas de la máquina.

Permitir mover la automatización a otra computadora modificando solo la configuración de entorno, sin alterar código fuente ni configuración funcional.

#### Tecnologías oficiales

| Tecnología | Uso |
|---|---|
| PyYAML | Lectura y escritura oficial de `config.yaml`. |
| python-dotenv | Carga oficial de variables definidas en `.env`. |

#### Reglas de configuración

- El código fuente no contendrá valores de configuración modificables.
- Toda configuración funcional se almacena en `config.yaml`.
- Toda configuración dependiente de máquina se almacena en `.env`.
- La configuración se carga automáticamente al iniciar la automatización.
- Los módulos acceden a la configuración mediante mecanismos definidos por la arquitectura.
- La automatización debe poder moverse a otra máquina modificando solo los archivos de configuración.

---

### 5.8 Gestión de dependencias

**Alternativas evaluadas**: pip, Poetry y uv.

**Decisión oficial**: **pip** como gestor oficial de dependencias.

**Inventario oficial**:

```text
requirements.txt
```

**Justificación de pip**: parte del ecosistema oficial de Python; excelente estabilidad; amplia documentación; compatibilidad con todas las librerías seleccionadas; simplicidad; no introduce complejidad innecesaria. Las alternativas evaluadas ofrecen funcionalidades adicionales que no representan beneficio significativo para la arquitectura definida.

#### Reglas de `requirements.txt`

- Constituye el inventario oficial de dependencias.
- Registra todas las librerías externas aprobadas con sus versiones para garantizar reproducibilidad.
- No incluye librerías de la librería estándar de Python.
- En caso de diferencia entre este documento y `requirements.txt`, prevalecen las versiones registradas en `requirements.txt`.

#### Control de versiones

Toda incorporación, actualización o eliminación de dependencia debe reflejarse inmediatamente en `requirements.txt`.

#### Restricciones

- Usar exclusivamente pip como gestor oficial.
- Mantener `requirements.txt` actualizado.
- No incorporar dependencias sin evaluación y aprobación previas.
- Evitar duplicación de funcionalidades entre librerías.
- Priorizar la librería estándar cuando cubra adecuadamente la necesidad.

---

### 5.9 Herramientas de desarrollo

**Objetivo**: definir herramientas oficiales para desarrollo, depuración y mantenimiento, priorizando simplicidad, estabilidad y compatibilidad con el stack.

Necesidades cubiertas: edición de código, administración del entorno de desarrollo, depuración, validación de calidad de código y verificación de tipado estático.

| Herramienta | Rol oficial | Justificación |
|---|---|---|
| Visual Studio Code | Editor oficial de desarrollo. | Compatibilidad con Python, integración con Git, amplio ecosistema de extensiones, herramientas integradas de depuración, estabilidad y disponibilidad gratuita. |
| venv | Mecanismo oficial de entornos virtuales. | Forma parte de la librería estándar de Python; no requiere dependencias adicionales y cubre las necesidades del proyecto. |
| Black | Formateo automático de código fuente. | Garantiza estilo uniforme durante el desarrollo. |
| Ruff | Análisis estático de código. | Detecta errores potenciales, problemas de calidad y desviaciones de buenas prácticas antes de la ejecución. |
| mypy | Verificación estática de tipos. | Complementa la validación de Pydantic y detecta inconsistencias durante el desarrollo. |

**Principios de uso**: estilo uniforme, detección temprana de errores, menor complejidad de mantenimiento, legibilidad y consistencia, integración correcta con el stack.

**Restricciones**: herramientas gratuitas, compatibles con Python y el stack oficial, sin duplicar funcionalidad, incorporadas solo cuando aporten beneficio técnico demostrable.

---

### 5.10 Herramientas de pruebas

**Alternativas evaluadas**: unittest y pytest.

**Decisión oficial**: **pytest**.

**Justificación**: sintaxis simple y fácil de mantener; excelente documentación; amplia adopción en el ecosistema Python; flexibilidad para distintos tipos de pruebas; excelente integración con Visual Studio Code; capacidad de extensión mediante plugins.

**Alcance**: pruebas automatizadas pueden verificar operación de módulos individuales, integración entre componentes, procesamiento de datos, reglas de negocio y funcionamiento correcto de funciones críticas. Se implementarán pruebas cuando la complejidad o impacto del componente lo justifique.

**Principios**: verificar comportamiento esperado; ser reproducibles; mantener independencia entre pruebas; facilitar detección temprana de errores; evolucionar junto con el código.

**Restricciones**: compatibles con el stack oficial; mantenerse actualizadas; no introducir complejidad innecesaria; usarse principalmente para validar componentes cuya criticidad justifique pruebas automatizadas.

---

### 5.11 Herramientas de documentación

**Alternativas evaluadas**: Markdown `.md`, MkDocs y Sphinx.

**Decisión oficial**: **Markdown `.md`** como formato oficial para toda la documentación técnica y funcional.

**Justificación**: formato abierto y ampliamente adoptado; excelente legibilidad editable y renderizada; integración nativa con Git; compatibilidad con Visual Studio Code; bajo mantenimiento; no requiere herramientas adicionales; facilita versionado junto al código. MkDocs y Sphinx se orientan principalmente a generación automática de sitios de documentación, necesidad no requerida por el proyecto.

**Organización**: toda documentación oficial debe seguir la estructura documental definida. Cada documento debe tratar un tema específico y mantenerse actualizado conforme evoluciona el proyecto.

**Principios**: consistencia con la implementación; actualización cuando se aprueben cambios relevantes; organización y estructura; evitar duplicación; claridad, precisión y facilidad de consulta.

**Restricciones**: usar Markdown oficial; compatibilidad con Visual Studio Code y Git; no incorporar herramientas adicionales de generación automática de documentación mientras no exista requisito funcional que lo justifique.

---

### 5.12 Control de versiones

**Alternativas evaluadas**: Git y administración manual de versiones.

**Decisión oficial**: **Git**.

Inicialmente, el repositorio se gestiona localmente en la máquina donde se desarrolla la automatización.

**Justificación**: estándar de la industria; historial completo del proyecto; facilita recuperación de versiones anteriores; integración correcta con Visual Studio Code; permite versionar código y documentación juntos; no requiere servicios externos para funcionar.

**Alcance**: Git versiona código fuente, documentación técnica, archivos de configuración y recursos necesarios para el proyecto. No se usa para almacenar archivos generados automáticamente ni información temporal.

**Principios**: registrar cambios organizadamente; mantener historial claro; hacer commits solo cuando los cambios sean funcionalmente estables; mantener código y documentación sincronizados.

**Restricciones**: Git es el único sistema oficial de control de versiones; mantener repositorio actualizado durante todo el desarrollo; no depender de plataformas remotas para el funcionamiento del control de versiones.

---

### 5.13 Herramienta auxiliar de hojas de cálculo

**Decisión oficial**: **ONLYOFFICE** como herramienta oficial para consultar, editar y gestionar archivos de hoja de cálculo usados por la automatización.

**Justificación**: permite trabajar directamente con archivos `.xlsx`; opera completamente en local; no requiere servicios en la nube; interfaz familiar para el usuario; facilita revisión y edición manual de información; compatible con el mecanismo de almacenamiento definido.

**Alcance**: consulta de información almacenada, revisión de resultados, modificaciones manuales cuando sea necesario y verificación de contenido de hojas de cálculo. La lectura y escritura automática de archivos `.xlsx`, cuando corresponda, sigue realizándose mediante `openpyxl`.

**Principios**: complementar la operación de la automatización; no reemplazar componentes del stack oficial; facilitar interacción del usuario; reducir complejidad operacional.

**Restricciones**: gratuita; operación local; compatibilidad con el stack oficial; no duplicar funcionalidades provistas por otras tecnologías.

---

## 6. Compatibilidad entre tecnologías

Todas las tecnologías seleccionadas deben ser compatibles entre sí y tener una responsabilidad claramente definida dentro de la arquitectura.

No se permiten tecnologías que:

- Dupliquen funcionalidades existentes.
- Generen conflictos de integración.
- Introduzcan dependencias innecesarias.
- Aumenten complejidad sin beneficio técnico demostrable.

### 6.1 Matriz de integración

| Tecnología | Compatible con | Función principal |
|---|---|---|
| Python | Todo el stack. | Lenguaje principal del proyecto. |
| Playwright | BeautifulSoup4, Tenacity, Loguru. | Automatización de navegador. |
| BeautifulSoup4 + lxml | Playwright. | Procesamiento y análisis de HTML. |
| Pydantic | Todo el sistema. | Validación, serialización y deserialización de datos. |
| Ollama | Qwen, Gemma. | Motor local de inferencia de IA, usado como fallback o ruta local configurable. |
| Ollama Cloud | Gemma 4 31B. | Motor nube de inferencia de IA, plan gratuito. |
| Qwen 3.5 4B | Ollama. | Modelo local de lenguaje. |
| Gemma 4 31B | Ollama Cloud. | Modelo nube de lenguaje. |
| SQLite | Python `sqlite3`, `shared/persistence.py`, DB Browser for SQLite. | Base de datos oficial del proyecto. |
| openpyxl | ONLYOFFICE. | Gestión automática de archivos `.xlsx` cuando se usen hojas de cálculo. |
| PyYAML | python-dotenv. | Gestión de configuración del proyecto. |
| Loguru | Todo el stack. | Registro de eventos y auditoría. |
| Tenacity | Playwright, Ollama, httpx. | Reintentos automáticos. |
| RapidFuzz | Pydantic. | Comparación aproximada de texto. |
| httpx | Tenacity, Loguru. | Solicitudes HTTP cuando no se requiere navegador. |
| Git | Todo el proyecto. | Control de versiones. |

### 6.2 Integración arquitectónica

Cada componente debe interactuar solo con los elementos necesarios para cumplir su responsabilidad. La arquitectura favorece bajo acoplamiento, alta cohesión, separación de responsabilidades, facilidad de mantenimiento y evolución futura sin afectar el resto del sistema.

### 6.3 Compatibilidad futura

Toda nueva tecnología debe pasar evaluación previa antes de incorporarse. Como mínimo debe demostrar:

- Compatibilidad técnica con tecnologías existentes.
- Ausencia de conflictos funcionales.
- Integración con la arquitectura definida.
- Beneficio técnico claramente justificado.

### 6.4 Restricciones de incorporación

- Mantener compatibilidad con el stack oficial.
- No reemplazar componentes existentes sin evaluación previa.
- No introducir dependencias redundantes.
- Preservar estabilidad y coherencia de la arquitectura.

---

## 7. Restricciones tecnológicas generales

Estas restricciones deben respetarse durante todo el ciclo de vida del proyecto.

### 7.1 Software gratuito

Todas las tecnologías, herramientas, librerías y componentes deben ser de uso gratuito. No se adoptarán tecnologías cuyo uso dependa de licencias de pago, suscripciones obligatorias o costos recurrentes para operar la automatización.

### 7.2 Ejecución local

La automatización debe ejecutarse principalmente en la máquina del usuario. No debe depender de servicios externos para su operación principal. Los componentes críticos deben operar localmente.

Excepción oficial vigente: el acceso a Ollama Cloud para IA, mediante plan gratuito, con fallback local configurable.

### 7.3 Inteligencia artificial

Reglas vigentes:

- Toda interacción con modelos de lenguaje debe realizarse a través del AI Service definido por la arquitectura.
- La ruta oficial vigente es cloud-primary con Ollama Cloud, plan gratuito.
- El fallback local, si se activa, debe ejecutarse vía Ollama.
- No se usarán APIs comerciales de pago como componente principal de IA.
- La restricción original de ejecutar IA exclusivamente local queda sustituida por la decisión `2026-07-30 (Phase 3)`, manteniéndose el fallback local configurable.

### 7.4 Compatibilidad tecnológica

Toda nueva tecnología debe ser compatible con el stack oficial. No se introducirán componentes que generen incompatibilidades, conflictos de integración o duplicación de funcionalidades.

### 7.5 Minimización de dependencias

Las dependencias externas solo se incorporan si:

- Resuelven una necesidad real del proyecto.
- Aportan ventaja técnica demostrable.
- No existe solución equivalente en la librería estándar de Python.
- No duplican funcionalidad ya cubierta por otra tecnología del stack.

### 7.6 Mantenibilidad

Se priorizan tecnologías con mantenimiento activo, documentación suficiente, comunidad consolidada, estabilidad y amplia adopción en su ecosistema.

### 7.7 Simplicidad

Cuando existan alternativas técnicamente equivalentes, se elegirá la que:

- Introduzca menor complejidad.
- Requiera menos mantenimiento.
- Facilite mejor evolución futura.
- Se integre mejor con el resto del stack.

### 7.8 Portabilidad

La automatización debe poder moverse a otra máquina con la menor cantidad posible de modificaciones. La configuración del sistema debe mantenerse separada del código fuente para facilitar portabilidad.

### 7.9 Prohibiciones generales

Durante el desarrollo del proyecto no está permitido:

- Incorporar tecnologías sin evaluación técnica previa.
- Duplicar funcionalidades mediante herramientas distintas.
- Introducir dependencias sin beneficio claramente justificado.
- Modificar el stack oficial sin actualizar previamente la documentación correspondiente.

---

## 8. Estrategia de actualización y reemplazo tecnológico

### 8.1 Principio general

El stack tecnológico debe mantenerse lo más estable posible. Las tecnologías no se reemplazan solo por aparición de nuevas alternativas o tendencias de mercado. Toda modificación debe responder a una necesidad técnica real y aportar mejora demostrable.

### 8.2 Criterios para actualización

Una tecnología puede actualizarse cuando:

- Existen mejoras relevantes en estabilidad, rendimiento o seguridad.
- Se corrigen errores que afectan la operación del proyecto.
- La nueva versión mantiene compatibilidad con el resto del stack.
- La actualización no implica cambios arquitectónicos injustificados.

### 8.3 Criterios para reemplazo

Una tecnología puede reemplazarse solo si ocurre al menos una de estas situaciones:

- Deja de tener mantenimiento activo.
- Presenta problemas de compatibilidad no resolubles.
- Existe una alternativa claramente superior para las necesidades del proyecto.
- El reemplazo aporta beneficios técnicos significativos que justifican el costo de migración.

La sola existencia de una tecnología más nueva no es razón suficiente.

### 8.4 Proceso de evaluación previo

Antes de aprobar actualización o reemplazo, debe realizarse evaluación técnica que contemple, como mínimo:

- Compatibilidad con el stack oficial.
- Impacto en la arquitectura del proyecto.
- Riesgos asociados a la migración.
- Beneficios esperados.
- Esfuerzo de implementación.
- Impacto en mantenimiento futuro.

La decisión debe documentarse antes de incorporarse al proyecto.

### 8.5 Compatibilidad durante transición

Al reemplazar una tecnología, debe asegurarse que la transición no comprometa:

- Integridad de la información.
- Estabilidad de la automatización.
- Compatibilidad con los demás componentes del sistema.

Siempre que sea posible, las migraciones deben realizarse de manera controlada y verificable.

### 8.6 Documentación obligatoria

Toda actualización o reemplazo aprobado debe reflejarse, como mínimo, en:

- Este documento.
- Inventario oficial de pila tecnológica.
- Documentación técnica afectada.
- `requirements.txt`, cuando aplique.

### 8.7 Restricciones de evolución

- No modificar tecnologías sin evaluación técnica previa.
- No introducir cambios que aumenten innecesariamente la complejidad.
- Mantener coherencia con los principios tecnológicos definidos.
- Preservar estabilidad, mantenibilidad y portabilidad.

---

## 9. Criterios de aceptación del stack

El stack tecnológico se considera oficialmente aprobado cuando cumple, como mínimo:

### 9.1 Criterios generales

- Todas las tecnologías fueron evaluadas técnicamente.
- Existe justificación documentada de cada decisión.
- No hay duplicaciones funcionales entre tecnologías.
- Todas las tecnologías son compatibles entre sí.
- El stack mantiene coherencia con la arquitectura definida.

### 9.2 Compatibilidad

Las tecnologías se integran correctamente sin conflictos funcionales ni arquitectónicos. La incorporación de un nuevo componente no debe comprometer la estabilidad del resto del sistema.

### 9.3 Mantenibilidad

El stack favorece mantenimiento mediante tecnologías estables, documentación suficiente, comunidad activa, baja complejidad y facilidad de actualización.

### 9.4 Sostenibilidad

Las tecnologías se alinean con los principios generales del proyecto:

- Uso gratuito.
- Ejecución local como base principal.
- Independencia de servicios externos para operación principal, con la excepción oficial vigente de IA cloud gratuita con fallback local.
- Facilidad de mantenimiento.
- Escalabilidad según necesidades de la automatización.

### 9.5 Consistencia documental

Toda tecnología aprobada debe documentarse en:

- Este documento.
- Inventario oficial de pila tecnológica.
- Documentación técnica correspondiente, cuando aplique.

### 9.6 Aceptación final

El stack queda oficialmente aprobado cuando cumple todos los criterios anteriores. Cualquier incorporación, modificación o reemplazo posterior debe reevaluarse según estos mismos criterios antes de formar parte oficial del stack.

---

## 10. Inventario oficial de tecnología

Este inventario consolida las tecnologías oficialmente aprobadas. Constituye la referencia oficial del stack tecnológico del proyecto.

| Categoría | Tecnología | Propósito |
|---|---|---|
| Lenguaje de programación | Python 3.12 | Desarrollo de la automatización. |
| Procesamiento HTML | BeautifulSoup4 | Análisis y extracción de información desde HTML. |
| Parser HTML | lxml | Parser usado por BeautifulSoup4. |
| Validación de datos | Pydantic v2 | Validación, serialización y deserialización de datos. |
| Registro de eventos | Loguru | Logging, trazabilidad y auditoría. |
| Comparación de texto | RapidFuzz | Comparación aproximada de cadenas. |
| Reintentos | Tenacity | Gestión automática de reintentos. |
| Cliente HTTP | httpx | Solicitudes HTTP cuando no se requiere navegador. |
| Automatización de navegador | Playwright | Navegación e interacción con sitios web. |
| Motor IA local | Ollama | Inferencia local de modelos de lenguaje, fallback configurable. |
| Motor IA nube | Ollama Cloud | Inferencia nube de modelos de lenguaje, plan gratuito. |
| Modelo IA local | Qwen 3.5 4B | Modelo local para fallback, desarrollo o tareas locales asignadas. |
| Modelo IA nube | Gemma 4 31B | Modelo nube para procesamiento profundo y generación de contenido. |
| Persistencia oficial | SQLite | Base de datos local oficial. |
| Archivo de base de datos | `data/job_search.db` | Archivo oficial de persistencia. |
| Acceso a datos | `shared/persistence.py` | Único punto de acceso a base de datos. |
| Consulta manual de base de datos | DB Browser for SQLite | Herramienta gratuita compatible para consulta y edición manual. |
| Configuración funcional | `config.yaml` | Configuración de comportamiento de la automatización. |
| Variables de entorno | `.env` | Configuración específica de máquina. |
| Gestión YAML | PyYAML | Lectura y escritura de archivos YAML. |
| Carga de entorno | python-dotenv | Carga automática del archivo `.env`. |
| Gestión de dependencias | pip | Instalación y gestión de dependencias. |
| Inventario de dependencias | `requirements.txt` | Registro oficial de librerías externas y versiones. |
| Editor de código | Visual Studio Code | Desarrollo de la automatización. |
| Entorno virtual | venv | Aislamiento del entorno de desarrollo. |
| Formateo de código | Black | Formateo automático de código fuente. |
| Análisis estático | Ruff | Análisis de calidad de código. |
| Tipado estático | mypy | Verificación de tipos. |
| Pruebas | pytest | Pruebas automatizadas. |
| Documentación | Markdown `.md` | Documentación técnica y funcional. |
| Control de versiones | Git | Versionado del proyecto. |
| Gestión automática de `.xlsx` | openpyxl | Lectura y escritura automática de hojas de cálculo cuando se usen. |
| Herramienta auxiliar `.xlsx` | ONLYOFFICE | Consulta y edición manual local de archivos `.xlsx`. |

**Nota**: el documento original listaba `.xlsx` como almacenamiento oficial en el inventario. Tras la migración descrita en la sección de base de datos, la persistencia oficial vigente es **SQLite**. `openpyxl` y `ONLYOFFICE` se conservan como herramientas auxiliares para hojas de cálculo, no como base de datos oficial.

Cualquier incorporación, reemplazo o eliminación de tecnología debe cumplir el proceso de evaluación definido antes de formar parte del stack oficial. Este inventario debe mantenerse actualizado durante toda la vida del proyecto.
