from unittest.mock import patch

import pytest

from shared.decision_engine import (
    _classify,
    _decide,
    _score_experience,
    _score_technology,
    evaluar,
)
from shared.errors import ConfigurationError
from shared.models import (
    DecisionEvaluation,
    EvaluationResult,
    ProcessedOffer,
    Profile,
)


def test_puntuar_experiencia_supera() -> None:
    perfil = Profile(experience_years=8)
    oferta = ProcessedOffer(offer_id="OFP-T1", clean_title="Test", experience_years=5)
    assert _score_experience(oferta, perfil) == 100.0


def test_puntuar_experiencia_parcial() -> None:
    perfil = Profile(experience_years=3)
    oferta = ProcessedOffer(offer_id="OFP-T2", clean_title="Test", experience_years=6)
    assert _score_experience(oferta, perfil) == 50.0


def test_puntuar_tecnologia_coincide() -> None:
    perfil = Profile(tecnologias={"Python": 5, "SQL": 4})
    oferta = ProcessedOffer(
        offer_id="OFP-T3", clean_title="Test", tecnologias=["Python", "SQL"]
    )
    puntaje = _score_technology(oferta, perfil)
    assert puntaje > 90.0


def test_clasificar_alta() -> None:
    assert _classify(90.0) == EvaluationResult.HIGH


def test_clasificar_media() -> None:
    assert _classify(65.0) == EvaluationResult.MEDIUM


def test_clasificar_baja() -> None:
    assert _classify(30.0) == EvaluationResult.LOW


def test_decidir_continuar() -> None:
    assert _decide(EvaluationResult.HIGH) == DecisionEvaluation.CONTINUE
    assert _decide(EvaluationResult.MEDIUM) == DecisionEvaluation.CONTINUE


def test_decidir_descartar() -> None:
    assert _decide(EvaluationResult.LOW) == DecisionEvaluation.DISCARD


def test_evaluar_alta(perfil_ejemplo: Profile) -> None:
    oferta = ProcessedOffer(
        offer_id="OFP-T4",
        clean_title="Data Engineer Senior",
        tecnologias=["Python", "SQL", "Spark"],
        experience_years=5,
        clean_location="Madrid",
        modalidad="remoto",
        idiomas=["Ingles"],
        salario_min=60000,
        salario_max=80000,
    )
    resultado = evaluar(oferta, perfil_ejemplo)
    assert resultado.resultado in (
        EvaluationResult.HIGH,
        EvaluationResult.MEDIUM,
    )
    assert resultado.decision == DecisionEvaluation.CONTINUE
    assert resultado.score > 50.0


def test_evaluar_baja(perfil_ejemplo: Profile) -> None:
    oferta = ProcessedOffer(
        offer_id="OFP-T5",
        clean_title="Junior Trainee",
        tecnologias=[],
        experience_years=0,
        clean_location="OtroPais",
        modalidad="presencial",
        idiomas=[],
    )
    resultado = evaluar(oferta, perfil_ejemplo)
    assert resultado.score < 50.0


def test_evaluar_excluida(perfil_ejemplo: Profile) -> None:
    oferta = ProcessedOffer(
        offer_id="OFP-T6",
        clean_title="Senior en EvilCorp",
        tecnologias=["Python"],
    )
    resultado = evaluar(oferta, perfil_ejemplo)
    assert resultado.score == 0.0
    assert resultado.decision == DecisionEvaluation.DISCARD


def test_pesos_validos_continua(perfil_ejemplo: Profile) -> None:
    oferta = ProcessedOffer(
        offer_id="OFP-T7",
        clean_title="Data Engineer",
        tecnologias=["Python"],
        experience_years=3,
    )
    config_valida = {
        "evaluation": {
            "weights": {"experiencia": 0.50, "tecnologia": 0.50},
            "high_compatibility_threshold": 80,
            "medium_compatibility_threshold": 50,
        },
        "profile": {},
    }
    with patch("shared.decision_engine.load", return_value=config_valida):
        resultado = evaluar(oferta, perfil_ejemplo)
        assert isinstance(resultado.score, float)
        assert resultado.resultado in EvaluationResult


def test_pesos_invalidos_lanza_error(perfil_ejemplo: Profile) -> None:
    oferta = ProcessedOffer(
        offer_id="OFP-T8",
        clean_title="Data Engineer",
        tecnologias=["Python"],
    )
    config_invalida = {
        "evaluation": {
            "weights": {"experiencia": 0.80, "tecnologia": 0.70},
        },
        "profile": {},
    }
    with patch("shared.decision_engine.load", return_value=config_invalida):
        with pytest.raises(ConfigurationError) as exc_info:
            evaluar(oferta, perfil_ejemplo)
    msg = str(exc_info.value)
    assert "sum=1.5" in msg
    assert "expected=1.0" in msg
    assert "config/config.yaml" in msg
