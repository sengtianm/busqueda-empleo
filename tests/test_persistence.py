from pathlib import Path

from shared.persistence import (
    find_by_id,
    generate_id,
    read_table,
    update,
    write_batch,
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


def test_init_db_crea_nueve_tablas(temp_db_file: Path) -> None:
    import sqlite3

    conn = sqlite3.connect(str(temp_db_file))
    try:
        tablas = {
            fila[0] for fila in conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
    finally:
        conn.close()
    expected = {"secuencia_ids", "fuentes", "empresas", "ubicaciones",
                "ofertas", "corridas", "eventos", "sesiones", "bloqueo"}
    assert expected.issubset(tablas)


def test_write_batch_ok(temp_db_file: Path) -> None:
    filas = [
        {"url": f"https://x.com/{i}", "titulo": f"Titulo {i}",
         "descripcion_original": "d"} for i in range(3)
    ]
    write_batch("ofertas", filas)
    rows = read_table("ofertas")
    assert len(rows) == 3
    assert all(r["titulo"].startswith("Titulo") for r in rows)


def test_write_batch_rollback_parcial(temp_db_file: Path) -> None:
    import sqlite3

    from shared.persistence import write_batch

    try:
        write_batch("ofertas", [
            {"url": "https://x.com/ok", "titulo": "Ok",
             "descripcion_original": "d"},
            {"url": None},
        ])
    except sqlite3.IntegrityError:
        pass
    else:
        raise AssertionError("write_batch deberia fallar con url NULL")
    rows = read_table("ofertas")
    assert rows == []


def test_acquire_and_release_lock(temp_db_file: Path) -> None:
    from shared.persistence import acquire_lock, check_lock, release_lock

    assert acquire_lock("COR-0001", "2026-08-07 10:00:00") is True
    assert check_lock() == {"run_id": "COR-0001", "timestamp": "2026-08-07 10:00:00"}
    release_lock("COR-0001")
    assert check_lock() is None


def test_lock_obsoleto_se_sobrescribe(temp_db_file: Path) -> None:
    import datetime

    from shared.persistence import acquire_lock, check_lock

    viejo = datetime.datetime.now() - datetime.timedelta(minutes=300)
    assert acquire_lock("COR-0001", viejo.strftime("%Y-%m-%d %H:%M:%S")) is True
    assert acquire_lock("COR-0002", datetime.datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S")) is True
    lock = check_lock()
    assert lock is not None
    assert lock["run_id"] == "COR-0002"


def test_lock_vigente_rechaza(temp_db_file: Path) -> None:
    import datetime

    from shared.persistence import acquire_lock

    ahora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    assert acquire_lock("COR-0001", ahora) is True
    assert acquire_lock("COR-0002", ahora) is False


def test_generate_id_prefijos_nuevos(temp_db_file: Path) -> None:
    from shared.persistence import generate_id

    assert generate_id("corridas").startswith("COR-")
    assert generate_id("sesiones").startswith("SES-")
    assert generate_id("eventos").startswith("EVT-")
    assert generate_id("bloqueo").startswith("BLO-")


def test_esquema_ofertas_sin_not_null(temp_db_file: Path) -> None:
    import sqlite3

    conn = sqlite3.connect(str(temp_db_file))
    try:
        columnas = {
            fila[1]: fila[3] for fila in conn.execute(
                "PRAGMA table_info(ofertas)"
            ).fetchall()
        }
    finally:
        conn.close()
    assert columnas["titulo"] == 0
    assert columnas["descripcion_original"] == 0


def test_migracion_c2_desde_esquema_antiguo(tmp_path: Path) -> None:
    import sqlite3

    from shared.persistence import change_path, init_db, read_table, reset_path

    path = tmp_path / "vieja.db"
    conn = sqlite3.connect(str(path))
    conn.execute(
        "CREATE TABLE ofertas ("
        "id TEXT PRIMARY KEY,"
        "url TEXT NOT NULL,"
        "titulo TEXT NOT NULL,"
        "descripcion_original TEXT NOT NULL"
        ")"
    )
    conn.execute(
        "INSERT INTO ofertas (id, url, titulo, descripcion_original) "
        "VALUES ('OFE-0001', 'https://x.com/1', 'Titulo Antiguo', 'Desc')"
    )
    conn.commit()
    conn.close()

    change_path(path)
    try:
        init_db()
        columnas = {
            fila[1]: fila[3] for fila in sqlite3.connect(str(path)).execute(
                "PRAGMA table_info(ofertas)"
            ).fetchall()
        }
        assert columnas["titulo"] == 0
        assert columnas["descripcion_original"] == 0
        rows = read_table("ofertas")
        assert len(rows) == 1
        assert rows[0]["id"] == "OFE-0001"
        assert rows[0]["titulo"] == "Titulo Antiguo"
    finally:
        reset_path()


def test_migracion_c2_idempotente(tmp_path: Path) -> None:
    import sqlite3

    from shared.persistence import change_path, init_db, reset_path

    path = tmp_path / "nueva.db"
    conn = sqlite3.connect(str(path))
    conn.execute(
        "CREATE TABLE ofertas ("
        "id TEXT PRIMARY KEY,"
        "url TEXT NOT NULL,"
        "titulo TEXT NOT NULL,"
        "descripcion_original TEXT NOT NULL"
        ")"
    )
    conn.commit()
    conn.close()

    change_path(path)
    try:
        init_db()
        init_db()
        columnas = {
            fila[1]: fila[3] for fila in sqlite3.connect(str(path)).execute(
                "PRAGMA table_info(ofertas)"
            ).fetchall()
        }
        assert columnas["titulo"] == 0
        assert columnas["descripcion_original"] == 0
    finally:
        reset_path()
