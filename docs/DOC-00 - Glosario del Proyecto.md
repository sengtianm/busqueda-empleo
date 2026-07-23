# Documento 0
# Glosario del Proyecto

> **Objetivo**
>
> Establecer la definición oficial de todos los conceptos utilizados durante el proyecto, garantizando una terminología uniforme en la documentación, el desarrollo y el mantenimiento de la automatización.

---

# Principios del glosario

- Cada término tendrá una única definición oficial.
- Ningún documento redefinirá un término existente.
- Todo concepto nuevo deberá incorporarse a este documento.
- Las definiciones serán independientes de la tecnología utilizada.
- Los códigos de identificación son permanentes y nunca se reutilizarán.

---

# Categorías

1. Conceptos generales
2. Actores
3. Flujo funcional
4. Procesamiento
5. Datos
6. Decisiones
7. Arquitectura
8. Gestión

---

# 1. Conceptos generales

## GLO-001
### Automatización

Sistema diseñado para ejecutar de forma autónoma las tareas repetitivas relacionadas con la búsqueda de empleo, manteniendo al usuario como responsable de las decisiones estratégicas.

---

## GLO-002
### Oferta de empleo

Publicación de una oportunidad laboral obtenida desde una fuente de empleo y registrada dentro del sistema para su procesamiento.

---

## GLO-003
### Fuente de empleo

Plataforma, sitio web, API o cualquier otro origen desde el cual la automatización obtiene oportunidades laborales.

---

## GLO-004
### Perfil profesional

Conjunto de información profesional utilizada para evaluar la compatibilidad del usuario con una oferta.

---

## GLO-005
### Compatibilidad

Grado de coincidencia entre el perfil profesional del usuario y los requisitos de una oferta.

---

## GLO-006
### Prioridad

Nivel asignado a una oferta según los criterios de evaluación establecidos.

---

## GLO-007
### Candidatura

Conjunto de recursos preparados para apoyar una postulación a una oferta de empleo.

---

## GLO-008
### Insumo

Documento, análisis o cualquier otro recurso generado por la automatización para apoyar una candidatura.

---

# 2. Actores

## GLO-009
### Usuario

Persona propietaria de la automatización y responsable de las decisiones estratégicas.

---

## GLO-010
### Dependencia externa

Sistema, servicio o plataforma con la que interactúa la automatización para obtener información o ejecutar procesos.

---

# 3. Flujo funcional

## GLO-011
### Flujo funcional

Secuencia ordenada de procesos que sigue una oferta desde su descubrimiento hasta la finalización de su procesamiento.

---

## GLO-012
### Proceso funcional (PF)

Etapa específica dentro del flujo funcional.

---

## GLO-013
### Ciclo de vida

Conjunto de etapas funcionales por las que puede pasar una oferta durante su permanencia en el sistema.

---

## GLO-014
### Estado del ciclo de vida

Etapa funcional en la que se encuentra actualmente una oferta.

---

## GLO-015
### Estado operativo

Condición técnica u operativa de una oferta durante su procesamiento.

Ejemplos:

- En ejecución
- En espera
- Reintentando
- Pausada
- Error

---

# 4. Procesamiento

## GLO-016
### Descubrimiento

Proceso mediante el cual la automatización identifica nuevas ofertas de empleo.

---

## GLO-017
### Preparación

Proceso de limpieza, normalización y validación de la información obtenida.

---

## GLO-018
### Evaluación inicial

Proceso mediante el cual la automatización calcula el nivel de compatibilidad de una oferta aplicando las reglas definidas.

---

## GLO-019
### Procesamiento profundo

Proceso de análisis detallado de una oferta para generar información estratégica e insumos para la candidatura.

---

## GLO-020
### Normalización

Transformación de la información a formatos uniformes para facilitar su procesamiento.

---

## GLO-021
### Validación

Proceso mediante el cual se verifica que una oferta cumple las condiciones necesarias para continuar el flujo funcional.

---

## GLO-022
### Reprocesamiento

Nueva ejecución de una o varias etapas del flujo funcional sobre una oferta previamente procesada.

---

## GLO-023
### Duplicado

Oferta que representa la misma oportunidad laboral que otra ya registrada en el sistema.

---

# 5. Datos

## GLO-024
### Entrada

Información recibida por la automatización desde una fuente externa.

---

## GLO-025
### Dato interno

Información generada y mantenida por la automatización para controlar su funcionamiento.

---

## GLO-026
### Salida

Información entregada por la automatización como resultado de su procesamiento.

---

## GLO-027
### Historial

Registro cronológico de todos los eventos relacionados con una oferta.

---

## GLO-028
### Trazabilidad

Capacidad de reconstruir el recorrido completo de una oferta, incluyendo acciones, decisiones, estados y resultados.

---

# 6. Decisiones

## GLO-029
### Acción automática

Actividad operativa ejecutada automáticamente por la automatización sin requerir una decisión.

---

## GLO-030
### Decisión automática

Elección realizada por la automatización utilizando reglas previamente documentadas.

---

## GLO-031
### Recomendación

Sugerencia generada por la automatización para apoyar la toma de decisiones del usuario.

---

## GLO-032
### Decisión estratégica

Decisión reservada exclusivamente al usuario debido a su impacto personal, profesional o legal.

---

## GLO-033
### Regla de negocio

Condición documentada que determina cómo debe actuar la automatización en una situación específica.

---

## GLO-034
### Regla funcional

Norma permanente que define el funcionamiento general del sistema.

---

# 7. Arquitectura

## GLO-035
### Motor de procesos

Componente encargado de ejecutar y coordinar el flujo funcional de la automatización.

---

## GLO-036
### Motor de decisiones

Componente encargado de aplicar las reglas de negocio para producir decisiones automáticas y recomendaciones.

---

## GLO-037
### Módulo

Componente funcional independiente que implementa una parte específica de la automatización.

---

## GLO-038
### Configuración

Conjunto de parámetros que determinan el comportamiento de la automatización.

---

# 8. Gestión

## GLO-039
### Auditoría

Capacidad del sistema para justificar cada acción, decisión y cambio de estado mediante registros verificables.

---

## GLO-040
### Métrica

Indicador utilizado para medir el rendimiento, funcionamiento o calidad de la automatización.

---

## GLO-041
### Registro (Log)

Evento almacenado por el sistema para documentar la ejecución de procesos, decisiones, errores o acciones relevantes.

---

## GLO-042
### Error

Situación que impide la ejecución normal de un proceso y requiere una estrategia de recuperación o intervención.

---

## GLO-043
### Excepción

Situación no habitual contemplada por las reglas del sistema que modifica el flujo normal de procesamiento sin representar necesariamente un error.
