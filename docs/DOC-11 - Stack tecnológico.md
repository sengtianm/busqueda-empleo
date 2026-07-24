# Documento 11 - Stack Tecnológico

## 1. Propósito del documento

El presente documento define el stack tecnológico oficial de la automatización de búsqueda de empleo.

Su propósito es establecer, justificar y documentar las tecnologías, herramientas, librerías, frameworks, componentes y metodologías que conformarán la base tecnológica del proyecto, garantizando que todas las decisiones técnicas sean consistentes con los objetivos, el alcance, los requisitos y los principios definidos en la documentación oficial.

Este documento constituye la referencia oficial para la selección de tecnologías durante el diseño, desarrollo, pruebas, mantenimiento y evolución de la automatización. Ningún componente tecnológico deberá incorporarse al proyecto sin haber sido previamente evaluado conforme a los criterios establecidos en este documento.

Las decisiones aquí documentadas deberán mantener coherencia con los Documentos 0 al 10, incluyendo los requisitos funcionales y no funcionales, el modelo de decisiones, el flujo de datos, los estándares del proyecto, el modelo de manejo de errores, la arquitectura de carpetas, el alcance y objetivos, la investigación de fuentes de empleo y el perfil profesional del usuario.

Las tecnologías seleccionadas deberán satisfacer los criterios principales del proyecto, priorizando el uso de herramientas gratuitas, una arquitectura práctica, mantenible y escalable, y una adecuada independencia tecnológica que facilite la evolución futura de la solución.

Asimismo, este documento servirá como fundamento para la elaboración de los documentos posteriores de Arquitectura General del Sistema, Modelo de Datos y Desarrollo del MVP, garantizando que todas las decisiones de implementación se apoyen sobre un stack tecnológico previamente analizado, justificado y aprobado.

Toda modificación al stack tecnológico deberá documentarse, justificarse y aprobarse formalmente antes de incorporarse al proyecto, preservando la trazabilidad y la coherencia con el resto de la documentación oficial.

---

## 2. Principios para la selección tecnológica

La selección de cualquier tecnología, herramienta, librería, framework o componente que forme parte del stack tecnológico de la automatización deberá realizarse conforme a los principios definidos en este capítulo.

Estos principios constituyen los criterios oficiales de evaluación tecnológica del proyecto y serán de aplicación obligatoria durante el análisis, comparación, selección, sustitución o actualización de cualquier componente tecnológico.

Toda decisión tecnológica deberá estar debidamente justificada mediante una evaluación objetiva de estos principios, garantizando la coherencia con los objetivos del proyecto y con la documentación oficial previamente aprobada.

Se establecen los siguientes principios oficiales:

### PST-001. Uso de tecnologías gratuitas

Se priorizarán exclusivamente tecnologías cuya utilización sea gratuita para el alcance definido del proyecto.

### PST-002. Licenciamiento compatible

Las tecnologías seleccionadas deberán contar con licencias que permitan su utilización, modificación y distribución conforme a los objetivos del proyecto.

### PST-003. Madurez tecnológica

Las tecnologías deberán encontrarse suficientemente consolidadas y demostrar estabilidad para su utilización en entornos reales.

### PST-004. Estabilidad

Se priorizarán tecnologías con un historial de funcionamiento estable y con bajo riesgo de cambios disruptivos frecuentes.

### PST-005. Comunidad y ecosistema

Las tecnologías deberán disponer de una comunidad activa que facilite soporte, evolución y disponibilidad de recursos técnicos.

### PST-006. Calidad de la documentación

Deberán contar con documentación oficial completa, actualizada y suficiente para facilitar su implementación y mantenimiento.

### PST-007. Compatibilidad

Las tecnologías deberán integrarse correctamente con el resto del stack tecnológico seleccionado.

### PST-008. Modularidad

Deberán favorecer una arquitectura modular que facilite el aislamiento de responsabilidades y la reutilización de componentes.

### PST-009. Escalabilidad

Las tecnologías deberán permitir el crecimiento funcional y técnico de la automatización sin requerir rediseños significativos.

### PST-010. Mantenibilidad

Las soluciones seleccionadas deberán facilitar la comprensión, actualización y mantenimiento del sistema a largo plazo.

### PST-011. Rendimiento

Deberán ofrecer un desempeño adecuado para las cargas de trabajo previstas en el proyecto.

### PST-012. Seguridad

Las tecnologías deberán incorporar mecanismos que favorezcan el desarrollo de soluciones seguras y confiables.

### PST-013. Portabilidad

Se priorizarán tecnologías que permitan ejecutar la solución en distintos entornos con el menor esfuerzo posible.

### PST-014. Independencia tecnológica

Siempre que sea viable, se evitará generar dependencias innecesarias con proveedores, plataformas o servicios específicos.

### PST-015. Facilidad de integración

Las tecnologías deberán integrarse de forma sencilla con los componentes internos y externos de la automatización.

### PST-016. Actualización sostenible

Las tecnologías deberán presentar un ciclo de evolución que permita actualizar el sistema sin afectar significativamente su estabilidad.

### PST-017. Consumo eficiente de recursos

Se priorizarán tecnologías que utilicen eficientemente los recursos de hardware disponibles.

### PST-018. Facilidad para pruebas

Las tecnologías deberán facilitar la implementación de pruebas automatizadas y procesos de validación.

### PST-019. Compatibilidad con inteligencia artificial

Deberán integrarse adecuadamente con los modelos de lenguaje y demás componentes de inteligencia artificial utilizados por la automatización.

### PST-020. Compatibilidad con automatización web

Las tecnologías deberán permitir la automatización robusta de procesos de navegación, extracción e interacción con plataformas web.

### PST-021. Curva de aprendizaje

Se valorarán tecnologías cuya complejidad de adopción resulte razonable para facilitar el mantenimiento futuro del proyecto.

### PST-022. Riesgo de obsolescencia

Se priorizarán tecnologías con perspectivas favorables de continuidad, mantenimiento y evolución dentro de la industria.

Todos los principios definidos en este capítulo tendrán carácter obligatorio y servirán como base para la evaluación comparativa de las alternativas tecnológicas analizadas en los capítulos posteriores de este documento.

---

## 3. Criterios de evaluación de tecnologías

La selección de cualquier tecnología, herramienta, librería, framework o componente del stack tecnológico deberá realizarse mediante un proceso de evaluación objetivo, uniforme, reproducible y documentado.

Todas las alternativas tecnológicas deberán evaluarse utilizando la metodología definida en este capítulo, con el propósito de garantizar que las decisiones adoptadas sean técnicamente justificables, coherentes con los principios establecidos en este documento y alineadas con los objetivos generales del proyecto.

La evaluación tecnológica oficial del proyecto estará compuesta por dos etapas obligatorias: la evaluación de criterios eliminatorios y la evaluación de criterios puntuables.

---

### 3.1. Evaluación de criterios eliminatorios

Los criterios eliminatorios corresponden a aquellos principios cuyo incumplimiento hace incompatible una tecnología con los objetivos, restricciones o requisitos del proyecto.

Toda tecnología deberá cumplir la totalidad de estos criterios para continuar el proceso de evaluación.

El incumplimiento de cualquiera de ellos implicará el descarte inmediato de la alternativa evaluada, independientemente de las ventajas que pueda presentar en otros aspectos.

Los criterios eliminatorios oficiales son los siguientes:

| Código | Principio |
|---------|-----------|
| PST-001 | Uso de tecnologías gratuitas |
| PST-002 | Licenciamiento compatible |
| PST-007 | Compatibilidad con el resto del stack tecnológico |
| PST-012 | Seguridad |
| PST-015 | Facilidad de integración |
| PST-019 | Compatibilidad con inteligencia artificial (cuando aplique) |
| PST-020 | Compatibilidad con automatización web (cuando aplique) |

---

### 3.2. Evaluación de criterios puntuables

Las tecnologías que superen la etapa anterior serán evaluadas mediante un sistema de puntuación ponderada.

Cada criterio recibirá un peso proporcional a su importancia dentro del proyecto.

Posteriormente, cada tecnología será calificada frente a cada criterio, obteniendo una puntuación total que permitirá realizar comparaciones objetivas entre las diferentes alternativas.

Los criterios puntuables oficiales son los siguientes:

| Código | Principio |
|---------|-----------|
| PST-003 | Madurez tecnológica |
| PST-004 | Estabilidad |
| PST-005 | Comunidad y ecosistema |
| PST-006 | Calidad de la documentación |
| PST-008 | Modularidad |
| PST-009 | Escalabilidad |
| PST-010 | Mantenibilidad |
| PST-011 | Rendimiento |
| PST-013 | Portabilidad |
| PST-014 | Independencia tecnológica |
| PST-016 | Actualización sostenible |
| PST-017 | Consumo eficiente de recursos |
| PST-018 | Facilidad para pruebas |
| PST-021 | Curva de aprendizaje |
| PST-022 | Riesgo de obsolescencia |

---

### 3.3. Principios de evaluación

Toda evaluación tecnológica deberá cumplir los siguientes principios:

- Objetividad.
- Uniformidad.
- Trazabilidad.
- Transparencia.
- Reproducibilidad.
- Comparabilidad.
- Justificación documental.

Ninguna tecnología podrá ser seleccionada mediante criterios subjetivos o preferencias personales.

---

### 3.4. Matriz oficial de evaluación tecnológica

Toda decisión tecnológica deberá quedar respaldada mediante una matriz oficial de evaluación que documente, como mínimo:

- Tecnologías evaluadas.
- Criterios eliminatorios aplicados.
- Resultado de cada criterio eliminatorio.
- Criterios puntuables considerados.
- Peso asignado a cada criterio.
- Calificación obtenida por cada alternativa.
- Puntuación total obtenida.
- Justificación técnica de la decisión adoptada.

La matriz de evaluación constituirá el soporte documental oficial de todas las decisiones tecnológicas registradas en este documento.

---

### 3.5. Reglas de decisión

La selección de una tecnología deberá cumplir simultáneamente las siguientes condiciones:

1. Superar todos los criterios eliminatorios.
2. Obtener la mayor puntuación ponderada entre las alternativas evaluadas.
3. No contradecir ningún documento oficial del proyecto.
4. No incumplir los requisitos funcionales ni los requisitos no funcionales.
5. Mantener la coherencia con la arquitectura general definida para la automatización.

---

### 3.6. Reevaluación tecnológica

Cuando una tecnología sea reemplazada, actualizada o incorporada al proyecto, deberá realizarse una nueva evaluación utilizando exactamente esta misma metodología.

Toda reevaluación deberá documentarse formalmente para preservar la trazabilidad histórica de las decisiones tecnológicas del proyecto.

### 3.7. Escala oficial de calificación

Con el fin de garantizar la uniformidad de todas las evaluaciones tecnológicas realizadas dentro del proyecto, se adopta la siguiente escala oficial de calificación para los criterios puntuables.

| Calificación | Interpretación |
|--------------|----------------|
| 0 | No cumple el criterio. |
| 1 | Cumplimiento muy deficiente. |
| 2 | Cumplimiento deficiente. |
| 3 | Cumplimiento aceptable. |
| 4 | Cumplimiento alto. |
| 5 | Cumplimiento excelente. |

Todas las tecnologías evaluadas deberán calificarse utilizando exclusivamente esta escala.

No se permitirán escalas diferentes dentro del presente documento.

---

### 3.8. Ponderación oficial de criterios

Los criterios puntuables tendrán un peso relativo que reflejará su importancia para el proyecto.

La ponderación oficial será la siguiente:

| Código | Criterio | Peso (%) |
|---------|----------|---------:|
| PST-003 | Madurez tecnológica | 8 |
| PST-004 | Estabilidad | 8 |
| PST-005 | Comunidad y ecosistema | 8 |
| PST-006 | Calidad de la documentación | 8 |
| PST-008 | Modularidad | 7 |
| PST-009 | Escalabilidad | 10 |
| PST-010 | Mantenibilidad | 10 |
| PST-011 | Rendimiento | 7 |
| PST-013 | Portabilidad | 5 |
| PST-014 | Independencia tecnológica | 6 |
| PST-016 | Actualización sostenible | 5 |
| PST-017 | Consumo eficiente de recursos | 5 |
| PST-018 | Facilidad para pruebas | 6 |
| PST-021 | Curva de aprendizaje | 2 |
| PST-022 | Riesgo de obsolescencia | 5 |

La suma de todas las ponderaciones deberá ser siempre igual al 100 %.

La puntuación final de cada alternativa tecnológica se calculará aplicando estas ponderaciones sobre la calificación obtenida en cada criterio puntuable.

---

### 3.9. Cálculo de la puntuación final

La puntuación final de una tecnología se obtendrá mediante la suma de las puntuaciones ponderadas de todos los criterios puntuables, una vez haya superado satisfactoriamente la evaluación de los criterios eliminatorios.

Esta puntuación constituirá la referencia oficial para comparar alternativas tecnológicas dentro del proyecto.

La selección de una tecnología no dependerá exclusivamente de su puntuación final, sino también del cumplimiento de los criterios eliminatorios y de las reglas de decisión establecidas en este documento.


---

## 4. Arquitectura tecnológica general

La arquitectura tecnológica de la automatización define la forma en que se organizarán los componentes técnicos del sistema para garantizar el cumplimiento de los objetivos, requisitos y principios establecidos en la documentación oficial del proyecto.

Su propósito es proporcionar una estructura tecnológica coherente, mantenible, escalable y desacoplada, que sirva como base para la selección de tecnologías y para el desarrollo de todos los módulos de la automatización.

La arquitectura definida en este documento constituye el modelo oficial que deberán respetar todos los componentes tecnológicos incorporados al proyecto.

---

### 4.1. Modelo arquitectónico

La automatización adopta una **arquitectura híbrida**, compuesta por la integración de varios patrones arquitectónicos complementarios, seleccionados de acuerdo con las características y necesidades específicas del proyecto.

Esta arquitectura combina los siguientes enfoques:

- Arquitectura modular.
- Organización interna por capas.
- Flujo secuencial de procesamiento.
- Servicios compartidos.
- Persistencia centralizada.

La combinación de estos patrones permite aprovechar las fortalezas de cada uno sin introducir complejidad innecesaria.

---

### 4.2. Arquitectura modular

La solución estará dividida en módulos funcionales independientes, cada uno responsable de una etapa específica del flujo de procesamiento de ofertas.

Cada módulo tendrá una única responsabilidad y podrá evolucionar de manera independiente siempre que respete las interfaces y contratos definidos por la arquitectura.

---

### 4.3. Organización interna por capas

Cada módulo deberá organizar internamente sus componentes mediante una separación clara de responsabilidades.

Como principio general, deberá existir separación entre:

- Lógica de negocio.
- Acceso a datos.
- Integración con servicios externos.
- Configuración.
- Componentes de infraestructura.

Esta organización busca reducir el acoplamiento interno y facilitar el mantenimiento del sistema.

---

### 4.4. Flujo secuencial de procesamiento

La arquitectura respetará el flujo oficial de procesamiento definido para la automatización.

Cada módulo recibirá una oferta en un estado determinado, ejecutará exclusivamente las operaciones correspondientes a su responsabilidad y entregará el resultado al siguiente módulo del flujo.

No se permitirán dependencias que alteren el orden oficial del procesamiento.

---

### 4.5. Servicios compartidos

Las funcionalidades comunes de la automatización deberán implementarse como servicios reutilizables accesibles por los distintos módulos del sistema.

Entre estos servicios podrán encontrarse, entre otros:

- Configuración.
- Persistencia.
- Gestión de estados.
- Registro de eventos.
- Manejo de errores.
- Inteligencia artificial.
- Gestión de prompts.
- Utilidades comunes.

La reutilización de estos componentes deberá evitar la duplicación de responsabilidades dentro de la arquitectura.

---

### 4.6. Persistencia centralizada

Toda la información oficial del proyecto deberá mantenerse en una fuente única de persistencia compartida por los módulos autorizados.

La arquitectura deberá garantizar la consistencia, trazabilidad e integridad de la información durante todo el ciclo de vida de las ofertas procesadas.

No se permitirá la existencia de repositorios paralelos que comprometan la integridad de los datos.

---

### 4.7. Principios de la arquitectura tecnológica

La arquitectura tecnológica deberá preservar permanentemente los siguientes principios:

- Modularidad.
- Bajo acoplamiento.
- Alta cohesión.
- Escalabilidad.
- Mantenibilidad.
- Reutilización de componentes.
- Separación de responsabilidades.
- Consistencia de datos.
- Trazabilidad.
- Evolución controlada.

---

### 4.8. Evolución arquitectónica

Toda incorporación, sustitución o modificación de componentes tecnológicos deberá respetar la arquitectura definida en este documento.

Cualquier cambio estructural deberá documentarse, justificarse y aprobarse antes de su implementación, garantizando la compatibilidad con el resto del sistema y con la documentación oficial del proyecto.

---

## 5. Lenguaje de programación

### 5.1. Objetivo

El lenguaje de programación constituye la base tecnológica sobre la cual se desarrollará la totalidad de la automatización.

Su selección deberá garantizar la compatibilidad con la arquitectura tecnológica definida en este documento, así como satisfacer los requisitos funcionales, no funcionales y los criterios oficiales de evaluación establecidos para el proyecto.

---

### 5.2. Alternativas evaluadas

Para la selección del lenguaje de programación se evaluaron las siguientes alternativas:

- Python
- Node.js (JavaScript/TypeScript)
- C#
- Java
- Go

Las demás alternativas fueron descartadas por no ofrecer ventajas técnicas relevantes para los objetivos específicos de la automatización.

---

### 5.3. Evaluación técnica

Las alternativas fueron analizadas considerando, entre otros, los siguientes aspectos:

- Compatibilidad con automatización web.
- Integración con modelos de inteligencia artificial.
- Ecosistema de librerías.
- Procesamiento de datos.
- Madurez tecnológica.
- Comunidad y documentación.
- Facilidad de mantenimiento.
- Escalabilidad.
- Compatibilidad con la arquitectura del proyecto.

Como resultado del análisis, Python obtuvo la mejor evaluación global al ofrecer la mayor compatibilidad con los objetivos y necesidades de la automatización.

---

### 5.4. Lenguaje seleccionado

Se establece Python 3.12 como lenguaje de programación oficial del proyecto.

Python será utilizado para el desarrollo de todos los módulos funcionales, componentes compartidos, procesos de automatización, integración con inteligencia artificial, procesamiento de datos y demás elementos que conformen la solución.

---

### 5.5. Justificación de la decisión

La selección de Python se fundamenta en los siguientes factores:

- Excelente compatibilidad con procesos de automatización web.
- Ecosistema maduro y ampliamente consolidado para integración con modelos de inteligencia artificial.
- Amplia disponibilidad de librerías para procesamiento de datos.
- Excelente documentación oficial y comunidad de desarrollo.
- Alto nivel de mantenibilidad.
- Gran estabilidad tecnológica.
- Compatibilidad con arquitecturas modulares.
- Bajo riesgo de obsolescencia.
- Compatibilidad con los criterios tecnológicos definidos en este documento.

La evaluación realizada concluye que Python representa la alternativa con mejor equilibrio entre funcionalidad, mantenibilidad, escalabilidad y facilidad de evolución para los objetivos del proyecto.

---

### 5.6. Alcance de la decisión

La presente decisión será aplicable a todos los desarrollos que formen parte de la automatización.

La incorporación de componentes implementados en otros lenguajes únicamente podrá realizarse cuando exista una justificación técnica debidamente documentada y aprobada conforme a la metodología de evaluación definida en este documento.

---

# 6. Librerías y dependencias principales

## 6.1 Objetivo

Definir las librerías principales que formarán parte del núcleo de la automatización, estableciendo aquellas dependencias que aportan una funcionalidad esencial y que no pueden ser reemplazadas de manera adecuada por la biblioteca estándar de Python o por otra tecnología ya adoptada dentro del stack.

Las librerías seleccionadas deberán mantenerse activamente, ser compatibles con el resto del stack tecnológico y aportar un beneficio técnico real para el proyecto.

---

## 6.2 Criterios de selección

Toda librería incorporada al proyecto deberá cumplir, como mínimo, los siguientes criterios:

- Resolver una necesidad real de la automatización.
- Aportar un beneficio técnico frente a la biblioteca estándar de Python.
- No duplicar funcionalidades ya cubiertas por otra tecnología del stack.
- Contar con mantenimiento activo y una comunidad consolidada.
- Ser estable y ampliamente utilizada en proyectos de producción.
- Integrarse correctamente con el resto de las tecnologías seleccionadas.
- Mantener la complejidad del proyecto al mínimo posible.

No se incorporarán dependencias únicamente por conveniencia, popularidad o por ofrecer funcionalidades que no serán utilizadas por la automatización.

---

## 6.3 Librerías oficiales

### BeautifulSoup4

Se adopta **BeautifulSoup4** como la librería oficial para el procesamiento y análisis del código HTML obtenido durante la automatización.

Su responsabilidad será interpretar la estructura del DOM y facilitar la extracción organizada de información.

---

### lxml

Se adopta **lxml** como parser oficial utilizado por BeautifulSoup4.

Su utilización permitirá mejorar el rendimiento durante el procesamiento del HTML sin modificar la interfaz de trabajo proporcionada por BeautifulSoup4.

---

### Pydantic v2

Se adopta **Pydantic v2** como la librería oficial para la definición, validación, serialización y deserialización de todos los modelos de datos utilizados por la automatización.

Toda la información intercambiada entre módulos deberá representarse mediante modelos Pydantic.

---

### Loguru

Se adopta **Loguru** como la librería oficial para el sistema de registro de eventos, trazabilidad y auditoría de la automatización.

Todo registro operativo deberá realizarse mediante esta librería.

---

### RapidFuzz

Se adopta **RapidFuzz** como la librería oficial para realizar comparaciones aproximadas de texto y cálculo de similitud entre cadenas cuando dichas operaciones puedan resolverse mediante algoritmos determinísticos.

---

### Tenacity

Se adopta **Tenacity** como la librería oficial para implementar políticas de reintento sobre operaciones que interactúan con recursos externos potencialmente inestables.

Su utilización permitirá centralizar la estrategia de recuperación frente a errores temporales.

---

### httpx

Se adopta **httpx** como la librería oficial para realizar solicitudes HTTP cuando dichas operaciones no requieran la utilización del navegador automatizado.

Su selección garantiza compatibilidad con arquitecturas síncronas y asíncronas.

---

## 6.4 Biblioteca estándar de Python

Además de las librerías anteriores, la automatización utilizará componentes de la biblioteca estándar de Python cuando resulten suficientes para resolver una necesidad específica.

Entre ellas se encuentran:

- pathlib
- re
- json
- hashlib
- uuid
- datetime
- time

Podrán utilizarse otras librerías de la biblioteca estándar cuando exista una necesidad técnica justificada, sin que ello implique modificar el stack tecnológico oficial.

---

## 6.5 Librerías descartadas

Durante la evaluación tecnológica se analizaron diferentes alternativas que finalmente no fueron incorporadas al proyecto por no aportar un beneficio técnico suficiente o por duplicar funcionalidades ya cubiertas por otras tecnologías seleccionadas.

Entre ellas se encuentran:

- requests
- spaCy
- NLTK
- Stanza
- jsonschema

Estas tecnologías podrán reevaluarse únicamente si en el futuro aparece un requisito funcional que justifique su incorporación.

---

## 6.6 Principios de utilización

Las librerías oficiales deberán utilizarse respetando los siguientes principios:

- Cada librería tendrá una única responsabilidad claramente definida.
- No se permitirá incorporar dependencias que dupliquen funcionalidades existentes.
- Siempre se priorizará la biblioteca estándar de Python cuando cubra adecuadamente la necesidad.
- Toda nueva dependencia deberá ser evaluada conforme a los criterios definidos en este documento antes de ser incorporada al proyecto.

---

# 7. Frameworks

## 7.1 Objetivo

Definir si la automatización requiere la adopción de uno o más frameworks como parte del stack tecnológico oficial.

La incorporación de un framework únicamente será aceptada cuando aporte un beneficio técnico real que no pueda obtenerse mediante el lenguaje de programación, la arquitectura definida o las librerías oficiales del proyecto.

---

## 7.2 Evaluación

Durante la investigación se analizaron diferentes alternativas de frameworks para Python, incluyendo frameworks de automatización, desarrollo web y scraping.

Como resultado del análisis se concluyó que la arquitectura del proyecto no requiere la incorporación de ningún framework.

Las funcionalidades necesarias serán cubiertas mediante:

- Python como lenguaje de programación.
- Arquitectura modular propia.
- Librerías oficiales definidas en este documento.
- Playwright para la automatización del navegador.
- Ollama como motor de inferencia para la inteligencia artificial.

La adopción de un framework introduciría complejidad adicional sin aportar un beneficio técnico significativo para los objetivos del proyecto.

---

## 7.3 Decisión

El proyecto **no adoptará ningún framework** como parte del stack tecnológico oficial.

La automatización será desarrollada mediante una arquitectura modular implementada directamente sobre Python y las librerías oficiales seleccionadas.

---

## 7.4 Justificación

Esta decisión se fundamenta en los siguientes criterios:

- La arquitectura definida no requiere las funcionalidades proporcionadas por un framework.
- La incorporación de un framework aumentaría la complejidad del proyecto sin aportar ventajas proporcionales.
- Se mantiene un mayor control sobre la arquitectura y la evolución del sistema.
- Se reduce el número de dependencias externas.
- Se facilita el mantenimiento y la comprensión del código.

---

## 7.5 Alcance

Si en el futuro surgiera un requisito funcional que justificara la incorporación de un framework, dicha decisión deberá someterse nuevamente al proceso de evaluación tecnológica definido en este documento antes de formar parte del stack oficial.

---

# 8. Automatización del navegador

## 8.1 Objetivo

Definir la tecnología oficial encargada de la automatización del navegador para realizar la interacción con los portales de empleo durante todas las etapas de descubrimiento, recopilación y procesamiento de ofertas.

---

## 8.2 Necesidad

La automatización requiere interactuar con aplicaciones web modernas que utilizan contenido dinámico, autenticación, JavaScript y distintos mecanismos de carga asíncrona.

Entre las operaciones que realizará el navegador se encuentran:

- Acceder a portales de empleo.
- Realizar búsquedas.
- Aplicar filtros.
- Navegar entre resultados.
- Gestionar sesiones de usuario cuando sea necesario.
- Extraer información de las ofertas.
- Descargar archivos cuando corresponda.
- Obtener el código HTML para su posterior procesamiento.

Estas necesidades requieren una herramienta de automatización robusta y compatible con aplicaciones web modernas.

---

## 8.3 Tecnologías evaluadas

Durante la investigación tecnológica se evaluaron las siguientes alternativas:

- Selenium.
- Playwright.
- Puppeteer.

Después del análisis técnico se concluyó que Playwright representa la alternativa más adecuada para los objetivos y la arquitectura del proyecto.

---

## 8.4 Tecnología seleccionada

Se adopta **Playwright** como la tecnología oficial para la automatización del navegador.

---

## 8.5 Justificación técnica

La selección de Playwright se fundamenta en los siguientes aspectos:

- Excelente compatibilidad con aplicaciones web modernas.
- Soporte nativo para Chromium, Firefox y WebKit.
- Gestión automática de esperas durante la navegación.
- API moderna y mantenida activamente.
- Excelente integración con Python.
- Alta estabilidad durante procesos de automatización prolongados.
- Excelente documentación y amplia adopción por la comunidad.

La evaluación realizada no identificó ventajas técnicas suficientes en Selenium o Puppeteer que justificaran su incorporación al proyecto.

---

## 8.6 Alcance

Playwright será responsable exclusivamente de la automatización del navegador.

Entre sus responsabilidades se encuentran:

- Control del navegador.
- Navegación entre páginas.
- Interacción con elementos de la interfaz.
- Gestión de sesiones.
- Obtención del contenido HTML.
- Capturas de pantalla cuando sean necesarias.
- Descarga de archivos.

El procesamiento del HTML obtenido será responsabilidad de BeautifulSoup4 utilizando lxml como parser, de acuerdo con las decisiones definidas en el stack tecnológico.

---

## 8.7 Restricciones

Toda automatización del navegador deberá realizarse mediante Playwright.

No se incorporarán tecnologías adicionales para automatización del navegador mientras Playwright cubra los requisitos funcionales del proyecto.

Cualquier sustitución futura deberá someterse al proceso de evaluación tecnológica definido en este documento.

---

# 9. Inteligencia artificial (LLM)

## 9.1 Objetivo

Definir la arquitectura, tecnologías y criterios oficiales para la incorporación de inteligencia artificial mediante Modelos de Lenguaje de Gran Escala (LLM), los cuales serán responsables del análisis, interpretación y generación de contenido dentro de la automatización.

---

## 9.2 Necesidad

La automatización requiere capacidades de razonamiento que no pueden resolverse únicamente mediante reglas determinísticas o algoritmos tradicionales.

El modelo de lenguaje será responsable de tareas como:

- Analizar ofertas de empleo.
- Interpretar requisitos técnicos y funcionales.
- Extraer información relevante.
- Evaluar la compatibilidad entre las ofertas y el perfil profesional.
- Generar diagnósticos y recomendaciones.
- Redactar documentos profesionales.
- Responder siguiendo instrucciones definidas mediante prompts estructurados.

---

## 9.3 Estrategia de inteligencia artificial

El proyecto adoptará una estrategia híbrida que combina un modelo local para tareas de alto volumen y un modelo cloud para tareas que requieren mayor calidad de razonamiento y generación de contenido.

El modelo local se ejecutará mediante Ollama y será utilizado para tareas repetitivas y evaluaciones determinísticas complementarias (módulo de evaluación inicial).

El modelo cloud se ejecutará mediante Ollama Cloud (plan gratuito) y será utilizado exclusivamente para tareas que requieren análisis profundo y generación de contenido profesional (módulo de procesamiento profundo).

Esta decisión equilibra:

- Sin costos por uso para tareas de alto volumen (local).
- Calidad superior donde más importa (cloud).
- Privacidad de la información sensible mediante procesamiento local.
- Independencia operativa al mantener el flujo básico funcionando sin conexión.

---

## 9.4 Motores de inferencia

El proyecto adopta dos motores de inferencia según el propósito:

### 9.4.1 Motor local

Se adopta **Ollama** como el motor local para la ejecución de modelos de lenguaje en tareas de alto volumen.

La selección de Ollama como motor local se fundamenta en:

- Ejecución completamente local.
- Instalación y administración sencillas.
- Excelente integración con Python.
- Amplio catálogo de modelos compatibles.
- Mantenimiento activo.
- Excelente documentación.

### 9.4.2 Motor cloud

Se adopta **Ollama Cloud** como el motor cloud para tareas que requieren mayor capacidad de razonamiento.

La selección de Ollama Cloud se fundamenta en:

- Acceso a modelos de gran escala sin requerir hardware local.
- Plan gratuito con modelos de alta capacidad.
- Misma interfaz de API que Ollama local, facilitando la integración.
- Sin costos operativos para el plan gratuito.

---

## 9.5 Arquitectura de integración

La automatización no accederá directamente al modelo de lenguaje.

Toda comunicación con el LLM deberá realizarse mediante un Servicio de IA interno que actuará como único punto de acceso a los motores de inferencia.

Este servicio será responsable de:

- Administrar la comunicación con los proveedores de IA (local y cloud).
- Enrutar cada solicitud al proveedor adecuado según el propósito.
- Centralizar la gestión de prompts.
- Validar las solicitudes y respuestas.
- Gestionar errores y reintentos.
- Desacoplar el resto de la arquitectura del modelo utilizado.

El enrutamiento se define mediante la sección `ia_routing` en `config.yaml`, donde se asigna cada propósito (`evaluacion`, `procesamiento`) al proveedor correspondiente (`local` o `cloud`).

Esta estrategia permitirá sustituir o rebalancear los modelos y proveedores sin modificar los módulos funcionales de la automatización.

---

## 9.6 Estrategia de utilización del modelo

El modelo de lenguaje será utilizado únicamente para tareas que requieran comprensión, razonamiento o generación de contenido.

Las operaciones determinísticas continuarán resolviéndose mediante algoritmos tradicionales y librerías especializadas.

Esta separación evita utilizar el LLM para tareas donde no aporta un beneficio técnico.

---

## 9.7 Selección de modelos

El proyecto utiliza dos modelos según el propósito y el hardware disponible:

### 9.7.1 Modelo local

- **Familia:** Qwen.
- **Modelo:** Qwen 3.5 4B (`qwen3.5:4b`).
- **Hardware objetivo:** GPU con 4 GB de VRAM (NVIDIA GTX 1650 Mobile).

La selección se fundamenta en:

- Buen seguimiento de instrucciones.
- Buen desempeño en español e inglés.
- Capacidad suficiente para clasificación y análisis básico.
- Cabe completamente en 4 GB de VRAM, garantizando velocidad.
- Compatibilidad con Ollama.

### 9.7.2 Modelo cloud

- **Modelo:** Gemma 4 31B.
- **Proveedor:** Ollama Cloud (plan gratuito).

La selección se fundamenta en:

- Alto rendimiento en razonamiento y generación de texto.
- Excelente calidad en español e inglés.
- Capacidad para análisis profundo y redacción profesional.
- Acceso gratuito mediante plan free de Ollama Cloud.

---

## 9.8 Evolución de los modelos

Los modelos definidos en este documento corresponden a la selección inicial del proyecto.

La arquitectura permitirá sustituir cualquiera de los modelos en el futuro siempre que:

- Exista evidencia técnica que justifique el cambio.
- El nuevo modelo cumpla los criterios de admisión definidos por el proyecto.
- Supere el proceso oficial de evaluación tecnológica.
- Su incorporación no afecte la arquitectura general de la automatización.

La separación por propósito (local/cloud) facilita la evolución independiente de cada modelo sin afectar al otro.

---

## 9.9 Alcance

El modelo de lenguaje será utilizado para:

- Interpretación de ofertas.
- Extracción inteligente de información.
- Evaluación de compatibilidad.
- Generación de contenido profesional.
- Clasificación y razonamiento.
- Asistencia en la toma de decisiones dentro del flujo de procesamiento.

No será utilizado para tareas determinísticas que puedan resolverse mediante algoritmos tradicionales.

---

## 9.10 Restricciones

La inteligencia artificial del proyecto deberá cumplir las siguientes restricciones:

- El modelo local debe ejecutarse mediante Ollama.
- El modelo cloud debe ser accesible mediante plan gratuito, sin costos recurrentes.
- El enrutamiento entre modelos debe ser transparente para los módulos funcionales.
- Toda comunicación debe realizarse exclusivamente mediante el Servicio de IA definido por la arquitectura.
- El flujo de evaluación inicial (módulo 3) debe poder funcionar sin conexión a Internet.
- Los modelos deben poder sustituirse en el futuro sin modificar la lógica de negocio de la automatización.

---

# 10. Base de datos

## 10.1 Objetivo

Definir el mecanismo oficial de almacenamiento persistente de la automatización, garantizando que la información pueda almacenarse, consultarse, actualizarse y mantenerse de forma sencilla, robusta y completamente local.

---

## 10.2 Necesidad

La automatización requiere almacenar de forma persistente la información generada durante su funcionamiento.

Entre los datos que deberán conservarse se encuentran:

- Ofertas de empleo.
- Empresas.
- Resultados de evaluación.
- Estado de procesamiento.
- Historial de ejecución.
- Configuración persistente.
- Información necesaria para el funcionamiento de la automatización.

El almacenamiento deberá facilitar tanto el acceso automático por parte del sistema como la consulta y edición manual por parte del usuario cuando sea necesario.

---

## 10.3 Tecnologías evaluadas

Durante la investigación se evaluaron las siguientes alternativas:

- SQLite.
- Google Sheets.
- Hoja de cálculo local.

Después del análisis técnico y considerando los objetivos del proyecto, se concluyó que una hoja de cálculo local representa la alternativa más adecuada.

---

## 10.4 Tecnología seleccionada

Se adopta una **hoja de cálculo local en formato Microsoft Excel (.xlsx)** como mecanismo oficial de almacenamiento persistente de la automatización.

La gestión de dicha hoja de cálculo se realizará mediante la librería **openpyxl**.

---

## 10.5 Justificación técnica

La selección de una hoja de cálculo local se fundamenta en los siguientes aspectos:

- Toda la información permanecerá almacenada localmente.
- No requiere instalar ni administrar un sistema gestor de bases de datos.
- Permite consultar y modificar la información utilizando una interfaz conocida por el usuario.
- Es totalmente compatible con ONLYOFFICE.
- Puede ser gestionada automáticamente desde Python mediante openpyxl.
- Reduce significativamente la complejidad de mantenimiento del proyecto.

Para el volumen de información previsto en la automatización, esta solución satisface los requisitos funcionales sin introducir la complejidad propia de un sistema gestor de bases de datos tradicional.

---

## 10.6 Organización de la información

La hoja de cálculo podrá dividirse en múltiples hojas (tabs), organizadas según las necesidades funcionales de la automatización.

La estructura definitiva será definida durante el diseño del modelo de datos del proyecto.

---

## 10.7 Acceso a la información

Toda lectura y escritura sobre la hoja de cálculo deberá realizarse exclusivamente mediante los módulos de acceso a datos desarrollados para la automatización.

No se permitirá que los módulos funcionales manipulen directamente la estructura del archivo.

Esta separación reduce el acoplamiento y facilita futuras modificaciones del sistema de almacenamiento si fueran necesarias.

---

## 10.8 Compatibilidad

El almacenamiento deberá mantenerse compatible con:

- Python.
- openpyxl.
- ONLYOFFICE.

La utilización del formato `.xlsx` garantiza además la compatibilidad con otras herramientas de hojas de cálculo que puedan adoptarse en el futuro.

---

## 10.9 Restricciones

El almacenamiento persistente del proyecto deberá cumplir las siguientes restricciones:

- Permanecer completamente local.
- Utilizar el formato oficial `.xlsx`.
- Ser gestionado mediante openpyxl.
- No depender de servicios externos.
- Permitir la consulta y edición manual mediante ONLYOFFICE cuando sea necesario.

---

# 11. Gestión de configuración y variables de entorno

## 11.1 Objetivo

Definir el mecanismo oficial para administrar la configuración de la automatización y las variables dependientes del entorno de ejecución, garantizando una separación clara entre la configuración del sistema y el código fuente.

---

## 11.2 Necesidad

La automatización requiere almacenar parámetros de configuración que podrán modificarse durante la vida útil del proyecto sin necesidad de realizar cambios en el código.

Entre ellos se encuentran:

- Directorios de trabajo.
- Ubicación de la hoja de cálculo principal.
- Ubicación de la hoja de vida.
- Ubicación del portafolio profesional.
- Directorio de documentos generados.
- Configuración del modelo de IA.
- Configuración del navegador.
- Parámetros generales de funcionamiento.

La separación entre configuración y código facilita el mantenimiento, la portabilidad y la reutilización de la automatización.

---

## 11.3 Estrategia de configuración

La configuración del proyecto se dividirá en dos componentes independientes:

### Configuración funcional

Corresponde a los parámetros que definen el comportamiento de la automatización.

Se almacenará en un archivo:

**config.yaml**

---

### Variables del entorno

Corresponden a la información específica del equipo donde se ejecuta la automatización.

Se almacenarán en un archivo:

**.env**

---

## 11.4 Archivo config.yaml

El archivo `config.yaml` contendrá la configuración funcional del proyecto.

Entre otros aspectos podrá almacenar:

- Configuración general.
- Parámetros de procesamiento.
- Configuración del navegador.
- Configuración del modelo de IA.
- Límites de procesamiento.
- Parámetros de evaluación.
- Configuración de módulos.

Su contenido estará organizado de forma jerárquica para facilitar su mantenimiento y lectura.

---

## 11.5 Archivo .env

El archivo `.env` contendrá únicamente información dependiente del entorno de ejecución.

Entre otros aspectos podrá almacenar:

- Rutas locales.
- Directorios de trabajo.
- Ubicación de Ollama.
- Ubicación de la hoja de cálculo.
- Variables específicas del equipo.

Este archivo permitirá trasladar la automatización a otro computador modificando únicamente la configuración del entorno, sin alterar el código fuente ni la configuración funcional.

---

## 11.6 Tecnologías seleccionadas

Se adoptan las siguientes tecnologías como parte del stack oficial:

### PyYAML

Será la librería oficial para la lectura y escritura del archivo `config.yaml`.

---

### python-dotenv

Será la librería oficial para la carga de variables definidas en el archivo `.env`.

---

## 11.7 Principios de utilización

La gestión de configuración deberá cumplir los siguientes principios:

- El código fuente no contendrá valores de configuración modificables.
- Toda configuración funcional deberá almacenarse en `config.yaml`.
- Toda configuración dependiente del equipo deberá almacenarse en `.env`.
- La configuración deberá cargarse automáticamente durante el inicio de la automatización.
- Los módulos accederán a la configuración mediante los mecanismos definidos por la arquitectura del proyecto.

---

## 11.8 Restricciones

La gestión de configuración deberá cumplir las siguientes restricciones:

- No almacenar información de configuración directamente en el código.
- Mantener separadas la configuración funcional y las variables del entorno.
- Utilizar exclusivamente `config.yaml` y `.env` como mecanismos oficiales de configuración.
- Garantizar que la automatización pueda trasladarse a otro equipo modificando únicamente los archivos de configuración.

---

# 12. Gestión de dependencias

## 12.1 Objetivo

Definir el mecanismo oficial para la instalación, actualización y administración de las dependencias utilizadas por la automatización, garantizando un entorno de desarrollo reproducible, estable y fácil de mantener.

---

## 12.2 Necesidad

La automatización utilizará diversas librerías externas para implementar sus funcionalidades.

Es necesario disponer de un mecanismo que permita:

- Instalar todas las dependencias del proyecto.
- Mantener versiones compatibles entre ellas.
- Reproducir el entorno de desarrollo en cualquier momento.
- Facilitar futuras actualizaciones.
- Reducir problemas derivados de incompatibilidades entre versiones.

---

## 12.3 Tecnologías evaluadas

Durante la evaluación tecnológica se analizaron las siguientes alternativas:

- pip
- Poetry
- uv

Después del análisis técnico se concluyó que `pip` representa la alternativa más adecuada para las necesidades del proyecto.

---

## 12.4 Tecnología seleccionada

Se adopta **pip** como el gestor oficial de dependencias de la automatización.

Como inventario oficial de dependencias se utilizará el archivo:

**requirements.txt**

---

## 12.5 Justificación técnica

La selección de `pip` se fundamenta en los siguientes aspectos:

- Forma parte del ecosistema oficial de Python.
- Excelente estabilidad.
- Amplia documentación.
- Compatibilidad con todas las librerías seleccionadas para el proyecto.
- Simplicidad de utilización.
- No incorpora complejidad innecesaria.

Las alternativas evaluadas ofrecen funcionalidades adicionales que no representan un beneficio significativo para la arquitectura definida.

---

## 12.6 Archivo requirements.txt

El archivo `requirements.txt` constituirá el inventario oficial de dependencias del proyecto.

En él se registrarán todas las librerías externas aprobadas como parte del stack tecnológico, indicando sus versiones correspondientes para garantizar la reproducibilidad del entorno.

No deberán incluirse librerías de la biblioteca estándar de Python.

El archivo requirements.txt constituirá además la referencia oficial de las versiones de las dependencias utilizadas por el proyecto. En caso de existir diferencias entre este documento y el archivo requirements.txt, prevalecerán las versiones registradas en este último.

---

## 12.7 Gestión de versiones

Las versiones de las dependencias deberán mantenerse controladas para evitar incompatibilidades entre componentes del sistema.

Toda incorporación, actualización o eliminación de una dependencia deberá reflejarse inmediatamente en el archivo `requirements.txt`.

---

## 12.8 Restricciones

La gestión de dependencias deberá cumplir las siguientes restricciones:

- Utilizar exclusivamente `pip` como gestor oficial.
- Mantener actualizado el archivo `requirements.txt`.
- No incorporar dependencias que no hayan sido previamente evaluadas y aprobadas.
- Evitar la duplicidad de funcionalidades entre librerías.
- Priorizar siempre la biblioteca estándar de Python cuando cubra adecuadamente una necesidad del proyecto.

---

# 13. Herramientas de desarrollo

## 13.1 Objetivo

Definir las herramientas oficiales que serán utilizadas durante el desarrollo, depuración y mantenimiento de la automatización, garantizando un entorno de trabajo estable, sencillo y compatible con el stack tecnológico definido para el proyecto.

---

## 13.2 Necesidad

El desarrollo de la automatización requiere herramientas que faciliten:

- La edición del código fuente.
- La administración del entorno de desarrollo.
- La depuración de la aplicación.
- La validación de la calidad del código.
- La verificación del tipado estático.

La selección de estas herramientas deberá priorizar la simplicidad, la estabilidad y su integración con el resto del stack tecnológico.

---

## 13.3 Tecnologías evaluadas

Durante la evaluación tecnológica se analizaron diferentes herramientas utilizadas habitualmente para el desarrollo en Python.

Como resultado del análisis se seleccionaron únicamente aquellas que aportan un beneficio técnico real para el proyecto.

---

## 13.4 Editor de código

Se adopta **Visual Studio Code** como el entorno oficial de desarrollo.

La selección se fundamenta en:

- Compatibilidad con Python.
- Excelente integración con Git.
- Amplio ecosistema de extensiones.
- Herramientas integradas de depuración.
- Estabilidad.
- Disponibilidad gratuita.

---

## 13.5 Entorno virtual

Se adopta **venv** como mecanismo oficial para la creación y administración de entornos virtuales.

Al formar parte de la biblioteca estándar de Python, no requiere dependencias adicionales y cubre completamente las necesidades del proyecto.

---

## 13.6 Formato del código

Se adopta **Black** como herramienta oficial para el formateo automático del código fuente.

Su utilización garantizará un estilo uniforme durante todo el desarrollo de la automatización.

---

## 13.7 Análisis estático

Se adopta **Ruff** como herramienta oficial para el análisis estático del código.

Su utilización permitirá detectar errores potenciales, problemas de calidad y desviaciones respecto a las buenas prácticas de desarrollo antes de la ejecución del programa.

---

## 13.8 Verificación de tipos

Se adopta **mypy** como herramienta oficial para la verificación del tipado estático del proyecto.

Su utilización complementará la validación realizada mediante Pydantic, detectando inconsistencias durante el desarrollo.

---

## 13.9 Principios de utilización

Las herramientas de desarrollo deberán utilizarse siguiendo los siguientes principios:

- Mantener un estilo de código uniforme.
- Detectar errores lo antes posible durante el desarrollo.
- Reducir la complejidad del mantenimiento.
- Favorecer la legibilidad y consistencia del código.
- Integrarse correctamente con el resto del stack tecnológico.

---

## 13.10 Restricciones

Las herramientas de desarrollo deberán cumplir las siguientes restricciones:

- Ser gratuitas.
- Mantener compatibilidad con Python y el stack tecnológico oficial.
- No duplicar funcionalidades ya cubiertas por otras herramientas.
- Incorporarse únicamente cuando aporten un beneficio técnico demostrable para el proyecto.

---

# 14. Herramientas de pruebas

## 14.1 Objetivo

Definir las herramientas oficiales para la realización de pruebas durante el desarrollo de la automatización, con el fin de verificar el correcto funcionamiento de sus componentes y reducir el riesgo de introducir errores durante la evolución del proyecto.

---

## 14.2 Necesidad

La automatización estará compuesta por múltiples módulos independientes que evolucionarán de forma progresiva.

Será necesario verificar que las nuevas funcionalidades no afecten el comportamiento de los componentes previamente desarrollados y que los resultados obtenidos sean consistentes con los requisitos del proyecto.

---

## 14.3 Tecnologías evaluadas

Durante la evaluación tecnológica se analizaron las siguientes alternativas:

- unittest
- pytest

Después del análisis técnico se concluyó que **pytest** representa la alternativa más adecuada para las necesidades del proyecto.

---

## 14.4 Tecnología seleccionada

Se adopta **pytest** como la herramienta oficial para la ejecución de pruebas automatizadas del proyecto.

---

## 14.5 Justificación técnica

La selección de pytest se fundamenta en los siguientes aspectos:

- Sintaxis sencilla y fácil de mantener.
- Excelente documentación.
- Amplia adopción dentro del ecosistema Python.
- Gran flexibilidad para diferentes tipos de pruebas.
- Excelente integración con Visual Studio Code.
- Posibilidad de ampliar sus capacidades mediante plugins cuando sea necesario.

---

## 14.6 Alcance

Las pruebas automatizadas podrán utilizarse para verificar, entre otros aspectos:

- Funcionamiento de módulos individuales.
- Integración entre componentes.
- Procesamiento de datos.
- Validación de reglas de negocio.
- Correcto funcionamiento de funciones críticas.

La implementación de pruebas se realizará cuando la complejidad o el impacto del componente lo justifiquen.

---

## 14.7 Principios de utilización

Las pruebas deberán cumplir los siguientes principios:

- Verificar el comportamiento esperado del sistema.
- Ser reproducibles.
- Mantener independencia entre sí.
- Facilitar la detección temprana de errores.
- Evolucionar junto con el código fuente.

---

## 14.8 Restricciones

Las herramientas de pruebas deberán cumplir las siguientes restricciones:

- Ser compatibles con el stack tecnológico oficial.
- Mantenerse actualizadas.
- No introducir complejidad innecesaria.
- Utilizarse principalmente para validar componentes cuya criticidad justifique la existencia de pruebas automatizadas.

---

# 15. Herramientas de documentación

## 15.1 Objetivo

Definir el formato y las herramientas oficiales para la creación, mantenimiento y actualización de la documentación del proyecto, garantizando que toda la información técnica y funcional permanezca organizada, consistente y fácilmente consultable durante todo el ciclo de vida de la automatización.

---

## 15.2 Necesidad

La automatización requiere una documentación estructurada que permita:

- Registrar las decisiones técnicas del proyecto.
- Documentar la arquitectura.
- Mantener especificaciones funcionales.
- Documentar los módulos desarrollados.
- Registrar procedimientos de instalación, configuración y mantenimiento.
- Facilitar la evolución futura del proyecto.

---

## 15.3 Tecnologías evaluadas

Durante la evaluación tecnológica se analizaron las siguientes alternativas:

- Markdown (.md)
- MkDocs
- Sphinx

Después del análisis técnico se concluyó que **Markdown** representa la alternativa más adecuada para las necesidades del proyecto.

---

## 15.4 Tecnología seleccionada

Se adopta **Markdown (.md)** como el formato oficial para toda la documentación técnica y funcional del proyecto.

---

## 15.5 Justificación técnica

La selección de Markdown se fundamenta en los siguientes aspectos:

- Formato abierto y ampliamente adoptado.
- Excelente legibilidad tanto en formato editable como renderizado.
- Integración nativa con Git.
- Compatibilidad con Visual Studio Code.
- Bajo mantenimiento.
- No requiere herramientas adicionales para su utilización.
- Facilita el versionado de la documentación junto con el código fuente.

Las alternativas evaluadas incorporan funcionalidades orientadas principalmente a la generación automática de sitios de documentación, las cuales no representan una necesidad para este proyecto.

---

## 15.6 Organización de la documentación

Toda la documentación oficial del proyecto deberá mantenerse organizada siguiendo la estructura documental definida para la automatización.

Cada documento deberá abordar una temática específica y mantenerse actualizado conforme evolucione el proyecto.

---

## 15.7 Principios de utilización

La documentación deberá cumplir los siguientes principios:

- Mantener coherencia con la implementación del proyecto.
- Actualizarse cuando se aprueben cambios relevantes.
- Permanecer organizada y estructurada.
- Evitar duplicidad de información.
- Ser clara, precisa y fácilmente consultable.

---

## 15.8 Restricciones

Las herramientas de documentación deberán cumplir las siguientes restricciones:

- Utilizar Markdown como formato oficial.
- Mantener compatibilidad con Visual Studio Code y Git.
- No incorporar herramientas adicionales de generación automática de documentación mientras no exista un requisito funcional que lo justifique.

---

# 16. Herramientas de control de versiones

## 16.1 Objetivo

Definir las herramientas oficiales para el control de versiones del código fuente y la documentación del proyecto, garantizando la trazabilidad de los cambios, la recuperación de versiones anteriores y una evolución organizada de la automatización.

---

## 16.2 Necesidad

El proyecto evolucionará de manera progresiva mediante la incorporación de nuevas funcionalidades, correcciones y mejoras.

Resulta necesario disponer de un mecanismo que permita:

- Registrar el historial de cambios.
- Recuperar versiones anteriores.
- Mantener la integridad del proyecto.
- Facilitar el desarrollo seguro de nuevas funcionalidades.
- Versionar tanto el código como la documentación oficial.

---

## 16.3 Tecnologías evaluadas

Durante la evaluación tecnológica se analizaron las siguientes alternativas:

- Git.
- Administración manual de versiones.

Después del análisis técnico se concluyó que **Git** representa la alternativa más adecuada para las necesidades del proyecto.

---

## 16.4 Tecnología seleccionada

Se adopta **Git** como el sistema oficial de control de versiones del proyecto.

Inicialmente el repositorio será administrado de forma local en el equipo donde se desarrolla la automatización.

---

## 16.5 Justificación técnica

La selección de Git se fundamenta en los siguientes aspectos:

- Es el estándar de la industria para el control de versiones.
- Permite mantener un historial completo del proyecto.
- Facilita la recuperación de versiones anteriores.
- Se integra correctamente con Visual Studio Code.
- Permite versionar conjuntamente el código y la documentación.
- No requiere servicios externos para su funcionamiento.

---

## 16.6 Alcance

Git será utilizado para versionar:

- Código fuente.
- Documentación técnica.
- Archivos de configuración.
- Recursos necesarios para el desarrollo del proyecto.

No se utilizará para almacenar archivos generados automáticamente ni información temporal.

---

## 16.7 Principios de utilización

La gestión de versiones deberá cumplir los siguientes principios:

- Registrar los cambios de forma organizada.
- Mantener un historial claro del desarrollo.
- Realizar commits únicamente cuando los cambios sean funcionalmente estables.
- Mantener sincronizados el código y la documentación.

---

## 16.8 Restricciones

El control de versiones deberá cumplir las siguientes restricciones:

- Utilizar Git como único sistema oficial de control de versiones.
- Mantener el repositorio actualizado durante todo el desarrollo del proyecto.
- No depender de plataformas remotas para el funcionamiento del sistema de control de versiones.

---

# 17. Herramientas auxiliares

## 17.1 Objetivo

Definir las herramientas complementarias que apoyarán el desarrollo, ejecución y mantenimiento de la automatización, sin formar parte directa del código fuente ni del stack principal del proyecto.

---

## 17.2 Necesidad

Durante el desarrollo y la utilización de la automatización será necesario disponer de herramientas que faciliten determinadas actividades operativas sin afectar la arquitectura del sistema.

Estas herramientas deberán complementar el funcionamiento de la automatización y aportar un beneficio práctico para el usuario.

---

## 17.3 Tecnología seleccionada

Se adopta **ONLYOFFICE** como la herramienta oficial para la consulta, edición y administración de los archivos de hoja de cálculo utilizados por la automatización.

---

## 17.4 Justificación técnica

La selección de ONLYOFFICE se fundamenta en los siguientes aspectos:

- Permite trabajar directamente con archivos en formato `.xlsx`.
- Funciona completamente de forma local.
- No requiere servicios en la nube.
- Ofrece una interfaz conocida para el usuario.
- Facilita la revisión y edición manual de la información almacenada por la automatización.
- Es compatible con el mecanismo de almacenamiento definido para el proyecto.

---

## 17.5 Alcance

ONLYOFFICE será utilizado para:

- Consultar la información almacenada por la automatización.
- Revisar resultados.
- Realizar modificaciones manuales cuando sea necesario.
- Verificar el contenido de las hojas de cálculo utilizadas por el sistema.

La automatización continuará siendo responsable de la lectura y escritura automática de los archivos mediante `openpyxl`.

---

## 17.6 Principios de utilización

Las herramientas auxiliares deberán cumplir los siguientes principios:

- Complementar el funcionamiento de la automatización.
- No sustituir componentes del stack tecnológico oficial.
- Facilitar la interacción del usuario con el sistema.
- Reducir la complejidad operativa del proyecto.

---

## 17.7 Restricciones

Las herramientas auxiliares deberán cumplir las siguientes restricciones:

- Ser gratuitas.
- Funcionar localmente.
- Mantener compatibilidad con el stack tecnológico oficial.
- No duplicar funcionalidades proporcionadas por otras tecnologías del proyecto.

---

# 18. Compatibilidad entre tecnologías

## 18.1 Objetivo

Definir los criterios de compatibilidad entre las tecnologías que conforman el stack oficial del proyecto, garantizando que todos sus componentes puedan integrarse correctamente y funcionar como un sistema único y coherente.

---

## 18.2 Principio de compatibilidad

Todas las tecnologías seleccionadas deberán ser compatibles entre sí y desempeñar una responsabilidad claramente definida dentro de la arquitectura.

No se incorporarán tecnologías que:

- Dupliquen funcionalidades existentes.
- Generen conflictos de integración.
- Introduzcan dependencias innecesarias.
- Incrementen la complejidad del proyecto sin aportar un beneficio técnico demostrable.

---

## 18.3 Compatibilidad del stack tecnológico

| Tecnología | Compatible con | Función principal |
|------------|----------------|-------------------|
| Python | Todo el stack | Lenguaje principal del proyecto. |
| Playwright | BeautifulSoup4, Tenacity, Loguru | Automatización del navegador. |
| BeautifulSoup4 + lxml | Playwright | Procesamiento y análisis del HTML. |
| Pydantic | Todo el sistema | Validación y serialización de datos. |
| Ollama | Qwen, Gemma | Motor de inferencia local para IA. |
| Ollama Cloud | Gemma 4 31B | Motor de inferencia cloud para IA. |
| Qwen 3.5 4B | Ollama | Modelo de lenguaje local. |
| Gemma 4 31B | Ollama Cloud | Modelo de lenguaje cloud. |
| openpyxl | ONLYOFFICE | Gestión del almacenamiento en archivos `.xlsx`. |
| PyYAML | python-dotenv | Gestión de la configuración del proyecto. |
| Loguru | Todo el stack | Registro de eventos y auditoría. |
| Tenacity | Playwright, Ollama, httpx | Reintentos automáticos. |
| RapidFuzz | Pydantic | Comparación aproximada de texto. |
| httpx | Tenacity, Loguru | Solicitudes HTTP cuando no se requiera el navegador. |
| Git | Todo el proyecto | Control de versiones. |

---

## 18.4 Integración arquitectónica

Cada componente del stack tecnológico deberá interactuar únicamente con los elementos necesarios para cumplir su responsabilidad.

La arquitectura deberá favorecer:

- Bajo acoplamiento.
- Alta cohesión.
- Separación de responsabilidades.
- Facilidad de mantenimiento.
- Posibilidad de evolución futura sin afectar el resto del sistema.

---

## 18.5 Compatibilidad futura

Toda nueva tecnología propuesta deberá superar un proceso de evaluación antes de incorporarse al stack oficial.

Como mínimo deberá demostrar:

- Compatibilidad técnica con las tecnologías existentes.
- Ausencia de conflictos funcionales.
- Integración con la arquitectura definida.
- Beneficio técnico claramente justificado.

---

## 18.6 Restricciones

La incorporación de nuevas tecnologías deberá cumplir las siguientes restricciones:

- Mantener la compatibilidad con el stack oficial.
- No sustituir componentes existentes sin una evaluación previa.
- No introducir dependencias redundantes.
- Preservar la estabilidad y coherencia de la arquitectura del proyecto.


---

# 19. Restricciones tecnológicas

## 19.1 Objetivo

Definir las restricciones tecnológicas que deberán respetarse durante todo el ciclo de vida del proyecto, con el fin de garantizar la coherencia del stack tecnológico, facilitar el mantenimiento de la automatización y evitar la incorporación de tecnologías que contradigan los principios definidos para el proyecto.

---

## 19.2 Software gratuito

Todas las tecnologías, herramientas, librerías y componentes incorporados al proyecto deberán ser de uso gratuito.

No se adoptarán tecnologías cuya utilización dependa de licencias de pago, suscripciones obligatorias o costos recurrentes para el funcionamiento de la automatización.

---

## 19.3 Ejecución local

La automatización deberá ejecutarse completamente en el equipo del usuario.

No dependerá de servicios externos para su funcionamiento principal.

Los componentes críticos del sistema deberán operar de forma local.

---

## 19.4 Inteligencia artificial

La inteligencia artificial deberá ejecutarse mediante modelos locales.

No se utilizarán APIs comerciales como componente principal de la automatización.

Toda interacción con el modelo de lenguaje deberá realizarse mediante la arquitectura definida para el Servicio de IA.

---

## 19.5 Compatibilidad tecnológica

Toda nueva tecnología incorporada deberá ser compatible con el stack tecnológico oficial.

No podrán introducirse componentes que generen incompatibilidades, conflictos de integración o duplicidad de funcionalidades.

---

## 19.6 Minimización de dependencias

Las dependencias externas deberán incorporarse únicamente cuando:

- Resuelvan una necesidad real del proyecto.
- Aporten una ventaja técnica demostrable.
- No exista una solución equivalente en la biblioteca estándar de Python.
- No dupliquen funcionalidades ya cubiertas por otra tecnología del stack.

---

## 19.7 Mantenibilidad

Se priorizarán tecnologías que cumplan los siguientes criterios:

- Mantenimiento activo.
- Documentación suficiente.
- Comunidad consolidada.
- Estabilidad.
- Amplia adopción dentro del ecosistema correspondiente.

---

## 19.8 Simplicidad

Cuando existan varias alternativas técnicamente equivalentes, se seleccionará aquella que:

- Introduzca menor complejidad.
- Requiera menor mantenimiento.
- Facilite la evolución futura del proyecto.
- Se integre mejor con el resto del stack tecnológico.

---

## 19.9 Portabilidad

La automatización deberá poder trasladarse a otro equipo con el menor número posible de modificaciones.

La configuración del sistema deberá mantenerse separada del código fuente para facilitar dicha portabilidad.

---

## 19.10 Restricciones generales

Durante el desarrollo del proyecto no se permitirá:

- Incorporar tecnologías sin una evaluación técnica previa.
- Duplicar funcionalidades mediante herramientas diferentes.
- Introducir dependencias que no aporten un beneficio claramente justificado.
- Modificar el stack tecnológico oficial sin actualizar previamente la documentación correspondiente.


---

# 20. Estrategia de actualización y reemplazo de tecnologías

## 20.1 Objetivo

Definir el procedimiento que deberá seguirse para actualizar, sustituir o incorporar tecnologías dentro del stack oficial del proyecto, garantizando la estabilidad de la automatización y la coherencia de la arquitectura tecnológica.

---

## 20.2 Principios generales

El stack tecnológico del proyecto deberá mantenerse lo más estable posible.

Las tecnologías seleccionadas no serán reemplazadas únicamente por la aparición de nuevas alternativas o por cambios en las tendencias del mercado.

Toda modificación deberá responder a una necesidad técnica real y aportar una mejora demostrable para el proyecto.

---

## 20.3 Criterios para la actualización

Una tecnología podrá ser actualizada cuando:

- Existan mejoras relevantes en estabilidad, rendimiento o seguridad.
- Se corrijan errores que afecten el funcionamiento del proyecto.
- La nueva versión mantenga compatibilidad con el resto del stack tecnológico.
- La actualización no implique cambios arquitectónicos injustificados.

---

## 20.4 Criterios para el reemplazo

Una tecnología podrá ser reemplazada únicamente cuando ocurra al menos una de las siguientes situaciones:

- Deje de mantenerse activamente.
- Presente problemas de compatibilidad que no puedan resolverse.
- Exista una alternativa claramente superior para las necesidades del proyecto.
- El reemplazo aporte beneficios técnicos significativos que justifiquen el costo de la migración.

El simple hecho de que exista una tecnología más reciente no constituirá un motivo suficiente para realizar un reemplazo.

---

## 20.5 Proceso de evaluación

Antes de aprobar cualquier actualización o reemplazo deberá realizarse una evaluación técnica que contemple, como mínimo:

- Compatibilidad con el stack tecnológico oficial.
- Impacto sobre la arquitectura del proyecto.
- Riesgos asociados a la migración.
- Beneficios esperados.
- Esfuerzo de implementación.
- Impacto sobre el mantenimiento futuro.

La decisión deberá quedar documentada antes de incorporarse al proyecto.

---

## 20.6 Compatibilidad durante la transición

Cuando una tecnología sea reemplazada, deberá garantizarse que la transición no comprometa:

- La integridad de la información.
- La estabilidad de la automatización.
- La compatibilidad con los demás componentes del sistema.

Siempre que sea posible, las migraciones deberán realizarse de forma controlada y verificable.

---

## 20.7 Documentación

Toda actualización o reemplazo aprobado deberá reflejarse en la documentación oficial del proyecto.

Como mínimo deberán actualizarse:

- El presente documento.
- El inventario oficial del stack tecnológico.
- La documentación técnica afectada.
- El archivo `requirements.txt`, cuando corresponda.

---

## 20.8 Restricciones

La evolución del stack tecnológico deberá cumplir las siguientes restricciones:

- No modificar tecnologías sin una evaluación técnica previa.
- No introducir cambios que incrementen innecesariamente la complejidad del proyecto.
- Mantener la coherencia con los principios tecnológicos definidos en este documento.
- Preservar la estabilidad, mantenibilidad y portabilidad de la automatización.

---

# 21. Criterios de aceptación

## 21.1 Objetivo

Definir los criterios que deberá cumplir el stack tecnológico para considerarse oficialmente aprobado como parte de la arquitectura de la automatización.

Estos criterios servirán como referencia para validar futuras incorporaciones, modificaciones o reemplazos de tecnologías.

---

## 21.2 Criterios generales

El stack tecnológico será considerado aceptado cuando cumpla, como mínimo, los siguientes criterios:

- Todas las tecnologías hayan sido evaluadas técnicamente.
- Exista una justificación documentada para cada decisión adoptada.
- No existan duplicidades funcionales entre tecnologías.
- Todas las tecnologías sean compatibles entre sí.
- El stack mantenga coherencia con la arquitectura definida para el proyecto.

---

## 21.3 Compatibilidad

Las tecnologías seleccionadas deberán integrarse correctamente entre sí sin generar conflictos funcionales o arquitectónicos.

La incorporación de un nuevo componente no deberá comprometer la estabilidad del resto del sistema.

---

## 21.4 Mantenibilidad

El stack deberá favorecer el mantenimiento del proyecto mediante:

- Tecnologías estables.
- Documentación suficiente.
- Comunidad activa.
- Bajo nivel de complejidad.
- Facilidad de actualización.

---

## 21.5 Sostenibilidad

Las tecnologías seleccionadas deberán alinearse con los principios generales del proyecto:

- Uso gratuito.
- Ejecución local.
- Independencia de servicios externos para el funcionamiento principal.
- Facilidad de mantenimiento.
- Escalabilidad acorde con las necesidades de la automatización.

---

## 21.6 Consistencia documental

Toda tecnología aprobada deberá encontrarse documentada en:

- El presente documento.
- El inventario oficial del stack tecnológico.
- La documentación técnica correspondiente, cuando aplique.

---

## 21.7 Aceptación final

El stack tecnológico se considerará oficialmente aprobado cuando cumpla la totalidad de los criterios definidos en este capítulo.

Cualquier incorporación, modificación o reemplazo posterior deberá volver a evaluarse conforme a estos mismos criterios antes de formar parte del stack tecnológico oficial.

---

# 22. Inventario oficial del stack tecnológico

## 22.1 Objetivo

Consolidar en un único inventario todas las tecnologías oficialmente aprobadas para el desarrollo, ejecución y mantenimiento de la automatización.

Este inventario constituye la referencia oficial del stack tecnológico del proyecto.

---

## 22.2 Inventario oficial

| Categoría | Tecnología oficial | Propósito |
|-----------|--------------------|-----------|
| Lenguaje de programación | Python | Desarrollo de la automatización. |
| Procesamiento de HTML | BeautifulSoup4 | Análisis y extracción de información del HTML. |
| Parser HTML | lxml | Parser utilizado por BeautifulSoup4. |
| Validación de datos | Pydantic v2 | Validación, serialización y deserialización de datos. |
| Registro de eventos | Loguru | Sistema de registro y auditoría. |
| Comparación de texto | RapidFuzz | Comparación aproximada de cadenas de texto. |
| Reintentos | Tenacity | Gestión automática de reintentos. |
| Cliente HTTP | httpx | Solicitudes HTTP cuando no se requiera el navegador. |
| Automatización del navegador | Playwright | Automatización de navegación e interacción con sitios web. |
| Inteligencia artificial (local) | Ollama | Motor de inferencia local para modelos de lenguaje. |
| Inteligencia artificial (cloud) | Ollama Cloud | Motor de inferencia cloud para modelos de lenguaje (plan gratuito). |
| Modelo de lenguaje (local) | Qwen 3.5 4B | Modelo local para evaluación y tareas de alto volumen. |
| Modelo de lenguaje (cloud) | Gemma 4 31B | Modelo cloud para procesamiento profundo y generación de contenido. |
| Almacenamiento persistente | Archivo `.xlsx` | Almacenamiento oficial de la información del proyecto. |
| Gestión del archivo `.xlsx` | openpyxl | Lectura y escritura de la hoja de cálculo. |
| Configuración | config.yaml | Configuración funcional de la automatización. |
| Variables de entorno | .env | Configuración específica del entorno de ejecución. |
| Gestión de configuración | PyYAML | Lectura y escritura de archivos YAML. |
| Variables de entorno | python-dotenv | Carga automática del archivo `.env`. |
| Gestión de dependencias | pip | Instalación y administración de dependencias. |
| Inventario de dependencias | requirements.txt | Registro oficial de librerías externas. |
| Editor de código | Visual Studio Code | Desarrollo de la automatización. |
| Entorno virtual | venv | Aislamiento del entorno de desarrollo. |
| Formateo de código | Black | Formato automático del código fuente. |
| Análisis estático | Ruff | Análisis de calidad del código. |
| Tipado estático | mypy | Verificación de tipos. |
| Pruebas | pytest | Pruebas automatizadas. |
| Documentación | Markdown (.md) | Documentación técnica y funcional. |
| Control de versiones | Git | Versionado del proyecto. |
| Herramienta auxiliar | ONLYOFFICE | Consulta y edición manual de los archivos `.xlsx`. |

---

## 22.3 Observaciones

El presente inventario constituye el stack tecnológico oficial de la automatización.

Cualquier incorporación, sustitución o eliminación de una tecnología deberá cumplir el proceso de evaluación definido en este documento antes de formar parte del stack oficial.

Este inventario deberá mantenerse actualizado durante toda la vida útil del proyecto.
