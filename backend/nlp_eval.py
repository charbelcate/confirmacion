# -*- coding: utf-8 -*-
"""
Segunda capa de evaluación para respuestas abiertas: similitud semántica
con un modelo preentrenado de "sentence embeddings" (no un modelo
entrenado a la medida — para eso hace falta un historial real de
respuestas revisadas por un catequista, que todavía no existe).

Cómo se usa (ver app.py, función `_evaluar_item_abierto`): cuando la
respuesta del niño NO contiene ninguna de las `palabras_esperadas` del
ítem (primer filtro, en content.py), en vez de rechazarla de inmediato se
compara su significado con una lista de `respuestas_referencia` (también
en content.py, unas 2-3 frases correctas de ejemplo por ítem) usando este
módulo. Si el parecido de significado supera `UMBRAL_SIMILITUD`, la
respuesta se acepta igual, aunque use palabras distintas a las previstas
(por ejemplo: "Dios Vivo" para "¿Cómo llama san Pablo a la Iglesia?",
aunque "VIVO" no estuviera en la lista de palabras esperadas).

Diseño a prueba de fallos: TODO en este módulo está pensado para que, si
la librería no está instalada, o el modelo no se puede descargar (por
ejemplo, por no tener acceso a internet en el momento de arrancar el
servidor), la app nunca se caiga por esto — simplemente se sigue
evaluando solo con "palabras_esperadas", como si esta capa no existiera.
Por eso los imports de `sentence_transformers` están DENTRO de la función
(no arriba del archivo): así, aunque la librería no esté instalada,
`import nlp_eval` en app.py no falla nunca.

Nota para quien despliegue esto en su propio servidor: el modelo
(`MODELO_NOMBRE`) se descarga una sola vez, la primera vez que se usa, y
pesa unos cientos de MB — asegúrate de correr el servidor al menos una
vez con acceso a internet antes de ponerlo en un lugar sin conexión. El
valor de `UMBRAL_SIMILITUD` de abajo es un punto de partida razonable
pero no fue validado con respuestas reales (en el entorno donde se
escribió este código no había acceso a internet para probar el modelo
real) — conviene ajustarlo con el script de calibración sugerido en el
README una vez que el proyecto esté corriendo con conexión a internet.
"""
import functools
import logging

logger = logging.getLogger(__name__)

MODELO_NOMBRE = "paraphrase-multilingual-MiniLM-L12-v2"

# Umbral de similitud coseno (0.0 a 1.0) a partir del cual dos frases se
# consideran "el mismo significado". Provisional — ver nota arriba.
UMBRAL_SIMILITUD = 0.55

_modelo = None
_intento_carga_fallido = False


def _obtener_modelo():
    """Carga el modelo una sola vez (patrón singleton perezoso). Devuelve
    None si la librería no está instalada o el modelo no se pudo
    descargar/cargar — en ese caso no se vuelve a intentar en la misma
    ejecución del servidor, para no repetir un intento costoso que ya
    sabemos que va a fallar."""
    global _modelo, _intento_carga_fallido
    if _modelo is not None:
        return _modelo
    if _intento_carga_fallido:
        return None
    try:
        from sentence_transformers import SentenceTransformer
        _modelo = SentenceTransformer(MODELO_NOMBRE)
        logger.info("nlp_eval: modelo '%s' cargado correctamente.", MODELO_NOMBRE)
        return _modelo
    except Exception as exc:  # noqa: BLE001 - queremos capturar cualquier fallo
        _intento_carga_fallido = True
        logger.warning(
            "nlp_eval: no se pudo cargar el modelo de similitud semántica "
            "('%s'). La app seguirá funcionando solo con palabras_esperadas. "
            "Detalle: %s",
            MODELO_NOMBRE,
            exc,
        )
        return None


@functools.lru_cache(maxsize=256)
def _embedding_referencias(referencias_tupla):
    """Calcula (y cachea) los embeddings de una tupla de frases de
    referencia. Se cachea porque las listas `respuestas_referencia` de
    content.py son fijas: no tiene sentido recalcular sus embeddings en
    cada respuesta que manda un niño."""
    modelo = _obtener_modelo()
    if modelo is None:
        return None
    return modelo.encode(list(referencias_tupla), convert_to_tensor=True)


def similitud_maxima(texto, referencias):
    """Devuelve la mayor similitud (float entre 0.0 y 1.0) entre `texto`
    y cualquiera de las frases de `referencias`, o None si el modelo no
    está disponible (no instalado, o no se pudo descargar) — en ese caso
    quien llama debe ignorar esta capa y decidir solo con
    palabras_esperadas, no tratar el None como "no hay parecido"."""
    if not texto or not referencias:
        return None
    modelo = _obtener_modelo()
    if modelo is None:
        return None
    try:
        from sentence_transformers import util
        emb_refs = _embedding_referencias(tuple(referencias))
        if emb_refs is None:
            return None
        emb_texto = modelo.encode([texto], convert_to_tensor=True)
        puntajes = util.cos_sim(emb_texto, emb_refs)[0]
        return float(puntajes.max())
    except Exception as exc:  # noqa: BLE001
        logger.warning("nlp_eval: fallo al calcular similitud: %s", exc)
        return None
