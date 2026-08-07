# Especificación Canónica — Nodo INICIO

**Versión:** 1.3 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
INICIO — Arranque de la corrida e inicialización del contexto de ejecución.

### 1.2 Posición en el flujo
Punto de entrada único del módulo. Precede a toda decisión y acción de negocio. El elemento punteado "Descubrimiento de oportunidades" es el rótulo/disparador del módulo, **no** un nodo ejecutable. Ninguna decisión posterior (empezando por "¿Existe al menos una fuente/plataforma de empleo configurada?", que opera sobre la lista filtrada) puede ejecutarse sin el contexto que este nodo produce.

### 1.3 Objetivo
Instanciar la corrida y preparar el contexto de ejecución (trazabilidad, configuración validada y filtrada, conexiones, concurrencia y estado inicial) para que los nodos posteriores consuman un contexto listo y se concentren exclusivamente en el flujo de negocio.

### 1.4 Descripción funcional
Al recibir el disparador de ejecución, el nodo: (1) crea la instancia de corrida con identificador único y marca de tiempo; (2) carga la configuración y valida el nivel global (artefacto legible, estructura general coherente, identificadores únicos); (3) verifica disponibilidad y permisos de escritura de las bases de datos del módulo; (4) valida concurrencia mediante un bloqueo persistente; (5) valida el nivel por fuente (ficha completa: esquema de acceso, `sets_de_filtros`, `politicas_de_captura` consistente si presente) y filtra la lista, descartando fuentes incompletas con evento crítico; (6) inicializa el estado de la corrida (iterador de fuentes sobre la lista filtrada y contadores); (7) entrega el control al siguiente nodo. Cualquier error fatal de inicialización o una concurrencia activa producen terminación controlada en "Finalizar Proceso" con el estado correspondiente, antes de tocar cualquier fuente de empleo.

**Separación de responsabilidades:**
- *Flujo de negocio:* arrancar la corrida y verificar precondiciones operativas. Este nodo **no** accede a fuentes de empleo, **no** aplica filtros, **no** consulta ofertas y **no** valida si existen fuentes configuradas.
- *Implementación técnica:* trazabilidad (`run_id`), conexiones, bloqueo de concurrencia y estado inicial.
- *Límite de validación:* INICIO garantiza "ficha completa y consistente"; **no** garantiza "ingreso exitoso" ni "captura exitosa". No accede al almacén seguro de credenciales ni a las plataformas (RN-09).

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos por set, captura y almacena la información original de las ofertas según políticas de captura por fuente; **no** interpreta, clasifica, puntúa ni decide adecuación de oportunidades. Este nodo no debe contener ninguna lógica de ese tipo.

### 1.5 Entradas
- Disparador de ejecución (manual o programado; el nodo no distingue entre ambos).
- Almacén de configuración de la automatización (fuentes con ficha de acceso, `sets_de_filtros` y `politicas_de_captura` por fuente, parámetros globales —incluidos valores por defecto de políticas de captura—, parámetros de conexión).
- Estado persistente de bloqueo de ejecuciones (si existe).

### 1.6 Salidas
- Contexto de ejecución inicializado: `run_id`, marca de tiempo de inicio, lista de fuentes filtrada a fuentes estructuralmente válidas (cada una con su ficha: acceso, `sets_de_filtros`, `politicas_de_captura` o defectos globales), iterador de fuentes en estado "ninguna fuente seleccionada aún", contadores/variables de sesión, conexiones activas, bloqueo adquirido.
- Eventos de descarte por fuente incompleta en "errores o sucesos" (si aplica).
- Control al nodo siguiente (camino normal).
- Terminación en "Finalizar Proceso" con estado *error* o *concurrencia* (camino de excepción).

### 1.7 Reglas de negocio
- **RN-01:** Toda corrida se identifica de forma única (`run_id`); todo registro generado por el módulo (errores, sucesos, sesiones, ofertas) queda enlazado a su `run_id`.
- **RN-02:** Solo puede existir una ejecución activa del módulo a la vez (bloqueo de concurrencia).
- **RN-03:** El iterador de fuentes se reinicia al inicio de cada corrida: cada corrida recorre todas las fuentes configuradas desde la primera. *Formalizada en el nodo "¿Quedan fuentes por procesar en esta corrida?" v1.0.*
- **RN-04:** Este nodo no valida si existen fuentes configuradas; esa validación pertenece exclusivamente al nodo siguiente.
- **RN-05:** Este nodo no accede a fuentes de empleo ni ejecuta búsquedas.
- **RN-06:** Todo error fatal de inicialización termina la corrida antes de cualquier procesamiento.
- **RN-07:** Los identificadores de fuente son únicos por configuración. La validación se ejecuta en este nodo y sostiene el contrato de trazabilidad por `source_id` de los nodos posteriores (RN-06 del nodo "Seleccionar la siguiente fuente pendiente").
- **RN-08:** Toda fuente debe tener su ficha completa y consistente: esquema de acceso (URL/plataforma, tipo de acceso `publico|con_autenticacion`, referencia de credenciales si `con_autenticacion`, criterio verificable de ingreso exitoso, timeout), `sets_de_filtros` (lista no vacía de sets; cada set es una lista de filtros, posiblemente vacía = búsqueda base) y, si presente, `politicas_de_captura` consistente. Una fuente con ficha incompleta o inconsistente se descarta en el arranque con evento crítico y no entra a la iteración; la corrida continúa con las válidas.
- **RN-09:** Este nodo no ejecuta validaciones runtime: resolución de credenciales en el almacén seguro, validez de credenciales, alcanzabilidad de plataformas, cumplimiento de criterios de éxito y aplicabilidad de filtros pertenecen a "Entrar a la fuente seleccionada" (y sus decisiones sucesoras).
- **RN-10:** El mecanismo de captura (masivo vs. incremental) es propiedad del adaptador de plataforma; la configuración no lo define, solo lo acota mediante `politicas_de_captura` (límites y pausas). Justificación: el mecanismo depende de lo que la plataforma permite (técnico); configurarlo generaría inconsistencias fuente-adaptador.
- **RN-11:** `politicas_de_captura` ausente o parcial en una fuente → se aplican los valores por defecto globales; si presente, se valida consistencia (rangos y tipos).

### 1.8 Validaciones
- **VAL-01 (run_id):** unicidad y no nulidad del identificador generado.
- **VAL-02 (configuración, nivel global):** almacén existente y legible; estructura general consistente; identificadores de fuente únicos (RN-07). **No** se valida aquí la completitud por fuente (VAL-06) ni si la lista está vacía (RN-04).
- **VAL-03 (bases de datos):** las conexiones abiertas y prueba de escritura exitosa en cada una, sin confirmación definitiva (rollback posterior).
- **VAL-04 (bloqueo):** estado de bloqueo legible; evaluación de obsolescencia por marca de tiempo contra umbral configurable; timestamps coherentes.
- **VAL-05 (contexto final):** contexto completo (run_id, lista filtrada, conexiones, bloqueo, estado) antes de entregar control.
- **VAL-06 (ficha por fuente):** cada fuente posee esquema de acceso completo, `sets_de_filtros` no vacío y consistente, y `politicas_de_captura` consistente si presente (RN-08, RN-11); las que no lo cumplen se descartan (ERR-12), sin abortar la corrida.

### 1.9 Condiciones
- **Continuación normal:** nivel global de configuración válido + bases de datos disponibles + sin concurrencia activa. Los descartes por fuente (ERR-12) no impiden la continuación.
- **Terminación:** configuración ausente/ilegible/corrupta; identificadores de fuente duplicados; base de datos indisponible/bloqueada/sin permisos; concurrencia activa (terminación controlada, no falla); estado de bloqueo no decidible (aborto).
- **Descarte por fuente:** no termina la corrida; emite evento crítico y filtra la lista (incluye ficha de acceso incompleta, `sets_de_filtros` vacío/inválido o `politicas_de_captura` inconsistente). Si tras el filtrado no queda ninguna fuente, el flujo siguiente lo resuelve con terminación normal `sin_fuentes` (RN-04).

### 1.10 Ramas y salidas del nodo
No es nodo de decisión (sin ramas Sí/No). Salidas:
- **Normal:** → decisión "¿Existe al menos una fuente/plataforma de empleo configurada?" (opera sobre la lista filtrada).
- **Excepción:** → "Finalizar Proceso" con estados *error* o *concurrencia*. *(Cambio aprobado al diagrama: se agrega esta rama; los motivos/estados de "Finalizar Proceso" aprobados a la fecha —error, concurrencia, sin_fuentes, corrida_completada— se formalizarán al llegar a ese nodo.)*

### 1.11 Manejo de errores y excepciones
Definiciones: *aborto* = terminación inmediata por falla no recuperable; *terminación controlada* = finalización sin procesamiento (concurrencia); *descarte* = exclusión de una fuente de la iteración con evento crítico, sin detener la corrida. Registro: en "errores o sucesos" si está disponible; de lo contrario, registro crítico local (consola/archivo, documentado en la implementación). Todo registro incluye `run_id`, marca de tiempo, tipo (error/suceso) y descripción; los descartes incluyen además `source_id`.

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Colisión o fallo de generación de `run_id` | 1 | Registro crítico local | Reintento único; si persiste, aborto | error |
| ERR-02 | Configuración ausente | 2 | Registro crítico local (aún sin BD conectada) | Aborto | error |
| ERR-03 | Configuración ilegible | 2 | Registro crítico local | Aborto | error |
| ERR-04 | Configuración corrupta / estructura global inconsistente | 2 | Registro crítico local | Aborto | error |
| ERR-05 | BD indisponible / bloqueada / sin permisos | 3 | Evento crítico en "errores o sucesos" si accesible; si no, local | Aborto | error |
| ERR-06 | Concurrencia activa (otra corrida en ejecución) | 4 | Evento "finalización por concurrencia" | Terminación controlada | concurrencia |
| ERR-07 | Bloqueo obsoleto (corrida caída; antigüedad > umbral configurable) | 4 | Suceso de sobrescritura | Sobrescribir bloqueo y continuar | — (continúa) |
| ERR-08 | Estado de bloqueo no decidible | 4 | Evento crítico | Aborto | error |
| ERR-09 | Contienda de adquisición de bloqueo (dos corridas simultáneas) | 4 | — | Criterio de atomicidad/unicidad en la adquisición; el perdedor cae en ERR-06 | concurrencia |
| ERR-10 | Falla interna de inicialización de estado | 6 | Evento crítico en "errores o sucesos" | Aborto | error |
| ERR-11 | Identificadores de fuente duplicados en la configuración | 2 | Registro crítico local | Aborto | error |
| ERR-12 | Ficha por fuente incompleta o inconsistente (esquema de acceso, `sets_de_filtros` vacío/inválido, `politicas_de_captura` inconsistente) | 5 | Evento crítico en "errores o sucesos" con `run_id` + `source_id` | Descartar la fuente y continuar con las válidas | — (continúa) |

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** ninguno (entrada del módulo).
- **Sucesor normal:** "¿Existe al menos una fuente/plataforma de empleo configurada?" (sobre lista filtrada).
- **Sucesor de excepción:** "Finalizar Proceso".
- **Contrato entregado:** el contexto de ejecución completo es la única interfaz con los nodos posteriores; ningún nodo posterior debe reinicializar conexiones ni estado de corrida. La lista de fuentes del contexto contiene únicamente fuentes estructuralmente válidas (RN-08), cada una con `sets_de_filtros` y políticas de captura resueltas (propias o por defecto); el iterador de fuentes y las decisiones operan sobre ella.
- **Impactos aprobados sobre nodos futuros:**
  1. `run_id` deberá registrarse en las bases de datos del módulo (afecta esquemas de los nodos de registro).
  2. La liberación del bloqueo corresponderá al nodo "Finalizar Proceso".
  3. La RN-03 quedó formalizada en el nodo "¿Quedan fuentes por procesar en esta corrida?" v1.0.
  4. La unicidad de identificadores (RN-07) sostiene la trazabilidad por `source_id` definida en el nodo "Seleccionar la siguiente fuente pendiente" (RN-06 de ese nodo).
  5. "Entrar a la fuente seleccionada" asume ficha de acceso completa (sin revalidación estructural) y es el propietario exclusivo de las validaciones runtime (RN-09).
  6. "Aplicar filtros básicos" v1.1 iterará por `sets_de_filtros` de la fuente corriente; el iterador de sets se reinicia al cambiar de fuente (reedición menor de "Seleccionar la siguiente fuente pendiente" a señalar en su turno).
  7. "Capturar ofertas" consumirá `politicas_de_captura` resueltas (propias o por defecto) y el mecanismo de captura lo definirá su adaptador (RN-10).

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología: no impone lenguaje, librerías ni motor de BD.
- El contexto de ejecución debe implementarse como una única estructura/objeto que se transmite a todos los nodos posteriores.
- El bloqueo debe ser persistente (p. ej., registro en BD con `run_id` y marca de tiempo); el umbral de obsolescencia es un parámetro de configuración.
- El registro crítico local es el mecanismo de respaldo cuando "errores o sucesos" no está disponible; su destino (consola/archivo) debe quedar documentado.
- La prueba de escritura de VAL-03 debe revertirse (rollback) para no dejar datos de prueba.
- Orden de pasos justificado: la dependencia de datos obliga a leer la configuración (con sus parámetros de conexión) antes de abrir bases de datos; la validación por fuente se ejecuta después de abrir BD y adquirir el bloqueo para poder persistir eventos de descarte en "errores o sucesos" y evitar trabajo duplicado en corridas concurrentes.
- INICIO no accede al almacén seguro de credenciales ni a las plataformas (RN-09); la referencia de credenciales se valida solo como campo presente y consistente.
- `politicas_de_captura`: resolver valores por defecto globales en la carga (RN-11) y exponer en la ficha los valores efectivos; rangos válidos: `max_paginas` ≥ 1, `max_ofertas_por_corrida` ≥ 1, `pausa_entre_lotes` ≥ 0; `estrategia_anti_bloqueo` dentro del conjunto definido por la implementación.
- `sets_de_filtros`: preservar orden de configuración (define el orden de iteración de sets); un set vacío = búsqueda base.
- No implementar en este nodo lógica de negocio del módulo (fuentes, filtros, ofertas, captura) ni la validación de existencia de fuentes (RN-04, RN-05).

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Recibir disparador e instanciar la corrida | Evento de disparo (manual o programado) | Crear instancia de ejecución; generar `run_id` único; registrar marca de tiempo de inicio | Instancia de corrida (`run_id`, timestamp) | VAL-01 | ERR-01 |
| 2 | Cargar configuración y validar nivel global | Almacén de configuración (fuentes, sets de filtros, políticas de captura, parámetros globales y de conexión) | Leer almacén; validar nivel global (VAL-02): legibilidad, estructura general, unicidad de identificadores (RN-07). No valida completitud por fuente (VAL-06) ni lista vacía (RN-04) | Configuración cruda cargada en contexto | VAL-02 | ERR-02, ERR-03, ERR-04, ERR-11 |
| 3 | Verificar disponibilidad de bases de datos | Parámetros de conexión de las bases de datos del módulo: "Ofertas Totales", "errores o sucesos", "control de sesiones" y las demás que correspondan | Abrir las conexiones; prueba de escritura sin confirmación definitiva (rollback) | Conexiones disponibles en contexto | VAL-03 | ERR-05 |
| 4 | Validar concurrencia (bloqueo) | `run_id`; estado de bloqueo persistente; umbral de obsolescencia configurable | Leer bloqueo. Activo y no obsoleto → evento y terminación controlada. Obsoleto → sobrescribir, registrar suceso y continuar. Inexistente → marcar bloqueo activo con `run_id` y timestamp | Bloqueo adquirido, o terminación controlada en "Finalizar Proceso" (estado concurrencia) | VAL-04 | ERR-06, ERR-07, ERR-08, ERR-09 |
| 5 | Validar fichas por fuente y filtrar lista | Configuración cruda en contexto | Por cada fuente, validar ficha completa (VAL-06/RN-08): esquema de acceso, `sets_de_filtros` no vacío y consistente, `politicas_de_captura` consistente si presente; resolver políticas efectivas con defectos globales (RN-11). Ficha válida → conservar. Ficha incompleta/inconsistente → evento crítico con `run_id` + `source_id` y descarte (ERR-12) | Lista filtrada de fuentes estructuralmente válidas (con políticas efectivas) en contexto; eventos de descarte | VAL-06 | ERR-12 (por fuente, no aborta) |
| 6 | Inicializar estado de la corrida | `run_id`; lista filtrada; semántica del iterador (RN-03: reinicio por corrida) | Fijar iterador de fuentes en "ninguna fuente seleccionada aún" sobre la lista filtrada; inicializar contadores y variables de sesión | Contexto de ejecución completo | Iterador en estado inicial; contadores en cero | ERR-10 |
| 7 | Entregar control | Contexto de ejecución completo | Cerrar el nodo y entregar control y contexto al siguiente nodo | Flujo hacia "¿Existe al menos una fuente/plataforma configurada?" | VAL-05 | Contexto incompleto (no debería ocurrir): tratar como ERR-10 |

---

# Especificación Canónica — Nodo Decisión: "¿Existe al menos una fuente/plataforma de empleo configurada?"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Decisión de existencia de fuentes configuradas — "¿Existe al menos una fuente/plataforma de empleo configurada?".

### 1.2 Posición en el flujo
Primera decisión de negocio del módulo, inmediatamente después de INICIO. Su posición es definitiva: sin fuentes configuradas no hay nada que buscar, y la evaluación es la más barata del flujo. No requiere reubicación ni cambio estructural en el diagrama.

### 1.3 Objetivo
Decidir si la corrida continúa el flujo de descubrimiento o termina de forma controlada, según exista o no al menos una fuente configurada. Evita ejecutar el flujo completo sin datos de trabajo.

### 1.4 Descripción funcional
El nodo consume el contexto de ejecución producido por INICIO, lee la lista de fuentes desde la configuración ya cargada en memoria (sin releer el almacén), evalúa si la lista contiene al menos un elemento y bifurca: con resultado Sí entrega el control al siguiente nodo con el contrato "lista de fuentes no vacía"; con resultado No fija el motivo de terminación `sin_fuentes` (tipo suceso, no error) y entrega el control a "Finalizar Proceso", que es el punto único de registro de terminaciones. El nodo no realiza I/O al almacén de configuración, no accede a fuentes de empleo y no revalida la estructura de la configuración.

**Separación de responsabilidades:**
- *Flujo de negocio:* primera condición de continuidad del módulo (propiedad exclusiva de este nodo según RN-04 de INICIO).
- *Implementación técnica:* evaluación pura en memoria sobre el contexto; sin efectos secundarios salvo fijar el motivo de terminación en la rama No.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos, captura y almacena información original de ofertas; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no contiene lógica de ese tipo ni acceso a fuentes.

### 1.5 Entradas
- Contexto de ejecución de INICIO: configuración cargada y validada estructuralmente (lista de fuentes), `run_id`, conexiones activas, bloqueo adquirido.

### 1.6 Salidas
- **Rama Sí:** control al nodo "¿Es la primera ejecución del ciclo?" con el contrato "lista de fuentes no vacía".
- **Rama No:** control a "Finalizar Proceso" con motivo de terminación `sin_fuentes` (tipo suceso).
- **Falla interna (única excepción):** control a "Finalizar Proceso" con estado *error* (ver ERR-01).

### 1.7 Reglas de negocio
- **RN-01:** El nodo evalúa exclusivamente sobre el contexto en memoria; el contexto es la única fuente de verdad. Prohibido releer el almacén de configuración.
- **RN-02:** "Fuente configurada" = presente en la configuración cargada. No existen estados habilitada/deshabilitada en esta etapa del diseño.
- **RN-03:** El nodo no revalida la estructura de la configuración (responsabilidad ya ejecutada por INICIO, VAL-02/VAL-05).
- **RN-04:** La ausencia de fuentes es un estado de configuración válido, no una falla: la rama No produce terminación controlada con motivo `sin_fuentes`, tipo suceso (no error).
- **RN-05:** El nodo no registra eventos ni errores por sí mismo; todo registro de terminación lo realiza "Finalizar Proceso" (punto único), con `run_id`, marca de tiempo, tipo y descripción (RN-01 de INICIO).
- **RN-06:** Contrato de la rama Sí: todos los nodos posteriores asumen lista de fuentes no vacía; ningún nodo posterior revalida existencia de fuentes.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** El contexto contiene la lista de fuentes y es accesible antes de evaluar.
- **VAL-02:** La evaluación se realiza exclusivamente sobre la lista leída en el paso 1; conteo entero ≥ 0; sin revalidación estructural.
- **VAL-03:** La rama Sí solo se ejecuta con resultado de condición verdadero (conteo > 0).
- **VAL-04:** En la rama No, el motivo `sin_fuentes` queda fijado en el contexto junto con `run_id` y marca de tiempo antes de entregar control.

### 1.9 Condiciones
- **Continuación (Sí):** conteo de fuentes > 0.
- **Terminación controlada (No):** conteo de fuentes == 0 → "Finalizar Proceso" con motivo `sin_fuentes`.
- **Aborto:** contexto sin configuración o incompleto (falla interna; ver ERR-01) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
Nodo de decisión binaria:
- **Sí** (≥ 1 fuente configurada) → "¿Es la primera ejecución del ciclo?".
- **No** (0 fuentes configuradas) → "Finalizar Proceso" (motivo `sin_fuentes`, tipo suceso).

### 1.11 Manejo de errores y excepciones
Única excepción del nodo; el registro lo ejecuta "Finalizar Proceso" o el mecanismo disponible según contrato de INICIO:

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Contexto sin configuración o incompleto (no debería ocurrir por VAL-02/VAL-05 de INICIO) | 1 | Evento crítico en "errores o sucesos" | Aborto | error |

Escenarios límite cubiertos: lista vacía (rama No, no es error); lista presente pero vacía tras carga válida (idem); contexto corrupto en tránsito (ERR-01). No existen otras condiciones de error: la evaluación es pura sobre datos ya validados.

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** INICIO (provee el contexto de ejecución).
- **Sucesor normal (Sí):** "¿Es la primera ejecución del ciclo?". *Pendiente: al llegar a ese nodo se propondrá su redefinición según RN-03 de INICIO (reinicio del iterador por corrida); la salida Sí de este nodo no cambia.*
- **Sucesor de terminación (No):** "Finalizar Proceso" con motivo `sin_fuentes`.
- **Sucesor de aborto (ERR-01):** "Finalizar Proceso" con estado *error*.
- **Contrato entregado:** rama Sí garantiza lista no vacía (RN-06); rama No garantiza motivo de terminación fijado en el contexto (VAL-04).
- **Impactos aprobados sobre nodos futuros:**
  1. Ningún nodo posterior revalida existencia de fuentes (RN-06).
  2. "Finalizar Proceso" amplía su contrato de motivos/estados con `sin_fuentes` (se formalizará al llegar a ese nodo).
- **Estado del diagrama:** no se requieren cambios al diagrama para este nodo más allá de los ya aprobados (rama de excepción de INICIO y estados de Finalizar Proceso).

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Nodo de evaluación pura: sin I/O al almacén, sin acceso a red/fuentes, sin escritura en bases de datos. El único efecto colateral admisible es fijar el motivo de terminación en el contexto (rama No).
- No implementar revalidación estructural de la configuración ni lógica de estados de fuente (RN-02, RN-03).
- El suceso de terminación `sin_fuentes` se registra en "Finalizar Proceso" con `run_id`, marca de tiempo, tipo suceso y descripción; este nodo solo fija el motivo en el contexto.
- La lectura de la lista debe provenir del mismo objeto de contexto definido en INICIO; no copiar ni transformar la lista en este nodo.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer lista de fuentes del contexto | Contexto de ejecución (configuración cargada y validada en INICIO) | Acceder a la lista de fuentes del contexto; no releer el almacén (RN-01) | Lista de fuentes (posiblemente vacía) | VAL-01 | ERR-01 |
| 2 | Evaluar condición "al menos una fuente configurada" | Lista de fuentes | Contar elementos; condición = conteo > 0; sin revalidación estructural (RN-03) | Resultado booleano (Sí/No) | VAL-02 | Ninguna aplicable |
| 3 | Rama Sí — Entregar control | Resultado = Sí; contexto | Cerrar el nodo y entregar control con contrato "lista de fuentes no vacía" (RN-06) | Flujo hacia "¿Es la primera ejecución del ciclo?" | VAL-03 | Ninguna |
| 4 | Rama No — Fijar motivo y entregar control | Resultado = No; `run_id` | Fijar en el contexto el motivo de terminación `sin_fuentes` (tipo suceso, no error; RN-04); entregar control a Finalizar Proceso; el registro del suceso lo realiza ese nodo (RN-05) | Flujo hacia Finalizar Proceso (motivo `sin_fuentes`) | VAL-04 | Ninguna |

---

# Especificación Canónica — Nodo Decisión: "¿Quedan fuentes por procesar en esta corrida?"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Decisión de control de iteración de fuentes — "¿Quedan fuentes por procesar en esta corrida?".

### 1.2 Posición en el flujo y estado del diagrama
Punto único de control del bucle de fuentes: toda pasada (arranque de la corrida o retorno tras terminar o fallar una fuente) pasa por este nodo. Recibe el flujo inicial de la rama Sí de "¿Existe al menos una fuente/plataforma de empleo configurada?" y los tres retornos del bucle de procesamiento de fuentes.

### 1.3 Objetivo
Controlar la iteración de fuentes de la corrida: determinar si quedan fuentes pendientes de procesamiento; con resultado Sí entregar el control al nodo de selección con contrato de siguiente pendiente; con resultado No terminar la corrida de forma normal.

### 1.4 Descripción funcional
El nodo consume el contexto de ejecución, lee la lista de fuentes y el iterador desde el contexto en memoria (sin releer el almacén), calcula las fuentes pendientes (no marcadas como procesadas en esta corrida, en orden de configuración) y bifurca: con Sí entrega control al nodo de selección; con No fija el motivo de terminación normal `corrida_completada` (tipo suceso) y entrega control a "Finalizar Proceso", punto único de registro de terminaciones. El nodo es de evaluación pura: no avanza el iterador ni marca fuentes como procesadas; esa responsabilidad es del nodo de selección.

**Separación de responsabilidades:**
- *Flujo de negocio:* condición de continuidad del bucle de fuentes y salida normal de la corrida.
- *Implementación técnica:* evaluación pura en memoria sobre el contexto; único efecto colateral admisible: fijar el motivo de terminación en la rama No.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos, captura y almacena información original de ofertas; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no contiene lógica de ese tipo ni acceso a fuentes.

### 1.5 Entradas
- Contexto de ejecución: lista de fuentes (no vacía por contrato del nodo de existencia), iterador de fuentes (estado "ninguna" al inicio de la corrida o progreso de procesadas), `run_id`.

### 1.6 Salidas
- **Rama Sí:** control a "Seleccionar la siguiente fuente pendiente" con contrato "existe siguiente fuente pendiente en orden de configuración".
- **Rama No:** control a "Finalizar Proceso" con motivo de terminación normal `corrida_completada` (tipo suceso).
- **Falla interna (única excepción):** control a "Finalizar Proceso" con estado *error* (ver ERR-01).

### 1.7 Reglas de negocio
- **RN-01:** El nodo evalúa exclusivamente sobre el contexto en memoria; prohibido releer el almacén de configuración.
- **RN-02:** Fuente pendiente = fuente no marcada como procesada en la corrida actual; el orden de procesamiento es el orden de la configuración.
- **RN-03:** "Una fuente que falló (ingreso o búsqueda) se considera procesada dentro de la corrida y el bucle no la reselecta. Los reintentos condicionales internos del nodo 'Entrar a la fuente seleccionada' (v1.1) ocurren dentro de una única pasada y no modifican esta regla: la fuente se marca procesada al seleccionarse y su resultado (éxito o fallo tras agotar reintentos aplicables) no altera el avance del iterador."
- **RN-04:** Este nodo no avanza el iterador ni marca fuentes como procesadas; es evaluación pura. El avance del iterador es responsabilidad exclusiva de "Seleccionar la siguiente fuente pendiente".
- **RN-05:** La rama No es terminación normal de la corrida, no una falla: motivo `corrida_completada`, tipo suceso. El registro lo realiza "Finalizar Proceso" (punto único) con `run_id`, marca de tiempo, tipo y descripción.
- **RN-06:** Contrato de la rama Sí: garantiza que existe una siguiente fuente pendiente en orden de configuración.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** El contexto contiene el iterador y la lista de fuentes accesibles y coherentes (iterador en estado "ninguna" o progreso válido) antes de evaluar.
- **VAL-02:** El cálculo de pendientes se realiza exclusivamente sobre los datos leídos en el paso 1; conteo entero ≥ 0; orden de configuración respetado.
- **VAL-03:** La rama Sí solo se ejecuta con conteo de pendientes > 0.
- **VAL-04:** En la rama No, el motivo `corrida_completada` queda fijado en el contexto junto con `run_id` y marca de tiempo antes de entregar control.

### 1.9 Condiciones
- **Continuación (Sí):** conteo de fuentes pendientes > 0.
- **Terminación normal (No):** conteo de fuentes pendientes == 0 → "Finalizar Proceso" con motivo `corrida_completada`.
- **Aborto:** iterador ausente o corrupto en el contexto (falla interna; ver ERR-01) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
Nodo de decisión binaria:
- **Sí** (≥ 1 fuente pendiente) → "Seleccionar la siguiente fuente pendiente".
- **No** (0 fuentes pendientes) → "Finalizar Proceso" (motivo `corrida_completada`, tipo suceso).

### 1.11 Manejo de errores y excepciones
Única excepción del nodo:

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Iterador ausente o corrupto en el contexto (no debería ocurrir por paso 5 de INICIO) | 1 | Evento crítico en "errores o sucesos" | Aborto | error |

Escenarios límite cubiertos: primera pasada con iterador en "ninguna" (todas las fuentes pendientes → Sí); retorno tras fuente fallida (la fuente ya figura procesada por RN-03, no se reselecta); lista no vacía con todas procesadas (→ No, terminación normal). No existen otras condiciones de error: la evaluación es pura sobre datos ya validados.

### 1.12 Dependencias y contratos con otros nodos
- **Antecesores:** rama Sí de "¿Existe al menos una fuente/plataforma de empleo configurada?"; y los tres retornos del bucle: desde el registro de ingreso fallido, desde el registro de búsqueda sin ofertas, y desde la rama No de "¿Quedan ofertas por capturar?".
- **Sucesor normal (Sí):** "Seleccionar la siguiente fuente pendiente".
- **Sucesor de terminación (No):** "Finalizar Proceso" (motivo `corrida_completada`).
- **Sucesor de aborto (ERR-01):** "Finalizar Proceso" (estado *error*).
- **Contratos entregados:** rama Sí garantiza siguiente fuente pendiente (RN-06); rama No garantiza motivo fijado en el contexto (VAL-04).
- **Impactos aprobados sobre nodos futuros:**
  1. "Seleccionar la siguiente fuente pendiente" es el único responsable de avanzar el iterador y marcar la fuente como procesada al seleccionarla; los retornos del bucle encontrarán siempre el iterador avanzado.
  2. "Finalizar Proceso" amplía su contrato de motivos con `corrida_completada` (terminación normal; se formalizará al llegar a ese nodo).
  3. Los nodos de procesamiento de fuente asumen siempre una fuente corriente válida seleccionada.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Nodo de evaluación pura: sin I/O al almacén, sin acceso a red/fuentes, sin escritura en bases de datos, sin avance del iterador (RN-04). Único efecto colateral admisible: fijar el motivo de terminación en el contexto (rama No).
- El iterador debe implementarse como estado de corrida dentro del mismo objeto de contexto definido en INICIO (reiniciado por corrida, RN-03 de INICIO); almacenar progreso de procesadas y respetar el orden de configuración.
- No implementar reintentos ni re-evaluación de fuentes fallidas (RN-03).
- El suceso `corrida_completada` se registra en "Finalizar Proceso"; este nodo solo fija el motivo en el contexto.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer estado de iteración del contexto | Contexto (lista de fuentes, iterador, `run_id`) | Acceder al iterador y a la lista desde el contexto; no releer el almacén (RN-01) | Datos de iteración (progreso de procesadas) | VAL-01 | ERR-01 |
| 2 | Calcular fuentes pendientes | Lista de fuentes; iterador | Pendientes = fuentes no marcadas como procesadas en esta corrida, en orden de configuración (RN-02); conteo ≥ 0; condición = conteo > 0 | Conteo de pendientes y resultado booleano (Sí/No) | VAL-02 | Ninguna aplicable |
| 3 | Rama Sí — Entregar control | Resultado = Sí; contexto | Cerrar el nodo y entregar control con contrato "existe siguiente fuente pendiente en orden de configuración" (RN-06) | Flujo hacia "Seleccionar la siguiente fuente pendiente" | VAL-03 | Ninguna |
| 4 | Rama No — Fijar motivo y entregar control | Resultado = No; `run_id` | Fijar en el contexto el motivo de terminación `corrida_completada` (tipo suceso, terminación normal; RN-05); entregar control a Finalizar Proceso; el registro lo realiza ese nodo | Flujo hacia Finalizar Proceso (motivo `corrida_completada`) | VAL-04 | Ninguna |

---

# Especificación Canónica — Nodo Proceso: "Seleccionar la siguiente fuente pendiente"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Selección de fuente — "Seleccionar la siguiente fuente pendiente".

### 1.2 Posición en el flujo y estado del diagrama
Nodo de acción ubicado entre la decisión "¿Quedan fuentes por procesar en esta corrida?" (rama Sí) y "Entrar a la fuente seleccionada".

### 1.3 Objetivo
Materializar la selección de la fuente que se procesará en la pasada actual del bucle: avanzar el iterador de la corrida, marcar la fuente seleccionada como procesada y exponer la fuente corriente con sus parámetros en el contexto de ejecución.

### 1.4 Descripción funcional
El nodo consume el contexto con el contrato de la rama Sí (existe al menos una fuente pendiente), identifica la primera entrada no procesada de la lista en orden de configuración (iteración por posición), la marca como procesada en el momento de la selección, la fija como fuente corriente exponiendo sus parámetros (datos de acceso y filtros básicos), y entrega el control a "Entrar a la fuente seleccionada". El marcado al momento de la selección garantiza el progreso del bucle en todos los caminos, incluidos los de falla de la fuente.

**Separación de responsabilidades:**
- *Flujo de negocio:* determinar qué fuente se procesa en la pasada actual.
- *Implementación técnica:* mutación del iterador y del estado de fuente corriente dentro del contexto; sin I/O al almacén, sin acceso a red/fuentes.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos, captura y almacena información original de ofertas; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no accede a la fuente ni ejecuta búsquedas.

### 1.5 Entradas
- Contexto de ejecución con el contrato de la rama Sí de la decisión de iteración: lista de fuentes, iterador, `run_id`, garantía de existencia de al menos una fuente pendiente en orden de configuración.

### 1.6 Salidas
- Contexto actualizado: iterador avanzado con la fuente marcada como procesada; fuente corriente definida (`source_id`, posición, parámetros de acceso, filtros básicos).
- Control a "Entrar a la fuente seleccionada" con contrato "fuente corriente válida".
- **Falla interna (única excepción):** control a "Finalizar Proceso" con estado *error* (ver ERR-01 a ERR-03).

### 1.7 Reglas de negocio
- **RN-01:** El nodo opera exclusivamente sobre el contexto en memoria; prohibido releer el almacén de configuración.
- **RN-02:** La selección es la primera entrada no procesada de la lista, en orden de configuración; la clave de iteración es la posición en la lista.
- **RN-03:** La fuente se marca como procesada **en el momento de la selección**; esto garantiza el progreso del bucle ante fallas posteriores de la fuente (coherente con "fuente fallida = procesada dentro de la corrida", regla del nodo de iteración).
- **RN-04:** Este nodo es el único responsable de avanzar el iterador y marcar fuentes como procesadas; ningún otro nodo muta el iterador.
- **RN-05:** La fuente corriente expone en el contexto todos los parámetros requeridos por el bloque de procesamiento: datos de acceso y filtros básicos.
- **RN-06:** El identificador de la fuente corriente (`source_id`) es el atributo de trazabilidad por fuente y deberá incluirse, junto con `run_id`, en todo registro que generen los nodos posteriores ("errores o sucesos", "control de sesiones", "Ofertas Totales").
- **RN-07:** El nodo no revalida la estructura de la configuración (responsabilidad de INICIO).

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** El contexto contiene lista e iterador accesibles y coherentes antes de operar.
- **VAL-02:** La posición seleccionada corresponde a una entrada no procesada y dentro del rango de la lista.
- **VAL-03:** Tras la mutación, el iterador refleja la fuente como procesada y la fuente corriente queda definida con `source_id` y parámetros completos (acceso y filtros).

### 1.9 Condiciones
- **Continuación normal:** contrato Sí cumplido → selección, mutación y entrega de control.
- **Aborto:** iterador ausente/corrupto; ausencia de fuente pendiente pese al contrato Sí; falla interna al mutar el contexto → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
No es nodo de decisión. Salida normal única hacia "Entrar a la fuente seleccionada"; salida de aborto hacia "Finalizar Proceso" (estado *error*).

### 1.11 Manejo de errores y excepciones

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Iterador ausente o corrupto en el contexto | 1 | Evento crítico en "errores o sucesos" | Aborto | error |
| ERR-02 | Ausencia de fuente pendiente pese al contrato Sí (violación de contrato del nodo de iteración) | 2 | Evento crítico en "errores o sucesos" | Aborto | error |
| ERR-03 | Falla interna al mutar el contexto (iterador o fuente corriente) | 3 | Evento crítico en "errores o sucesos" | Aborto | error |

Escenarios límite cubiertos: configuración con entradas duplicadas (la iteración por posición procesa cada entrada por separado; `source_id` conserva la trazabilidad); primera pasada de la corrida (iterador en "ninguna" → primera entrada); retorno tras fuente fallida (la fuente fallida ya figura procesada y no se reselecta, RN-03).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** decisión "¿Quedan fuentes por procesar en esta corrida?" (rama Sí).
- **Sucesor normal:** "Entrar a la fuente seleccionada".
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contrato consumido:** rama Sí (existe siguiente fuente pendiente en orden de configuración).
- **Contrato entregado:** "fuente corriente válida" (fuente corriente con `source_id`, posición y parámetros completos); ningún nodo posterior reselecta fuente.
- **Contratos de trazabilidad:** `run_id` + `source_id` en todos los registros de nodos posteriores (RN-06).
- **Contrato aguas arriba aplicado:** identificadores de fuente únicos por configuración (validación de unicidad formalizada en INICIO v1.1; este nodo no la ejecuta, la asume).
- **Impactos aprobados sobre nodos futuros:**
  1. "Entrar a la fuente seleccionada" y todo el bloque de procesamiento consumen la fuente corriente del contexto.
  2. Los filtros básicos de la fuente corriente serán consumidos por el nodo "Aplicar los filtros básicos…".
  3. Los nodos de registro incorporan `source_id` en sus esquemas.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Único nodo que muta el iterador; implementarlo como operación atómica sobre el contexto (marcar procesada + fijar fuente corriente) para evitar estados intermedios inconsistentes (ERR-03).
- Iterador por posición; `source_id` solo para trazabilidad y vinculación de registros.
- No realizar acceso a red, ingreso a plataformas ni búsquedas en este nodo.
- No revalidar estructura de configuración (RN-07).

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer estado de selección del contexto | Contexto (lista de fuentes, iterador, `run_id`) con contrato Sí de la decisión | Acceder a lista e iterador desde el contexto; no releer el almacén (RN-01) | Datos de selección | VAL-01 | ERR-01 |
| 2 | Determinar la siguiente fuente pendiente | Lista de fuentes; iterador | Identificar la primera entrada no procesada en orden de configuración (iteración por posición, RN-02) | Posición y `source_id` de la fuente a seleccionar | VAL-02 | ERR-02 |
| 3 | Avanzar iterador, marcar procesada y fijar fuente corriente | Posición y `source_id` de la fuente | Marcar la entrada como procesada en el momento de la selección (RN-03); fijarla como fuente corriente exponiendo `source_id`, posición, parámetros de acceso y filtros básicos (RN-05) | Contexto actualizado: iterador avanzado + fuente corriente lista | VAL-03 | ERR-03 |
| 4 | Entregar control | Contexto actualizado | Cerrar el nodo y entregar control con contrato "fuente corriente válida" y trazabilidad `run_id` + `source_id` (RN-06) | Flujo hacia "Entrar a la fuente seleccionada" | Contexto completo (fuente corriente con parámetros) | Ninguna |

---

# Especificación Canónica — Nodo Proceso: "Entrar a la fuente seleccionada"

**Versión:** 1.1 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Ingreso a la fuente — "Entrar a la fuente seleccionada".

### 1.2 Posición en el flujo
Entre "Seleccionar la siguiente fuente pendiente" y la decisión "¿El ingreso fue exitoso?". Es el primer nodo del módulo que toca el mundo externo (plataformas de empleo). Posición definitiva; sin cambios estructurales al diagrama.

### 1.3 Objetivo
Intentar el acceso/ingreso a la plataforma de la fuente corriente según su ficha de acceso, con reintentos condicionales ante fallas transitorias, autenticar si corresponde, y dejar en el contexto (a) un resultado estructurado de ingreso (`entry_result`) para la decisión siguiente y (b) una sesión activa reutilizable por los nodos posteriores, solo en caso de éxito.

### 1.4 Descripción funcional
El nodo lee la ficha de acceso de la fuente corriente desde el contexto, resuelve credenciales desde el almacén seguro si el tipo de acceso lo requiere, abre un canal de sesión y accede a la plataforma dentro de un timeout configurable, ejecuta el flujo de autenticación si corresponde, y evalúa el criterio verificable de ingreso exitoso de la fuente. Los pasos de acceso y autenticación están envueltos en un ciclo de intento con reintento condicional: ante un código reintentable (`fuente_inalcanzable`, `timeout_ingreso`) y con intentos restantes, cierra el canal, aplica backoff y reintenta desde el acceso; ante un código no reintentable o reintentos agotados, construye evidencia de fallo. Con el resultado construye `entry_result` = {estado, codigo_motivo, evidencia_acotada sin datos sensibles, número de intentos}. En éxito crea `session_id` único y guarda handle de canal + `session_id` en el contexto; en fallo cierra el canal y garantiza ausencia de sesión. Entrega control a "¿El ingreso fue exitoso?".

**Flujo interno:** secuencia con salida temprana: cualquier fallo en los pasos 2–4 que no sea reintentable (o agote reintentos) salta al paso 5 (construcción de `entry_result`). Ningún fallo de intento aborta la corrida; el aborto queda reservado a violaciones de contrato/contexto.

**Separación de responsabilidades:**
- *Flujo de negocio:* intentar el ingreso con resiliencia acotada y producir evidencia evaluable; la evaluación booleana del resultado pertenece a la decisión siguiente.
- *Implementación técnica:* canal de sesión, autenticación, timeouts, política de reintentos, gestión de credenciales y evidencia.
- *Límite:* este nodo **no** aplica filtros, **no** lee ofertas, **no** revalida la estructura de la ficha (garantizada por INICIO v1.2), **no** interpreta contenido.

### 1.5 Entradas
- Contexto de ejecución: fuente corriente con ficha de acceso completa (`source_id`, URL/plataforma, tipo de acceso `publico|con_autenticacion`, referencia de credenciales, criterio verificable de ingreso exitoso, filtros básicos, timeout), `run_id`.
- Parámetros de reintento y backoff (configuración global; máx. reintentos por defecto 2).
- Almacén seguro de credenciales, accedido exclusivamente por este nodo.

### 1.6 Salidas
- `entry_result` en contexto: `{estado: exito|fallo, codigo_motivo, evidencia_acotada, numero_de_intentos}` sin datos sensibles.
- En éxito: sesión activa en contexto (`session_id` único + handle de canal).
- En fallo: canal cerrado, sin sesión en contexto.
- Control único a "¿El ingreso fue exitoso?".
- **Aborto (única excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-09).

### 1.7 Reglas de negocio
- **RN-01:** El nodo opera sobre el contexto; no relee el almacén de configuración ni revalida la estructura de la ficha (propiedad de INICIO v1.2, RN-08 de ese nodo).
- **RN-02:** El almacén seguro de credenciales es accedido exclusivamente por este nodo; credenciales y tokens nunca se registran en logs, eventos ni bases de datos, ni se persisten fuera del uso en memoria.
- **RN-03:** Intento con reintentos condicionales: hasta N reintentos (configurable, por defecto 2) con backoff configurable, exclusivos para los códigos reintentables `fuente_inalcanzable` y `timeout_ingreso`; cada reintento cierra el canal previo y re-ejecuta desde el acceso (paso 3). Los códigos `credenciales_no_disponibles`, `autenticacion_rechazada`, `bloqueo_plataforma`, `criterio_no_cumplido` y `error_interno_fuente` producen evidencia de fallo inmediata sin reintento (fallas deterministas o rechazo de plataforma; reintentar no cambia el resultado y aumenta el riesgo anti-bot).
- **RN-04:** Toda falla de intento (tras agotar reintentos aplicables, o sin derecho a ellos) produce evidencia de fallo con su código de motivo y la fuente se omite (decidido aguas abajo); el aborto queda reservado a violaciones de contrato/contexto.
- **RN-05:** `session_id` se crea únicamente en éxito; en fallo el canal se cierra y no existe sesión en el contexto.
- **RN-06:** La evidencia de `entry_result` es acotada y sin datos sensibles (p. ej., estado/URL final, presencia o ausencia de elementos esperados, mensaje público de la plataforma, número de intentos).
- **RN-07:** Todo evento generado por este nodo incluye `run_id` y `source_id`.
- **RN-08:** Este nodo no aplica filtros, no captura ofertas y no interpreta contenido de la plataforma.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** Ficha de acceso accesible y presente en el contexto antes de operar (lectura defensiva).
- **VAL-02:** Si `con_autenticacion`, credenciales resueltas del almacén seguro y no vacías antes de abrir canal.
- **VAL-03:** Todo acceso y autenticación acotados por el timeout configurable de la fuente.
- **VAL-04:** `entry_result` estructurado con estado, código de motivo, evidencia acotada sin datos sensibles y número de intentos.
- **VAL-05:** En éxito, sesión guardada en contexto con `session_id` único y handle operativo; en fallo, canal cerrado y ausencia de sesión.
- **VAL-06:** Política de reintentos: contador de reintentos ≤ máximo configurado; backoff aplicado entre intentos; reintento exclusivo para códigos reintentables (RN-03); cada reintento parte de canal cerrado.

### 1.9 Condiciones
- **Continuación normal:** `entry_result` construido (éxito o fallo) → entrega de control a la decisión.
- **Reintento condicional:** falla con código reintentable y intentos restantes → nuevo intento tras backoff; reintentos agotados o código no reintentable → evidencia de fallo.
- **Fallo de fuente (no aborto):** cualquiera de los códigos de motivo de fallo → `entry_result` fallo → la fuente se omite aguas abajo.
- **Aborto:** ficha ausente/corrupta en contexto (ERR-01); corrupción del contexto (ERR-09) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
No es nodo de decisión. Salida normal única hacia "¿El ingreso fue exitoso?"; salida de aborto hacia "Finalizar Proceso" (estado *error*). Flujo interno con salida temprana al paso 5 ante fallos no reintentables o reintentos agotados (1.4).

### 1.11 Manejo de errores y excepciones
*Evidencia de fallo* = construcción de `entry_result` con el código de motivo y salto/cierre según corresponda; no aborta la corrida. *Aborto* = terminación en "Finalizar Proceso" con estado *error*. *Reintentable* = sujeto a la política de reintentos de RN-03/VAL-06.

| Código | Error / excepción | Reintentable | Detección (paso) | Registro / acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Ficha ausente o corrupta en contexto (violación de contrato de INICIO v1.2) | No | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`); aborto | error |
| ERR-02 | `credenciales_no_disponibles`: referencia no resoluble o credenciales vacías | No | 2 | Evidencia de fallo; no se abre canal; salto al paso 5 | continúa (fallo de fuente) |
| ERR-03 | `fuente_inalcanzable`: red/DNS/plataforma caída | Sí | 3 | Con intentos restantes: cerrar canal, backoff, reintentar desde paso 3. Agotados: evidencia de fallo; salto al paso 5 | continúa (fallo de fuente) |
| ERR-04 | `timeout_ingreso`: acceso o autenticación fuera del timeout | Sí | 3/4 | Ídem ERR-03 (el reintento re-ejecuta desde paso 3) | continúa (fallo de fuente) |
| ERR-05 | `autenticacion_rechazada`: credenciales inválidas según la plataforma | No | 4 | Evidencia de fallo; salto al paso 5 | continúa (fallo de fuente) |
| ERR-06 | `bloqueo_plataforma`: captcha/anti-bot/desafío | No | 4 | Evidencia de fallo; salto al paso 5 | continúa (fallo de fuente) |
| ERR-07 | `criterio_no_cumplido`: intento completo sin reconocimiento del estado esperado | No | 5 | Evidencia de fallo | continúa (fallo de fuente) |
| ERR-08 | `error_interno_fuente`: falla interna inesperada durante el intento o la captura | No | 3–5 | Evidencia de fallo; cerrar canal si quedó abierto | continúa (fallo de fuente) |
| ERR-09 | Corrupción del contexto durante la captura | No | 5 | Evento crítico en "errores o sucesos"; aborto | error |

**Contrato de códigos de motivo (para la decisión siguiente y el nodo de registro):** `ingreso_exitoso`, `credenciales_no_disponibles`, `fuente_inalcanzable`, `timeout_ingreso`, `autenticacion_rechazada`, `bloqueo_plataforma`, `criterio_no_cumplido`, `error_interno_fuente`.

Escenarios límite cubiertos: fuente `publico` (pasos 2 y 4 sin efecto); fuente `con_autenticacion` con almacén seguro caído (ERR-02, sin reintento); plataforma con cambio de layout (ERR-07, sin reintento); caída transitoria de red o lentitud (ERR-03/ERR-04, con reintento acotado); canal parcialmente abierto al fallar (cierre garantizado en todo camino, incluido cada reintento); credenciales nunca expuestas en evidencia o registros (RN-02, RN-06).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** "Seleccionar la siguiente fuente pendiente" (contrato: fuente corriente válida con ficha completa).
- **Sucesor normal:** "¿El ingreso fue exitoso?" (evalúa `entry_result` sin sondear la plataforma).
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** ficha completa garantizada por INICIO v1.2 (RN-08 de ese nodo); trazabilidad `run_id` + `source_id`; parámetros globales de reintento/backoff.
- **Contratos entregados:** `entry_result` estructurado (con número de intentos); `session_id` + handle de sesión solo en éxito.
- **Impactos aprobados sobre nodos futuros:**
  1. La decisión "¿El ingreso fue exitoso?" es evaluación pura sobre `entry_result`.
  2. El nodo de registro de ingreso fallido consume los códigos de motivo y puede leer el número de intentos de la evidencia.
  3. `session_id` alimentará "control de sesiones" y los registros de ofertas.
  4. Los filtros básicos de la fuente corriente se consumen en el nodo de filtros, no aquí.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología: el canal de sesión puede ser navegador o API según la plataforma; el contrato funcional es idéntico.
- Parámetros de reintento: máximo configurable (por defecto 2) y backoff configurable (se recomienda creciente); el número total de intentos es 1 + máx. reintentos.
- Cada reintento debe partir de canal cerrado y re-ejecutar desde el acceso (paso 3), para evitar estados parciales de canal o autenticación.
- Nunca reintentar códigos no reintentables (RN-03): reintentar `bloqueo_plataforma` o `autenticacion_rechazada` aumenta el riesgo de ban sin beneficio.
- El handle de sesión debe quedar en el contexto para los nodos posteriores; garantizar cierre del canal en todo camino de fallo (sin fugas de recursos).
- Timeout configurable por fuente con valor global por defecto.
- Evidencia acotada y sin datos sensibles; nunca credenciales, tokens ni cookies de sesión en eventos o bases de datos.
- No implementar lógica de filtros/ofertas (RN-08).
- `session_id` único por sesión; vinculado a `run_id` y `source_id` en los registros que lo consuman.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer ficha de acceso de la fuente corriente | Contexto (fuente corriente, `run_id`) | Acceder a URL, tipo de acceso, referencia de credenciales, criterio de éxito y timeout desde el contexto; no releer almacén ni revalidar estructura (RN-01) | Parámetros de acceso | VAL-01 | ERR-01 |
| 2 | Resolver credenciales si aplica | Tipo de acceso; referencia; almacén seguro | Si `con_autenticacion`: obtener credenciales del almacén seguro y verificar no vacías (RN-02); fallo → motivo y salto al paso 5 sin abrir canal, sin reintento. Si `publico`: sin efecto | Credenciales en memoria, o N/A | VAL-02 | ERR-02 |
| 3 | Abrir canal y acceder a la plataforma (con reintento condicional) | Parámetros de acceso; timeout; parámetros de reintento/backoff | Abrir canal; acceder a la URL dentro del timeout (RN-03/VAL-03). Fallo reintentable con intentos restantes: cerrar canal, backoff, repetir paso 3. Fallo reintentable agotado o fallo no reintentable: cerrar canal y salto al paso 5 | Canal abierto con estado inicial | VAL-03, VAL-06 | ERR-03, ERR-04, ERR-08 |
| 4 | Autenticar si aplica (con reintento condicional de timeout) | Canal; credenciales; parámetros de reintento/backoff | Si `con_autenticacion`: ejecutar flujo de autenticación dentro del timeout sin registrar credenciales/tokens (RN-02). `timeout_ingreso` con intentos restantes: cerrar canal, backoff, re-ejecutar desde paso 3. `autenticacion_rechazada` o `bloqueo_plataforma`: sin reintento, cerrar canal y salto al paso 5. Si `publico`: sin efecto | Estado de canal post-autenticación | VAL-03, VAL-06 | ERR-04, ERR-05, ERR-06, ERR-08 |
| 5 | Evaluar criterio de éxito y construir `entry_result` | Estado del canal; criterio verificable de la fuente; contador de intentos | Aplicar el criterio; construir `entry_result` con número de intentos y evidencia acotada (RN-06). Éxito: crear `session_id` único y guardar handle + `session_id` (RN-05). Fallo (incluido criterio no cumplido): cerrar canal, sin sesión | `entry_result` en contexto; sesión lista o ausente | VAL-04, VAL-05 | ERR-07, ERR-08, ERR-09 |
| 6 | Entregar control | Contexto con `entry_result` | Cerrar el nodo y entregar control a la decisión de ingreso | Flujo hacia "¿El ingreso fue exitoso?" | `entry_result` presente en contexto | Ninguna |

---

# Especificación Canónica — Nodo Decisión: "¿El ingreso fue exitoso?"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Decisión de ingreso — "¿El ingreso fue exitoso?".

### 1.2 Posición en el flujo
Entre "Entrar a la fuente seleccionada" (v1.1) y el bloque de procesamiento de la fuente. Rama Sí hacia "Aplicar los filtros básicos establecidos para esa fuente/plataforma"; rama No hacia "Registrar error o suceso en 'errores o sucesos'". Posición definitiva; sin cambios estructurales al diagrama.

### 1.3 Objetivo
Evaluar el resultado del intento de ingreso y bifurcar: con Sí, continuar el procesamiento de la fuente con una sesión activa; con No, derivar al registro del fallo y posterior omisión de la fuente.

### 1.4 Descripción funcional
El nodo lee `entry_result` del contexto, valida su consistencia (estructura completa y, en éxito, presencia de la sesión), evalúa la condición `estado == exito` y bifurca. Es una decisión pura: no sondea la plataforma ni la sesión y no realiza registros; el registro del fallo pertenece al nodo de la rama No. Una inconsistencia del contrato recibido (entry_result ausente/corrupto, estructura inválida, o éxito sin sesión) se trata como violación de contrato y aborta la corrida en "Finalizar Proceso" con estado *error*.

**Separación de responsabilidades:**
- *Flujo de negocio:* bifurcación entre procesar la fuente u omitirla con registro.
- *Implementación técnica:* evaluación pura en memoria sobre el contexto; sin acceso externo.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos, captura y almacena información original de ofertas; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no contiene lógica de ese tipo.

### 1.5 Entradas
- Contexto de ejecución: `entry_result` = {estado: exito|fallo, codigo_motivo, evidencia_acotada, numero_de_intentos}; sesión activa (`session_id` + handle) si el estado es exito; `run_id`; `source_id`.

### 1.6 Salidas
- **Rama Sí:** control a "Aplicar los filtros básicos establecidos para esa fuente/plataforma" con contrato "sesión activa disponible".
- **Rama No:** control a "Registrar error o suceso en 'errores o sucesos'" con `entry_result` disponible como carga de registro.
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-02).

### 1.7 Reglas de negocio
- **RN-01:** Evaluación pura sobre `entry_result` en el contexto; prohibido sondear la plataforma o la sesión desde este nodo.
- **RN-02:** Condición de la decisión = `entry_result.estado == exito`.
- **RN-03:** Validación de consistencia del contrato recibido: estructura completa de `entry_result` y, si estado = exito, sesión presente en contexto. La violación se trata como falla visible (aborto), no como degradación silenciosa.
- **RN-04:** Este nodo no registra eventos ni errores; el registro del fallo pertenece exclusivamente al nodo de la rama No (punto único de registro por camino).
- **RN-05:** La rama Sí garantiza el contrato "sesión activa disponible"; la rama No garantiza `entry_result` disponible como carga de registro para el nodo siguiente.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** `entry_result` presente y accesible en el contexto antes de evaluar.
- **VAL-02:** Estructura completa de `entry_result`: estado, codigo_motivo, evidencia_acotada, numero_de_intentos.
- **VAL-03:** Si estado = exito, sesión presente en contexto (handle operativo + `session_id`).

### 1.9 Condiciones
- **Continuación (Sí):** estado = exito y consistencia validada → nodo de filtros.
- **Derivación a registro (No):** estado = fallo y consistencia validada → nodo de registro.
- **Aborto:** `entry_result` ausente/corrupto (ERR-01); estructura inválida o estado exito sin sesión (ERR-02) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
Nodo de decisión binaria:
- **Sí** (`entry_result.estado == exito`) → "Aplicar los filtros básicos establecidos para esa fuente/plataforma".
- **No** (`entry_result.estado == fallo`) → "Registrar error o suceso en 'errores o sucesos'".

### 1.11 Manejo de errores y excepciones

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | `entry_result` ausente o corrupto en contexto (violación de contrato de "Entrar" v1.1) | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`) | Aborto | error |
| ERR-02 | Estructura de `entry_result` inválida, o estado exito sin sesión presente (violación de VAL-05 de "Entrar") | 2 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`) | Aborto | error |

Escenarios límite cubiertos: fallo con cualquier código de motivo (la decisión no interpreta el motivo, solo el estado); éxito con sesión operativa (rama Sí); violaciones de contrato entre nodos (aborto visible).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** "Entrar a la fuente seleccionada" v1.1 (provee `entry_result` y, en éxito, la sesión).
- **Sucesor normal (Sí):** "Aplicar los filtros básicos establecidos para esa fuente/plataforma".
- **Sucesor de fallo (No):** "Registrar error o suceso en 'errores o sucesos'".
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** `entry_result` estructurado y sesión condicional (contratos de "Entrar" v1.1).
- **Contratos entregados:** rama Sí → "sesión activa disponible"; rama No → `entry_result` como carga de registro.
- **Impactos aprobados sobre nodos futuros:**
  1. El nodo de registro (rama No) consumirá `entry_result` completo (codigo_motivo + numero_de_intentos + evidencia) para tipificar y describir el evento.
  2. El nodo de filtros (rama Sí) consumirá la sesión activa sin revalidarla.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Nodo de evaluación pura: sin I/O externo, sin escrituras en bases de datos salvo el evento crítico del protocolo de aborto.
- No interpretar ni ramificar por codigo_motivo en este nodo: la bifurcación es exclusivamente por estado (RN-02). La tipificación por motivo pertenece al nodo de registro.
- No registrar el fallo en este nodo (RN-04).
- La validación de consistencia (RN-03) es defensiva ante bugs de "Entrar"; no debe usarse para lógica de negocio.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer `entry_result` del contexto | Contexto (`entry_result`, sesión si existe, `run_id`, `source_id`) | Acceder a `entry_result` desde el contexto; no sondear la plataforma ni la sesión (RN-01) | `entry_result` | VAL-01 | ERR-01 |
| 2 | Validar consistencia del contrato | `entry_result`; contexto | Verificar estructura completa (VAL-02); si estado = exito, verificar sesión presente con handle + `session_id` (VAL-03) | `entry_result` validado | VAL-02, VAL-03 | ERR-02 |
| 3 | Evaluar condición "ingreso exitoso" | `entry_result` validado | Condición = estado == exito (RN-02) | Resultado booleano (Sí/No) | — | Ninguna aplicable |
| 4 | Rama Sí — Entregar control | Resultado = Sí; contexto con sesión | Cerrar el nodo y entregar control con contrato "sesión activa disponible" (RN-05) | Flujo hacia "Aplicar los filtros básicos establecidos para esa fuente/plataforma" | estado = exito y sesión presente | Ninguna |
| 5 | Rama No — Entregar control con carga de registro | Resultado = No; `entry_result` | No registrar en este nodo (RN-04); entregar control con `entry_result` disponible como carga de registro (RN-05) | Flujo hacia "Registrar error o suceso en 'errores o sucesos'" | estado = fallo | Ninguna |

---

# Especificación Canónica — Nodo Proceso: "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales"

**Versión:** 1.1 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Búsqueda con filtros básicos — "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales".

### 1.2 Posición en el flujo
Entre la rama Sí de "¿El ingreso fue exitoso?" (primera pasada de la fuente) o la rama Sí de "¿Quedan sets de filtros por aplicar en esta fuente?" (pasadas siguientes), y la decisión "¿Se encontraron ofertas?". Nodo re-entrante por set de filtros. Sin otros cambios estructurales.

### 1.3 Objetivo
Seleccionar el siguiente set de filtros pendiente de la fuente corriente, ejecutar la búsqueda/consulta en la plataforma dentro de la sesión activa aplicando ese set, interpretar la respuesta y dejar en el contexto un `search_result` estructurado (primera página de referencias de ofertas, estado de paginación, metadatos y `set_indice`) para la decisión y el recorrido siguientes.

### 1.4 Descripción funcional
El nodo lee del contexto la sesión activa, los `sets_de_filtros` de la fuente corriente y el iterador de sets. Si la fuente corriente cambió desde el último uso del iterador, lo reinicia a "ninguno". Selecciona el primer set no procesado en orden de configuración, lo marca como procesado en el momento de la selección y lo fija como `set_corriente`. Aplica los filtros del set mediante el adaptador de la plataforma, ejecuta la búsqueda dentro del timeout con reintentos condicionales ante fallas transitorias, e interpreta la respuesta cruda convirtiéndola en una lista ordenada de referencias de oferta (identificador/URL) de la primera página, más estado de paginación y total declarado si la plataforma lo expone. Construye `search_result` = {estado, codigo_motivo, evidencia_acotada, ofertas_primera_pagina, estado_paginacion, total_declarado, set_indice, numero_de_intentos} y lo guarda en el contexto. Entrega control a "¿Se encontraron ofertas?".

**Límites del nodo (no hace):** no decide si hay ofertas (propiedad de la decisión siguiente); no decide si quedan sets pendientes (propiedad de la decisión de sets); no captura la información completa de cada oferta (propiedad del nodo de captura); no interpreta ni evalúa contenido de ofertas; no recorre páginas posteriores (propiedad del bucle de captura).

**Separación de responsabilidades:**
- *Flujo de negocio:* acotar cada búsqueda a oportunidades potencialmente relevantes mediante el set de filtros corriente.
- *Implementación técnica:* iterador de sets, adaptador por plataforma (aplicación de filtros y parseo de respuesta), timeouts, reintentos, paginación perezosa.

### 1.5 Entradas
- Contexto de ejecución: sesión activa (`session_id` + handle), `sets_de_filtros` de la fuente corriente (lista no vacía, ordenada, cada set posiblemente vacío), iterador de sets (estado "ninguno" o progreso de procesados), `fuente_corriente` (`source_id`), `run_id`, `session_id`.
- Parámetros globales: timeout de consulta, máximo de reintentos (por defecto 2), backoff.

### 1.6 Salidas
- `set_corriente` fijado en contexto (índice + filtros) e iterador de sets avanzado.
- `search_result` en contexto: `{estado: exito|fallo, codigo_motivo, evidencia_acotada, ofertas_primera_pagina: [referencias], estado_paginacion, total_declarado (o indeterminado), set_indice, numero_de_intentos}`.
- Control único a "¿Se encontraron ofertas?".
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-08).

### 1.7 Reglas de negocio
- **RN-01:** El nodo opera sobre el contexto; no relee el almacén de configuración.
- **RN-02:** Se aplican únicamente los filtros del `set_corriente` configurado para la fuente corriente; el adaptador de la plataforma los mapea al mecanismo propio de esa fuente (parámetros, UI o API).
- **RN-03:** Set con lista vacía de filtros = búsqueda base con valores por defecto de la plataforma; es configuración válida, no defecto.
- **RN-04:** Filtros del set configurados pero no aplicables en runtime = fallo `filtros_no_aplicables` para ese set; prohibido continuar con búsqueda sin filtros. El fallo descarta el set, no la fuente (la fuente continúa con sus sets restantes aguas abajo).
- **RN-05:** Alcance perezoso: el nodo produce la primera página de referencias y el estado de paginación; el recorrido de páginas posteriores pertenece al bucle de captura.
- **RN-06:** Reintentos condicionales idénticos a "Entrar a la fuente seleccionada" v1.1: reintentables solo `fuente_inalcanzable` y `timeout_consulta`, con los mismos parámetros globales; el resto produce evidencia de fallo inmediata.
- **RN-07:** Sesión expirada durante la consulta = fallo `sesion_expirada`; no existe re-ingreso automático dentro de este nodo.
- **RN-08:** El nodo estructura referencias de oferta (identificador/URL en orden de plataforma); no captura información completa, no interpreta contenido, no decide si hay ofertas.
- **RN-09:** Evidencia acotada y sin datos sensibles; trazabilidad `run_id` + `source_id` + `session_id` + `set_indice` en todo evento.
- **RN-10:** Iterador de sets propiedad de este nodo: se reinicia a "ninguno" cuando cambia la fuente corriente; en cada entrada selecciona el primer set no procesado en orden de configuración y lo marca como procesado en el momento de la selección (garantiza progreso del bucle de sets ante cualquier resultado del set).
- **RN-11:** Este nodo no decide si quedan sets pendientes; esa evaluación pertenece a la decisión "¿Quedan sets de filtros por aplicar en esta fuente?", que lee el iterador.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** Sesión activa, `sets_de_filtros` e iterador de sets presentes y accesibles en el contexto antes de operar.
- **VAL-02:** Consulta y aplicación de filtros acotadas por timeout configurable.
- **VAL-03:** Política de reintentos: contador ≤ máximo configurado; backoff aplicado; solo códigos reintentables; cada reintento independiente.
- **VAL-04:** La interpretación produce lista ordenada de referencias + estado de paginación; respuesta no interpretable → `respuesta_invalida`.
- **VAL-05:** `search_result` completo y estructurado en el contexto (con `set_indice`) antes de entregar control.
- **VAL-06:** Iterador de sets coherente (reiniciado si cambió la fuente); el set seleccionado existe en la lista y está dentro de rango; tras la selección queda marcado como procesado.

### 1.9 Condiciones
- **Continuación normal:** `search_result` construido (éxito con lista posiblemente vacía, o fallo) → entrega de control a la decisión.
- **Fallo de set (no aborto, no descarte de fuente):** cualquier código de motivo de fallo → `search_result` fallo → el set se omite y la fuente continúa con sus sets restantes aguas abajo.
- **Aborto:** sesión, sets o iterador ausentes/corruptos en contexto, o ausencia de set pendiente pese al enrutamiento (ERR-01); corrupción del contexto (ERR-08) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
No es nodo de decisión. Salida normal única hacia "¿Se encontraron ofertas?"; salida de aborto hacia "Finalizar Proceso" (estado *error*). Re-entrada desde la rama Sí de "¿Quedan sets de filtros por aplicar en esta fuente?".

### 1.11 Manejo de errores y excepciones
*Evidencia de fallo* = construcción de `search_result` con el código de motivo; no aborta la corrida y no descarta la fuente (solo el set). *Aborto* = terminación en "Finalizar Proceso" con estado *error*. *Reintentable* = sujeto a RN-06/VAL-03.

| Código | Error / excepción | Reintentable | Detección (paso) | Registro / acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Sesión, `sets_de_filtros` o iterador de sets ausentes/corruptos en contexto; o ausencia de set pendiente pese al enrutamiento (violación de contratos previos) | No | 1–2 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`); aborto | error |
| ERR-02 | `filtros_no_aplicables`: filtros del set no soportados por la plataforma en runtime | No | 3 | Evidencia de fallo (set omitido) | continúa (fallo de set) |
| ERR-03 | `fuente_inalcanzable`: red/DNS/plataforma caída durante la consulta | Sí | 3 | Con intentos restantes: backoff y reintento; agotados: evidencia de fallo | continúa (fallo de set) |
| ERR-04 | `timeout_consulta`: consulta fuera del timeout | Sí | 3 | Ídem ERR-03 | continúa (fallo de set) |
| ERR-05 | `sesion_expirada`: sesión caducada durante la consulta | No | 3 | Evidencia de fallo; sin re-ingreso (RN-07) | continúa (fallo de set) |
| ERR-06 | `respuesta_invalida`: respuesta corrupta o no interpretable | No | 4 | Evidencia de fallo | continúa (fallo de set) |
| ERR-07 | `error_interno_consulta`: falla interna inesperada durante consulta o interpretación | No | 3–5 | Evidencia de fallo | continúa (fallo de set) |
| ERR-08 | Corrupción del contexto durante la construcción de `search_result` | No | 5 | Evento crítico en "errores o sucesos"; aborto | error |

**Contrato de códigos de motivo (consulta):** `consulta_exitosa`, `filtros_no_aplicables`, `respuesta_invalida`, `fuente_inalcanzable`, `timeout_consulta`, `sesion_expirada`, `error_interno_consulta`.

**Definición de éxito del nodo:** consulta ejecutada, filtros del set aplicados (si configurados) y respuesta interpretada; la lista de referencias puede ser vacía (resultado válido que el flujo siguiente tratará como "sin ofertas en este set" y avanzará al siguiente set).

Escenarios límite cubiertos: set vacío (búsqueda base, RN-03); plataforma sin soporte de filtros del set (ERR-02, set omitido, fuente continúa); respuesta vacía válida vs. respuesta corrupta (éxito con lista vacía vs. ERR-06); sesión expirada a mitad de consulta (ERR-05); caída transitoria (ERR-03/ERR-04 con reintento acotado); cambio de fuente (reinicio del iterador, RN-10); re-entrada por set siguiente (iterador ya avanzado).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesores:** rama Sí de "¿El ingreso fue exitoso?" (primera pasada de la fuente); rama Sí de "¿Quedan sets de filtros por aplicar en esta fuente?" (pasadas siguientes).
- **Sucesor normal:** "¿Se encontraron ofertas?".
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** sesión activa; `sets_de_filtros` no vacío y ordenado (ficha, RN-08 de INICIO v1.3); parámetros globales de timeout/reintentos/backoff.
- **Contratos entregados:** `search_result` estructurado con `set_indice`; iterador de sets avanzado.
- **Impactos aprobados sobre nodos futuros:**
  1. "¿Se encontraron ofertas?" v1.1 (reedición pendiente): rama Sí → "Capturar ofertas"; rama No → registro y luego enrutamiento a la decisión de sets (un set fallido o vacío no descarta la fuente).
  2. La decisión "¿Quedan sets de filtros por aplicar en esta fuente?" lee el iterador de sets (propiedad de este nodo, RN-10/RN-11); su rama No retorna a "¿Quedan fuentes por procesar en esta corrida?".
  3. El bucle de captura consume `ofertas_primera_pagina` y `estado_paginacion` del set corriente.
  4. Los registros de ofertas y eventos incorporan `set_indice` (RN-09).
  5. Refinamiento aprobado: "Seleccionar la siguiente fuente pendiente" **no** requiere reedición por el iterador de sets (propiedad de este nodo).

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología; el adaptador por fuente encapsula el mecanismo de filtros y el criterio de interpretación de la plataforma.
- Iterador de sets: estado en contexto vinculado a `source_id`; al detectar cambio de fuente, reiniciar a "ninguno" antes de seleccionar (RN-10). Marcado como procesado en el momento de la selección (progreso garantizado ante cualquier resultado del set).
- Referencias de oferta = identificador/URL en orden de plataforma; sin captura de contenido en este nodo.
- `total_declarado` solo si la plataforma lo expone; de lo contrario, valor indeterminado (no es criterio de bucle).
- Estado de paginación debe permitir al bucle solicitar la página siguiente sin re-ejecutar la búsqueda del set.
- Nunca continuar con búsqueda sin filtros ante filtros no aplicables (RN-04).
- Evidencia acotada y sin datos sensibles; nunca credenciales/tokens/cookies en eventos o bases de datos.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer insumos de búsqueda del contexto | Contexto (sesión activa, `sets_de_filtros`, iterador de sets, `source_id`, `run_id`, `session_id`, parámetros de timeout/reintentos) | Acceder a sesión, sets, iterador y parámetros desde el contexto; no releer almacén (RN-01) | Insumos de búsqueda | VAL-01 | ERR-01 |
| 2 | Seleccionar siguiente set de filtros pendiente | Sets; iterador de sets; `source_id` | Si cambió la fuente: reiniciar iterador a "ninguno" (RN-10). Seleccionar primer set no procesado en orden de configuración; marcarlo como procesado; fijar `set_corriente` (índice + filtros). Ausencia de set pendiente (no debería ocurrir por enrutamiento): violación de contrato | `set_corriente` fijado; iterador avanzado | VAL-06 | ERR-01 |
| 3 | Aplicar filtros del set y ejecutar la consulta | Sesión; filtros del `set_corriente` (lista posiblemente vacía); timeout; parámetros de reintento/backoff | Mapear y aplicar los filtros del set mediante el adaptador (RN-02); set vacío → búsqueda base (RN-03); ejecutar consulta dentro del timeout (VAL-02). Fallo reintentable con intentos restantes: backoff y reintento (VAL-03); agotados o no reintentable: evidencia de fallo y salto al paso 5 | Respuesta cruda de la plataforma | VAL-02, VAL-03 | ERR-02, ERR-03, ERR-04, ERR-05, ERR-07 |
| 4 | Interpretar respuesta y construir conjunto de resultados | Respuesta cruda; criterio de interpretación del adaptador | Convertir la respuesta en lista ordenada de referencias de oferta de la primera página; extraer `estado_paginacion` y `total_declarado` si la plataforma lo expone (RN-05, RN-08); respuesta no interpretable → `respuesta_invalida` y salto al paso 5 | Conjunto de resultados (referencias + paginación + total) | VAL-04 | ERR-06, ERR-07 |
| 5 | Construir `search_result` y guardar en contexto | Conjunto de resultados o código de fallo; `set_indice`; contador de intentos | Construir `search_result` = {estado, codigo_motivo, evidencia_acotada, ofertas_primera_pagina, estado_paginacion, total_declarado, set_indice, numero_de_intentos} (RN-09); éxito = consulta ejecutada, filtros del set aplicados y respuesta interpretada, con lista posiblemente vacía | `search_result` en contexto | VAL-05 | ERR-07, ERR-08 |
| 6 | Entregar control | Contexto con `search_result` | Cerrar el nodo y entregar control a la decisión de resultados | Flujo hacia "¿Se encontraron ofertas?" | `search_result` presente en contexto | Ninguna |

---

# Especificación Canónica — Nodo Decisión: "¿Se encontraron ofertas?"

**Versión:** 1.1 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Decisión de resultados — "¿Se encontraron ofertas?".

### 1.2 Posición en el flujo y estado del diagrama
Entre "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales" (v1.1) y, según rama, "Capturar ofertas" (Sí) o "Registrar suceso o error en 'errores o sucesos'" (No).

**Cambios aprobados sobre el diagrama original que este documento oficializa:** (a) el nodo de conteo ("Contar o revisar el número total de ofertas encontradas") se elimina; la auditoría de sesión vive dentro de "Capturar ofertas"; (b) la rama No, tras el registro, se enruta a la decisión de sets de filtros, no a la iteración de fuentes; (c) el bucle por oferta original ("¿Es la primera oferta…", selección y captura por oferta) fue reemplazado por el bloque de captura por lote con políticas por fuente.

### 1.3 Objetivo
Evaluar el resultado de la búsqueda del set corriente y bifurcar: con Sí, iniciar el bloque de captura de ofertas; con No, derivar al registro del resultado del set y continuación de la fuente con sus sets restantes.

### 1.4 Descripción funcional
El nodo lee `search_result` del contexto, valida su consistencia (estructura completa y, en éxito, lista de referencias presente con conteo ≥ 0), evalúa la condición `estado == exito y conteo de referencias > 0` y bifurca. Es una decisión pura: no re-consulta la plataforma y no realiza registros; la tipificación error vs. suceso del camino No pertenece al nodo de registro. Una inconsistencia del contrato recibido se trata como violación de contrato y aborta la corrida en "Finalizar Proceso" con estado *error*.

**Separación de responsabilidades:**
- *Flujo de negocio:* bifurcación entre capturar ofertas del set corriente u omitir el set con registro.
- *Implementación técnica:* evaluación pura en memoria sobre el contexto; sin acceso externo.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos por set, captura y almacena información original de ofertas según políticas de captura por fuente; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no contiene lógica de ese tipo.

### 1.5 Entradas
- Contexto de ejecución: `search_result` = {estado: exito|fallo, codigo_motivo, evidencia_acotada, ofertas_primera_pagina: [referencias], estado_paginacion, total_declarado (o indeterminado), set_indice, numero_de_intentos}; `run_id`; `source_id`; `session_id`.

### 1.6 Salidas
- **Rama Sí:** control a "Capturar ofertas" con contrato "referencias no vacías + estado de paginación disponibles".
- **Rama No:** control a "Registrar suceso o error en 'errores o sucesos'" con `search_result` disponible como carga de registro.
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-02).

### 1.7 Reglas de negocio
- **RN-01:** Evaluación pura sobre `search_result` en el contexto; prohibido re-consultar la plataforma desde este nodo.
- **RN-02:** Condición de la decisión = `search_result.estado == exito` y conteo de referencias de `ofertas_primera_pagina` > 0.
- **RN-03:** Consulta exitosa con conteo 0 = resultado válido sin ofertas en el set corriente → rama No (registro como suceso, tipificado aguas abajo).
- **RN-04:** Validación de consistencia del contrato recibido: estructura completa de `search_result` y, si estado = exito, lista de referencias presente con conteo ≥ 0. La violación se trata como falla visible (aborto), no como degradación silenciosa.
- **RN-05:** Este nodo no registra eventos ni errores y no tipifica error vs. suceso; ambas responsabilidades pertenecen al nodo de la rama No.
- **RN-06:** La rama Sí garantiza el contrato "referencias no vacías + estado de paginación disponibles"; la rama No garantiza `search_result` disponible como carga de registro.
- **RN-07:** No existe nodo de conteo en el flujo; el registro de auditoría de sesión pertenece a "Capturar ofertas".
- **RN-08:** La rama No omite el set de filtros corriente, no la fuente; la continuación con los sets restantes o el cierre de la fuente los decide "¿Quedan sets de filtros por aplicar en esta fuente?" tras el registro.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** `search_result` presente y accesible en el contexto antes de evaluar.
- **VAL-02:** Estructura completa de `search_result` (incluido `set_indice`); si estado = exito, lista de referencias presente (puede ser vacía) y conteo ≥ 0.
- **VAL-03:** La rama Sí solo se ejecuta con estado = exito y conteo > 0.

### 1.9 Condiciones
- **Continuación (Sí):** estado = exito y conteo > 0 y consistencia validada → "Capturar ofertas".
- **Derivación a registro (No):** estado = fallo (cualquier código), o estado = exito con conteo = 0, y consistencia validada → nodo de registro; el set corriente queda omitido y la fuente continúa aguas abajo con sus sets restantes (RN-08).
- **Aborto:** `search_result` ausente/corrupto (ERR-01); estructura inválida o éxito sin lista de referencias (ERR-02) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
Nodo de decisión binaria:
- **Sí** (`estado == exito` y conteo de referencias > 0) → "Capturar ofertas".
- **No** (`estado == fallo`, o `estado == exito` y conteo == 0) → "Registrar suceso o error en 'errores o sucesos'".

### 1.11 Manejo de errores y excepciones

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | `search_result` ausente o corrupto en contexto (violación de contrato de "Aplicar filtros" v1.1) | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`) | Aborto | error |
| ERR-02 | Estructura de `search_result` inválida, o estado exito sin lista de referencias presente | 2 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`) | Aborto | error |

Escenarios límite cubiertos: consulta fallida con cualquier código de motivo (rama No, set omitido, fuente continúa con sets restantes); consulta exitosa sin ofertas (rama No, registro como suceso aguas abajo); consulta exitosa con ofertas (rama Sí); violaciones de contrato entre nodos (aborto visible). La decisión no interpreta codigo_motivo ni contenido de ofertas (RN-01, RN-05).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales" v1.1 (provee `search_result` con `set_indice`).
- **Sucesor normal (Sí):** "Capturar ofertas".
- **Sucesor de fallo/vacío (No):** "Registrar suceso o error en 'errores o sucesos'" (que enruta a la decisión de sets, RN-08).
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** `search_result` estructurado con `set_indice` (contrato de "Aplicar filtros" v1.1).
- **Contratos entregados:** rama Sí → "referencias no vacías + estado de paginación disponibles"; rama No → `search_result` como carga de registro.
- **Impactos aprobados sobre nodos futuros:**
  1. El nodo de registro (rama No) consumirá `search_result` completo, tipificará error vs. suceso según estado/codigo_motivo/conteo, incluirá `set_indice`, y enrutará a "¿Quedan sets de filtros por aplicar en esta fuente?".
  2. "Capturar ofertas" consumirá `ofertas_primera_pagina` y `estado_paginacion` bajo contrato de no vaciedad, aplicará `politicas_de_captura` y escribirá la auditoría de sesión en "control de sesiones".
  3. La decisión "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" cerrará el bucle de captura del set; la decisión de sets cerrará la fuente o reentrará a "Aplicar filtros".

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Nodo de evaluación pura: sin I/O externo, sin escrituras en bases de datos salvo el evento crítico del protocolo de aborto.
- No ramificar ni tipificar por codigo_motivo en este nodo: la bifurcación es exclusivamente por estado + conteo (RN-02, RN-03).
- No registrar en este nodo (RN-05).
- La rama No nunca descarta la fuente por sí misma (RN-08); el alcance del descarte es el set corriente.
- La validación de consistencia (RN-04) es defensiva ante bugs del nodo de búsqueda; no debe usarse para lógica de negocio.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer `search_result` del contexto | Contexto (`search_result` con `set_indice`, `run_id`, `source_id`, `session_id`) | Acceder a `search_result` desde el contexto; no re-consultar la plataforma (RN-01) | `search_result` | VAL-01 | ERR-01 |
| 2 | Validar consistencia del contrato | `search_result` | Verificar estructura completa incluido `set_indice` (VAL-02); si estado = exito, verificar lista de referencias presente con conteo ≥ 0 | `search_result` validado | VAL-02 | ERR-02 |
| 3 | Evaluar condición "se encontraron ofertas" | `search_result` validado | Condición = estado == exito y conteo de referencias > 0 (RN-02, RN-03) | Resultado booleano (Sí/No) | — | Ninguna aplicable |
| 4 | Rama Sí — Entregar control | Resultado = Sí; contexto | Cerrar el nodo y entregar control con contrato "referencias no vacías + estado de paginación disponibles" (RN-06) | Flujo hacia "Capturar ofertas" | VAL-03 | Ninguna |
| 5 | Rama No — Entregar control con carga de registro | Resultado = No; `search_result` | No registrar ni tipificar en este nodo (RN-05); entregar control con `search_result` disponible como carga de registro (RN-06); el set corriente queda omitido y la fuente continúa aguas abajo (RN-08) | Flujo hacia "Registrar suceso o error en 'errores o sucesos'" | — | Ninguna |

---

# Especificación Canónica — Nodo Proceso: "Capturar ofertas"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Captura de ofertas — "Capturar ofertas".

### 1.2 Posición en el flujo
Entre la rama Sí de "¿Se encontraron ofertas?" (v1.1, primer lote del set) o la rama Sí de "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" (lotes siguientes), y "Registrar ofertas capturadas en 'Ofertas Totales'". Nodo re-entrante por lote.

### 1.3 Objetivo
Capturar la información completa disponible de las ofertas del lote corriente de la búsqueda del set actual, aplicando las `politicas_de_captura` efectivas de la fuente mediante el adaptador de plataforma (mecanismo masivo o incremental), actualizar el progreso de captura y escribir la auditoría de sesión en "control de sesiones" en el primer lote del set. **No registra ofertas**: la persistencia en "Ofertas Totales" pertenece al nodo siguiente.

### 1.4 Descripción funcional
El nodo lee del contexto los insumos de captura (`search_result` con referencias y paginación, sesión activa, políticas efectivas, progreso de captura). En el primer lote del (session_id, set_indice) escribe el registro de auditoría en "control de sesiones" (con tolerancia a degradación). Determina el alcance del lote (primera pasada: referencias de `search_result`; pasadas siguientes: página siguiente vía `estado_paginacion`, con pausas y estrategia anti-bloqueo), verificando límites antes de capturar (`max_paginas`, `max_ofertas_por_corrida` por corrida+fuente). Captura la información completa disponible de cada oferta del lote según el adaptador; una falla por oferta la excluye con evento propio sin afectar el lote. Evalúa el resultado del lote (éxito con lote completo o parcial por ofertas omitidas; fallo con código y lote parcial conservado), actualiza progreso (`paginas_consumidas`, `capturadas_acumuladas_fuente`, `limite_alcanzado`) y guarda `capture_batch` y `estado_captura` en el contexto. Entrega control a "Registrar ofertas capturadas en 'Ofertas Totales'".

**Separación de responsabilidades:**
- *Flujo de negocio:* recuperar la información original de las ofertas dentro de los límites seguros de la fuente.
- *Implementación técnica:* adaptador de plataforma (mecanismo masivo/incremental), pausas, estrategia anti-bloqueo, reintentos a nivel página, auditoría de sesión.
- *Límite:* este nodo no registra ofertas, no interpreta ni clasifica contenido, no decide continuación del bucle (propiedad de las decisiones siguientes).

### 1.5 Entradas
- Contexto de ejecución: `search_result` (`ofertas_primera_pagina`, `estado_paginacion`, `set_indice`, `total_declarado`), sesión activa (`session_id` + handle), `politicas_de_captura` efectivas (`max_paginas`, `max_ofertas_por_corrida` [alcance corrida+fuente], `pausa_entre_lotes`, `estrategia_anti_bloqueo`), progreso de captura de la búsqueda actual (`paginas_consumidas`, `capturadas_acumuladas_fuente`), `run_id`, `source_id`.
- Parámetros globales: máximo de reintentos (por defecto 2), backoff.

### 1.6 Salidas
- `capture_batch` en contexto: lista de ofertas capturadas con información original + metadatos de trazabilidad (`run_id`, `source_id`, `session_id`, `set_indice`, referencia).
- `estado_captura` en contexto: `{estado: exito|fallo, codigo_motivo, paginas_consumidas, capturadas_acumuladas_fuente, limite_alcanzado}`.
- Registro de auditoría de sesión en "control de sesiones" (primer lote del set) o marca de auditoría degradada.
- Control único a "Registrar ofertas capturadas en 'Ofertas Totales'".
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-09).

### 1.7 Reglas de negocio
- **RN-01:** El nodo opera sobre el contexto; no relee el almacén de configuración.
- **RN-02:** La granularidad del lote la define el adaptador de plataforma: masivo = hasta los límites en una pasada; incremental = un lote/página por pasada con pausas. La configuración solo acota mediante límites (RN-10 de INICIO v1.3).
- **RN-03:** Se captura toda la información disponible de cada oferta (información original); prohibido interpretar, clasificar o evaluar contenido.
- **RN-04:** Falla en una oferta individual = exclusión de la oferta del lote + evento `oferta_no_capturada` con su referencia; el lote continúa.
- **RN-05:** Límites verificados antes de capturar: `max_paginas` por búsqueda (set) y `max_ofertas_por_corrida` con alcance (corrida, fuente). Límite alcanzado → lote vacío + `limite_alcanzado` = true.
- **RN-06:** Reintentos condicionales a nivel página/captura, idénticos a los nodos anteriores: reintentables solo `fuente_inalcanzable` y `timeout_captura`, con los mismos parámetros globales; el resto produce fallo inmediato. Ante fallo de lote, se conserva el lote parcial capturado.
- **RN-07:** Auditoría de sesión por (session_id, set_indice), escrita en el primer lote del set: {session_id, run_id, source_id, set_indice, timestamp, total_declarado, conteo_primera_pagina, hay_mas_paginas, coherencia, estado_auditoria}. Fallo de escritura: reintento único; si persiste, evento crítico y continuación con auditoría degradada.
- **RN-08:** Este nodo no escribe en "Ofertas Totales"; el registro de ofertas pertenece exclusivamente al nodo siguiente.
- **RN-09:** Evidencia acotada y sin datos sensibles; trazabilidad `run_id` + `source_id` + `session_id` + `set_indice` en todo evento y en cada oferta capturada.
- **RN-10:** `limite_alcanzado` es la señal de cierre para las decisiones siguientes: "¿Quedan ofertas por capturar en la búsqueda actual?" lo excluye de su condición Sí, y "¿Quedan sets de filtros por aplicar en esta fuente?" lo trata como cierre de la fuente.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** Insumos de captura presentes y accesibles en el contexto antes de operar.
- **VAL-02:** Límites (`max_paginas`, `max_ofertas_por_corrida`) verificados antes de obtener/capturar cualquier lote.
- **VAL-03:** Política de reintentos: contador ≤ máximo configurado; backoff aplicado; solo códigos reintentables.
- **VAL-04:** En mecanismo incremental, `pausa_entre_lotes` y `estrategia_anti_bloqueo` aplicadas entre capturas/páginas.
- **VAL-05:** `capture_batch` y `estado_captura` completos en el contexto con trazabilidad antes de entregar control.
- **VAL-06:** Registro de auditoría con esquema completo, o marca degradada documentada.

### 1.9 Condiciones
- **Continuación normal:** `estado_captura` construido (éxito con lote completo/parcial por ofertas omitidas, o fallo con lote parcial, o lote vacío por límite) → entrega de control al registro.
- **Fallo de lote (no aborto):** código de fallo con lote parcial conservado → el registro persiste lo capturado y las decisiones siguientes cierran el bucle según sus condiciones.
- **Aborto:** insumos ausentes/corruptos (ERR-01); corrupción del contexto (ERR-09) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
No es nodo de decisión. Salida normal única hacia "Registrar ofertas capturadas en 'Ofertas Totales'"; salida de aborto hacia "Finalizar Proceso" (estado *error*). Re-entrada desde la rama Sí de "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?".

### 1.11 Manejo de errores y excepciones
*Fallo de lote* = `estado_captura` con código de motivo y lote parcial conservado; no aborta. *Aborto* = terminación en "Finalizar Proceso" con estado *error*. *Reintentable* = sujeto a RN-06/VAL-03.

| Código | Error / excepción | Reintentable | Detección (paso) | Registro / acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Insumos de captura ausentes/corruptos en contexto (violación de contratos previos) | No | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`); aborto | error |
| ERR-02 | Fallo de escritura de auditoría de sesión tras reintento único | No | 2 | Evento crítico; continuar con auditoría degradada (RN-07) | continúa |
| ERR-03 | `fuente_inalcanzable`: red/DNS/plataforma caída al obtener página/capturar | Sí | 3–4 | Con intentos restantes: backoff y reintento; agotados: fallo de lote con lote parcial | continúa (fallo de lote) |
| ERR-04 | `timeout_captura`: página/captura fuera del timeout | Sí | 3–4 | Ídem ERR-03 | continúa (fallo de lote) |
| ERR-05 | `sesion_expirada`: sesión caducada durante la captura | No | 4 | Fallo de lote con lote parcial; sin re-ingreso | continúa (fallo de lote) |
| ERR-06 | `bloqueo_plataforma`: captcha/anti-bot/desafío durante la captura | No | 4 | Fallo de lote con lote parcial | continúa (fallo de lote) |
| ERR-07 | `respuesta_invalida`: página de resultados/detalle no interpretable | No | 3–4 | Fallo de lote con lote parcial | continúa (fallo de lote) |
| ERR-08 | `error_interno_captura`: falla interna inesperada durante la captura | No | 3–5 | Fallo de lote con lote parcial | continúa (fallo de lote) |
| ERR-09 | Corrupción del contexto al guardar `capture_batch`/`estado_captura` | No | 6 | Evento crítico en "errores o sucesos"; aborto | error |
| EVT-01 | `oferta_no_capturada`: falla en una oferta individual | No | 4 | Evento con referencia de la oferta; exclusión del lote; el lote continúa (RN-04) | continúa |

**Contrato de códigos de motivo (captura):** `captura_exitosa`, `fuente_inalcanzable`, `timeout_captura`, `sesion_expirada`, `bloqueo_plataforma`, `respuesta_invalida`, `error_interno_captura`; evento por oferta: `oferta_no_capturada`.

Escenarios límite cubiertos: mecanismo masivo (una pasada hasta límites) vs. incremental (lotes con pausas); límite de páginas o de ofertas alcanzado (lote vacío + `limite_alcanzado`); oferta individual defectuosa (EVT-01); caída transitoria de página (ERR-03/ERR-04 con reintento); bloqueo o sesión expirada a mitad de lote (lote parcial conservado); lote vacío por límites igualmente entregado al registro (no-op aguas abajo).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesores:** rama Sí de "¿Se encontraron ofertas?" v1.1 (primer lote del set); rama Sí de "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" (lotes siguientes).
- **Sucesor normal:** "Registrar ofertas capturadas en 'Ofertas Totales'".
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** `search_result` con referencias y paginación ("Aplicar filtros" v1.1); sesión activa ("Entrar" v1.1); `politicas_de_captura` efectivas (INICIO v1.3); progreso de captura de la búsqueda actual.
- **Contratos entregados:** `capture_batch` (información original + trazabilidad); `estado_captura` (progreso + `limite_alcanzado`); auditoría de sesión por (session_id, set_indice).
- **Impactos aprobados sobre nodos futuros:**
  1. "Registrar ofertas capturadas en 'Ofertas Totales'" consumirá `capture_batch`; lote vacío = no-op; la identidad de oferta (deduplicación entre sets/páginas) se definirá en su iteración.
  2. "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" usará `estado_captura`: Sí requiere estado = exito y páginas restantes según `estado_paginacion` y `paginas_consumidas < max_paginas` y no `limite_alcanzado`.
  3. "¿Quedan sets de filtros por aplicar en esta fuente?" tratará `limite_alcanzado` como cierre de la fuente.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología; el adaptador por fuente encapsula el mecanismo de captura (masivo/incremental) y el acceso al detalle de oferta.
- Aplicar `pausa_entre_lotes` y `estrategia_anti_bloqueo` en mecanismo incremental (RN-02, VAL-04); nunca credenciales/tokens/cookies en eventos o bases de datos.
- El progreso de captura (`paginas_consumidas`, `capturadas_acumuladas_fuente`) debe persistir en el contexto entre pasadas del bucle; `capturadas_acumuladas_fuente` alimenta el límite por (corrida, fuente) (RN-05).
- Lote parcial ante fallo de lote: conservar lo capturado; el registro lo persiste (RN-06).
- Auditoría de sesión: escribir una única vez por (session_id, set_indice); idempotencia requerida ante reentradas del bucle.
- No escribir en "Ofertas Totales" (RN-08); no interpretar contenido (RN-03).

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer insumos de captura del contexto | Contexto (`search_result`, sesión, políticas efectivas, progreso de captura, `run_id`, `source_id`, parámetros de reintento) | Acceder a insumos desde el contexto; no releer almacén (RN-01) | Insumos de captura | VAL-01 | ERR-01 |
| 2 | Escribir auditoría de sesión (solo primer lote del set) | `session_id`, `set_indice`, `search_result` (total_declarado, conteo primera página, paginación) | Si primer lote de (session_id, set_indice): escribir registro en "control de sesiones" con esquema completo y estado_auditoria = completa (RN-07). Fallo: reintento único; si persiste, evento crítico y continuar degradado | Registro persistido o marca degradada | VAL-06 | ERR-02 |
| 3 | Determinar alcance del lote y verificar límites | Progreso de captura; políticas; `estado_paginacion` | Primera pasada: referencias de `search_result`. Pasadas siguientes: obtener página siguiente vía `estado_paginacion` con `pausa_entre_lotes` y `estrategia_anti_bloqueo` (VAL-04). Verificar límites antes de capturar (VAL-02/RN-05); límite alcanzado → lote vacío + `limite_alcanzado` y salto al paso 5 | Alcance del lote (referencias) o lote vacío con límite | VAL-02, VAL-03 | ERR-03, ERR-04, ERR-08 |
| 4 | Capturar información completa por oferta | Referencias del lote; sesión; adaptador | Por cada referencia: capturar toda la información disponible según el adaptador (RN-03); en incremental, pausas y anti-bloqueo entre capturas (VAL-04). Falla por oferta: excluir + evento `oferta_no_capturada` con referencia; el lote continúa (RN-04) | Ofertas capturadas (información original) | VAL-04 | EVT-01; ERR-05, ERR-06, ERR-07, ERR-08 |
| 5 | Evaluar resultado del lote y construir `estado_captura` | Resultado de capturas; progreso; contador de intentos | Éxito (lote completo o parcial por ofertas omitidas) o fallo con código y lote parcial conservado (RN-06); actualizar `paginas_consumidas` y `capturadas_acumuladas_fuente`; calcular `limite_alcanzado` (RN-05) | `estado_captura` + lote capturado | — | ERR-03, ERR-04, ERR-05, ERR-06, ERR-07, ERR-08 |
| 6 | Guardar `capture_batch` y `estado_captura` en contexto | Lote capturado; `estado_captura` | Persistir ambos en contexto con metadatos de trazabilidad por oferta (`run_id`, `source_id`, `session_id`, `set_indice`, referencia) (RN-09) | Contexto actualizado | VAL-05 | ERR-09 |
| 7 | Entregar control | Contexto con `capture_batch` y `estado_captura` | Cerrar el nodo y entregar control al registro | Flujo hacia "Registrar ofertas capturadas en 'Ofertas Totales'" | `capture_batch` y `estado_captura` presentes | Ninguna |

---

# Especificación Canónica — Nodo Proceso: "Registrar ofertas capturadas en 'Ofertas Totales'"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Registro de ofertas — "Registrar ofertas capturadas en 'Ofertas Totales'".

### 1.2 Posición en el flujo
Entre "Capturar ofertas" (v1.0) y la decisión "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?". Posición definitiva.

### 1.3 Objetivo
Persistir el lote capturado (`capture_batch`) en la base de datos "Ofertas Totales" conservando la información original de cada oferta con trazabilidad completa y el identificador externo crudo cuando exista, y liberar el lote del contexto. **Este nodo no deduplica, no normaliza y no verifica identidad de ofertas**: la deduplicación pertenece al Módulo 2 sobre este almacén crudo.

### 1.4 Descripción funcional
El nodo lee `capture_batch` del contexto. Si el lote está vacío, no escribe nada y continúa (no-op). Si no, persiste todas las ofertas del lote en una única transacción: cada oferta se inserta como una fila nueva con su información original íntegra tal como llegó del adaptador, el campo `id_externo_url` en modo best-effort (ID de la plataforma o URL cruda; nulo si el adaptador no pudo extraerlo) y los metadatos de trazabilidad (`run_id`, `source_id`, `session_id`, `set_indice`, marca de tiempo de captura). Ante fallo de escritura o transacción, reintenta una vez; si persiste, emite evento crítico y aborta la corrida ("Ofertas Totales" es la salida esencial del módulo). Tras persistir, libera el lote del contexto y entrega control a la decisión de continuación.

**Separación de responsabilidades:**
- *Flujo de negocio:* conservar la información original de cada oferta capturada con trazabilidad.
- *Implementación técnica:* transaccionalidad, reintento único, liberación de memoria.
- *Límite:* este nodo **no** deduplica (Módulo 2), **no** normaliza URLs ni contenido (Módulo 2), **no** interpreta ni clasifica contenido, **no** sobrescribe filas existentes (solo inserta).

### 1.5 Entradas
- Contexto de ejecución: `capture_batch` (ofertas con información original íntegra, `id_externo_url` best-effort, y metadatos `run_id`, `source_id`, `session_id`, `set_indice`, referencia), conexión a "Ofertas Totales".

### 1.6 Salidas
- Lote persistido en "Ofertas Totales" (una fila nueva por oferta capturada), o ninguna escritura si el lote está vacío.
- Contexto con `capture_batch` liberado.
- Control único a "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?".
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-02).

### 1.7 Reglas de negocio
- **RN-01:** El nodo opera sobre el contexto; no relee almacenes de configuración ni re-consulta plataformas.
- **RN-02:** Inserción simple: cada oferta capturada produce una fila nueva; sin verificación de duplicados, sin comparación contra filas existentes, sin sobrescritura. La deduplicación pertenece al Módulo 2.
- **RN-03:** Cada fila conserva la información original íntegra tal como llegó del adaptador, más `id_externo_url` (best-effort, nullable) y los metadatos de trazabilidad (`run_id`, `source_id`, `session_id`, `set_indice`, marca de tiempo de captura).
- **RN-04:** Prohibido transformar, normalizar o limpiar contenido o URLs en este nodo; lo crudo se conserva crudo. La normalización pertenece al Módulo 2.
- **RN-05:** Lote vacío = no-op: sin escrituras, sin error, continuación normal.
- **RN-06:** El lote se persiste en una única transacción (todo o nada); no se admiten lotes parcialmente persistidos.
- **RN-07:** Fallo de escritura o transacción en "Ofertas Totales": reintento único; si persiste, evento crítico y aborto. Justificación: es la salida esencial del módulo; continuar sin persistir produciría corridas que descubren pero no almacenan.
- **RN-08:** Tras la persistencia exitosa (o no-op), el lote se libera del contexto.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** `capture_batch` presente y accesible en el contexto antes de operar.
- **VAL-02:** Cada oferta del lote posee información original y metadatos de trazabilidad completos; `id_externo_url` puede ser nulo.
- **VAL-03:** Persistencia ejecutada en una única transacción (RN-06).
- **VAL-04:** Lote liberado del contexto y control entregado tras persistencia o no-op.

### 1.9 Condiciones
- **Continuación normal:** lote persistido (transacción completa) o lote vacío (no-op) → entrega de control a la decisión de continuación.
- **Aborto:** `capture_batch` ausente/corrupto (ERR-01); fallo de escritura/transacción tras reintento único (ERR-02) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
No es nodo de decisión. Salida normal única hacia "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"; salida de aborto hacia "Finalizar Proceso" (estado *error*).

### 1.11 Manejo de errores y excepciones

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | `capture_batch` ausente o corrupto en contexto (violación de contrato de "Capturar ofertas" v1.0) | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`) | Aborto | error |
| ERR-02 | Fallo de escritura o transacción en "Ofertas Totales" tras reintento único | 3 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`) | Aborto (RN-07) | error |

Escenarios límite cubiertos: lote vacío por límite alcanzado o lote fallido (no-op, RN-05); lote con ofertas sin `id_externo_url` (se almacenan con campo nulo; el Módulo 2 las resolverá por capa difusa); transacción fallida a mitad (rollback completo, reintento único, aborto si persiste); caída de la corrida tras persistir (lo persistido queda, el lote liberado no se reprocesa).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** "Capturar ofertas" v1.0 (provee `capture_batch` con trazabilidad e `id_externo_url` best-effort).
- **Sucesor normal:** "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?".
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** `capture_batch` estructurado (contrato de "Capturar ofertas" v1.0).
- **Contratos entregados:** "Ofertas Totales" como almacén crudo de información original con trazabilidad e `id_externo_url` crudo; lote liberado del contexto.
- **Impactos aprobados sobre nodos futuros:**
  1. La decisión de continuación no depende de este nodo (lee `estado_captura` de "Capturar ofertas").
  2. El Módulo 2 consumirá "Ofertas Totales" y aplicará deduplicación en dos capas (estricta por `source_id`+`id_externo_url` normalizado; difusa por título+empresa+ubicación para ofertas sin coincidencia o sin ID). Este módulo no ejecuta ni anticipa esa lógica.
  3. Esquema funcional de "Ofertas Totales" (nivel negocio): por fila, información original íntegra, `id_externo_url` (nullable), `run_id`, `source_id`, `session_id`, `set_indice`, marca de tiempo de captura.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Insertar siempre filas nuevas; nunca actualizar ni sobrescribir filas existentes (RN-02).
- No normalizar URLs ni contenido (RN-04); `id_externo_url` se conserva tal como lo extrajo el adaptador.
- Transacción única por lote (RN-06); rollback completo ante cualquier fallo parcial.
- Reintento único ante fallo de escritura; aborto si persiste (RN-07).
- No interpretar, clasificar ni evaluar contenido (límite del módulo).
- Liberar el lote del contexto inmediatamente tras persistir o decidir no-op (RN-08).

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer lote del contexto | Contexto (`capture_batch`, conexión a "Ofertas Totales") | Acceder al lote desde el contexto; no releer almacenes ni re-consultar plataformas (RN-01) | Lote a persistir | VAL-01 | ERR-01 |
| 2 | Evaluar lote vacío | Lote | Si lote vacío: no-op; salto al paso 4 (RN-05) | Señal de continuación | — | Ninguna |
| 3 | Persistir lote transaccionalmente | Lote con información original, `id_externo_url` y metadatos | En una única transacción (RN-06/VAL-03): insertar cada oferta como fila nueva con información original íntegra, `id_externo_url` (nullable) y metadatos de trazabilidad (RN-02, RN-03, RN-04). Fallo de escritura/transacción: reintento único; si persiste, aborto (RN-07) | Lote persistido en "Ofertas Totales" | VAL-02, VAL-03 | ERR-02 |
| 4 | Liberar lote y entregar control | Contexto | Liberar `capture_batch` del contexto (RN-08); cerrar el nodo y entregar control | Contexto con lote liberado; flujo hacia "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" | VAL-04 | Ninguna |

---

# Especificación Canónica — Nodo Decisión: "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Decisión de continuación del bucle de captura — "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?".

### 1.2 Posición en el flujo
Entre "Registrar ofertas capturadas en 'Ofertas Totales'" (v1.0) y, según rama, "Capturar ofertas" (Sí, siguiente lote) o "¿Quedan sets de filtros por aplicar en esta fuente?" (No). Punto único de control del bucle de lotes de la búsqueda del set corriente.

### 1.3 Objetivo
Evaluar si la búsqueda del set corriente tiene aún ofertas capturables dentro de los límites de política de la fuente, y bifurcar: con Sí, reentrar a "Capturar ofertas" para el siguiente lote; con No, cerrar la búsqueda y pasar a la evaluación de sets de filtros.

### 1.4 Descripción funcional
El nodo lee del contexto `estado_captura`, `estado_paginacion` y las políticas efectivas de captura, valida su consistencia y evalúa la condición compuesta: `estado_captura.estado == exito` y `estado_paginacion` reporta pendientes y `paginas_consumidas < max_paginas` y `limite_alcanzado == false`. Con resultado Sí entrega control a "Capturar ofertas"; con No entrega control a "¿Quedan sets de filtros por aplicar en esta fuente?". Es una decisión pura: no consulta la plataforma, no registra, no reintenta y no muta estado. Una inconsistencia de los insumos se trata como violación de contrato y aborta la corrida en "Finalizar Proceso" con estado *error*.

**Separación de responsabilidades:**
- *Flujo de negocio:* control de continuación del bucle de captura acotado por políticas.
- *Implementación técnica:* evaluación pura en memoria sobre el contexto; sin acceso externo.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos por set, captura y almacena información original de ofertas según políticas de captura por fuente; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no contiene lógica de ese tipo.

### 1.5 Entradas
- Contexto de ejecución: `estado_captura` = {estado: exito|fallo, codigo_motivo, paginas_consumidas, capturadas_acumuladas_fuente, limite_alcanzado}; `estado_paginacion` de `search_result`; `politicas_de_captura` efectivas (`max_paginas`, `max_ofertas_por_corrida`); `run_id`; `source_id`; `session_id`; `set_indice`.

### 1.6 Salidas
- **Rama Sí:** control a "Capturar ofertas" (siguiente lote).
- **Rama No:** control a "¿Quedan sets de filtros por aplicar en esta fuente?".
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-02).

### 1.7 Reglas de negocio
- **RN-01:** Evaluación pura sobre el contexto; prohibido consultar la plataforma desde este nodo.
- **RN-02:** Condición de la rama Sí = conjunción de: `estado_captura.estado == exito`; `estado_paginacion` reporta pendientes; `paginas_consumidas < max_paginas`; `limite_alcanzado == false`.
- **RN-03:** `estado_captura.estado == fallo` cierra la búsqueda (rama No); los reintentos ante fallas transitorias son responsabilidad interna del nodo de captura y no se duplican aquí.
- **RN-04:** Lote vacío con páginas restantes continúa (rama Sí): una página intermedia vacía es escenario válido; el bucle queda acotado porque `paginas_consumidas` incrementa en cada pasada.
- **RN-05:** Validación de consistencia de insumos: estructura completa de `estado_captura` y presencia de políticas. La violación se trata como falla visible (aborto), no como degradación silenciosa.
- **RN-06:** Este nodo no registra eventos, no reintenta y no muta estado del contexto.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** Insumos (`estado_captura`, `estado_paginacion`, políticas) presentes y accesibles en el contexto antes de evaluar.
- **VAL-02:** Estructura completa de `estado_captura` (estado, paginas_consumidas, limite_alcanzado) y presencia de `max_paginas` y `max_ofertas_por_corrida`.
- **VAL-03:** La rama Sí solo se ejecuta con la condición compuesta completa (RN-02).

### 1.9 Condiciones
- **Continuación (Sí):** los cuatro conjuntos de RN-02 se cumplen → "Capturar ofertas".
- **Cierre de búsqueda (No):** cualquiera de los cuatro falla (incluido `estado_captura.estado == fallo`) → "¿Quedan sets de filtros por aplicar en esta fuente?".
- **Aborto:** insumos ausentes/corruptos (ERR-01); estructura inválida o políticas ausentes (ERR-02) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
Nodo de decisión binaria:
- **Sí** (condición compuesta RN-02 verdadera) → "Capturar ofertas".
- **No** (cualquier conjunto falso) → "¿Quedan sets de filtros por aplicar en esta fuente?".

### 1.11 Manejo de errores y excepciones

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Insumos ausentes o corruptos en contexto (violación de contratos de "Capturar ofertas" v1.0 / "Aplicar filtros" v1.1) | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`) | Aborto | error |
| ERR-02 | Estructura de `estado_captura` inválida, o políticas (`max_paginas`, `max_ofertas_por_corrida`) ausentes | 2 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`+`set_indice`) | Aborto | error |

Escenarios límite cubiertos: lote fallido con código no reintentable (No, cierre de búsqueda); lote fallido tras reintentos agotados (idem); límite de páginas o de ofertas alcanzado (No); paginación sin pendientes (No); página intermedia vacía con pendientes y límites holgados (Sí, acotado por `max_paginas`); violaciones de contrato entre nodos (aborto visible).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** "Registrar ofertas capturadas en 'Ofertas Totales'" v1.0.
- **Sucesor normal (Sí):** "Capturar ofertas" v1.0 (re-entrada con progreso actualizado).
- **Sucesor de cierre (No):** "¿Quedan sets de filtros por aplicar en esta fuente?".
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** `estado_captura` con progreso y `limite_alcanzado` ("Capturar ofertas" v1.0); `estado_paginacion` ("Aplicar filtros" v1.1); políticas efectivas (INICIO v1.3).
- **Contratos entregados:** rama Sí → re-entrada de captura; rama No → cierre de la búsqueda actual.
- **Impactos aprobados sobre nodos futuros:**
  1. "¿Quedan sets de filtros por aplicar en esta fuente?" tratará además `limite_alcanzado == true` como cierre de la fuente aunque queden sets pendientes.
  2. La rama Sí reentra a "Capturar ofertas" bajo el contrato de progreso actualizado (`paginas_consumidas`, `capturadas_acumuladas_fuente`).

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Nodo de evaluación pura: sin I/O externo, sin escrituras, sin reintentos, sin mutación de estado (RN-01, RN-03, RN-06).
- La condición compuesta debe evaluarse en el orden definido (RN-02) por claridad de diagnóstico; el resultado es el mismo en cualquier orden.
- No interpretar `codigo_motivo` ni contenido de ofertas en este nodo; la bifurcación usa exclusivamente estado, paginación y límites.
- La validación de consistencia (RN-05) es defensiva ante bugs de nodos anteriores; no debe usarse para lógica de negocio.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer insumos de la decisión del contexto | Contexto (`estado_captura`, `estado_paginacion`, políticas efectivas, ids) | Acceder a insumos desde el contexto; no consultar la plataforma (RN-01) | Insumos de decisión | VAL-01 | ERR-01 |
| 2 | Validar consistencia de insumos | Insumos | Verificar estructura completa de `estado_captura` y presencia de `max_paginas` y `max_ofertas_por_corrida` (RN-05) | Insumos validados | VAL-02 | ERR-02 |
| 3 | Evaluar condición compuesta | Insumos validados | Condición Sí = estado == exito y paginación con pendientes y paginas_consumidas < max_paginas y limite_alcanzado == false (RN-02, RN-03, RN-04); en caso contrario, No | Resultado booleano (Sí/No) | — | Ninguna aplicable |
| 4 | Rama Sí — Entregar control | Resultado = Sí; contexto | Cerrar el nodo y entregar control para el siguiente lote | Flujo hacia "Capturar ofertas" | VAL-03 | Ninguna |
| 5 | Rama No — Entregar control | Resultado = No; contexto | Cerrar el nodo y entregar control para la evaluación de sets | Flujo hacia "¿Quedan sets de filtros por aplicar en esta fuente?" | — | Ninguna |

---

# Especificación Canónica — Nodo Decisión: "¿Quedan sets de filtros por aplicar en esta fuente?"

**Versión:** 1.0 (aprobada) · **Módulo:** Descubrimiento de oportunidades (Módulo 1 de la automatización de búsqueda de empleo)

---

## 1. Información general

### 1.1 Nombre del nodo
Decisión de continuación por sets de filtros — "¿Quedan sets de filtros por aplicar en esta fuente?".

### 1.2 Posición en el flujo
Entre la rama No de "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" (v1.0) y, según rama, "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales" (Sí, siguiente set) o "¿Quedan fuentes por procesar en esta corrida?" (No, fuente terminada). Cierra el ciclo de sets de la fuente corriente.

### 1.3 Objetivo
Evaluar si la fuente corriente tiene sets de filtros pendientes y si las condiciones permiten continuar, y bifurcar: con Sí, reentrar al nodo de filtros con el siguiente set; con No, cerrar la fuente y retornar a la iteración de fuentes.

### 1.4 Descripción funcional
El nodo lee del contexto el iterador de sets, el `search_result` del set corriente, el `estado_captura` (discriminado por `set_indice`) y `limite_alcanzado`. Valida consistencia, clasifica si la fuente está comprometida (último fallo del set corriente con código del Grupo A), y evalúa la condición compuesta: quedan sets no procesados y `limite_alcanzado == false` y fuente no comprometida. Con Sí entrega control a "Aplicar los filtros básicos…"; con No entrega control a "¿Quedan fuentes por procesar en esta corrida?". Es una decisión pura: no consulta la plataforma, no registra, no reintenta y no muta estado (no avanza el iterador de sets; propiedad de "Aplicar filtros"). Una inconsistencia de insumos se trata como violación de contrato y aborta la corrida en "Finalizar Proceso" con estado *error*.

**Separación de responsabilidades:**
- *Flujo de negocio:* cierre del ciclo de sets de la fuente y retorno a la iteración de fuentes.
- *Implementación técnica:* evaluación pura en memoria sobre el contexto; sin acceso externo.

**Contexto del módulo (límites de alcance):** el módulo consulta fuentes configuradas, aplica filtros básicos por set, captura y almacena información original de ofertas según políticas de captura por fuente; no interpreta, clasifica, puntúa ni decide adecuación. Este nodo no contiene lógica de ese tipo.

### 1.5 Entradas
- Contexto de ejecución: iterador de sets (progreso de procesados vs. total, vinculado a `source_id`; propiedad de "Aplicar filtros" v1.1); `search_result` del set corriente (con `set_indice`); `estado_captura` (con `set_indice`, contrato de "Capturar ofertas" v1.1); `limite_alcanzado`; `run_id`; `source_id`; `session_id`.

### 1.6 Salidas
- **Rama Sí:** control a "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales" (siguiente set).
- **Rama No:** control a "¿Quedan fuentes por procesar en esta corrida?" (fuente terminada).
- **Aborto (excepción):** control a "Finalizar Proceso" con estado *error* (ERR-01, ERR-02).

### 1.7 Reglas de negocio
- **RN-01:** Evaluación pura sobre el contexto; prohibido consultar la plataforma desde este nodo.
- **RN-02:** Condición de la rama Sí = conjunción de: quedan sets no procesados; `limite_alcanzado == false`; `fuente_comprometida == false`.
- **RN-03:** La clasificación de códigos en Grupo A / Grupo B es propiedad exclusiva de este nodo (política centralizada de cierre de fuente):
  - **Grupo A — comprometen la fuente** (cierran la fuente): `sesion_expirada`, `bloqueo_plataforma`, `fuente_inalcanzable`, `timeout_consulta`, `timeout_captura`, `error_interno_consulta`, `error_interno_captura`.
  - **Grupo B — propios del set** (continúan con el siguiente set): `filtros_no_aplicables`, `respuesta_invalida`.
- **RN-04:** El resultado del set corriente se lee de `search_result` (si su búsqueda falló) y de `estado_captura` solo si `estado_captura.set_indice == set_indice` corriente (evita leer estado obsoleto de sets anteriores).
- **RN-05:** Validación de consistencia de insumos: iterador coherente con `source_id` y `search_result.set_indice` == set corriente. La violación se trata como falla visible (aborto), no como degradación silenciosa.
- **RN-06:** Este nodo no registra eventos, no reintenta y no muta estado; el iterador de sets lo avanza exclusivamente "Aplicar filtros" (RN-10 de ese nodo).
- **RN-07:** La fuente corriente ya figura como procesada en el iterador de fuentes (marcada al seleccionarse); la rama No no requiere mutación adicional.

### 1.8 Validaciones
*(Códigos locales a este nodo.)*
- **VAL-01:** Insumos (iterador de sets, `search_result`, `estado_captura`, `limite_alcanzado`) presentes y accesibles en el contexto antes de evaluar.
- **VAL-02:** Iterador coherente con `source_id`; `search_result.set_indice` == set corriente.
- **VAL-03:** La rama Sí solo se ejecuta con la condición compuesta completa (RN-02).

### 1.9 Condiciones
- **Continuación (Sí):** quedan sets no procesados y `limite_alcanzado == false` y fuente no comprometida → "Aplicar los filtros básicos…".
- **Cierre de fuente (No):** cualquiera de las tres falla (sin sets restantes, límite de ofertas de la fuente alcanzado, o fuente comprometida por fallo Grupo A) → "¿Quedan fuentes por procesar en esta corrida?".
- **Aborto:** insumos ausentes/corruptos (ERR-01); iterador incoherente o `set_indice` desalineado (ERR-02) → "Finalizar Proceso" con estado *error*.

### 1.10 Ramas de decisión
Nodo de decisión binaria:
- **Sí** (condición compuesta RN-02 verdadera) → "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales".
- **No** (cualquier conjunto falso) → "¿Quedan fuentes por procesar en esta corrida?".

### 1.11 Manejo de errores y excepciones

| Código | Error / excepción | Detección (paso) | Registro | Acción | Estado de salida |
|---|---|---|---|---|---|
| ERR-01 | Insumos ausentes o corruptos en contexto (violación de contratos previos) | 1 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`) | Aborto | error |
| ERR-02 | Iterador de sets incoherente con `source_id`, o `search_result.set_indice` desalineado con el set corriente | 2 | Evento crítico en "errores o sucesos" (`run_id`+`source_id`+`session_id`) | Aborto | error |

Escenarios límite cubiertos: sesión expirada o bloqueo anti-bot en el set corriente (fuente comprometida → No, cierre limpio sin recorrer sets restantes); límite de ofertas de la fuente alcanzado con sets pendientes (No); todos los sets procesados (No); set fallido con código Grupo B (Sí, siguiente set); búsqueda del set corriente exitosa sin captura posterior (fuente no comprometida por ese resultado).

### 1.12 Dependencias y contratos con otros nodos
- **Antecesor:** rama No de "¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?" v1.0.
- **Sucesor normal (Sí):** "Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales" v1.1.
- **Sucesor de cierre (No):** "¿Quedan fuentes por procesar en esta corrida?" v1.0.
- **Sucesor de aborto:** "Finalizar Proceso" (estado *error*).
- **Contratos consumidos:** iterador de sets ("Aplicar filtros" v1.1); `search_result` con `set_indice` ("Aplicar filtros" v1.1); `estado_captura` con `set_indice` ("Capturar ofertas" v1.1); `limite_alcanzado`.
- **Contratos entregados:** rama Sí → re-entrada de filtros con siguiente set; rama No → fuente terminada para la iteración de fuentes.
- **Impactos aprobados sobre nodos futuros:**
  1. La rama No retorna a la iteración de fuentes sin mutación adicional (RN-07).
  2. La reedición "Capturar ofertas" v1.1 (agregar `set_indice` a `estado_captura`) queda aprobada; su documento se entregará cuando se solicite.

### 1.13 Notas de implementación (para desarrollador o agente de IA)
- Especificación agnóstica de tecnología.
- Nodo de evaluación pura: sin I/O externo, sin escrituras, sin reintentos, sin mutación de estado (RN-01, RN-06).
- La política Grupo A/Grupo B (RN-03) vive únicamente en este nodo; los nodos productores solo emiten códigos de motivo sin clasificarlos.
- No avanzar ni reiniciar el iterador de sets en este nodo (RN-06).
- La validación de consistencia (RN-05) es defensiva ante bugs de nodos anteriores; no debe usarse para lógica de negocio.

---

## 2. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Validaciones | Posibles errores o excepciones |
|---|---|---|---|---|---|---|
| 1 | Leer insumos de la decisión del contexto | Contexto (iterador de sets, `search_result` del set corriente, `estado_captura`, `limite_alcanzado`, ids) | Acceder a insumos desde el contexto; no consultar la plataforma (RN-01) | Insumos de decisión | VAL-01 | ERR-01 |
| 2 | Validar consistencia de insumos | Insumos | Verificar iterador coherente con `source_id` y `search_result.set_indice` == set corriente (RN-05) | Insumos validados | VAL-02 | ERR-02 |
| 3 | Clasificar compromiso de la fuente | `search_result` (set corriente); `estado_captura` (si `set_indice` == set corriente) | fuente_comprometida = (búsqueda del set corriente en fallo con código Grupo A) o (captura del set corriente en fallo con código Grupo A) (RN-03, RN-04) | Bandera fuente_comprometida | — | Ninguna aplicable |
| 4 | Evaluar condición compuesta | Insumos validados; bandera | Condición Sí = quedan sets no procesados y `limite_alcanzado == false` y fuente_comprometida == false (RN-02); en caso contrario, No | Resultado booleano (Sí/No) | — | Ninguna aplicable |
| 5 | Rama Sí — Entregar control | Resultado = Sí; contexto | Cerrar el nodo y entregar control para el siguiente set | Flujo hacia "Aplicar los filtros básicos establecidos para esa fuente/plataforma…" | VAL-03 | Ninguna |
| 6 | Rama No — Entregar control | Resultado = No; contexto | Cerrar el nodo y entregar control para la iteración de fuentes (RN-07) | Flujo hacia "¿Quedan fuentes por procesar en esta corrida?" | — | Ninguna |

---

**Especificación Canónica — Nodo: "Finalizar Proceso" (terminal)**

## 1. Identificación del siguiente paso

Último nodo pendiente del Módulo 1: **"Finalizar Proceso"**, punto de convergencia de todas las terminaciones. Existe en el diagrama original; esta iteración lo especifica y oficializa los motivos/estados acumulados en iteraciones previas.

## 2. Análisis y justificación del nodo

**Por qué está en esta posición:** es el nodo terminal único; toda corrida termina aquí por cualquier camino (normal, controlado o error). Centraliza el cierre: registro de terminación, liberación del bloqueo y limpieza de recursos.

**Objetivo:** cerrar la corrida de forma determinista: persistir el evento de terminación con su motivo y estado, liberar el bloqueo de concurrencia si esta corrida lo posee, cerrar recursos abiertos y terminar el proceso.

**Entradas:**
- Contexto (best-effort): motivo/estado de terminación fijado por el nodo enrutador (`corrida_completada`, `sin_fuentes`, `concurrencia`, o `error` con su evento crítico ya escrito por el productor), `run_id`, iterador de fuentes (progreso), estado del bloqueo, handle de sesión abierto (si existe), conexiones de BD.

**Salidas:**
- Evento de terminación persistido en "errores o sucesos" (o registro crítico local si la escritura falla).
- Bloqueo liberado (si esta corrida lo poseía).
- Recursos cerrados.
- **Sin sucesor:** fin del proceso.

**Ramas:** no es nodo de decisión.

**Conjunto oficial de estados/motivos (formalización de lo aprobado en iteraciones previas):**

| Estado | Motivos | Tipo de evento |
|---|---|---|
| normal | `corrida_completada`, `sin_fuentes` | suceso |
| concurrencia | `concurrencia` | suceso |
| error | cualquier aborto (el evento crítico de la causa ya lo escribió el productor) | error |

**Decisiones de diseño (comparación y justificación):**

| Decisión | Alternativas | Recomendación y justificación |
|---|---|---|
| Contenido del evento de terminación | A. Minimal (run_id, timestamp, estado, motivo, fuentes_procesadas si disponible). B. Resumen completo de la corrida | **A.** El detalle ya existe en los eventos por nodo; duplicar resúmenes acopla y ensucia. |
| Liberación del bloqueo | A. Incondicional. B. Condicional a propiedad (lock owner == run_id) | **B.** En la ruta `concurrencia` esta corrida **no** posee el bloqueo; liberarlo incondicionalmente rompería el bloqueo de la corrida activa. |
| Fallo de liberación del bloqueo | A. Aborto/error fatal. B. Reintento único + registro local + continuar | **B.** Ya estamos terminando; el umbral de obsolescencia (ERR-07 de INICIO) auto-sana un bloqueo pegado en la próxima corrida. |
| Contexto corrupto al llegar | A. Aborto sin cierre. B. Cierre best-effort con motivo por defecto | **B.** El productor ya escribió el evento crítico; Finalizar debe intentar liberar bloqueo y cerrar recursos con lo que haya disponible. |
| Limpieza de recursos | A. Implícita por fin de proceso. B. Cierre explícito best-effort (canal de sesión, conexiones) | **B.** Un canal de navegador/API puede sobrevivir al proceso según implementación; el cierre explícito evita fugas. |

**Coherencia con decisiones previas:** liberación del bloqueo asignada a este nodo (impacto 2 de INICIO); registro de terminación en este nodo (patrón RN-05 de las decisiones); motivos `sin_fuentes`/`corrida_completada`/`concurrencia`/`error` ya aprobados; obsolescencia del bloqueo como respaldo.

**Impacto sobre nodos futuros:** ninguno (terminal). Con este nodo queda completo el conjunto de nodos del Módulo 1.

## 3. Especificación funcional

| Paso | Acción de la automatización | Entrada | Proceso | Salida | Posibles errores o excepciones |
|---|---|---|---|---|---|
| 1 | Leer estado de terminación y recursos (best-effort) | Contexto (motivo/estado, `run_id`, iterador, estado de bloqueo, handle de sesión, conexiones) | Leer con tolerancia: contexto ilegible/parcial → estado = error, motivo = `desconocido`, continuar con lo disponible; motivo fuera del conjunto oficial → normalizar a error/`desconocido` | Estado de terminación y recursos a cerrar | Contexto corrupto/ausente: no aborta (ya en terminación); continuar best-effort |
| 2 | Registrar evento de terminación en "errores o sucesos" | Estado, motivo, `run_id`, fuentes_procesadas (si disponible) | Escribir evento {run_id, timestamp, estado, tipo (suceso/error según estado), motivo, fuentes_procesadas}. Fallo: reintento único; si persiste, registro crítico local y continuar | Evento persistido o registro local | Fallo de escritura tras reintento: registro crítico local + continuación (no aborta) |
| 3 | Liberar bloqueo de concurrencia si corresponde | Estado del bloqueo; `run_id` | Si el bloqueo existe y su propietario == run_id: liberar. Fallo: reintento único; si persiste, registro crítico local y continuar (la obsolescencia lo sanea en la próxima corrida). Si no es propietario: sin acción | Bloqueo liberado o sin acción | Fallo de liberación tras reintento: registro crítico local + continuación |
| 4 | Cerrar recursos abiertos (best-effort) | Handle de sesión (si existe); conexiones de BD | Cerrar canal de sesión abierto y conexiones de BD; errores de cierre se registran localmente y no impiden la terminación | Recursos cerrados | Errores de cierre: registro local + continuación |
| 5 | Terminar el proceso | — | Cerrar el nodo; sin flujo de salida | Fin de la corrida | Ninguna |

## 4. Validación

Quedan sujetos a tu aprobación:
1. Conjunto oficial de estados/motivos y su tipo de evento (tabla).
2. Evento de terminación minimal con `fuentes_procesadas` opcional.
3. Liberación de bloqueo condicional a propiedad; fallo cubierto por obsolescencia.
4. Cierre best-effort ante contexto corrupto (sin aborto en terminación).
5. Cierre explícito de recursos (canal de sesión y conexiones).
6. La tabla de especificación tal como está.

Con este nodo queda completo el conjunto de nodos del Módulo 1 (pendiente solo la reedición "Capturar ofertas" v1.1 con `set_indice`, aprobada y a entregar si la solicitas). Espero tu aprobación o correcciones.
