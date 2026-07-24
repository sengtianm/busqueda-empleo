from unittest.mock import patch
from uuid import uuid4

import pytest

from shared.decision_engine import (
    _clasificar,
    _decidir,
    _puntuar_experiencia,
    _puntuar_tecnologia,
    evaluar,
)
from shared.errors import ErrorConfiguracion
from shared.models import (
    DecisionEvaluacion,
    OfertaProcesada,
    Perfil,
    ResultadoEvaluacion,
)


def test_puntuar_experiencia_supera() -> None:
    perfil = Perfil(experiencia_anios=8)
    oferta = OfertaProcesada(oferta_id=uuid4(), titulo_limpio="Test", experiencia_anios=5)
    assert _puntuar_experiencia(oferta, perfil) == 100.0


def test_puntuar_experiencia_parcial() -> None:
    perfil = Perfil(experiencia_anios=3)
    oferta = OfertaProcesada(oferta_id=uuid4(), titulo_limpio="Test", experiencia_anios=6)
    assert _puntuar_experiencia(oferta, perfil) == 50.0


def test_puntuar_tecnologia_coincide() -> None:
    perfil = Perfil(tecnologias={"Python": 5, "SQL": 4})
    oferta = OfertaProcesada(
        oferta_id=uuid4(), titulo_limpio="Test", tecnologias=["Python", "SQL"]
    )
    puntaje = _puntuar_tecnologia(oferta, perfil)
    assert puntaje > 90.0


def test_clasificar_alta() -> None:
    assert _clasificar(90.0) == ResultadoEvaluacion.ALTA


def test_clasificar_media() -> None:
    assert _clasificar(65.0) == ResultadoEvaluacion.MEDIA


def test_clasificar_baja() -> None:
    assert _clasificar(30.0) == ResultadoEvaluacion.BAJA


def test_decidir_continuar() -> None:
    assert _decidir(ResultadoEvaluacion.ALTA) == DecisionEvaluacion.CONTINUAR
    assert _decidir(ResultadoEvaluacion.MEDIA) == DecisionEvaluacion.CONTINUAR


def test_decidir_descartar() -> None:
    assert _decidir(ResultadoEvaluacion.BAJA) == DecisionEvaluacion.DESCARTAR


def test_evaluar_alta(perfil_ejemplo: Perfil) -> None:
    oferta = OfertaProcesada(
        oferta_id=uuid4(),
        titulo_limpio="Data Engineer Senior",
        tecnologias=["Python", "SQL", "Spark"],
        experiencia_anios=5,
        ubicacion_limpia="Madrid",
        modalidad="remoto",
        idiomas=["Ingles"],
        salario_min=60000,
        salario_max=80000,
    )
    resultado = evaluar(oferta, perfil_ejemplo)
    assert resultado.resultado in (
        ResultadoEvaluacion.ALTA,
        ResultadoEvaluacion.MEDIA,
    )
    assert resultado.decision == DecisionEvaluacion.CONTINUAR
    assert resultado.puntaje > 50.0


def test_evaluar_baja(perfil_ejemplo: Perfil) -> None:
    oferta = OfertaProcesada(
        oferta_id=uuid4(),
        titulo_limpio="Junior Trainee",
        tecnologias=[],
        experiencia_anios=0,
        ubicacion_limpia="OtroPais",
        modalidad="presencial",
        idiomas=[],
    )
    resultado = evaluar(oferta, perfil_ejemplo)
    assert resultado.puntaje < 50.0


def test_evaluar_excluida(perfil_ejemplo: Perfil) -> None:
    oferta = OfertaProcesada(
        oferta_id=uuid4(),
        titulo_limpio="Senior en EvilCorp",
        tecnologias=["Python"],
    )
    resultado = evaluar(oferta, perfil_ejemplo)
    assert resultado.puntaje == 0.0
    assert resultado.decision == DecisionEvaluacion.DESCARTAR


def test_pesos_validos_continua(perfil_ejemplo: Perfil) -> None:
    oferta = OfertaProcesada(
        oferta_id=uuid4(),
        titulo_limpio="Data Engineer",
        tecnologias=["Python"],
        experiencia_anios=3,
    )
    config_valida = {
        "evaluacion": {
            "pesos": {"experiencia": 0.50, "tecnologia": 0.50},
            "umbral_compatibilidad_alta": 80,
            "umbral_compatibilidad_media": 50,
        },
        "perfil": {},
    }
    with patch("shared.decision_engine.cargar", return_value=config_valida):
        resultado = evaluar(oferta, perfil_ejemplo)
        assert isinstance(resultado.puntaje, float)
        assert resultado.resultado in ResultadoEvaluacion


def test_pesos_invalidos_lanza_error(perfil_ejemplo: Perfil) -> None:
    oferta = OfertaProcesada(
        oferta_id=uuid4(),
        titulo_limpio="Data Engineer",
        tecnologias=["Python"],
    )
    config_invalida = {
        "evaluacion": {
            "pesos": {"experiencia": 0.80, "tecnologia": 0.70},
        },
        "perfil": {},
    }
    with patch("shared.decision_engine.cargar", return_value=config_invalida):
        with pytest.raises(ErrorConfiguracion) as exc_info:
            evaluar(oferta, perfil_ejemplo)
    msg = str(exc_info.value)
    assert "suma=1.5" in msg
    assert "esperado=1.0" in msg
    assert "config/config.yaml" in msg
