# Prueba manual de prompts — Fase 3

## Requisitos

| Recurso | Para | Instrucciones |
|---------|------|---------------|
| Ollama local | PRM-001 | `ollama pull qwen3.5:4b` + `ollama serve` |
| API Key Ollama Cloud | PRM-002 al 005 | Copiar `config/.env.template` → `config/.env` y rellenar `IA_CLOUD_API_KEY` |

## Ejecución

```bash
# Activar el entorno virtual
source .venv/bin/activate

# Probar PRM-001 (evaluación, modelo local)
python scripts/probar_prompt.py PRM-001 --dry-run   # Ver prompt sin enviar
python scripts/probar_prompt.py PRM-001              # Ejecutar contra modelo

# Probar PRM-002 a PRM-005 (procesamiento, modelo cloud)
python scripts/probar_prompt.py PRM-002 --dry-run
python scripts/probar_prompt.py PRM-002

python scripts/probar_prompt.py PRM-003 --dry-run
python scripts/probar_prompt.py PRM-003

python scripts/probar_prompt.py PRM-004 --dry-run
python scripts/probar_prompt.py PRM-004

python scripts/probar_prompt.py PRM-005 --dry-run
python scripts/probar_prompt.py PRM-005
```

## Criterios de aceptación

Cada prompt debe:

- [ ] Recibir el prompt renderizado correctamente (sin `{{ }}` sin reemplazar)
- [ ] El modelo responde con JSON válido
- [ ] El JSON contiene todos los campos del resultado esperado
- [ ] El contenido es coherente con la oferta de ejemplo y el perfil

## Si falla

| Síntoma | Causa probable | Solución |
|---------|---------------|----------|
| `Connection refused` | Ollama local no está corriendo | Ejecutar `ollama serve` |
| `401 Unauthorized` | API Key de cloud no configurada | Rellenar `IA_CLOUD_API_KEY` en `.env` |
| `Prompt no encontrado` | ID mal escrito | Usar PRM-001 a PRM-005 |
| Respuesta vacía | Timeout | Aumentar `timeout_segundos` en `config.yaml` |

## Contexto de prueba

Los datos de prueba están en `tests/fixtures/contextos_prompt.yaml`.
Incluye: oferta de Data Engineer Senior, perfil profesional, y resultados simulados de PRM-002 y PRM-004.
