import math

from rapidfuzz import fuzz

from shared.config import cargar
from shared.errors import ErrorConfiguracion
from shared.models import (
    DecisionEvaluacion,
    Evaluacion,
    OfertaProcesada,
    Perfil,
    ResultadoEvaluacion,
)


def cargar_perfil() -> Perfil:
    config = cargar()
    datos = config.get("perfil", {})
    return Perfil(**datos)


def _puntuar_experiencia(oferta: OfertaProcesada, perfil: Perfil) -> float:
    if oferta.experiencia_anios is None or oferta.experiencia_anios == 0:
        return 100.0
    ratio = perfil.experiencia_anios / oferta.experiencia_anios
    return min(100.0, ratio * 100.0)


def _puntuar_tecnologia(oferta: OfertaProcesada, perfil: Perfil) -> float:
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


def _puntuar_ubicacion(oferta: OfertaProcesada, perfil: Perfil) -> float:
    if not perfil.ubicaciones_preferidas or not oferta.ubicacion_limpia:
        return 50.0
    mejor = max(
        fuzz.partial_ratio(oferta.ubicacion_limpia, pref)
        for pref in perfil.ubicaciones_preferidas
    )
    return float(mejor)


def _puntuar_modalidad(oferta: OfertaProcesada, perfil: Perfil) -> float:
    if not perfil.modalidades_preferidas or not oferta.modalidad:
        return 50.0
    for pref in perfil.modalidades_preferidas:
        if pref.lower() == oferta.modalidad.lower():
            return 100.0
    return 0.0


def _puntuar_idiomas(oferta: OfertaProcesada, perfil: Perfil) -> float:
    if not oferta.idiomas or not perfil.idiomas:
        return 100.0
    oferta_ids = set(i.lower() for i in oferta.idiomas)
    perfil_ids = set(i.lower() for i in perfil.idiomas)
    if not oferta_ids:
        return 100.0
    cubiertos = oferta_ids & perfil_ids
    return (len(cubiertos) / len(oferta_ids)) * 100.0


def _puntuar_seniority(oferta: OfertaProcesada, perfil: Perfil) -> float:
    if not perfil.seniority:
        return 100.0
    oferta_seniority = _inferir_seniority(oferta)
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


def _inferir_seniority(oferta: OfertaProcesada) -> str:
    texto = (oferta.titulo_limpio + " " + oferta.descripcion_limpia).lower()
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


def _verificar_excluidas(oferta: OfertaProcesada, perfil: Perfil) -> bool:
    if not perfil.empresas_excluidas:
        return False
    texto = (oferta.titulo_limpio + " " + oferta.descripcion_limpia).lower()
    for empresa in perfil.empresas_excluidas:
        if empresa.lower() in texto:
            return True
    return False


def _penalizar_salario(oferta: OfertaProcesada, perfil: Perfil) -> float:
    if perfil.salario_minimo is None:
        return 0.0
    salario_oferta = oferta.salario_max or oferta.salario_min
    if salario_oferta is None:
        return 10.0
    if salario_oferta >= perfil.salario_minimo:
        return 0.0
    return min(30.0, (1 - salario_oferta / perfil.salario_minimo) * 30.0)


def _calcular_puntaje(
    oferta: OfertaProcesada,
    perfil: Perfil,
    pesos: dict[str, float],
) -> tuple[float, dict[str, float]]:
    if _verificar_excluidas(oferta, perfil):
        return 0.0, {"excluida": 0.0}

    parciales: dict[str, float] = {}
    parciales["experiencia"] = _puntuar_experiencia(oferta, perfil)
    parciales["tecnologia"] = _puntuar_tecnologia(oferta, perfil)
    parciales["ubicacion"] = _puntuar_ubicacion(oferta, perfil)
    parciales["modalidad"] = _puntuar_modalidad(oferta, perfil)
    parciales["idiomas"] = _puntuar_idiomas(oferta, perfil)
    parciales["seniority"] = _puntuar_seniority(oferta, perfil)

    puntaje = sum(
        parciales.get(criterio, 0.0) * peso
        for criterio, peso in pesos.items()
    )
    penalizacion = _penalizar_salario(oferta, perfil)
    puntaje = max(0.0, puntaje - penalizacion)
    return puntaje, parciales


def _clasificar(puntaje: float) -> ResultadoEvaluacion:
    config = cargar()
    eval_cfg = config.get("evaluacion", {})
    alta = float(eval_cfg.get("umbral_compatibilidad_alta", 80))
    media = float(eval_cfg.get("umbral_compatibilidad_media", 50))
    if puntaje >= alta:
        return ResultadoEvaluacion.ALTA
    if puntaje >= media:
        return ResultadoEvaluacion.MEDIA
    return ResultadoEvaluacion.BAJA


def _decidir(resultado: ResultadoEvaluacion) -> DecisionEvaluacion:
    if resultado in (ResultadoEvaluacion.ALTA, ResultadoEvaluacion.MEDIA):
        return DecisionEvaluacion.CONTINUAR
    return DecisionEvaluacion.DESCARTAR


def _justificar(
    puntaje: float,
    parciales: dict[str, float],
    pesos: dict[str, float],
    penalizacion: float,
    excluida: bool,
) -> str:
    if excluida:
        return "Oferta descartada: la empresa esta en la lista de exclusion"
    partes: list[str] = []
    for criterio, peso in pesos.items():
        val = parciales.get(criterio, 0.0)
        contrib = val * peso
        partes.append(f"{criterio}: {val:.1f}/100 (peso {peso:.2f}) → {contrib:.1f} pts")
    if penalizacion > 0:
        partes.append(f"penalizacion por salario: -{penalizacion:.1f} pts")
    partes.append(f"Total: {puntaje:.1f}/100")
    return " | ".join(partes)


def evaluar(oferta: OfertaProcesada, perfil: Perfil | None = None) -> Evaluacion:
    if perfil is None:
        perfil = cargar_perfil()
    config = cargar()
    pesos = config.get("evaluacion", {}).get("pesos", {})
    suma_pesos = sum(pesos.values())
    if not math.isclose(suma_pesos, 1.0, abs_tol=1e-6):
        raise ErrorConfiguracion(
            "002",
            f"Pesos de evaluacion invalidos: suma={suma_pesos}, esperado=1.0. "
            f"Revise la seccion 'evaluacion.pesos' en config/config.yaml",
            modulo_origen="decision_engine",
        )
    excluida = _verificar_excluidas(oferta, perfil)
    puntaje, parciales = _calcular_puntaje(oferta, perfil, pesos)
    penalizacion = _penalizar_salario(oferta, perfil)
    resultado = _clasificar(puntaje)
    decision = _decidir(resultado)
    justificacion = _justificar(puntaje, parciales, pesos, penalizacion, excluida)
    umbral_aprobacion = float(
        config.get("evaluacion", {}).get("umbral_compatibilidad_media", 50)
    )
    return Evaluacion(
        oferta_procesada_id=oferta.id,
        resultado=resultado,
        puntaje=puntaje,
        umbral_aprobacion=umbral_aprobacion,
        decision=decision,
        justificacion=justificacion,
        criterios_evaluados=", ".join(pesos.keys()),
    )
