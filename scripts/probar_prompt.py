#!/usr/bin/env python3
"""Prueba prompts de IA contra Ollama local o cloud.

Uso:
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

from shared.config import cargar  # noqa: E402
from shared.ia_service import (  # noqa: E402
    analizar,
    cargar_prompt,
    renderizar_prompt,
)

_RUTA_CONTEXTOS = _RAIZ / "tests" / "fixtures" / "contextos_prompt.yaml"

RUTA_PROMPT: dict[str, str] = {
    "PRM-001": "evaluacion_inicial/compatibilidad",
    "PRM-002": "procesamiento/diagnostico",
    "PRM-003": "procesamiento/extraccion_estrategica",
    "PRM-004": "procesamiento/diseno_candidatura",
    "PRM-005": "procesamiento/insumos",
}

PROPOSITO: dict[str, str] = {
    "PRM-001": "evaluacion",
    "PRM-002": "procesamiento",
    "PRM-003": "procesamiento",
    "PRM-004": "procesamiento",
    "PRM-005": "procesamiento",
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
                f"  [ADVERTENCIA] Variable '{var_prompt}' no encontrada en contexto",
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
        description="Prueba prompts de IA con Ollama (local o cloud)"
    )
    parser.add_argument(
        "prompt_id",
        help="ID del prompt: PRM-001 .. PRM-005, o ruta como 'evaluacion_inicial/compatibilidad'",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Solo mostrar el prompt renderizado sin enviar al modelo",
    )
    parser.add_argument(
        "--context",
        default=None,
        help="Ruta alternativa al archivo de contexto YAML",
    )
    args = parser.parse_args()

    prompt_id = args.prompt_id.upper() if args.prompt_id.startswith("PRM") else args.prompt_id
    ruta_prompt = _nombre_prompt(prompt_id)
    proposito = PROPOSITO.get(prompt_id, "evaluacion")

    ruta_contextos = Path(args.context) if args.context else _RUTA_CONTEXTOS
    if not ruta_contextos.exists():
        print(f"Error: archivo de contexto no encontrado: {ruta_contextos}", file=sys.stderr)
        sys.exit(1)

    print(f"Prompt:     {prompt_id} → {ruta_prompt}")
    print(f"Propósito:  {proposito}")
    print(f"Contexto:   {ruta_contextos}")

    datos_crudos = _cargar_contexto(ruta_contextos)
    contexto = _construir_contexto(datos_crudos, prompt_id)
    print(f"Variables:  {', '.join(contexto.keys())}")

    try:
        template = cargar_prompt(ruta_prompt)
    except Exception as e:
        print(f"Error al cargar prompt: {e}", file=sys.stderr)
        sys.exit(1)

    prompt_renderizado = renderizar_prompt(template, contexto)

    print(f"\n{'='*70}")
    print("PROMPT RENDERIZADO:")
    print(f"{'='*70}")
    print(prompt_renderizado)
    print(f"{'='*70}")

    if args.dry_run:
        print("\nModo dry-run: no se envió al modelo.")
        return

    routing = cargar().get("ia_routing", {})
    proveedor = routing.get(proposito, "local")
    print(f"\nEnviando a {proveedor}...")
    try:
        resultado = analizar(ruta_prompt, contexto, proposito=proposito)
        print(f"\n{'='*70}")
        print("RESPUESTA DEL MODELO:")
        print(f"{'='*70}")
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print(f"{'='*70}")
    except Exception as e:
        print(f"\nError del modelo: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
