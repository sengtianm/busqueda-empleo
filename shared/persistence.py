import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from shared.config import load
from shared.errors import PersistenceError

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
        "enlace_base TEXT DEFAULT '',"
        "activa INTEGER DEFAULT 1,"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT ''"
        ")"
    ),
    "empresas": (
        "CREATE TABLE IF NOT EXISTS empresas ("
        "id TEXT PRIMARY KEY,"
        "nombre TEXT NOT NULL,"
        "nombre_normalizado TEXT DEFAULT '',"
        "sitio_web TEXT DEFAULT '',"
        "perfil_linkedin TEXT DEFAULT '',"
        "sector TEXT DEFAULT '',"
        "tamano TEXT DEFAULT '',"
        "descripcion TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT ''"
        ")"
    ),
    "ubicaciones": (
        "CREATE TABLE IF NOT EXISTS ubicaciones ("
        "id TEXT PRIMARY KEY,"
        "ciudad TEXT DEFAULT '',"
        "region TEXT DEFAULT '',"
        "pais TEXT DEFAULT '',"
        "modalidad TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT ''"
        ")"
    ),
    "ofertas": (
        "CREATE TABLE IF NOT EXISTS ofertas ("
        "id TEXT PRIMARY KEY,"
        "identificador_origen TEXT DEFAULT '',"
        "enlace TEXT NOT NULL,"
        "titulo TEXT DEFAULT '',"
        "descripcion_original TEXT DEFAULT '',"
        "fecha_publicacion TEXT DEFAULT '',"
        "fecha_descubrimiento TEXT DEFAULT '',"
        "estado TEXT DEFAULT 'descubierta' "
        "CHECK(estado IN ('descubierta','preparada','evaluada',"
        "'aceptada','descartada','procesada','finalizada')),"
        "observaciones TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT '',"
        "fuente_id TEXT DEFAULT '',"
        "empresa_id TEXT DEFAULT '',"
        "ubicacion_id TEXT DEFAULT '',"
        "empresa_nombre TEXT DEFAULT '',"
        "ubicacion_nombre TEXT DEFAULT '',"
        "id_corrida TEXT DEFAULT '',"
        "id_sesion TEXT DEFAULT '',"
        "indice_set INTEGER DEFAULT '',"
        "id_externo TEXT DEFAULT '',"
        "fecha_ultima_verificacion TEXT DEFAULT ''"
        ")"
    ),
    "corridas": (
        "CREATE TABLE IF NOT EXISTS corridas ("
        "id_corrida TEXT PRIMARY KEY,"
        "fecha_inicio TEXT NOT NULL,"
        "estado TEXT NOT NULL,"
        "fecha_fin TEXT DEFAULT '',"
        "motivo_terminacion TEXT DEFAULT '',"
        "total_ofertas INTEGER DEFAULT 0,"
        "total_errores INTEGER DEFAULT 0,"
        "total_sucesos INTEGER DEFAULT 0,"
        "fuentes_procesadas INTEGER DEFAULT 0"
        ")"
    ),
    "eventos": (
        "CREATE TABLE IF NOT EXISTS eventos ("
        "evento_id TEXT PRIMARY KEY,"
        "id_corrida TEXT NOT NULL,"
        "fuente_id TEXT DEFAULT '',"
        "id_sesion TEXT DEFAULT '',"
        "indice_set INTEGER DEFAULT '',"
        "marca_temporal TEXT NOT NULL,"
        "tipo TEXT NOT NULL CHECK(tipo IN ('error','suceso')),"
        "codigo TEXT NOT NULL,"
        "evidencia TEXT DEFAULT '',"
        "id_oferta TEXT DEFAULT ''"
        ")"
    ),
    "sesiones": (
        "CREATE TABLE IF NOT EXISTS sesiones ("
        "id TEXT PRIMARY KEY,"
        "id_sesion TEXT NOT NULL,"
        "id_corrida TEXT NOT NULL,"
        "fuente_id TEXT NOT NULL,"
        "indice_set INTEGER DEFAULT '',"
        "marca_temporal TEXT NOT NULL,"
        "total_declarado INTEGER DEFAULT '',"
        "conteo INTEGER DEFAULT '',"
        "estado TEXT NOT NULL,"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT ''"
        ")"
    ),
    "bloqueo": (
        "CREATE TABLE IF NOT EXISTS bloqueo ("
        "id_corrida TEXT PRIMARY KEY,"
        "marca_temporal TEXT NOT NULL"
        ")"
    ),
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
        _migrar_espanol_total(conn)
        _migrate_ofertas(conn)
        _migrate_ofertas_timestamp_ultima_verificacion(conn)
        _migrate_ofertas_empresa_nombre(conn)
        _migrate_corridas_finalizacion(conn)
        _migrate_sesiones_id(conn)
        conn.commit()
    finally:
        conn.close()


MAPA_COLUMNAS_ESPANOL: dict[str, dict[str, str]] = {
    "fuentes": {
        "url_base": "enlace_base",
        "creation_date": "fecha_creacion",
        "last_edit_date": "fecha_ultima_edicion",
    },
    "empresas": {
        "normalized_name": "nombre_normalizado",
        "linkedin": "perfil_linkedin",
        "size": "tamano",
        "creation_date": "fecha_creacion",
        "last_edit_date": "fecha_ultima_edicion",
    },
    "ubicaciones": {
        "creation_date": "fecha_creacion",
        "last_edit_date": "fecha_ultima_edicion",
    },
    "ofertas": {
        "source_identifier": "identificador_origen",
        "url": "enlace",
        "discovery_date": "fecha_descubrimiento",
        "creation_date": "fecha_creacion",
        "last_edit_date": "fecha_ultima_edicion",
        "run_id": "id_corrida",
        "session_id": "id_sesion",
        "set_indice": "indice_set",
        "id_externo_url": "id_externo",
        "timestamp_ultima_verificacion": "fecha_ultima_verificacion",
    },
    "corridas": {
        "run_id": "id_corrida",
        "timestamp_inicio": "fecha_inicio",
        "timestamp_fin": "fecha_fin",
    },
    "eventos": {
        "run_id": "id_corrida",
        "source_id": "fuente_id",
        "session_id": "id_sesion",
        "set_indice": "indice_set",
        "timestamp": "marca_temporal",
        "offer_id": "id_oferta",
    },
    "sesiones": {
        "session_id": "id_sesion",
        "run_id": "id_corrida",
        "source_id": "fuente_id",
        "set_indice": "indice_set",
        "timestamp": "marca_temporal",
        "creation_date": "fecha_creacion",
        "last_edit_date": "fecha_ultima_edicion",
    },
    "bloqueo": {
        "run_id": "id_corrida",
        "timestamp": "marca_temporal",
    },
}

_TABLAS_ESQUEMA: tuple[str, ...] = (
    "fuentes", "empresas", "ubicaciones", "ofertas",
    "corridas", "eventos", "sesiones", "bloqueo",
)


def _migrar_espanol_total(conn: sqlite3.Connection) -> None:
    """D7/D8 migration: full Spanish schema (columns + `ofertas.estado` CHECK).

    Rebuilds each tracked table from the Spanish ESQUEMAS when its current
    schema still uses English column names, mapping old columns to their
    Spanish equivalents (MAPA_COLUMNAS_ESPANOL) so no data is lost and the
    `estado` CHECK constraint is recreated with Spanish values. Runs before
    the legacy migrations so they operate on the Spanish schema. Idempotent:
    a table is rebuilt only when it lacks some expected Spanish column.
    """
    for nombre_tabla in _TABLAS_ESQUEMA:
        filas = conn.execute(
            f"PRAGMA table_info({nombre_tabla})"
        ).fetchall()
        columnas_actuales = {fila["name"] for fila in filas}
        if not columnas_actuales:
            conn.execute(ESQUEMAS[nombre_tabla])
            continue
        conn.execute(
            ESQUEMAS[nombre_tabla].replace(
                f"TABLE IF NOT EXISTS {nombre_tabla}",
                f"TABLE {nombre_tabla}_nueva",
            )
        )
        esperadas = {
            fila["name"]
            for fila in conn.execute(
                f"PRAGMA table_info({nombre_tabla}_nueva)"
            ).fetchall()
        }
        if esperadas.issubset(columnas_actuales):
            conn.execute(f"DROP TABLE {nombre_tabla}_nueva")
            continue
        seleccion = []
        destinos = []
        for columna in columnas_actuales:
            if columna in MAPA_COLUMNAS_ESPANOL[nombre_tabla]:
                nuevo = MAPA_COLUMNAS_ESPANOL[nombre_tabla][columna]
                if nuevo in esperadas:
                    seleccion.append(f"{columna} AS {nuevo}")
                    destinos.append(nuevo)
            elif columna in esperadas:
                if nombre_tabla == "ofertas" and columna == "estado":
                    seleccion.append(
                        "CASE estado WHEN 'discovered' THEN 'descubierta' "
                        "WHEN 'prepared' THEN 'preparada' "
                        "WHEN 'evaluated' THEN 'evaluada' "
                        "WHEN 'accepted' THEN 'aceptada' "
                        "WHEN 'discarded' THEN 'descartada' "
                        "WHEN 'processed' THEN 'procesada' "
                        "WHEN 'finalized' THEN 'finalizada' "
                        "ELSE estado END AS estado"
                    )
                    destinos.append("estado")
                else:
                    seleccion.append(columna)
                    destinos.append(columna)
        conn.execute(
            f"INSERT INTO {nombre_tabla}_nueva ({', '.join(destinos)}) "
            f"SELECT {', '.join(seleccion)} FROM {nombre_tabla}"
        )
        conn.execute(f"DROP TABLE {nombre_tabla}")
        conn.execute(
            f"ALTER TABLE {nombre_tabla}_nueva RENAME TO {nombre_tabla}"
        )
    conn.execute(
        "UPDATE sesiones SET id = id_sesion WHERE id IS NULL OR id = ''"
    )


def _migrate_sesiones_id(conn: sqlite3.Connection) -> None:
    """Sesiones migration: align the table with `escribir_fila` generic inserts.

    `escribir_fila` inserts an `id` (and `fecha_creacion`/`fecha_ultima_edicion`) column
    by default, but the legacy `sesiones` table was declared with
    `id_sesion TEXT PRIMARY KEY` and no `id` column, so every session audit
    insert failed with "table sesiones has no column named id". The table is
    rebuilt with `id TEXT PRIMARY KEY` carrying the id_sesion value.
    Migration is idempotent: it only runs when the `id` column is missing.
    """
    columnas = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(sesiones)").fetchall()
    }
    if "id" in columnas:
        return
    conn.execute("ALTER TABLE sesiones RENAME TO sesiones_legacy")
    conn.execute(ESQUEMAS["sesiones"])
    comunes = [
        nombre
        for nombre in columnas
        if nombre in {
            fila["name"]
            for fila in conn.execute("PRAGMA table_info(sesiones)").fetchall()
        }
    ]
    lista = ", ".join(comunes)
    conn.execute(
        f"INSERT INTO sesiones ({lista}) SELECT {lista} FROM sesiones_legacy"
    )
    conn.execute(
        "UPDATE sesiones SET id = id_sesion WHERE id IS NULL OR id = ''"
    )
    conn.execute("DROP TABLE sesiones_legacy")


def _migrate_ofertas(conn: sqlite3.Connection) -> None:
    """C2 migration: "lo crudo se conserva crudo".

    SQLite cannot drop a NOT NULL constraint in place, so the `ofertas` table
    is rebuilt without NOT NULL on `titulo` and `descripcion_original`, allowing
    capturing raw listings that lack those fields. The columns of traceability
    (`id_corrida`, `id_sesion`, `indice_set`, `id_externo`) are included in the
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
    nuevas = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ofertas_nueva)").fetchall()
    }
    comunes = [
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ofertas)").fetchall()
        if fila["name"] in nuevas
    ]
    lista = ", ".join(comunes)
    conn.execute(
        f"INSERT INTO ofertas_nueva ({lista}) SELECT {lista} FROM ofertas"
    )
    conn.execute("DROP TABLE ofertas")
    conn.execute("ALTER TABLE ofertas_nueva RENAME TO ofertas")


def _migrate_ofertas_empresa_nombre(conn: sqlite3.Connection) -> None:
    """4.4 fix migration: rebuild `ofertas` with FK-free schema + name columns.

    The old schema declared `fuente_id`, `empresa_id` and `ubicacion_id` as
    foreign keys, so capturing without catalog rows failed with FOREIGN KEY
    constraint errors. SQLite cannot drop FK constraints in place, so the
    table is rebuilt from the current schema (no REFERENCES clauses, plus
    `empresa_nombre` and `ubicacion_nombre`). Idempotent: only runs when the
    current table still lacks `empresa_nombre`.
    """
    columnas = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ofertas)").fetchall()
    }
    if "empresa_nombre" in columnas and "ubicacion_nombre" in columnas:
        return
    conn.execute(
        ESQUEMAS["ofertas"].replace("TABLE IF NOT EXISTS ofertas", "TABLE ofertas_nueva")
    )
    nuevas = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ofertas_nueva)").fetchall()
    }
    comunes = [
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ofertas)").fetchall()
        if fila["name"] in nuevas
    ]
    lista = ", ".join(comunes)
    conn.execute(f"INSERT INTO ofertas_nueva ({lista}) SELECT {lista} FROM ofertas")
    conn.execute("DROP TABLE ofertas")
    conn.execute("ALTER TABLE ofertas_nueva RENAME TO ofertas")


def _migrate_ofertas_timestamp_ultima_verificacion(conn: sqlite3.Connection) -> None:
    """4.4 migration: ensure `ofertas.fecha_ultima_verificacion` exists.

    The capture upsert refreshes this column for re-seen listings. The column
    is added on first init if absent; subsequent inits are no-ops.
    """
    columnas = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ofertas)").fetchall()
    }
    if "fecha_ultima_verificacion" not in columnas:
        conn.execute(
            "ALTER TABLE ofertas ADD COLUMN "
            "fecha_ultima_verificacion TEXT DEFAULT ''"
        )


_COLUMNAS_FINALIZACION_CORRIDAS: tuple[str, ...] = (
    "fecha_fin TEXT DEFAULT ''",
    "motivo_terminacion TEXT DEFAULT ''",
    "total_ofertas INTEGER DEFAULT 0",
    "total_errores INTEGER DEFAULT 0",
    "total_sucesos INTEGER DEFAULT 0",
    "fuentes_procesadas INTEGER DEFAULT 0",
)


def _migrate_corridas_finalizacion(conn: sqlite3.Connection) -> None:
    """4.5 migration: add closure metrics columns to `corridas`.

    The Finalizar Proceso node persists closure metrics (fecha_fin,
    motivo_terminacion, total_ofertas, total_errores, total_sucesos,
    fuentes_procesadas) via `actualizar_corrida`. Columns are added one by
    one on first init if absent; subsequent inits are no-ops (idempotent,
    tolerates partially migrated legacy DBs).
    """
    columnas = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(corridas)").fetchall()
    }
    for definicion in _COLUMNAS_FINALIZACION_CORRIDAS:
        nombre_columna = definicion.split(" ")[0]
        if nombre_columna not in columnas:
            conn.execute(f"ALTER TABLE corridas ADD COLUMN {definicion}")


def generar_id(tabla: str) -> str:
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


def leer_tabla(
    tabla: str, filtros: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    conn = _connection()
    try:
        if filtros:
            condiciones = " AND ".join(f"{k} = :{k}" for k in filtros.keys())
            sql = f"SELECT * FROM {tabla} WHERE {condiciones}"
            cursor = conn.execute(sql, dict(filtros))
        else:
            cursor = conn.execute(f"SELECT * FROM {tabla}")
        results: list[dict[str, Any]] = []
        for f in cursor.fetchall():
            r = _deserialize(f)
            if r is not None:
                results.append(r)
        return results
    finally:
        conn.close()


def escribir_fila(tabla: str, datos: dict[str, Any]) -> str:
    d = _serialize(datos)
    if "id" not in d or not d["id"]:
        d["id"] = generar_id(tabla)
    ahora = _now()
    if not d.get("fecha_creacion"):
        d["fecha_creacion"] = ahora
    d["fecha_ultima_edicion"] = ahora

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


def buscar_por_id(tabla: str, id_valor: str) -> dict[str, Any] | None:
    conn = _connection()
    try:
        cursor = conn.execute(f"SELECT * FROM {tabla} WHERE id = ?", (id_valor,))
        return _deserialize(cursor.fetchone())
    finally:
        conn.close()


def actualizar_fila(tabla: str, id_valor: str, datos: dict[str, Any]) -> bool:
    d = _serialize(datos)
    d["fecha_ultima_edicion"] = _now()
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


def escribir_lote(tabla: str, filas: list[dict[str, Any]]) -> None:
    if not filas:
        return
    now = _now()
    preparadas: list[dict[str, Any]] = []
    for datos in filas:
        d = _serialize(datos)
        if "id" not in d or not d["id"]:
            d["id"] = generar_id(tabla)
        if not d.get("fecha_creacion"):
            d["fecha_creacion"] = now
        d["fecha_ultima_edicion"] = now
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


def umbral_obsolescencia_minutos(config: dict[str, Any] | None = None) -> int:
    cfg = config if config is not None else load()
    valor = (cfg.get("concurrencia") or {}).get(
        "umbral_obsolescencia_minutos", 120
    )
    try:
        return int(valor)
    except (TypeError, ValueError):
        return 120


def adquirir_bloqueo(
    id_corrida: str,
    marca_temporal: str,
    forzar: bool = False,
    umbral_minutos: int | None = None,
) -> bool:
    conn = _connection()
    try:
        conn.execute("BEGIN IMMEDIATE")
        fila = conn.execute(
            "SELECT * FROM bloqueo ORDER BY marca_temporal DESC LIMIT 1"
        ).fetchone()
        if fila is None:
            try:
                conn.execute(
                    "INSERT INTO bloqueo (id_corrida, marca_temporal) VALUES (?, ?)",
                    (id_corrida, marca_temporal),
                )
            except sqlite3.IntegrityError:
                conn.rollback()
                return False
            conn.commit()
            return True
        if forzar:
            cursor = conn.execute(
                "UPDATE bloqueo SET id_corrida = ?, marca_temporal = ? WHERE id_corrida = ?",
                (id_corrida, marca_temporal, fila["id_corrida"]),
            )
            if cursor.rowcount == 0:
                conn.rollback()
                return False
            conn.commit()
            return True
        actual = datetime.strptime(fila["marca_temporal"], "%Y-%m-%d %H:%M:%S")
        if umbral_minutos is None:
            umbral_minutos = umbral_obsolescencia_minutos()
        vigente = (
            datetime.now() - actual
        ).total_seconds() / 60 < umbral_minutos if umbral_minutos > 0 else True
        if vigente:
            conn.rollback()
            return False
        cursor = conn.execute(
            "UPDATE bloqueo SET id_corrida = ?, marca_temporal = ? WHERE id_corrida = ?",
            (id_corrida, marca_temporal, fila["id_corrida"]),
        )
        if cursor.rowcount == 0:
            conn.rollback()
            return False
        conn.commit()
        return True
    finally:
        conn.close()


def liberar_bloqueo(id_corrida: str) -> None:
    """Releases the concurrency lock for a run (Finalizar node)."""
    conn = _connection()
    try:
        conn.execute("DELETE FROM bloqueo WHERE id_corrida = ?", (id_corrida,))
        conn.commit()
    finally:
        conn.close()


def consultar_bloqueo() -> dict[str, Any] | None:
    conn = _connection()
    try:
        fila = conn.execute(
            "SELECT * FROM bloqueo ORDER BY marca_temporal DESC LIMIT 1"
        ).fetchone()
        return dict(fila) if fila is not None else None
    finally:
        conn.close()


def sondear_escritura() -> None:
    """VAL-03 probe: INSERT with immediate rollback on the bloqueo table."""
    try:
        conn = _connection()
    except sqlite3.Error as exc:
        raise PersistenceError("01", f"Connection failed: {exc}") from exc
    try:
        conn.execute(
            "INSERT INTO bloqueo (id_corrida, marca_temporal) VALUES (?, ?)",
            (f"PROBE-{uuid.uuid4().hex[:8]}", _now()),
        )
        conn.rollback()
    except sqlite3.Error as exc:
        raise PersistenceError("01", f"Write probe failed: {exc}") from exc
    finally:
        conn.close()


def registrar_corrida(datos: dict[str, Any]) -> None:
    """Registers a run row in `corridas`, idempotent per id_corrida."""
    d = _serialize(datos)
    conn = _connection()
    try:
        conn.execute(
            "INSERT INTO corridas (id_corrida, fecha_inicio, estado) "
            "VALUES (:id_corrida, :fecha_inicio, :estado) "
            "ON CONFLICT (id_corrida) DO NOTHING",
            {
                "id_corrida": d["id_corrida"],
                "fecha_inicio": d.get("fecha_inicio") or _now(),
                "estado": d.get("estado") or "",
            },
        )
        conn.commit()
    finally:
        conn.close()


def actualizar_corrida(id_corrida: str, campos: dict[str, Any]) -> bool:
    """Updates the `corridas` row of a run; returns whether a row matched.

    Closes a run (Finalizar Proceso node): persists the final state and the
    closure metrics (`fecha_fin`, `motivo_terminacion`, `total_ofertas`,
    `total_errores`, `total_sucesos`, `fuentes_procesadas`). Follows the
    `actualizar_fila` pattern; `corridas` is keyed by `id_corrida` instead of `id`.
    """
    d = _serialize(campos)
    asignaciones = ", ".join(f"{k} = :{k}" for k in d.keys())
    d["_run_id"] = id_corrida
    sql = f"UPDATE corridas SET {asignaciones} WHERE id_corrida = :_run_id"
    conn = _connection()
    try:
        cursor = conn.execute(sql, d)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()


def upsert_oferta(oferta: dict[str, Any]) -> str:
    """Inserts or updates an offer by `id_externo`.

    If a row with the same `id_externo` already exists, only its
    `fecha_ultima_verificacion` is refreshed and its `id` is returned.
    Otherwise a new `id` is generated and the row is inserted.

    Returns:
        The offer `id` (str).
    """
    d = dict(oferta)
    id_externo = d.get("id_externo")
    if id_externo:
        existentes = leer_tabla("ofertas", {"id_externo": id_externo})
        if existentes:
            actualizar_fila(
                "ofertas",
                cast(str, existentes[0]["id"]),
                {"fecha_ultima_verificacion": _now()},
            )
            return cast(str, existentes[0]["id"])
    if "id" not in d or not d["id"]:
        d["id"] = generar_id("ofertas")
    return escribir_fila("ofertas", d)


def escribir_evento(datos: dict[str, Any]) -> str:
    """Registers an event/success row in `eventos`; returns its evento_id."""
    d = _serialize(datos)
    evento_id = str(d.get("evento_id") or generar_id("eventos"))
    d["evento_id"] = evento_id
    if not d.get("marca_temporal"):
        d["marca_temporal"] = _now()
    columnas = ", ".join(d.keys())
    placeholders = ", ".join(f":{k}" for k in d.keys())
    conn = _connection()
    try:
        conn.execute(f"INSERT INTO eventos ({columnas}) VALUES ({placeholders})", d)
        conn.commit()
        return evento_id
    finally:
        conn.close()
