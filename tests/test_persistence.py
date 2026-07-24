from pathlib import Path

from shared.persistence import actualizar, buscar_por_id, escribir_fila, leer_hoja


def test_escribir_y_leer(archivo_xlsx_temporal: Path) -> None:
    datos = {"id": "1", "nombre": "Test", "valor": 123}
    escribir_fila(archivo_xlsx_temporal, "Sheet1", datos)
    filas = leer_hoja(archivo_xlsx_temporal)
    assert len(filas) == 1
    assert filas[0]["nombre"] == "Test"


def test_buscar_por_id_existente(archivo_xlsx_temporal: Path) -> None:
    escribir_fila(archivo_xlsx_temporal, "Sheet1", {"id": "1", "nombre": "Uno"})
    escribir_fila(archivo_xlsx_temporal, "Sheet1", {"id": "2", "nombre": "Dos"})
    resultado = buscar_por_id(archivo_xlsx_temporal, "Sheet1", "id", "1")
    assert resultado is not None
    assert resultado["nombre"] == "Uno"


def test_buscar_por_id_inexistente(archivo_xlsx_temporal: Path) -> None:
    escribir_fila(archivo_xlsx_temporal, "Sheet1", {"id": "1", "nombre": "Uno"})
    resultado = buscar_por_id(archivo_xlsx_temporal, "Sheet1", "id", "99")
    assert resultado is None


def test_actualizar(archivo_xlsx_temporal: Path) -> None:
    escribir_fila(archivo_xlsx_temporal, "Sheet1", {"id": "1", "nombre": "Viejo"})
    ok = actualizar(archivo_xlsx_temporal, "Sheet1", "id", "1", {"nombre": "Nuevo"})
    assert ok is True
    filas = leer_hoja(archivo_xlsx_temporal)
    assert filas[0]["nombre"] == "Nuevo"


def test_actualizar_inexistente(archivo_xlsx_temporal: Path) -> None:
    escribir_fila(archivo_xlsx_temporal, "Sheet1", {"id": "1", "nombre": "Uno"})
    ok = actualizar(archivo_xlsx_temporal, "Sheet1", "id", "99", {"nombre": "Nuevo"})
    assert ok is False


def test_leer_hoja_archivo_inexistente() -> None:
    resultado = leer_hoja(Path("/tmp/no_existe.xlsx"))
    assert resultado == []
