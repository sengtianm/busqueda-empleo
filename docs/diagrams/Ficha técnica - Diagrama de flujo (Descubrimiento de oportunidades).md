# Especificación canónica densificada — Módulo 1: Descubrimiento de oportunidades

## Convenciones comunes

- **Alcance del módulo**: consultar fuentes configuradas, aplicar filtros básicos por `sets_de_filtros`, capturar y almacenar información original de ofertas según `politicas_de_captura`. No interpreta, clasifica, puntúa ni decide adecuación.
- **Contexto de ejecución**: única estructura/objeto transmitida a todos los nodos. Ningún nodo posterior reinicializa conexiones ni estado, salvo responsabilidad asignada.
- **Trazabilidad**: todo registro incluye `id_corrida`; cuando aplica, también `fuente_id`, `id_sesion` y `indice_set`.
- **Registro**: en `"errores o sucesos"` si está disponible; si no, registro crítico local (consola/archivo documentado). Todo evento incluye `id_corrida`, marca_temporal, tipo y descripción; los descartes/fallos por fuente incluyen `fuente_id`.
- **Aborto**: terminación inmediata en `"Finalizar Proceso"` con estado `error`.
- **Terminación controlada/normal**: cierre sin procesamiento o previsto; lo registra `"Finalizar Proceso"`.
- **Reintentos**: máximo global por defecto 2; backoff configurable. Solo son reintentables los códigos declarados en cada nodo. Credenciales, tokens y cookies nunca se registran, evidencian ni persisten.

---

## Nodo proceso: INICIO — Arranque de la corrida e inicialización del contexto de ejecución  
**Versión**: 1.3 (aprobada)

### Posición
Punto de entrada único del módulo; precede toda decisión y acción de negocio. El elemento punteado `"Descubrimiento de oportunidades"` es rótulo/disparador, no nodo ejecutable. Ninguna decisión posterior puede ejecutarse sin el contexto producido aquí.

### Objetivo
Instanciar la corrida y preparar el contexto de ejecución: trazabilidad, configuración validada y filtrada, conexiones, concurrencia y estado inicial.

### Descripción funcional
Al recibir disparador:
1. Crea instancia de corrida con `id_corrida` único y `fecha_inicio`.
2. Carga configuración y valida nivel global.
3. Verifica disponibilidad y permisos de escritura de las BD del módulo.
4. Valida concurrencia mediante bloqueo persistente.
5. Valida ficha por fuente y filtra la lista, descartando fuentes incompletas con evento crítico.
6. Inicializa estado: iterador sobre lista filtrada y contadores.
7. Entrega control al siguiente nodo.

Error fatal de inicialización o concurrencia activa producen terminación controlada en `"Finalizar Proceso"` antes de tocar cualquier fuente.

### Responsabilidad
- **Negocio**: arrancar corrida y verificar precondiciones operativas. No accede fuentes, no aplica filtros, no consulta ofertas, no valida existencia de fuentes.
- **Técnica**: `id_corrida`, conexiones, bloqueo de concurrencia, estado inicial.
- **Límite**: garantiza “ficha completa y consistente”; no garantiza ingreso ni captura exitosos. No accede al almacén seguro de credenciales ni a plataformas.

### Entradas
- Disparador manual o programado.
- Almacén de configuración: fuentes con ficha de acceso, `sets_de_filtros`, `politicas_de_captura`, parámetros globales —incluidos defaults de captura— y parámetros de conexión.
- Estado persistente de bloqueo, si existe.

### Salidas
- Contexto inicializado: `id_corrida`, fecha_inicio, lista filtrada de fuentes válidas —cada una con acceso, `sets_de_filtros` y políticas efectivas—, iterador en “ninguna fuente seleccionada aún”, contadores/variables, conexiones activas, bloqueo adquirido.
- Eventos de descarte por fuente incompleta, si aplica.
- Control normal al nodo siguiente.
- Terminación en `"Finalizar Proceso"` con estado `error` o `concurrencia`.

### Reglas de negocio
- **RN-01**: toda corrida tiene `id_corrida` único; todo registro del módulo queda enlazado a él.
- **RN-02**: solo una ejecución activa del módulo a la vez.
- **RN-03**: el iterador de fuentes se reinicia al inicio de cada corrida; formalizado en `"¿Quedan fuentes por procesar en esta corrida?"` v1.0.
- **RN-04**: este nodo no valida si existen fuentes configuradas; esa validación es del nodo siguiente.
- **RN-05**: este nodo no accede fuentes ni ejecuta búsquedas.
- **RN-06**: todo error fatal de inicialización termina la corrida antes de cualquier procesamiento.
- **RN-07**: identificadores de fuente únicos por configuración; validados aquí y sostienen la trazabilidad por `fuente_id` de nodos posteriores.
- **RN-08**: toda fuente debe tener ficha completa y consistente:
  - esquema de acceso: URL/plataforma, tipo `publico|con_autenticacion`, referencia de credenciales si `con_autenticacion`, criterio verificable de ingreso exitoso, timeout;
  - `sets_de_filtros`: lista no vacía; cada set es lista de filtros, posiblemente vacía = búsqueda base;
  - `politicas_de_captura` consistente si presente.  
  Fuente incompleta/inconsistente se descarta con evento crítico; la corrida continúa con las válidas.
- **RN-09**: este nodo no ejecuta validaciones runtime: resolución de credenciales, validez de credenciales, alcanzabilidad, criterios de éxito y aplicabilidad de filtros pertenecen a `"Entrar a la fuente seleccionada"`.
- **RN-10**: el mecanismo de captura (masivo vs incremental) es del adaptador de plataforma; la configuración solo lo acota vía `politicas_de_captura`. Justificación: el mecanismo depende de la plataforma; configurarlo generaría inconsistencias fuente-adaptador.
- **RN-11**: `politicas_de_captura` ausente o parcial → defaults globales; si presente, validar rangos y tipos.

### Validaciones
- **VAL-01**: `id_corrida` único y no nulo.
- **VAL-02**: configuración global: almacén existente/legible, estructura consistente, identificadores de fuente únicos. No valida completitud por fuente ni lista vacía.
- **VAL-03**: BD: conexiones abiertas y prueba de escritura exitosa con rollback.
- **VAL-04**: bloqueo legible; obsolescencia por marca_temporal contra umbral configurable; marcas temporales coherentes.
- **VAL-05**: contexto completo antes de entregar control.
- **VAL-06**: ficha por fuente completa/consistente; incumplimientos se descartan sin abortar.

### Condiciones
- **Continuación normal**: configuración global válida + BD disponibles + sin concurrencia activa. Descartes ERR-12 no impiden continuar.
- **Terminación**: configuración ausente/ilegible/corrupta; IDs duplicados; BD indisponible/bloqueada/sin permisos; concurrencia activa; estado de bloqueo no decidible.
- **Descarte por fuente**: no termina la corrida; emite evento crítico y filtra la lista. Si no quedan fuentes, el nodo siguiente resuelve `sin_fuentes`.

### Ramas
- **Normal** → `"¿Existe al menos una fuente/plataforma de empleo configurada?"`.
- **Excepción** → `"Finalizar Proceso"` con estado `error` o `concurrencia`.

### Errores y excepciones

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | Colisión o fallo de generación de `id_corrida` | 1 | Registro crítico local | Reintento único; si persiste, aborto | `error` |
| ERR-02 | Configuración ausente | 2 | Registro crítico local | Aborto | `error` |
| ERR-03 | Configuración ilegible | 2 | Registro crítico local | Aborto | `error` |
| ERR-04 | Configuración corrupta / estructura global inconsistente | 2 | Registro crítico local | Aborto | `error` |
| ERR-05 | BD indisponible / bloqueada / sin permisos | 3 | Evento crítico en `"errores o sucesos"` si accesible; si no, local | Aborto | `error` |
| ERR-06 | Concurrencia activa | 4 | Evento “finalización por concurrencia” | Terminación controlada | `concurrencia` |
| ERR-07 | Bloqueo obsoleto (antigüedad > umbral) | 4 | Suceso de sobrescritura | Sobrescribir bloqueo y continuar | continúa |
| ERR-08 | Estado de bloqueo no decidible | 4 | Evento crítico | Aborto | `error` |
| ERR-09 | Contienda de adquisición de bloqueo | 4 | — | Atomicidad/unicidad; perdedor cae en ERR-06 | `concurrencia` |
| ERR-10 | Falla interna de inicialización de estado | 6 | Evento crítico en `"errores o sucesos"` | Aborto | `error` |
| ERR-11 | IDs de fuente duplicados | 2 | Registro crítico local | Aborto | `error` |
| ERR-12 | Ficha por fuente incompleta/inconsistente | 5 | Evento crítico con `id_corrida` + `fuente_id` | Descartar fuente y continuar | continúa |

### Dependencias y contratos
- **Antecesor**: ninguno.
- **Sucesor normal**: `"¿Existe al menos una fuente/plataforma de empleo configurada?"`.
- **Sucesor de excepción**: `"Finalizar Proceso"`.
- **Contrato entregado**: contexto completo como única interfaz; lista contiene solo fuentes estructuralmente válidas, con `sets_de_filtros` y políticas resueltas.
- **Impactos aprobados**:
  - `id_corrida` se registra en BD del módulo.
  - `"Finalizar Proceso"` libera el bloqueo.
  - RN-03 formalizada en `"¿Quedan fuentes por procesar…?"` v1.0.
  - RN-07 sostiene trazabilidad por `fuente_id` en `"Seleccionar la siguiente fuente pendiente"`.
  - `"Entrar a la fuente seleccionada"` asume ficha completa y posee validaciones runtime.
  - `"Aplicar filtros básicos"` v1.1 itera `sets_de_filtros`; el iterador de sets se reinicia al cambiar de fuente.
  - `"Capturar ofertas"` consume políticas efectivas; el adaptador define mecanismo de captura.

### Notas de implementación
- Agnóstico de tecnología.
- Contexto como única estructura/objeto.
- Bloqueo persistente con `id_corrida` y marca_temporal; umbral de obsolescencia configurable.
- Registro crítico local documentado.
- Prueba de escritura con rollback.
- Orden obligatorio: configuración antes que BD; validación por fuente después de BD y bloqueo para persistir descartes y evitar trabajo concurrente.
- No acceder al almacén seguro ni a plataformas; referencia de credenciales solo se valida como campo presente y consistente.
- `politicas_de_captura`: resolver defaults en carga y exponer valores efectivos; rangos: `max_paginas` ≥ 1, `max_ofertas_por_corrida` ≥ 1, `pausa_entre_lotes` ≥ 0; `estrategia_anti_bloqueo` dentro del conjunto definido.
- `sets_de_filtros`: preservar orden; set vacío = búsqueda base.
- No implementar lógica de negocio ni validación de existencia de fuentes.

### Pasos funcionales
1. **Recibir disparador e instanciar corrida**. Entrada: evento manual/programado. Proceso: crear instancia, generar `id_corrida`, fecha_inicio. Salida: instancia. Val: VAL-01. Err: ERR-01.
2. **Cargar configuración y validar nivel global**. Entrada: almacén de configuración. Proceso: leer; validar legibilidad, estructura, unicidad de IDs. No valida completitud por fuente ni lista vacía. Salida: configuración cruda en contexto. Val: VAL-02. Err: ERR-02, ERR-03, ERR-04, ERR-11.
3. **Verificar BD**. Entrada: parámetros de conexión de `"Ofertas Totales"`, `"errores o sucesos"`, `"control de sesiones"` y demás. Proceso: abrir conexiones; prueba de escritura con rollback. Salida: conexiones disponibles. Val: VAL-03. Err: ERR-05.
4. **Validar concurrencia**. Entrada: `id_corrida`, estado de bloqueo, umbral. Proceso: leer bloqueo; activo no obsoleto → terminación controlada; obsoleto → sobrescribir y continuar; inexistente → marcar bloqueo. Salida: bloqueo adquirido o terminación. Val: VAL-04. Err: ERR-06, ERR-07, ERR-08, ERR-09.
5. **Validar fichas y filtrar lista**. Entrada: configuración cruda. Proceso: por fuente, validar ficha; resolver políticas efectivas; fuente válida → conservar; inválida → evento crítico y descarte. Salida: lista filtrada con políticas efectivas; eventos. Val: VAL-06. Err: ERR-12.
6. **Inicializar estado**. Entrada: `id_corrida`, lista filtrada. Proceso: fijar iterador en “ninguna fuente seleccionada aún”; inicializar contadores. Salida: contexto completo. Val: iterador/contadores iniciales. Err: ERR-10.
7. **Entregar control**. Entrada: contexto completo. Proceso: cerrar nodo. Salida: flujo a `"¿Existe al menos una fuente/plataforma de empleo configurada?"`. Val: VAL-05. Err: contexto incompleto → ERR-10.

---

## Nodo decisión: “¿Existe al menos una fuente/plataforma de empleo configurada?”  
**Versión**: 1.0 (aprobada)

### Posición
Primera decisión de negocio, inmediatamente después de INICIO. Posición definitiva.

### Objetivo
Decidir si la corrida continúa o termina controladamente según exista al menos una fuente configurada.

### Descripción funcional
Lee la lista de fuentes del contexto en memoria, sin releer almacén. Si hay ≥ 1 fuente, entrega control al nodo siguiente con contrato “lista no vacía”. Si hay 0, fija motivo `sin_fuentes` —suceso, no error— y entrega control a `"Finalizar Proceso"`. No realiza I/O, no accede fuentes, no revalida estructura.

### Entradas
Contexto de INICIO: lista de fuentes, `id_corrida`, conexiones activas, bloqueo adquirido.

### Salidas
- **Sí** → `"¿Es la primera ejecución del ciclo?"` con lista no vacía.
- **No** → `"Finalizar Proceso"` con motivo `sin_fuentes`.
- **Falla interna** → `"Finalizar Proceso"` con estado `error`.

### Reglas de negocio
- **RN-01**: evaluar solo contexto; prohibido releer almacén.
- **RN-02**: “fuente configurada” = presente en configuración cargada; no hay estados habilitada/deshabilitada.
- **RN-03**: no revalidar estructura; ya lo hizo INICIO.
- **RN-04**: ausencia de fuentes es configuración válida; rama No = terminación controlada `sin_fuentes`, tipo suceso.
- **RN-05**: este nodo no registra; `"Finalizar Proceso"` registra la terminación.
- **RN-06**: rama Sí garantiza lista no vacía; ningún nodo posterior revalida existencia.

### Validaciones
- **VAL-01**: lista de fuentes accesible en contexto.
- **VAL-02**: evaluación sobre lista leída; conteo entero ≥ 0; sin revalidación.
- **VAL-03**: rama Sí solo con conteo > 0.
- **VAL-04**: en rama No, `sin_fuentes` fijado con `id_corrida` y marca_temporal antes de entregar control.

### Condiciones y ramas
- **Sí**: conteo > 0 → `"¿Es la primera ejecución del ciclo?"`.
- **No**: conteo == 0 → `"Finalizar Proceso"` con `sin_fuentes`.
- **Aborto**: contexto sin configuración/incompleto → `"Finalizar Proceso"` con `error`.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | Contexto sin configuración o incompleto | 1 | Evento crítico en `"errores o sucesos"` | Aborto | `error` |

### Dependencias y contratos
- **Antecesor**: INICIO.
- **Sucesor Sí**: `"¿Es la primera ejecución del ciclo?"`; pendiente redefinición según RN-03 de INICIO; la salida Sí no cambia.
- **Sucesor No**: `"Finalizar Proceso"` con `sin_fuentes`.
- **Impactos aprobados**: ningún nodo posterior revalida existencia; `"Finalizar Proceso"` incorpora `sin_fuentes`.

### Notas de implementación
- Nodo de evaluación pura: sin I/O, sin red, sin escritura, salvo fijar motivo en rama No.
- No implementar revalidación estructural ni estados de fuente.
- Leer la lista del mismo objeto de contexto; no copiar ni transformar.

### Pasos funcionales
1. **Leer lista del contexto**. Entrada: contexto. Proceso: acceder a lista; no releer almacén. Salida: lista posiblemente vacía. Val: VAL-01. Err: ERR-01.
2. **Evaluar existencia**. Entrada: lista. Proceso: contar; condición = conteo > 0. Salida: Sí/No. Val: VAL-02. Err: ninguna.
3. **Rama Sí**. Entrada: resultado Sí. Proceso: entregar control. Salida: flujo a `"¿Es la primera ejecución del ciclo?"`. Val: VAL-03. Err: ninguna.
4. **Rama No**. Entrada: resultado No, `id_corrida`. Proceso: fijar `sin_fuentes` y entregar control. Salida: flujo a `"Finalizar Proceso"`. Val: VAL-04. Err: ninguna.

---

## Nodo decisión: “¿Quedan fuentes por procesar en esta corrida?”  
**Versión**: 1.0 (aprobada)

### Posición
Punto único de control del bucle de fuentes. Recibe:
- rama Sí de `"¿Existe al menos una fuente/plataforma de empleo configurada?"`;
- retorno desde registro de ingreso fallido;
- retorno desde registro de búsqueda sin ofertas;
- rama No de `"¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"`.

### Objetivo
Determinar si quedan fuentes pendientes. Sí → selección de fuente. No → terminación normal `corrida_completada`.

### Descripción funcional
Lee lista e iterador del contexto. Calcula pendientes = fuentes no marcadas procesadas, en orden de configuración. No avanza iterador ni marca fuentes; eso pertenece a `"Seleccionar la siguiente fuente pendiente"`.

### Entradas
Contexto: lista de fuentes no vacía, iterador, `id_corrida`.

### Salidas
- **Sí** → `"Seleccionar la siguiente fuente pendiente"` con contrato de siguiente pendiente.
- **No** → `"Finalizar Proceso"` con `corrida_completada`.
- **Falla interna** → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: solo contexto; prohibido releer almacén.
- **RN-02**: pendiente = no marcada como procesada; orden de configuración.
- **RN-03**: fuente fallida se considera procesada; no se reselecta. Reintentos internos de `"Entrar a la fuente seleccionada"` ocurren dentro de una pasada y no alteran el iterador.
- **RN-04**: este nodo no avanza ni marca; evaluación pura.
- **RN-05**: rama No = terminación normal `corrida_completada`, tipo suceso; registra `"Finalizar Proceso"`.
- **RN-06**: rama Sí garantiza siguiente fuente pendiente en orden.

### Validaciones
- **VAL-01**: iterador y lista accesibles y coherentes.
- **VAL-02**: cálculo solo sobre datos leídos; conteo ≥ 0; orden respetado.
- **VAL-03**: Sí solo con pendientes > 0.
- **VAL-04**: en No, `corrida_completada` fijado con `id_corrida` y marca_temporal.

### Condiciones y ramas
- **Sí**: pendientes > 0 → `"Seleccionar la siguiente fuente pendiente"`.
- **No**: pendientes == 0 → `"Finalizar Proceso"` con `corrida_completada`.
- **Aborto**: iterador ausente/corrupto → `"Finalizar Proceso"` con `error`.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | Iterador ausente o corrupto | 1 | Evento crítico en `"errores o sucesos"` | Aborto | `error` |

### Dependencias y contratos
- **Antecesores**: rama Sí de existencia y tres retornos del bucle.
- **Sucesor Sí**: `"Seleccionar la siguiente fuente pendiente"`.
- **Sucesor No**: `"Finalizar Proceso"`.
- **Impactos aprobados**:
  - `"Seleccionar la siguiente fuente pendiente"` es único responsable de avanzar/marcar.
  - `"Finalizar Proceso"` incorpora `corrida_completada`.
  - Nodos de procesamiento asumen fuente corriente válida.

### Notas de implementación
- Evaluación pura; sin I/O, sin mutación de iterador.
- Iterador como estado de corrida en contexto; reiniciado por corrida; progreso de procesadas; orden de configuración.
- No reintentar ni reevaluar fuentes fallidas.

### Pasos funcionales
1. **Leer estado de iteración**. Entrada: contexto. Proceso: acceder a lista e iterador. Salida: datos de iteración. Val: VAL-01. Err: ERR-01.
2. **Calcular pendientes**. Entrada: lista, iterador. Proceso: pendientes = no procesadas en orden; condición = conteo > 0. Salida: Sí/No. Val: VAL-02. Err: ninguna.
3. **Rama Sí**. Entrada: resultado Sí. Proceso: entregar control. Salida: flujo a `"Seleccionar la siguiente fuente pendiente"`. Val: VAL-03. Err: ninguna.
4. **Rama No**. Entrada: resultado No, `id_corrida`. Proceso: fijar `corrida_completada` y entregar control. Salida: flujo a `"Finalizar Proceso"`. Val: VAL-04. Err: ninguna.

---

## Nodo proceso: “Seleccionar la siguiente fuente pendiente”  
**Versión**: 1.0 (aprobada)

### Posición
Entre rama Sí de `"¿Quedan fuentes por procesar en esta corrida?"` y `"Entrar a la fuente seleccionada"`.

### Objetivo
Avanzar el iterador, marcar como procesada la fuente seleccionada y exponer la fuente corriente con sus parámetros.

### Descripción funcional
Identifica la primera entrada no procesada en orden de configuración, la marca como procesada en el momento de selección, la fija como fuente corriente con `fuente_id`, posición, acceso y filtros básicos, y entrega control.

### Entradas
Contexto con contrato Sí: lista, iterador, `id_corrida`, existencia de fuente pendiente.

### Salidas
- Contexto actualizado: iterador avanzado; fuente marcada procesada; fuente corriente definida.
- Control a `"Entrar a la fuente seleccionada"` con contrato “fuente corriente válida”.
- Falla interna → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: solo contexto; prohibido releer almacén.
- **RN-02**: selección = primera entrada no procesada en orden de configuración; clave = posición.
- **RN-03**: marcar procesada al seleccionar garantiza progreso ante fallas posteriores.
- **RN-04**: único nodo que avanza iterador y marca fuentes.
- **RN-05**: fuente corriente expone todos los parámetros requeridos: acceso y filtros básicos.
- **RN-06**: `fuente_id` + `id_corrida` deben incluirse en todo registro posterior.
- **RN-07**: no revalida estructura; responsabilidad de INICIO.

### Validaciones
- **VAL-01**: lista e iterador accesibles/coherentes.
- **VAL-02**: posición seleccionada no procesada y dentro de rango.
- **VAL-03**: tras mutación, iterador refleja procesada y fuente corriente tiene `fuente_id` y parámetros completos.

### Condiciones
- **Normal**: contrato Sí cumplido → selección, mutación y control.
- **Aborto**: iterador ausente/corrupto; ausencia de pendiente pese a contrato; falla al mutar contexto.

### Ramas
- Salida normal única → `"Entrar a la fuente seleccionada"`.
- Aborto → `"Finalizar Proceso"` con `error`.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | Iterador ausente o corrupto | 1 | Evento crítico en `"errores o sucesos"` | Aborto | `error` |
| ERR-02 | Ausencia de fuente pendiente pese a contrato Sí | 2 | Evento crítico en `"errores o sucesos"` | Aborto | `error` |
| ERR-03 | Falla interna al mutar contexto | 3 | Evento crítico en `"errores o sucesos"` | Aborto | `error` |

### Dependencias y contratos
- **Antecesor**: `"¿Quedan fuentes por procesar…?"` rama Sí.
- **Sucesor**: `"Entrar a la fuente seleccionada"`.
- **Contrato consumido**: existe siguiente fuente pendiente.
- **Contrato entregado**: fuente corriente válida; ningún nodo posterior reselecta fuente.
- **Impactos aprobados**:
  - Bloque de procesamiento consume fuente corriente.
  - Filtros básicos se consumen en `"Aplicar filtros básicos"`.
  - Registros incorporan `fuente_id`.

### Notas de implementación
- Mutación atómica: marcar procesada + fijar fuente corriente.
- Iteración por posición; `fuente_id` solo trazabilidad.
- Sin red, sin ingreso, sin búsquedas.
- Sin revalidación estructural.

### Pasos funcionales
1. **Leer estado de selección**. Entrada: contexto. Proceso: acceder a lista e iterador. Salida: datos de selección. Val: VAL-01. Err: ERR-01.
2. **Determinar siguiente pendiente**. Entrada: lista, iterador. Proceso: primera entrada no procesada en orden. Salida: posición y `fuente_id`. Val: VAL-02. Err: ERR-02.
3. **Mutar contexto**. Entrada: posición y `fuente_id`. Proceso: marcar procesada; fijar fuente corriente con parámetros. Salida: contexto actualizado. Val: VAL-03. Err: ERR-03.
4. **Entregar control**. Entrada: contexto actualizado. Proceso: cerrar nodo. Salida: flujo a `"Entrar a la fuente seleccionada"` con trazabilidad. Val: contexto completo. Err: ninguna.

---

## Nodo proceso: “Entrar a la fuente seleccionada”  
**Versión**: 1.1 (aprobada)

### Posición
Entre `"Seleccionar la siguiente fuente pendiente"` y `"¿El ingreso fue exitoso?"`. Primer nodo que toca plataformas externas. Posición definitiva.

### Objetivo
Intentar acceso/ingreso a la plataforma de la fuente corriente según ficha de acceso, con reintentos condicionales, autenticar si corresponde, y producir:
- `entry_result` estructurado;
- sesión activa solo en éxito.

### Descripción funcional
Lee ficha de acceso del contexto. Si `con_autenticacion`, resuelve credenciales del almacén seguro. Abre canal y accede dentro del timeout. Autentica si aplica. Evalúa criterio verificable de éxito.

Ciclo de intento:
- códigos reintentables: `fuente_inalcanzable`, `tiempo_agotado_ingreso`;
- con intentos restantes: cerrar canal, backoff y reintentar desde acceso;
- código no reintentable o intentos agotados: evidencia de fallo.

Construye:
```text
entry_result = {
  estado: exito|fallo,
  codigo_motivo,
  evidencia_acotada,
  numero_de_intentos
}
```
En éxito crea `id_sesion` único y guarda handle + `id_sesion`. En fallo cierra canal y garantiza ausencia de sesión. Entrega control a `"¿El ingreso fue exitoso?"`.

### Entradas
- Contexto: fuente corriente con ficha completa: `fuente_id`, URL/plataforma, tipo `publico|con_autenticacion`, referencia de credenciales, criterio de éxito, filtros básicos, timeout; `id_corrida`.
- Parámetros globales de reintento/backoff; máximo por defecto 2.
- Almacén seguro de credenciales, accedido exclusivamente por este nodo.

### Salidas
- `entry_result` en contexto, sin datos sensibles.
- En éxito: sesión activa (`id_sesion` + handle).
- En fallo: canal cerrado, sin sesión.
- Control único a `"¿El ingreso fue exitoso?"`.
- Aborto → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: opera sobre contexto; no relee almacén ni revalida ficha.
- **RN-02**: almacén seguro accedido solo aquí; credenciales/tokens nunca se registran ni persisten fuera de memoria.
- **RN-03**: reintentos condicionales hasta N configurables (default 2), con backoff, solo para `fuente_inalcanzable` y `tiempo_agotado_ingreso`. Cada reintento cierra canal previo y reejecuta desde acceso. No reintentables: `credenciales_no_disponibles`, `autenticacion_rechazada`, `bloqueo_plataforma`, `criterio_no_cumplido`, `error_interno_fuente`.
- **RN-04**: toda falla de intento produce evidencia de fallo; la fuente se omite aguas abajo. Aborto solo por violación de contrato/contexto.
- **RN-05**: `id_sesion` solo en éxito; en fallo canal cerrado y sin sesión.
- **RN-06**: evidencia acotada y sin datos sensibles.
- **RN-07**: eventos incluyen `id_corrida` y `fuente_id`.
- **RN-08**: no aplica filtros, no captura ofertas, no interpreta contenido.

### Validaciones
- **VAL-01**: ficha accesible en contexto.
- **VAL-02**: si `con_autenticacion`, credenciales resueltas y no vacías antes de abrir canal.
- **VAL-03**: acceso/autenticación acotados por timeout.
- **VAL-04**: `entry_result` estructurado completo.
- **VAL-05**: éxito → sesión con `id_sesion` y handle; fallo → canal cerrado y sin sesión.
- **VAL-06**: reintentos ≤ máximo; backoff; solo códigos reintentables; cada reintento desde canal cerrado.

### Condiciones
- **Normal**: `entry_result` construido → decisión.
- **Reintento**: código reintentable con intentos restantes.
- **Fallo de fuente**: no aborto; `entry_result` fallo.
- **Aborto**: ficha ausente/corrupta; corrupción de contexto.

### Ramas
- Normal única → `"¿El ingreso fue exitoso?"`.
- Aborto → `"Finalizar Proceso"` con `error`.
- Flujo interno con salida temprana a construcción de `entry_result`.

### Errores y excepciones

| Código | Error / excepción | Reintentable | Detección | Registro / acción | Estado |
|---|---|:---:|---:|---|---|
| ERR-01 | Ficha ausente o corrupta en contexto | No | 1 | Evento crítico; aborto | `error` |
| ERR-02 | `credenciales_no_disponibles`: referencia no resoluble o vacías | No | 2 | Evidencia de fallo; no abrir canal; salto a `entry_result` | fallo de fuente |
| ERR-03 | `fuente_inalcanzable`: red/DNS/plataforma caída | Sí | 3 | Con intentos: cerrar canal, backoff, reintentar; agotados: evidencia de fallo | fallo de fuente |
| ERR-04 | `tiempo_agotado_ingreso` | Sí | 3/4 | Ídem ERR-03 | fallo de fuente |
| ERR-05 | `autenticacion_rechazada` | No | 4 | Evidencia de fallo | fallo de fuente |
| ERR-06 | `bloqueo_plataforma`: captcha/anti-bot/desafío | No | 4 | Evidencia de fallo | fallo de fuente |
| ERR-07 | `criterio_no_cumplido` | No | 5 | Evidencia de fallo | fallo de fuente |
| ERR-08 | `error_interno_fuente` | No | 3–5 | Evidencia de fallo; cerrar canal si quedó abierto | fallo de fuente |
| ERR-09 | Corrupción del contexto | No | 5 | Evento crítico; aborto | `error` |

**Contrato de códigos**: `ingreso_exitoso`, `credenciales_no_disponibles`, `fuente_inalcanzable`, `tiempo_agotado_ingreso`, `autenticacion_rechazada`, `bloqueo_plataforma`, `criterio_no_cumplido`, `error_interno_fuente`.

### Escenarios límite
- Fuente `publico`: pasos de credenciales/autenticación sin efecto.
- Almacén seguro caído con fuente autenticada: ERR-02, sin reintento.
- Cambio de layout: ERR-07.
- Caída transitoria o lentitud: ERR-03/ERR-04 con reintento acotado.
- Canal parcialmente abierto: cierre garantizado en todo camino.
- Credenciales nunca expuestas en evidencia o registros.

### Dependencias y contratos
- **Antecesor**: `"Seleccionar la siguiente fuente pendiente"`.
- **Sucesor normal**: `"¿El ingreso fue exitoso?"`.
- **Sucesor de aborto**: `"Finalizar Proceso"`.
- **Contratos consumidos**: ficha completa; trazabilidad; parámetros de reintento/backoff.
- **Contratos entregados**: `entry_result`; sesión solo en éxito.
- **Impactos aprobados**:
  - decisión siguiente evalúa solo `entry_result`;
  - registro de fallo consume código, intentos y evidencia;
  - `id_sesion` alimenta `"control de sesiones"` y registros de ofertas;
  - filtros se consumen en nodo de filtros.

### Notas de implementación
- Canal puede ser navegador o API; contrato funcional idéntico.
- Intentos totales = 1 + máx. reintentos.
- Cada reintento parte de canal cerrado y reejecuta acceso.
- Nunca reintentar códigos no reintentables.
- Garantizar cierre de canal en todo fallo.
- Timeout por fuente con default global.
- Evidencia sin credenciales/tokens/cookies.
- `id_sesion` único y vinculado a `id_corrida` y `fuente_id`.

### Pasos funcionales
1. **Leer ficha**. Entrada: contexto. Proceso: acceder a URL, tipo, referencia, criterio, timeout. Salida: parámetros de acceso. Val: VAL-01. Err: ERR-01.
2. **Resolver credenciales si aplica**. Entrada: tipo/referencia/almacén seguro. Proceso: si `con_autenticacion`, obtener y verificar no vacías; si fallo, salto a `entry_result`; si `publico`, sin efecto. Salida: credenciales en memoria o N/A. Val: VAL-02. Err: ERR-02.
3. **Abrir canal y acceder**. Entrada: parámetros, timeout, reintentos. Proceso: abrir canal y acceder; fallo reintentable → cerrar, backoff, repetir; fallo no reintentable/agotado → salto a `entry_result`. Salida: canal abierto. Val: VAL-03, VAL-06. Err: ERR-03, ERR-04, ERR-08.
4. **Autenticar si aplica**. Entrada: canal, credenciales. Proceso: autenticar dentro de timeout; `tiempo_agotado_ingreso` reintentable → reejecutar desde paso 3; `autenticacion_rechazada`/`bloqueo_plataforma` → fallo; `publico` sin efecto. Salida: estado post-autenticación. Val: VAL-03, VAL-06. Err: ERR-04, ERR-05, ERR-06, ERR-08.
5. **Evaluar criterio y construir `entry_result`**. Entrada: estado del canal, criterio, contador. Proceso: aplicar criterio; construir `entry_result`; éxito → `id_sesion` + handle; fallo → cerrar canal sin sesión. Salida: `entry_result`; sesión lista o ausente. Val: VAL-04, VAL-05. Err: ERR-07, ERR-08, ERR-09.
6. **Entregar control**. Entrada: contexto con `entry_result`. Proceso: cerrar nodo. Salida: flujo a `"¿El ingreso fue exitoso?"`. Val: `entry_result` presente. Err: ninguna.

---

## Nodo decisión: “¿El ingreso fue exitoso?”  
**Versión**: 1.0 (aprobada)

### Posición
Entre `"Entrar a la fuente seleccionada"` v1.1 y el bloque de procesamiento. Sí → `"Aplicar los filtros básicos…"`. No → `"Registrar error o suceso en 'errores o sucesos'"`.

### Objetivo
Evaluar `entry_result` y bifurcar: procesar fuente con sesión activa o derivar fallo a registro.

### Descripción funcional
Lee `entry_result`, valida estructura y, si éxito, presencia de sesión. Evalúa `estado == exito`. Es decisión pura: no sondea plataforma, no registra. Inconsistencia de contrato aborta.

### Entradas
Contexto: `entry_result`, sesión si éxito, `id_corrida`, `fuente_id`.

### Salidas
- **Sí** → `"Aplicar los filtros básicos…"` con sesión activa disponible.
- **No** → `"Registrar error o suceso en 'errores o sucesos'"` con `entry_result` como carga.
- **Aborto** → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: evaluación pura sobre `entry_result`; prohibido sondear plataforma/sesión.
- **RN-02**: condición = `entry_result.estado == exito`.
- **RN-03**: validar consistencia: estructura completa y, si éxito, sesión presente. Violación = aborto visible.
- **RN-04**: este nodo no registra; el registro del fallo pertenece a la rama No.
- **RN-05**: contratos: Sí garantiza sesión; No garantiza `entry_result` disponible.

### Validaciones
- **VAL-01**: `entry_result` presente.
- **VAL-02**: estructura completa: estado, `codigo_motivo`, evidencia, `numero_de_intentos`.
- **VAL-03**: si éxito, sesión presente con handle y `id_sesion`.

### Condiciones y ramas
- **Sí**: estado = `exito` y consistencia validada.
- **No**: estado = `fallo` y consistencia validada.
- **Aborto**: `entry_result` ausente/corrupto o estructura inválida/éxito sin sesión.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | `entry_result` ausente o corrupto | 1 | Evento crítico con `id_corrida` + `fuente_id` | Aborto | `error` |
| ERR-02 | Estructura inválida o éxito sin sesión | 2 | Evento crítico con `id_corrida` + `fuente_id` | Aborto | `error` |

### Dependencias y contratos
- **Antecesor**: `"Entrar a la fuente seleccionada"` v1.1.
- **Sucesor Sí**: `"Aplicar los filtros básicos…"`.
- **Sucesor No**: `"Registrar error o suceso en 'errores o sucesos'"`.
- **Impactos aprobados**:
  - registro consume `entry_result` completo;
  - nodo de filtros consume sesión sin revalidarla.

### Notas de implementación
- Evaluación pura; sin I/O externo salvo evento crítico de aborto.
- No ramificar por `codigo_motivo`; solo por estado.
- No registrar fallo aquí.

### Pasos funcionales
1. **Leer `entry_result`**. Entrada: contexto. Proceso: acceder sin sondear. Salida: `entry_result`. Val: VAL-01. Err: ERR-01.
2. **Validar consistencia**. Entrada: `entry_result`. Proceso: verificar estructura; si éxito, sesión. Salida: validado. Val: VAL-02, VAL-03. Err: ERR-02.
3. **Evaluar**. Entrada: validado. Proceso: `estado == exito`. Salida: Sí/No. Err: ninguna.
4. **Rama Sí**. Entrada: Sí, sesión. Proceso: entregar control. Salida: flujo a filtros. Val: VAL-03. Err: ninguna.
5. **Rama No**. Entrada: No, `entry_result`. Proceso: entregar control sin registrar. Salida: flujo a registro. Err: ninguna.

---

## Nodo proceso: “Aplicar los filtros básicos establecidos para esa fuente/plataforma para encontrar ofertas laborales”  
**Versión**: 1.1 (aprobada)

### Posición
Entre:
- rama Sí de `"¿El ingreso fue exitoso?"` en primera pasada;
- rama Sí de `"¿Quedan sets de filtros por aplicar en esta fuente?"` en pasadas siguientes.

Sucesor: `"¿Se encontraron ofertas?"`. Nodo re-entrante por set.

### Objetivo
Seleccionar el siguiente set pendiente, ejecutar la búsqueda con ese set dentro de la sesión, interpretar la respuesta y producir `search_result` con primera página de referencias, paginación, metadatos y `indice_set`.

### Descripción funcional
Lee sesión, `sets_de_filtros` e iterador de sets. Si cambió la fuente, reinicia iterador a “ninguno”. Selecciona primer set no procesado en orden de configuración, lo marca procesado al seleccionarlo y lo fija como `set_corriente`. Aplica filtros mediante adaptador, ejecuta consulta con timeout y reintentos condicionales, interpreta respuesta cruda y produce:
```text
search_result = {
  estado: exito|fallo,
  codigo_motivo,
  evidencia_acotada,
  ofertas_primera_pagina: [referencias],
  estado_paginacion,
  total_declarado | indeterminado,
  indice_set,
  numero_de_intentos
}
```
Entrega control a `"¿Se encontraron ofertas?"`.

### Límites
No decide si hay ofertas; no decide si quedan sets; no captura información completa; no interpreta contenido; no recorre páginas posteriores.

### Entradas
- Sesión activa: `id_sesion` + handle.
- `sets_de_filtros` de fuente corriente: lista no vacía, ordenada; cada set posiblemente vacío.
- Iterador de sets.
- `fuente_id`, `id_corrida`, `id_sesion`.
- Timeout de consulta, máx. reintentos, backoff.

### Salidas
- `set_corriente` fijado e iterador avanzado.
- `search_result` en contexto.
- Control único a `"¿Se encontraron ofertas?"`.
- Aborto → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: solo contexto; no releer almacén.
- **RN-02**: aplicar únicamente filtros del `set_corriente`; adaptador los mapea al mecanismo de la plataforma.
- **RN-03**: set vacío = búsqueda base; configuración válida.
- **RN-04**: filtros configurados pero no aplicables en runtime = fallo `filtros_no_aplicables`; prohibido continuar sin filtros. Falla descarta el set, no la fuente.
- **RN-05**: alcance perezoso: primera página y estado de paginación; páginas posteriores pertenecen al bucle de captura.
- **RN-06**: reintentos solo para `fuente_inalcanzable` y `tiempo_agotado_consulta`; resto fallo inmediato.
- **RN-07**: sesión expirada = `sesion_expirada`; sin re-ingreso automático.
- **RN-08**: produce referencias de oferta (identificador/URL en orden de plataforma); no captura contenido ni interpreta.
- **RN-09**: evidencia acotada; trazabilidad `id_corrida` + `fuente_id` + `id_sesion` + `indice_set`.
- **RN-10**: iterador de sets propiedad de este nodo: se reinicia al cambiar fuente; selecciona primer set pendiente y lo marca procesado al seleccionar.
- **RN-11**: no decide si quedan sets; eso pertenece a `"¿Quedan sets de filtros…?"`.

### Validaciones
- **VAL-01**: sesión, sets e iterador presentes.
- **VAL-02**: consulta acotada por timeout.
- **VAL-03**: política de reintentos cumplida.
- **VAL-04**: interpretación produce referencias ordenadas + paginación; no interpretable = `respuesta_invalida`.
- **VAL-05**: `search_result` completo con `indice_set` antes de entregar control.
- **VAL-06**: iterador coherente; set seleccionado existe/rango; queda marcado procesado.

### Condiciones
- **Normal**: `search_result` construido, éxito con lista posiblemente vacía o fallo.
- **Fallo de set**: no aborta ni descarta fuente.
- **Aborto**: sesión/sets/iterador ausentes/corruptos; ausencia de set pendiente; corrupción de contexto.

### Ramas
- Salida normal única → `"¿Se encontraron ofertas?"`.
- Aborto → `"Finalizar Proceso"` con `error`.
- Re-entrada desde `"¿Quedan sets de filtros…?"`.

### Errores y excepciones

| Código | Error / excepción | Reintentable | Detección | Registro / acción | Estado |
|---|---|:---:|---:|---|---|
| ERR-01 | Sesión, sets o iterador ausentes/corruptos; o ausencia de set pendiente | No | 1–2 | Evento crítico; aborto | `error` |
| ERR-02 | `filtros_no_aplicables` | No | 3 | Evidencia de fallo; set omitido | fallo de set |
| ERR-03 | `fuente_inalcanzable` | Sí | 3 | Backoff/reintento; agotado → evidencia | fallo de set |
| ERR-04 | `tiempo_agotado_consulta` | Sí | 3 | Ídem ERR-03 | fallo de set |
| ERR-05 | `sesion_expirada` | No | 3 | Evidencia de fallo; sin re-ingreso | fallo de set |
| ERR-06 | `respuesta_invalida` | No | 4 | Evidencia de fallo | fallo de set |
| ERR-07 | `error_interno_consulta` | No | 3–5 | Evidencia de fallo | fallo de set |
| ERR-08 | Corrupción del contexto al construir `search_result` | No | 5 | Evento crítico; aborto | `error` |

**Contrato de códigos**: `consulta_exitosa`, `filtros_no_aplicables`, `respuesta_invalida`, `fuente_inalcanzable`, `tiempo_agotado_consulta`, `sesion_expirada`, `error_interno_consulta`.

**Éxito del nodo**: consulta ejecutada, filtros aplicados si configurados, respuesta interpretada; lista puede ser vacía.

### Escenarios límite
- Set vacío → búsqueda base.
- Plataforma sin soporte de filtros → ERR-02; set omitido, fuente continúa.
- Respuesta vacía válida vs corrupta: éxito con lista vacía vs ERR-06.
- Sesión expirada durante consulta → ERR-05.
- Caída transitoria → ERR-03/ERR-04 con reintento.
- Cambio de fuente → reinicio de iterador.
- Re-entrada por siguiente set → iterador ya avanzado.

### Dependencias y contratos
- **Antecesores**: rama Sí de ingreso; rama Sí de sets.
- **Sucesor normal**: `"¿Se encontraron ofertas?"`.
- **Sucesor de aborto**: `"Finalizar Proceso"`.
- **Contratos consumidos**: sesión activa; sets no vacíos/ordenados; timeout/reintentos/backoff.
- **Contratos entregados**: `search_result` con `indice_set`; iterador avanzado.
- **Impactos aprobados**:
  - `"¿Se encontraron ofertas?"` v1.1: Sí → captura; No → registro y luego decisión de sets.
  - `"¿Quedan sets…?"` lee iterador; su No retorna a fuentes.
  - Bucle de captura consume `ofertas_primera_pagina` y `estado_paginacion`.
  - Registros incorporan `indice_set`.
  - `"Seleccionar la siguiente fuente pendiente"` no requiere reedición por iterador de sets.

### Notas de implementación
- Adaptador por fuente encapsula filtros e interpretación.
- Iterador vinculado a `fuente_id`; reiniciar si cambió fuente; marcar al seleccionar.
- Referencias = identificador/URL en orden de plataforma.
- `total_declarado` solo si la plataforma lo expone; si no, indeterminado.
- `estado_paginacion` debe permitir pedir página siguiente sin re-ejecutar búsqueda.
- Nunca continuar sin filtros ante `filtros_no_aplicables`.
- Evidencia sin credenciales/tokens/cookies.

### Pasos funcionales
1. **Leer insumos**. Entrada: sesión, sets, iterador, IDs, timeout/reintentos. Proceso: acceder desde contexto. Salida: insumos. Val: VAL-01. Err: ERR-01.
2. **Seleccionar set pendiente**. Entrada: sets, iterador, `fuente_id`. Proceso: reiniciar si cambió fuente; seleccionar primer no procesado; marcar procesado; fijar `set_corriente`. Salida: `set_corriente`, iterador avanzado. Val: VAL-06. Err: ERR-01.
3. **Aplicar filtros y ejecutar consulta**. Entrada: sesión, filtros, timeout, reintentos. Proceso: mapear filtros; set vacío = base; consulta; reintentos según código. Salida: respuesta cruda. Val: VAL-02, VAL-03. Err: ERR-02, ERR-03, ERR-04, ERR-05, ERR-07.
4. **Interpretar respuesta**. Entrada: respuesta cruda. Proceso: convertir a referencias ordenadas; extraer paginación y total si existe; no interpretable = `respuesta_invalida`. Salida: referencias + paginación + total. Val: VAL-04. Err: ERR-06, ERR-07.
5. **Construir `search_result`**. Entrada: resultados o fallo, `indice_set`, intentos. Proceso: construir estructura completa. Salida: `search_result` en contexto. Val: VAL-05. Err: ERR-07, ERR-08.
6. **Entregar control**. Entrada: contexto con `search_result`. Proceso: cerrar nodo. Salida: flujo a `"¿Se encontraron ofertas?"`. Err: ninguna.

---

## Nodo decisión: “¿Se encontraron ofertas?”  
**Versión**: 1.1 (aprobada)

### Posición y cambios aprobados
Entre `"Aplicar los filtros básicos…"` v1.1 y:
- Sí → `"Capturar ofertas"`;
- No → `"Registrar suceso o error en 'errores o sucesos'"`.

Cambios oficializados:
1. Se elimina el nodo de conteo; auditoría de sesión vive dentro de `"Capturar ofertas"`.
2. Rama No, tras registro, se enruta a `"¿Quedan sets de filtros por aplicar en esta fuente?"`, no a iteración de fuentes.
3. Bucle por oferta reemplazado por captura por lote con políticas por fuente.

### Objetivo
Evaluar `search_result` del set corriente y bifurcar: capturar ofertas o registrar resultado del set y continuar con sets restantes.

### Descripción funcional
Lee `search_result`, valida consistencia, evalúa:
```text
estado == exito y conteo(ofertas_primera_pagina) > 0
```
Decisión pura: no re-consulta plataforma, no registra, no tipifica. Inconsistencia aborta.

### Entradas
Contexto: `search_result`, `id_corrida`, `fuente_id`, `id_sesion`.

### Salidas
- **Sí** → `"Capturar ofertas"` con referencias no vacías + paginación.
- **No** → `"Registrar suceso o error en 'errores o sucesos'"` con `search_result` como carga.
- **Aborto** → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: evaluación pura; prohibido re-consultar plataforma.
- **RN-02**: condición = éxito y conteo > 0.
- **RN-03**: éxito con conteo 0 = válido sin ofertas → rama No; registro como suceso aguas abajo.
- **RN-04**: validar estructura completa y, si éxito, lista presente con conteo ≥ 0; violación = aborto.
- **RN-05**: no registra ni tipifica; lo hace nodo de rama No.
- **RN-06**: contratos: Sí garantiza referencias no vacías + paginación; No garantiza carga de registro.
- **RN-07**: no existe nodo de conteo; auditoría de sesión pertenece a `"Capturar ofertas"`.
- **RN-08**: rama No omite el set corriente, no la fuente; continuación decide `"¿Quedan sets…?"`.

### Validaciones
- **VAL-01**: `search_result` presente.
- **VAL-02**: estructura completa incluido `indice_set`; si éxito, lista presente con conteo ≥ 0.
- **VAL-03**: Sí solo con éxito y conteo > 0.

### Condiciones y ramas
- **Sí**: éxito y conteo > 0.
- **No**: fallo cualquier código, o éxito con conteo 0.
- **Aborto**: `search_result` ausente/corrupto o estructura inválida/éxito sin lista.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | `search_result` ausente o corrupto | 1 | Evento crítico con `id_corrida`, `fuente_id`, `id_sesion`, `indice_set` | Aborto | `error` |
| ERR-02 | Estructura inválida o éxito sin lista | 2 | Evento crítico con `id_corrida`, `fuente_id`, `id_sesion`, `indice_set` | Aborto | `error` |

### Escenarios límite
- Búsqueda fallida con cualquier código → No; set omitido, fuente continúa.
- Éxito sin ofertas → No; suceso aguas abajo.
- Éxito con ofertas → Sí.
- Violación de contrato → aborto visible.

### Dependencias y contratos
- **Antecesor**: `"Aplicar los filtros básicos…"` v1.1.
- **Sucesor Sí**: `"Capturar ofertas"`.
- **Sucesor No**: registro, que enruta a `"¿Quedan sets…?"`.
- **Impactos aprobados**:
  - registro consume `search_result`, tipifica error/suceso, incluye `indice_set`, enruta a sets;
  - `"Capturar ofertas"` consume primera página/paginación, aplica políticas y escribe auditoría;
  - `"¿Quedan ofertas…?"` cierra bucle de captura; sets cierra fuente o reentra.

### Notas de implementación
- Evaluación pura; sin I/O externo salvo evento crítico de aborto.
- No ramificar por `codigo_motivo`.
- No registrar aquí.
- Rama No nunca descarta fuente por sí misma.

### Pasos funcionales
1. **Leer `search_result`**. Entrada: contexto. Proceso: acceder sin re-consultar. Salida: `search_result`. Val: VAL-01. Err: ERR-01.
2. **Validar consistencia**. Entrada: `search_result`. Proceso: estructura y lista si éxito. Salida: validado. Val: VAL-02. Err: ERR-02.
3. **Evaluar**. Entrada: validado. Proceso: éxito y conteo > 0. Salida: Sí/No. Err: ninguna.
4. **Rama Sí**. Entrada: Sí. Proceso: entregar control. Salida: flujo a `"Capturar ofertas"`. Val: VAL-03. Err: ninguna.
5. **Rama No**. Entrada: No, `search_result`. Proceso: entregar control sin registrar; set omitido. Salida: flujo a registro. Err: ninguna.

---

## Nodo proceso: “Capturar ofertas”  
**Versión**: 1.1 (aprobada)  
**Nota de implementación aprobada**: reedición 2026-08-11 — `estado_captura` incorpora `indice_set`; la implementación de la sub-fase 4.4 ya lo produce (desde 2026-08-09).

### Posición
Entre:
- rama Sí de `"¿Se encontraron ofertas?"` para primer lote del set;
- rama Sí de `"¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"` para lotes siguientes.

Sucesor: `"Registrar ofertas capturadas en 'Ofertas Totales'"`. Nodo re-entrante por lote.

### Objetivo
Capturar información completa disponible de las ofertas del lote corriente, aplicar `politicas_de_captura` efectivas mediante adaptador, actualizar progreso y escribir auditoría de sesión en `"control de sesiones"` en el primer lote del set. No registra ofertas en `"Ofertas Totales"`.

### Descripción funcional
Lee insumos de captura. En primer lote del par `(id_sesion, indice_set)` escribe auditoría con tolerancia a degradación. Determina alcance del lote:
- primera pasada: referencias de `search_result`;
- pasadas siguientes: página siguiente vía `estado_paginacion`, con pausas y estrategia anti-bloqueo.

Verifica límites antes de capturar:
- `max_paginas` por búsqueda/set;
- `max_ofertas_por_corrida` con alcance `(corrida, fuente)`.

Captura información original de cada oferta del lote. Falla individual excluye la oferta con evento `oferta_no_capturada`; el lote continúa. Evalúa resultado del lote, actualiza progreso y guarda `capture_batch` + `estado_captura`.

### Entradas
- `search_result`: `ofertas_primera_pagina`, `estado_paginacion`, `indice_set`, `total_declarado`.
- Sesión activa: `id_sesion` + handle.
- Políticas efectivas: `max_paginas`, `max_ofertas_por_corrida`, `pausa_entre_lotes`, `estrategia_anti_bloqueo`.
- Progreso: `paginas_consumidas`, `capturadas_acumuladas_fuente`.
- `id_corrida`, `fuente_id`.
- Reintentos/backoff globales.

### Salidas
- `capture_batch`: ofertas capturadas con información original + trazabilidad por oferta.
- `estado_captura`: `{estado, codigo_motivo, paginas_consumidas, capturadas_acumuladas_fuente, limite_alcanzado, indice_set}`.
- Auditoría de sesión en `"control de sesiones"` o marca degradada.
- Control único a `"Registrar ofertas capturadas en 'Ofertas Totales'"`.
- Aborto → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: solo contexto; no releer almacén.
- **RN-02**: granularidad del lote definida por adaptador: masivo o incremental; configuración solo acota límites.
- **RN-03**: capturar toda la información original disponible; prohibido interpretar/clasificar/evaluar.
- **RN-04**: falla por oferta = exclusión + evento `oferta_no_capturada`; lote continúa.
- **RN-05**: límites verificados antes de capturar. Límite alcanzado → lote vacío + `limite_alcanzado = true`.
- **RN-06**: reintentos solo para `fuente_inalcanzable` y `tiempo_agotado_captura`; resto fallo inmediato. Ante fallo de lote, conservar lote parcial.
- **RN-07**: auditoría por `(id_sesion, indice_set)` en primer lote:
  ```text
  id_sesion, id_corrida, fuente_id, indice_set, marca_temporal,
  total_declarado, conteo_primera_pagina, hay_mas_paginas,
  coherencia, estado_auditoria
  ```
  Fallo de escritura: reintento único; si persiste, evento crítico y continuación degradada.
- **RN-08**: no escribe en `"Ofertas Totales"`; registro pertenece al nodo siguiente.
- **RN-09**: evidencia acotada; trazabilidad completa en eventos y ofertas.
- **RN-10**: `limite_alcanzado` es señal de cierre: excluye Sí en `"¿Quedan ofertas…?"` y `"¿Quedan sets…?"` lo trata como cierre de fuente.

### Validaciones
- **VAL-01**: insumos presentes.
- **VAL-02**: límites verificados antes de capturar.
- **VAL-03**: política de reintentos cumplida.
- **VAL-04**: en incremental, pausas y anti-bloqueo aplicados.
- **VAL-05**: `capture_batch` y `estado_captura` completos con trazabilidad.
- **VAL-06**: auditoría completa o marca degradada documentada.

### Condiciones
- **Normal**: `estado_captura` construido: éxito completo/parcial, fallo con lote parcial, o lote vacío por límite.
- **Fallo de lote**: no aborto; lote parcial conservado.
- **Aborto**: insumos ausentes/corruptos; corrupción de contexto.

### Ramas
- Normal única → `"Registrar ofertas capturadas en 'Ofertas Totales'"`.
- Aborto → `"Finalizar Proceso"` con `error`.
- Re-entrada desde `"¿Quedan ofertas…?"`.

### Errores y eventos

| Código | Error / evento | Reint. | Detección | Registro / acción | Estado |
|---|---|:---:|---:|---|---|
| ERR-01 | Insumos ausentes/corruptos | No | 1 | Evento crítico; aborto | `error` |
| ERR-02 | Fallo de auditoría tras reintento único | No | 2 | Evento crítico; continuar degradado | continúa |
| ERR-03 | `fuente_inalcanzable` | Sí | 3–4 | Backoff/reintento; agotado → fallo de lote con parcial | fallo de lote |
| ERR-04 | `tiempo_agotado_captura` | Sí | 3–4 | Ídem ERR-03 | fallo de lote |
| ERR-05 | `sesion_expirada` | No | 4 | Fallo de lote con parcial; sin re-ingreso | fallo de lote |
| ERR-06 | `bloqueo_plataforma` | No | 4 | Fallo de lote con parcial | fallo de lote |
| ERR-07 | `respuesta_invalida` | No | 3–4 | Fallo de lote con parcial | fallo de lote |
| ERR-08 | `error_interno_captura` | No | 3–5 | Fallo de lote con parcial | fallo de lote |
| ERR-09 | Corrupción del contexto al guardar | No | 6 | Evento crítico; aborto | `error` |
| EVT-01 | `oferta_no_capturada` | No | 4 | Evento con referencia; excluir oferta; lote continúa | continúa |

**Contrato de códigos**: `captura_exitosa`, `fuente_inalcanzable`, `tiempo_agotado_captura`, `sesion_expirada`, `bloqueo_plataforma`, `respuesta_invalida`, `error_interno_captura`; evento por oferta: `oferta_no_capturada`.

### Escenarios límite
- Mecanismo masivo vs incremental.
- Límite de páginas u ofertas alcanzado → lote vacío + `limite_alcanzado`.
- Oferta individual defectuosa → EVT-01.
- Caída transitoria de página → ERR-03/ERR-04 con reintento.
- Bloqueo o sesión expirada a mitad de lote → lote parcial conservado.
- Lote vacío por límites entregado al registro como no-op.

### Dependencias y contratos
- **Antecesores**: `"¿Se encontraron ofertas?"`; `"¿Quedan ofertas…?"`.
- **Sucesor normal**: `"Registrar ofertas capturadas en 'Ofertas Totales'"`.
- **Sucesor de aborto**: `"Finalizar Proceso"`.
- **Contratos consumidos**: `search_result`, sesión, políticas efectivas, progreso.
- **Contratos entregados**: `capture_batch`, `estado_captura`, auditoría por `(id_sesion, indice_set)`.
- **Impactos aprobados**:
  - registro consume `capture_batch`; lote vacío = no-op; deduplicación se define allí;
  - `"¿Quedan ofertas…?"` usa `estado_captura`, `estado_paginacion`, `max_paginas`, `limite_alcanzado`;
  - `"¿Quedan sets…?"` trata `limite_alcanzado` como cierre de fuente.

### Notas de implementación
- Adaptador encapsula mecanismo masivo/incremental y acceso a detalle.
- Aplicar `pausa_entre_lotes` y `estrategia_anti_bloqueo` en incremental.
- Progreso persiste en contexto entre pasadas.
- Conservar lote parcial ante fallo.
- Auditoría única por `(id_sesion, indice_set)`; idempotencia ante reentradas.
- No escribir en `"Ofertas Totales"`; no interpretar contenido.

### Pasos funcionales
1. **Leer insumos**. Entrada: `search_result`, sesión, políticas, progreso, IDs. Proceso: acceder desde contexto. Salida: insumos. Val: VAL-01. Err: ERR-01.
2. **Auditoría de sesión**. Entrada: `id_sesion`, `indice_set`, `search_result`. Proceso: si primer lote, escribir registro completo; fallo → reintento único y degradado. Salida: registro o marca degradada. Val: VAL-06. Err: ERR-02.
3. **Determinar lote y límites**. Entrada: progreso, políticas, `estado_paginacion`. Proceso: primera pasada usa referencias; siguientes, página siguiente con pausas/anti-bloqueo; verificar límites; límite → lote vacío + `limite_alcanzado`. Salida: alcance del lote o lote vacío. Val: VAL-02, VAL-03. Err: ERR-03, ERR-04, ERR-08.
4. **Capturar por oferta**. Entrada: referencias, sesión, adaptador. Proceso: capturar información disponible; fallas individuales excluyen con evento. Salida: ofertas capturadas. Val: VAL-04. Err: EVT-01; ERR-05, ERR-06, ERR-07, ERR-08.
5. **Evaluar lote y progreso**. Entrada: capturas, progreso, intentos. Proceso: éxito/fallo; actualizar `paginas_consumidas`, `capturadas_acumuladas_fuente`; calcular `limite_alcanzado`. Salida: `estado_captura` + lote. Err: ERR-03 a ERR-08.
6. **Guardar en contexto**. Entrada: lote, `estado_captura`. Proceso: persistir con trazabilidad por oferta. Salida: contexto actualizado. Val: VAL-05. Err: ERR-09.
7. **Entregar control**. Entrada: contexto. Proceso: cerrar nodo. Salida: flujo a `"Registrar ofertas capturadas en 'Ofertas Totales'"`. Err: ninguna.

---

## Nodo proceso: “Registrar ofertas capturadas en 'Ofertas Totales'”  
**Versión**: 1.0 (aprobada)  
**Nota de implementación aprobada**: Sub-fase 4.4, 2026-08-09.

### Posición
Entre `"Capturar ofertas"` v1.0 y `"¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"`. Posición definitiva.

### Objetivo
Persistir `capture_batch` en `"Ofertas Totales"` conservando información original, trazabilidad e `id_externo` crudo cuando exista, y liberar el lote. No normaliza ni verifica identidad más allá de `id_externo`. La deduplicación avanzada en dos capas pertenece al Módulo 2.

### NOTA — Desvío aprobado Sub-fase 4.4
- Se introdujo deduplicación por `id_externo` vía `upsert_oferta`.
- Si la fila existe: solo se refresca `fecha_ultima_verificacion` y se conserva el `id`.
- Si no existe: se inserta fila nueva.
- Persistencia por oferta; RN-06 de transacción única de lote queda relajada a nivel de oferta.
- MVP: catálogos `empresas`/`ubicaciones` no resueltos:
  - `empresa_id` y `ubicacion_id` = `NULL`;
  - crudo del adaptador en `empresa_nombre` y `ubicacion_nombre`;
  - `fuente_id` guardado en `fuente_id` sin constraint FK.
- Documentado en DOC-13/13-A y tracker, 2026-08-09.

### Descripción funcional
Lee `capture_batch`:
- lote vacío → no-op, sin escritura ni error;
- lote no vacío → persistir ofertas.

Base 1.0: persistencia como filas nuevas en única transacción.  
Bajo NOTA aprobada: persistencia por oferta mediante upsert por `id_externo`.

Fallo de escritura: reintento único; si persiste, evento crítico y aborto. Tras persistir o no-op, libera lote.

### Entradas
Contexto: `capture_batch` con información original, `id_externo` best-effort, metadatos `id_corrida`, `fuente_id`, `id_sesion`, `indice_set`, referencia; conexión a `"Ofertas Totales"`.

### Salidas
- Lote persistido o ninguna escritura si vacío.
- Contexto con `capture_batch` liberado.
- Control único a `"¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"`.
- Aborto → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: solo contexto; no releer almacenes ni re-consultar plataformas.
- **RN-02** (con NOTA): upsert por `id_externo`; existente refresca `fecha_ultima_verificacion` y conserva `id`; nuevo inserta. Deduplicación dos capas del Módulo 2 no se ejecuta aquí.
- **RN-03**: cada fila conserva información original íntegra, `id_externo` nullable, `empresa_nombre`/`ubicacion_nombre` crudos, `empresa_id`/`ubicacion_id` NULL en MVP, y trazabilidad: `id_corrida`, `fuente_id`, `id_sesion`, `indice_set`, marcas temporales de captura y última verificación.
- **RN-04**: prohibido transformar, normalizar o limpiar contenido o URLs; crudo se conserva crudo.
- **RN-05**: lote vacío = no-op.
- **RN-06**: base: transacción única por lote; bajo NOTA aprobada, persistencia por oferta.
- **RN-07**: fallo de escritura/transacción: reintento único; si persiste, evento crítico y aborto. `"Ofertas Totales"` es salida esencial.
- **RN-08**: liberar lote tras persistir o no-op.

### Validaciones
- **VAL-01**: `capture_batch` presente.
- **VAL-02**: cada oferta tiene información original y metadatos; `id_externo` nullable.
- **VAL-03**: base: transacción única; NOTA aprobada: persistencia por oferta.
- **VAL-04**: lote liberado y control entregado.

### Condiciones
- **Normal**: lote persistido o lote vacío.
- **Aborto**: `capture_batch` ausente/corrupto; fallo de escritura tras reintento.

### Ramas
- Normal única → `"¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?"`.
- Aborto → `"Finalizar Proceso"` con `error`.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | `capture_batch` ausente o corrupto | 1 | Evento crítico con `id_corrida`, `fuente_id`, `id_sesion`, `indice_set` | Aborto | `error` |
| ERR-02 | Fallo de escritura/transacción tras reintento único | 3 | Evento crítico con `id_corrida`, `fuente_id`, `id_sesion`, `indice_set` | Aborto | `error` |

### Escenarios límite
- Lote vacío por límite o fallo → no-op.
- Ofertas sin `id_externo` → campo nulo; Módulo 2 resolverá por capa difusa.
- Fallo parcial → rollback/base según modo; reintento único; aborto si persiste.
- Caída tras persistir → lo persistido queda; lote liberado no se reprocesa.

### Dependencias y contratos
- **Antecesor**: `"Capturar ofertas"` v1.0.
- **Sucesor normal**: `"¿Quedan ofertas por capturar…?"`.
- **Sucesor de aborto**: `"Finalizar Proceso"`.
- **Contrato entregado**: `"Ofertas Totales"` como almacén crudo con trazabilidad e `id_externo`; lote liberado.
- **Impactos aprobados**:
  - decisión siguiente no depende de este nodo;
  - Módulo 2 aplicará deduplicación dos capas: estricta por `fuente_id` + `id_externo` normalizado; difusa por título+empresa+ubicación.

### Notas de implementación
- Base 1.0: insertar filas nuevas, transacción única, rollback completo.
- NOTA 4.4 aprobada: upsert por `id_externo` y persistencia por oferta.
- No normalizar URLs ni contenido.
- Reintento único; aborto si persiste.
- Liberar lote inmediatamente.
- No interpretar contenido.

### Pasos funcionales
1. **Leer lote**. Entrada: contexto, conexión. Proceso: acceder a `capture_batch`. Salida: lote. Val: VAL-01. Err: ERR-01.
2. **Evaluar lote vacío**. Entrada: lote. Proceso: si vacío, no-op y salto a liberación. Salida: señal de continuación. Err: ninguna.
3. **Persistir**. Entrada: lote. Proceso: upsert por oferta según NOTA: existente refresca `fecha_ultima_verificacion`; nuevo inserta con información original, crudos y trazabilidad. Fallo → reintento único; si persiste, aborto. Salida: lote persistido. Val: VAL-02, VAL-03. Err: ERR-02.
4. **Liberar y entregar**. Entrada: contexto. Proceso: liberar `capture_batch`; cerrar nodo. Salida: flujo a `"¿Quedan ofertas por capturar…?"`. Val: VAL-04. Err: ninguna.

---

## Nodo decisión: “¿Quedan ofertas por capturar en la búsqueda actual (según políticas)?”  
**Versión**: 1.0 (aprobada)

### Posición
Entre `"Registrar ofertas capturadas en 'Ofertas Totales'"` y:
- Sí → `"Capturar ofertas"`;
- No → `"¿Quedan sets de filtros por aplicar en esta fuente?"`.

Punto único de control del bucle de lotes del set corriente.

### Objetivo
Evaluar si quedan ofertas capturables dentro de límites de política; Sí reentra a captura; No cierra búsqueda y pasa a sets.

### Descripción funcional
Lee `estado_captura`, `estado_paginacion` y políticas. Valida consistencia. Evalúa condición compuesta:
```text
estado_captura.estado == exito
y estado_paginacion reporta pendientes
y paginas_consumidas < max_paginas
y limite_alcanzado == false
```
Decisión pura: no consulta plataforma, no registra, no reintenta, no muta estado.

### Entradas
Contexto: `estado_captura`, `estado_paginacion`, políticas efectivas, `id_corrida`, `fuente_id`, `id_sesion`, `indice_set`.

### Salidas
- **Sí** → `"Capturar ofertas"` para siguiente lote.
- **No** → `"¿Quedan sets de filtros por aplicar en esta fuente?"`.
- **Aborto** → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: evaluación pura sobre contexto; prohibido consultar plataforma.
- **RN-02**: condición Sí = conjunción completa indicada.
- **RN-03**: `estado_captura.estado == fallo` cierra búsqueda; reintentos transitorios son responsabilidad de captura.
- **RN-04**: lote vacío con páginas restantes continúa; bucle acotado por `paginas_consumidas`.
- **RN-05**: validar consistencia de insumos; violación = aborto visible.
- **RN-06**: no registra, no reintenta, no muta estado.

### Validaciones
- **VAL-01**: insumos presentes.
- **VAL-02**: `estado_captura` completo; `max_paginas` y `max_ofertas_por_corrida` presentes.
- **VAL-03**: Sí solo con condición compuesta completa.

### Condiciones y ramas
- **Sí**: los cuatro conjuntos verdaderos.
- **No**: cualquiera falso, incluido fallo de captura.
- **Aborto**: insumos ausentes/corruptos o estructura inválida/políticas ausentes.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | Insumos ausentes/corruptos | 1 | Evento crítico con IDs | Aborto | `error` |
| ERR-02 | `estado_captura` inválido o políticas ausentes | 2 | Evento crítico con IDs | Aborto | `error` |

### Escenarios límite
- Lote fallido no reintentable → No.
- Límite alcanzado → No.
- Paginación sin pendientes → No.
- Página intermedia vacía con pendientes y límites holgados → Sí.
- Violación de contrato → aborto.

### Dependencias y contratos
- **Antecesor**: `"Registrar ofertas capturadas en 'Ofertas Totales'"`.
- **Sucesor Sí**: `"Capturar ofertas"`.
- **Sucesor No**: `"¿Quedan sets de filtros por aplicar en esta fuente?"`.
- **Impactos aprobados**:
  - sets tratará `limite_alcanzado == true` como cierre de fuente;
  - reentrada con progreso actualizado.

### Notas de implementación
- Evaluación pura; sin I/O, sin escrituras, sin reintentos, sin mutación.
- Evaluar en orden definido para diagnóstico.
- No interpretar `codigo_motivo` ni contenido.

### Pasos funcionales
1. **Leer insumos**. Entrada: `estado_captura`, paginación, políticas, IDs. Proceso: acceder desde contexto. Salida: insumos. Val: VAL-01. Err: ERR-01.
2. **Validar consistencia**. Entrada: insumos. Proceso: estructura y políticas. Salida: validados. Val: VAL-02. Err: ERR-02.
3. **Evaluar condición**. Entrada: validados. Proceso: conjunción RN-02. Salida: Sí/No. Err: ninguna.
4. **Rama Sí**. Entrada: Sí. Proceso: entregar control. Salida: flujo a `"Capturar ofertas"`. Val: VAL-03. Err: ninguna.
5. **Rama No**. Entrada: No. Proceso: entregar control. Salida: flujo a `"¿Quedan sets…?"`. Err: ninguna.

---

## Nodo decisión: “¿Quedan sets de filtros por aplicar en esta fuente?”  
**Versión**: 1.0 (aprobada)

### Posición
Entre rama No de `"¿Quedan ofertas por capturar…?"` y:
- Sí → `"Aplicar los filtros básicos…"`;
- No → `"¿Quedan fuentes por procesar en esta corrida?"`.

Cierra el ciclo de sets de la fuente corriente.

### Objetivo
Evaluar si quedan sets pendientes y si la fuente puede continuar. Sí reentra a filtros; No cierra fuente y retorna a iteración de fuentes.

### Descripción funcional
Lee iterador de sets, `search_result` del set corriente, `estado_captura` si `indice_set` coincide, y `limite_alcanzado`. Valida consistencia. Clasifica si la fuente está comprometida por fallo Grupo A. Evalúa:
```text
quedan sets no procesados
y limite_alcanzado == false
y fuente_comprometida == false
```
No muta iterador; el iterador pertenece a `"Aplicar filtros básicos"`.

### Entradas
Contexto: iterador de sets, `search_result`, `estado_captura`, `limite_alcanzado`, `id_corrida`, `fuente_id`, `id_sesion`.

### Salidas
- **Sí** → `"Aplicar los filtros básicos…"` con siguiente set.
- **No** → `"¿Quedan fuentes por procesar en esta corrida?"`.
- **Aborto** → `"Finalizar Proceso"` con `error`.

### Reglas de negocio
- **RN-01**: evaluación pura; prohibido consultar plataforma.
- **RN-02**: condición Sí = conjunción completa.
- **RN-03**: clasificación Grupo A / Grupo B propiedad exclusiva de este nodo:
  - **Grupo A — comprometen la fuente**: `sesion_expirada`, `bloqueo_plataforma`, `fuente_inalcanzable`, `tiempo_agotado_consulta`, `tiempo_agotado_captura`, `error_interno_consulta`, `error_interno_captura`.
  - **Grupo B — propios del set**: `filtros_no_aplicables`, `respuesta_invalida`.
- **RN-04**: resultado del set corriente se lee de `search_result` si búsqueda falló; de `estado_captura` solo si `estado_captura.indice_set == indice_set` corriente.
- **RN-05**: validar consistencia: iterador coherente con `fuente_id`; `search_result.indice_set` == set corriente.
- **RN-06**: no registra, no reintenta, no muta estado; iterador de sets lo avanza `"Aplicar filtros básicos"`.
- **RN-07**: fuente corriente ya figura procesada en iterador de fuentes; rama No no requiere mutación adicional.

### Validaciones
- **VAL-01**: insumos presentes.
- **VAL-02**: iterador coherente; `indice_set` alineado.
- **VAL-03**: Sí solo con condición completa.

### Condiciones y ramas
- **Sí**: quedan sets, límite no alcanzado, fuente no comprometida.
- **No**: sin sets restantes, límite alcanzado o fuente comprometida por Grupo A.
- **Aborto**: insumos ausentes/corruptos o iterador/`indice_set` incoherente.

### Errores

| Código | Error / excepción | Detección | Registro | Acción | Estado |
|---|---|---:|---|---|---|
| ERR-01 | Insumos ausentes/corruptos | 1 | Evento crítico con `id_corrida`, `fuente_id`, `id_sesion` | Aborto | `error` |
| ERR-02 | Iterador incoherente o `indice_set` desalineado | 2 | Evento crítico con `id_corrida`, `fuente_id`, `id_sesion` | Aborto | `error` |

### Escenarios límite
- Sesión expirada o bloqueo anti-bot → fuente comprometida, cierre limpio.
- Límite de ofertas alcanzado con sets pendientes → No.
- Todos los sets procesados → No.
- Fallo Grupo B → Sí, siguiente set.
- Búsqueda exitosa sin captura posterior → fuente no comprometida por eso.

### Dependencias y contratos
- **Antecesor**: rama No de `"¿Quedan ofertas…?"`.
- **Sucesor Sí**: `"Aplicar los filtros básicos…"`.
- **Sucesor No**: `"¿Quedan fuentes por procesar…?"`.
- **Impactos aprobados**:
  - rama No retorna sin mutación adicional;
  - reedición `"Capturar ofertas"` v1.1 con `indice_set` en `estado_captura` implementada (sub-fase 4.4) y documentada en este documento (2026-08-11).

### Notas de implementación
- Evaluación pura; sin I/O, sin mutación.
- Política Grupo A/B vive solo aquí.
- No avanzar/reiniciar iterador de sets.
- Validación defensiva, no lógica de negocio.

### Pasos funcionales
1. **Leer insumos**. Entrada: iterador, `search_result`, `estado_captura`, límite, IDs. Proceso: acceder desde contexto. Salida: insumos. Val: VAL-01. Err: ERR-01.
2. **Validar consistencia**. Entrada: insumos. Proceso: iterador con `fuente_id`; `indice_set` corriente. Salida: validados. Val: VAL-02. Err: ERR-02.
3. **Clasificar compromiso**. Entrada: `search_result`, `estado_captura` si coincide. Proceso: `fuente_comprometida` = fallo Grupo A en búsqueda o captura del set corriente. Salida: bandera. Err: ninguna.
4. **Evaluar condición**. Entrada: validados, bandera. Proceso: conjunción RN-02. Salida: Sí/No. Err: ninguna.
5. **Rama Sí**. Entrada: Sí. Proceso: entregar control. Salida: flujo a `"Aplicar los filtros básicos…"`. Val: VAL-03. Err: ninguna.
6. **Rama No**. Entrada: No. Proceso: entregar control a iteración de fuentes. Salida: flujo a `"¿Quedan fuentes…?"`. Err: ninguna.

---

## Nodo terminal: “Finalizar Proceso”

### Identificación
Último nodo pendiente del Módulo 1. Punto de convergencia de todas las terminaciones. Oficializa motivos/estados acumulados.

### Objetivo
Cerrar la corrida de forma determinista:
1. persistir evento de terminación;
2. liberar bloqueo de concurrencia si esta corrida lo posee;
3. cerrar recursos abiertos;
4. terminar proceso.

### Entradas
Contexto best-effort:
- motivo/estado de terminación: `corrida_completada`, `sin_fuentes`, `concurrencia`, o `error`;
- `id_corrida`;
- iterador de fuentes/progreso;
- estado de bloqueo;
- handle de sesión abierto, si existe;
- conexiones de BD.

### Salidas
- Evento de terminación persistido en `"errores o sucesos"` o registro crítico local si falla escritura.
- Bloqueo liberado si esta corrida lo poseía.
- Recursos cerrados.
- Sin sucesor: fin del proceso.

### Ramas
No es nodo de decisión.

### Estados/motivos oficiales

| Estado | Motivos | Tipo |
|---|---|---|
| `normal` | `corrida_completada`, `sin_fuentes` | suceso |
| `concurrencia` | `concurrencia` | suceso |
| `error` | cualquier aborto; evento crítico de la causa ya escrito por el productor | error |

### Decisiones de diseño

| Decisión | Alternativas | Recomendación y justificación |
|---|---|---|
| Contenido del evento de terminación | A. Minimal: `id_corrida`, marca_temporal, estado, motivo, `fuentes_procesadas` si disponible. B. Resumen completo. | **A**: el detalle ya existe en eventos por nodo; duplicar resúmenes acopla y ensucia. |
| Liberación del bloqueo | A. Incondicional. B. Condicional a propiedad: lock owner == `id_corrida`. | **B**: en ruta `concurrencia` esta corrida no posee el bloqueo; liberarlo rompería la corrida activa. |
| Fallo de liberación del bloqueo | A. Aborto/error fatal. B. Reintento único + registro local + continuar. | **B**: ya en terminación; obsolescencia de bloqueo auto-sana en próxima corrida. |
| Contexto corrupto al llegar | A. Aborto sin cierre. B. Cierre best-effort con motivo por defecto. | **B**: productor ya escribió evento crítico; Finalizar debe intentar liberar/cerrar con lo disponible. |
| Limpieza de recursos | A. Implícita por fin de proceso. B. Cierre explícito best-effort. | **B**: canal de navegador/API puede sobrevivir según implementación; cierre explícito evita fugas. |

### Especificación funcional
1. **Leer estado y recursos (best-effort)**. Entrada: contexto. Proceso: leer con tolerancia; contexto ilegible/parcial → estado `error`, motivo `desconocido`; motivo fuera del conjunto → normalizar a `error`/`desconocido`. Salida: estado y recursos a cerrar. Excepción: no aborta; continuar best-effort.
2. **Registrar evento de terminación**. Entrada: estado, motivo, `id_corrida`, `fuentes_procesadas` si disponible. Proceso: escribir `{id_corrida, marca_temporal, estado, tipo, motivo, fuentes_procesadas}`; fallo → reintento único; si persiste, registro crítico local y continuar. Salida: evento persistido o registro local. Excepción: fallo tras reintento no aborta.
3. **Liberar bloqueo si corresponde**. Entrada: estado de bloqueo, `id_corrida`. Proceso: si bloqueo existe y propietario == `id_corrida`, liberar; fallo → reintento único; si persiste, registro local y continuar; si no propietario, sin acción. Salida: bloqueo liberado o sin acción. Excepción: fallo tras reintento no aborta.
4. **Cerrar recursos abiertos (best-effort)**. Entrada: handle de sesión si existe; conexiones BD. Proceso: cerrar canal y conexiones; errores se registran localmente y no impiden terminación. Salida: recursos cerrados. Excepción: errores de cierre no abortan.
5. **Terminar proceso**. Entrada: —. Proceso: cerrar nodo. Salida: fin de corrida. Excepción: ninguna.

### Puntos de aprobación
- Conjunto oficial de estados/motivos y tipo de evento.
- Evento de terminación minimal con `fuentes_procesadas` opcional.
- Liberación de bloqueo condicional a propiedad; fallo cubierto por obsolescencia.
- Cierre best-effort ante contexto corrupto.
- Cierre explícito de recursos.
- Tabla funcional tal como está.

### Estado del módulo
Con este nodo queda completo el conjunto de nodos del Módulo 1. Pendientes de implementación: ninguno. La reedición `"Capturar ofertas"` v1.1 con `indice_set` en `estado_captura` quedó implementada y documentada (2026-08-11); el documento pasa a ser el registro as-built del Módulo 1. Identificadores alineados al catálogo español (decisiones D7/D8, 2026-08-11): `run_id`→`id_corrida`, `source_id`→`fuente_id`, `session_id`→`id_sesion`, `set_indice`→`indice_set`, `id_externo_url`→`id_externo`, `timestamp_ultima_verificacion`→`fecha_ultima_verificacion`, timeout `tiempo_agotado_ingreso/consulta/captura`.
