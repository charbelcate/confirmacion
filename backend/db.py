# -*- coding: utf-8 -*-
"""
Persistencia del progreso del niño — separada de la base de conocimiento
(content.py), tal como define el modelo: "El conocimiento se mantendrá
separado de las actividades y de los datos personales del niño."

Se usa SQLite para este piloto (cero configuración). El documento maestro ya
prevé migrar a PostgreSQL cuando el proyecto pase a producción; el código de
la API no tendría que cambiar mucho porque las consultas son simples.

No se guarda ningún dato personal del niño: solo un "código" que asigna el
catequista (por ejemplo, un nombre corto o un código de grupo), sin correo,
sin apellido, sin datos identificables.
"""
import sqlite3
import datetime
import os

# El archivo de la base de datos vive dentro de una subcarpeta dedicada
# ("db_persistent") en vez de suelto en backend/, para que coincida con la
# ruta que se monta como volumen persistente en producción (Easypanel,
# sección "Almacenamiento" del servicio) — así el progreso sobrevive cada
# vez que se reconstruye el contenedor. Mismo patrón que el tutor de
# Primera Comunión. Se puede cambiar sin tocar código con la variable de
# entorno CATEQUESIS_DATA_DIR, por si el volumen se monta en otra ruta.
_CARPETA_DATOS = os.environ.get("CATEQUESIS_DATA_DIR") or os.path.join(
    os.path.dirname(__file__), "db_persistent"
)
os.makedirs(_CARPETA_DATOS, exist_ok=True)
DB_PATH = os.path.join(_CARPETA_DATOS, "catequesis_confirmacion.db")


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_conn()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS ninos (
        codigo TEXT PRIMARY KEY,
        creado_en TEXT
    );

    CREATE TABLE IF NOT EXISTS intentos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        codigo_nino TEXT,
        encuentro_id TEXT,
        contenido_id TEXT,
        actividad_id TEXT,
        intento INTEGER,
        aciertos INTEGER,
        total INTEGER,
        estado_actividad TEXT,
        pistas_usadas INTEGER,
        fecha_hora TEXT
    );

    CREATE TABLE IF NOT EXISTS estado_actividad (
        codigo_nino TEXT,
        actividad_id TEXT,
        contenido_id TEXT,
        estado TEXT,
        intentos INTEGER,
        pistas_usadas INTEGER,
        PRIMARY KEY (codigo_nino, actividad_id)
    );
    """)
    conn.commit()
    conn.close()


def asegurar_nino(codigo):
    conn = get_conn()
    conn.execute(
        "INSERT OR IGNORE INTO ninos (codigo, creado_en) VALUES (?, ?)",
        (codigo, datetime.datetime.utcnow().isoformat()),
    )
    conn.commit()
    conn.close()


def obtener_estado_actividad(codigo_nino, actividad_id):
    conn = get_conn()
    row = conn.execute(
        "SELECT * FROM estado_actividad WHERE codigo_nino=? AND actividad_id=?",
        (codigo_nino, actividad_id),
    ).fetchone()
    conn.close()
    return dict(row) if row else None


def registrar_intento(codigo_nino, encuentro_id, contenido_id, actividad_id,
                       intento, aciertos, total, estado_actividad, pistas_usadas):
    conn = get_conn()
    conn.execute(
        """INSERT INTO intentos
           (codigo_nino, encuentro_id, contenido_id, actividad_id, intento,
            aciertos, total, estado_actividad, pistas_usadas, fecha_hora)
           VALUES (?,?,?,?,?,?,?,?,?,?)""",
        (codigo_nino, encuentro_id, contenido_id, actividad_id, intento,
         aciertos, total, estado_actividad, pistas_usadas,
         datetime.datetime.utcnow().isoformat()),
    )
    conn.execute(
        """INSERT INTO estado_actividad (codigo_nino, actividad_id, contenido_id, estado, intentos, pistas_usadas)
           VALUES (?,?,?,?,?,?)
           ON CONFLICT(codigo_nino, actividad_id)
           DO UPDATE SET estado=excluded.estado, intentos=excluded.intentos,
                         pistas_usadas=excluded.pistas_usadas""",
        (codigo_nino, actividad_id, contenido_id, estado_actividad, intento, pistas_usadas),
    )
    conn.commit()
    conn.close()


def estados_de_contenido(codigo_nino, actividad_ids):
    conn = get_conn()
    estados = []
    for aid in actividad_ids:
        row = conn.execute(
            "SELECT estado FROM estado_actividad WHERE codigo_nino=? AND actividad_id=?",
            (codigo_nino, aid),
        ).fetchone()
        estados.append(row["estado"] if row else None)
    conn.close()
    return estados


def progreso_actividades(codigo_nino, actividad_ids):
    conn = get_conn()
    out = {}
    for aid in actividad_ids:
        row = conn.execute(
            "SELECT estado, intentos, pistas_usadas FROM estado_actividad WHERE codigo_nino=? AND actividad_id=?",
            (codigo_nino, aid),
        ).fetchone()
        out[aid] = dict(row) if row else {"estado": None, "intentos": 0, "pistas_usadas": 0}
    conn.close()
    return out


# --------------------------------------------------- módulo de catequista --
# Estas consultas son de solo lectura: el catequista nunca modifica el
# progreso de un joven desde aquí, solo lo consulta — para acompañar y
# motivar, no para calificar (ver app.py, ruta /api/catequista/...).

def nino_existe(codigo):
    conn = get_conn()
    row = conn.execute("SELECT 1 FROM ninos WHERE codigo=?", (codigo,)).fetchone()
    conn.close()
    return row is not None


def listar_ninos():
    """Todos los códigos que ya entraron a la app al menos una vez, con la
    fecha en que se vieron por primera y por última vez. Se usa para armar
    la lista que ve el catequista (ver resumen_nino para el avance de cada
    uno)."""
    conn = get_conn()
    rows = conn.execute(
        """SELECT n.codigo, n.creado_en, MAX(i.fecha_hora) AS ultima_actividad
           FROM ninos n LEFT JOIN intentos i ON i.codigo_nino = n.codigo
           GROUP BY n.codigo
           ORDER BY n.creado_en DESC"""
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def resumen_nino(codigo):
    """Cuántas actividades tiene este código en cada estado. No incluye las
    actividades que todavía no se han intentado (esas no tienen fila en
    estado_actividad); el llamador las calcula como total - suma de estos
    conteos."""
    conn = get_conn()
    filas = conn.execute(
        "SELECT estado, COUNT(*) AS n FROM estado_actividad WHERE codigo_nino=? GROUP BY estado",
        (codigo,),
    ).fetchall()
    conn.close()
    conteos = {"LOGRADO": 0, "EN_PROCESO": 0, "REQUIERE_ACOMPANAMIENTO": 0}
    for f in filas:
        conteos[f["estado"]] = f["n"]
    return conteos


def progreso_completo_nino(codigo):
    """Estado + intentos + pistas_usadas de TODAS las actividades que este
    código ya intentó, indexado por actividad_id — para armar el detalle
    completo que ve el catequista al entrar a un joven en particular."""
    conn = get_conn()
    rows = conn.execute(
        "SELECT actividad_id, estado, intentos, pistas_usadas FROM estado_actividad WHERE codigo_nino=?",
        (codigo,),
    ).fetchall()
    conn.close()
    return {r["actividad_id"]: dict(r) for r in rows}


# ------------------------------------------------------- módulo de admin --
# Acción destructiva reservada a quien coordina el reinicio del tutorial
# (ver app.py, ruta /api/admin/limpiar-bd, protegida con CLAVE_ADMIN y una
# frase de confirmación — nunca se llama por accidente).

def contar_registros():
    """Cuántos jóvenes/intentos hay antes de borrar — para mostrarlo en la
    confirmación y que quien limpia sepa el tamaño real de lo que borra."""
    conn = get_conn()
    ninos = conn.execute("SELECT COUNT(*) AS n FROM ninos").fetchone()["n"]
    intentos = conn.execute("SELECT COUNT(*) AS n FROM intentos").fetchone()["n"]
    conn.close()
    return {"ninos": ninos, "intentos": intentos}


def limpiar_todo():
    """Borra TODO el progreso (las tres tablas), dejando las tablas vacías
    pero con su estructura intacta — como si nadie hubiera entrado nunca.
    No hay "deshacer" dentro de la app; la llamada en app.py hace una copia
    de respaldo del archivo .db antes de invocar esta función."""
    conn = get_conn()
    conn.execute("DELETE FROM estado_actividad")
    conn.execute("DELETE FROM intentos")
    conn.execute("DELETE FROM ninos")
    conn.commit()
    conn.close()
