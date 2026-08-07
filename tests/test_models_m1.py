from datetime import datetime, timezone

from shared.models import (
    AuditoriaSesion,
    CaptureBatch,
    Corrida,
    EntryResult,
    EstadoCaptura,
    EstadoCorrida,
    EventoAlmacen,
    FichaFuente,
    GrupoCodigo,
    Offer,
    PoliticasCaptura,
    SearchResult,
    SetFiltros,
    TipoEvento,
)


def test_offer_trazabilidad_opcional(example_offer: Offer) -> None:
    assert example_offer.run_id is None
    assert example_offer.session_id is None
    assert example_offer.set_indice is None
    assert example_offer.id_externo_url is None


def test_offer_trazabilidad_completa() -> None:
    offer = Offer(
        url="https://www.linkedin.com/jobs/view/123",
        titulo="Data Engineer",
        descripcion_original="Descripcion",
        run_id="COR-0001",
        session_id="SES-0001",
        set_indice=0,
        id_externo_url="123",
    )
    assert offer.run_id == "COR-0001"
    assert offer.session_id == "SES-0001"
    assert offer.set_indice == 0
    assert offer.id_externo_url == "123"


def test_corrida_estado_por_defecto() -> None:
    corrida = Corrida(run_id="COR-0001")
    assert corrida.estado == EstadoCorrida.EN_EJECUCION
    corrida = Corrida(run_id="COR-0002", estado=EstadoCorrida.COMPLETADA)
    assert corrida.estado == EstadoCorrida.COMPLETADA


def test_evento_almacen() -> None:
    evento = EventoAlmacen(
        run_id="COR-0001",
        tipo=TipoEvento.ERROR,
        codigo="ERR-05",
        evidencia="evidencia",
    )
    assert evento.tipo == TipoEvento.ERROR
    assert evento.codigo == "ERR-05"
    assert evento.offer_id is None


def test_auditoria_sesion_minima() -> None:
    auditoria = AuditoriaSesion(
        session_id="SES-0001",
        run_id="COR-0001",
        source_id="linkedin",
        set_indice=0,
        timestamp=datetime(2026, 8, 7, tzinfo=timezone.utc),
        total_declarado=37,
        conteo=25,
        estado="activa",
    )
    assert auditoria.session_id == "SES-0001"
    assert auditoria.run_id == "COR-0001"
    assert auditoria.source_id == "linkedin"
    assert auditoria.set_indice == 0
    assert auditoria.total_declarado == 37
    assert auditoria.conteo == 25
    assert auditoria.estado == "activa"


def test_politicas_captura_defaults() -> None:
    politicas = PoliticasCaptura()
    assert politicas.max_paginas == 5
    assert politicas.max_ofertas_por_corrida == 25
    assert politicas.pausa_entre_lotes_segundos == 10
    assert politicas.estrategia_anti_bloqueo == "pausa_aleatoria"


def test_ficha_fuente_linkedin() -> None:
    ficha = FichaFuente(
        source_id="linkedin",
        nombre="LinkedIn",
        url="https://www.linkedin.com/jobs/search",
        tipo_acceso="con_autenticacion",
        credenciales_referencia=["LINKEDIN_EMAIL", "LINKEDIN_PASSWORD"],
        criterio_exito="global-nav",
        timeout_segundos=30,
    )
    assert ficha.source_id == "linkedin"
    assert ficha.tipo_acceso == "con_autenticacion"
    assert "LINKEDIN_EMAIL" in ficha.credenciales_referencia
    assert ficha.criterio_exito == "global-nav"


def test_set_filtros() -> None:
    set_filtros = SetFiltros(
        source_id="linkedin",
        indice=0,
        filtros=[{"tipo": "keywords", "valor": ["Data Engineer"]}],
    )
    assert set_filtros.indice == 0
    assert set_filtros.filtros[0]["tipo"] == "keywords"


def test_entry_result() -> None:
    resultado = EntryResult(
        estado="exito",
        codigo_motivo="",
        evidencia_acotada="nav visible",
    )
    assert resultado.estado == "exito"
    assert resultado.numero_de_intentos == 0


def test_search_result() -> None:
    resultado = SearchResult(
        estado="exito",
        codigo_motivo="",
        ofertas_primera_pagina=[],
        estado_paginacion="inicial",
        total_declarado=37,
        set_indice=0,
    )
    assert resultado.total_declarado == 37
    assert resultado.set_indice == 0


def test_capture_batch() -> None:
    ofertas = [
        Offer(url="https://x.com/1", titulo="Oferta 1", descripcion_original="d1"),
    ]
    lote = CaptureBatch(
        ofertas=ofertas,
        run_id="COR-0001",
        source_id="linkedin",
        session_id="SES-0001",
        set_indice=0,
        paginas_consumidas=1,
    )
    assert len(lote.ofertas) == 1
    assert lote.paginas_consumidas == 1


def test_estado_captura() -> None:
    estado = EstadoCaptura(
        estado="completa",
        codigo_motivo="",
        paginas_consumidas=3,
        capturadas_acumuladas_fuente=25,
        limite_alcanzado=False,
    )
    assert estado.capturadas_acumuladas_fuente == 25
    assert estado.limite_alcanzado is False


def test_enums() -> None:
    assert GrupoCodigo.GRUPO_A.value == "grupo_a"
    assert GrupoCodigo.GRUPO_B.value == "grupo_b"
    assert TipoEvento.ERROR.value == "error"
    assert TipoEvento.SUCESO.value == "suceso"
    assert EstadoCorrida.EN_EJECUCION.value == "en_ejecucion"
    assert EstadoCorrida.COMPLETADA.value == "completada"
    assert EstadoCorrida.ERROR.value == "error"
    assert EstadoCorrida.CONCURRENCIA.value == "concurrencia"
