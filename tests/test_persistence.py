from pathlib import Path

from shared.persistence import (
    actualizar,
    buscar_por_id,
    escribir_fila,
    generar_id,
    leer_tabla,
)


def test_generar_id_secuencia(archivo_bd_temporal: Path) -> None:
    id1 = generar_id("empresas")
    id2 = generar_id("empresas")
    id3 = generar_id("empresas")
    assert id1 == "EMP-0001"
    assert id2 == "EMP-0002"
    assert id3 == "EMP-0003"


def test_generar_id_por_tabla(archivo_bd_temporal: Path) -> None:
    emp = generar_id("empresas")
    ofe = generar_id("ofertas")
    fnt = generar_id("fuentes")
    assert emp.startswith("EMP-")
    assert ofe.startswith("OFE-")
    assert fnt.startswith("FNT-")


def test_escribir_y_leer(archivo_bd_temporal: Path) -> None:
    datos = {"nombre": "Test", "sector": "tecnologia"}
    id_generado = escribir_fila("empresas", datos)
    assert id_generado.startswith("EMP-")
    filas = leer_tabla("empresas")
    assert len(filas) == 1
    assert filas[0]["nombre"] == "Test"
    assert filas[0]["id"] == id_generado


def test_buscar_por_id_existente(archivo_bd_temporal: Path) -> None:
    id1 = escribir_fila("empresas", {"nombre": "Uno", "sector": "tech"})
    escribir_fila("empresas", {"nombre": "Dos", "sector": "fintech"})
    resultado = buscar_por_id("empresas", id1)
    assert resultado is not None
    assert resultado["nombre"] == "Uno"


def test_buscar_por_id_inexistente(archivo_bd_temporal: Path) -> None:
    resultado = buscar_por_id("empresas", "EMP-9999")
    assert resultado is None


def test_actualizar(archivo_bd_temporal: Path) -> None:
    id1 = escribir_fila("empresas", {"nombre": "Viejo", "sector": "tech"})
    ok = actualizar("empresas", id1, {"nombre": "Nuevo"})
    assert ok is True
    filas = leer_tabla("empresas")
    assert filas[0]["nombre"] == "Nuevo"


def test_actualizar_inexistente(archivo_bd_temporal: Path) -> None:
    ok = actualizar("empresas", "EMP-9999", {"nombre": "Nuevo"})
    assert ok is False


def test_escribir_con_id_explicito(archivo_bd_temporal: Path) -> None:
    id_devuelto = escribir_fila("empresas", {"id": "EMP-0100", "nombre": "Custom"})
    assert id_devuelto == "EMP-0100"
    resultado = buscar_por_id("empresas", "EMP-0100")
    assert resultado is not None
    assert resultado["nombre"] == "Custom"


def test_listas_json(archivo_bd_temporal: Path) -> None:
    id_oferta = escribir_fila("ofertas", {
        "url": "https://example.com/job",
        "titulo": "Data Engineer",
        "descripcion_original": "Test",
    })
    resultado = buscar_por_id("ofertas", id_oferta)
    assert resultado is not None
    assert resultado["url"] == "https://example.com/job"
    assert resultado["titulo"] == "Data Engineer"
