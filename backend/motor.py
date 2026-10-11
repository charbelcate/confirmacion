# -*- coding: utf-8 -*-
"""
Motor de formación + reforzamiento.

Principio: la evaluación existe para ACOMPAÑAR, no para aprobar o reprobar.
Ninguna actividad puede bloquear el camino del joven: cada actividad admite
hasta MAX_INTENTOS (10) intentos con ayuda graduada; si al décimo intento no
se alcanza el requisito, se le MUESTRAN LOS RESULTADOS (respuestas correctas)
y puede SEGUIR ADELANTE.

Escalera de acompañamiento (intentos sin logro):
  1  -> retroalimentación breve + nueva oportunidad
  2  -> pista nivel 1
  3  -> pista nivel 2
  4  -> pista nivel 3 (la última disponible)
  5  -> cambio de enfoque: revisar elemento por elemento
  6  -> explicación breve del contenido (menor exigencia en la mirada)
  7  -> ejemplo resuelto: se muestra UNA respuesta correcta como modelo
  8  -> acompañamiento paso a paso
  9  -> último intento, con aviso amable de que luego se verán los resultados
  10 -> MOSTRAR RESULTADOS y seguir adelante
        (actividad: COMPLETADA_CON_RESULTADOS)

- Si en cualquier intento se alcanza el requisito, la actividad queda LOGRADO
  (aunque haya sido con ayuda; el historial conserva intentos y pistas).
- Después del intento 10 el joven puede volver a intentarlo cuando quiera:
  si lo logra pasa a LOGRADO; si no, sigue COMPLETADA_CON_RESULTADOS (nunca
  retrocede ni se bloquea).
- REQUIERE_ACOMPANAMIENTO ya no se asigna a una actividad suelta: se calcula
  a nivel de contenido cuando 2 o más de sus actividades terminaron con
  resultados mostrados (ver estado_contenido).
- Nunca se penaliza ni se pone nota.
"""

MAX_INTENTOS = 10
UMBRAL_ACOMPANAMIENTO = 2  # actividades con resultados mostrados en un mismo contenido

LOGRADO = "LOGRADO"
EN_PROCESO = "EN_PROCESO"
COMPLETADA_CON_RESULTADOS = "COMPLETADA_CON_RESULTADOS"
REQUIERE_ACOMPANAMIENTO = "REQUIERE_ACOMPANAMIENTO"
NO_LOGRADO = "NO_LOGRADO"

ESTADOS = (NO_LOGRADO, EN_PROCESO, LOGRADO, COMPLETADA_CON_RESULTADOS, REQUIERE_ACOMPANAMIENTO)

# Estados que cuentan como "actividad terminada" para poder avanzar.
ESTADOS_TERMINADOS = (LOGRADO, COMPLETADA_CON_RESULTADOS)

MENSAJES = {
    5: "Probemos de otra manera: revisa tus respuestas una por una, con calma.",
    6: "Vamos a repasar la idea central del tema antes de volver a intentarlo.",
    7: "Te muestro un ejemplo ya resuelto para que veas cómo es.",
    8: "Vamos paso a paso: empieza por lo que tienes más claro y deja lo difícil para el final.",
    9: "Inténtalo una vez más. Si no sale, revisaremos juntos los resultados y seguimos adelante.",
}
MENSAJE_RESULTADOS = ("Gracias por tu constancia: no te rendiste, y eso también es aprender. "
                      "Revisa con calma los resultados y sigamos adelante.")


def actividad_terminada(estado):
    return estado in ESTADOS_TERMINADOS


def _pista(pistas, nivel):
    """nivel 1..3 -> pista correspondiente (o la última disponible)."""
    if not pistas:
        return None
    return pistas[min(nivel, len(pistas)) - 1]


def evaluar(actividad, aciertos, total, intento, estado_previo=None):
    """Aplica las reglas del motor y devuelve el resultado de este intento."""
    requisito = actividad["requisito"]
    pistas = actividad.get("pistas", [])
    logrado = aciertos >= requisito

    base = {
        "aciertos": aciertos,
        "total": total,
        "requisito": requisito,
        "intentos_maximos": MAX_INTENTOS,
        "pista": None,
        "mostrar_ejemplo": False,
        "mostrar_respuesta": False,   # se conserva por compatibilidad
        "mostrar_resultados": False,
        "puede_continuar": False,
        "ultimo_intento": False,
    }

    if logrado:
        mensaje = actividad["feedback_ok"]
        if intento > 1:
            mensaje = "¡Muy bien! Lo lograste. " + mensaje
        return {**base, "logrado": True, "estado_actividad": LOGRADO,
                "mensaje": mensaje, "puede_continuar": True}

    # Ya había llegado al límite antes (reintento voluntario): no retrocede.
    if intento >= MAX_INTENTOS or estado_previo == COMPLETADA_CON_RESULTADOS:
        return {**base, "logrado": False, "estado_actividad": COMPLETADA_CON_RESULTADOS,
                "mensaje": MENSAJE_RESULTADOS, "mostrar_respuesta": True,
                "mostrar_resultados": True, "puede_continuar": True}

    r = {**base, "logrado": False, "estado_actividad": EN_PROCESO,
         "mensaje": actividad["feedback_falta"]}
    if intento in (2, 3, 4):
        r["pista"] = _pista(pistas, intento - 1)
    elif intento == 5:
        r["mensaje"] = MENSAJES[5] + " " + actividad["feedback_falta"]
        r["pista"] = _pista(pistas, 1)
    elif intento == 6:
        r["mensaje"] = MENSAJES[6]
        r["pista"] = _pista(pistas, 3)
    elif intento == 7:
        r["mensaje"] = MENSAJES[7]
        r["mostrar_ejemplo"] = True
    elif intento == 8:
        r["mensaje"] = MENSAJES[8]
        r["mostrar_ejemplo"] = True
        r["pista"] = _pista(pistas, 3)
    elif intento == 9:
        r["mensaje"] = MENSAJES[9]
        r["mostrar_ejemplo"] = True
        r["ultimo_intento"] = True
    return r


def estado_contenido(estados_actividades):
    """
    estados_actividades: lista de estados (uno por actividad del contenido,
    o None si aún no se intentó). Devuelve el estado global del contenido.
    Mostrar resultados NO equivale a LOGRADO.
    """
    total = len(estados_actividades)
    logradas = sum(1 for e in estados_actividades if e == LOGRADO)
    con_resultados = sum(1 for e in estados_actividades if e == COMPLETADA_CON_RESULTADOS)
    intentadas = sum(1 for e in estados_actividades if e is not None)

    if logradas >= max(1, round(total * 0.8)):
        return LOGRADO
    if con_resultados >= UMBRAL_ACOMPANAMIENTO or any(e == REQUIERE_ACOMPANAMIENTO for e in estados_actividades):
        return REQUIERE_ACOMPANAMIENTO
    if intentadas > 0:
        return EN_PROCESO
    return NO_LOGRADO
