import math

from loguru import logger
from rapidfuzz import fuzz

from shared.config import load
from shared.errors import ConfigurationError
from shared.models import (
    DecisionEvaluation,
    Evaluation,
    EvaluationResult,
    ProcessedOffer,
    Profile,
)


def load_profile() -> Profile:
    config = load()
    data = config.get("profile", {})
    profile = Profile(**data)
    _warn_if_incomplete(profile)
    return profile


def _warn_if_incomplete(profile: Profile) -> None:
    missing: list[str] = []
    if not profile.tecnologias:
        missing.append("tecnologias")
    if profile.experience_years <= 0:
        missing.append("experience_years")
    if not profile.seniority:
        missing.append("seniority")
    if not profile.ubicaciones_preferidas:
        missing.append("ubicaciones_preferidas")
    if not profile.modalidades_preferidas:
        missing.append("modalidades_preferidas")
    if profile.salario_minimo is None:
        missing.append("salario_minimo")
    if missing:
        logger.warning(
            "Profile is incomplete; evaluation results may be misleading. "
            "Missing keys: {}",
            ", ".join(missing),
        )


def _score_experience(offer: ProcessedOffer, profile: Profile) -> float:
    if offer.experience_years is None or offer.experience_years == 0:
        return 100.0
    ratio = profile.experience_years / offer.experience_years
    return min(100.0, ratio * 100.0)


def _score_technology(offer: ProcessedOffer, profile: Profile) -> float:
    if not profile.tecnologias or not offer.tecnologias:
        return 0.0
    scores: list[float] = []
    for offer_tech in offer.tecnologias:
        best = max(
            fuzz.token_sort_ratio(offer_tech, profile_tech)
            for profile_tech in profile.tecnologias
        )
        scores.append(float(best))
    return sum(scores) / len(scores) if scores else 0.0


def _score_location(offer: ProcessedOffer, profile: Profile) -> float:
    if not profile.ubicaciones_preferidas or not offer.clean_location:
        return 50.0
    best = max(
        fuzz.partial_ratio(offer.clean_location, preferred)
        for preferred in profile.ubicaciones_preferidas
    )
    return float(best)


def _score_modality(offer: ProcessedOffer, profile: Profile) -> float:
    if not profile.modalidades_preferidas or not offer.modalidad:
        return 50.0
    for preferred in profile.modalidades_preferidas:
        if preferred.lower() == offer.modalidad.lower():
            return 100.0
    return 0.0


def _score_languages(offer: ProcessedOffer, profile: Profile) -> float:
    if not offer.idiomas or not profile.idiomas:
        return 100.0
    offer_languages = set(i.lower() for i in offer.idiomas)
    profile_languages = set(i.lower() for i in profile.idiomas)
    if not offer_languages:
        return 100.0
    covered = offer_languages & profile_languages
    return (len(covered) / len(offer_languages)) * 100.0


def _score_seniority(offer: ProcessedOffer, profile: Profile) -> float:
    if not profile.seniority:
        return 100.0
    offer_seniority = _infer_seniority(offer)
    if not offer_seniority:
        return 50.0
    levels = ["jr", "junior", "semisenior", "senior", "lead", "principal"]
    if profile.seniority.lower() == offer_seniority.lower():
        return 100.0
    profile_idx = next(
        (i for i, n in enumerate(levels) if n in profile.seniority.lower()),
        -1,
    )
    offer_idx = next(
        (i for i, n in enumerate(levels) if n in offer_seniority.lower()),
        -1,
    )
    if profile_idx >= 0 and offer_idx >= 0:
        diff = abs(profile_idx - offer_idx)
        if diff == 1:
            return 50.0
    return 0.0


def _infer_seniority(offer: ProcessedOffer) -> str:
    text = (offer.clean_title + " " + offer.clean_description).lower()
    levels = {
        "principal": "principal",
        "lead": "lead",
        "senior": "senior",
        "sr": "senior",
        "semisenior": "semisenior",
        "ssr": "semisenior",
        "junior": "junior",
        "jr": "junior",
        "trainee": "jr",
    }
    for keyword, level in levels.items():
        if keyword in text:
            return level
    return ""


def _check_excluded(offer: ProcessedOffer, profile: Profile) -> bool:
    if not profile.empresas_excluidas:
        return False
    text = (offer.clean_title + " " + offer.clean_description).lower()
    for company in profile.empresas_excluidas:
        if company.lower() in text:
            return True
    return False


def _penalize_salary(offer: ProcessedOffer, profile: Profile) -> float:
    if profile.salario_minimo is None:
        return 0.0
    offer_salary = offer.salario_max or offer.salario_min
    if offer_salary is None:
        return 10.0
    if offer_salary >= profile.salario_minimo:
        return 0.0
    return min(30.0, (1 - offer_salary / profile.salario_minimo) * 30.0)


def _calculate_score(
    offer: ProcessedOffer,
    profile: Profile,
    weights: dict[str, float],
) -> tuple[float, dict[str, float]]:
    if _check_excluded(offer, profile):
        return 0.0, {"excluida": 0.0}

    partials: dict[str, float] = {}
    partials["experiencia"] = _score_experience(offer, profile)
    partials["tecnologia"] = _score_technology(offer, profile)
    partials["ubicacion"] = _score_location(offer, profile)
    partials["modalidad"] = _score_modality(offer, profile)
    partials["idiomas"] = _score_languages(offer, profile)
    partials["seniority"] = _score_seniority(offer, profile)

    score = sum(
        partials.get(criterion, 0.0) * weight
        for criterion, weight in weights.items()
    )
    penalty = _penalize_salary(offer, profile)
    score = max(0.0, score - penalty)
    return score, partials


def _classify(score: float) -> EvaluationResult:
    config = load()
    eval_cfg = config.get("evaluation", {})
    high_threshold = float(eval_cfg.get("high_compatibility_threshold", 80))
    medium_threshold = float(eval_cfg.get("medium_compatibility_threshold", 50))
    if score >= high_threshold:
        return EvaluationResult.HIGH
    if score >= medium_threshold:
        return EvaluationResult.MEDIUM
    return EvaluationResult.LOW


def _decide(result: EvaluationResult) -> DecisionEvaluation:
    if result in (EvaluationResult.HIGH, EvaluationResult.MEDIUM):
        return DecisionEvaluation.CONTINUE
    return DecisionEvaluation.DISCARD


def _justify(
    score: float,
    partials: dict[str, float],
    weights: dict[str, float],
    penalty: float,
    excluded: bool,
) -> str:
    if excluded:
        return "Offer discarded: company is in the exclusion list"
    parts: list[str] = []
    for criterion, weight in weights.items():
        value = partials.get(criterion, 0.0)
        contribution = value * weight
        parts.append(f"{criterion}: {value:.1f}/100 (weight {weight:.2f}) → {contribution:.1f} pts")
    if penalty > 0:
        parts.append(f"salary penalty: -{penalty:.1f} pts")
    parts.append(f"Total: {score:.1f}/100")
    return " | ".join(parts)


def evaluate(offer: ProcessedOffer, profile: Profile | None = None) -> Evaluation:
    if profile is None:
        profile = load_profile()
    config = load()
    weights = config.get("evaluation", {}).get("weights", {})
    weights_sum = sum(weights.values())
    if not math.isclose(weights_sum, 1.0, abs_tol=1e-6):
        raise ConfigurationError(
            "002",
            f"Invalid evaluation weights: sum={weights_sum}, expected=1.0. "
            f"Check the 'evaluation.weights' section in config/config.yaml",
            source_module="decision_engine",
        )
    excluded = _check_excluded(offer, profile)
    score, partials = _calculate_score(offer, profile, weights)
    penalty = _penalize_salary(offer, profile)
    result = _classify(score)
    decision = _decide(result)
    justification = _justify(score, partials, weights, penalty, excluded)
    approval_threshold = float(
        config.get("evaluation", {}).get("compatibility_threshold_medium", 50)
    )
    return Evaluation(
        processed_offer_id=offer.id,
        resultado=result,
        score=score,
        approval_threshold=approval_threshold,
        decision=decision,
        justification=justification,
        evaluated_criteria=", ".join(weights.keys()),
    )
