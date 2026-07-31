from pathlib import Path

from shared.persistence import (
    find_by_id,
    generate_id,
    read_table,
    update,
    write_row,
)


def test_generate_id_sequence(temp_db_file: Path) -> None:
    id_1 = generate_id("empresas")
    id_2 = generate_id("empresas")
    id_3 = generate_id("empresas")
    assert id_1 == "EMP-0001"
    assert id_2 == "EMP-0002"
    assert id_3 == "EMP-0003"


def test_generate_id_per_table(temp_db_file: Path) -> None:
    company_id = generate_id("empresas")
    offer_id = generate_id("ofertas")
    source_id = generate_id("fuentes")
    assert company_id.startswith("EMP-")
    assert offer_id.startswith("OFE-")
    assert source_id.startswith("FNT-")


def test_write_and_read(temp_db_file: Path) -> None:
    data = {"nombre": "Test", "sector": "tecnologia"}
    generated_id = write_row("empresas", data)
    assert generated_id.startswith("EMP-")
    rows = read_table("empresas")
    assert len(rows) == 1
    assert rows[0]["nombre"] == "Test"
    assert rows[0]["id"] == generated_id


def test_find_by_id_existing(temp_db_file: Path) -> None:
    id_1 = write_row("empresas", {"nombre": "Uno", "sector": "tech"})
    write_row("empresas", {"nombre": "Dos", "sector": "fintech"})
    result = find_by_id("empresas", id_1)
    assert result is not None
    assert result["nombre"] == "Uno"


def test_find_by_id_missing(temp_db_file: Path) -> None:
    result = find_by_id("empresas", "EMP-9999")
    assert result is None


def test_update(temp_db_file: Path) -> None:
    id_1 = write_row("empresas", {"nombre": "Viejo", "sector": "tech"})
    ok = update("empresas", id_1, {"nombre": "Nuevo"})
    assert ok is True
    rows = read_table("empresas")
    assert rows[0]["nombre"] == "Nuevo"


def test_update_missing(temp_db_file: Path) -> None:
    ok = update("empresas", "EMP-9999", {"nombre": "Nuevo"})
    assert ok is False


def test_write_with_explicit_id(temp_db_file: Path) -> None:
    returned_id = write_row("empresas", {"id": "EMP-0100", "nombre": "Custom"})
    assert returned_id == "EMP-0100"
    result = find_by_id("empresas", "EMP-0100")
    assert result is not None
    assert result["nombre"] == "Custom"


def test_json_lists(temp_db_file: Path) -> None:
    offer_id = write_row("ofertas", {
        "url": "https://example.com/job",
        "titulo": "Data Engineer",
        "descripcion_original": "Test",
    })
    result = find_by_id("ofertas", offer_id)
    assert result is not None
    assert result["url"] == "https://example.com/job"
    assert result["titulo"] == "Data Engineer"
