import json
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from loguru import logger

from shared.config import load
from shared.errors import PersistenceError
from shared.models import Corrida, EventoAlmacen
from shared.utilidades import ahora

_DB_PATH: Path | None = None

PREFIXES: dict[str, str] = {
    "empresas": "EMP",
    "ubicaciones": "UBI",
    "ofertas_descubiertas": "OFE",
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
        "ciudad TEXT DEFAULT 'N/A',"
        "region TEXT DEFAULT 'N/A',"
        "pais TEXT DEFAULT 'N/A',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT ''"
        ")"
    ),
    "ofertas_descubiertas": (
        "CREATE TABLE IF NOT EXISTS ofertas_descubiertas ("
        "id TEXT PRIMARY KEY,"
        "enlace TEXT NOT NULL,"
        "titulo TEXT DEFAULT '',"
        "descripcion_original TEXT DEFAULT 'N/A',"
        "fecha_publicacion TEXT DEFAULT 'N/A',"
        "fecha_descubrimiento TEXT DEFAULT '',"
        "estado TEXT DEFAULT 'descubierta' "
        "CHECK(estado IN ('descubierta','preparada','duplicada','evaluada',"
        "'aceptada','descartada','procesada','finalizada')),"
        "observaciones TEXT DEFAULT 'N/A',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_ultima_edicion TEXT DEFAULT '',"
        "fuente_id TEXT DEFAULT '',"
        "empresa_id TEXT DEFAULT 'N/A',"
        "ubicacion_id TEXT DEFAULT 'N/A',"
        "id_corrida TEXT DEFAULT '',"
        "id_sesion TEXT DEFAULT '',"
        "indice_set INTEGER DEFAULT '',"
        "id_externo TEXT DEFAULT '',"
        "fecha_ultima_verificacion TEXT DEFAULT '',"
        "id_duplicidad TEXT DEFAULT 'N/A',"
        "ubicacion_nombre TEXT DEFAULT 'N/A',"
        "modalidad TEXT DEFAULT 'N/A'"
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
        "fuentes_procesadas INTEGER DEFAULT 0,"
        "total_preparadas INTEGER DEFAULT 0,"
        "total_duplicadas INTEGER DEFAULT 0"
        ")"
    ),
    "eventos": (
        "CREATE TABLE IF NOT EXISTS eventos ("
        "evento_id TEXT PRIMARY KEY,"
        "id_corrida TEXT NOT NULL,"
        "fuente_id TEXT DEFAULT 'N/A',"
        "id_sesion TEXT DEFAULT 'N/A',"
        "indice_set INTEGER DEFAULT 'N/A',"
        "marca_temporal TEXT NOT NULL,"
        "tipo TEXT NOT NULL CHECK(tipo IN ('error','suceso')),"
        "codigo TEXT NOT NULL,"
        "evidencia TEXT DEFAULT 'N/A',"
        "id_oferta TEXT DEFAULT 'N/A'"
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

_INDICES: tuple[str, ...] = (
    "CREATE INDEX IF NOT EXISTS idx_ofertas_id_externo "
    "ON ofertas_descubiertas(id_externo)",
    "CREATE INDEX IF NOT EXISTS idx_ofertas_id_corrida "
    "ON ofertas_descubiertas(id_corrida)",
    "CREATE INDEX IF NOT EXISTS idx_eventos_id_corrida ON eventos(id_corrida)",
)


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


def init_db() -> None:
    conn = _connection()
    try:
        _migrate_ofertas_descubiertas(conn)
        tablas = ("secuencia_ids", "empresas", "ubicaciones",
                  "ofertas_descubiertas", "corridas", "eventos",
                  "sesiones", "bloqueo")
        for nombre_tabla in tablas:
            conn.execute(ESQUEMAS[nombre_tabla])
        _migrar_espanol_total(conn)
        _migrate_ofertas(conn)
        _migrate_ofertas_timestamp_ultima_verificacion(conn)
        _migrate_ofertas_empresa_nombre(conn)
        _migrate_corridas_finalizacion(conn)
        _migrate_sesiones_id(conn)
        _migrate_limpieza_d31(conn)
        _migrate_preparacion_d33(conn)
        for sentencia in _INDICES:
            conn.execute(sentencia)
        conn.commit()
    finally:
        conn.close()


def _migrate_ofertas_descubiertas(conn: sqlite3.Connection) -> None:
    """D32 migration: rename the `ofertas` table to `ofertas_descubiertas`.

    Renames the physical table when a DB created before decision D32 still
    holds `ofertas`; SQLite keeps the indexes under their same names and the
    `secuencia_ids` row is updated so the next generated id continues the
    `OFE` sequence without collisions. Runs before the schema creation loop
    so the new `CREATE TABLE IF NOT EXISTS` never creates an empty duplicate.
    Idempotent: no-op when the rename is already applied.
    """
    tablas = {
        fila["name"]
        for fila in conn.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table'"
        ).fetchall()
    }
    if "ofertas" in tablas and "ofertas_descubiertas" not in tablas:
        conn.execute("ALTER TABLE ofertas RENAME TO ofertas_descubiertas")
    if "secuencia_ids" in tablas:
        conn.execute(
            "UPDATE secuencia_ids SET tabla_nombre = 'ofertas_descubiertas' "
            "WHERE tabla_nombre = 'ofertas'"
        )


MAPA_COLUMNAS_ESPANOL: dict[str, dict[str, str]] = {
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
    "ofertas_descubiertas": {
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
    "empresas", "ubicaciones", "ofertas_descubiertas",
    "corridas", "eventos", "sesiones", "bloqueo",
)


def _migrar_espanol_total(conn: sqlite3.Connection) -> None:
    """D7/D8 migration: full Spanish schema (columns + `ofertas_descubiertas.estado` CHECK).

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
                if nombre_tabla == "ofertas_descubiertas" and columna == "estado":
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

    SQLite cannot drop a NOT NULL constraint in place, so the
    `ofertas_descubiertas` table is rebuilt without NOT NULL on `titulo` and
    `descripcion_original`, allowing capturing raw listings that lack those
    fields. The columns of traceability (`id_corrida`, `id_sesion`,
    `indice_set`, `id_externo`) are included in the new schema. Migration is
    idempotent: it only runs when the current schema still declares
    `titulo NOT NULL`.
    """
    columnas = {
        fila["name"]: fila["notnull"]
        for fila in conn.execute(
            "PRAGMA table_info(ofertas_descubiertas)"
        ).fetchall()
    }
    if "titulo" in columnas and columnas["titulo"] == 0:
        return
    conn.execute(
        ESQUEMAS["ofertas_descubiertas"].replace(
            "TABLE IF NOT EXISTS ofertas_descubiertas",
            "TABLE ofertas_descubiertas_nueva",
        )
    )
    nuevas = {
        fila["name"]
        for fila in conn.execute(
            "PRAGMA table_info(ofertas_descubiertas_nueva)"
        ).fetchall()
    }
    comunes = [
        fila["name"]
        for fila in conn.execute(
            "PRAGMA table_info(ofertas_descubiertas)"
        ).fetchall()
        if fila["name"] in nuevas
    ]
    lista = ", ".join(comunes)
    conn.execute(
        f"INSERT INTO ofertas_descubiertas_nueva ({lista}) SELECT {lista} "
        "FROM ofertas_descubiertas"
    )
    conn.execute("DROP TABLE ofertas_descubiertas")
    conn.execute(
        "ALTER TABLE ofertas_descubiertas_nueva "
        "RENAME TO ofertas_descubiertas"
    )


def _migrate_ofertas_empresa_nombre(conn: sqlite3.Connection) -> None:
    """D29 migration: drop `empresa_nombre` from `ofertas_descubiertas`.

    D4 (2026-08-09) added raw-string company/location columns; D29
    (2026-08-17) removes them from the model: the adapter no longer
    extracts company/location from the cards (only the publication date),
    so raw strings are not persisted. SQLite >= 3.35 supports in-place
    `ALTER TABLE ... DROP COLUMN`; each column is dropped only if present
    (idempotent). `ubicacion_nombre` is NO LONGER dropped here: decision
    D33 re-adds it for Module 2 (partial D29 reversal), so dropping it
    first would silently destroy pre-D29 values.
    """
    columnas = {
        fila["name"]
        for fila in conn.execute(
            "PRAGMA table_info(ofertas_descubiertas)"
        ).fetchall()
    }
    if "empresa_nombre" in columnas:
        conn.execute(
            "ALTER TABLE ofertas_descubiertas DROP COLUMN empresa_nombre"
        )


def _migrate_ofertas_timestamp_ultima_verificacion(conn: sqlite3.Connection) -> None:
    """4.4 migration: ensure `ofertas_descubiertas.fecha_ultima_verificacion` exists.

    The capture upsert refreshes this column for re-seen listings. The column
    is added on first init if absent; subsequent inits are no-ops.
    """
    columnas = {
        fila["name"]
        for fila in conn.execute(
            "PRAGMA table_info(ofertas_descubiertas)"
        ).fetchall()
    }
    if "fecha_ultima_verificacion" not in columnas:
        conn.execute(
            "ALTER TABLE ofertas_descubiertas ADD COLUMN "
            "fecha_ultima_verificacion TEXT DEFAULT ''"
        )


def _migrate_limpieza_d31(conn: sqlite3.Connection) -> None:
    """D31 migration: schema cleanup + no-empty-field rule (N/A).

    (1) Drops the `fuentes` table and its `secuencia_ids` row (sources are
    config-driven; the catalog was never populated).
    (2) Drops `ofertas_descubiertas.identificador_origen` (dead duplicate of
    `id_externo`). `eventos.id_oferta` is NO LONGER dropped here: decision
    D33 re-adds it for Module 2 per-offer traceability, superseding D31 D-1
    on that column.
    (3) Backfills the no-empty-field rule (decision D31): empty/NULL values
    in the non-nullable-by-semantics columns become 'N/A' so no field stays
    empty (the backfill updates are per-column and safe no-ops when no row
    matches; the DROP COLUMN steps are guarded by a column-presence check).
    `ofertas_descubiertas.fecha_ultima_verificacion` is exempted (only
    refreshed on re-visits; D31 point 4 keeps its current behavior).
    Idempotent: every destructive step only runs when its target is present.
    """
    conn.execute("DROP TABLE IF EXISTS fuentes")
    conn.execute("DELETE FROM secuencia_ids WHERE tabla_nombre = 'fuentes'")
    actuales_ofertas = {
        fila["name"]
        for fila in conn.execute(
            "PRAGMA table_info(ofertas_descubiertas)"
        ).fetchall()
    }
    if "identificador_origen" in actuales_ofertas:
        conn.execute(
            "ALTER TABLE ofertas_descubiertas DROP COLUMN identificador_origen"
        )
    for columna in (
        "descripcion_original",
        "fecha_publicacion",
        "observaciones",
        "empresa_id",
        "ubicacion_id",
    ):
        conn.execute(
            f"UPDATE ofertas_descubiertas SET {columna} = 'N/A' "
            f"WHERE {columna} IS NULL OR {columna} = ''"
        )
    for columna in ("fuente_id", "id_sesion", "indice_set", "evidencia"):
        conn.execute(
            f"UPDATE eventos SET {columna} = 'N/A' "
            f"WHERE {columna} IS NULL OR {columna} = ''"
        )


_ADICIONES_PREPARACION: tuple[tuple[str, str], ...] = (
    ("ofertas_descubiertas", "id_duplicidad TEXT DEFAULT 'N/A'"),
    ("ofertas_descubiertas", "ubicacion_nombre TEXT DEFAULT 'N/A'"),
    ("ofertas_descubiertas", "modalidad TEXT DEFAULT 'N/A'"),
    ("corridas", "total_preparadas INTEGER DEFAULT 0"),
    ("corridas", "total_duplicadas INTEGER DEFAULT 0"),
    ("eventos", "id_oferta TEXT DEFAULT 'N/A'"),
)


def _migrate_preparacion_d33(conn: sqlite3.Connection) -> None:
    """D33 migration: Module 2 (Preparation) consolidated schema dependencies.

    (1) Adds the preparation columns when absent (on legacy DBs the
    `_migrar_espanol_total` rebuild usually applies them from ESQUEMAS; this
    guarded pass is the explicit safety net): `ofertas_descubiertas`.
    `id_duplicidad`/`ubicacion_nombre`/`modalidad` ('N/A'), `corridas`.
    `total_preparadas`/`total_duplicadas` (0) and `eventos`.`id_oferta`
    ('N/A'; re-added, superseding D31 D-1).
    (2) Drops `ubicaciones.modalidad`: `ubicaciones` is restructured to the
    `(ciudad, region, pais)` tuple (components default 'N/A'); the extra
    column does not trigger the rebuild path, so the drop must be explicit.
    The `estado` CHECK with 'duplicada' comes from the updated ESQUEMAS via
    the same rebuild. Idempotent: every step only runs when its target is
    present.
    """
    columnas_por_tabla = {
        tabla: {
            fila["name"]
            for fila in conn.execute(f"PRAGMA table_info({tabla})").fetchall()
        }
        for tabla in ("ofertas_descubiertas", "corridas", "eventos")
    }
    for tabla, definicion in _ADICIONES_PREPARACION:
        nombre_columna = definicion.split(" ")[0]
        if nombre_columna not in columnas_por_tabla[tabla]:
            conn.execute(f"ALTER TABLE {tabla} ADD COLUMN {definicion}")
    columnas_ubicaciones = {
        fila["name"]
        for fila in conn.execute("PRAGMA table_info(ubicaciones)").fetchall()
    }
    if "modalidad" in columnas_ubicaciones:
        conn.execute("ALTER TABLE ubicaciones DROP COLUMN modalidad")


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


def _generar_id_en(conn: sqlite3.Connection, tabla: str) -> str:
    """Generates the next sequential id for `tabla` on an existing connection.

    Reads the `RETURNING` value of the single upsert statement, so no extra
    SELECT is needed. The caller decides when to commit.
    """
    prefijo = PREFIXES.get(tabla)
    if prefijo is None:
        disponibles = list(PREFIXES.keys())
        raise ValueError(f"Unknown table: {tabla}. Available prefixes: {disponibles}")
    fila = conn.execute(
        "INSERT INTO secuencia_ids (tabla_nombre, prefijo, ultimo_numero) VALUES (?, ?, 1) "
        "ON CONFLICT(tabla_nombre) DO UPDATE SET ultimo_numero = ultimo_numero + 1 "
        "RETURNING ultimo_numero",
        (tabla, prefijo),
    ).fetchone()
    assert fila is not None
    return f"{prefijo}-{int(fila[0]):04d}"


def generar_id(tabla: str) -> str:
    conn = _connection()
    try:
        resultado = _generar_id_en(conn, tabla)
        conn.commit()
        return resultado
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


def contar_filas(tabla: str, filtros: dict[str, Any] | None = None) -> int:
    """Counts rows of a table; optional equality filters."""
    conn = _connection()
    try:
        if filtros:
            condiciones = " AND ".join(f"{k} = :{k}" for k in filtros.keys())
            cursor = conn.execute(
                f"SELECT COUNT(*) FROM {tabla} WHERE {condiciones}", dict(filtros)
            )
        else:
            cursor = conn.execute(f"SELECT COUNT(*) FROM {tabla}")
        fila = cursor.fetchone()
        return int(fila[0]) if fila is not None else 0
    finally:
        conn.close()


def contar_distintos(
    tabla: str, columna: str, filtros: dict[str, Any] | None = None
) -> int:
    """Counts distinct non-empty values of a column (equality filters).

    Empty values are NULL, '' and 'N/A' (no-empty-field rule, decision D31:
    'N/A' is the placeholder for not-applicable fields).
    """
    conn = _connection()
    try:
        condiciones = (
            f"{columna} IS NOT NULL AND {columna} != '' "
            f"AND {columna} != 'N/A'"
        )
        params: dict[str, Any] = {}
        if filtros:
            condiciones += " AND " + " AND ".join(f"{k} = :{k}" for k in filtros.keys())
            params = dict(filtros)
        cursor = conn.execute(
            f"SELECT COUNT(DISTINCT {columna}) FROM {tabla} WHERE {condiciones}",
            params,
        )
        fila = cursor.fetchone()
        return int(fila[0]) if fila is not None else 0
    finally:
        conn.close()


def escribir_fila(tabla: str, datos: dict[str, Any]) -> str:
    d = _serialize(datos)
    if "id" not in d or not d["id"]:
        d["id"] = generar_id(tabla)
    marca = ahora()
    if not d.get("fecha_creacion"):
        d["fecha_creacion"] = marca
    d["fecha_ultima_edicion"] = marca

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
    d["fecha_ultima_edicion"] = ahora()
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
            (f"PROBE-{uuid.uuid4().hex[:8]}", ahora()),
        )
        conn.rollback()
    except sqlite3.Error as exc:
        raise PersistenceError("01", f"Write probe failed: {exc}") from exc
    finally:
        conn.close()


def registrar_corrida(datos: dict[str, Any]) -> None:
    """Registers a run row in `corridas`, idempotent per id_corrida.

    Validates the row against `Corrida` (Pydantic) before writing so schema
    drift surfaces at runtime instead of producing silently corrupted rows.
    """
    Corrida.model_validate(datos)
    d = _serialize(datos)
    conn = _connection()
    try:
        conn.execute(
            "INSERT INTO corridas (id_corrida, fecha_inicio, estado) "
            "VALUES (:id_corrida, :fecha_inicio, :estado) "
            "ON CONFLICT (id_corrida) DO NOTHING",
            {
                "id_corrida": d["id_corrida"],
                "fecha_inicio": d.get("fecha_inicio") or ahora(),
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
    Validates the closure fields against `Corrida` (Pydantic) before writing
    so schema drift surfaces at runtime (P4-13; deferred from D23).
    """
    Corrida(id_corrida=id_corrida, **campos)
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


def _upsert_ofertas_en(
    conn: sqlite3.Connection, filas: list[dict[str, Any]]
) -> tuple[list[str], int]:
    """Upserts offers on an existing connection, dedup by `id_externo`.

    Existing rows only refresh `fecha_ultima_verificacion`; new rows get a
    generated `id` on the same connection. Row-level failures are logged and
    counted without aborting the remaining rows; the caller commits.
    Returns (ids_registradas, fallidas). No-empty-field rule (D31): empty
    values in `descripcion_original`/`fecha_publicacion`/`observaciones`/
    `empresa_id`/`ubicacion_id` are persisted as 'N/A'.
    """
    registradas: list[str] = []
    fallidas = 0
    if not filas:
        return registradas, fallidas
    preparadas = [_serialize(dict(f)) for f in filas]
    for d in preparadas:
        for campo in (
            "descripcion_original",
            "fecha_publicacion",
            "observaciones",
            "empresa_id",
            "ubicacion_id",
        ):
            if not d.get(campo):
                d[campo] = "N/A"
    id_externos = [d.get("id_externo") for d in preparadas if d.get("id_externo")]
    ids_por_id_externo: dict[str, str] = {}
    if id_externos:
        marcas = ",".join("?" for _ in id_externos)
        for fila in conn.execute(
            "SELECT id_externo, id FROM ofertas_descubiertas "
            f"WHERE id_externo IN ({marcas})",
            id_externos,
        ).fetchall():
            ids_por_id_externo[str(fila["id_externo"])] = str(fila["id"])
    marca = ahora()
    for d in preparadas:
        try:
            id_externo = d.get("id_externo")
            if id_externo and id_externo in ids_por_id_externo:
                conn.execute(
                    "UPDATE ofertas_descubiertas "
                    "SET fecha_ultima_verificacion = ? WHERE id = ?",
                    (marca, ids_por_id_externo[id_externo]),
                )
                registradas.append(ids_por_id_externo[id_externo])
                continue
            if not d.get("id"):
                d["id"] = _generar_id_en(conn, "ofertas_descubiertas")
            if not d.get("fecha_creacion"):
                d["fecha_creacion"] = marca
            d["fecha_ultima_edicion"] = marca
            columnas = list(d.keys())
            placeholders = [":" + k for k in d.keys()]
            conn.execute(
                "INSERT INTO ofertas_descubiertas "
                f"({', '.join(columnas)}) VALUES ({', '.join(placeholders)})",
                d,
            )
            registradas.append(cast(str, d["id"]))
            if id_externo:
                ids_por_id_externo[id_externo] = cast(str, d["id"])
        except Exception as exc:
            logger.error(
                f"Oferta no registrada en lote | "
                f"id_externo={d.get('id_externo')} | "
                f"id_corrida={d.get('id_corrida')} | {exc}"
            )
            fallidas += 1
    return registradas, fallidas


def upsert_lote_ofertas(filas: list[dict[str, Any]]) -> tuple[int, int]:
    """Inserts or updates a batch of offers in a single connection.

    Deduplicates by `id_externo` like `upsert_oferta` but in one
    transaction. Returns (registradas, fallidas); row-level failures never
    abort the remaining rows. Connection failures raise.
    """
    if not filas:
        return 0, 0
    conn = _connection()
    try:
        ids, fallidas = _upsert_ofertas_en(conn, filas)
        conn.commit()
        return len(ids), fallidas
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def upsert_oferta(oferta: dict[str, Any]) -> str:
    """Inserts or updates a single offer by `id_externo` (public API).

    Thin wrapper over the batch upsert; returns the offer `id` (str).
    A row rejected at row level raises `PersistenceError` instead of the
    misleading `IndexError` of an empty result list.
    """
    conn = _connection()
    try:
        ids, _ = _upsert_ofertas_en(conn, [oferta])
        if not ids:
            raise PersistenceError(
                "09",
                f"Oferta no registrada (fila inválida) | "
                f"id_externo={oferta.get('id_externo')}",
            )
        conn.commit()
        return ids[0]
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def escribir_evento(datos: dict[str, Any]) -> str:
    """Registers an event/success row in `eventos`; returns its evento_id.

    Validates the row against `EventoAlmacen` (Pydantic) before writing so
    schema drift surfaces at runtime instead of producing corrupted rows.
    """
    EventoAlmacen.model_validate(datos)
    d = _serialize(datos)
    for campo in ("fuente_id", "id_sesion", "evidencia", "id_oferta"):
        if not d.get(campo):
            d[campo] = "N/A"
    if d.get("indice_set") is None:
        d["indice_set"] = "N/A"
    evento_id = str(d.get("evento_id") or generar_id("eventos"))
    d["evento_id"] = evento_id
    if not d.get("marca_temporal"):
        d["marca_temporal"] = ahora()
    columnas = ", ".join(d.keys())
    placeholders = ", ".join(f":{k}" for k in d.keys())
    conn = _connection()
    try:
        conn.execute(f"INSERT INTO eventos ({columnas}) VALUES ({placeholders})", d)
        conn.commit()
        return evento_id
    finally:
        conn.close()


def escribir_evento_seguro(datos: dict[str, Any], contexto_log: str = "") -> None:
    """Writes an event best-effort: never aborts, falls back to Loguru.

    Single non-aborting wrapper replacing the per-node try/except copies
    (inicio, captura, control_fuentes, registro, finalizar). The node
    builds the full row dict; validation and persistence stay in
    `escribir_evento`.
    """
    try:
        escribir_evento(datos)
    except Exception as exc:
        run = contexto_log or str(datos.get("id_corrida", ""))
        codigo = str(datos.get("codigo", ""))
        logger.error(f"Evento no persistible | run={run} | codigo={codigo} | {exc}")
