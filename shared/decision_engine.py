import math

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
    datos = config.get("profile", {})
    return Profile(**datos)


def _score_experience(oferta: ProcessedOffer, perfil: Profile) -> float:
    if oferta.experience_years is None or oferta.experience_years == 0:
        return 100.0
    ratio = perfil.experience_years / oferta.experience_years
    return min(100.0, ratio * 100.0)


def _score_technology(oferta: ProcessedOffer, perfil: Profile) -> float:
    if not perfil.tecnologias or not oferta.tecnologias:
        return 0.0
    puntajes: list[float] = []
    for tec_oferta in oferta.tecnologias:
        mejor = max(
            fuzz.token_sort_ratio(tec_oferta, tec_perfil)
            for tec_perfil in perfil.tecnologias
        )
        puntajes.append(float(mejor))
    return sum(puntajes) / len(puntajes) if puntajes else 0.0


def _score_location(oferta: ProcessedOffer, perfil: Profile) -> float:
    if not perfil.ubicaciones_preferidas or not oferta.clean_location:
        return 50.0
    mejor = max(
        fuzz.partial_ratio(oferta.clean_location, pref)
        for pref in perfil.ubicaciones_preferidas
    )
    return float(mejor)


def _score_modality(oferta: ProcessedOffer, perfil: Profile) -> float:
    if not perfil.modalidades_preferidas or not oferta.modalidad:
        return 50.0
    for pref in perfil.modalidades_preferidas:
        if pref.lower() == oferta.modalidad.lower():
            return 100.0
    return 0.0


def _score_languages(oferta: ProcessedOffer, perfil: Profile) -> float:
    if not oferta.idiomas or not perfil.idiomas:
        return 100.0
    oferta_ids = set(i.lower() for i in oferta.idiomas)
    perfil_ids = set(i.lower() for i in perfil.idiomas)
    if not oferta_ids:
        return 100.0
    cubiertos = oferta_ids & perfil_ids
    return (len(cubiertos) / len(oferta_ids)) * 100.0


def _score_seniority(oferta: ProcessedOffer, perfil: Profile) -> float:
    if not perfil.seniority:
        return 100.0
    oferta_seniority = _infer_seniority(oferta)
    if not oferta_seniority:
        return 50.0
    niveles = ["jr", "junior", "semisenior", "senior", "lead", "principal"]
    if perfil.seniority.lower() == oferta_seniority.lower():
        return 100.0
    idx_perfil = next(
        (i for i, n in enumerate(niveles) if n in perfil.seniority.lower()),
        -1,
    )
    idx_oferta = next(
        (i for i, n in enumerate(niveles) if n in oferta_seniority.lower()),
        -1,
    )
    if idx_perfil >= 0 and idx_oferta >= 0:
        diff = abs(idx_perfil - idx_oferta)
        if diff == 1:
            return 50.0
    return 0.0


def _infer_seniority(oferta: ProcessedOffer) -> str:
    texto = (oferta.clean_title + " " + oferta.clean_description).lower()
    niveles = {
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
    for palabra, nivel in niveles.items():
        if palabra in texto:
            return nivel
    return ""


def _check_excluded(oferta: ProcessedOffer, perfil: Profile) -> bool:
    if not perfil.empresas_excluidas:
        return False
    texto = (oferta.clean_title + " " + oferta.clean_description).lower()
    for empresa in perfil.empresas_excluidas:
        if empresa.lower() in texto:
            return True
    return False


def _penalize_salary(oferta: ProcessedOffer, perfil: Profile) -> float:
    if perfil.salario_minimo is None:
        return 0.0
    salario_oferta = oferta.salario_max or oferta.salario_min
    if salario_oferta is None:
        return 10.0
    if salario_oferta >= perfil.salario_minimo:
        return 0.0
    return min(30.0, (1 - salario_oferta / perfil.salario_minimo) * 30.0)


def _calculate_score(
    oferta: ProcessedOffer,
    perfil: Profile,
    pesos: dict[str, float],
) -> tuple[float, dict[str, float]]:
    if _check_excluded(oferta, perfil):
        return 0.0, {"excluida": 0.0}

    parciales: dict[str, float] = {}
    parciales["experiencia"] = _score_experience(oferta, perfil)
    parciales["tecnologia"] = _score_technology(oferta, perfil)
    parciales["ubicacion"] = _score_location(oferta, perfil)
    parciales["modalidad"] = _score_modality(oferta, perfil)
    parciales["idiomas"] = _score_languages(oferta, perfil)
    parciales["seniority"] = _score_seniority(oferta, perfil)

    puntaje = sum(
        parciales.get(criterio, 0.0) * peso
        for criterio, peso in pesos.items()
    )
    penalizacion = _penalize_salary(oferta, perfil)
    puntaje = max(0.0, puntaje - penalizacion)
    return puntaje, parciales


def _classify(puntaje: float) -> EvaluationResult:
    config = load()
    eval_cfg = config.get("evaluation", {})
    alta = float(eval_cfg.get("high_compatibility_threshold", 80))
    media = float(eval_cfg.get("medium_compatibility_threshold", 50))
    if puntaje >= alta:
        return EvaluationResult.HIGH
    if puntaje >= media:
        return EvaluationResult.MEDIUM
    return EvaluationResult.LOW


def _decide(resultado: EvaluationResult) -> DecisionEvaluation:
    if resultado in (EvaluationResult.HIGH, EvaluationResult.MEDIUM):
        return DecisionEvaluation.CONTINUE
    return DecisionEvaluation.DISCARD


def _justify(
    puntaje: float,
    parciales: dict[str, float],
    pesos: dict[str, float],
    penalizacion: float,
    excluida: bool,
) -> str:
    if excluida:
        return "Offer discarded: company is in the exclusion list"
    partes: list[str] = []
    for criterio, peso in pesos.items():
        val = parciales.get(criterio, 0.0)
        contrib = val * peso
        partes.append(f"{criterio}: {val:.1f}/100 (weight {peso:.2f}) → {contrib:.1f} pts")
    if penalizacion > 0:
        partes.append(f"salary penalty: -{penalizacion:.1f} pts")
    partes.append(f"Total: {puntaje:.1f}/100")
    return " | ".join(partes)


def evaluar(oferta: ProcessedOffer, perfil: Profile | None = None) -> Evaluation:
    if perfil is None:
        perfil = load_profile()
    config = load()
    pesos = config.get("evaluation", {}).get("weights", {})
    suma_pesos = sum(pesos.values())
    if not math.isclose(suma_pesos, 1.0, abs_tol=1e-6):
        raise ConfigurationError(
            "002",
            f"Invalid evaluation weights: sum={suma_pesos}, expected=1.0. "
            f"Check the 'evaluation.weights' section in config/config.yaml",
            source_module="decision_engine",
        )
    excluida = _check_excluded(oferta, perfil)
    puntaje, parciales = _calculate_score(oferta, perfil, pesos)
    penalizacion = _penalize_salary(oferta, perfil)
    resultado = _classify(puntaje)
    decision = _decide(resultado)
    justificacion = _justify(puntaje, parciales, pesos, penalizacion, excluida)
    umbral_aprobacion = float(
        config.get("evaluation", {}).get("compatibility_threshold_medium", 50)
    )
    return Evaluation(
        processed_offer_id=oferta.id,
        resultado=resultado,
        score=puntaje,
        approval_threshold=umbral_aprobacion,
        decision=decision,
        justification=justificacion,
        evaluated_criteria=", ".join(pesos.keys()),
    )
