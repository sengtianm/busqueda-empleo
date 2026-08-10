from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

from modules.discovery.nodes.finalizar import (
    consultar_metricas,
    finalizar_proceso,
)
from modules.discovery.run_context import RunContext
from shared.persistence import actualizar_corrida, read_table, write_corrida


def _contexto() -> RunContext:
    config_fuentes = [
        {
            "source_id": "LI-01",
            "nombre": "LinkedIn",
            "ficha_acceso": {
                "url": "https://www.linkedin.com/jobs",
                "tipo_acceso": "publico",
                "criterio_exito": "global-nav",
                "timeout_segundos": 10,
            },
            "sets_de_filtros": [{"set_indice": 0, "filtros": []}],
        }
    ]
    return RunContext(config_fuentes=config_fuentes, run_id="COR-0001")


def test_finalizar_corrida_completada_estado_completada() -> None:
    contexto = _contexto()
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida") as mock_update:
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                res = finalizar_proceso(contexto, "corrida_completada")

    assert res.estado == "ok"
    campos = mock_update.call_args.args[1]
    assert campos["estado"] == "completada"
    assert campos["motivo_terminacion"] == "corrida_completada"


def test_finalizar_sin_fuentes_estado_sin_fuentes() -> None:
    contexto = _contexto()
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida") as mock_update:
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                res = finalizar_proceso(contexto, "sin_fuentes")

    assert res.estado == "ok"
    campos = mock_update.call_args.args[1]
    assert campos["estado"] == "sin_fuentes"


def test_finalizar_aborto_estado_abortada() -> None:
    contexto = _contexto()
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida") as mock_update:
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                res = finalizar_proceso(contexto, "aborto")

    assert res.estado == "ok"
    campos = mock_update.call_args.args[1]
    assert campos["estado"] == "abortada"


def test_finalizar_metricas_consultadas_de_bd() -> None:
    contexto = _contexto()
    eventos = [
        {"run_id": "COR-0001", "tipo": "error", "source_id": "LI-01"},
        {"run_id": "COR-0001", "tipo": "suceso", "source_id": "LI-01"},
        {"run_id": "COR-0001", "tipo": "suceso", "source_id": "OTRA"},
    ]

    def _read_table_side(
        tabla: str, filtros: dict[str, Any] | None = None
    ) -> list[dict[str, Any]]:
        if tabla == "ofertas":
            return [{"id": "OFE-1"}, {"id": "OFE-2"}]
        return eventos

    with patch(
        "modules.discovery.nodes.finalizar.read_table", side_effect=_read_table_side
    ) as mock_read:
        with patch("modules.discovery.nodes.finalizar.actualizar_corrida") as mock_update:
            with patch("modules.discovery.nodes.finalizar.write_evento"):
                with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                    finalizar_proceso(contexto, "corrida_completada")

    assert mock_read.call_count == 4
    campos = mock_update.call_args.args[1]
    assert campos["total_ofertas"] == 2
    assert campos["total_errores"] == 1
    assert campos["total_sucesos"] == 2
    assert campos["fuentes_procesadas"] == 2


def test_finalizar_actualizar_corrida_campos_correctos() -> None:
    contexto = _contexto()
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida") as mock_update:
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                finalizar_proceso(contexto, "corrida_completada")

    args = mock_update.call_args.args
    assert args[0] == "COR-0001"
    campos = args[1]
    assert set(campos.keys()) == {
        "estado",
        "timestamp_fin",
        "motivo_terminacion",
        "total_ofertas",
        "total_errores",
        "total_sucesos",
        "fuentes_procesadas",
    }
    assert isinstance(campos["timestamp_fin"], str) and campos["timestamp_fin"]


def test_finalizar_actualizar_corrida_fallo_reintenta_y_continua() -> None:
    contexto = _contexto()
    with patch(
        "modules.discovery.nodes.finalizar.actualizar_corrida",
        side_effect=RuntimeError("db"),
    ) as mock_update:
        with patch("modules.discovery.nodes.finalizar.write_evento") as mock_evento:
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo") as mock_lock:
                with patch("modules.discovery.nodes.finalizar.logger"):
                    res = finalizar_proceso(contexto, "aborto")

    assert res.estado == "ok"
    assert mock_update.call_count == 2
    mock_evento.assert_called_once()
    mock_lock.assert_called_once()


def test_finalizar_playwright_sin_sesion_no_cierra() -> None:
    contexto = _contexto()
    contexto.handle_sesion = None
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida"):
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                res = finalizar_proceso(contexto, "motivo_no_definido")

    assert res.estado == "ok"


def test_finalizar_playwright_sesion_abierta_cierra() -> None:
    contexto = _contexto()
    pagina = MagicMock()
    contexto.handle_sesion = pagina
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida"):
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                res = finalizar_proceso(contexto, "corrida_completada")

    assert res.estado == "ok"
    pagina.close.assert_called_once()


def test_finalizar_playwright_browser_y_instance_cerrados() -> None:
    contexto = _contexto()
    browser = MagicMock()
    playwright_instance = MagicMock()
    setattr(contexto, "browser", browser)
    setattr(contexto, "playwright_instance", playwright_instance)
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida"):
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                finalizar_proceso(contexto, "corrida_completada")

    browser.close.assert_called_once()
    playwright_instance.stop.assert_called_once()


def test_finalizar_liberar_bloqueo_siempre() -> None:
    contexto = _contexto()
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida"):
        with patch("modules.discovery.nodes.finalizar.write_evento"):
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo") as mock_lock:
                finalizar_proceso(contexto, "corrida_completada")

    mock_lock.assert_called_once_with("COR-0001")


def test_finalizar_evento_tipo_suceso_completada() -> None:
    contexto = _contexto()
    with patch("modules.discovery.nodes.finalizar.actualizar_corrida"):
        with patch("modules.discovery.nodes.finalizar.write_evento") as mock_evento:
            with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                finalizar_proceso(contexto, "corrida_completada")

    datos = mock_evento.call_args.args[0]
    assert datos["tipo"] == "suceso"
    assert datos["codigo"] == "corrida_completada"
    assert "total_ofertas" in datos["evidencia"]


def test_finalizar_evento_tipo_error_para_no_completada() -> None:
    contexto = _contexto()
    for motivo, esperado in (("sin_fuentes", "error"), ("aborto", "error")):
        with patch("modules.discovery.nodes.finalizar.actualizar_corrida"):
            with patch("modules.discovery.nodes.finalizar.write_evento") as mock_evento:
                with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                    finalizar_proceso(contexto, motivo)
        datos = mock_evento.call_args.args[0]
        assert datos["tipo"] == esperado
        assert datos["codigo"] == motivo


def test_finalizar_metricas_fallan_a_ceros() -> None:
    contexto = _contexto()
    with patch(
        "modules.discovery.nodes.finalizar.read_table",
        side_effect=RuntimeError("db"),
    ):
        with patch("modules.discovery.nodes.finalizar.actualizar_corrida") as mock_update:
            with patch("modules.discovery.nodes.finalizar.write_evento"):
                with patch("modules.discovery.nodes.finalizar.liberar_bloqueo"):
                    with patch("modules.discovery.nodes.finalizar.logger"):
                        res = finalizar_proceso(contexto, "corrida_completada")

    assert res.estado == "ok"
    campos = mock_update.call_args.args[1]
    assert campos["total_ofertas"] == 0
    assert campos["total_errores"] == 0
    assert campos["total_sucesos"] == 0
    assert campos["fuentes_procesadas"] == 0


def test_finalizar_contexto_none_best_effort() -> None:
    with patch("modules.discovery.nodes.finalizar.liberar_bloqueo") as mock_lock:
        res = finalizar_proceso(None, "aborto")

    assert res.estado == "ok"
    assert res.contexto is None
    mock_lock.assert_not_called()


def test_consultar_metricas_contexto_none() -> None:
    metricas = consultar_metricas(None)
    assert metricas == {
        "total_ofertas": 0,
        "total_errores": 0,
        "total_sucesos": 0,
        "fuentes_procesadas": 0,
    }


def test_actualizar_corrida_bd_real(temp_db_file: Path) -> None:
    """End-to-end: write_corrida + actualizar_corrida persist closure data."""
    write_corrida(
        {
            "run_id": "COR-0001",
            "timestamp_inicio": "2026-08-10 10:00:00",
            "estado": "en_ejecucion",
        }
    )
    ok = actualizar_corrida(
        "COR-0001",
        {
            "estado": "completada",
            "timestamp_fin": "2026-08-10 10:05:00",
            "motivo_terminacion": "corrida_completada",
            "total_ofertas": 3,
            "total_errores": 1,
            "total_sucesos": 5,
            "fuentes_procesadas": 1,
        },
    )
    fila = read_table("corridas")[0]
    assert ok is True
    assert fila["estado"] == "completada"
    assert fila["motivo_terminacion"] == "corrida_completada"
    assert fila["total_ofertas"] == 3
    assert fila["total_sucesos"] == 5


def test_actualizar_corrida_sin_fila(temp_db_file: Path) -> None:
    ok = actualizar_corrida("COR-9999", {"estado": "abortada"})
    assert ok is False
