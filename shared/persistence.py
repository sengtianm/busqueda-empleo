import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from shared.config import load

_DB_PATH: Path | None = None

PREFIXES: dict[str, str] = {
    "fuentes": "FNT",
    "empresas": "EMP",
    "ubicaciones": "UBI",
    "ofertas": "OFE",
    "corridas": "COR",
    "sesiones": "SES",
    "eventos": "EVT",
    "bloqueo": "BLO",
}

JSON_COLUMNS: set[str] = {
    "requisitos",
    "tecnologias",
    "idiomas",
}

ESQUEMAS: dict[str, str] = {
    "secuencia_ids": (
        "CREATE TABLE IF NOT EXISTS secuencia_ids ("
        "tabla_nombre TEXT PRIMARY KEY,"
        "prefijo TEXT NOT NULL,"
        "ultimo_numero INTEGER NOT NULL DEFAULT 0"
        ")"
    ),
    "fuentes": (
        "CREATE TABLE IF NOT EXISTS fuentes ("
        "id TEXT PRIMARY KEY,"
        "nombre TEXT NOT NULL,"
        "tipo TEXT DEFAULT '',"
        "url_base TEXT DEFAULT '',"
        "activa INTEGER DEFAULT 1,"
        "creation_date TEXT DEFAULT '',"
        "last_edit_date TEXT DEFAULT ''"
        ")"
    ),
    "empresas": (
        "CREATE TABLE IF NOT EXISTS empresas ("
        "id TEXT PRIMARY KEY,"
        "nombre TEXT NOT NULL,"
        "normalized_name TEXT DEFAULT '',"
        "sitio_web TEXT DEFAULT '',"
        "linkedin TEXT DEFAULT '',"
        "sector TEXT DEFAULT '',"
        "size TEXT DEFAULT '',"
        "descripcion TEXT DEFAULT '',"
        "creation_date TEXT DEFAULT '',"
        "last_edit_date TEXT DEFAULT ''"
        ")"
    ),
    "ubicaciones": (
        "CREATE TABLE IF NOT EXISTS ubicaciones ("
        "id TEXT PRIMARY KEY,"
        "ciudad TEXT DEFAULT '',"
        "region TEXT DEFAULT '',"
        "pais TEXT DEFAULT '',"
        "modalidad TEXT DEFAULT '',"
        "creation_date TEXT DEFAULT '',"
        "last_edit_date TEXT DEFAULT ''"
        ")"
    ),
    "ofertas": (
        "CREATE TABLE IF NOT EXISTS ofertas ("
        "id TEXT PRIMARY KEY,"
        "source_identifier TEXT DEFAULT '',"
        "url TEXT NOT NULL,"
        "titulo TEXT DEFAULT '',"
        "descripcion_original TEXT DEFAULT '',"
        "fecha_publicacion TEXT DEFAULT '',"
        "discovery_date TEXT DEFAULT '',"
        "estado TEXT DEFAULT 'discovered' "
        "CHECK(estado IN ('discovered','prepared','evaluated',"
        "'accepted','discarded','processed','finalized')),"
        "observaciones TEXT DEFAULT '',"
        "creation_date TEXT DEFAULT '',"
        "last_edit_date TEXT DEFAULT '',"
        "fuente_id TEXT REFERENCES fuentes(id),"
        "empresa_id TEXT REFERENCES empresas(id),"
        "ubicacion_id TEXT REFERENCES ubicaciones(id),"
        "run_id TEXT DEFAULT '',"
        "session_id TEXT DEFAULT '',"
        "set_indice INTEGER DEFAULT '',"
        "id_externo_url TEXT DEFAULT ''"
        ")"
    ),
    "corridas": (
        "CREATE TABLE IF NOT EXISTS corridas ("
        "run_id TEXT PRIMARY KEY,"
        "timestamp_inicio TEXT NOT NULL,"
        "estado TEXT NOT NULL"
        ")"
    ),
    "eventos": (
        "CREATE TABLE IF NOT EXISTS eventos ("
        "evento_id TEXT PRIMARY KEY,"
        "run_id TEXT NOT NULL,"
        "source_id TEXT DEFAULT '',"
        "session_id TEXT DEFAULT '',"
        "set_indice INTEGER DEFAULT '',"
        "timestamp TEXT NOT NULL,"
        "tipo TEXT NOT NULL CHECK(tipo IN ('error','suceso')),"
        "codigo TEXT NOT NULL,"
        "evidencia TEXT DEFAULT '',"
        "offer_id TEXT DEFAULT ''"
        ")"
    ),
    "sesiones": (
        "CREATE TABLE IF NOT EXISTS sesiones ("
        "session_id TEXT PRIMARY KEY,"
        "run_id TEXT NOT NULL,"
        "source_id TEXT NOT NULL,"
        "set_indice INTEGER DEFAULT '',"
        "timestamp TEXT NOT NULL,"
        "total_declarado INTEGER DEFAULT '',"
        "conteo INTEGER DEFAULT '',"
        "estado TEXT NOT NULL"
        ")"
    ),
    "bloqueo": (
        "CREATE TABLE IF NOT EXISTS bloqueo ("
        "run_id TEXT PRIMARY KEY,"
        "timestamp TEXT NOT NULL"
        ")"
    ),
}


def _db_path() -> Path:
    if _DB_PATH is not None:
        return _DB_PATH
    cfg = load()
    return Path(cfg.get("persistence", {}).get("db_file", "data/busqueda_empleo.db"))


def change_path(ruta: Path) -> None:
    global _DB_PATH
    _DB_PATH = ruta


def reset_path() -> None:
    global _DB_PATH
    _DB_PATH = None


def _connection() -> sqlite3.Connection:
    ruta = _db_path()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(ruta))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _serialize(datos: dict[str, Any]) -> dict[str, Any]:
    d = dict(datos)
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(v, bool):
            d[k] = 1 if v else 0
        elif isinstance(v, (list, dict)):
            d[k] = json.dumps(v, ensure_ascii=False)
    return d


def _deserialize(fila: sqlite3.Row | None) -> dict[str, Any] | None:
    if fila is None:
        return None
    d = dict(fila)
    for k, v in d.items():
        if isinstance(v, int) and k == "activa":
            d[k] = bool(v)
        elif isinstance(v, str) and k in JSON_COLUMNS:
            try:
                d[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                pass
    return d


def init_db() -> None:
    conn = _connection()
    try:
        tablas = ("secuencia_ids", "fuentes", "empresas", "ubicaciones",
                  "ofertas", "corridas", "eventos", "sesiones", "bloqueo")
        for nombre_tabla in tablas:
            conn.execute(ESQUEMAS[nombre_tabla])
        _migrate_ofertas(conn)
        conn.commit()
    finally:
        conn.close()


def _migrate_ofertas(conn: sqlite3.Connection) -> None:
    """C2 migration: "lo crudo se conserva crudo".

    SQLite cannot drop a NOT NULL constraint in place, so the `ofertas` table
    is rebuilt without NOT NULL on `titulo` and `descripcion_original`, allowing
    capturing raw listings that lack those fields. The columns of traceability
    (`run_id`, `session_id`, `set_indice`, `id_externo_url`) are included in the
    new schema. Migration is idempotent: it only runs when the current schema
    still declares `titulo NOT NULL`.
    """
    columnas = {
        fila["name"]: fila["notnull"]
        for fila in conn.execute("PRAGMA table_info(ofertas)").fetchall()
    }
    if "titulo" in columnas and columnas["titulo"] == 0:
        return
    conn.execute(
        ESQUEMAS["ofertas"].replace("TABLE IF NOT EXISTS ofertas", "TABLE ofertas_nueva")
    )
    comunes = [c for c in conn.execute("PRAGMA table_info(ofertas)").fetchall()]
    nombres = [fila["name"] for fila in comunes]
    lista = ", ".join(nombres)
    conn.execute(
        f"INSERT INTO ofertas_nueva ({lista}) SELECT {lista} FROM ofertas"
    )
    conn.execute("DROP TABLE ofertas")
    conn.execute("ALTER TABLE ofertas_nueva RENAME TO ofertas")


def generate_id(tabla: str) -> str:
    prefijo = PREFIXES.get(tabla)
    if prefijo is None:
        disponibles = list(PREFIXES.keys())
        raise ValueError(f"Unknown table: {tabla}. Available prefixes: {disponibles}")
    conn = _connection()
    try:
        conn.execute(
            "INSERT INTO secuencia_ids (tabla_nombre, prefijo, ultimo_numero) VALUES (?, ?, 1) "
            "ON CONFLICT(tabla_nombre) DO UPDATE SET ultimo_numero = ultimo_numero + 1 "
            "RETURNING ultimo_numero",
            (tabla, prefijo),
        )
        fila = conn.execute(
            "SELECT ultimo_numero FROM secuencia_ids WHERE tabla_nombre = ?", (tabla,)
        ).fetchone()
        assert fila is not None
        num = fila["ultimo_numero"]
        conn.commit()
        return f"{prefijo}-{num:04d}"
    finally:
        conn.close()


def read_table(tabla: str) -> list[dict[str, Any]]:
    conn = _connection()
    try:
        cursor = conn.execute(f"SELECT * FROM {tabla}")
        results: list[dict[str, Any]] = []
        for f in cursor.fetchall():
            r = _deserialize(f)
            if r is not None:
                results.append(r)
        return results
    finally:
        conn.close()


def write_row(tabla: str, datos: dict[str, Any]) -> str:
    d = _serialize(datos)
    if "id" not in d or not d["id"]:
        d["id"] = generate_id(tabla)
    ahora = _now()
    if not d.get("creation_date"):
        d["creation_date"] = ahora
    d["last_edit_date"] = ahora

    columnas = [k for k in d.keys()]
    placeholders = [":" + k for k in d.keys()]
    sql = f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({', '.join(placeholders)})"
    conn = _connection()
    try:
        conn.execute(sql, d)
        conn.commit()
        return cast(str, d["id"])
    finally:
        conn.close()


def find_by_id(tabla: str, id_valor: str) -> dict[str, Any] | None:
    conn = _connection()
    try:
        cursor = conn.execute(f"SELECT * FROM {tabla} WHERE id = ?", (id_valor,))
        return _deserialize(cursor.fetchone())
    finally:
        conn.close()


def update(tabla: str, id_valor: str, datos: dict[str, Any]) -> bool:
    d = _serialize(datos)
    d["last_edit_date"] = _now()
    if "id" in d:
        del d["id"]
    asignaciones = ", ".join(f"{k} = :{k}" for k in d.keys())
    d["_id_valor"] = id_valor
    sql = f"UPDATE {tabla} SET {asignaciones} WHERE id = :_id_valor"
    conn = _connection()
    try:
        cursor = conn.execute(sql, d)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def write_batch(tabla: str, filas: list[dict[str, Any]]) -> None:
    if not filas:
        return
    now = _now()
    preparadas: list[dict[str, Any]] = []
    for datos in filas:
        d = _serialize(datos)
        if "id" not in d or not d["id"]:
            d["id"] = generate_id(tabla)
        if not d.get("creation_date"):
            d["creation_date"] = now
        d["last_edit_date"] = now
        preparadas.append(d)

    columnas = sorted({k for d in preparadas for k in d.keys()})
    placeholders = ", ".join(f":{k}" for k in columnas)
    sql = f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({placeholders})"
    conn = _connection()
    try:
        for d in preparadas:
            conn.execute(sql, {k: d.get(k) for k in columnas})
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def _umbral_obsolescencia_minutos() -> int:
    cfg = load().get("concurrencia", {})
    return int(cfg.get("umbral_obsolescencia_minutos", 120))


def acquire_lock(run_id: str, timestamp: str) -> bool:
    conn = _connection()
    try:
        fila = conn.execute(
            "SELECT * FROM bloqueo ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        if fila is None:
            conn.execute(
                "INSERT OR REPLACE INTO bloqueo (run_id, timestamp) VALUES (?, ?)",
                (run_id, timestamp),
            )
            conn.commit()
            return True
        actual = datetime.strptime(fila["timestamp"], "%Y-%m-%d %H:%M:%S")
        umbral_minutos = _umbral_obsolescencia_minutos()
        vigente = (
            datetime.now() - actual
        ).total_seconds() / 60 < umbral_minutos if umbral_minutos > 0 else True
        if vigente:
            return False
        conn.execute(
            "INSERT OR REPLACE INTO bloqueo (run_id, timestamp) VALUES (?, ?)",
            (run_id, timestamp),
        )
        conn.commit()
        return True
    finally:
        conn.close()


def release_lock(run_id: str) -> None:
    conn = _connection()
    try:
        conn.execute("DELETE FROM bloqueo WHERE run_id = ?", (run_id,))
        conn.commit()
    finally:
        conn.close()


def check_lock() -> dict[str, Any] | None:
    conn = _connection()
    try:
        fila = conn.execute(
            "SELECT * FROM bloqueo ORDER BY timestamp DESC LIMIT 1"
        ).fetchone()
        return dict(fila) if fila is not None else None
    finally:
        conn.close()
