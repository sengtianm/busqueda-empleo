"""Entry point of the Discovery module: `python -m modules.discovery`."""

from modules.discovery.orchestrator import ejecutar_flujo
from shared.logging_setup import setup

setup()
ejecutar_flujo()
