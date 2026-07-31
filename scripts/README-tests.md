# Manual Prompt Testing — Phase 3

## Requirements

| Resource | For | Instructions |
|----------|-----|--------------|
| Local Ollama | PRM-001 | `ollama pull qwen3.5:4b` + `ollama serve` |
| Ollama Cloud API Key | PRM-002 to 005 | Copy `config/.env.template` → `config/.env` and fill in `IA_CLOUD_API_KEY` |

## Execution

```bash
# Activate the virtual environment
source .venv/bin/activate

# Test PRM-001 (evaluation, local model)
python scripts/probar_prompt.py PRM-001 --dry-run   # View prompt without sending
python scripts/probar_prompt.py PRM-001              # Execute against model

# Test PRM-002 to PRM-005 (processing, cloud model)
python scripts/probar_prompt.py PRM-002 --dry-run
python scripts/probar_prompt.py PRM-002

python scripts/probar_prompt.py PRM-003 --dry-run
python scripts/probar_prompt.py PRM-003

python scripts/probar_prompt.py PRM-004 --dry-run
python scripts/probar_prompt.py PRM-004

python scripts/probar_prompt.py PRM-005 --dry-run
python scripts/probar_prompt.py PRM-005
```

## Acceptance Criteria

Each prompt must:

- [ ] Receive the prompt rendered correctly (no unreplaced `{{ }}`)
- [ ] The model responds with valid JSON
- [ ] The JSON contains all expected output fields
- [ ] The content is coherent with the example offer and profile

## Troubleshooting

| Symptom | Probable Cause | Solution |
|---------|---------------|----------|
| `Connection refused` | Local Ollama is not running | Run `ollama serve` |
| `401 Unauthorized` | Cloud API Key not configured | Fill in `IA_CLOUD_API_KEY` in `.env` |
| `Prompt not found` | Misspelled ID | Use PRM-001 to PRM-005 |
| Empty response | Timeout | Increase `timeout_seconds` in `config.yaml` |

## Test Context

Test data is located in `tests/fixtures/contextos_prompt.yaml`.
Includes: Senior Data Engineer offer, professional profile, and simulated results from PRM-002 and PRM-004.
