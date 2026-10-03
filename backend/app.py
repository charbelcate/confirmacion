# -*- coding: utf-8 -*-
"""
Microservicio de Formación y Reforzamiento Catequético — Confirmación
======================================================================
API REST (Flask) idéntica en su motor al piloto de Primera Comunión
(catequesis-pc01-pwa): mismo `motor.py` (escalera de refuerzo por
intentos), mismo `db.py` (SQLite, sin datos personales) y misma
`app.py` (esta), sin ningún cambio de lógica. Lo único que cambia entre
ambos proyectos es `content.py` (la base de conocimiento) y el
`frontend/` (rebrandeado para Confirmación). Ver el docstring de
content.py para el detalle del primer prototipo (C0N1 a C0N3).

Cómo correrlo:
    cd backend
    pip install -r requirements.txt
    python app.py
Luego abre http://localhost:5000 en el navegador (o en el teléfono, si
está en la misma red, usando la IP de la computadora).
"""
import datetime
import os
import random
import re
import unicodedata

from flask import Flask, jsonify, request, send_from_directory

import content
import db
import motor
import nlp_eval

app = Flask(__name__, static_folder="../frontend", static_url_path="")

db.init_db()

# Clave compartida para el módulo de catequista (ver rutas /api/catequista/...
# al final de este archivo). NO es un sistema de usuarios — es una sola
# clave, igual de simple que el "código" del joven, pensada solo para que
# nadie entre por curiosidad a ver el progreso de otro. Cámbiala en
# producción con la variable de entorno CLAVE_CATEQUISTA (en Easypanel,
# sección "Variables de entorno" del servicio) — usa una clave DISTINTA a
# la del proyecto de Primera Comunión, para que sean paneles separados.
CLAVE_CATEQUISTA = os.environ.get("CLAVE_CATEQUISTA", "catequista2026")

# Clave para reiniciar el tutorial de reforzamiento desde cero (borra todo
# el progreso). Es OTRA clave, separada de CLAVE_CATEQUISTA, pensada para
# que solo la persona que coordina un reinicio (no cualquier catequista)
# pueda hacerlo. Cámbiala en producción con la variable de entorno
# CLAVE_ADMIN (Easypanel, sección "Variables de entorno" del servicio).
CLAVE_ADMIN = os.environ.get("CLAVE_ADMIN", "admin2026")

# Frase exacta que hay que escribir para confirmar la limpieza — además de
# la clave, para que un clic o una llamada accidental nunca borre nada por
# error. No es configurable a propósito: es solo un freno de seguridad.
FRASE_CONFIRMACION_LIMPIEZA = "BORRAR TODO"


# --------------------------------------------------------------- utils --
def sin_acentos(texto):
    if texto is None:
        return ""
    nfkd = unicodedata.normalize("NFKD", str(texto))
    return "".join(c for c in nfkd if not unicodedata.combining(c)).strip().upper()


def contiene_palabra_alerta(texto):
    """True si `texto` contiene alguna palabra de content.PALABRAS_ALERTA,
    como palabra completa (no como parte de otra palabra) e ignorando
    acentos y mayúsculas."""
    normalizado = sin_acentos(texto)
    if not normalizado:
        return False
    # sin_acentos ya deja el texto en A-Z (NFKD también reduce la Ñ a N),
    # así que basta con separar en palabras alfabéticas.
    palabras = set(re.findall(r"[A-Z]+", normalizado))
    return bool(palabras & content.PALABRAS_ALERTA)


# Frases que indican que la respuesta RECHAZA o contradice explícitamente
# la idea sobre la que se pregunta (p. ej. "no debo hacer caso a la
# palabra de Dios"). Si aparece una de estas señales, una coincidencia de
# "palabras_esperadas" ya no basta para aceptar la respuesta de inmediato:
# solo nombrar el tema ("Dios", "Jesús", "seguir") no es suficiente si la
# frase lo está negando. En ese caso se exige además que la respuesta se
# parezca en significado a alguna "respuestas_referencia" (nivel 2); si no
# hay semejanza, queda correctamente como "fuera_de_tema".
SENALES_NEGACION = [
    "NO DEBO", "NO DEBERIA", "NO DEBIA", "NO HAY QUE HACER CASO",
    "NO HAGO CASO", "NO LE HAGO CASO", "NO VOY A HACER CASO",
    "NO CREO EN", "NO QUIERO SEGUIR", "NO VOY A SEGUIR", "ME NIEGO A",
    "RECHAZO A", "NO ME IMPORTA DIOS", "NO ME IMPORTA JESUS",
    "NO LE HAGO CASO A", "NO SE DEBE HACER CASO",
]


def _contiene_senal_negacion(texto_normalizado):
    """True si `texto_normalizado` (ya pasado por sin_acentos) contiene
    alguna frase de SENALES_NEGACION."""
    return any(s in texto_normalizado for s in SENALES_NEGACION)


def _evaluar_item_abierto(texto, item):
    """Evalúa un ítem 'abierta' (respuesta libre): devuelve (cuenta_como_
    acierto, motivo). motivo es None si se aceptó, o "vacio" / "alerta" /
    "fuera_de_tema" si no se contó como acierto.

      - "vacio": no escribió nada.
      - "alerta": la respuesta contiene una palabra de content.PALABRAS_ALERTA
        (p. ej. "odiar"), sin importar el resto del texto.
      - "fuera_de_tema": el ítem declara "palabras_esperadas" (porque la
        pregunta tiene una dirección correcta clara, según la cita bíblica
        o la situación planteada), la respuesta no contiene ninguna —
        p. ej. "hacer incendios" a una pregunta sobre cuidar la creación —
        Y TAMPOCO se parece en significado a ninguna "respuestas_referencia"
        del ítem (ver más abajo).
        Los ítems sin "palabras_esperadas" (preguntas genuinamente
        personales) aceptan cualquier respuesta no vacía y sin alerta.

    Dos niveles para decidir si la respuesta "sí toca el tema", del más
    simple al más flexible:
      1. Coincidencia de palabras ("palabras_esperadas"): rápida, sin
         dependencias, pero solo detecta las palabras exactas que se
         anticiparon al escribir el contenido.
      2. Si el nivel 1 no encuentra nada, y el ítem tiene
         "respuestas_referencia" (frases de ejemplo correctas), se compara
         el SIGNIFICADO de la respuesta con esas frases usando un modelo
         de lenguaje preentrenado (nlp_eval.similitud_maxima) — así se
         acepta una respuesta que dice lo mismo con otras palabras (p. ej.
         "Dios Vivo" para "¿cómo llama san Pablo a la Iglesia?", aunque
         "VIVO" no estuviera en la lista de palabras esperadas). Si el
         modelo no está disponible (no instalado, o sin conexión para
         descargarlo), nlp_eval devuelve None y este nivel simplemente no
         se aplica — el resultado del nivel 1 queda como está, la app
         nunca falla por esto.
    """
    texto = (texto or "").strip()
    if not texto:
        return False, "vacio"
    if contiene_palabra_alerta(texto):
        return False, "alerta"
    esperadas = item.get("palabras_esperadas")
    if esperadas:
        normalizado = sin_acentos(texto)
        coincide = any(sin_acentos(w) in normalizado for w in esperadas)
        if coincide and not _contiene_senal_negacion(normalizado):
            return True, None
        referencias = item.get("respuestas_referencia")
        if referencias:
            similitud = nlp_eval.similitud_maxima(texto, referencias)
            if similitud is not None and similitud >= nlp_eval.UMBRAL_SIMILITUD:
                return True, None
        return False, "fuera_de_tema"
    return True, None


def _motivo_abiertos(items, respuestas):
    """Motivo más relevante entre los ítems 'abierta' de `items` que no se
    contaron como acierto ("alerta" pesa más que "fuera_de_tema"), o None
    si todos los abiertos se aceptaron (o no hay ítems abiertos). Se usa
    solo para elegir el mensaje de la API, no para calcular aciertos."""
    motivos = set()
    for i, it in enumerate(items):
        if not it.get("abierta"):
            continue
        val = respuestas[i] if respuestas and i < len(respuestas) else ""
        ok, motivo = _evaluar_item_abierto(val, it)
        if not ok and motivo != "vacio":
            motivos.add(motivo)
    if "alerta" in motivos:
        return "alerta"
    if "fuera_de_tema" in motivos:
        return "fuera_de_tema"
    return None


# Tipos cuya mecánica de INTERACCIÓN es "responder una lista de ítems con
# texto + respuesta (rellenar)": completar, crucigrama (definición -> palabra)
# y recuperación (que además admite ítems "abiertos", sin respuesta única).
TIPOS_RELLENAR = {"completar", "crucigrama", "recuperacion"}
# Tipos cuya mecánica es "elegir una opción entre varias, por cada ítem":
# selección múltiple, aplicación (una situación real + varias respuestas
# válidas) y el modo "preguntas" de los retos. Un ítem puede usar
# "correctas" (lista de índices válidos) en vez de un único "correcta"
# cuando más de una opción es igualmente aceptable.
TIPOS_OPCION = {"seleccion_multiple", "aplicacion"}


def actividad_publica(actividad_id, actividad):
    """Versión del contenido de una actividad SIN respuestas correctas."""
    tipo = actividad["tipo"]
    base = {"id": actividad_id, "tipo": tipo, "titulo": actividad["titulo"],
            "contenido_id": actividad["contenido_id"]}

    if tipo == "sopa_letras":
        base["palabras"] = actividad["palabras"]
        base["grid"] = generar_sopa_letras(actividad["palabras"])

    elif tipo == "crucigrama":
        filas, columnas, palabras = generar_layout_crucigrama(actividad["items"])
        base["filas"] = filas
        base["columnas"] = columnas
        base["palabras"] = palabras

    elif tipo in TIPOS_RELLENAR:
        base["items"] = [
            {"texto": it["texto"], "banco": it.get("banco", []), "abierta": it.get("abierta", False)}
            for it in actividad["items"]
        ]

    elif tipo == "verdadero_falso":
        base["items"] = [{"texto": it["texto"]} for it in actividad["items"]]

    elif tipo in TIPOS_OPCION:
        base["items"] = [{"texto": it["texto"], "opciones": it["opciones"]} for it in actividad["items"]]
        if tipo == "aplicacion":
            base["situacion"] = actividad.get("situacion")

    elif tipo == "unir_parejas":
        base["terminos"] = [p["termino"] for p in actividad["pares"]]
        base["definiciones"] = [p["definicion"] for p in actividad["pares"]]

    elif tipo == "reto":
        modo = actividad.get("modo")
        base["modo"] = modo
        base["instruccion"] = actividad.get("instruccion")
        base["tiempo_segundos"] = actividad.get("tiempo_segundos", 45)
        if modo == "preguntas":
            base["items"] = [{"texto": it["texto"], "opciones": it["opciones"]} for it in actividad["items"]]
        elif modo == "elegir_libres":
            base["banco"] = actividad["banco"]
            base["minimo"] = actividad["minimo"]

    if actividad.get("reflexion"):
        base["reflexion"] = actividad["reflexion"]

    return base


# ------------------------------------------------ generador de sopa de letras --
DIRECCIONES = [(0, 1), (1, 0)]  # horizontal, vertical (mantiene el juego simple)


def generar_sopa_letras(palabras, tam=None):
    palabras_norm = [sin_acentos(p) for p in palabras]
    tam = tam or max(10, max(len(p) for p in palabras_norm) + 2)
    grid = [[None] * tam for _ in range(tam)]

    for palabra in sorted(palabras_norm, key=len, reverse=True):
        colocada = False
        intentos = 0
        while not colocada and intentos < 200:
            intentos += 1
            dr, dc = random.choice(DIRECCIONES)
            max_r = tam - (len(palabra) if dr else 1)
            max_c = tam - (len(palabra) if dc else 1)
            if max_r < 0 or max_c < 0:
                continue
            r0 = random.randint(0, max_r)
            c0 = random.randint(0, max_c)
            ok = True
            for i, ch in enumerate(palabra):
                r, c = r0 + dr * i, c0 + dc * i
                if grid[r][c] is not None and grid[r][c] != ch:
                    ok = False
                    break
            if ok:
                for i, ch in enumerate(palabra):
                    r, c = r0 + dr * i, c0 + dc * i
                    grid[r][c] = ch
                colocada = True

    letras = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for r in range(tam):
        for c in range(tam):
            if grid[r][c] is None:
                grid[r][c] = random.choice(letras)
    return grid


# --------------------------------------------------- generador de crucigrama --
def generar_layout_crucigrama(items):
    """Coloca las palabras de un crucigrama en una cuadrícula real, buscando
    cruces genuinos entre ellas (misma letra, direcciones perpendiculares) —
    igual que un crucigrama de verdad, no una lista de espacios para rellenar.
    Nunca deja una palabra "pegada" a otra sin cruzarse de verdad (ni por el
    costado, ni extendiéndola por delante o por detrás): eso haría que dos
    palabras distintas parecieran una sola al leerlas. Si una palabra no
    encuentra ningún cruce limpio, se coloca aparte en su propia fila,
    separada del resto (sigue siendo jugable, solo que no cruza con nada).
    Es determinístico: la misma lista de ítems siempre produce el mismo
    trazado, para que el niño no vea el crucigrama "recolocado" si recarga
    la página a mitad de resolverlo."""
    palabras = [sin_acentos(it["respuesta"]) for it in items]
    orden = sorted(range(len(items)), key=lambda i: -len(palabras[i]))

    grid = {}       # (fila, columna) -> letra
    celda_dir = {}  # (fila, columna) -> {"H", "V"} direcciones ya usadas ahí
    coloc = {}      # idx original -> {fila, columna, direccion}

    def cabe(fila, col, direccion, palabra):
        """Además de no chocar letras, una palabra nueva NUNCA debe quedar
        pegada (sin cruzarse de verdad) a otra ya colocada: ni tocando su
        costado, ni extendiéndola por delante o por detrás. Si no, dos
        palabras distintas parecen una sola al leerlas (así se detectó que
        la última letra de AMOR quedaba pegada, sin cruzarse, a la primera
        fila de DIOS)."""
        dr, dc = (1, 0) if direccion == "V" else (0, 1)
        pr, pc = (0, 1) if direccion == "V" else (1, 0)  # paso perpendicular
        n = len(palabra)
        for i, ch in enumerate(palabra):
            r, c = fila + dr * i, col + dc * i
            existente = grid.get((r, c))
            if existente is not None:
                if existente != ch:
                    return False
                # cruce legítimo en esta celda: no se exige nada más aquí
            elif grid.get((r + pr, c + pc)) is not None or grid.get((r - pr, c - pc)) is not None:
                return False  # celda nueva pegada por el costado a otra palabra
        r0, c0 = fila - dr, col - dc
        r1, c1 = fila + dr * n, col + dc * n
        if grid.get((r0, c0)) is not None or grid.get((r1, c1)) is not None:
            return False  # pegada justo antes del inicio o después del final
        return True

    def buscar_cruce(palabra):
        for i, ch in enumerate(palabra):
            for (r, c), existente in grid.items():
                if existente != ch:
                    continue
                dirs_aqui = celda_dir.get((r, c), set())
                if dirs_aqui == {"H"}:
                    nueva_dir = "V"
                elif dirs_aqui == {"V"}:
                    nueva_dir = "H"
                else:
                    continue  # celda ya saturada (o vacía, no debería pasar)
                fila = r - i if nueva_dir == "V" else r
                col = c - i if nueva_dir == "H" else c
                if cabe(fila, col, nueva_dir, palabra):
                    return fila, col, nueva_dir
        return None

    for idx in orden:
        palabra = palabras[idx]
        if not grid:
            fila, col, direccion = 0, 0, "H"
        else:
            candidato = buscar_cruce(palabra)
            if candidato:
                fila, col, direccion = candidato
            else:
                fila, col, direccion = (max(r for r, _ in grid) + 2), 0, "H"

        dr, dc = (1, 0) if direccion == "V" else (0, 1)
        for i, ch in enumerate(palabra):
            r, c = fila + dr * i, col + dc * i
            grid[(r, c)] = ch
            celda_dir.setdefault((r, c), set()).add(direccion)
        coloc[idx] = {"fila": fila, "columna": col, "direccion": direccion}

    min_r = min(r for r, _ in grid)
    min_c = min(c for _, c in grid)
    for p in coloc.values():
        p["fila"] -= min_r
        p["columna"] -= min_c
    filas = max(r for r, _ in grid) - min_r + 1
    columnas = max(c for _, c in grid) - min_c + 1

    inicios = sorted({(p["fila"], p["columna"]) for p in coloc.values()})
    numero_de = {celda: n + 1 for n, celda in enumerate(inicios)}

    resultado = []
    for i, it in enumerate(items):
        p = coloc[i]
        resultado.append({
            "num": numero_de[(p["fila"], p["columna"])], "direccion": p["direccion"],
            "fila": p["fila"], "columna": p["columna"],
            "longitud": len(palabras[i]), "clave": it["texto"],
        })
    return filas, columnas, resultado


# ------------------------------------------------------ validadores por tipo --
def _evaluar_rellenar(items, respuestas):
    """completar / crucigrama / recuperación: ítems con texto+respuesta,
    o ítems 'abiertos' (ver _evaluar_item_abierto: exigen participación,
    ausencia de palabras de alerta y, si el ítem lo declara, al menos una
    palabra esperada del tema)."""
    aciertos = 0
    for i, it in enumerate(items):
        val = respuestas[i] if respuestas and i < len(respuestas) else ""
        if it.get("abierta"):
            ok, _motivo = _evaluar_item_abierto(val, it)
            if ok:
                aciertos += 1
        else:
            if sin_acentos(val) == sin_acentos(it["respuesta"]):
                aciertos += 1
    return aciertos, len(items)


def _evaluar_opciones(items, respuestas):
    """seleccion_multiple / reto (modo preguntas): ítems con opciones +
    índice correcto. Un ítem puede usar "correctas" (lista de índices
    válidos) en vez de un único "correcta" cuando más de una opción es
    igualmente aceptable."""
    aciertos = 0
    for i, it in enumerate(items):
        if not respuestas or i >= len(respuestas):
            continue
        val = respuestas[i]
        correctas = it.get("correctas")
        ok = (val in correctas) if correctas is not None else (val == it["correcta"])
        if ok:
            aciertos += 1
    return aciertos, len(items)


def evaluar_respuestas(actividad, respuestas):
    tipo = actividad["tipo"]

    if tipo == "sopa_letras":
        encontradas = {sin_acentos(p) for p in (respuestas or [])}
        objetivo = {sin_acentos(p) for p in actividad["palabras"]}
        aciertos = len(encontradas & objetivo)
        incluir = {sin_acentos(w) for w in actividad.get("incluir", [])}
        if incluir and not incluir.issubset(encontradas & objetivo):
            aciertos = min(aciertos, actividad["requisito"] - 1)
        return aciertos, len(objetivo)

    if tipo in TIPOS_RELLENAR:
        items = actividad["items"]
        aciertos, total = _evaluar_rellenar(items, respuestas)
        incluir = {sin_acentos(w) for w in actividad.get("incluir", [])}
        if incluir:
            respondidas_ok = set()
            for i, it in enumerate(items):
                val = respuestas[i] if respuestas and i < len(respuestas) else ""
                if not it.get("abierta") and sin_acentos(val) == sin_acentos(it["respuesta"]):
                    respondidas_ok.add(sin_acentos(it["respuesta"]))
            if not incluir.issubset(respondidas_ok):
                aciertos = min(aciertos, actividad["requisito"] - 1)
        return aciertos, total

    if tipo == "verdadero_falso":
        items = actividad["items"]
        aciertos = sum(
            1 for i, it in enumerate(items)
            if respuestas and i < len(respuestas) and bool(respuestas[i]) == it["respuesta"]
        )
        return aciertos, len(items)

    if tipo in TIPOS_OPCION:
        return _evaluar_opciones(actividad["items"], respuestas)

    if tipo == "unir_parejas":
        pares = actividad["pares"]
        correctas = {(sin_acentos(p["termino"]), sin_acentos(p["definicion"])) for p in pares}
        enviadas = {(sin_acentos(r.get("termino")), sin_acentos(r.get("definicion")))
                    for r in (respuestas or [])}
        aciertos = len(correctas & enviadas)
        return aciertos, len(pares)

    if tipo == "reto":
        modo = actividad.get("modo")
        if modo == "preguntas":
            return _evaluar_opciones(actividad["items"], respuestas)
        if modo == "elegir_libres":
            seleccionadas = {sin_acentos(p) for p in (respuestas or [])}
            banco = {sin_acentos(p) for p in actividad["banco"]}
            correctas = actividad.get("correctas")
            validas = {sin_acentos(p) for p in correctas} if correctas else banco
            aciertos = len(seleccionadas & validas & banco)
            minimo = actividad["minimo"]
            return min(aciertos, minimo), minimo

    return 0, 1


# -------------------------------------------------- bloqueo de avance --
# El itinerario se recorre en un único orden lineal (content.CONTENIDOS,
# que ya cruza de un encuentro al siguiente): un contenido solo se
# desbloquea cuando el anterior está COMPLETO (sus 10 actividades en
# LOGRADO, no solo el 80% que ya alcanza para el estado "LOGRADO" del
# contenido — el mismo criterio estricto que ya se usaba para invitar al
# siguiente tema). Un encuentro se considera desbloqueado cuando lo está
# su primer contenido. Esto se aplica tanto en el frontend (para no
# mostrar como clicable lo que no toca todavía) como aquí en la API (para
# que tampoco se pueda "saltar" manipulando la URL a mano).
MENSAJE_BLOQUEADO = ("No puedes avanzar todavía: primero debes completar todas "
                      "las actividades de «{titulo}».")


def contenido_completo(codigo, contenido_id):
    """True si TODAS las actividades de ese contenido están LOGRADO para
    este niño (no solo el 80% que ya lo marca como LOGRADO)."""
    aids = content.actividades_de_contenido(contenido_id)
    estados = db.estados_de_contenido(codigo, aids)
    return len(estados) > 0 and all(e == "LOGRADO" for e in estados)


def contenido_desbloqueado(codigo, contenido_id):
    """Devuelve (desbloqueado, requiere): "requiere" es {"id", "titulo"}
    del contenido pendiente si está bloqueado, o None si ya se puede
    entrar."""
    anterior = content.anterior_contenido_de(contenido_id)
    if anterior is None:
        return True, None
    if contenido_completo(codigo, anterior["id"]):
        return True, None
    return False, {"id": anterior["id"], "titulo": anterior["titulo"]}


# ------------------------------------------------------------------ rutas --
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/encuentros")
def api_encuentros():
    """Lista de encuentros disponibles, con el progreso resumido del niño
    en cada uno — para la pantalla de selección (varios encuentros: PC01,
    PC02, ...)."""
    codigo = request.args.get("nino", "").strip()
    if not codigo:
        return jsonify({"error": "Falta el código del niño (parámetro ?nino=)."}), 400
    db.asegurar_nino(codigo)

    out = []
    for e in content.ENCUENTROS:
        contenidos = content.contenidos_de_encuentro(e["id"])
        total_actividades = 0
        logradas = 0
        for c in contenidos:
            aids = content.actividades_de_contenido(c["id"])
            estados = db.estados_de_contenido(codigo, aids)
            total_actividades += len(aids)
            logradas += sum(1 for est in estados if est == "LOGRADO")
        desbloqueado, requiere = contenido_desbloqueado(codigo, contenidos[0]["id"])
        out.append({
            "id": e["id"], "titulo": e["titulo"], "texto_biblico": e["texto_biblico"],
            "total_contenidos": len(contenidos), "total_actividades": total_actividades,
            "logradas": logradas,
            "desbloqueado": desbloqueado,
            "requiere": requiere,
        })
    return jsonify({"encuentros": out})


@app.route("/api/encuentro/<encuentro_id>")
def api_encuentro(encuentro_id):
    codigo = request.args.get("nino", "").strip()
    if not codigo:
        return jsonify({"error": "Falta el código del niño (parámetro ?nino=)."}), 400
    encuentro = content.encuentro_de(encuentro_id)
    if not encuentro:
        return jsonify({"error": "Encuentro no encontrado."}), 404
    db.asegurar_nino(codigo)

    contenidos_out = []
    for c in content.contenidos_de_encuentro(encuentro_id):
        aids = content.actividades_de_contenido(c["id"])
        estados = db.estados_de_contenido(codigo, aids)
        desbloqueado, requiere = contenido_desbloqueado(codigo, c["id"])
        contenidos_out.append({
            "id": c["id"],
            "titulo": c["titulo"],
            "total_actividades": len(aids),
            "logradas": sum(1 for e in estados if e == "LOGRADO"),
            "estado": motor.estado_contenido(estados),
            "desbloqueado": desbloqueado,
            "requiere": requiere,
        })

    return jsonify({
        "encuentro": encuentro,
        "contenidos": contenidos_out,
        "encuentro_desbloqueado": contenidos_out[0]["desbloqueado"] if contenidos_out else True,
        "requiere": contenidos_out[0]["requiere"] if contenidos_out else None,
    })


@app.route("/api/contenido/<contenido_id>/actividades")
def api_contenido_actividades(contenido_id):
    codigo = request.args.get("nino", "").strip()
    if not codigo:
        return jsonify({"error": "Falta el código del niño (parámetro ?nino=)."}), 400
    db.asegurar_nino(codigo)

    desbloqueado, requiere = contenido_desbloqueado(codigo, contenido_id)
    if not desbloqueado:
        return jsonify({
            "error": MENSAJE_BLOQUEADO.format(titulo=requiere["titulo"]),
            "bloqueado": True,
            "requiere": requiere,
        }), 403

    aids = content.actividades_de_contenido(contenido_id)
    progreso = db.progreso_actividades(codigo, aids)
    out = []
    for aid in aids:
        a = content.ACTIVIDADES[aid]
        p = progreso[aid]
        out.append({
            "id": aid, "tipo": a["tipo"], "titulo": a["titulo"],
            "estado": p["estado"], "intentos": p["intentos"],
        })
    titulo = next((c["titulo"] for c in content.CONTENIDOS if c["id"] == contenido_id), contenido_id)
    return jsonify({"contenido_id": contenido_id, "titulo": titulo, "actividades": out})


@app.route("/api/actividad/<actividad_id>")
def api_actividad(actividad_id):
    a = content.ACTIVIDADES.get(actividad_id)
    if not a:
        return jsonify({"error": "Actividad no encontrada."}), 404

    # El código del niño es opcional aquí (por compatibilidad), pero si se
    # manda, se aplica el mismo bloqueo de avance que en el resto de la API
    # — así tampoco se puede abrir una actividad "saltada" escribiendo la
    # URL a mano.
    codigo = request.args.get("nino", "").strip()
    if codigo:
        desbloqueado, requiere = contenido_desbloqueado(codigo, a["contenido_id"])
        if not desbloqueado:
            return jsonify({
                "error": MENSAJE_BLOQUEADO.format(titulo=requiere["titulo"]),
                "bloqueado": True,
                "requiere": requiere,
            }), 403

    return jsonify(actividad_publica(actividad_id, a))


@app.route("/api/actividad/<actividad_id>/responder", methods=["POST"])
def api_responder(actividad_id):
    a = content.ACTIVIDADES.get(actividad_id)
    if not a:
        return jsonify({"error": "Actividad no encontrada."}), 404

    payload = request.get_json(force=True, silent=True) or {}
    codigo = (payload.get("nino") or "").strip()
    respuestas = payload.get("respuestas")
    if not codigo:
        return jsonify({"error": "Falta el código del niño."}), 400

    db.asegurar_nino(codigo)

    desbloqueado, requiere = contenido_desbloqueado(codigo, a["contenido_id"])
    if not desbloqueado:
        return jsonify({
            "error": MENSAJE_BLOQUEADO.format(titulo=requiere["titulo"]),
            "bloqueado": True,
            "requiere": requiere,
        }), 403

    estado_previo = db.obtener_estado_actividad(codigo, actividad_id)
    intento_actual = (estado_previo["intentos"] if estado_previo else 0) + 1

    aciertos, total = evaluar_respuestas(a, respuestas)
    resultado = motor.evaluar(a, aciertos, total, intento_actual)

    # Si alguna respuesta a un ítem "abierta" contiene una palabra de
    # content.PALABRAS_ALERTA, o no toca ninguna "palabras_esperadas" del
    # ítem, ya no cuenta como acierto (ver _evaluar_item_abierto), pero
    # además avisamos con un mensaje específico en vez del feedback_falta
    # genérico, y lo marcamos en la respuesta para que quede visible en el
    # registro de progreso del catequista.
    motivo_abierto = a["tipo"] in TIPOS_RELLENAR and _motivo_abiertos(a["items"], respuestas)
    alerta_contenido = motivo_abierto == "alerta"
    fuera_de_tema = motivo_abierto == "fuera_de_tema"
    if not resultado["logrado"]:
        if alerta_contenido:
            resultado["mensaje"] = content.FEEDBACK_ALERTA
        elif fuera_de_tema:
            resultado["mensaje"] = content.FEEDBACK_FUERA_DE_TEMA

    pistas_usadas_prev = estado_previo["pistas_usadas"] if estado_previo else 0
    pistas_usadas = pistas_usadas_prev + (1 if resultado["pista"] else 0)

    db.registrar_intento(
        codigo_nino=codigo, encuentro_id=a["contenido_id"].split("-")[0],
        contenido_id=a["contenido_id"], actividad_id=actividad_id,
        intento=intento_actual, aciertos=aciertos, total=total,
        estado_actividad=resultado["estado_actividad"], pistas_usadas=pistas_usadas,
    )

    aids_contenido = content.actividades_de_contenido(a["contenido_id"])
    estados = db.estados_de_contenido(codigo, aids_contenido)
    estado_contenido = motor.estado_contenido(estados)
    # "contenido_completo": TODAS sus actividades logradas (no solo el 80% que
    # ya marca el contenido como LOGRADO) — es lo que dispara la invitación a
    # pasar al siguiente tema, para que aparezca justo al terminar la última.
    contenido_completo = len(estados) > 0 and all(e == "LOGRADO" for e in estados)

    respuesta_correcta = None
    if resultado["mostrar_respuesta"]:
        respuesta_correcta = extraer_respuesta_correcta(a)

    contenido_actual = content.contenido_de(a["contenido_id"])
    siguiente = content.siguiente_contenido_de(a["contenido_id"])
    # "camino_completo": no hay ningún contenido siguiente en todo el itinerario
    # (es decir, este era PC16-C06, el último de los 16 encuentros) Y se acaban
    # de completar todas sus actividades. Es la señal que usa el frontend para
    # mostrar, en vez del aviso genérico de "encuentro completado", la
    # animación final del camino con los 16 encuentros y el abrazo de Jesús.
    camino_completo = contenido_completo and siguiente is None

    return jsonify({
        **resultado,
        "intento": intento_actual,
        "pistas_usadas": pistas_usadas,
        "respuesta_correcta": respuesta_correcta,
        "estado_contenido": estado_contenido,
        "contenido_completo": contenido_completo,
        "contenido_titulo": contenido_actual["titulo"] if contenido_actual else None,
        "alerta_contenido": alerta_contenido,
        "fuera_de_tema": fuera_de_tema,
        "siguiente_contenido": (
            {"id": siguiente["id"], "titulo": siguiente["titulo"]} if siguiente else None
        ),
        "camino_completo": camino_completo,
    })


def extraer_respuesta_correcta(actividad):
    tipo = actividad["tipo"]
    if tipo == "sopa_letras":
        return actividad["palabras"]
    if tipo in TIPOS_RELLENAR:
        return [(it["respuesta"] if not it.get("abierta") else "(respuesta abierta)") for it in actividad["items"]]
    if tipo == "verdadero_falso":
        return [it["respuesta"] for it in actividad["items"]]
    if tipo in TIPOS_OPCION:
        out = []
        for it in actividad["items"]:
            correctas = it.get("correctas")
            if correctas is not None:
                out.append(" · ".join(it["opciones"][idx] for idx in correctas))
            else:
                out.append(it["opciones"][it["correcta"]])
        return out
    if tipo == "unir_parejas":
        return [{"termino": p["termino"], "definicion": p["definicion"]} for p in actividad["pares"]]
    if tipo == "reto":
        modo = actividad.get("modo")
        if modo == "preguntas":
            return [it["opciones"][it["correcta"]] for it in actividad["items"]]
        if modo == "elegir_libres":
            correctas = actividad.get("correctas")
            return correctas if correctas else actividad["banco"]
    return None


# -------------------------------------------------- módulo de catequista --
# Vista de solo lectura para que el catequista vea el avance de los jóvenes
# con su propio código de grupo — pensada para ACOMPAÑAR y MOTIVAR, no para
# vigilar ni calificar: no hay ninguna acción aquí que modifique el
# progreso de un joven, solo consultas. La idea es que el catequista note
# rápido a quién conviene animar (porque no ha empezado, lleva varios días
# sin entrar, o se quedó atascado en algo) en vez de tener que revisar
# actividad por actividad.
DIAS_SIN_ACTIVIDAD_PARA_ANIMAR = 7


def _autorizado_catequista():
    clave = request.args.get("clave") or (request.get_json(silent=True) or {}).get("clave")
    return clave == CLAVE_CATEQUISTA


def _dias_desde(fecha_iso):
    if not fecha_iso:
        return None
    try:
        fecha = datetime.datetime.fromisoformat(fecha_iso)
    except ValueError:
        return None
    return (datetime.datetime.utcnow() - fecha).days


def _semaforo(logradas, total, requiere_acompanamiento, dias_inactivo):
    """"al_dia" (verde): completó todo.
    "en_proceso" (amarillo): ya logró alguna actividad, sin señales de alerta.
    "sin_empezar" (neutro): todavía no logra ninguna, pero está dentro del
    margen de días normal — no hace falta alarmarse todavía.
    "necesita_animo" (rojo): tiene alguna actividad en
    REQUIERE_ACOMPANAMIENTO, o lleva más de DIAS_SIN_ACTIVIDAD_PARA_ANIMAR
    días sin entrar (haya empezado o no) con el itinerario sin terminar."""
    if logradas >= total:
        return "al_dia"
    if requiere_acompanamiento > 0:
        return "necesita_animo"
    if dias_inactivo is None or dias_inactivo >= DIAS_SIN_ACTIVIDAD_PARA_ANIMAR:
        return "necesita_animo"
    return "en_proceso" if logradas > 0 else "sin_empezar"


def _grupo_de_codigo(codigo):
    """Si el código sigue el patrón NOMBRE-G1 / NOMBRE-G2 / ..., devuelve
    "G1", "G2", etc. Si el código no trae un grupo al final (o el catequista
    no lo usó así), devuelve None — esos jóvenes caen en "Sin grupo"."""
    if "-" not in codigo:
        return None
    sufijo = codigo.rsplit("-", 1)[-1].strip().upper()
    if sufijo.startswith("G") and sufijo[1:].isdigit():
        return sufijo
    if sufijo.isdigit():
        return "G" + sufijo
    return None


def _normalizar_grupo(texto):
    """Convierte lo que escriba el catequista ("1", "g1", " G1 ") al mismo
    formato que usa _grupo_de_codigo ("G1"), para poder compararlos."""
    if not texto:
        return None
    texto = texto.strip().upper()
    if texto.startswith("G") and texto[1:].isdigit():
        return texto
    if texto.isdigit():
        return "G" + texto
    return texto  # por si el catequista usa otro formato de grupo


@app.route("/api/catequista/ninos")
def api_catequista_ninos():
    if not _autorizado_catequista():
        return jsonify({"error": "Clave de catequista incorrecta."}), 403

    grupo_filtro = _normalizar_grupo(request.args.get("grupo"))

    total_actividades = len(content.ACTIVIDADES)
    out = []
    grupos_disponibles = set()
    for n in db.listar_ninos():
        grupo_nino = _grupo_de_codigo(n["codigo"])
        if grupo_nino:
            grupos_disponibles.add(grupo_nino)
        if grupo_filtro and grupo_nino != grupo_filtro:
            continue
        conteos = db.resumen_nino(n["codigo"])
        logradas = conteos["LOGRADO"]
        dias_inactivo = _dias_desde(n["ultima_actividad"] or n["creado_en"])
        out.append({
            "codigo": n["codigo"],
            "grupo": grupo_nino,
            "creado_en": n["creado_en"],
            "ultima_actividad": n["ultima_actividad"],
            "dias_inactivo": dias_inactivo,
            "logradas": logradas,
            "total_actividades": total_actividades,
            "en_proceso": conteos["EN_PROCESO"],
            "requiere_acompanamiento": conteos["REQUIERE_ACOMPANAMIENTO"],
            "estado": _semaforo(logradas, total_actividades, conteos["REQUIERE_ACOMPANAMIENTO"], dias_inactivo),
        })
    # Los que necesitan ánimo primero, para que el catequista los vea de una vez.
    orden_estado = {"necesita_animo": 0, "en_proceso": 1, "sin_empezar": 2, "al_dia": 3}
    out.sort(key=lambda x: (orden_estado[x["estado"]], -(x["dias_inactivo"] or 0)))
    return jsonify({
        "ninos": out,
        "grupo_filtro": grupo_filtro,
        "grupos_disponibles": sorted(grupos_disponibles),
    })


@app.route("/api/catequista/nino/<codigo>")
def api_catequista_nino(codigo):
    if not _autorizado_catequista():
        return jsonify({"error": "Clave de catequista incorrecta."}), 403
    if not db.nino_existe(codigo):
        return jsonify({"error": "No hay ningún joven registrado con ese código."}), 404

    progreso = db.progreso_completo_nino(codigo)
    encuentros_out = []
    for e in content.ENCUENTROS:
        contenidos_out = []
        for c in content.contenidos_de_encuentro(e["id"]):
            aids = content.actividades_de_contenido(c["id"])
            actividades_out = []
            for aid in aids:
                a = content.ACTIVIDADES[aid]
                p = progreso.get(aid)
                actividades_out.append({
                    "id": aid,
                    "titulo": a["titulo"],
                    "tipo": a["tipo"],
                    "estado": p["estado"] if p else "NO_INICIADA",
                    "intentos": p["intentos"] if p else 0,
                    "pistas_usadas": p["pistas_usadas"] if p else 0,
                })
            contenidos_out.append({
                "id": c["id"],
                "titulo": c["titulo"],
                "actividades": actividades_out,
            })
        encuentros_out.append({
            "id": e["id"],
            "titulo": e["titulo"],
            "contenidos": contenidos_out,
        })

    return jsonify({"codigo": codigo, "encuentros": encuentros_out})


# ------------------------------------------------------- módulo de admin --
# Acción destructiva (borra TODO el progreso de TODOS los jóvenes, para
# reiniciar el tutorial de reforzamiento desde cero). Protegida con una
# clave separada de la de catequista y una frase de confirmación exacta,
# para que solo la persona que coordina el reinicio pueda hacerlo, y nunca
# por accidente. Antes de borrar, se guarda una copia de respaldo del
# archivo de la base de datos junto al original.

@app.route("/api/admin/estado-bd")
def api_admin_estado_bd():
    """Solo consulta cuántos jóvenes/intentos hay registrados ahora mismo —
    para que la pantalla de confirmación muestre el tamaño real antes de
    que la persona decida borrar."""
    clave = request.args.get("clave") or ""
    if clave != CLAVE_ADMIN:
        return jsonify({"error": "Clave de administrador incorrecta."}), 403
    return jsonify(db.contar_registros())


@app.route("/api/admin/limpiar-bd", methods=["POST"])
def api_admin_limpiar_bd():
    datos = request.get_json(silent=True) or {}
    clave = datos.get("clave") or ""
    confirmar = (datos.get("confirmar") or "").strip()

    if clave != CLAVE_ADMIN:
        return jsonify({"error": "Clave de administrador incorrecta."}), 403
    if confirmar != FRASE_CONFIRMACION_LIMPIEZA:
        return jsonify({
            "error": f'Para confirmar, escribe exactamente "{FRASE_CONFIRMACION_LIMPIEZA}".'
        }), 400

    conteo_antes = db.contar_registros()

    # Respaldo en JSON de todas las filas antes de borrar, por si hace
    # falta revisarlo o restaurarlo manualmente más adelante. Con MariaDB
    # ya no hay un único archivo .db que copiar (ver db.respaldar_a_archivo
    # en db.py), así que se vuelca el contenido completo de las tablas a
    # un JSON junto al código de la app.
    respaldo_nombre = None
    try:
        sello = datetime.datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        respaldo_nombre = f"catequesis_confirmacion_respaldo_{sello}.json"
        carpeta_respaldos = os.environ.get("CATEQUESIS_BACKUP_DIR") or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "respaldos"
        )
        respaldo_ruta = os.path.join(carpeta_respaldos, respaldo_nombre)
        db.respaldar_a_archivo(respaldo_ruta)
    except Exception:
        respaldo_nombre = None

    db.limpiar_todo()

    return jsonify({
        "ok": True,
        "ninos_eliminados": conteo_antes["ninos"],
        "intentos_eliminados": conteo_antes["intentos"],
        "respaldo": respaldo_nombre,
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
