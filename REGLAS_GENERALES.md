# 📋 REGLAS GENERALES DEL PROYECTO

## 🎯 Propósito del Proyecto
Sistema automatizado de búsqueda de empleo: descubre, recopila, prepara, evalúa, procesa y gestiona oportunidades para reducir tiempo/esfuerzo y apoyar la toma de decisiones.

**Objetivo:** Desde el descubrimiento hasta inputs de aplicación de alta calidad con trazabilidad completa e intervención manual mínima.

---

## 🏗️ Arquitectura

### Capas
1. **Módulos Funcionales**: `modules/` (discovery, preparation, evaluation, processing, management)
2. **Servicios Compartidos**: `shared/` (config, models, persistence, ia_service, decision_engine, state_machine)
3. **Infraestructura**: config, logs, data, tests, docs

### Flujo de Trabajo
```
Discovery → Preparation → Evaluation → Processing → Management
```

**Regla crítica:** Ningún módulo funcional puede acceder directamente a la base de datos.

---

## 🛠️ Stack Tecnológico
- Python 3.12+
- Playwright, BeautifulSoup4 + lxml, Pydantic v2, Loguru, RapidFuzz, Tenacity, httpx
- SQLite (IDs secuenciales con prefijos: EMP-0001, COR-0001, etc.)
- IA: Ollama local (qwen3.5:4b) + Cloud (gemma4:31b) vía proxy local
- Testing: pytest, ruff, mypy, black
- Configuración: PyYAML + python-dotenv

---

## 📁 Estructura del Proyecto

| Directorio | Propósito |
|------------|-----------|
| `docs/` | Documentación oficial (fichas técnicas, decisiones, tracker, diseños) |
| `config/` | Configuración centralizada (`config.yaml`, `.env.template`) |
| `prompts/` | Prompts oficiales (PRM-001 a PRM-005+, separados del código) |
| `modules/` | Módulos funcionales: discovery, preparation, evaluation, processing, management |
| `shared/` | Recursos reutilizables: config, errors, logging, retry, models, persistence, ia_service, decision_engine, state_machine |
| `data/` | Datos persistentes (input, processing, output, backup) - **NO versionar DBs** |
| `logs/` | Logs y auditoría |
| `temp/` | Archivos temporales |
| `scripts/` | Scripts auxiliares (ej. testeador de prompts) |
| `tests/` | Tests (fixtures en `tests/fixtures/`) |

---

## 📝 Convenciones de Código

### Idioma
| Elemento | Idioma | Ejemplo |
|----------|--------|---------|
| Código (variables, funciones, clases) | Inglés | `execute_search`, `capture_batch` |
| Documentación, configuración, prompts | Inglés | `config.yaml`, `PRM-001.md` |
| Nombres de directorios/archivos | Inglés | `modules/discovery/nodes/` |
| **Base de datos** (tablas, campos) | Español | `ofertas`, `id_externo`, `estado_captura` |
| **Modelos de datos** (`shared/models.py`) | Español | `Oferta`, `Fuente`, `EstadoCaptura` |
| **Persistencia** (`shared/persistence.py`) | Español | `upsert_oferta`, `leer_tabla` |
| **Estados y códigos** | Español | `capturada`, `timeout_red` |
| **Módulo discovery** (nodos, tests) | Español | `ejecutar_inicio`, `ResultadoInicio`, `fuentes_filtradas` |
| Conversaciones con el usuario | Español | Todo el diálogo |

### Reglas de Diseño
- Configuración separada de lógica de negocio
- Prompts separados del código
- Sin valores hardcodeados
- Cada transformación debe preservar datos originales
- Nunca incluir API keys, tokens, passwords o datos sensibles en el repositorio

### Estilo de Respuesta
- Español, conciso, encabezados/listas claros
- Nunca modificar archivos sin explicar primero

---

## 🔧 Skills Disponibles

### Skills Generales (`.agents/skills/`)
| Skill | Propósito |
|-------|-----------|
| `accessibility` | Accesibilidad web |
| `frontend-design` | Diseño frontend |
| `pydantic` | Modelado con Pydantic v2 |
| `python-executor` | Ejecución segura de Python |
| `python-testing-patterns` | Patrones de testing |
| `seo` | Optimización SEO |

### Skills del Proyecto (`.opencode/skills/`)
| Skill | Propósito | Uso automático cuando |
|-------|-----------|----------------------|
| `code-review` | Revisión de código | Implementación completada |
| `decision-making` | Toma de decisiones estructurada | Hay múltiples enfoques posibles |
| `implement-module` | Implementación de módulos | Se solicita crear/modificar módulo |
| `playwright` | Automatización browser | Interacción con LinkedIn/web |
| `project-architecture` | Validación arquitectónica | Cualquier cambio estructural |
| `project-documentation` | Documentación oficial | Actualizar docs |
| `python-best-practices` | Mejores prácticas Python | Todo código Python |
| `review-against-documentation` | Verificación contra docs | Cierre de tarea |
| `systematic-debugging` | Debug sistemático | Hay errores/fallos |

**Nota:** Los skills se aplican **automáticamente** según corresponda. No es necesario invocarlos explícitamente.

---

## 📜 Comandos Disponibles (`.opencode/commands/`)

| Comando | Etapa | Cuándo se usa |
|---------|-------|---------------|
| `/resume` | Contexto | Usuario invoca para ver estado del proyecto |
| `/check-analisis` | Analizar | **Automático**: agente aplica después de cada request |
| `/check-planeacion` | Planear | Usuario invoca: agente crea plan y espera aprobación |
| `/check-implementacion` | Implementar | Usuario invoca: aprueba plan y autoriza implementación |
| `/check-tests` | Verificar | Solo si el request requiere tests |
| `/check-cierre` | Cerrar | **Automático**: auto-verificación post-implementación |
| `/save` | Guardar | Usuario invoca al final de sesión (NUNCA automático) |

### Reglas del Workflow
1. Usuario invoca `/resume` → envía request (define tarea)
2. `/check-analisis` automático (readiness, gaps, impactos, riesgos, enfoques)
3. Plan solo con `/check-planeacion`
4. Implementar solo tras `/check-implementacion` aprobado
5. Validar post-cambio: lint + typecheck siempre; `/check-tests` solo si requiere
6. `/check-cierre` automático: criterios aceptación, diff, reviewers
7. Reporte de cierre → esperar aprobación antes de continuar
8. `/save` al final de sesión → actualiza session history
9. **Nunca trabajar en más de una tarea a la vez**

---

## 🔒 Seguridad y Git

### `.gitignore` - Lo que NO se sube
```
.env (pero .env.template SÍ se versiona)
venv/
__pycache__/, *.pyc
.pytest_cache/, .mypy_cache/, .ruff_cache/
coverage, htmlcov/
logs/* (excepto .gitkeep)
*.tmp, *.bak
.idea/, .vscode/, .DS_Store
*.db-shm, *.db-wal, *.db-journal
data/input/*, data/processing/*, data/output/*, data/backup/*
data/*.db (excepto .gitkeep)
temp/* (excepto .gitkeep)
dist/, build/, *.egg-info/
```

### Reglas de Commit
1. **Scope**: todos los archivos modificados/creados en la sesión
2. **Exclusiones**: solo lo definido en `.gitignore`
3. **Verificar**: `git status` y `git diff` deben coincidir con lo esperado
4. **Stage**: `git add -A` → revisar `git diff --cached`
5. **Formato**: Inglés, convencional, imperativo: `<type>(<scope>): <summary>` (≤72 chars)
   - Ej: `feat(discovery): add capture node`, `docs(history): update session 21`
6. **Push**: `git push origin <branch>` (nunca force-push sin autorización)
7. **Reportar**: hash del commit, resultado del push, worktree limpio

### Ramas
- Cada fase/módulo/cambio significativo en rama dedicada
- Nombres descriptivos: `fase-4`, `modulo-2-preparation`, `docs/...`
- Rama activa hasta que usuario autorice merge a `main`
- **Nunca hacer merge sin autorización explícita**

---

## ✅ Validación

### Comandos de Validación
```bash
ruff check .          # Lint (E/F/I/N/W, line-length 100)
mypy .                # Typecheck (strict)
pytest tests/         # Test suite (278 passing)
```

### Definition of Done
1. Validaciones relevantes ejecutadas (lint + typecheck siempre; pytest solo si aplica)
2. Criterios de aceptación del MVP Execution Plan verificados
3. Reporte entregado: Objetivo, Archivos modificados, Validaciones, Resultado, Issues
4. Reviewers aplicados: `code-reviewer`, `docs-reviewer`

### Estrategia de Testing
- Unit tests con fixtures en `tests/fixtures/`
- Integration tests tagged (Playwright)
- Respuestas LLM mockeables
- Data layer con archivos SQLite temporales

---

## 📚 Documentación Oficial

### Modelo de Autoridad
Solo documentos **primarios de construcción** son consultables (autoritativos, siempre actuales).

| Categoría | Documento | Cubre |
|-----------|-----------|-------|
| **Primario** | Ficha técnica (por módulo) | Especificación nivel nodo: flujo, reglas, códigos error, estados |
| **Primario** | DOC-13A | Modelo de datos detallado: entidades, atributos, catálogos, ERD |
| **Primario** | Appendix 5A | Catálogo oficial de prefijos (IDs, códigos) |
| **Primario** | Decision log | Decisiones aprobadas y desviaciones D1–D17 |
| **Primario** | MVP Execution Plan | Orden de construcción y criterios de aceptación |
| **Primario** | tracker.md | Estado actual de cada fase y tarea |
| **Primario** | AGENTS.md | Contrato operativo, convenciones, validación |
| **Operacional** | session history.md | Registro por sesión (actualizado con `/save`) |

### Orden de Lectura
```
AGENTS.md → decision log → ficha del módulo actual → DOC-13A → docs referenciados por la tarea
```
**No leer documentación innecesaria.**

### Mantener Documentos Actualizados
- Tras cada tarea/fase validada, actualizar AGENTS.md si cambian secciones existentes
- Solo actualizar secciones existentes (temas nuevos → Session History)
- AGENTS.md corto y útil para nuevo desarrollador
- Actualizar `tracker.md` cuando cambie estado de tarea/fase
- Incluir diffs de AGENTS.md y tracker.md en reporte de tarea
- Toda documentación oficial vive en `docs/` (single source of truth)

---

## 🔍 Close Gate

Al cerrar cada tarea, ejecutar **`docs-reviewer`**:
- Verificar cambios implementados contra documentos primarios
- Detectar documentation drift antes de validación
- Documentos de referencia: decision log, ficha del módulo, DOC-13A, MVP Plan, tracker, AGENTS.md

---

## 💾 Session History (`/save`)

### Reglas
- Solo con invocación del usuario (**NUNCA automático**)
- Historia gestionada por número de sesión (más reciente primero)
- Número = último existente + 1
- Una entrada por sesión de OpenCode (una conversación)
- Obtener ID de sesión:
  ```bash
  sqlite3 ~/.local/share/opencode/opencode.db "SELECT id, substr(title,1,60), datetime(time_updated, 'unixepoch', 'localtime') FROM session ORDER BY time_updated DESC LIMIT 1;"
  ```
- Formato de fecha: `DD/MM/YYYY`

### Campos de Entrada
| Campo | Contenido |
|-------|-----------|
| **Topics** | Bullets tipo keyword, una línea c/u, sin hashes/files/reglas |
| **Decisions** | Solo decisiones nuevas/modificadas de la sesión actual |
| **Status** | Fases completadas/pendientes (✅/⬜), resultados Ruff/mypy/pytest, rama activa |

### Proceso `/save`
1. Actualizar `session history.md` (crear/actualizar entrada de sesión actual)
2. Actualizar `tracker.md` si alguna tarea cambió de estado
3. Commit único con todos los cambios de la sesión
4. Push a rama actual
5. Reportar: hash, resultado push, worktree limpio

---

## 🚫 Restricciones

- **No** nuevas dependencias sin autorización
- **No** modificaciones a arquitectura, modelo de datos, workflow, stack tecnológico o reglas de negocio sin autorización
- **No** modificaciones a documentación oficial sin autorización
- **No** commits sin revisión previa del usuario (excepto `/save`)
- **No** merges sin autorización explícita

---

## ❓ Incertidumbre

**Nunca inventar una solución:** detenerse, explicar el problema y esperar decisión del usuario.

---

## 🤝 Cómo Trabajar Conmigo

### Lo que hago automáticamente
- Aplicar skills relevantes según la tarea
- Ejecutar `/check-analisis` tras cada request
- Ejecutar `/check-cierre` tras implementar
- Seguir convenciones de código y documentación
- Validar con ruff/mypy/pytest según corresponda
- Respetar arquitectura y patrones existentes

### Lo que necesito de ti
- Definir claramente qué quieres construir o resolver
- Aprobar planes antes de implementar (`/check-planeacion` → `/check-implementacion`)
- Invocar `/save` al final de cada sesión
- Decidir cuando haya incertidumbre o múltiples enfoques

### Flujo recomendado
```
1. /resume (para contexto)
2. Tu request → Yo analizo automáticamente
3. /check-planeacion (te presento plan)
4. /check-implementacion (apruebas → implemento)
5. Yo valido y cierro automáticamente
6. Repetir para siguiente tarea
7. /save (al finalizar sesión)
```

---

## 📊 Estado Actual (Resumen)

| Fase | Módulo | Estado | Notas |
|------|--------|--------|-------|
| 0 | Definición | ✅ Completa | Alcance, reglas, criterios |
| 1 | Infraestructura | ✅ Completa | Directorios, git, venv, config, logging, errors, models, persistence |
| 2 | Servicios compartidos | ✅ Completa | ia_service, decision_engine, state_machine |
| 3 | Prompts | ✅ Completa | PRM-001 a PRM-005 |
| 4 | Discovery | ✅ Completo | 12 nodos + orchestrator + LinkedIn adapter |
| 5 | Preparation | ⬜ Pendiente | Próximo módulo a construir |
| 6 | Evaluation | ⬜ Pendiente | - |
| 7 | Processing | ⬜ Pendiente | - |
| 8 | Management | ⬜ Pendiente | - |
| 9 | Integración MVP | ⬜ Pendiente | - |

**Tests:** 278/278 pasando (~3.6s)  
**Rama activa:** `fase-4`  
**Último commit:** 13 ago 2026, 06:48:05 -0500

---

## 📞 Contacto y Soporte

Para dudas sobre estas reglas, consultar:
- `AGENTS.md` (contrato operativo principal)
- `.opencode/commands/` (definición detallada de comandos)
- `.agents/skills/` y `.opencode/skills/` (descripciones de skills)
- `docs/history/decision log.md` (decisiones arquitectónicas)
