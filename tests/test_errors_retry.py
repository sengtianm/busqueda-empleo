from unittest.mock import patch

from shared.errors import (
    BaseError,
    NetworkError,
    PersistenceError,
    Severity,
)
from shared.retry import ejecutar_con_reintento, should_retry


def test_base_error_con_trazabilidad() -> None:
    err = NetworkError(
        "01",
        message="Fuente inalcanzable",
        run_id="COR-0001",
        source_id="linkedin",
        session_id="SES-0001",
        set_indice=0,
    )
    assert err.run_id == "COR-0001"
    assert err.source_id == "linkedin"
    assert err.session_id == "SES-0001"
    assert err.set_indice == 0
    d = err.to_dict()
    assert d["run_id"] == "COR-0001"
    assert d["set_indice"] == 0


def test_base_error_sin_trazabilidad() -> None:
    err = BaseError("ERR-01", "Mensaje")
    assert err.code == "ERR-01"
    assert err.run_id is None
    assert err.source_id is None
    assert err.session_id is None
    assert err.set_indice is None


def test_subclases_heredan_trazabilidad() -> None:
    err = NetworkError(
        "01",
        message="Sin conexion",
        run_id="COR-0001",
        set_indice=2,
    )
    assert err.code == "ER-RED-01"
    assert err.run_id == "COR-0001"
    assert err.set_indice == 2

    err_db = PersistenceError("10", message="Error BD", source_id="local")
    assert err_db.code == "ER-DB-10"
    assert err_db.source_id == "local"


def test_jerarquia_y_severidades_intactas() -> None:
    err = NetworkError("01", message="x")
    assert isinstance(err, BaseError)
    assert err.severity == Severity.MEDIUM
    assert NetworkError("07", message="x").code == "ER-RED-07"


def test_should_retry_reintentables() -> None:
    assert should_retry("fuente_inalcanzable") is True
    assert should_retry("tiempo_agotado_ingreso") is True
    assert should_retry("tiempo_agotado_consulta") is True
    assert should_retry("tiempo_agotado_captura") is True


def test_should_retry_no_reintentables() -> None:
    assert should_retry("bloqueo_plataforma") is False
    assert should_retry("autenticacion_rechazada") is False
    assert should_retry("credenciales_no_disponibles") is False
    assert should_retry("criterio_no_cumplido") is False
    assert should_retry("sesion_expirada") is False
    assert should_retry("") is False


class _ErrorConCodigo(Exception):
    def __init__(self, codigo_motivo: str) -> None:
        self.codigo_motivo = codigo_motivo
        super().__init__(codigo_motivo)


def test_ejecutar_con_reintento_reintenta_hasta_limite() -> None:
    llamadas = 0

    def _falla_reintentable() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("fuente_inalcanzable")

    try:
        ejecutar_con_reintento(
            _falla_reintentable,
            max_attempts=3,
            base_wait=0.001,
            multiplier=1,
        )
    except _ErrorConCodigo:
        pass
    assert llamadas == 3


def test_ejecutar_con_reintento_no_reintenta_no_reintentable() -> None:
    llamadas = 0

    def _falla_bloqueo() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("bloqueo_plataforma")

    try:
        ejecutar_con_reintento(
            _falla_bloqueo,
            max_attempts=3,
            base_wait=0.001,
            multiplier=1,
        )
    except _ErrorConCodigo as e:
        assert e.codigo_motivo == "bloqueo_plataforma"
    assert llamadas == 1


def test_ejecutar_con_reintento_exito_sin_reintento() -> None:
    llamadas = 0

    def _exito() -> str:
        nonlocal llamadas
        llamadas += 1
        return "ok"

    resultado, intentos = ejecutar_con_reintento(
        _exito, max_attempts=3, base_wait=0.001, multiplier=1
    )
    assert resultado == "ok"
    assert intentos == 1
    assert llamadas == 1


def test_ejecutar_con_reintento_reintenta_y_exita() -> None:
    llamadas = 0

    def _falla_una_vez() -> str:
        nonlocal llamadas
        llamadas += 1
        if llamadas == 1:
            raise _ErrorConCodigo("tiempo_agotado_captura")
        return "ok"

    resultado, intentos = ejecutar_con_reintento(
        _falla_una_vez, max_attempts=3, base_wait=0.001, multiplier=1
    )
    assert resultado == "ok"
    assert intentos == 2
    assert llamadas == 2


def test_ejecutar_con_reintento_baseerror_no_reintenta() -> None:
    llamadas = 0

    def _falla_network() -> None:
        nonlocal llamadas
        llamadas += 1
        raise NetworkError("05", message="Sin red")

    try:
        ejecutar_con_reintento(
            _falla_network,
            max_attempts=3,
            base_wait=0.001,
            multiplier=1,
        )
    except NetworkError:
        pass
    assert llamadas == 1


def test_ejecutar_con_reintento_fallo_final_recibe_contexto() -> None:
    llamadas = 0
    capturado: list[tuple[BaseException, int]] = []

    def _falla() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("tiempo_agotado_ingreso")

    def _al_fallo_final(exc: BaseException, intentos: int) -> str:
        capturado.append((exc, intentos))
        return "fallo"

    resultado, intentos = ejecutar_con_reintento(
        _falla,
        al_fallo_final=_al_fallo_final,
        max_attempts=2,
        base_wait=0.001,
        multiplier=1,
    )
    assert resultado == "fallo"
    assert intentos == 2
    assert llamadas == 2
    exc, num = capturado[0]
    assert isinstance(exc, _ErrorConCodigo)
    assert num == 2


def test_ejecutar_con_reintento_error_interno_rellanza() -> None:
    llamadas = 0

    def _falla_generica() -> None:
        nonlocal llamadas
        llamadas += 1
        raise ValueError("boom")

    try:
        ejecutar_con_reintento(
            _falla_generica,
            max_attempts=3,
            base_wait=0.001,
            multiplier=1,
        )
    except ValueError:
        pass
    assert llamadas == 1


def test_ejecutar_con_reintento_error_interno_con_callback() -> None:
    def _falla_generica() -> None:
        raise ValueError("boom")

    def _al_error_interno(exc: Exception, intentos: int) -> str:
        assert isinstance(exc, ValueError)
        assert intentos == 1
        return f"interno:{exc}"

    resultado, intentos = ejecutar_con_reintento(
        _falla_generica,
        al_error_interno=_al_error_interno,
        max_attempts=3,
        base_wait=0.001,
        multiplier=1,
    )
    assert resultado == "interno:boom"
    assert intentos == 1


def test_ejecutar_con_reintento_al_reintento_se_invoca() -> None:
    llamadas = 0
    limpiezas = 0

    def _falla_una_vez() -> str:
        nonlocal llamadas
        llamadas += 1
        if llamadas == 1:
            raise _ErrorConCodigo("fuente_inalcanzable")
        return "ok"

    def _limpiar() -> None:
        nonlocal limpiezas
        limpiezas += 1

    resultado, intentos = ejecutar_con_reintento(
        _falla_una_vez,
        al_reintento=_limpiar,
        max_attempts=3,
        base_wait=0.001,
        multiplier=1,
    )
    assert resultado == "ok"
    assert intentos == 2
    assert limpiezas == 1


def test_ejecutar_con_reintento_sin_intentos_configurados() -> None:
    def _nunca_llamada() -> None:
        raise AssertionError("no debería llamarse")

    try:
        ejecutar_con_reintento(_nunca_llamada, max_attempts=0)
    except RuntimeError as e:
        assert str(e) == "no attempts configured"


def test_ejecutar_con_reintento_sin_intentos_con_callback() -> None:
    def _nunca_llamada() -> None:
        raise AssertionError("no debería llamarse")

    def _al_error_interno(exc: Exception, intentos: int) -> str:
        assert isinstance(exc, RuntimeError)
        assert intentos == 0
        return "sin intentos"

    resultado, intentos = ejecutar_con_reintento(
        _nunca_llamada,
        al_error_interno=_al_error_interno,
        max_attempts=0,
    )
    assert resultado == "sin intentos"
    assert intentos == 0


def test_ejecutar_con_reintento_backoff_exponencial() -> None:
    llamadas = 0

    def _falla() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("fuente_inalcanzable")

    with patch("shared.retry.time.sleep") as mock_sleep:
        try:
            ejecutar_con_reintento(
                _falla, max_attempts=3, base_wait=2, multiplier=2, max_wait=30
            )
        except _ErrorConCodigo:
            pass

    waits = [call.args[0] for call in mock_sleep.call_args_list]
    assert waits == [2.0, 4.0]


def test_ejecutar_con_reintento_backoff_con_tope_max_wait() -> None:
    llamadas = 0

    def _falla() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("fuente_inalcanzable")

    with patch("shared.retry.time.sleep") as mock_sleep:
        try:
            ejecutar_con_reintento(
                _falla, max_attempts=3, base_wait=2, multiplier=10, max_wait=5
            )
        except _ErrorConCodigo:
            pass

    waits = [call.args[0] for call in mock_sleep.call_args_list]
    assert waits == [2.0, 5.0]
