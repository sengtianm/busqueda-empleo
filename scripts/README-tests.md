# Manual Prompt Testing — Phase 3

## Requirements

| Resource | For | Instructions |
|----------|-----|--------------|
| Ollama Cloud API Key | PRM-001 to PRM-005 | Copy `config/.env.template` → `config/.env` and fill in `IA_CLOUD_API_KEY` |
| Local Ollama (optional fallback) | Local routing | `ollama pull qwen3.5:4b` + `ollama serve`, then set `ai_routing` to `local` in `config.yaml` |

> Both `evaluation` and `processing` route to the **cloud** provider by default (`ai_routing` in `config.yaml`).

## Execution

```bash
# Activate the virtual environment
source .venv/bin/activate

# Test PRM-001 (evaluation, cloud model)
python scripts/prompt_tester.py PRM-001 --dry-run   # View prompt without sending
python scripts/prompt_tester.py PRM-001              # Execute against model

# Test PRM-002 to PRM-005 (processing, cloud model)
python scripts/prompt_tester.py PRM-002 --dry-run
python scripts/prompt_tester.py PRM-002

python scripts/prompt_tester.py PRM-003 --dry-run
python scripts/prompt_tester.py PRM-003

python scripts/prompt_tester.py PRM-004 --dry-run
python scripts/prompt_tester.py PRM-004

python scripts/prompt_tester.py PRM-005 --dry-run
python scripts/prompt_tester.py PRM-005
```

## Acceptance Criteria

Each prompt must:

- [ ] Receive the prompt rendered correctly (no unreplaced `{{ }}`)
- [ ] The model responds with valid JSON
- [ ] The JSON contains all expected output fields (per the Detailed Evaluation entity, DOC-13A §2.7):

| Prompt | Output fields |
|--------|---------------|
| PRM-001 | evaluation result (initial evaluation) |
| PRM-002 | `resultado_organizacional`, `problema_organizacional`, `perfil_profesional_requerido` |
| PRM-003 | `coincidencias_perfil`, `logica_xyz`, `hipotesis_valor`, `informacion_descartada` |
| PRM-004 | `ajuste_tecnico`, `justificacion_ajuste_tecnico`, `ajuste_funcional`, `justificacion_ajuste_funcional`, `ajuste_estrategico`, `justificacion_ajuste_estrategico` |
| PRM-005 | `riesgo_sobrecalificacion`, `justificacion_riesgo`, `recomendacion_final`, `justificacion_recomendacion`, `insumos_carta_presentacion` |

- [ ] The content is coherent with the example offer and profile
- [ ] PRM-003 consumes the output of PRM-002; PRM-004 consumes PRM-002 + PRM-003; PRM-005 consumes PRM-002..004 (chained execution)

## Troubleshooting

| Symptom | Probable Cause | Solution |
|---------|---------------|----------|
| `Connection refused` | Cloud endpoint is not reachable | Check `IA_CLOUD_ENDPOINT` and network access |
| `401 Unauthorized` | Cloud API Key not configured | Fill in `IA_CLOUD_API_KEY` in `.env` |
| `Prompt not found` | Misspelled ID | Use PRM-001 to PRM-005 |
| Empty response | Timeout | Increase `timeout_seconds` in `config.yaml` |

## Test Context

Test data is located in `tests/fixtures/prompt_contexts.yaml`.
Includes: Senior Data Engineer offer, professional profile, and simulated results from PRM-002 and PRM-004.
