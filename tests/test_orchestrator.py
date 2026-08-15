from types import SimpleNamespace
from typing import Any
from unittest.mock import MagicMock, patch

from modules.discovery.nodes.busqueda import ResultadoBusqueda
from modules.discovery.nodes.captura import ResultadoCaptura
from modules.discovery.nodes.control_fuentes import ResultadoControlFuentes
from modules.discovery.nodes.ingreso import ResultadoIngreso
from modules.discovery.nodes.inicio import ResultadoInicio
from modules.discovery.orchestrator import ejecutar_flujo
from modules.discovery.run_context import RunContext

_METRICAS = {
    "total_ofertas": 2,
    "total_errores": 1,
    "total_sucesos": 4,
    "fuentes_procesadas": 1,
}


def _contexto(n_fuentes: int = 1) -> RunContext:
    config_fuentes = [
        {
            "fuente_id": f"LI-0{i}",
            "nombre": "LinkedIn",
            "ficha_acceso": {
                "enlace": "https://www.linkedin.com/jobs",
                "tipo_acceso": "publico",
                "criterio_exito": "global-nav",
                "timeout_segundos": 10,
            },
            "sets_de_filtros": [{"indice_set": 0, "filtros": []}],
        }
        for i in range(n_fuentes)
    ]
    return RunContext(config_fuentes=config_fuentes)


def _res_ctrl(decision: str = "") -> ResultadoControlFuentes:
    return ResultadoControlFuentes(estado="ok", decision=decision)


def _res_busq(decision: str = "") -> ResultadoBusqueda:
    return ResultadoBusqueda(estado="ok", decision=decision)


def _res_capt(decision: str = "") -> ResultadoCaptura:
    return ResultadoCaptura(estado="ok", decision=decision)


def _res_ing(decision: str = "") -> ResultadoIngreso:
    return ResultadoIngreso(estado="ok", decision=decision)


def _rastrear(orden: list[str], nombre: str, ret: Any) -> Any:
    def _side(*args: Any, **kwargs: Any) -> Any:
        orden.append(nombre)
        return ret

    return _side


def _secuencia(orden: list[str], nombre: str, rets: list[Any]) -> Any:
    def _side(*args: Any, **kwargs: Any) -> Any:
        orden.append(nombre)
        return rets.pop(0)

    return _side


def test_flujo_completo_exitoso_finaliza_completada() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch(
            "modules.discovery.orchestrator.aplicar_filtros",
            return_value=_res_busq(),
        ),
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            return_value=_res_capt("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ) as mock_final,
    ):
        ejecutar_flujo()

    mock_final.assert_called_once()
    assert mock_final.call_args.args[1] == "corrida_completada"


def test_inicio_falla_no_ejecuta_finalizar(capsys: Any) -> None:
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="error", codigo="ERR-05", descripcion="database unavailable"
            ),
        ),
        patch("modules.discovery.orchestrator.finalizar_proceso") as mock_final,
    ):
        ejecutar_flujo()

    mock_final.assert_not_called()
    salida = capsys.readouterr().out
    assert "INICIO" in salida


def test_inicio_concurrencia_no_ejecuta_finalizar() -> None:
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="concurrencia", codigo="ERR-06"
            ),
        ),
        patch("modules.discovery.orchestrator.finalizar_proceso") as mock_final,
    ):
        ejecutar_flujo()

    mock_final.assert_not_called()


def test_sin_fuentes_finaliza_con_sin_fuentes() -> None:
    contexto = _contexto()
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("no"),
        ),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ) as mock_final,
    ):
        ejecutar_flujo()

    mock_final.assert_called_once()
    assert mock_final.call_args.args[1] == "sin_fuentes"


def test_ingreso_falla_registra_evento_y_sigue_fuente_siguiente() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento") as mock_evento,
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ) as mock_final,
    ):
        ejecutar_flujo()

    assert mock_evento.call_count == 2
    mock_evento.assert_called_with(contexto)
    assert mock_final.call_args.args[1] == "corrida_completada"
    assert mock_evento.call_args_list[1].args[0] is contexto


def test_busqueda_sin_ofertas_registra_evento_y_sigue_set() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch("modules.discovery.orchestrator.aplicar_filtros") as mock_filtros,
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            side_effect=[_res_busq("no"), _res_busq("si")],
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            side_effect=[_res_capt("si"), _res_capt("no")],
        ),
        patch("modules.discovery.orchestrator.registrar_evento") as mock_evento,
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ),
    ):
        ejecutar_flujo()

    assert mock_filtros.call_count == 2
    assert mock_evento.call_count == 1
    mock_evento.assert_called_with(contexto)


def test_error_nodo_aborta_con_aborto() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch(
            "modules.discovery.orchestrator.aplicar_filtros",
            return_value=_res_busq(),
        ),
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=ResultadoCaptura(
                estado="error", codigo="ERR-07", descripcion="internal failure"
            ),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            return_value=_res_capt("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ) as mock_final,
    ):
        ejecutar_flujo()

    mock_final.assert_called_once()
    assert mock_final.call_args.args[1] == "aborto"


def test_bucle_fuentes_dos_fuentes_secuenciales() -> None:
    contexto = _contexto(n_fuentes=2)
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ) as mock_seleccion,
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch("modules.discovery.orchestrator.aplicar_filtros") as mock_filtros,
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            return_value=_res_capt("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ) as mock_final,
    ):
        ejecutar_flujo()

    assert mock_seleccion.call_count == 2
    assert mock_filtros.call_count == 2
    assert mock_final.call_args.args[1] == "corrida_completada"


def test_bucle_sets_dos_sets_para_una_fuente() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch("modules.discovery.orchestrator.aplicar_filtros") as mock_filtros,
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            side_effect=[_res_capt("si"), _res_capt("no")],
        ) as mock_sets,
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ),
    ):
        ejecutar_flujo()

    assert mock_filtros.call_count == 2
    assert mock_sets.call_count == 2


def test_sesion_anterior_cerrada_al_cambiar_fuente() -> None:
    contexto = _contexto(n_fuentes=2)
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    contexto.handle_sesion = MagicMock()
    contexto.id_sesion = "SES-0001"
    with (
        patch(
            "modules.discovery.orchestrator.cerrar_recursos",
            return_value=None,
        ) as mock_cerrar,
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch(
            "modules.discovery.orchestrator.aplicar_filtros",
            return_value=_res_busq(),
        ),
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            return_value=_res_capt("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ),
    ):
        ejecutar_flujo()

    assert mock_cerrar.call_count == 2
    assert all(call.args[0] is contexto for call in mock_cerrar.call_args_list)
    assert contexto.id_sesion is None


def test_logging_informativo_en_hitos() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    contexto.capture_batch = MagicMock()
    contexto.capture_batch.ofertas = [1, 2, 3]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch(
            "modules.discovery.orchestrator.aplicar_filtros",
            return_value=_res_busq(),
        ),
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            return_value=_res_capt("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ),
        patch("modules.discovery.orchestrator.logger") as mock_logger,
    ):
        ejecutar_flujo()

    mensajes = [str(c.args[0]) for c in mock_logger.info.call_args_list]
    assert any("iniciada" in m for m in mensajes)
    assert any("Procesando fuente" in m for m in mensajes)
    assert any("Ingreso exitoso" in m for m in mensajes)
    assert any("Capturadas 3" in m for m in mensajes)
    assert any("Corrida finalizada" in m for m in mensajes)


def test_metricas_en_mensaje_final() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            return_value=ResultadoInicio(
                estado="ok", id_corrida=contexto.id_corrida, contexto=contexto
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            return_value=_res_ctrl("si"),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=[_res_ctrl("si"), _res_ctrl("no")],
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            return_value=_res_ctrl(),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            return_value=_res_ing(),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            return_value=_res_ing("si"),
        ),
        patch(
            "modules.discovery.orchestrator.aplicar_filtros",
            return_value=_res_busq(),
        ),
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            return_value=_res_busq("si"),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            return_value=_res_capt(),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            return_value=_res_capt("no"),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            return_value=SimpleNamespace(metricas=_METRICAS),
        ),
        patch("modules.discovery.orchestrator.logger") as mock_logger,
    ):
        ejecutar_flujo()

    mensajes = [str(c.args[0]) for c in mock_logger.info.call_args_list]
    final = next(m for m in mensajes if "Corrida finalizada" in m)
    assert "total_ofertas=2" in final
    assert "total_errores=1" in final
    assert "total_sucesos=4" in final
    assert "fuentes_procesadas=1" in final


def test_orden_llamadas_nodos() -> None:
    contexto = _contexto()
    contexto.fuente_corriente = contexto.fuentes_filtradas[0]
    orden: list[str] = []
    with (
        patch(
            "modules.discovery.orchestrator.ejecutar_inicio",
            side_effect=_rastrear(
                orden,
                "inicio",
                ResultadoInicio(estado="ok", id_corrida=contexto.id_corrida, contexto=contexto),
            ),
        ),
        patch(
            "modules.discovery.orchestrator.existen_fuentes_configuradas",
            side_effect=_rastrear(orden, "existen", _res_ctrl("si")),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_fuentes_por_procesar",
            side_effect=_secuencia(
                orden, "quedan_fuentes", [_res_ctrl("si"), _res_ctrl("no")]
            ),
        ),
        patch(
            "modules.discovery.orchestrator.seleccionar_fuente_pendiente",
            side_effect=_rastrear(orden, "seleccionar", _res_ctrl()),
        ),
        patch(
            "modules.discovery.orchestrator.ejecutar_ingreso",
            side_effect=_rastrear(orden, "ingreso", _res_ing()),
        ),
        patch(
            "modules.discovery.orchestrator.ingreso_exitoso",
            side_effect=_rastrear(orden, "ingreso_exitoso", _res_ing("si")),
        ),
        patch(
            "modules.discovery.orchestrator.aplicar_filtros",
            side_effect=_rastrear(orden, "aplicar_filtros", _res_busq()),
        ),
        patch(
            "modules.discovery.orchestrator.se_encontraron_ofertas",
            side_effect=_rastrear(orden, "se_encontraron", _res_busq("si")),
        ),
        patch(
            "modules.discovery.orchestrator.capturar_ofertas",
            side_effect=_rastrear(orden, "capturar", _res_capt()),
        ),
        patch(
            "modules.discovery.orchestrator.registrar_ofertas",
            side_effect=_rastrear(orden, "registrar_ofertas", _res_capt()),
        ),
        patch(
            "modules.discovery.orchestrator.quedan_sets_por_aplicar",
            side_effect=_rastrear(orden, "quedan_sets", _res_capt("no")),
        ),
        patch("modules.discovery.orchestrator.registrar_evento"),
        patch(
            "modules.discovery.orchestrator.finalizar_proceso",
            side_effect=_rastrear(orden, "finalizar", SimpleNamespace(metricas=_METRICAS)),
        ),
    ):
        ejecutar_flujo()

    assert orden == [
        "inicio",
        "existen",
        "quedan_fuentes",
        "seleccionar",
        "ingreso",
        "ingreso_exitoso",
        "aplicar_filtros",
        "se_encontraron",
        "capturar",
        "registrar_ofertas",
        "quedan_sets",
        "quedan_fuentes",
        "finalizar",
    ]
