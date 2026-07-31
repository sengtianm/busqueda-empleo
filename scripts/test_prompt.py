#!/usr/bin/env python3
"""Test AI prompts against local or cloud Ollama.

Usage:
    python scripts/probar_prompt.py PRM-001
    python scripts/probar_prompt.py PRM-001 --dry-run
    python scripts/probar_prompt.py PRM-002 --context ruta/contexto.yaml
"""

import argparse
import json
import sys
from pathlib import Path

_RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_RAIZ))

import yaml  # noqa: E402

from shared.config import load  # noqa: E402
from shared.ia_service import (  # noqa: E402
    analyze,
    load_prompt,
    renderizar_prompt,
)

_RUTA_CONTEXTOS = _RAIZ / "tests" / "fixtures" / "contextos_prompt.yaml"

RUTA_PROMPT: dict[str, str] = {
    "PRM-001": "initial_evaluation/compatibility",
    "PRM-002": "processing/diagnostic",
    "PRM-003": "processing/strategic_extraction",
    "PRM-004": "processing/application_design",
    "PRM-005": "processing/inputs",
}

PROPOSITO: dict[str, str] = {
    "PRM-001": "evaluation",
    "PRM-002": "processing",
    "PRM-003": "processing",
    "PRM-004": "processing",
    "PRM-005": "processing",
}

VARS_POR_PROMPT: dict[str, list[str]] = {
    "PRM-001": ["oferta", "perfil"],
    "PRM-002": ["oferta"],
    "PRM-003": ["oferta", "perfil"],
    "PRM-004": ["oferta", "perfil", "diagnostico"],
    "PRM-005": ["oferta", "perfil", "estrategia"],
}

MAPEO_VARIABLES: dict[str, str] = {
    "oferta": "oferta_ejemplo",
    "perfil": "perfil_ejemplo",
    "diagnostico": "diagnostico_ejemplo",
    "estrategia": "estrategia_ejemplo",
}


def _cargar_contexto(ruta: Path) -> dict[str, object]:
    with open(ruta, encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def _construir_contexto(
    datos_crudos: dict[str, object], prompt_id: str
) -> dict[str, str]:
    claves_necesarias = VARS_POR_PROMPT.get(prompt_id, [])
    contexto: dict[str, str] = {}
    for var_prompt in claves_necesarias:
        clave_fixture = MAPEO_VARIABLES.get(var_prompt, var_prompt)
        valor = datos_crudos.get(clave_fixture)
        if valor is None:
            print(
                f"  [WARNING] Variable '{var_prompt}' not found in context",
                file=sys.stderr,
            )
            contexto[var_prompt] = ""
        else:
            contexto[var_prompt] = json.dumps(valor, ensure_ascii=False)
    return contexto


def _nombre_prompt(prompt_id: str) -> str:
    ruta = RUTA_PROMPT.get(prompt_id)
    if ruta:
        return ruta
    return prompt_id


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Test AI prompts with Ollama (local or cloud)"
    )
    parser.add_argument(
        "prompt_id",
        help="Prompt ID: PRM-001 .. PRM-005, or path like 'evaluacion_inicial/compatibilidad'",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Only show the rendered prompt without sending to model",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Alternative path to the YAML context file",
    )
    args = parser.parse_args()

    prompt_id = args.prompt_id.upper() if args.prompt_id.startswith("PRM") else args.prompt_id
    ruta_prompt = _nombre_prompt(prompt_id)
    proposito = PROPOSITO.get(prompt_id, "evaluation")

    ruta_contextos = Path(args.context) if args.context else _RUTA_CONTEXTOS
    if not ruta_contextos.exists():
        print(f"Error: context file not found: {ruta_contextos}", file=sys.stderr)
        sys.exit(1)

    print(f"Prompt:     {prompt_id} → {ruta_prompt}")
    print(f"Purpose:  {proposito}")
    print(f"Context:   {ruta_contextos}")

    datos_crudos = _cargar_contexto(ruta_contextos)
    contexto = _construir_contexto(datos_crudos, prompt_id)
    print(f"Variables:  {', '.join(contexto.keys())}")

    try:
        template = load_prompt(ruta_prompt)
    except Exception as e:
        print(f"Error loading prompt: {e}", file=sys.stderr)
        sys.exit(1)

    prompt_renderizado = renderizar_prompt(template, contexto)

    print(f"\n{'='*70}")
    print("RENDERED PROMPT:")
    print(f"{'='*70}")
    print(prompt_renderizado)
    print(f"{'='*70}")

    if args.dry_run:
        print("\nDry-run mode: not sent to model.")
        return

    routing = load().get("ai_routing", {})
    proveedor = routing.get(proposito, "local")
    print(f"\nSending to {proveedor}...")
    try:
        resultado = analyze(ruta_prompt, contexto, purpose=proposito)
        print(f"\n{'='*70}")
        print("MODEL RESPONSE:")
        print(f"{'='*70}")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print(f"{'='*70}")
    except Exception as e:
        print(f"\nModel error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
