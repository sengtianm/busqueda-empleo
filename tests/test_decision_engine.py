from unittest.mock import patch

import pytest

from shared.decision_engine import (
    _classify,
    _decide,
    _score_experience,
    _score_technology,
    evaluate,
    load_profile,
)
from shared.errors import ConfigurationError
from shared.models import (
    DecisionEvaluation,
    EvaluationResult,
    ProcessedOffer,
    Profile,
)


def test_score_experience_exceeds() -> None:
    profile = Profile(anos_experiencia=8)
    offer = ProcessedOffer(id_oferta="OFP-T1", titulo_limpio="Test", anos_experiencia=5)
    assert _score_experience(offer, profile) == 100.0


def test_score_experience_partial() -> None:
    profile = Profile(anos_experiencia=3)
    offer = ProcessedOffer(id_oferta="OFP-T2", titulo_limpio="Test", anos_experiencia=6)
    assert _score_experience(offer, profile) == 50.0


def test_score_technology_match() -> None:
    profile = Profile(tecnologias={"Python": 5, "SQL": 4})
    offer = ProcessedOffer(
        id_oferta="OFP-T3", titulo_limpio="Test", tecnologias=["Python", "SQL"]
    )
    score = _score_technology(offer, profile)
    assert score > 90.0


def test_classify_high() -> None:
    assert _classify(90.0) == EvaluationResult.HIGH


def test_classify_medium() -> None:
    assert _classify(65.0) == EvaluationResult.MEDIUM


def test_classify_low() -> None:
    assert _classify(30.0) == EvaluationResult.LOW


def test_decide_continue() -> None:
    assert _decide(EvaluationResult.HIGH) == DecisionEvaluation.CONTINUE
    assert _decide(EvaluationResult.MEDIUM) == DecisionEvaluation.CONTINUE


def test_decide_discard() -> None:
    assert _decide(EvaluationResult.LOW) == DecisionEvaluation.DISCARD


def test_evaluate_high(example_profile: Profile) -> None:
    offer = ProcessedOffer(
        id_oferta="OFP-T4",
        titulo_limpio="Data Engineer Senior",
        tecnologias=["Python", "SQL", "Spark"],
        anos_experiencia=5,
        ubicacion_limpia="Madrid",
        modalidad="remoto",
        idiomas=["Ingles"],
        salario_min=60000,
        salario_max=80000,
    )
    result = evaluate(offer, example_profile)
    assert result.resultado in (
        EvaluationResult.HIGH,
        EvaluationResult.MEDIUM,
    )
    assert result.decision == DecisionEvaluation.CONTINUE
    assert result.score > 50.0


def test_evaluate_low(example_profile: Profile) -> None:
    offer = ProcessedOffer(
        id_oferta="OFP-T5",
        titulo_limpio="Junior Trainee",
        tecnologias=[],
        anos_experiencia=0,
        ubicacion_limpia="OtroPais",
        modalidad="presencial",
        idiomas=[],
    )
    result = evaluate(offer, example_profile)
    assert result.score < 50.0


def test_evaluate_excluded(example_profile: Profile) -> None:
    offer = ProcessedOffer(
        id_oferta="OFP-T6",
        titulo_limpio="Senior en EvilCorp",
        tecnologias=["Python"],
    )
    result = evaluate(offer, example_profile)
    assert result.score == 0.0
    assert result.decision == DecisionEvaluation.DISCARD


def test_valid_weights_continue(example_profile: Profile) -> None:
    offer = ProcessedOffer(
        id_oferta="OFP-T7",
        titulo_limpio="Data Engineer",
        tecnologias=["Python"],
        anos_experiencia=3,
    )
    valid_config = {
        "evaluation": {
            "weights": {"experiencia": 0.50, "tecnologia": 0.50},
            "high_compatibility_threshold": 80,
            "medium_compatibility_threshold": 50,
        },
        "profile": {},
    }
    with patch("shared.decision_engine.load", return_value=valid_config):
        result = evaluate(offer, example_profile)
        assert isinstance(result.score, float)
        assert result.resultado in EvaluationResult


def test_load_profile_warns_if_incomplete() -> None:
    config: dict[str, object] = {"profile": {}}
    with patch("shared.decision_engine.load", return_value=config), patch(
        "shared.decision_engine.logger.warning"
    ) as mock_warning:
        profile = load_profile()
    assert profile.tecnologias == {}
    mock_warning.assert_called_once()


def test_invalid_weights_raise(example_profile: Profile) -> None:
    offer = ProcessedOffer(
        id_oferta="OFP-T8",
        titulo_limpio="Data Engineer",
        tecnologias=["Python"],
    )
    invalid_config = {
        "evaluation": {
            "weights": {"experiencia": 0.80, "tecnologia": 0.70},
        },
        "profile": {},
    }
    with patch("shared.decision_engine.load", return_value=invalid_config):
        with pytest.raises(ConfigurationError) as exc_info:
            evaluate(offer, example_profile)
    message = str(exc_info.value)
    assert "sum=1.5" in message
    assert "expected=1.0" in message
    assert "config/config.yaml" in message
