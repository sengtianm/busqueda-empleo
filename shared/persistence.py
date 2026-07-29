import json
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any, cast

from shared.config import cargar

_DB_PATH: Path | None = None

PREFIJOS: dict[str, str] = {
    "fuentes": "FNT",
    "empresas": "EMP",
    "ubicaciones": "UBI",
    "ofertas": "OFE",
    "ofertas_procesadas": "OFP",
    "evaluaciones": "EVL",
    "resultados_procesamiento": "RSP",
}

COLUMNAS_JSON: set[str] = {
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
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_actualizacion TEXT DEFAULT ''"
        ")"
    ),
    "empresas": (
        "CREATE TABLE IF NOT EXISTS empresas ("
        "id TEXT PRIMARY KEY,"
        "nombre TEXT NOT NULL,"
        "nombre_normalizado TEXT DEFAULT '',"
        "sitio_web TEXT DEFAULT '',"
        "linkedin TEXT DEFAULT '',"
        "sector TEXT DEFAULT '',"
        "tamano TEXT DEFAULT '',"
        "descripcion TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_actualizacion TEXT DEFAULT ''"
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
        "fecha_actualizacion TEXT DEFAULT ''"
        ")"
    ),
    "ofertas": (
        "CREATE TABLE IF NOT EXISTS ofertas ("
        "id TEXT PRIMARY KEY,"
        "fuente_id TEXT REFERENCES fuentes(id),"
        "empresa_id TEXT REFERENCES empresas(id),"
        "ubicacion_id TEXT REFERENCES ubicaciones(id),"
        "identificador_fuente TEXT DEFAULT '',"
        "url TEXT NOT NULL,"
        "titulo TEXT NOT NULL,"
        "descripcion_original TEXT NOT NULL,"
        "fecha_publicacion TEXT DEFAULT '',"
        "fecha_descubrimiento TEXT DEFAULT '',"
        "estado TEXT DEFAULT 'descubierta',"
        "activa INTEGER DEFAULT 1,"
        "observaciones TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_actualizacion TEXT DEFAULT ''"
        ")"
    ),
    "ofertas_procesadas": (
        "CREATE TABLE IF NOT EXISTS ofertas_procesadas ("
        "id TEXT PRIMARY KEY,"
        "oferta_id TEXT REFERENCES ofertas(id),"
        "titulo_limpio TEXT DEFAULT '',"
        "descripcion_limpia TEXT DEFAULT '',"
        "salario_min REAL,"
        "salario_max REAL,"
        "moneda TEXT DEFAULT '',"
        "ubicacion_limpia TEXT DEFAULT '',"
        "modalidad TEXT DEFAULT '',"
        "requisitos TEXT DEFAULT '[]',"
        "tecnologias TEXT DEFAULT '[]',"
        "idiomas TEXT DEFAULT '[]',"
        "experiencia_anios INTEGER,"
        "fecha_procesamiento TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_actualizacion TEXT DEFAULT ''"
        ")"
    ),
    "evaluaciones": (
        "CREATE TABLE IF NOT EXISTS evaluaciones ("
        "id TEXT PRIMARY KEY,"
        "oferta_procesada_id TEXT REFERENCES ofertas_procesadas(id),"
        "resultado TEXT NOT NULL,"
        "puntaje REAL NOT NULL,"
        "umbral_aprobacion REAL DEFAULT 50.0,"
        "decision TEXT NOT NULL,"
        "justificacion TEXT DEFAULT '',"
        "criterios_evaluados TEXT DEFAULT '',"
        "fecha_evaluacion TEXT DEFAULT '',"
        "version_modelo TEXT DEFAULT 'v1',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_actualizacion TEXT DEFAULT ''"
        ")"
    ),
    "resultados_procesamiento": (
        "CREATE TABLE IF NOT EXISTS resultados_procesamiento ("
        "id TEXT PRIMARY KEY,"
        "oferta_procesada_id TEXT REFERENCES ofertas_procesadas(id),"
        "diagnostico TEXT DEFAULT '',"
        "extraccion_estrategica TEXT DEFAULT '',"
        "diseno_candidatura TEXT DEFAULT '',"
        "borrador_carta TEXT DEFAULT '',"
        "preparacion_entrevista TEXT DEFAULT '',"
        "fecha_procesamiento TEXT DEFAULT '',"
        "fecha_creacion TEXT DEFAULT '',"
        "fecha_actualizacion TEXT DEFAULT ''"
        ")"
    ),
}


def _ruta_bd() -> Path:
    if _DB_PATH is not None:
        return _DB_PATH
    cfg = cargar()
    return Path(cfg.get("persistencia", {}).get("archivo_bd", "data/busqueda_empleo.db"))


def cambiar_ruta(ruta: Path) -> None:
    global _DB_PATH
    _DB_PATH = ruta


def restablecer_ruta() -> None:
    global _DB_PATH
    _DB_PATH = None


def _conexion() -> sqlite3.Connection:
    ruta = _ruta_bd()
    ruta.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(ruta))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def _ahora() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def _serializar(datos: dict[str, Any]) -> dict[str, Any]:
    d = dict(datos)
    for k, v in d.items():
        if isinstance(v, datetime):
            d[k] = v.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(v, bool):
            d[k] = 1 if v else 0
        elif isinstance(v, (list, dict)):
            d[k] = json.dumps(v, ensure_ascii=False)
    return d


def _deserializar(fila: sqlite3.Row | None) -> dict[str, Any] | None:
    if fila is None:
        return None
    d = dict(fila)
    for k, v in d.items():
        if isinstance(v, int) and k == "activa":
            d[k] = bool(v)
        elif isinstance(v, str) and k in COLUMNAS_JSON:
            try:
                d[k] = json.loads(v)
            except (json.JSONDecodeError, TypeError):
                pass
    return d


def inicializar_bd() -> None:
    conn = _conexion()
    try:
        tablas = ("secuencia_ids", "fuentes", "empresas", "ubicaciones",
                  "ofertas", "ofertas_procesadas", "evaluaciones",
                  "resultados_procesamiento")
        for nombre_tabla in tablas:
            conn.execute(ESQUEMAS[nombre_tabla])
        conn.commit()
    finally:
        conn.close()


def generar_id(tabla: str) -> str:
    prefijo = PREFIJOS.get(tabla)
    if prefijo is None:
        disponibles = list(PREFIJOS.keys())
        raise ValueError(f"Tabla desconocida: {tabla}. Prefijos disponibles: {disponibles}")
    conn = _conexion()
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


def leer_tabla(tabla: str) -> list[dict[str, Any]]:
    conn = _conexion()
    try:
        cursor = conn.execute(f"SELECT * FROM {tabla}")
        resultados: list[dict[str, Any]] = []
        for f in cursor.fetchall():
            r = _deserializar(f)
            if r is not None:
                resultados.append(r)
        return resultados
    finally:
        conn.close()


def escribir_fila(tabla: str, datos: dict[str, Any]) -> str:
    d = _serializar(datos)
    if "id" not in d or not d["id"]:
        d["id"] = generar_id(tabla)
    ahora = _ahora()
    if not d.get("fecha_creacion"):
        d["fecha_creacion"] = ahora
    d["fecha_actualizacion"] = ahora

    columnas = [k for k in d.keys()]
    placeholders = [":" + k for k in d.keys()]
    sql = f"INSERT INTO {tabla} ({', '.join(columnas)}) VALUES ({', '.join(placeholders)})"
    conn = _conexion()
    try:
        conn.execute(sql, d)
        conn.commit()
        return cast(str, d["id"])
    finally:
        conn.close()


def buscar_por_id(tabla: str, id_valor: str) -> dict[str, Any] | None:
    conn = _conexion()
    try:
        cursor = conn.execute(f"SELECT * FROM {tabla} WHERE id = ?", (id_valor,))
        return _deserializar(cursor.fetchone())
    finally:
        conn.close()


def actualizar(tabla: str, id_valor: str, datos: dict[str, Any]) -> bool:
    d = _serializar(datos)
    d["fecha_actualizacion"] = _ahora()
    if "id" in d:
        del d["id"]
    asignaciones = ", ".join(f"{k} = :{k}" for k in d.keys())
    d["_id_valor"] = id_valor
    sql = f"UPDATE {tabla} SET {asignaciones} WHERE id = :_id_valor"
    conn = _conexion()
    try:
        cursor = conn.execute(sql, d)
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
