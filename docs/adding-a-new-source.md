# Adding a New Source (Guía para añadir una nueva fuente)

Guía operativa para incorporar una nueva plataforma de empleo (p. ej. un portal
de ofertas) al pipeline sin tocar el flujo de los nodos ni el orquestador
transversal (`modules/orchestrator/`).
Estado del proyecto: **solo LinkedIn** está registrado; esta guía prepara la
incorporación futura de cualquier otra fuente.

---

## 1. Modelo mental

Cada fuente tiene **tres piezas**:

1. **Configuración** (`config/config.yaml`): la "receta" — acceso, filtros, políticas.
2. **Adaptador** (`modules/discovery/adapters/<fuente>.py`): el "traductor" —
   cómo entrar, buscar y capturar EN ESA plataforma (selectores, paginación,
   scroll, detalle uno a uno, anti-bloqueo).
3. **Registro** (`modules/discovery/adapters/registry.py`): la "agenda" que
   mapea `fuente_id` → clase adaptadora. Los nodos (ingreso/búsqueda/captura)
   piden aquí el adaptador; **no se modifican al añadir una fuente**.

Regla de diseño **RN-10** (ficha técnica del Módulo 1): el mecanismo de captura
(masivo/incremental, paginación/scroll/detalle) es responsabilidad del
adaptador; la configuración solo lo acota vía `politicas_de_captura`.

---

## 2. Pasos para añadir una fuente

### Paso 0 — Investigación de la plataforma (imprescindible)

Antes de escribir código, documenta (fuera del repo o en borrador):

- **Acceso**: ¿pública o con autenticación? ¿qué credenciales y dónde se
  guardan (config/.env)? ¿existe un criterio de éxito verificable en el HTML
  tras entrar (p. ej. `MainFeed` para LinkedIn)?
- **Búsqueda**: URL de búsqueda, parámetros de filtros soportados
  (palabras clave, ubicación, modalidad, fecha de publicación, nivel).
- **Listado de resultados**: estructura HTML de las tarjetas (selectores),
  cuántas ofertas por página, cómo se pasa a la siguiente página
  (parámetro `?start`, botón, scroll infinito), y cómo se detecta el **fin**
  de la búsqueda.
- **Anti-bloqueo**: qué señales indican bloqueo/captcha en contenido visible,
  ritmos seguros de pausa entre páginas.
- **Oferta**: qué identifica a una oferta de forma única (URL canónica
  `id_externo`), qué campos mínimos se pueden extraer del listado sin entrar
  al detalle (título, enlace). El enriquecimiento con descripción es tarea
  posterior del Módulo 2 (Preparación de ofertas, fase 5), no del adaptador —
  ver la ficha técnica autoritativa
  [`docs/diagrams/Ficha técnica - Diagrama de flujo (Preparación de ofertas).md`](docs/diagrams/Ficha%20técnica%20-%20Diagrama%20de%20flujo%20(Preparación%20de%20ofertas).md).

### Paso 1 — Configuración (`config/config.yaml`)

Añade un bloque en `fuentes:` (modelo actual con LinkedIn):

```yaml
fuentes:
  - fuente_id: "linkedin"          # identificador único (trazabilidad)
    nombre: "LinkedIn"
    ficha_acceso:
      enlace: "https://www.linkedin.com/jobs/search"
      tipo_acceso: "con_autenticacion"   # o "publico"
      credenciales_referencia: ["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"]
      criterio_exito: "MainFeed"          # texto presente en HTML tras entrar
      timeout_segundos: 30
    sets_de_filtros:
      - indice_set: 0
        filtros:
          - tipo: "keywords"
            valor: ["Data Engineer"]
          - tipo: "ubicacion"
            valor: "Colombia"
          - tipo: "modalidad"
            valor: "remoto"
          - tipo: "fecha_publicacion"
            valor: "r86400"
    politicas_de_captura:
      max_paginas: 100
      max_ofertas_por_corrida: 1000
      pausa_entre_lotes_segundos: 5
      tope_espera_paginas_sucesivas_segundos: 10
      estrategia_anti_bloqueo: "pausa_aleatoria"
```

Consideraciones:

- **Tipos de filtro soportados** (mapeo en `linkedin.py`, `_PARAMETROS_FILTROS`):
  `keywords`, `ubicacion`, `modalidad`, `fecha_publicacion`,
  `nivel_experiencia`. Si la nueva fuente no soporta un tipo usado en su
  bloque, el adaptador debe responder con `FlowError("filtros_no_aplicables")`.
- **Valores vacíos** se omiten (sin parámetro en la URL).
- `politicas_de_captura` por fuente tiene precedencia sobre la sección
  global `captura:` (ver `run_context.py`).
- Las credenciales se referencian por nombre; el secreto vive en
  `config/.env` (nunca en el repo).

### Paso 2 — Crear el adaptador (`modules/discovery/adapters/<fuente>.py`)

Debe cumplir el contrato `AdaptadorPlataforma` (definido en `registry.py`,
verificado por mypy strict). Cuatro métodos obligatorios:

```python
class AdaptadorPlataforma(Protocol):
    def enter_source(page, ficha, credenciales=None) -> EntryResult: ...
    def apply_filters(page, ficha, set_filtros, politicas) -> SearchResult: ...
    def capture_batch(page, ficha, set_filtros, politicas) -> tuple[CaptureBatch, EstadoCaptura]: ...
    def close_session(page) -> None: ...
```

- `enter_source` abre el canal y verifica el criterio de éxito de la ficha;
  si la fuente exige autenticación y faltan credenciales → `FlowError("credenciales_no_disponibles")`.
- `apply_filters` navega la búsqueda y devuelve la primera página (`SearchResult`).
- `capture_batch` recorre **todas** las páginas con la mecánica propia de la
  plataforma y devuelve el lote (`CaptureBatch`) + estado (`EstadoCaptura`).
  Tres mecánicas típicas (todas dentro del adaptador, RN-10):
  - **Listado con paginación** (patrón actual de LinkedIn): navegar
    `?start=N`, esperar tarjetas, extraer, hasta página vacía o ausencia del
    botón "Siguiente".
  - **Scroll infinito**: hacer scroll, esperar tarjetas nuevas, extraer,
    repetir hasta que no aparezcan más.
  - **Detalle uno a uno**: navegar cada oferta, extraer, volver al listado.
- `close_session` cierra la página que quedó abierta.
- Errores esperados → `FlowError` con códigos oficiales DOC-06:
  `fuente_inalcanzable`, `bloqueo_plataforma`, `sesion_expirada`,
  `autenticacion_rechazada`, `credenciales_no_disponibles`,
  `filtros_no_aplicables`, `tiempo_agotado_ingreso/consulta/captura`.
  El código `fuente_no_soportada` (sin adaptador registrado) lo emite el
  registro, no el adaptador, y nunca se reintenta.
- El adaptador recibe la `page` (abierta por el nodo de ingreso); **no crea
  su propio navegador** y **no accede a la base de datos** (solo
  `shared/` desde los nodos).
- Para testear pausas sin dormir, usa el patrón de `LinkedInAdapter(sleep_fn=...)`.
- Convención del módulo discovery: identificadores en español para conceptos
  de dominio (`capturar_ofertas`, `ResultadoCaptura`, docstrings en español).

### Paso 3 — Registrar el adaptador (`registry.py`)

Una sola línea en `REGISTRO_ADAPTADORES`:

```python
REGISTRO_ADAPTADORES: dict[str, type[AdaptadorPlataforma]] = {
    "linkedin": LinkedInAdapter,
    "<fuente_id>": NuevoAdaptador,   # ← nueva línea
}
```

Si la fuente no está registrada, `obtener_adaptador` falla limpio con
`FlowError("fuente_no_soportada")` (sin reintentos) — no rompe la corrida
con un error raro.

### Paso 4 — Tests

- Fixtures HTML realistas en `tests/fixtures/` (datos en español, como los
  existentes `lista_linkedin_sdui_2026.html`).
- `tests/test_<fuente>_adapter.py` siguiendo el patrón de
  `test_linkedin_adapter.py` (clase `FakePage` con `url`, `goto(wait_until=...)`,
  `content()`, `wait_for_selector`): ingreso, búsqueda, captura multi-página,
  dedup, límites (`max_paginas`, `max_ofertas_por_corrida`), bloqueo.
- Los tests de nodos parchean `obtener_adaptador` (ver `test_node_ingreso.py`),
  no la clase concreta.

### Paso 5 — Validación y prueba funcional

```bash
venv/bin/ruff check .        # lint (E/F/I/N/W, línea máx 100)
venv/bin/mypy .              # typecheck strict (valida el contrato del adaptador)
venv/bin/python -m pytest tests/ -q
venv/bin/python -m modules.discovery   # prueba funcional (requiere usuario y sesión real)
```

Verificar en la BD (`data/job_search.db`): eventos de la corrida
(`captura_completada` con `páginas=N | ofertas=M`), 0 errores, dedup por
`id_externo`, cierre `corrida_completada`.

### Paso 6 — Documentación implicada (cierre)

Actualizar (con autorización, según el flujo de trabajo de AGENTS.md):

| Documento | Qué se actualiza |
|---|---|
| Ficha técnica del módulo (`docs/diagrams/`) | Flujo, reglas de negocio y códigos de error específicos de la nueva fuente |
| Ficha técnica del orquestador transversal (`docs/diagrams/`) | Solo si el cambio afecta a la coordinación entre módulos (p. ej. añadir un módulo nuevo al registro `MODULOS` y a la sección `orquestador:` de `config.yaml`) |
| Decision log (`docs/history/decision log.md`) | Nueva decisión (p. ej. D13 del registro de adaptadores; mecanismo de captura elegido) |
| tracker.md (`docs/history/tracker.md`) | Estado de la nueva tarea/fase |
| session history.md (`docs/history/session history.md`) | Entrada de la sesión (solo vía `/save`) |
| README.md | Tabla de documentación y estado |

---

## 3. Checklist final

- [ ] Investigación documentada (acceso, selectores, paginación, fin, anti-bloqueo).
- [ ] Bloque completo en `config/config.yaml` (ficha, sets de filtros, políticas).
- [ ] Adaptador con los 4 métodos del contrato y códigos `FlowError` oficiales.
- [ ] Fuente registrada en `registry.py` (1 línea).
- [ ] Fixtures + tests (ingreso, búsqueda, captura, dedup, límites, bloqueo).
- [ ] `ruff`, `mypy`, `pytest` limpios.
- [ ] Prueba funcional real + verificación en BD.
- [ ] Documentación actualizada (ficha, decision log, tracker) con autorización.

## 4. Qué NO hacer

- No modificar los nodos (`ingreso.py`, `busqueda.py`, `captura.py`) ni el
  orquestador transversal (`modules/orchestrator/`) para añadir la fuente — se
  resuelve vía registro (`REGISTRO_ADAPTADORES` y `MODULOS`).
- No poner el mecanismo de captura en la configuración (RN-10).
- No acceder a la BD desde el adaptador.
- No guardar credenciales ni secretos en archivos del repositorio.
- No hardcodear valores de negocio (topes, pausas, tiempos) — van en config.
- No inventar códigos de error: usar los oficiales de DOC-06/Appendix 5A.