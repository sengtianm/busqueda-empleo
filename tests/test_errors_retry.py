from shared.errors import (
    BaseError,
    NetworkError,
    PersistenceError,
    Severity,
)
from shared.retry import retry_conditional, should_retry


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
    assert should_retry("timeout_ingreso") is True
    assert should_retry("timeout_consulta") is True
    assert should_retry("timeout_captura") is True


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


def test_retry_conditional_reintenta_hasta_limite() -> None:
    llamadas = 0

    @retry_conditional(max_reintentos=2, backoff_inicial=0.001)
    def _falla_reintentable() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("fuente_inalcanzable")

    try:
        _falla_reintentable()
    except _ErrorConCodigo:
        pass
    assert llamadas == 3


def test_retry_conditional_no_reintenta_no_reintentable() -> None:
    llamadas = 0

    @retry_conditional(max_reintentos=2, backoff_inicial=0.001)
    def _falla_bloqueo() -> None:
        nonlocal llamadas
        llamadas += 1
        raise _ErrorConCodigo("bloqueo_plataforma")

    try:
        _falla_bloqueo()
    except _ErrorConCodigo as e:
        assert e.codigo_motivo == "bloqueo_plataforma"
    assert llamadas == 1


def test_retry_conditional_exito_sin_reintento() -> None:
    llamadas = 0

    @retry_conditional(max_reintentos=2, backoff_inicial=0.001)
    def _exito() -> str:
        nonlocal llamadas
        llamadas += 1
        return "ok"

    assert _exito() == "ok"
    assert llamadas == 1


def test_retry_conditional_reintenta_y_exita() -> None:
    llamadas = 0

    @retry_conditional(max_reintentos=2, backoff_inicial=0.001)
    def _falla_una_vez() -> str:
        nonlocal llamadas
        llamadas += 1
        if llamadas == 1:
            raise _ErrorConCodigo("timeout_captura")
        return "ok"

    assert _falla_una_vez() == "ok"
    assert llamadas == 2


def test_retry_conditional_baseerror_con_code_no_reintenta() -> None:
    llamadas = 0

    @retry_conditional(max_reintentos=1, backoff_inicial=0.001)
    def _falla_network() -> None:
        nonlocal llamadas
        llamadas += 1
        raise NetworkError("05", message="Sin red")

    try:
        _falla_network()
    except NetworkError:
        pass
    assert llamadas == 1
