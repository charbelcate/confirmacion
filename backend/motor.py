# -*- coding: utf-8 -*-
"""
Motor de formación + reforzamiento (versión mínima, fiel a las reglas del
documento maestro, sección "Motor de reforzamiento" / "Reglas generales del
motor para las 10 actividades"):

  - Un error aislado NO marca el contenido como no logrado.
  - 1er intento fallido: retroalimentación breve + nueva oportunidad.
  - 2do intento fallido: pista graduada (nivel 1).
  - 3er intento fallido: pista graduada (nivel 2, más específica).
  - 4to intento fallido: se reduce la exigencia y se da una explicación breve
    (se muestra la respuesta), el contenido queda EN_PROCESO.
  - 5to intento en adelante sin lograrlo: REQUIERE_ACOMPAÑAMIENTO — se
    sugiere pedir ayuda al catequista. Nunca se penaliza ni se pone nota.
  - Si se alcanza el requisito de logro (aunque haya sido con pistas), la
    actividad queda LOGRADA.
"""

ESTADOS = ("NO_LOGRADO", "EN_PROCESO", "LOGRADO", "REQUIERE_ACOMPANAMIENTO")


def evaluar(actividad, aciertos, total, intento):
    """Aplica las reglas del motor y devuelve el resultado de este intento."""
    requisito = actividad["requisito"]
    pistas = actividad.get("pistas", [])
    logrado = aciertos >= requisito

    if logrado:
        mensaje = actividad["feedback_ok"]
        if intento > 1:
            mensaje = "¡Muy bien! Lo lograste. " + mensaje
        return {
            "logrado": True,
            "estado_actividad": "LOGRADO",
            "aciertos": aciertos,
            "total": total,
            "requisito": requisito,
            "mensaje": mensaje,
            "pista": None,
            "mostrar_respuesta": False,
        }

    # No logrado todavía: graduar la respuesta según el número de intento.
    mensaje = actividad["feedback_falta"]
    pista = None
    mostrar_respuesta = False
    estado = "EN_PROCESO"

    if intento == 1:
        mensaje = actividad["feedback_falta"]
    elif intento == 2:
        pista = pistas[0] if len(pistas) > 0 else None
    elif intento == 3:
        pista = pistas[1] if len(pistas) > 1 else (pistas[0] if pistas else None)
    elif intento == 4:
        mostrar_respuesta = True
        mensaje = "No pasa nada, vamos a repasarlo juntos. " + actividad["feedback_falta"]
    else:
        estado = "REQUIERE_ACOMPANAMIENTO"
        mostrar_respuesta = True
        mensaje = "Vamos a pedirle ayuda a tu catequista para repasar esto juntos."

    return {
        "logrado": False,
        "estado_actividad": estado,
        "aciertos": aciertos,
        "total": total,
        "requisito": requisito,
        "mensaje": mensaje,
        "pista": pista,
        "mostrar_respuesta": mostrar_respuesta,
    }


def estado_contenido(estados_actividades):
    """
    estados_actividades: lista de estados (uno por actividad del contenido,
    o None si aún no se intentó). Devuelve el estado global del contenido.
    """
    total = len(estados_actividades)
    logradas = sum(1 for e in estados_actividades if e == "LOGRADO")
    intentadas = sum(1 for e in estados_actividades if e is not None)

    if logradas >= max(1, round(total * 0.8)):
        return "LOGRADO"
    if any(e == "REQUIERE_ACOMPANAMIENTO" for e in estados_actividades):
        return "REQUIERE_ACOMPANAMIENTO"
    if intentadas > 0:
        return "EN_PROCESO"
    return "NO_LOGRADO"
