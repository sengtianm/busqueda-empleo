"""Internal: connection state and row serialization helpers."""

import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any

from shared.config import load

_DB_PATH: Path | None = None


JSON_COLUMNS: set[str] = {
    "requisitos",
    "tecnologias",
    "idiomas",
}



def _db_path() -> Path:
    if _DB_PATH is not None:
        return _DB_PATH
    cfg = load()
    return Path(cfg.get("persistence", {}).get("db_file", "data/job_search.db"))



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
