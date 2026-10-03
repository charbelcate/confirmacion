# -*- coding: utf-8 -*-
"""
Persistencia del progreso del joven — separada de la base de conocimiento
(content.py), tal como define el modelo: "El conocimiento se mantendrá
separado de las actividades y de los datos personales del joven."

Antes usaba SQLite en un archivo local; ahora usa MariaDB (vía PyMySQL),
en el servicio MariaDB compartido de Easypanel, con una base de datos y un
usuario propios para esta app (confirmacion_db / confirmacion_user) —
aislados de las demás apps del mismo servidor. Esto evita el problema que
tenía SQLite: si se borra y reinstala el servicio de la app en Easypanel,
la base de datos (que vive en el servicio de MariaDB, separado) no se
toca ni se pierde.

No se guarda ningún dato personal del joven: solo un "código" que asigna
el catequista (por ejemplo, un nombre corto o un código de grupo), sin
correo, sin apellido, sin datos identificables.

Variables de entorno esperadas (configurarlas en Easypanel, sección
Entorno del servicio):
  DB_HOST     (opcional, por defecto "web_mariadb")
  DB_PORT     (opcional, por defecto 3306)
  DB_USER     (opcional, por defecto "confirmacion_user")
  DB_NAME     (opcional, por defecto "confirmacion_db")
  DB_PASSWORD (obligatoria — la contraseña de confirmacion_user)
"""
import pymysql
import pymysql.cursors
import datetime
import json
import os

DB_HOST = os.environ.get("DB_HOST", "web_mariadb")
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ.get("DB_USER", "confirmacion_user")
DB_NAME = os.environ.get("DB_NAME", "confirmacion_db")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

if not DB_PASSWORD:
    raise RuntimeError(
        "Falta la variable de entorno DB_PASSWORD (la contraseña de "
        "confirmacion_user en MariaDB). Configúrala en Easypanel, "
        "sección 'Entorno' del servicio de confirmación."
    )


def get_conn():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        charset="utf8mb4",
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,
    )


def _ahora():
    """Fecha/hora actual en el formato que MariaDB espera para DATETIME."""
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _iso(valor):
    """Convierte un datetime.datetime (lo que devuelve PyMySQL para una
    columna DATETIME) a una cadena ISO 8601 — igual que lo devolvía
    SQLite antes (ahí las fechas siempre eran texto plano). Así app.py
    sigue recibiendo texto, como siempre, y no hay que tocarlo."""
    if valor is None:
        return None
    if isinstance(valor, (datetime.datetime, datetime.date)):
        return valor.isoformat()
    return valor


def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS ninos (
            codigo VARCHAR(100) PRIMARY KEY,
            creado_en DATETIME
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS intentos (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo_nino VARCHAR(100),
            encuentro_id VARCHAR(100),
            contenido_id VARCHAR(100),
            actividad_id VARCHAR(100),
            intento INT,
            aciertos INT,
            total INT,
            estado_actividad VARCHAR(50),
            pistas_usadas INT,
            fecha_hora DATETIME
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS estado_actividad (
            codigo_nino VARCHAR(100),
            actividad_id VARCHAR(100),
            contenido_id VARCHAR(100),
            estado VARCHAR(50),
            intentos INT,
            pistas_usadas INT,
            PRIMARY KEY (codigo_nino, actividad_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS respuestas_abiertas (
            id INT AUTO_INCREMENT PRIMARY KEY,
            codigo_nino VARCHAR(100),
            encuentro_id VARCHAR(100),
            contenido_id VARCHAR(100),
            actividad_id VARCHAR(100),
            item_index INT,
            pregunta_texto TEXT,
            texto_respuesta TEXT,
            logrado TINYINT(1),
            motivo VARCHAR(50),
            revisado TINYINT(1) DEFAULT 0,
            valido_catequista TINYINT(1) NULL,
            promovida TINYINT(1) DEFAULT 0,
            fecha_hora DATETIME,
            fecha_revision DATETIME NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
    """)
    conn.commit()
    cur.close()
    conn.close()


def asegurar_nino(codigo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT IGNORE INTO ninos (codigo, creado_en) VALUES (%s, %s)",
        (codigo, _ahora()),
    )
    conn.commit()
    cur.close()
    conn.close()


def obtener_estado_actividad(codigo_nino, actividad_id):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM estado_actividad WHERE codigo_nino=%s AND actividad_id=%s",
        (codigo_nino, actividad_id),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return dict(row) if row else None


def registrar_intento(codigo_nino, encuentro_id, contenido_id, actividad_id,
                       intento, aciertos, total, estado_actividad, pistas_usadas):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO intentos
           (codigo_nino, encuentro_id, contenido_id, actividad_id, intento,
            aciertos, total, estado_actividad, pistas_usadas, fecha_hora)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (codigo_nino, encuentro_id, contenido_id, actividad_id, intento,
         aciertos, total, estado_actividad, pistas_usadas, _ahora()),
    )
    cur.execute(
        """INSERT INTO estado_actividad
           (codigo_nino, actividad_id, contenido_id, estado, intentos, pistas_usadas)
           VALUES (%s,%s,%s,%s,%s,%s)
           ON DUPLICATE KEY UPDATE
               estado=VALUES(estado),
               intentos=VALUES(intentos),
               pistas_usadas=VALUES(pistas_usadas)""",
        (codigo_nino, actividad_id, contenido_id, estado_actividad, intento, pistas_usadas),
    )
    conn.commit()
    cur.close()
    conn.close()


def estados_de_contenido(codigo_nino, actividad_ids):
    conn = get_conn()
    cur = conn.cursor()
    estados = []
    for aid in actividad_ids:
        cur.execute(
            "SELECT estado FROM estado_actividad WHERE codigo_nino=%s AND actividad_id=%s",
            (codigo_nino, aid),
        )
        row = cur.fetchone()
        estados.append(row["estado"] if row else None)
    cur.close()
    conn.close()
    return estados


def progreso_actividades(codigo_nino, actividad_ids):
    conn = get_conn()
    cur = conn.cursor()
    out = {}
    for aid in actividad_ids:
        cur.execute(
            "SELECT estado, intentos, pistas_usadas FROM estado_actividad WHERE codigo_nino=%s AND actividad_id=%s",
            (codigo_nino, aid),
        )
        row = cur.fetchone()
        out[aid] = dict(row) if row else {"estado": None, "intentos": 0, "pistas_usadas": 0}
    cur.close()
    conn.close()
    return out


# ---------------------------------------- respuestas abiertas (revisión) --
# Guarda el texto de cada respuesta a una pregunta "abierta" (ver
# _evaluar_item_abierto en app.py), junto con el resultado automático de
# su evaluación, para que el catequista pueda revisarlas después desde su
# panel y confirmar cuáles son válidas aunque el sistema las haya
# rechazado (o al revés). No afecta el resultado de la actividad del
# joven: es solo un registro para revisión y mejora posterior — ver
# listar_respuestas_validas_no_promovidas, que usa esas confirmaciones
# para ampliar "respuestas_referencia" en content.py.

def guardar_respuesta_abierta(codigo_nino, encuentro_id, contenido_id, actividad_id,
                               item_index, pregunta_texto, texto_respuesta,
                               logrado, motivo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """INSERT INTO respuestas_abiertas
           (codigo_nino, encuentro_id, contenido_id, actividad_id, item_index,
            pregunta_texto, texto_respuesta, logrado, motivo, fecha_hora)
           VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""",
        (codigo_nino, encuentro_id, contenido_id, actividad_id, item_index,
         pregunta_texto, texto_respuesta, 1 if logrado else 0, motivo, _ahora()),
    )
    conn.commit()
    cur.close()
    conn.close()


def listar_respuestas_abiertas(solo_pendientes=True, limite=200):
    """Respuestas a preguntas abiertas para la pantalla de revisión del
    catequista. Por defecto solo las que todavía no se marcaron
    (revisado=0) — ver marcar_respuesta_abierta. Las más recientes primero."""
    conn = get_conn()
    cur = conn.cursor()
    if solo_pendientes:
        cur.execute(
            "SELECT * FROM respuestas_abiertas WHERE revisado=0 ORDER BY fecha_hora DESC LIMIT %s",
            (limite,),
        )
    else:
        cur.execute(
            "SELECT * FROM respuestas_abiertas ORDER BY fecha_hora DESC LIMIT %s",
            (limite,),
        )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        d["fecha_hora"] = _iso(d["fecha_hora"])
        d["fecha_revision"] = _iso(d["fecha_revision"])
        out.append(d)
    return out


def marcar_respuesta_abierta(id_respuesta, valido):
    """El catequista confirma (True) o descarta (False) una respuesta
    abierta tras leerla. No borra nada; solo queda marcada como revisada
    con su veredicto, para poder ampliar respuestas_referencia después."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE respuestas_abiertas SET revisado=1, valido_catequista=%s, fecha_revision=%s WHERE id=%s",
        (1 if valido else 0, _ahora(), id_respuesta),
    )
    conn.commit()
    afectadas = cur.rowcount
    cur.close()
    conn.close()
    return afectadas > 0


def listar_respuestas_validas_no_promovidas(limite=500):
    """Respuestas que el catequista ya confirmó como válidas y que todavía
    no se agregaron a "respuestas_referencia" en content.py — ver
    marcar_promovidas, que se llama después de copiarlas ahí a mano (o con
    un script), para no volver a traer las mismas la próxima vez."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """SELECT * FROM respuestas_abiertas
           WHERE valido_catequista=1 AND promovida=0
           ORDER BY actividad_id, item_index, fecha_hora
           LIMIT %s""",
        (limite,),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    out = []
    for r in rows:
        d = dict(r)
        d["fecha_hora"] = _iso(d["fecha_hora"])
        d["fecha_revision"] = _iso(d["fecha_revision"])
        out.append(d)
    return out


def marcar_promovidas(ids):
    """Marca estas respuestas (por id) como ya incorporadas a content.py,
    para que listar_respuestas_validas_no_promovidas no las vuelva a
    traer en la próxima ronda."""
    ids = [int(i) for i in (ids or [])]
    if not ids:
        return 0
    conn = get_conn()
    cur = conn.cursor()
    placeholders = ",".join(["%s"] * len(ids))
    cur.execute(
        f"UPDATE respuestas_abiertas SET promovida=1 WHERE id IN ({placeholders})",
        tuple(ids),
    )
    conn.commit()
    afectadas = cur.rowcount
    cur.close()
    conn.close()
    return afectadas


# --------------------------------------------------- módulo de catequista --
# Estas consultas son de solo lectura: el catequista nunca modifica el
# progreso de un joven desde aquí, solo lo consulta — para acompañar y
# motivar, no para calificar (ver app.py, ruta /api/catequista/...).

def nino_existe(codigo):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM ninos WHERE codigo=%s", (codigo,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row is not None


def listar_ninos():
    """Todos los códigos que ya entraron a la app al menos una vez, con la
    fecha en que se vieron por primera y por última vez. Se usa para armar
    la lista que ve el catequista (ver resumen_nino para el avance de cada
    uno)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """SELECT n.codigo, n.creado_en, MAX(i.fecha_hora) AS ultima_actividad
           FROM ninos n LEFT JOIN intentos i ON i.codigo_nino = n.codigo
           GROUP BY n.codigo, n.creado_en
           ORDER BY n.creado_en DESC"""
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {
            "codigo": r["codigo"],
            "creado_en": _iso(r["creado_en"]),
            "ultima_actividad": _iso(r["ultima_actividad"]),
        }
        for r in rows
    ]


def resumen_nino(codigo):
    """Cuántas actividades tiene este código en cada estado. No incluye las
    actividades que todavía no se han intentado (esas no tienen fila en
    estado_actividad); el llamador las calcula como total - suma de estos
    conteos."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT estado, COUNT(*) AS n FROM estado_actividad WHERE codigo_nino=%s GROUP BY estado",
        (codigo,),
    )
    filas = cur.fetchall()
    cur.close()
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
    cur = conn.cursor()
    cur.execute(
        "SELECT actividad_id, estado, intentos, pistas_usadas FROM estado_actividad WHERE codigo_nino=%s",
        (codigo,),
    )
    rows = cur.fetchall()
    cur.close()
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
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) AS n FROM ninos")
    ninos = cur.fetchone()["n"]
    cur.execute("SELECT COUNT(*) AS n FROM intentos")
    intentos = cur.fetchone()["n"]
    cur.close()
    conn.close()
    return {"ninos": ninos, "intentos": intentos}


def respaldar_a_archivo(ruta_archivo):
    """Exporta TODAS las filas de las tres tablas a un archivo JSON, como
    copia de seguridad antes de una limpieza total. Con SQLite esto era
    una copia binaria del archivo .db; con MariaDB ya no hay un archivo
    único que copiar, así que en su lugar se vuelca el contenido completo
    de cada tabla a un JSON legible, por si hace falta revisarlo o
    restaurarlo manualmente más adelante."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM ninos")
    ninos = cur.fetchall()
    cur.execute("SELECT * FROM intentos")
    intentos = cur.fetchall()
    cur.execute("SELECT * FROM estado_actividad")
    estado_actividad = cur.fetchall()
    cur.execute("SELECT * FROM respuestas_abiertas")
    respuestas_abiertas = cur.fetchall()
    cur.close()
    conn.close()

    datos = {
        "generado_en": _ahora(),
        "ninos": ninos,
        "intentos": intentos,
        "estado_actividad": estado_actividad,
        "respuestas_abiertas": respuestas_abiertas,
    }
    os.makedirs(os.path.dirname(ruta_archivo), exist_ok=True)
    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2, default=str)


def limpiar_todo():
    """Borra TODO el progreso (las tres tablas), dejando las tablas vacías
    pero con su estructura intacta — como si nadie hubiera entrado nunca.
    No hay "deshacer" dentro de la app; la llamada en app.py hace un
    respaldo en JSON antes de invocar esta función (ver respaldar_a_archivo)."""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM estado_actividad")
    cur.execute("DELETE FROM respuestas_abiertas")
    cur.execute("DELETE FROM intentos")
    cur.execute("DELETE FROM ninos")
    conn.commit()
    cur.close()
    conn.close()
