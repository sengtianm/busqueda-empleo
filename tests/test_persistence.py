from pathlib import Path

from shared.persistence import (
    find_by_id,
    generate_id,
    read_table,
    update,
    write_row,
)


def test_generar_id_secuencia(archivo_bd_temporal: Path) -> None:
    id1 = generate_id("empresas")
    id2 = generate_id("empresas")
    id3 = generate_id("empresas")
    assert id1 == "EMP-0001"
    assert id2 == "EMP-0002"
    assert id3 == "EMP-0003"


def test_generar_id_por_tabla(archivo_bd_temporal: Path) -> None:
    emp = generate_id("empresas")
    ofe = generate_id("ofertas")
    fnt = generate_id("fuentes")
    assert emp.startswith("EMP-")
    assert ofe.startswith("OFE-")
    assert fnt.startswith("FNT-")


def test_escribir_y_leer(archivo_bd_temporal: Path) -> None:
    datos = {"nombre": "Test", "sector": "tecnologia"}
    id_generado = write_row("empresas", datos)
    assert id_generado.startswith("EMP-")
    filas = read_table("empresas")
    assert len(filas) == 1
    assert filas[0]["nombre"] == "Test"
    assert filas[0]["id"] == id_generado


def test_buscar_por_id_existente(archivo_bd_temporal: Path) -> None:
    id1 = write_row("empresas", {"nombre": "Uno", "sector": "tech"})
    write_row("empresas", {"nombre": "Dos", "sector": "fintech"})
    resultado = find_by_id("empresas", id1)
    assert resultado is not None
    assert resultado["nombre"] == "Uno"


def test_buscar_por_id_inexistente(archivo_bd_temporal: Path) -> None:
    resultado = find_by_id("empresas", "EMP-9999")
    assert resultado is None


def test_actualizar(archivo_bd_temporal: Path) -> None:
    id1 = write_row("empresas", {"nombre": "Viejo", "sector": "tech"})
    ok = update("empresas", id1, {"nombre": "Nuevo"})
    assert ok is True
    filas = read_table("empresas")
    assert filas[0]["nombre"] == "Nuevo"


def test_actualizar_inexistente(archivo_bd_temporal: Path) -> None:
    ok = update("empresas", "EMP-9999", {"nombre": "Nuevo"})
    assert ok is False


def test_escribir_con_id_explicito(archivo_bd_temporal: Path) -> None:
    id_devuelto = write_row("empresas", {"id": "EMP-0100", "nombre": "Custom"})
    assert id_devuelto == "EMP-0100"
    resultado = find_by_id("empresas", "EMP-0100")
    assert resultado is not None
    assert resultado["nombre"] == "Custom"


def test_listas_json(archivo_bd_temporal: Path) -> None:
    id_oferta = write_row("ofertas", {
        "url": "https://example.com/job",
        "titulo": "Data Engineer",
        "descripcion_original": "Test",
    })
    resultado = find_by_id("ofertas", id_oferta)
    assert resultado is not None
    assert resultado["url"] == "https://example.com/job"
    assert resultado["titulo"] == "Data Engineer"
