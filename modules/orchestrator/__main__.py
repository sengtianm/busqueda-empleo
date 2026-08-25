"""Entry point of the transversal orchestrator: `python -m modules.orchestrator`."""

from modules.orchestrator.orchestrator import ejecutar_corrida_programada
from shared.logging_setup import setup

setup()
ejecutar_corrida_programada()
