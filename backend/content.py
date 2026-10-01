# -*- coding: utf-8 -*-
"""
Base de conocimiento — Camino de Confirmación (adolescentes y jóvenes)
========================================================================
Primer prototipo de construcción progresiva: los tres primeros temas del
programa de 22 encuentros — C0N1, C0N2 y C0N3 — cada uno con sus 6
contenidos y 10 actividades por contenido: 18 contenidos y 180
actividades en total. Se entrega así, a propósito, para que la
catequista/formadora lo revise antes de continuar con C0N4 a C0N22 (tal
como pide el propio documento fuente en su sección 12, "Propuesta de
revisión con el catequista").

Documento fuente: "Modelo de Formación y Reforzamiento de Catequesis —
Confirmación, adolescentes y jóvenes" (T1-T3), que a su vez toma como
referencia el modelo ya construido para Primera Comunión y lo adapta al
perfil adolescente/juvenil (14-16 años) y al temario de 22 encuentros.
Ese documento da, para cada uno de los 18 contenidos, su título,
competencia, cita bíblica principal y requisito de logro — y además
describe, de forma GENÉRICA e idéntica para los 18 contenidos, un banco
de 10 actividades por contenido (crucigrama avanzado, sopa de letras
estratégica, práctica con la Biblia, ordenar y reconstruir, verdadero/
falso con justificación, caso juvenil, podcast juvenil, creación digital
responsable, recuperación adaptativa y aplicación/misión), sin darles
contenido pedagógico concreto (palabras de crucigrama, afirmaciones,
casos, etc.) — igual que ocurrió con PC06-PC16 en el proyecto de
Primera Comunión. Ese contenido concreto de cada actividad se redactó
aquí siguiendo fielmente el objetivo, la competencia y la cita bíblica
que sí da el documento para cada contenido.

Encuentros de este primer prototipo:

  C0N1 — "Jesús nos llama a seguirlo" (C0N1-CO01 a C0N1-CO06,
         Marcos 1,16-20 / Mateo 28,19-20), sobre la vocación, el
         seguimiento y el discipulado: la llamada personal de Jesús, la
         respuesta libre, las prioridades que exige seguirlo, el
         discipulado como camino, los dones puestos al servicio de la
         misión y el seguimiento vivido en comunidad.
  C0N2 — "Jóvenes en la Biblia" (C0N2-CO01 a C0N2-CO06,
         1 Samuel 3,1-10 / Lucas 1,26-38), sobre Samuel y María como
         figuras juveniles de escucha y respuesta a la llamada de Dios:
         escuchar antes de responder, la fe confiada de María frente al
         miedo, la propia historia vocacional y el discernimiento
         acompañado.
  C0N3 — "Creer en tiempos de duda" (C0N3-CO01 a C0N3-CO06,
         Hechos 17,16-34), sobre la fe, la razón, la cultura y el
         anuncio del Evangelio a partir del discurso de Pablo en el
         Areópago: la duda que abre preguntas honestas, el diálogo con
         la cultura, la relación entre fe y razón, la cercanía de Dios,
         cómo responder preguntas difíciles y cómo dar razón de la
         esperanza con respeto.

Nomenclatura (sección 4 del documento fuente): C0N<n> identifica el
tema/encuentro, CO<nn> el contenido dentro del tema, y A<nn> la
actividad dentro del contenido — código completo, p. ej. C0N1-CO01-A03.
Es la misma estructura de PC<n>-C<nn>-A<nn> del proyecto de Primera
Comunión, solo que aquí el contenido usa el prefijo "CO" en vez de "C"
(para distinguirlo, tal como pide el propio documento fuente).

Mapeo de las 10 familias de actividad del documento fuente a los tipos
YA PROBADOS del motor de Primera Comunión (crucigrama, sopa_letras,
completar, verdadero_falso, seleccion_multiple, recuperacion,
aplicacion) — este proyecto reutiliza el motor entero (app.py, motor.py,
db.py) SIN NINGÚN CAMBIO de lógica, siguiendo el mismo criterio ya usado
varias veces en Primera Comunión: "reutilizar el motor ya probado en vez
de crear un tipo de actividad nuevo":

  A01 Crucigrama avanzado         -> tipo "crucigrama" (8 palabras en
                                      vez de 6, requisito más exigente)
  A02 Sopa de letras estratégica  -> tipo "sopa_letras" (8 palabras)
  A03 Práctica con la Biblia      -> tipo "completar" (idéntico a PC:
                                      un ítem cerrado con banco + un
                                      ítem "abierta" de reflexión)
  A04 Ordenar y reconstruir       -> tipo "completar": cada paso del
                                      relato/argumento se presenta
                                      desordenado como "pregunta", y la
                                      "respuesta" es su número de orden
                                      correcto (banco: "1".."5"), más un
                                      ítem "abierta" pidiendo justificar
                                      el orden elegido.
  A05 Verdadero/Falso justificado -> tipo "completar": cada afirmación
                                      es un ítem cuya "respuesta" es
                                      VERDADERO o FALSO (banco:
                                      ["VERDADERO","FALSO"]), más un
                                      ítem "abierta" pidiendo justificar
                                      una de las afirmaciones falsas.
  A06 Caso juvenil / selección    -> tipo "completar": cada caso es un
      razonada                       ítem cuya "respuesta" es la opción
                                      correcta (banco: las 3-4 opciones
                                      del caso), más un ítem "abierta"
                                      pidiendo justificar la elección.
  A07 Podcast juvenil             -> tipo "completar" con un solo ítem
                                      "abierta": el joven escribe el
                                      guion de su podcast (idea central +
                                      cita bíblica + aplicación), en vez
                                      de grabar audio de verdad — ver
                                      nota de diseño más abajo.
  A08 Creación digital responsable-> igual que A07: un solo ítem
                                      "abierta" donde el joven escribe el
                                      guion/storyboard, sin publicarlo ni
                                      grabarlo de verdad.
  A09 Recuperación adaptativa     -> tipo "recuperacion" (misma mecánica
                                      que completar, con un campo
                                      "reflexion" adicional no evaluado)
  A10 Aplicación y misión         -> tipo "aplicacion" (idéntico a PC:
                                      situación + una pregunta con varias
                                      opciones igualmente válidas)

Nota de diseño importante — A07/A08 (podcast, Reel/storyboard): el
documento fuente (sección 5 y 10) pide productos de audio/video breves,
pero aclara que "la creación digital no exige publicación pública" y que
"la actividad digital debe servir al aprendizaje, no un concurso de
popularidad". Grabar y calificar audio/video real está fuera del alcance
de este motor de reforzamiento automático (pensado para texto). Por eso,
en este prototipo, A07 y A08 se adaptan al mismo mecanismo de respuesta
abierta ya probado (el joven ESCRIBE el guion de su podcast o Reel, no
lo graba), evaluado con el mismo filtro de PALABRAS_ALERTA +
palabras_esperadas + similitud semántica que ya usa A03. Si más adelante
se quiere una versión con grabación real (subida de archivo, revisión
del catequista), sería una función nueva del motor, a evaluar después de
validar este primer prototipo.

Las respuestas del crucigrama y de los ítems tipo "completar" con banco
se escriben sin tildes ni Ñ, igual que en Primera Comunión, porque
generar_layout_crucigrama (en app.py) normaliza los acentos
automáticamente y la comparación de respuestas ya ignora acentos
(sin_acentos, en app.py).
"""

ENCUENTROS = [
    {
        "id": "C0N1",
        "titulo": "Jesús nos llama a seguirlo",
        "texto_biblico": "Marcos 1,16-20 / Mateo 28,19-20",
        "objetivo": "Descubrir el seguimiento de Jesús como una llamada personal que pide una respuesta libre.",
    },
    {
        "id": "C0N2",
        "titulo": "Jóvenes en la Biblia",
        "texto_biblico": "1 Samuel 3,1-10 / Lucas 1,26-38",
        "objetivo": "Reconocer en Samuel y en María una actitud de escucha y una respuesta confiada a la llamada de Dios.",
    },
    {
        "id": "C0N3",
        "titulo": "Creer en tiempos de duda",
        "texto_biblico": "Hechos 17,16-34",
        "objetivo": "Aprender, a partir de Pablo en el Areópago, a dialogar con la cultura y a dar razón de la propia fe con respeto.",
    },
]

CONTENIDOS = [
    {"id": "C0N1-CO01", "titulo": "Jesús llama por nuestro nombre"},
    {"id": "C0N1-CO02", "titulo": "Seguir a Jesús implica una respuesta"},
    {"id": "C0N1-CO03", "titulo": "Dejar las redes: prioridades y decisiones"},
    {"id": "C0N1-CO04", "titulo": "El discipulado es un camino"},
    {"id": "C0N1-CO05", "titulo": "Mis dones al servicio de la misión"},
    {"id": "C0N1-CO06", "titulo": "Seguir a Jesús con otros"},
    {"id": "C0N2-CO01", "titulo": "Samuel aprende a escuchar"},
    {"id": "C0N2-CO02", "titulo": "Habla, Señor: escuchar antes de responder"},
    {"id": "C0N2-CO03", "titulo": "María: una joven que responde con fe"},
    {"id": "C0N2-CO04", "titulo": "El miedo y la confianza"},
    {"id": "C0N2-CO05", "titulo": "Mi historia también puede ser llamada"},
    {"id": "C0N2-CO06", "titulo": "Discernir acompañados"},
    {"id": "C0N3-CO01", "titulo": "La duda puede abrir preguntas"},
    {"id": "C0N3-CO02", "titulo": "Pablo dialoga con la cultura"},
    {"id": "C0N3-CO03", "titulo": "Fe y razón no son enemigas"},
    {"id": "C0N3-CO04", "titulo": "Dios cercano al ser humano"},
    {"id": "C0N3-CO05", "titulo": "Responder a preguntas difíciles"},
    {"id": "C0N3-CO06", "titulo": "Dar razón de la esperanza"},
]

FEEDBACK_OK = "¡Muy bien! Sigue profundizando tu fe."
FEEDBACK_OK_ARGUMENTO = "¡Excelente! Supiste explicarlo con tus propias palabras."
FEEDBACK_OK_DISCERNIMIENTO = "¡Muy bien! Eso es discernir con calma."
FEEDBACK_FALTA = "Vamos a pensarlo juntos. Puedes intentarlo otra vez."

# Mensaje que recibe el joven cuando su respuesta abierta contiene una
# palabra de PALABRAS_ALERTA (ver más abajo), en vez del feedback_falta
# genérico de la actividad.
FEEDBACK_ALERTA = ("Esa respuesta no refleja lo que estamos trabajando en este tema. "
                    "Vuelve a pensarlo: ¿qué nos enseña este contenido sobre seguir a Jesús?")

# Mensaje que recibe el joven cuando su respuesta abierta no contiene
# ninguna palabra de alerta, pero tampoco toca el tema que se le
# pregunta (ver "palabras_esperadas" en los ítems y _evaluar_item_abierto
# en app.py).
FEEDBACK_FUERA_DE_TEMA = ("Escribiste algo, pero no se relaciona con lo que acabamos de leer o trabajar. "
                           "Vuelve a leer la cita bíblica o el caso planteado y responde otra vez con eso en mente.")

# Mismo mecanismo de dos niveles que en Primera Comunión (ver
# _evaluar_item_abierto en app.py): 1) coincidencia de palabras clave
# (PALABRAS_ALERTA / "palabras_esperadas"); 2) si el nivel 1 no encuentra
# nada y el ítem tiene "respuestas_referencia", se compara el SIGNIFICADO
# de la respuesta con esas frases (nlp_eval.similitud_maxima). Ninguno de
# los dos es un modelo de lenguaje perfecto: son filtros de apoyo, no un
# reemplazo del acompañamiento del catequista ante respuestas sensibles
# (tal como pide la sección 10 del documento fuente).
PALABRAS_ALERTA = {
    "ODIAR", "ODIO", "MATAR", "MATARIA", "PEGAR", "GOLPEAR", "GOLPE",
    "INSULTAR", "INSULTO", "MENTIR", "MENTIRA", "ROBAR", "ROBO",
    "HERIR", "LASTIMAR", "MALTRATAR", "MALTRATO", "BURLARSE", "BURLAR",
    "HUMILLAR", "DESPRECIAR", "DESTRUIR", "PELEAR", "PELEA", "VENGAR",
    "VENGANZA", "ABANDONAR", "TRAICIONAR", "TRAICION", "RIDICULIZAR",
}

ACTIVIDADES = {}


def _agregar(contenido_id, sufijo, actividad):
    actividad = dict(actividad)
    actividad["contenido_id"] = contenido_id
    actividad.setdefault("feedback_ok", FEEDBACK_OK)
    actividad.setdefault("feedback_falta", FEEDBACK_FALTA)
    actividad.setdefault("pistas", [])
    ACTIVIDADES[f"{contenido_id}-{sufijo}"] = actividad


# ==========================================================================
# C0N1 — Jesús nos llama a seguirlo   (Marcos 1,16-20)
# ==========================================================================

# --- C0N1-CO01 — Jesús llama por nuestro nombre --------------------------
_agregar("C0N1-CO01", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: la llamada junto al lago",
    "items": [
        {"texto": "Palabra que resume lo que Jesús hace cuando invita a alguien a seguirlo.", "respuesta": "LLAMADA"},
        {"texto": "Quien camina por la orilla del lago de Galilea y llama a los primeros discípulos.", "respuesta": "JESUS"},
        {"texto": "Nombre del primer pescador que Jesús llama (después será Pedro).", "respuesta": "SIMON"},
        {"texto": "Hermano de Simón, llamado junto con él.", "respuesta": "ANDRES"},
        {"texto": "Oficio de los primeros que Jesús llama.", "respuesta": "PESCADORES"},
        {"texto": "Lo que hacen los llamados: caminar detrás de Jesús y aprender de él.", "respuesta": "SEGUIR"},
        {"texto": "Lo que Simón y Andrés dejan en el suelo para seguir a Jesús.", "respuesta": "REDES"},
        {"texto": "Quien aprende de un maestro y camina con él; así queda Simón después de la llamada.", "respuesta": "DISCIPULO"},
    ],
    "incluir": ["JESUS", "LLAMADA"],
    "requisito": 6,
    "pistas": ["Todas las palabras aparecen en el relato de Marcos 1,16-20.",
               "JESUS y LLAMADA son las palabras centrales del contenido: empieza por esas."],
})

_agregar("C0N1-CO01", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: junto al lago de Galilea",
    "palabras": ["LLAMADA", "JESUS", "SIMON", "ANDRES", "PESCADORES", "SEGUIR", "REDES", "DISCIPULO"],
    "incluir": ["JESUS", "LLAMADA"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: JESUS y SIMON.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N1-CO01", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Marcos 1,16-20",
    "items": [
        {
            "texto": "Busca en tu Biblia Marcos 1,16-20 y completa lo que dice Jesús: «Venid en pos de mí, y os haré ______ de hombres.»",
            "respuesta": "PESCADORES",
            "banco": ["PESCADORES", "GUIAS", "MAESTROS"],
        },
        {
            "texto": "¿Qué crees que sintieron Simón y Andrés al escuchar a Jesús llamarlos por su nombre? ¿Alguna vez sentiste que Dios te invitaba a hacer algo?",
            "abierta": True,
            "palabras_esperadas": ["LLAMADO", "LLAMADA", "DIOS", "JESUS", "SEGUIR", "SORPRESA", "ALEGRIA", "MIEDO", "CONFIANZA", "INVITACION"],
            "respuestas_referencia": [
                "Sentí que Dios me invitaba a algo y me dio un poco de miedo pero también alegría.",
                "Alguna vez sentí que Dios me llamaba a ayudar a alguien y decidí hacerle caso a esa idea.",
                "Creo que se sorprendieron, pero confiaron en Jesús y lo siguieron sin dudarlo.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el evangelio de Marcos en el índice de tu Biblia; el capítulo es el 1.",
               "Lee los versículos 16 al 20 completos: la palabra que falta aparece tal como está en el texto."],
})

_agregar("C0N1-CO01", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: la escena junto al lago",
    "items": [
        {"texto": "Simón y Andrés lo siguen como discípulos.", "respuesta": "5", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Jesús camina por la orilla del mar de Galilea.", "respuesta": "1", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Simón y Andrés dejan las redes en el suelo.", "respuesta": "4", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Jesús ve a Simón y Andrés echando la red al mar.", "respuesta": "2", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Jesús los llama: «Venid en pos de mí».", "respuesta": "3", "banco": ["1", "2", "3", "4", "5"]},
        {
            "texto": "Justifica: ¿por qué crees que dejar las redes fue un paso importante antes de poder seguir a Jesús?",
            "abierta": True,
            "palabras_esperadas": ["DEJAR", "PRIORIDAD", "DECISION", "CONFIAR", "TRABAJO", "REDES", "LIBRE", "ESPACIO"],
            "respuestas_referencia": [
                "Porque mientras seguían aferrados a las redes no podían caminar detrás de Jesús con libertad.",
                "Dejar las redes fue una decisión que les hizo espacio en su vida para seguir a Jesús.",
                "Fue necesario soltar lo que tenían para poder confiar y seguir a Jesús de verdad.",
            ],
        },
    ],
    "requisito": 5,
    "pistas": ["Relee Marcos 1,16-20 en orden: primero Jesús camina, después ve, después llama.",
               "Los dos últimos pasos son dejar las redes y, solo después, seguirlo."],
})

_agregar("C0N1-CO01", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Jesús llamó a Simón y Andrés mientras estaban pescando.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Simón y Andrés tardaron varios días en decidir si seguían a Jesús.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Seguir a Jesús no les pidió ningún cambio en su vida cotidiana.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "La llamada de Jesús fue personal, dirigida a personas concretas y por su nombre.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas de arriba y explica, con el texto bíblico, por qué es falsa.",
            "abierta": True,
            "palabras_esperadas": ["INMEDIATO", "ENSEGUIDA", "DEJARON", "CAMBIO", "REDES", "RAPIDO", "LUEGO", "DECIDIERON"],
            "respuestas_referencia": [
                "Es falsa porque el texto dice que dejaron las redes en seguida, no que lo pensaron muchos días.",
                "Es falsa porque seguir a Jesús sí les cambió la vida: dejaron su trabajo de pescadores.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Marcos usa la palabra «en seguida» para describir la respuesta de los primeros discípulos.",
               "Dejar las redes y el barco sí fue un cambio grande en su vida cotidiana."],
})

_agregar("C0N1-CO01", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: responder a una llamada",
    "items": [
        {
            "texto": "Caso 1: Tomás siente que Dios lo invita a acercarse más a su parroquia, pero sus amigos se burlan de los que van seguido a misa. ¿Qué es lo más coherente con la llamada de Jesús a Simón y Andrés?",
            "respuesta": "Seguir yendo y hablarlo con su grupo de catequesis",
            "banco": ["Seguir yendo y hablarlo con su grupo de catequesis", "Dejar de ir para no sentirse distinto", "Ir a escondidas sin contarle a nadie"],
        },
        {
            "texto": "Caso 2: Valentina nota que pasa horas en el celular y le cuesta encontrar un momento para orar o leer la Biblia. ¿Cuál sería su versión de «dejar las redes»?",
            "respuesta": "Ponerse un horario fijo, corto, para desconectarse y estar con Dios",
            "banco": ["Ponerse un horario fijo, corto, para desconectarse y estar con Dios", "Borrar el celular para siempre sin ningún plan", "No cambiar nada porque el celular no tiene nada que ver con la fe"],
        },
        {
            "texto": "Caso 3: Un compañero le pregunta a Mateo por qué va a la catequesis de Confirmación. ¿Cuál es la respuesta más fiel al espíritu de la llamada de Jesús?",
            "respuesta": "Contarle con sencillez lo que significa para él seguir a Jesús",
            "banco": ["Contarle con sencillez lo que significa para él seguir a Jesús", "Cambiar de tema porque da vergüenza", "Presionarlo para que también vaya"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa es la opción más coherente con seguir a Jesús.",
            "abierta": True,
            "palabras_esperadas": ["JESUS", "SEGUIR", "COHERENTE", "FE", "DECISION", "LLAMADA", "PRIORIDAD"],
            "respuestas_referencia": [
                "Elegí el caso de Tomás, porque seguir a Jesús a veces pide sostener una decisión aunque otros se burlen.",
                "Elegí el caso de Valentina, porque hacerle espacio a Dios en la semana es una forma de responder a la llamada.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["En los tres casos, la opción coherente es la que sostiene la fe sin esconderla ni imponerla.",
               "Piensa qué haría alguien que, como Simón y Andrés, ya decidió seguir a Jesús."],
})

_agregar("C0N1-CO01", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: ¿qué significa seguir a Jesús hoy?",
    "items": [
        {
            "texto": "Vas a grabar un podcast de 2 a 3 minutos titulado «¿Qué significa seguir a Jesús hoy?». Escribe aquí el guion: una idea central, una referencia a Marcos 1,16-20 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["JESUS", "SEGUIR", "LLAMADA", "REDES", "DISCIPULO", "MARCOS", "RESPONDER"],
            "respuestas_referencia": [
                "Seguir a Jesús hoy es responder a su llamada en lo cotidiano, como Simón y Andrés dejaron las redes para seguirlo.",
                "Idea central: Jesús sigue llamando hoy. Cita: Marcos 1,16-20. Aplicación: elegir una prioridad esta semana para seguirlo mejor.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Empieza por escribir en una frase la idea central de tu podcast, antes de desarrollarla.",
               "No olvides mencionar Marcos 1,16-20 y cerrar con algo concreto de tu propia vida."],
})

_agregar("C0N1-CO01", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: una decisión que cambia el rumbo",
    "items": [
        {
            "texto": "Escribe el guion de un Reel de 45 segundos titulado «Una decisión que cambia el rumbo», inspirado en que Simón y Andrés dejaron las redes. No hace falta grabarlo ni publicarlo: describe las escenas y el mensaje.",
            "abierta": True,
            "palabras_esperadas": ["DEJAR", "DECISION", "SEGUIR", "JESUS", "CAMBIO", "REDES", "ESCENA"],
            "respuestas_referencia": [
                "Escena 1: alguien ocupado con su rutina. Escena 2: recibe una invitación importante. Escena 3: decide responder y su vida cambia, como Simón y Andrés al dejar las redes.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en tres escenas cortas: antes, el momento de la decisión, y después.",
               "El mensaje final debe conectar con dejar algo para seguir a Jesús."],
})

_agregar("C0N1-CO01", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: la llamada junto al lago",
    "items": [
        {
            "texto": "Completa: los primeros discípulos de Jesús eran ______ antes de seguirlo.",
            "respuesta": "PESCADORES",
            "banco": ["PESCADORES", "PASTORES", "AGRICULTORES"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué «redes» (cosas que te cuesta soltar) tendrías que dejar tú para seguir más de cerca a Jesús? Coméntalo con tu catequista.",
    "pistas": ["Piensa en el oficio de Simón y Andrés antes de conocer a Jesús."],
})

_agregar("C0N1-CO01", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: responder esta semana",
    "situacion": "Esta semana tienes varias oportunidades de responder a la llamada de Jesús: en la misa, en un momento de oración, ayudando a alguien o participando en tu grupo de catequesis.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para responder a la llamada de Jesús, como hicieron Simón y Andrés?",
            "opciones": [
                "Participar activamente en la misa del domingo",
                "Dedicar unos minutos diarios a la oración",
                "Ayudar a un compañero sin que te lo pidan",
                "Quedarme como estoy, sin cambiar nada",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una acción concreta que puedas hacer esta semana, no en una idea abstracta.",
               "Descarta la única opción que no responde a ninguna llamada."],
    "feedback_ok": "¡Muy bien! Responder a la llamada de Jesús empieza por gestos pequeños y concretos.",
})


# --- C0N1-CO02 — Seguir a Jesús implica una respuesta ---------------------
_agregar("C0N1-CO02", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: una respuesta libre",
    "items": [
        {"texto": "Lo que Jesús espera después de llamar: no una obligación, sino una...", "respuesta": "RESPUESTA"},
        {"texto": "Cualidad de una decisión que no se toma por presión ni por miedo.", "respuesta": "LIBRE"},
        {"texto": "Lo contrario de quedarse quieto: moverse, actuar, decidir.", "respuesta": "ACTUAR"},
        {"texto": "Palabra que describe la fe que confía aunque no se vea todo con claridad.", "respuesta": "CONFIANZA"},
        {"texto": "Lo que Simón y Andrés hacen «en seguida», sin dudarlo demasiado.", "respuesta": "OBEDECER"},
        {"texto": "Lo que Jesús pronuncia y que cambia el rumbo de la vida de dos pescadores.", "respuesta": "PALABRA"},
        {"texto": "Sentimiento que puede aparecer antes de tomar una decisión importante.", "respuesta": "DUDA"},
        {"texto": "Lo que se necesita para pasar de escuchar a Jesús a caminar con él.", "respuesta": "DECISION"},
    ],
    "incluir": ["RESPUESTA", "LIBRE"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con cómo se responde a una llamada.",
               "RESPUESTA y LIBRE son las palabras centrales: empieza por esas."],
})

_agregar("C0N1-CO02", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: responder con libertad",
    "palabras": ["RESPUESTA", "LIBRE", "ACTUAR", "CONFIANZA", "OBEDECER", "PALABRA", "DUDA", "DECISION"],
    "incluir": ["RESPUESTA", "LIBRE"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: DUDA y LIBRE.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N1-CO02", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Marcos 1,16-20",
    "items": [
        {
            "texto": "Busca en tu Biblia Marcos 1,18 y completa: «Y ______ dejando las redes, le siguieron.»",
            "respuesta": "ENSEGUIDA",
            "banco": ["ENSEGUIDA", "DESPUES", "NUNCA"],
        },
        {
            "texto": "¿Qué significa para ti que la respuesta de Simón y Andrés haya sido libre, y no obligada?",
            "abierta": True,
            "palabras_esperadas": ["LIBRE", "LIBERTAD", "ELECCION", "DECISION", "VOLUNTAD", "PROPIA", "CONVENCIDO"],
            "respuestas_referencia": [
                "Significa que nadie los obligó: ellos eligieron seguir a Jesús por su propia voluntad.",
                "Que la fe no se impone, se elige con libertad, igual que Simón y Andrés eligieron seguir a Jesús.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["El versículo está justo después de que Jesús los llama.",
               "La palabra que falta describe la rapidez de la respuesta."],
})

_agregar("C0N1-CO02", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: de la llamada a la respuesta",
    "items": [
        {"texto": "Simón y Andrés caminan junto a Jesús como discípulos.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Jesús pronuncia la invitación: «Venid en pos de mí».", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Simón y Andrés escuchan y consideran lo que se les pide.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Simón y Andrés deciden libremente responder que sí.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué el paso 3 (decidir libremente) es indispensable antes del paso 4 (caminar con Jesús)?",
            "abierta": True,
            "palabras_esperadas": ["LIBRE", "DECISION", "ELEGIR", "VOLUNTAD", "RESPUESTA", "CONVENCIDO"],
            "respuestas_referencia": [
                "Porque sin decidirlo libremente no sería una verdadera respuesta de fe, sino solo obedecer por obligación.",
                "Porque seguir a Jesús solo tiene sentido si se elige de verdad, no si se hace por presión.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Entre escuchar la invitación y caminar con Jesús hay siempre un momento de decisión libre.",
               "El orden va de la invitación a la decisión, y de la decisión a la acción."],
})

_agregar("C0N1-CO02", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Responder a Jesús es un acto libre, no una obligación impuesta.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Simón y Andrés respondieron a Jesús con indiferencia, sin darle importancia.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Una respuesta de fe verdadera nunca puede tener un poco de duda antes de decidirse.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dejar las redes fue la forma concreta en que Simón y Andrés expresaron su respuesta.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y justifica por qué lo es, con tus propias palabras.",
            "abierta": True,
            "palabras_esperadas": ["LIBRE", "DUDA", "NORMAL", "DECISION", "IMPORTANCIA", "ENSEGUIDA"],
            "respuestas_referencia": [
                "Es falsa porque el texto muestra que respondieron enseguida y con decisión, no con indiferencia.",
                "Es falsa porque es normal tener algo de duda antes de decidir algo importante; eso no anula la fe.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa si la actitud de Simón y Andrés fue de indiferencia o de decisión.",
               "Tener dudas antes de decidir no es lo mismo que no tener fe."],
})

_agregar("C0N1-CO02", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: decidir con libertad",
    "items": [
        {
            "texto": "Caso 1: Camila está considerando confirmarse, pero sus papás son quienes más insisten. Ella todavía no está segura de qué piensa. ¿Qué le convendría hacer primero?",
            "respuesta": "Hablar con su catequista sobre lo que ella misma piensa y siente",
            "banco": ["Hablar con su catequista sobre lo que ella misma piensa y siente", "Confirmarse solo para no discutir con sus papás", "Decir que no quiere ir más sin pensarlo"],
        },
        {
            "texto": "Caso 2: Diego siente que Dios lo invita a algo, pero le preocupa qué van a pensar sus compañeros de clase. ¿Cuál es la actitud más parecida a la de Simón y Andrés?",
            "respuesta": "Responder con libertad, aunque le tome un momento decidirse",
            "banco": ["Responder con libertad, aunque le tome un momento decidirse", "No responder nunca por miedo al qué dirán", "Responder solo si nadie más se entera"],
        },
        {
            "texto": "Caso 3: Sofía duda si de verdad quiere seguir en la catequesis de Confirmación. ¿Qué opción refleja mejor que la fe se elige con libertad?",
            "respuesta": "Conversar sus dudas con su catequista antes de decidir",
            "banco": ["Conversar sus dudas con su catequista antes de decidir", "Fingir que no tiene dudas para que nadie se preocupe", "Dejarlo todo de inmediato sin hablarlo con nadie"],
        },
        {
            "texto": "Elige uno de los tres casos y explica por qué esa opción respeta que la respuesta a Jesús sea libre.",
            "abierta": True,
            "palabras_esperadas": ["LIBRE", "LIBERTAD", "DECISION", "PROPIA", "RESPETO", "DUDA"],
            "respuestas_referencia": [
                "Elegí el caso de Camila, porque decidir con libertad significa pensarlo ella misma y no solo por sus papás.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["En los tres casos, la mejor opción es la que respeta la libertad y el proceso personal de decidir.",
               "Tener dudas y conversarlas no es lo opuesto a tener fe."],
})

_agregar("C0N1-CO02", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: decidir con libertad",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «¿Por qué la fe se elige y no se impone?». Incluye una idea central, una referencia a Marcos 1,16-20 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["LIBRE", "LIBERTAD", "ELEGIR", "DECISION", "JESUS", "RESPUESTA"],
            "respuestas_referencia": [
                "Idea central: la fe se elige libremente, como Simón y Andrés eligieron seguir a Jesús. Aplicación: reconocer una decisión de fe que yo mismo he tomado.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Empieza definiendo, en una frase, qué significa para ti que la fe sea libre.",
               "Cierra con un ejemplo concreto de tu propia vida."],
})

_agregar("C0N1-CO02", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: elegir por convicción",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) titulado «Elegir por convicción, no por presión», relacionado con la respuesta libre de Simón y Andrés. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["LIBRE", "CONVICCION", "DECISION", "PRESION", "ELEGIR"],
            "respuestas_referencia": [
                "Escena 1: alguien siente presión de un grupo. Escena 2: se detiene a pensar qué quiere de verdad. Escena 3: decide por convicción propia, como Simón y Andrés.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una situación juvenil donde decidir por convicción sea más difícil que dejarse llevar."],
})

_agregar("C0N1-CO02", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: una respuesta libre",
    "items": [
        {
            "texto": "Completa: la respuesta de Simón y Andrés a Jesús fue un acto ______, no una obligación.",
            "respuesta": "LIBRE",
            "banco": ["LIBRE", "FORZADO", "AUTOMATICO"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Alguna vez sentiste presión (de tu familia, tus amigos o del grupo) para tomar una decisión de fe? ¿Cómo lo manejaste? Coméntalo con tu catequista.",
    "pistas": ["Piensa en cómo describe el texto la respuesta de Simón y Andrés."],
})

_agregar("C0N1-CO02", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: una decisión propia",
    "situacion": "Seguir a Jesús es una decisión que se toma libremente, no por presión de otros ni por costumbre.",
    "items": [
        {
            "texto": "¿Qué puedes hacer esta semana para tomar tú mismo, con libertad, una decisión que acerque tu vida a Jesús?",
            "opciones": [
                "Elegir un momento de oración personal, sin que nadie me lo pida",
                "Preguntarme honestamente qué pienso yo de la fe, y hablarlo con mi catequista",
                "Participar en la catequesis por decisión propia, no solo por costumbre",
                "Dejar que otros decidan por mí sin pensarlo",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una acción que de verdad decidas tú, no que te impongan.",
               "Descarta la única opción que evita decidir por ti mismo."],
    "feedback_ok": "¡Muy bien! Decidir por ti mismo es parte de responder con libertad a la llamada de Jesús.",
})

# --- C0N1-CO03 — Dejar las redes: prioridades y decisiones ---------------
_agregar("C0N1-CO03", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: elegir prioridades",
    "items": [
        {"texto": "Lo que Simón y Andrés dejan en el suelo para poder seguir a Jesús.", "respuesta": "REDES"},
        {"texto": "Lo primero que se pone al elegir entre varias cosas importantes.", "respuesta": "PRIORIDAD"},
        {"texto": "Acto de elegir una opción entre varias posibles.", "respuesta": "DECISION"},
        {"texto": "Lo que ocupa el tiempo diario: estudios, redes sociales, amigos, deportes.", "respuesta": "RUTINA"},
        {"texto": "Palabra que describe algo que ocupa el primer lugar en la vida de alguien.", "respuesta": "CENTRAL"},
        {"texto": "Lo que se necesita soltar cuando algo nuevo e importante llega a la vida.", "respuesta": "SOLTAR"},
        {"texto": "Sinónimo de escoger, entre dos o más caminos posibles.", "respuesta": "ELEGIR"},
        {"texto": "Lo que tiene la vida cuando las prioridades están bien ordenadas.", "respuesta": "SENTIDO"},
    ],
    "incluir": ["PRIORIDAD", "DECISION"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con elegir qué va primero en la vida.",
               "PRIORIDAD y DECISION son las palabras centrales: empieza por esas."],
})

_agregar("C0N1-CO03", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: elegir prioridades",
    "palabras": ["REDES", "PRIORIDAD", "DECISION", "RUTINA", "CENTRAL", "SOLTAR", "ELEGIR", "SENTIDO"],
    "incluir": ["PRIORIDAD", "DECISION"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: REDES y SOLTAR.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N1-CO03", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Marcos 1,16-20",
    "items": [
        {
            "texto": "Busca en tu Biblia Marcos 1,18 y completa: «Y dejando las ______, le siguieron.»",
            "respuesta": "REDES",
            "banco": ["REDES", "BARCAS", "FAMILIAS"],
        },
        {
            "texto": "¿Qué «red» tendrías tú que dejar o reordenar en tu vida para darle más espacio a Jesús?",
            "abierta": True,
            "palabras_esperadas": ["TIEMPO", "CELULAR", "REDES", "PRIORIDAD", "ORDENAR", "ESPACIO", "DEJAR"],
            "respuestas_referencia": [
                "Tendría que ordenar mejor el tiempo que uso en el celular para hacerle espacio a la oración.",
                "Mi «red» sería la pereza para participar en la catequesis; tendría que dejarla de lado.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["El versículo describe qué dejan Simón y Andrés antes de seguir a Jesús.",
               "Piensa en algo real de tu semana, no solo en una idea general."],
})

_agregar("C0N1-CO03", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: cómo se elige una prioridad",
    "items": [
        {"texto": "Se elige la nueva prioridad y se actúa en consecuencia.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se identifica qué ocupa hoy el primer lugar en la vida.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se reconoce qué es lo que de verdad importa a la luz de la fe.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se compara lo que ocupa el primer lugar con lo que de verdad importa.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué comparar (paso 3) es necesario antes de poder elegir (paso 4)?",
            "abierta": True,
            "palabras_esperadas": ["COMPARAR", "DISCERNIR", "PENSAR", "DECIDIR", "CLARIDAD"],
            "respuestas_referencia": [
                "Porque sin comparar no se sabe si hay que cambiar algo; comparar da claridad antes de decidir.",
                "Porque decidir sin pensar antes puede llevar a elegir mal lo que realmente importa.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de identificar, a reconocer lo que importa, a comparar, y solo al final elegir.",
               "Elegir una prioridad sin antes pensarla no sería un verdadero discernimiento."],
})

_agregar("C0N1-CO03", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Elegir una prioridad significa que todo lo demás deja de importar por completo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Simón y Andrés reordenaron su vida para poder seguir a Jesús.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Un joven de hoy también puede tener que elegir prioridades para vivir su fe.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dejar las redes fue una decisión sin ningún costo real para los primeros discípulos.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["COSTO", "SACRIFICIO", "IMPORTA", "TRABAJO", "CAMBIO"],
            "respuestas_referencia": [
                "Es falsa porque dejar el trabajo de pescadores sí tuvo un costo real para Simón y Andrés.",
                "Es falsa porque elegir una prioridad no borra lo demás, solo lo ordena en su lugar.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Elegir una prioridad es ordenar, no eliminar todo lo demás.",
               "Piensa si dejar las redes y el barco tuvo o no un costo real."],
})

_agregar("C0N1-CO03", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: prioridades de verdad",
    "items": [
        {
            "texto": "Caso 1: Andrea tiene un examen importante el mismo día del retiro de Confirmación. ¿Qué actitud refleja mejor un discernimiento sano de prioridades?",
            "respuesta": "Buscar con tiempo cómo cumplir con ambas responsabilidades, sin dejar todo para último momento",
            "banco": ["Buscar con tiempo cómo cumplir con ambas responsabilidades, sin dejar todo para último momento", "Faltar al retiro sin avisar a nadie", "Faltar al examen sin hablar con sus profesores"],
        },
        {
            "texto": "Caso 2: Luis nota que dedica más horas a los videojuegos que a cualquier otra cosa en su semana. ¿Cuál sería un paso realista de reordenar prioridades?",
            "respuesta": "Ponerse un límite de tiempo y usar el resto para otras cosas importantes",
            "banco": ["Ponerse un límite de tiempo y usar el resto para otras cosas importantes", "Dejar los videojuegos de un día para otro sin ningún plan", "No cambiar nada porque son solo videojuegos"],
        },
        {
            "texto": "Caso 3: Fernanda tiene que elegir entre un plan con amigas y acompañar a su catequesis un domingo especial. ¿Qué le ayudaría a decidir mejor?",
            "respuesta": "Preguntarse qué es lo que de verdad quiere priorizar esa semana, y decidir con calma",
            "banco": ["Preguntarse qué es lo que de verdad quiere priorizar esa semana, y decidir con calma", "Decidir solo por lo que le da más pereza", "Dejar que decidan sus amigas por ella"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja un discernimiento maduro de prioridades.",
            "abierta": True,
            "palabras_esperadas": ["PRIORIDAD", "DISCERNIR", "PENSAR", "MADURO", "DECIDIR", "ORDEN"],
            "respuestas_referencia": [
                "Elegí el caso de Andrea, porque buscar con tiempo una solución es más maduro que decidir a último momento.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción madura siempre es la que piensa con calma, no la que actúa por impulso.",
               "Elegir prioridades no significa abandonar responsabilidades sin más."],
})

_agregar("C0N1-CO03", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mis prioridades hoy",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «¿Qué redes tengo que dejar yo?». Incluye una idea central, una referencia a Marcos 1,16-20 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["PRIORIDAD", "REDES", "DECISION", "ORDENAR", "JESUS", "ELEGIR"],
            "respuestas_referencia": [
                "Idea central: todos tenemos «redes» que reordenar para seguir a Jesús. Aplicación: elegir una prioridad concreta para esta semana.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una prioridad real de tu semana antes de escribir el guion.",
               "Cierra con un paso concreto y realista, no con una idea general."],
})

_agregar("C0N1-CO03", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: reordenar prioridades",
    "items": [
        {
            "texto": "Escribe el guion de un Reel de 45 segundos: «Lo que de verdad importa», mostrando cómo alguien reordena sus prioridades para hacerle espacio a su fe. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["PRIORIDAD", "ORDENAR", "IMPORTA", "FE", "ESPACIO", "DECISION"],
            "respuestas_referencia": [
                "Escena 1: alguien con la agenda llena. Escena 2: se detiene a pensar qué es lo que de verdad importa. Escena 3: le hace espacio a su fe en la semana.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en tres escenas cortas: antes, el momento de pensar, y el cambio."],
})

_agregar("C0N1-CO03", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: elegir prioridades",
    "items": [
        {
            "texto": "Completa: Simón y Andrés dejaron sus ______ para poder seguir a Jesús.",
            "respuesta": "REDES",
            "banco": ["REDES", "FAMILIAS", "CASAS"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Cuál es hoy tu prioridad número uno? ¿Le hace espacio a tu fe o la deja de lado? Coméntalo con tu catequista.",
    "pistas": ["Piensa en lo que Simón y Andrés dejaron en el suelo junto al lago."],
})

_agregar("C0N1-CO03", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: reordenar mi semana",
    "situacion": "Así como Simón y Andrés reordenaron su vida para seguir a Jesús, cada joven puede reordenar algo de su semana para darle más espacio a su fe.",
    "items": [
        {
            "texto": "¿Qué puedes reordenar tú esta semana para hacerle más espacio a tu fe?",
            "opciones": [
                "Reducir el tiempo en el celular para tener un momento de oración",
                "Organizar mejor mis tareas para no faltar a la catequesis",
                "Elegir conscientemente un momento de la semana para leer la Biblia",
                "Dejar todo exactamente igual que antes",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un cambio pequeño y realista, no en una transformación total.",
               "Descarta la única opción que no reordena nada."],
    "feedback_ok": "¡Muy bien! Reordenar la semana, aunque sea en algo pequeño, ya es un paso de discipulado.",
})


# --- C0N1-CO04 — El discipulado es un camino ------------------------------
_agregar("C0N1-CO04", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: un camino, no un salto",
    "items": [
        {"texto": "Palabra que describe el discipulado: no es un salto, es un...", "respuesta": "CAMINO"},
        {"texto": "Lo que sucede cuando alguien cambia de mentalidad y de vida por Dios.", "respuesta": "CONVERSION"},
        {"texto": "Lo contrario de quedarse igual: mejorar poco a poco.", "respuesta": "CRECER"},
        {"texto": "Palabra que describe algo que toma tiempo, no que ocurre de un día para otro.", "respuesta": "PROCESO"},
        {"texto": "Lo que hace un discípulo frente a su maestro: recibir enseñanza.", "respuesta": "APRENDER"},
        {"texto": "Cruz que, según Lucas 9,23, cada discípulo debe cargar cada día.", "respuesta": "CRUZ"},
        {"texto": "Palabra que describe algo que se repite día tras día, con constancia.", "respuesta": "DIARIO"},
        {"texto": "Lo que un caminante necesita para no perderse en el camino.", "respuesta": "RUMBO"},
    ],
    "incluir": ["CAMINO", "PROCESO"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con un discipulado que toma tiempo.",
               "CAMINO y PROCESO son las palabras centrales: empieza por esas."],
})

_agregar("C0N1-CO04", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: un camino de discipulado",
    "palabras": ["CAMINO", "CONVERSION", "CRECER", "PROCESO", "APRENDER", "CRUZ", "DIARIO", "RUMBO"],
    "incluir": ["CAMINO", "PROCESO"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: CRUZ y CAMINO.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N1-CO04", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Lucas 9,23",
    "items": [
        {
            "texto": "Busca en tu Biblia Lucas 9,23 y completa: «Si alguno quiere venir en pos de mí, niéguese a sí mismo, tome su cruz ______ y sígame.»",
            "respuesta": "CADADIA",
            "banco": ["CADADIA", "UNAVEZ", "ALGUNDIA"],
        },
        {
            "texto": "¿Qué significa para ti que el discipulado sea «cada día» y no una decisión que se toma una sola vez?",
            "abierta": True,
            "palabras_esperadas": ["DIARIO", "CADA DIA", "CONSTANCIA", "PROCESO", "SEGUIR", "TODOS LOS DIAS"],
            "respuestas_referencia": [
                "Significa que seguir a Jesús no se termina un día, sino que hay que elegirlo de nuevo cada día.",
                "Que la fe no es algo que se hace una vez y ya, sino un camino que se sostiene con constancia.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el evangelio de Lucas, capítulo 9, versículo 23.",
               "La expresión que falta indica que la cruz se toma con frecuencia, no una sola vez."],
})

_agregar("C0N1-CO04", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: etapas de un camino",
    "items": [
        {"texto": "El discípulo sigue aprendiendo y madurando en su fe con el paso del tiempo.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Una persona escucha por primera vez el llamado de Jesús.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Decide dar los primeros pasos y comienza a seguirlo.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Enfrenta dificultades, dudas y tropiezos en el camino.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué el paso 3 (dificultades) no significa que el discipulado haya fracasado?",
            "abierta": True,
            "palabras_esperadas": ["PROCESO", "CAMINO", "NORMAL", "CRECER", "DIFICULTAD", "MADURAR"],
            "respuestas_referencia": [
                "Porque el discipulado es un camino con tropiezos; las dificultades son parte normal de crecer en la fe.",
                "Porque un proceso incluye momentos difíciles, y superarlos también es parte de madurar como discípulo.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El discipulado empieza por escuchar, después se dan los primeros pasos, y luego vienen las dificultades.",
               "Madurar en la fe llega después de atravesar, no de evitar, las dificultades."],
})

_agregar("C0N1-CO04", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Ser discípulo de Jesús es un proceso que dura toda la vida.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Una vez que alguien decide seguir a Jesús, ya no necesita seguir aprendiendo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Tener dudas o tropiezos en el camino significa que la fe fracasó por completo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Lucas 9,23 habla de tomar la cruz «cada día», no una sola vez.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["APRENDER", "PROCESO", "CRECER", "NORMAL", "CAMINO", "MADURAR"],
            "respuestas_referencia": [
                "Es falsa porque el discipulado siempre implica seguir aprendiendo, no termina en un solo momento.",
                "Es falsa porque las dudas y tropiezos son parte normal del camino, no significan un fracaso total.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa si el discipulado es algo que se logra de una vez, o algo que se sostiene con el tiempo.",
               "Las dificultades en la fe no son un fracaso, son parte del camino."],
})

_agregar("C0N1-CO04", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: el camino no es una línea recta",
    "items": [
        {
            "texto": "Caso 1: Después de un tiempo entusiasmado con la catequesis, Julián empieza a sentir menos ganas de ir. ¿Qué actitud refleja mejor que el discipulado es un camino?",
            "respuesta": "Hablarlo con su catequista en vez de abandonar en silencio",
            "banco": ["Hablarlo con su catequista en vez de abandonar en silencio", "Dejar la catequesis de inmediato sin decir nada", "Fingir que todo está bien sin resolver lo que siente"],
        },
        {
            "texto": "Caso 2: Renata siente que, después de meses, no ha «avanzado» tanto como esperaba en su fe. ¿Qué le ayudaría a entender mejor el discipulado como proceso?",
            "respuesta": "Reconocer que crecer en la fe toma tiempo, y valorar los pasos pequeños",
            "banco": ["Reconocer que crecer en la fe toma tiempo, y valorar los pasos pequeños", "Pensar que si no avanzó rápido, ya no vale la pena seguir", "Compararse todo el tiempo con otros compañeros"],
        },
        {
            "texto": "Caso 3: Pedro tuvo una discusión fuerte con un amigo y se siente lejos de vivir lo que aprende en la catequesis. ¿Qué opción es más coherente con un camino de conversión?",
            "respuesta": "Reconocerlo, pedir perdón si hace falta y seguir intentándolo",
            "banco": ["Reconocerlo, pedir perdón si hace falta y seguir intentándolo", "Pensar que ya no puede considerarse discípulo de Jesús", "Evitar el tema y no volver a pensarlo"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja el discipulado como un camino, no como un examen que se aprueba o se reprueba.",
            "abierta": True,
            "palabras_esperadas": ["CAMINO", "PROCESO", "CRECER", "INTENTAR", "CONVERSION", "TIEMPO"],
            "respuestas_referencia": [
                "Elegí el caso de Pedro, porque un discípulo también se equivoca y lo importante es seguir intentándolo.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["En los tres casos, la mejor opción es la que no abandona ni se rinde ante la dificultad.",
               "El discipulado no se mide por no fallar nunca, sino por seguir intentándolo."],
})

_agregar("C0N1-CO04", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mi camino de fe",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Mi fe no es perfecta, y está bien». Incluye una idea central, una referencia a Lucas 9,23 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["CAMINO", "PROCESO", "CRECER", "CRUZ", "DIARIO", "APRENDER"],
            "respuestas_referencia": [
                "Idea central: el discipulado es un camino, no un examen perfecto. Aplicación: aceptar mis tropiezos y seguir intentándolo cada día.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un momento real en que tu fe tuvo un tropiezo y cómo seguiste adelante."],
})

_agregar("C0N1-CO04", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: un camino, paso a paso",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) que muestre el discipulado como un camino, no como un salto. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["CAMINO", "PASO", "PROCESO", "CRECER", "TIEMPO"],
            "respuestas_referencia": [
                "Escena 1: los primeros pasos, con entusiasmo. Escena 2: una dificultad en el camino. Escena 3: sigue caminando, un poco más maduro.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Muestra el paso del tiempo: no todo ocurre en una sola escena."],
})

_agregar("C0N1-CO04", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: un camino, no un salto",
    "items": [
        {
            "texto": "Completa: según Lucas 9,23, el discípulo debe tomar su cruz ______ y seguir a Jesús.",
            "respuesta": "CADADIA",
            "banco": ["CADADIA", "UNAVEZ", "NUNCA"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿En qué parte de tu camino de fe te sientes hoy: empezando, en una dificultad, o creciendo con más firmeza? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la expresión que usa Lucas para describir la frecuencia con que se toma la cruz."],
})

_agregar("C0N1-CO04", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: un paso hoy",
    "situacion": "El discipulado es un camino que se recorre paso a paso, no un examen que se aprueba de una vez.",
    "items": [
        {
            "texto": "¿Qué paso pequeño y concreto puedes dar esta semana en tu camino de fe?",
            "opciones": [
                "Perdonar algo pendiente con alguien cercano",
                "Sostener un hábito de oración aunque sea breve",
                "Reconocer un error y proponerme mejorar en algo concreto",
                "Esperar a sentirme «listo» para empezar cualquier cosa",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un paso pequeño, no en una meta enorme.",
               "Descarta la única opción que en realidad no da ningún paso."],
    "feedback_ok": "¡Muy bien! Los pasos pequeños y constantes son los que sostienen un camino de fe.",
})


# --- C0N1-CO05 — Mis dones al servicio de la misión -----------------------
_agregar("C0N1-CO05", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: dones para servir",
    "items": [
        {"texto": "Capacidad o talento que cada persona recibe de Dios para el bien de los demás.", "respuesta": "DON"},
        {"texto": "Lo que se hace cuando se pone un don al servicio de otra persona.", "respuesta": "SERVIR"},
        {"texto": "Palabra que describe la tarea de anunciar y vivir el Evangelio.", "respuesta": "MISION"},
        {"texto": "Cualidad o habilidad natural que alguien tiene, por ejemplo cantar o escuchar bien.", "respuesta": "TALENTO"},
        {"texto": "Comunidad de personas a la que cada joven puede aportar sus dones.", "respuesta": "IGLESIA"},
        {"texto": "Palabra bíblica para «regalo», usada por San Pedro al hablar de los dones.", "respuesta": "GRACIA"},
        {"texto": "Lo contrario de guardarse un don solo para uno mismo.", "respuesta": "COMPARTIR"},
        {"texto": "Persona que recibe el servicio o la ayuda de otra.", "respuesta": "PROJIMO"},
    ],
    "incluir": ["DON", "SERVIR"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con los talentos puestos al servicio de otros.",
               "DON y SERVIR son las palabras centrales: empieza por esas."],
})

_agregar("C0N1-CO05", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: dones para servir",
    "palabras": ["DON", "SERVIR", "MISION", "TALENTO", "IGLESIA", "GRACIA", "COMPARTIR", "PROJIMO"],
    "incluir": ["DON", "SERVIR"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: DON y GRACIA.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N1-CO05", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: 1 Pedro 4,10",
    "items": [
        {
            "texto": "Busca en tu Biblia 1 Pedro 4,10 y completa: «Cada uno ponga al servicio de los demás el ______ que ha recibido.»",
            "respuesta": "DON",
            "banco": ["DON", "DINERO", "TIEMPO"],
        },
        {
            "texto": "¿Cuál crees que es un don o talento tuyo que podrías poner al servicio de los demás?",
            "abierta": True,
            "palabras_esperadas": ["DON", "TALENTO", "SERVIR", "AYUDAR", "CAPACIDAD", "COMPARTIR"],
            "respuestas_referencia": [
                "Creo que se me da bien escuchar a los demás, y podría usar eso para acompañar a un compañero.",
                "Tengo facilidad para organizar cosas, y podría ayudar organizando actividades del grupo de catequesis.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca la primera carta de Pedro, capítulo 4, versículo 10.",
               "La palabra que falta es la misma que da título a esta actividad."],
})

_agregar("C0N1-CO05", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: de mi don a la misión",
    "items": [
        {"texto": "Esa capacidad se convierte en un servicio concreto para otra persona o para la comunidad.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Un joven descubre que tiene una capacidad o talento particular.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Reconoce que ese talento puede ser un don de Dios, no solo un mérito propio.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Piensa en una forma concreta de ponerlo al servicio de los demás.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué reconocer un talento como un don (paso 2) cambia la forma de usarlo?",
            "abierta": True,
            "palabras_esperadas": ["DON", "GRATITUD", "SERVIR", "COMPARTIR", "REGALO", "DIOS"],
            "respuestas_referencia": [
                "Porque si es un don de Dios, la actitud correcta es agradecerlo y compartirlo, no guardarlo solo para mí.",
                "Porque reconocerlo como un regalo invita a servir con humildad, no a usarlo solo para destacar.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de descubrir el talento, a reconocerlo como don, a pensar cómo servir con él.",
               "Un don que no se comparte pierde parte de su sentido, según 1 Pedro 4,10."],
})

_agregar("C0N1-CO05", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Según 1 Pedro 4,10, los dones se reciben para ponerlos al servicio de los demás.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Solo los adultos o los catequistas tienen dones útiles para la comunidad.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Un don que se guarda solo para uno mismo cumple igual su propósito.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Cualquier talento (organizar, escuchar, cantar, explicar) puede ponerse al servicio de la misión.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["JOVEN", "TODOS", "COMPARTIR", "SERVIR", "PROPOSITO"],
            "respuestas_referencia": [
                "Es falsa porque también los jóvenes tienen dones útiles para servir a su comunidad, no solo los adultos.",
                "Es falsa porque un don cumple su propósito cuando se comparte, no cuando se guarda solo para uno mismo.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["1 Pedro 4,10 habla de «cada uno», sin distinguir edades.",
               "Piensa qué sentido tiene un don que nunca se comparte con nadie."],
})

_agregar("C0N1-CO05", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: dones en acción",
    "items": [
        {
            "texto": "Caso 1: Martín es muy bueno explicando cosas complicadas de forma sencilla. ¿Cómo podría poner ese don al servicio de su grupo de catequesis?",
            "respuesta": "Ofrecerse a ayudar a un compañero que le cuesta entender un tema",
            "banco": ["Ofrecerse a ayudar a un compañero que le cuesta entender un tema", "Usarlo solo para quedar bien en los exámenes", "Guardárselo porque no cree que sea importante"],
        },
        {
            "texto": "Caso 2: Paola tiene facilidad para escuchar y hacer sentir bien a los demás. ¿Cuál sería una forma sencilla de poner ese don al servicio de la comunidad?",
            "respuesta": "Acompañar a un compañero que está pasando un momento difícil",
            "banco": ["Acompañar a un compañero que está pasando un momento difícil", "Usar ese don solo para hacer más amigos para sí misma", "Pensar que ese don no sirve para nada en la fe"],
        },
        {
            "texto": "Caso 3: Ricardo canta muy bien y le gusta la música. ¿Qué opción conecta mejor su talento con la misión de la Iglesia?",
            "respuesta": "Participar en el coro o en algún canto de la comunidad parroquial",
            "banco": ["Participar en el coro o en algún canto de la comunidad parroquial", "Cantar solo para sí mismo sin compartirlo nunca", "Pensar que cantar no tiene nada que ver con servir a Dios"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción es una verdadera forma de poner un don al servicio de los demás.",
            "abierta": True,
            "palabras_esperadas": ["DON", "SERVIR", "COMPARTIR", "COMUNIDAD", "TALENTO"],
            "respuestas_referencia": [
                "Elegí el caso de Martín, porque ayudar a un compañero pone su talento realmente al servicio de otros.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre pone el talento al servicio de otra persona o de la comunidad.",
               "Guardar un don solo para uno mismo no cumple el sentido que le da 1 Pedro 4,10."],
})

_agregar("C0N1-CO05", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mi don al servicio de otros",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «El don que tengo para compartir». Incluye una idea central, una referencia a 1 Pedro 4,10 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["DON", "SERVIR", "COMPARTIR", "TALENTO", "MISION"],
            "respuestas_referencia": [
                "Idea central: cada quien recibió un don para servir a los demás. Aplicación: usar mi propio talento para ayudar a alguien esta semana.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Empieza nombrando con claridad cuál es tu don, antes de explicar cómo compartirlo."],
})

_agregar("C0N1-CO05", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: talentos que sirven",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) que muestre a un joven descubriendo un don propio y poniéndolo al servicio de otros. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["DON", "TALENTO", "SERVIR", "AYUDAR", "COMPARTIR"],
            "respuestas_referencia": [
                "Escena 1: alguien descubre que tiene un talento. Escena 2: duda si compartirlo. Escena 3: lo pone al servicio de alguien más y ambos se benefician.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un talento juvenil común: organizar, escuchar, explicar, animar, crear."],
})

_agregar("C0N1-CO05", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: dones para servir",
    "items": [
        {
            "texto": "Completa: según 1 Pedro 4,10, cada uno debe poner su ______ al servicio de los demás.",
            "respuesta": "DON",
            "banco": ["DON", "DINERO", "TIEMPO LIBRE"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué don tuyo todavía no has puesto al servicio de los demás? ¿Qué te frena para hacerlo? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la palabra que usa 1 Pedro 4,10 para referirse a los talentos recibidos."],
})

_agregar("C0N1-CO05", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: mi don esta semana",
    "situacion": "Cada joven tiene al menos un don o talento que puede poner al servicio de su familia, su grupo o su parroquia.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para poner un don propio al servicio de otra persona?",
            "opciones": [
                "Ayudar a un compañero con algo en lo que soy bueno",
                "Ofrecerme para colaborar en una actividad de mi parroquia o grupo",
                "Usar un talento mío para animar o acompañar a alguien",
                "Guardar mis talentos solo para mí, sin compartirlos",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un talento real tuyo y una forma concreta de compartirlo.",
               "Descarta la única opción que no comparte nada con nadie."],
    "feedback_ok": "¡Muy bien! Poner un don al servicio de otros, aunque sea en algo pequeño, ya es vivir la misión.",
})


# --- C0N1-CO06 — Seguir a Jesús con otros ---------------------------------
_agregar("C0N1-CO06", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: seguir a Jesús en comunidad",
    "items": [
        {"texto": "Grupo de personas que comparten la fe y caminan juntas.", "respuesta": "COMUNIDAD"},
        {"texto": "Número de discípulos que Jesús eligió como grupo cercano.", "respuesta": "DOCE"},
        {"texto": "Palabra que describe la relación entre hermanos en la fe.", "respuesta": "FRATERNIDAD"},
        {"texto": "Lo contrario de vivir la fe solo, aislado de los demás.", "respuesta": "JUNTOS"},
        {"texto": "Grupo pequeño donde un joven vive de cerca su proceso de Confirmación.", "respuesta": "CATEQUESIS"},
        {"texto": "Lo que se construye cuando un grupo se ayuda y se sostiene mutuamente.", "respuesta": "APOYO"},
        {"texto": "Cualidad de estar presente y disponible para los demás del grupo.", "respuesta": "PRESENCIA"},
        {"texto": "Palabra que describe pertenecer de verdad a un grupo o comunidad.", "respuesta": "PERTENECER"},
    ],
    "incluir": ["COMUNIDAD", "JUNTOS"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con vivir la fe en comunidad, no en soledad.",
               "COMUNIDAD y JUNTOS son las palabras centrales: empieza por esas."],
})

_agregar("C0N1-CO06", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: seguir a Jesús en comunidad",
    "palabras": ["COMUNIDAD", "DOCE", "FRATERNIDAD", "JUNTOS", "CATEQUESIS", "APOYO", "PRESENCIA", "PERTENECER"],
    "incluir": ["COMUNIDAD", "JUNTOS"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: DOCE y APOYO.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N1-CO06", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Marcos 3,13-19",
    "items": [
        {
            "texto": "Busca en tu Biblia Marcos 3,13-14 y completa: «Y estableció a ______, para que estuviesen con él, y para enviarlos a predicar.»",
            "respuesta": "DOCE",
            "banco": ["DOCE", "TRES", "CIEN"],
        },
        {
            "texto": "¿Por qué crees que Jesús eligió llamar a un grupo, y no solo a discípulos por separado, cada uno por su cuenta?",
            "abierta": True,
            "palabras_esperadas": ["COMUNIDAD", "GRUPO", "JUNTOS", "APOYO", "FRATERNIDAD", "ACOMPAÑARSE"],
            "respuestas_referencia": [
                "Porque la fe se vive mejor en comunidad, apoyándose unos a otros en el camino.",
                "Porque un grupo puede sostenerse y ayudarse en los momentos difíciles, y eso fortalece la misión.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el evangelio de Marcos, capítulo 3, versículos 13 a 19.",
               "La palabra que falta es un número: cuántos discípulos eligió Jesús."],
})

_agregar("C0N1-CO06", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: de solo a comunidad",
    "items": [
        {"texto": "El grupo entero es enviado a anunciar y a vivir la misión juntos.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Jesús sube al monte y llama a los que él quiere.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Elige a doce para que estén con él, formando un grupo cercano.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Los Doce comparten tiempo, enseñanza y vida junto a Jesús.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué compartir tiempo juntos (paso 3) era necesario antes de ser enviados juntos (paso 4)?",
            "abierta": True,
            "palabras_esperadas": ["COMUNIDAD", "CONFIANZA", "PREPARAR", "JUNTOS", "APRENDER", "VINCULO"],
            "respuestas_referencia": [
                "Porque compartir tiempo juntos crea confianza y aprendizaje, algo necesario para poder ser enviados en misión.",
                "Porque un grupo que primero se conoce y se apoya puede sostenerse mejor cuando sale a anunciar juntos.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de ser llamados, a formar grupo, a compartir vida juntos, y solo después ser enviados.",
               "Un grupo unido puede sostener mejor la misión que cada uno por separado."],
})

_agregar("C0N1-CO06", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Jesús llamó a un grupo de Doce para que estuvieran con él y fueran enviados juntos.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Vivir la fe en comunidad no aporta nada que no se pueda vivir en soledad.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Un grupo de catequesis puede ser un lugar de apoyo real para un joven.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Aislarse de la comunidad de fe no tiene ninguna consecuencia para el discipulado.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["COMUNIDAD", "APOYO", "JUNTOS", "AISLAR", "FRATERNIDAD"],
            "respuestas_referencia": [
                "Es falsa porque vivir la fe en comunidad da apoyo, aprendizaje y fraternidad que en soledad se pierde.",
                "Es falsa porque aislarse de la comunidad puede debilitar la fe, ya que caminar juntos la sostiene.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa qué aporta un grupo que caminar solo no puede dar.",
               "Marcos 3,13-19 muestra a Jesús formando un grupo, no solo discípulos aislados."],
})

_agregar("C0N1-CO06", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: la fe se sostiene en comunidad",
    "items": [
        {
            "texto": "Caso 1: Emilia se siente desanimada con su fe y piensa en dejar de ir a la catequesis. ¿Qué actitud refleja mejor el valor de la comunidad?",
            "respuesta": "Contarle a su grupo o a su catequista cómo se siente antes de decidir",
            "banco": ["Contarle a su grupo o a su catequista cómo se siente antes de decidir", "Dejar de ir sin avisar ni hablarlo con nadie", "Guardarse todo para no molestar a los demás"],
        },
        {
            "texto": "Caso 2: Un compañero del grupo de Confirmación está pasando un momento familiar difícil. ¿Qué sería vivir la fraternidad de la que habla Marcos 3,13-19?",
            "respuesta": "Acompañarlo y hacerle saber que el grupo está con él",
            "banco": ["Acompañarlo y hacerle saber que el grupo está con él", "Ignorarlo porque no es un problema del grupo", "Hablar de su situación con otros a sus espaldas"],
        },
        {
            "texto": "Caso 3: Santiago prefiere vivir su fe completamente solo, sin participar de ningún grupo. ¿Qué le podrías compartir, con respeto, sobre la comunidad?",
            "respuesta": "Que la comunidad también puede sostener y enriquecer su fe personal",
            "banco": ["Que la comunidad también puede sostener y enriquecer su fe personal", "Que vivir en comunidad no tiene ningún valor real", "Que debe obligarse a participar aunque no quiera"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja el valor de vivir la fe en comunidad.",
            "abierta": True,
            "palabras_esperadas": ["COMUNIDAD", "APOYO", "ACOMPAÑAR", "JUNTOS", "FRATERNIDAD"],
            "respuestas_referencia": [
                "Elegí el caso de Emilia, porque compartir cómo se siente con su grupo puede sostenerla mejor que decidir sola.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre valora el acompañamiento del grupo, sin imponerlo por la fuerza.",
               "La comunidad no reemplaza la fe personal, pero sí puede sostenerla."],
})

_agregar("C0N1-CO06", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: no caminamos solos",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Por qué no sigo a Jesús solo». Incluye una idea central, una referencia a Marcos 3,13-19 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["COMUNIDAD", "JUNTOS", "GRUPO", "APOYO", "FRATERNIDAD"],
            "respuestas_referencia": [
                "Idea central: Jesús mismo formó un grupo para caminar junto a él. Aplicación: valorar más mi grupo de catequesis como parte de mi fe.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una experiencia real de apoyo que hayas vivido en un grupo."],
})

_agregar("C0N1-CO06", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: caminar juntos",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) que muestre a un grupo de jóvenes sosteniéndose mutuamente en su camino de fe. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["GRUPO", "COMUNIDAD", "APOYO", "JUNTOS", "ACOMPAÑAR"],
            "respuestas_referencia": [
                "Escena 1: alguien pasa un momento difícil solo. Escena 2: su grupo se entera y lo acompaña. Escena 3: siguen caminando juntos, más fuertes.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una situación real de un grupo de catequesis o de amigos que se apoyan."],
})

_agregar("C0N1-CO06", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: seguir a Jesús con otros",
    "items": [
        {
            "texto": "Completa: según Marcos 3,13-19, Jesús eligió a ______ discípulos para que estuvieran con él.",
            "respuesta": "DOCE",
            "banco": ["DOCE", "SIETE", "CIEN"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Quién te acompaña hoy en tu camino de fe? ¿A quién podrías acompañar tú? Coméntalo con tu catequista.",
    "pistas": ["Piensa en el número de discípulos que Jesús eligió como su grupo cercano."],
})

_agregar("C0N1-CO06", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: vivir en comunidad",
    "situacion": "Jesús formó un grupo para caminar junto a él; hoy, un grupo de catequesis, la parroquia o la familia pueden ser esa comunidad para un joven.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para vivir tu fe en comunidad, no en soledad?",
            "opciones": [
                "Participar activamente en mi grupo de catequesis",
                "Acompañar a un compañero que lo esté necesitando",
                "Compartir en familia algo de lo que estoy aprendiendo en Confirmación",
                "Evitar cualquier actividad grupal relacionada con mi fe",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una forma concreta de acompañar o dejarte acompañar esta semana.",
               "Descarta la única opción que aísla en vez de acompañar."],
    "feedback_ok": "¡Felicidades! Terminaste C0N1 «Jesús nos llama a seguirlo». Caminar en comunidad fortalece cada paso de tu fe.",
})

# ==========================================================================
# C0N2 — Jóvenes en la Biblia   (1 Samuel 3,1-10 / Lucas 1,26-38)
# ==========================================================================

# --- C0N2-CO01 — Samuel aprende a escuchar --------------------------------
_agregar("C0N2-CO01", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: Samuel escucha en el templo",
    "items": [
        {"texto": "Nombre del joven que servía en el templo y escuchó la voz de Dios de noche.", "respuesta": "SAMUEL"},
        {"texto": "Sacerdote anciano bajo cuyo cuidado vivía Samuel en el templo.", "respuesta": "ELI"},
        {"texto": "Número de veces que Samuel corrió donde Elí antes de entender quién lo llamaba.", "respuesta": "TRES"},
        {"texto": "Lugar sagrado donde dormía Samuel y donde escuchó la voz.", "respuesta": "TEMPLO"},
        {"texto": "Lo que Samuel hizo cada vez que escuchó su nombre: fue a ver a Elí.", "respuesta": "CORRIO"},
        {"texto": "Acción de prestar atención con toda la mente y el corazón.", "respuesta": "ESCUCHAR"},
        {"texto": "Palabra que describe estar dispuesto y abierto a lo que Dios pide.", "respuesta": "DISPONIBLE"},
        {"texto": "Sonido que Samuel escuchó en la noche y que al principio no reconoció.", "respuesta": "VOZ"},
    ],
    "incluir": ["SAMUEL", "ESCUCHAR"],
    "requisito": 6,
    "pistas": ["Todas las palabras aparecen en el relato de 1 Samuel 3,1-10.",
               "SAMUEL y ESCUCHAR son las palabras centrales: empieza por esas."],
})

_agregar("C0N2-CO01", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: Samuel escucha en el templo",
    "palabras": ["SAMUEL", "ELI", "TRES", "TEMPLO", "CORRIO", "ESCUCHAR", "DISPONIBLE", "VOZ"],
    "incluir": ["SAMUEL", "ESCUCHAR"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: ELI, VOZ y TRES.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N2-CO01", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: 1 Samuel 3,1-10",
    "items": [
        {
            "texto": "Busca en tu Biblia 1 Samuel 3,8-9 y completa: Elí entendió que era el ______ quien llamaba al joven.",
            "respuesta": "SEÑOR",
            "banco": ["SEÑOR", "VIENTO", "SACERDOTE"],
        },
        {
            "texto": "¿Por qué crees que Samuel necesitó la ayuda de Elí para reconocer que era Dios quien lo llamaba?",
            "abierta": True,
            "palabras_esperadas": ["JOVEN", "INEXPERIENCIA", "ACOMPAÑAR", "ELI", "AYUDA", "RECONOCER", "GUIAR"],
            "respuestas_referencia": [
                "Porque Samuel era joven y no tenía experiencia todavía para reconocer la voz de Dios por sí solo.",
                "Porque a veces necesitamos que alguien con más experiencia nos ayude a reconocer lo que Dios nos pide.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el primer libro de Samuel, capítulo 3, versículos 1 al 10.",
               "Elí fue quien ayudó a Samuel a entender de dónde venía la voz."],
})

_agregar("C0N2-CO01", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: la noche de Samuel",
    "items": [
        {"texto": "Samuel responde: «Habla, Señor, que tu siervo escucha».", "respuesta": "5", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Samuel duerme en el templo, cerca del arca de Dios.", "respuesta": "1", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Escucha una voz que lo llama por su nombre y corre donde Elí.", "respuesta": "2", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Después de la tercera vez, Elí entiende que es el Señor quien llama.", "respuesta": "3", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Elí le enseña a Samuel qué responder si la voz vuelve a llamarlo.", "respuesta": "4", "banco": ["1", "2", "3", "4", "5"]},
        {
            "texto": "Justifica: ¿por qué fue necesario que alguien (Elí) le enseñara a Samuel qué responder (paso 4), antes de que él respondiera bien (paso 5)?",
            "abierta": True,
            "palabras_esperadas": ["ENSEÑAR", "GUIAR", "ACOMPAÑAR", "APRENDER", "AYUDA"],
            "respuestas_referencia": [
                "Porque Samuel todavía no sabía cómo responder a Dios, y necesitó que alguien con experiencia se lo enseñara.",
                "Porque el discernimiento muchas veces se aprende con ayuda de otra persona que ya lo ha vivido.",
            ],
        },
    ],
    "requisito": 5,
    "pistas": ["Relee 1 Samuel 3,1-10 en orden: primero duerme, después escucha, después corre donde Elí.",
               "Elí enseña a Samuel la respuesta correcta antes de que la voz vuelva a llamarlo por cuarta vez."],
})

_agregar("C0N2-CO01", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Samuel reconoció de inmediato que era Dios quien lo llamaba.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Elí ayudó a Samuel a entender quién lo estaba llamando.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Samuel corrió donde Elí varias veces antes de entender lo que pasaba.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "El relato de Samuel enseña que Dios solo llama a personas adultas y con experiencia.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["JOVEN", "CONFUNDIDO", "TRES VECES", "SAMUEL", "NIÑO"],
            "respuestas_referencia": [
                "Es falsa porque Samuel al principio no reconoció la voz de Dios; pensó que era Elí quien lo llamaba.",
                "Es falsa porque Samuel era joven, todavía un niño al servicio del templo, y Dios lo llamó de todos modos.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa cuántas veces tuvo que correr Samuel antes de entender lo que pasaba.",
               "Samuel era joven cuando Dios lo llamó por primera vez."],
})

_agregar("C0N2-CO01", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: aprender a escuchar",
    "items": [
        {
            "texto": "Caso 1: Nicolás siente una inquietud interior sobre su vida de fe, pero no sabe bien qué hacer con eso. ¿Qué actitud se parece más a la de Samuel?",
            "respuesta": "Hablarlo con su catequista para entender mejor lo que siente",
            "banco": ["Hablarlo con su catequista para entender mejor lo que siente", "Ignorar la inquietud porque le parece rara", "Decidir algo importante sin pensarlo ni hablarlo con nadie"],
        },
        {
            "texto": "Caso 2: Valeria tiene la costumbre de hablar todo el tiempo y le cuesta quedarse en silencio. ¿Qué le ayudaría a aprender a escuchar como Samuel?",
            "respuesta": "Buscar momentos breves de silencio y quietud en su día",
            "banco": ["Buscar momentos breves de silencio y quietud en su día", "Pensar que el silencio no tiene ningún valor", "Evitar cualquier momento de quietud"],
        },
        {
            "texto": "Caso 3: Iván no está seguro de qué le está pidiendo Dios en esta etapa de su vida. ¿Qué actitud del relato de Samuel podría ayudarlo?",
            "respuesta": "Estar disponible y abierto, aunque todavía no tenga una respuesta clara",
            "banco": ["Estar disponible y abierto, aunque todavía no tenga una respuesta clara", "Dejar de pensarlo hasta que la respuesta aparezca sola", "Inventar una respuesta solo para no sentir incertidumbre"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja la actitud de escucha de Samuel.",
            "abierta": True,
            "palabras_esperadas": ["ESCUCHAR", "DISPONIBLE", "SILENCIO", "ABIERTO", "SAMUEL"],
            "respuestas_referencia": [
                "Elegí el caso de Iván, porque estar disponible sin tener todas las respuestas es justo lo que vivió Samuel.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La actitud de Samuel fue estar disponible y abierto, aunque al principio no entendiera todo.",
               "Escuchar de verdad muchas veces empieza por hacer silencio."],
})

_agregar("C0N2-CO01", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: aprender a escuchar como Samuel",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Lo que Samuel me enseña sobre escuchar». Incluye una idea central, una referencia a 1 Samuel 3,1-10 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["SAMUEL", "ESCUCHAR", "DISPONIBLE", "SILENCIO", "DIOS"],
            "respuestas_referencia": [
                "Idea central: escuchar a Dios pide disponibilidad, como la de Samuel. Aplicación: buscar un momento de silencio esta semana.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un momento real donde te haya costado escuchar con atención."],
})

_agregar("C0N2-CO01", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: aprender a escuchar",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) sobre un joven que aprende a hacer silencio para escuchar mejor lo que Dios le pide, inspirado en Samuel. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["SILENCIO", "ESCUCHAR", "SAMUEL", "DISPONIBLE", "QUIETUD"],
            "respuestas_referencia": [
                "Escena 1: un joven rodeado de ruido y notificaciones. Escena 2: se detiene y busca un momento de silencio. Escena 3: logra escuchar mejor lo que siente.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en el ruido cotidiano (celular, redes) que dificulta escuchar en silencio."],
})

_agregar("C0N2-CO01", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: Samuel aprende a escuchar",
    "items": [
        {
            "texto": "Completa: fue ______ quien ayudó a Samuel a entender que era Dios quien lo llamaba.",
            "respuesta": "ELI",
            "banco": ["ELI", "MOISES", "DAVID"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Hay alguien en tu vida (catequista, familiar, amigo) que te haya ayudado a entender mejor lo que Dios te pide, como Elí ayudó a Samuel? Coméntalo con tu catequista.",
    "pistas": ["Piensa en el sacerdote anciano que cuidaba a Samuel en el templo."],
})

_agregar("C0N2-CO01", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: hacer silencio para escuchar",
    "situacion": "Samuel necesitó estar en silencio y disponible para reconocer la voz de Dios. Un joven de hoy también puede buscar esos momentos.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para crear un momento de silencio y escucha, como Samuel?",
            "opciones": [
                "Apagar el celular unos minutos antes de dormir para hacer silencio",
                "Buscar un momento del día para orar sin distracciones",
                "Prestar atención con calma a lo que siento antes de reaccionar",
                "Llenar cada minuto del día con ruido o pantallas",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un momento concreto y realista para hacer silencio.",
               "Descarta la única opción que no deja espacio para escuchar."],
    "feedback_ok": "¡Muy bien! El silencio, aunque sea breve, ayuda a escuchar mejor, como le pasó a Samuel.",
})


# --- C0N2-CO02 — Habla, Señor: escuchar antes de responder ----------------
_agregar("C0N2-CO02", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: habla, Señor",
    "items": [
        {"texto": "Frase con la que Samuel responde a Dios: «Habla, Señor, que tu siervo...»", "respuesta": "ESCUCHA"},
        {"texto": "Proceso de reconocer con calma lo que Dios pide en una decisión.", "respuesta": "DISCERNIMIENTO"},
        {"texto": "Ausencia de ruido que ayuda a escuchar mejor.", "respuesta": "SILENCIO"},
        {"texto": "Cualidad de estar receptivo a algo nuevo, sin cerrarse de antemano.", "respuesta": "APERTURA"},
        {"texto": "Palabra que describe a quien está listo para servir y obedecer.", "respuesta": "SIERVO"},
        {"texto": "Lo contrario de responder de forma impulsiva y apresurada.", "respuesta": "CALMA"},
        {"texto": "Acción de detenerse a pensar antes de actuar o responder.", "respuesta": "REFLEXIONAR"},
        {"texto": "Palabra que describe el tiempo dedicado a hablar con Dios.", "respuesta": "ORACION"},
    ],
    "incluir": ["ESCUCHA", "DISCERNIMIENTO"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con escuchar antes de responder.",
               "ESCUCHA y DISCERNIMIENTO son las palabras centrales: empieza por esas."],
})

_agregar("C0N2-CO02", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: habla, Señor",
    "palabras": ["ESCUCHA", "DISCERNIMIENTO", "SILENCIO", "APERTURA", "SIERVO", "CALMA", "REFLEXIONAR", "ORACION"],
    "incluir": ["ESCUCHA", "DISCERNIMIENTO"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: CALMA y SIERVO.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N2-CO02", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: 1 Samuel 3,9-10",
    "items": [
        {
            "texto": "Busca en tu Biblia 1 Samuel 3,9-10 y completa lo que Samuel responde: «Habla, ______, que tu siervo escucha.»",
            "respuesta": "SEÑOR",
            "banco": ["SEÑOR", "ELI", "PADRE"],
        },
        {
            "texto": "¿Por qué crees que Samuel dijo primero «habla» y solo después «escucha», y no al revés?",
            "abierta": True,
            "palabras_esperadas": ["ESCUCHAR", "DISPONIBLE", "ABIERTO", "ORDEN", "PRIMERO"],
            "respuestas_referencia": [
                "Porque antes de responder cualquier cosa, primero hay que ponerse en actitud de escuchar con atención.",
                "Porque Samuel se puso disponible antes de saber qué le iban a decir, mostrando confianza y apertura.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el primer libro de Samuel, capítulo 3, versículos 9 y 10.",
               "La palabra que falta es la misma que usa Samuel para dirigirse a Dios."],
})

_agregar("C0N2-CO02", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: el camino del discernimiento",
    "items": [
        {"texto": "Se toma una decisión con más claridad y paz interior.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se busca un momento de silencio para poder escuchar.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se presta atención con calma a lo que se siente o se percibe.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se reflexiona sobre lo escuchado antes de actuar.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué el silencio (paso 1) es el primer paso de este proceso, y no el último?",
            "abierta": True,
            "palabras_esperadas": ["SILENCIO", "PRIMERO", "ESCUCHAR", "BASE", "CONDICION"],
            "respuestas_referencia": [
                "Porque sin silencio es difícil escuchar con atención lo que viene después; es la base del proceso.",
                "Porque el silencio crea las condiciones necesarias para poder discernir con calma.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El discernimiento empieza por hacer silencio, y termina en una decisión con más claridad.",
               "Sin el primer paso (silencio), los siguientes son más difíciles de dar."],
})

_agregar("C0N2-CO02", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Samuel respondió a Dios estando dispuesto a escuchar antes de saber qué le iban a decir.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "El discernimiento no necesita silencio ni calma para ser verdadero.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Responder de forma impulsiva, sin pensar, es la mejor forma de discernir.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Escuchar antes de responder ayuda a tomar decisiones con más claridad.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["SILENCIO", "CALMA", "PENSAR", "REFLEXIONAR", "DISCERNIR"],
            "respuestas_referencia": [
                "Es falsa porque el discernimiento necesita silencio y calma para poder escuchar con atención.",
                "Es falsa porque responder sin pensar no es discernir, sino actuar por impulso.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en la actitud de Samuel: calma, silencio y disposición a escuchar.",
               "Discernir es lo contrario de decidir de forma impulsiva."],
})

_agregar("C0N2-CO02", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: escuchar antes de responder",
    "items": [
        {
            "texto": "Caso 1: Daniel tiene que tomar una decisión importante sobre sus estudios y se siente presionado a responder rápido. ¿Qué le ayudaría a discernir mejor?",
            "respuesta": "Buscar un momento de calma y silencio antes de decidir",
            "banco": ["Buscar un momento de calma y silencio antes de decidir", "Responder lo primero que se le ocurra para salir del paso", "Decidir solo por lo que otros esperan de él"],
        },
        {
            "texto": "Caso 2: Camila recibió un mensaje que la hizo enojar y quiere responder de inmediato. ¿Qué actitud del relato de Samuel podría ayudarla?",
            "respuesta": "Tomarse un momento de calma antes de responder",
            "banco": ["Tomarse un momento de calma antes de responder", "Responder enojada sin pensarlo", "Ignorar completamente lo que siente"],
        },
        {
            "texto": "Caso 3: Esteban siente que Dios lo invita a algo, pero todavía no sabe bien qué es. ¿Qué actitud es más fiel a «habla, Señor, que tu siervo escucha»?",
            "respuesta": "Mantenerse abierto y disponible, aunque la respuesta tarde en llegar",
            "banco": ["Mantenerse abierto y disponible, aunque la respuesta tarde en llegar", "Exigir una respuesta inmediata y clara", "Dejar de prestarle atención a esa inquietud"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja la actitud de escuchar antes de responder.",
            "abierta": True,
            "palabras_esperadas": ["ESCUCHAR", "CALMA", "SILENCIO", "DISCERNIR", "ABIERTO"],
            "respuestas_referencia": [
                "Elegí el caso de Camila, porque tomarse un momento de calma antes de responder evita una reacción impulsiva.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre busca calma y escucha antes de actuar.",
               "Responder rápido no siempre es responder bien."],
})

_agregar("C0N2-CO02", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: escuchar antes de responder",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Por qué me cuesta escuchar antes de responder». Incluye una idea central, una referencia a 1 Samuel 3,9-10 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["ESCUCHAR", "CALMA", "SILENCIO", "DISCERNIR", "RESPONDER"],
            "respuestas_referencia": [
                "Idea central: como Samuel, primero hay que ponerse en actitud de escucha. Aplicación: practicar la calma antes de responder algo importante.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una situación real donde respondiste demasiado rápido y te hubiera convenido pensarlo más."],
})

_agregar("C0N2-CO02", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: pensar antes de responder",
    "items": [
        {
            "texto": "Escribe el guion de un Reel de 45 segundos: «Antes de responder, escucho», mostrando a alguien que se detiene a pensar antes de reaccionar. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["ESCUCHAR", "CALMA", "PENSAR", "REACCIONAR", "SILENCIO"],
            "respuestas_referencia": [
                "Escena 1: alguien a punto de reaccionar impulsivamente. Escena 2: se detiene y respira. Escena 3: responde con más calma y claridad.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una situación cotidiana donde detenerse antes de responder haría la diferencia."],
})

_agregar("C0N2-CO02", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: habla, Señor",
    "items": [
        {
            "texto": "Completa la frase de Samuel: «Habla, Señor, que tu ______ escucha.»",
            "respuesta": "SIERVO",
            "banco": ["SIERVO", "AMIGO", "PUEBLO"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿En qué momento de tu semana podrías practicar el silencio antes de responder algo importante? Coméntalo con tu catequista.",
    "pistas": ["Recuerda la frase exacta que Samuel le dice a Dios en 1 Samuel 3,10."],
})

_agregar("C0N2-CO02", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: practicar la escucha",
    "situacion": "Samuel respondió a Dios con disponibilidad, después de hacer silencio. Escuchar antes de responder también se puede practicar en la vida diaria.",
    "items": [
        {
            "texto": "¿Qué puedes practicar tú esta semana para escuchar mejor antes de responder?",
            "opciones": [
                "Respirar y pensar antes de responder un mensaje que me molesta",
                "Escuchar completo a alguien antes de opinar",
                "Hacer una pausa de oración antes de una decisión importante",
                "Responder siempre lo primero que se me ocurra",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una situación real de tu semana donde puedas practicar esto.",
               "Descarta la única opción que no implica ninguna pausa."],
    "feedback_ok": "¡Muy bien! Escuchar antes de responder es un hábito que se entrena, como lo vivió Samuel.",
})


# --- C0N2-CO03 — María: una joven que responde con fe ---------------------
_agregar("C0N2-CO03", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: el sí de María",
    "items": [
        {"texto": "Nombre de la joven a quien el ángel Gabriel anuncia que será madre del Salvador.", "respuesta": "MARIA"},
        {"texto": "Ángel que lleva el mensaje de Dios a María en Nazaret.", "respuesta": "GABRIEL"},
        {"texto": "Título con el que el ángel saluda a María: «llena de...»", "respuesta": "GRACIA"},
        {"texto": "Palabra final del sí de María: «hágase en mí según tu...»", "respuesta": "PALABRA"},
        {"texto": "Nombre del niño que María concebirá, según el anuncio del ángel.", "respuesta": "JESUS"},
        {"texto": "Título que María se da a sí misma al responder: «la esclava del...»", "respuesta": "SEÑOR"},
        {"texto": "Ciudad donde vivía María cuando recibió el anuncio del ángel.", "respuesta": "NAZARET"},
        {"texto": "Palabra que describe la respuesta de María: libre, sin ser obligada.", "respuesta": "LIBRE"},
    ],
    "incluir": ["MARIA", "PALABRA"],
    "requisito": 6,
    "pistas": ["Todas las palabras aparecen en el relato de la Anunciación, Lucas 1,26-38.",
               "MARIA y PALABRA son las palabras centrales: empieza por esas."],
})

_agregar("C0N2-CO03", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: el sí de María",
    "palabras": ["MARIA", "GABRIEL", "GRACIA", "PALABRA", "JESUS", "SEÑOR", "NAZARET", "LIBRE"],
    "incluir": ["MARIA", "PALABRA"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: MARIA y LIBRE.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N2-CO03", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Lucas 1,26-38",
    "items": [
        {
            "texto": "Busca en tu Biblia Lucas 1,38 y completa la respuesta de María: «He aquí la esclava del Señor; hágase en mí según tu ______.»",
            "respuesta": "PALABRA",
            "banco": ["PALABRA", "DESEO", "VOLUNTAD"],
        },
        {
            "texto": "¿Qué crees que hizo posible que María respondiera «sí» a algo tan grande e inesperado?",
            "abierta": True,
            "palabras_esperadas": ["CONFIANZA", "FE", "DIOS", "LIBRE", "VALENTIA", "DISPONIBLE"],
            "respuestas_referencia": [
                "Creo que su gran confianza en Dios le permitió decir sí, aunque no entendiera todo por completo.",
                "Su fe y su disponibilidad la ayudaron a responder con libertad, a pesar de lo inesperado del anuncio.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el evangelio de Lucas, capítulo 1, versículos 26 al 38.",
               "La palabra que falta es la misma que da título a esta actividad."],
})

_agregar("C0N2-CO03", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: la Anunciación",
    "items": [
        {"texto": "María responde: «Hágase en mí según tu palabra».", "respuesta": "5", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "El ángel Gabriel se presenta ante María y la saluda.", "respuesta": "1", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "María se turba y se pregunta qué significa ese saludo.", "respuesta": "2", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "El ángel le anuncia que será madre del Hijo de Dios.", "respuesta": "3", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "María pregunta cómo será posible eso, y el ángel le explica.", "respuesta": "4", "banco": ["1", "2", "3", "4", "5"]},
        {
            "texto": "Justifica: ¿por qué la pregunta de María (paso 4) no fue una falta de fe, sino parte de su proceso de discernimiento?",
            "abierta": True,
            "palabras_esperadas": ["PREGUNTAR", "DUDA", "DISCERNIR", "NORMAL", "ENTENDER"],
            "respuestas_referencia": [
                "Porque preguntar para entender mejor no es lo mismo que dudar de Dios; es parte de discernir con honestidad.",
                "Porque María quiso comprender antes de responder, y eso no le quitó valor a su sí final.",
            ],
        },
    ],
    "requisito": 5,
    "pistas": ["Relee Lucas 1,26-38 en orden: saludo, turbación, anuncio, pregunta, y finalmente la respuesta.",
               "Preguntar «¿cómo será esto?» no es lo mismo que negarse."],
})

_agregar("C0N2-CO03", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "María respondió al ángel con una fe libre y confiada.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "María no tuvo ninguna reacción de sorpresa ante el anuncio del ángel.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Preguntar «¿cómo será esto?» significa que María dudaba de Dios.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "María se llamó a sí misma «la esclava del Señor» al responder al ángel.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["TURBADA", "SORPRESA", "PREGUNTAR", "ENTENDER", "DUDA"],
            "respuestas_referencia": [
                "Es falsa porque el texto dice que María se turbó al escuchar el saludo del ángel.",
                "Es falsa porque preguntar cómo sería posible no fue duda, sino un intento honesto de comprender.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en cómo reaccionó María al principio del anuncio.",
               "Preguntar para entender es distinto de negarse a creer."],
})

_agregar("C0N2-CO03", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: responder con fe como María",
    "items": [
        {
            "texto": "Caso 1: Ana recibe una propuesta para ayudar en un servicio de la parroquia, pero le da miedo no ser capaz. ¿Qué actitud se parece más a la de María?",
            "respuesta": "Preguntar y entender mejor, y responder con confianza aunque tenga dudas",
            "banco": ["Preguntar y entender mejor, y responder con confianza aunque tenga dudas", "Decir que no de inmediato por miedo", "Aceptar sin pensar ni preguntar nada"],
        },
        {
            "texto": "Caso 2: Gabriel siente que Dios lo invita a algo grande, pero no entiende del todo qué significa. ¿Qué haría alguien que responde con fe, como María?",
            "respuesta": "Hacer preguntas honestas sin dejar de confiar",
            "banco": ["Hacer preguntas honestas sin dejar de confiar", "Ignorar lo que siente porque no lo entiende", "Fingir que ya lo entiende todo"],
        },
        {
            "texto": "Caso 3: Lucía duda si podrá cumplir un compromiso importante que asumió en su parroquia. ¿Qué actitud refleja mejor la fe confiada de María?",
            "respuesta": "Reconocer sus dudas y pedir ayuda para sostener el compromiso",
            "banco": ["Reconocer sus dudas y pedir ayuda para sostener el compromiso", "Abandonar el compromiso sin decir nada", "Fingir que no tiene ninguna duda"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja la fe confiada de María.",
            "abierta": True,
            "palabras_esperadas": ["FE", "CONFIANZA", "MARIA", "PREGUNTAR", "DUDA"],
            "respuestas_referencia": [
                "Elegí el caso de Ana, porque preguntar y aun así confiar es lo que hizo María ante el anuncio del ángel.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre combina honestidad (preguntar, reconocer dudas) con confianza.",
               "María no escondió su sorpresa, pero tampoco dejó que le impidiera responder con fe."],
})

_agregar("C0N2-CO03", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: el sí de María y el mío",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Lo que el sí de María me enseña». Incluye una idea central, una referencia a Lucas 1,26-38 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["MARIA", "FE", "CONFIANZA", "LIBRE", "RESPONDER"],
            "respuestas_referencia": [
                "Idea central: María respondió con fe libre a algo inesperado. Aplicación: animarme a responder con confianza a algo que Dios me pide.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una decisión propia donde tuviste que confiar aunque no entendieras todo."],
})

_agregar("C0N2-CO03", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: un sí que cambia todo",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) inspirado en el sí de María: alguien recibe una noticia inesperada, se sorprende, y responde con confianza. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["SORPRESA", "CONFIANZA", "RESPONDER", "FE", "MARIA"],
            "respuestas_referencia": [
                "Escena 1: alguien recibe una noticia que lo sorprende. Escena 2: se toma un momento para entenderla. Escena 3: responde con un sí confiado.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una noticia inesperada (buena, pero grande) y cómo alguien podría responder con fe."],
})

_agregar("C0N2-CO03", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: el sí de María",
    "items": [
        {
            "texto": "Completa: el ángel que anunció a María que sería madre de Jesús se llamaba ______.",
            "respuesta": "GABRIEL",
            "banco": ["GABRIEL", "MIGUEL", "RAFAEL"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué «sí» te está pidiendo Dios hoy a ti, aunque todavía no lo entiendas del todo? Coméntalo con tu catequista.",
    "pistas": ["Piensa en el nombre del ángel que aparece en Lucas 1,26."],
})

_agregar("C0N2-CO03", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: responder con fe",
    "situacion": "María respondió con fe libre y confiada a algo que no comprendía del todo. Un joven también puede responder así ante lo que Dios le pide.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para responder con más confianza a algo que sientes que Dios te pide?",
            "opciones": [
                "Animarme a dar un paso, aunque tenga dudas",
                "Hablarlo con mi catequista para entenderlo mejor",
                "Confiar en Dios aunque no tenga todas las respuestas",
                "Evitar cualquier decisión que me genere incertidumbre",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un paso concreto, no en una respuesta perfecta.",
               "Descarta la única opción que evita cualquier decisión."],
    "feedback_ok": "¡Muy bien! Responder con fe, aunque haya dudas, es parte del camino, como lo vivió María.",
})

# --- C0N2-CO04 — El miedo y la confianza -----------------------------------
_agregar("C0N2-CO04", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: no temas",
    "items": [
        {"texto": "Palabra que dice el ángel a María para calmar su turbación: «No...»", "respuesta": "TEMAS"},
        {"texto": "Sentimiento natural ante algo desconocido o inesperado.", "respuesta": "MIEDO"},
        {"texto": "Lo contrario de la duda: creer firmemente que Dios acompaña.", "respuesta": "CONFIANZA"},
        {"texto": "Palabra que describe algo que no se puede prever ni anticipar.", "respuesta": "INESPERADO"},
        {"texto": "Cualidad de quien actúa a pesar del miedo, no en ausencia de él.", "respuesta": "VALENTIA"},
        {"texto": "Lo que sintió María al escuchar el saludo del ángel: se...", "respuesta": "TURBO"},
        {"texto": "Palabra que describe la seguridad interior que da la fe.", "respuesta": "PAZ"},
        {"texto": "Lo que Dios promete a quien confía, según muchos pasajes bíblicos: su...", "respuesta": "PRESENCIA"},
    ],
    "incluir": ["MIEDO", "CONFIANZA"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con el miedo y la confianza en la fe.",
               "MIEDO y CONFIANZA son las palabras centrales: empieza por esas."],
})

_agregar("C0N2-CO04", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: no temas",
    "palabras": ["TEMAS", "MIEDO", "CONFIANZA", "INESPERADO", "VALENTIA", "TURBO", "PAZ", "PRESENCIA"],
    "incluir": ["MIEDO", "CONFIANZA"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: PAZ y TEMAS.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N2-CO04", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Lucas 1,29-38",
    "items": [
        {
            "texto": "Busca en tu Biblia Lucas 1,30 y completa lo que dice el ángel a María: «No temas, María, porque has hallado ______ delante de Dios.»",
            "respuesta": "GRACIA",
            "banco": ["GRACIA", "FAVOR", "RIQUEZA"],
        },
        {
            "texto": "¿Qué miedo has sentido tú alguna vez ante una decisión importante, y qué te ayudó (o te ayudaría) a enfrentarlo con confianza?",
            "abierta": True,
            "palabras_esperadas": ["MIEDO", "CONFIANZA", "DIOS", "ORACION", "APOYO", "FAMILIA"],
            "respuestas_referencia": [
                "Sentí miedo antes de un cambio importante, y hablarlo con mi familia me dio más confianza.",
                "Tuve miedo de una decisión sobre mis estudios, y la oración me ayudó a sentir más paz.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el evangelio de Lucas, capítulo 1, versículos 29 al 38.",
               "La palabra que falta es la misma que suele traducirse como «gracia» o «favor» de Dios."],
})

_agregar("C0N2-CO04", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: del miedo a la confianza",
    "items": [
        {"texto": "María, con confianza, responde que sí al plan de Dios.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "María se turba y siente temor ante el saludo del ángel.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "El ángel le dice: «No temas», y le explica lo que sucederá.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "María escucha con atención y empieza a comprender el mensaje.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué el miedo inicial de María (paso 1) no le impidió llegar a la confianza (paso 4)?",
            "abierta": True,
            "palabras_esperadas": ["MIEDO", "NORMAL", "CONFIANZA", "PROCESO", "ESCUCHAR"],
            "respuestas_referencia": [
                "Porque sentir miedo al principio es normal, y no impide después responder con confianza y fe.",
                "Porque el miedo fue solo el primer momento; escuchar y comprender la ayudó a pasar a la confianza.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El miedo de María no desaparece de golpe: pasa por escuchar y comprender antes de confiar.",
               "Sentir miedo al inicio no significa que la fe haya fallado."],
})

_agregar("C0N2-CO04", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "María sintió temor al principio del anuncio del ángel.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Sentir miedo significa automáticamente tener poca fe.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "El ángel invitó a María a no temer, no a fingir que no sentía nada.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "La confianza en Dios elimina por completo cualquier sensación de miedo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["MIEDO", "NORMAL", "FE", "CONFIANZA", "SENTIR"],
            "respuestas_referencia": [
                "Es falsa porque sentir miedo es humano y normal; no significa que falte fe.",
                "Es falsa porque la confianza no borra el miedo, ayuda a actuar a pesar de él.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa si la confianza y el miedo pueden coexistir en una misma persona.",
               "El ángel le dice a María «no temas», reconociendo que sí sentía temor."],
})

_agregar("C0N2-CO04", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: miedo y confianza",
    "items": [
        {
            "texto": "Caso 1: Laura tiene miedo de hablar en público durante una actividad de su parroquia. ¿Qué actitud refleja mejor la confianza que vivió María?",
            "respuesta": "Reconocer el miedo, prepararse y animarse a hacerlo de todos modos",
            "banco": ["Reconocer el miedo, prepararse y animarse a hacerlo de todos modos", "Evitar siempre cualquier situación que dé miedo", "Fingir que no siente miedo en absoluto"],
        },
        {
            "texto": "Caso 2: Bruno siente temor de comprometerse más con su fe por miedo a lo que piensen sus amigos. ¿Qué le ayudaría a responder con confianza?",
            "respuesta": "Hablar sus miedos con su catequista y dar un paso pequeño",
            "banco": ["Hablar sus miedos con su catequista y dar un paso pequeño", "Dejar de pensar en su fe para evitar el miedo", "Actuar solo si está seguro al cien por ciento"],
        },
        {
            "texto": "Caso 3: Daniela siente temor ante un cambio importante en su vida (mudanza, nuevo colegio). ¿Qué actitud es más parecida a la de María ante lo inesperado?",
            "respuesta": "Confiar en que Dios la acompaña, aunque el cambio le dé miedo",
            "banco": ["Confiar en que Dios la acompaña, aunque el cambio le dé miedo", "Resistirse al cambio sin ninguna apertura", "Pensar que Dios no tiene nada que ver con esta situación"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción combina reconocer el miedo con confiar en Dios.",
            "abierta": True,
            "palabras_esperadas": ["MIEDO", "CONFIANZA", "DIOS", "RECONOCER", "PASO"],
            "respuestas_referencia": [
                "Elegí el caso de Bruno, porque hablar el miedo y dar un paso pequeño refleja confianza sin negar lo que siente.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta reconoce el miedo, no lo niega ni se paraliza por él.",
               "Confiar en Dios no significa dejar de sentir miedo, sino actuar a pesar de él."],
})

_agregar("C0N2-CO04", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mi miedo y mi confianza",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «El miedo que sentí y la confianza que encontré». Incluye una idea central, una referencia a Lucas 1,29-38 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["MIEDO", "CONFIANZA", "DIOS", "MARIA", "TEMOR"],
            "respuestas_referencia": [
                "Idea central: como María, se puede sentir miedo y aun así confiar en Dios. Aplicación: reconocer un miedo propio y buscar apoyo para enfrentarlo.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un miedo real que hayas sentido y cómo lo enfrentaste."],
})

_agregar("C0N2-CO04", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: no temas",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) titulado «No temas», sobre un joven que reconoce su miedo y encuentra confianza para seguir adelante. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["MIEDO", "CONFIANZA", "TEMOR", "SEGUIR", "ADELANTE"],
            "respuestas_referencia": [
                "Escena 1: alguien enfrenta una situación que le da miedo. Escena 2: reconoce el miedo y busca apoyo. Escena 3: avanza con más confianza.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un miedo juvenil común: hablar en público, un cambio, una decisión importante."],
})

_agregar("C0N2-CO04", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: no temas",
    "items": [
        {
            "texto": "Completa: el ángel le dijo a María que había hallado ______ delante de Dios.",
            "respuesta": "GRACIA",
            "banco": ["GRACIA", "RIQUEZA", "FAMA"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué miedo sientes hoy ante alguna decisión de tu vida? ¿Con quién podrías hablarlo? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la palabra que el ángel usa para explicar por qué María no debía temer."],
})

_agregar("C0N2-CO04", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: enfrentar el miedo con fe",
    "situacion": "María sintió temor, pero no dejó que ese miedo le impidiera confiar en Dios y responder con libertad.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para enfrentar un miedo con más confianza en Dios?",
            "opciones": [
                "Hablar con alguien de confianza sobre lo que me da miedo",
                "Orar pidiendo fuerza para enfrentar una situación difícil",
                "Dar un paso pequeño hacia algo que me cuesta, aunque sienta temor",
                "Evitar por completo cualquier cosa que me genere miedo",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un miedo concreto tuyo y un paso pequeño y realista.",
               "Descarta la única opción que evita enfrentar cualquier cosa."],
    "feedback_ok": "¡Muy bien! Enfrentar el miedo con confianza, poco a poco, es parte de madurar en la fe.",
})


# --- C0N2-CO05 — Mi historia también puede ser llamada ---------------------
_agregar("C0N2-CO05", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: mi propia historia",
    "items": [
        {"texto": "Conjunto de experiencias, dones y circunstancias que forman la vida de una persona.", "respuesta": "HISTORIA"},
        {"texto": "Palabra que describe el llamado que Dios hace a cada persona en su propia vida.", "respuesta": "VOCACION"},
        {"texto": "Lo que hace única e irrepetible a cada persona.", "respuesta": "PROPIA"},
        {"texto": "Palabra que describe las capacidades y talentos recibidos de Dios.", "respuesta": "DONES"},
        {"texto": "Situaciones concretas (familia, lugar, momento) en las que vive cada persona.", "respuesta": "CIRCUNSTANCIAS"},
        {"texto": "Acto de darse cuenta de algo que antes no se veía con claridad.", "respuesta": "DESCUBRIR"},
        {"texto": "Palabra que describe una pregunta abierta sobre el propio camino de vida.", "respuesta": "INTERROGANTE"},
        {"texto": "Lo que se necesita para reconocer una llamada personal: atención a la propia vida.", "respuesta": "ATENCION"},
    ],
    "incluir": ["HISTORIA", "VOCACION"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con descubrir la propia vocación en la propia historia.",
               "HISTORIA y VOCACION son las palabras centrales: empieza por esas."],
})

_agregar("C0N2-CO05", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: mi propia historia",
    "palabras": ["HISTORIA", "VOCACION", "PROPIA", "DONES", "CIRCUNSTANCIAS", "DESCUBRIR", "INTERROGANTE", "ATENCION"],
    "incluir": ["HISTORIA", "VOCACION"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: DONES y PROPIA.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N2-CO05", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: 1 Samuel 3,1-10 y Lucas 1,26-38",
    "items": [
        {
            "texto": "Recordando los dos relatos que viste en este tema, completa: Dios llamó a Samuel siendo ______ y a María siendo una joven de Nazaret, cada uno en su propia historia.",
            "respuesta": "NIÑO",
            "banco": ["NIÑO", "ANCIANO", "REY"],
        },
        {
            "texto": "Pensando en tu propia historia (tu familia, tus dones, lo que te ha tocado vivir), ¿qué pregunta te gustaría hacerle a Dios sobre tu vocación?",
            "abierta": True,
            "palabras_esperadas": ["VOCACION", "DIOS", "VIDA", "FUTURO", "LLAMADA", "CAMINO", "PREGUNTA"],
            "respuestas_referencia": [
                "Me gustaría preguntarle a Dios qué espera de mí en esta etapa de mi vida.",
                "Quisiera saber si lo que me gusta hacer también puede ser parte de mi vocación.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Recuerda la edad de Samuel cuando Dios lo llamó por primera vez en el templo.",
               "No hay una respuesta única: se trata de una pregunta genuina y personal."],
})

_agregar("C0N2-CO05", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: descubrir mi propia llamada",
    "items": [
        {"texto": "Se da un paso concreto para explorar esa pregunta vocacional.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se presta atención a la propia historia, dones y circunstancias.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Aparece una pregunta o inquietud sobre el propio camino de vida.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se comparte esa pregunta con alguien de confianza (catequista, familia).", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué compartir la pregunta vocacional (paso 3) ayuda antes de dar un paso concreto (paso 4)?",
            "abierta": True,
            "palabras_esperadas": ["ACOMPAÑAR", "AYUDA", "CLARIDAD", "COMPARTIR", "DISCERNIR"],
            "respuestas_referencia": [
                "Porque compartirlo con alguien de confianza da claridad y ayuda a discernir mejor el paso siguiente.",
                "Porque no siempre es fácil ver con claridad la propia vocación en soledad; el acompañamiento ayuda.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de prestar atención, a hacerse preguntas, a compartirlas, y solo después actuar.",
               "Compartir una pregunta vocacional no es señal de debilidad, sino de sabiduría."],
})

_agregar("C0N2-CO05", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "La vocación cristiana solo la reciben algunas personas «especiales».", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dios puede llamar a alguien a través de su propia historia, dones y circunstancias.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Samuel y María fueron llamados en momentos y formas distintas, pero ambos respondieron con disponibilidad.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Descubrir la propia vocación es un proceso que ocurre de forma instantánea, sin ningún tiempo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["TODOS", "CADA", "PROCESO", "TIEMPO", "VOCACION"],
            "respuestas_referencia": [
                "Es falsa porque todos, no solo algunos, están llamados por Dios de alguna forma en su vida.",
                "Es falsa porque descubrir la vocación toma tiempo, como se vio en los procesos de Samuel y María.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa si la vocación es solo para sacerdotes o religiosas, o para toda persona.",
               "Compara cómo Samuel y María fueron llamados en momentos y edades distintas."],
})

_agregar("C0N2-CO05", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: mi historia también cuenta",
    "items": [
        {
            "texto": "Caso 1: Rodrigo piensa que su vida es «normal» y que Dios solo llama a personas con historias extraordinarias. ¿Qué le ayudaría a pensar distinto?",
            "respuesta": "Recordar que Samuel y María fueron personas comunes cuando Dios los llamó",
            "banco": ["Recordar que Samuel y María fueron personas comunes cuando Dios los llamó", "Pensar que su vida nunca podrá tener sentido vocacional", "Esperar algo extraordinario para creer que Dios lo llama"],
        },
        {
            "texto": "Caso 2: Antonella tiene facilidad para el arte y se pregunta si eso tiene algo que ver con su fe. ¿Qué actitud refleja mejor este contenido?",
            "respuesta": "Reconocer que sus dones también pueden ser parte de su vocación",
            "banco": ["Reconocer que sus dones también pueden ser parte de su vocación", "Pensar que el arte no tiene nada que ver con Dios", "Ignorar completamente sus talentos al pensar en su fe"],
        },
        {
            "texto": "Caso 3: Joaquín pasó por una situación familiar difícil y se pregunta si eso tiene sentido en su fe. ¿Qué actitud es más coherente con este contenido?",
            "respuesta": "Compartirlo con su catequista, confiando en que su historia también importa a Dios",
            "banco": ["Compartirlo con su catequista, confiando en que su historia también importa a Dios", "Pensar que esa situación lo aleja para siempre de cualquier vocación", "Evitar hablar de eso con cualquier persona"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción reconoce que la propia historia puede ser parte de una llamada.",
            "abierta": True,
            "palabras_esperadas": ["HISTORIA", "VOCACION", "DONES", "DIOS", "PROPIA"],
            "respuestas_referencia": [
                "Elegí el caso de Antonella, porque reconocer un talento como parte de la vocación es justo la idea de este contenido.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre reconoce valor en la propia historia, sin esperar algo extraordinario.",
               "Ni Samuel ni María tenían historias extraordinarias antes de ser llamados."],
})

_agregar("C0N2-CO05", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mi historia también puede ser llamada",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Mi historia también puede ser una llamada». Incluye una idea central, una referencia a Samuel o a María, y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["HISTORIA", "VOCACION", "DONES", "DIOS", "PROPIA"],
            "respuestas_referencia": [
                "Idea central: como Samuel y María, mi propia historia puede ser el lugar donde Dios me llama. Aplicación: prestar más atención a mis dones y circunstancias.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en algo concreto de tu propia historia (un don, una experiencia) antes de escribir."],
})

_agregar("C0N2-CO05", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: mi historia importa",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) titulado «Mi historia importa», mostrando a un joven que descubre que su propia vida tiene sentido vocacional. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["HISTORIA", "VOCACION", "DESCUBRIR", "PROPIA", "SENTIDO"],
            "respuestas_referencia": [
                "Escena 1: alguien piensa que su vida es «normal» y sin sentido especial. Escena 2: descubre un don o experiencia propia. Escena 3: entiende que eso también puede ser parte de su vocación.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un don o experiencia común que, vista con otros ojos, puede tener sentido vocacional."],
})

_agregar("C0N2-CO05", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: mi historia también cuenta",
    "items": [
        {
            "texto": "Completa: Dios llama a cada persona a través de su propia ______, dones y circunstancias.",
            "respuesta": "HISTORIA",
            "banco": ["HISTORIA", "FAMA", "RIQUEZA"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué parte de tu historia (un don, una experiencia, una circunstancia) crees que Dios podría estar usando para llamarte? Coméntalo con tu catequista.",
    "pistas": ["Piensa en lo que comparten Samuel y María: ambos fueron llamados dentro de su propia historia."],
})

_agregar("C0N2-CO05", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: explorar mi vocación",
    "situacion": "Así como Samuel y María descubrieron su llamada dentro de su propia historia, cada joven puede empezar a explorar la suya.",
    "items": [
        {
            "texto": "¿Qué paso concreto puedes dar esta semana para explorar tu propia pregunta vocacional?",
            "opciones": [
                "Escribir en un cuaderno una pregunta vocacional que tengo",
                "Hablar con mi catequista sobre un don que me gustaría poner al servicio de otros",
                "Dedicar un momento de oración a pedir claridad sobre mi camino",
                "Evitar pensar en el tema porque todavía soy joven",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un paso pequeño y concreto, no en una decisión definitiva.",
               "Descarta la única opción que evita explorar el tema."],
    "feedback_ok": "¡Muy bien! Explorar la propia vocación, paso a paso, es parte de crecer en la fe.",
})


# --- C0N2-CO06 — Discernir acompañados --------------------------------------
_agregar("C0N2-CO06", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: discernir con otros",
    "items": [
        {"texto": "Acción de pensar y decidir con calma un asunto importante.", "respuesta": "DISCERNIR"},
        {"texto": "Persona que camina junto a otra, ayudándola en su proceso de fe.", "respuesta": "ACOMPAÑANTE"},
        {"texto": "Sacerdote que ayudó a Samuel a reconocer la voz de Dios.", "respuesta": "ELI"},
        {"texto": "Familiar de María que confirmó, con su propio embarazo, el anuncio del ángel.", "respuesta": "ISABEL"},
        {"texto": "Lugar donde un joven encuentra apoyo para su proceso de fe.", "respuesta": "IGLESIA"},
        {"texto": "Cualidad de confiar en el consejo de alguien con más experiencia.", "respuesta": "HUMILDAD"},
        {"texto": "Palabra que describe a las personas de confianza que rodean a un joven.", "respuesta": "COMUNIDAD"},
        {"texto": "Lo que se recibe cuando alguien ayuda a ver con más claridad una situación.", "respuesta": "CONSEJO"},
    ],
    "incluir": ["DISCERNIR", "COMUNIDAD"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con discernir con la ayuda de otros.",
               "DISCERNIR y COMUNIDAD son las palabras centrales: empieza por esas."],
})

_agregar("C0N2-CO06", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: discernir con otros",
    "palabras": ["DISCERNIR", "ACOMPAÑANTE", "ELI", "ISABEL", "IGLESIA", "HUMILDAD", "COMUNIDAD", "CONSEJO"],
    "incluir": ["DISCERNIR", "COMUNIDAD"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: ELI e ISABEL.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N2-CO06", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: 1 Samuel 3,8-10 y Lucas 1,35-38",
    "items": [
        {
            "texto": "Busca en tu Biblia 1 Samuel 3,8-9 y completa: fue ______ quien entendió que era Dios quien llamaba a Samuel y le enseñó cómo responder.",
            "respuesta": "ELI",
            "banco": ["ELI", "SAMUEL", "DAVID"],
        },
        {
            "texto": "¿Por qué crees que tanto Samuel como María necesitaron, de alguna forma, el acompañamiento de otra persona para entender mejor su llamada?",
            "abierta": True,
            "palabras_esperadas": ["ACOMPAÑAR", "AYUDA", "COMUNIDAD", "APOYO", "CLARIDAD", "DISCERNIR"],
            "respuestas_referencia": [
                "Porque discernir en soledad es más difícil; el acompañamiento de otros ayuda a ver con más claridad.",
                "Porque tanto Elí como el ángel (y después Isabel) ayudaron a confirmar lo que cada uno estaba viviendo.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el primer libro de Samuel, capítulo 3, versículos 8 y 9.",
               "Recuerda quién ayudó a Samuel a entender que era Dios quien lo llamaba."],
})

_agregar("C0N2-CO06", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: discernir acompañados",
    "items": [
        {"texto": "Con esa ayuda, la persona toma la decisión con más claridad y paz.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Una persona siente una inquietud o llamada que no termina de entender.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Decide compartirlo con alguien de confianza (catequista, familia, comunidad).", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Esa persona de confianza escucha y ayuda a ver la situación con más claridad.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué compartir la inquietud (paso 2) suele ayudar más que resolverla completamente en soledad?",
            "abierta": True,
            "palabras_esperadas": ["ACOMPAÑAR", "CLARIDAD", "OTRA PERSPECTIVA", "AYUDA", "COMUNIDAD"],
            "respuestas_referencia": [
                "Porque otra persona puede aportar una perspectiva distinta que ayuda a ver con más claridad la situación.",
                "Porque, como Samuel con Elí, muchas veces se necesita ayuda externa para entender bien una inquietud interior.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de sentir la inquietud, a compartirla, a recibir ayuda, y solo después decidir.",
               "Tanto Samuel como María recibieron ayuda de otra persona en su proceso."],
})

_agregar("C0N2-CO06", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Elí ayudó a Samuel a reconocer que era Dios quien lo llamaba.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Discernir en comunidad es una señal de debilidad en la fe.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "El acompañamiento de otra persona puede ayudar a ver con más claridad una decisión.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "En la Biblia, discernir siempre se hace completamente en soledad, sin ayuda de nadie.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["ACOMPAÑAR", "AYUDA", "ELI", "MADUREZ", "HUMILDAD"],
            "respuestas_referencia": [
                "Es falsa porque pedir ayuda para discernir es señal de humildad y madurez, no de debilidad.",
                "Es falsa porque tanto Samuel como María recibieron algún tipo de acompañamiento en su proceso.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en el papel de Elí en la historia de Samuel.",
               "Pedir ayuda para discernir no debilita la fe, la fortalece."],
})

_agregar("C0N2-CO06", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: discernir acompañados",
    "items": [
        {
            "texto": "Caso 1: Patricia tiene una duda importante sobre su fe y prefiere resolverla completamente sola. ¿Qué le podrías sugerir, con respeto?",
            "respuesta": "Compartirla con su catequista para pensarla juntas",
            "banco": ["Compartirla con su catequista para pensarla juntas", "Que nunca hable de sus dudas con nadie", "Que resuelva la duda sin pensarla demasiado"],
        },
        {
            "texto": "Caso 2: Iker siente que Dios lo llama a algo, pero no confía en su propio criterio para decidir solo. ¿Qué actitud le ayudaría, como a Samuel?",
            "respuesta": "Buscar el consejo de alguien con más experiencia en la fe",
            "banco": ["Buscar el consejo de alguien con más experiencia en la fe", "Decidir sin pedir ayuda a nadie por miedo a parecer débil", "Ignorar completamente lo que siente"],
        },
        {
            "texto": "Caso 3: Melissa recibió un buen consejo de su catequista, pero al final decide algo distinto. ¿Qué es lo más coherente con el discernimiento acompañado?",
            "respuesta": "Agradecer el consejo y decidir con libertad, habiéndolo pensado con calma",
            "banco": ["Agradecer el consejo y decidir con libertad, habiéndolo pensado con calma", "Sentirse mal por no haber seguido el consejo al pie de la letra", "Dejar de pedir consejos en el futuro"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja un discernimiento maduro y acompañado.",
            "abierta": True,
            "palabras_esperadas": ["ACOMPAÑAR", "CONSEJO", "DISCERNIR", "LIBERTAD", "AYUDA"],
            "respuestas_referencia": [
                "Elegí el caso de Iker, porque buscar consejo no le quita libertad, lo ayuda a decidir con más claridad.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre valora el consejo de otros sin eliminar la libertad de decidir.",
               "Discernir acompañado no significa que otra persona decida por uno."],
})

_agregar("C0N2-CO06", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: no discierno solo",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Por qué no discierno solo». Incluye una idea central, una referencia a Samuel y Elí (o a María e Isabel), y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["ACOMPAÑAR", "DISCERNIR", "COMUNIDAD", "CONSEJO", "AYUDA"],
            "respuestas_referencia": [
                "Idea central: como Samuel con Elí, discernir se hace mejor acompañado. Aplicación: buscar el consejo de mi catequista ante una duda real.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una persona concreta con quien podrías compartir una duda importante de tu fe."],
})

_agregar("C0N2-CO06", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: pedir consejo",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) sobre un joven que, ante una duda importante, decide pedir consejo en vez de decidir solo. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["CONSEJO", "ACOMPAÑAR", "DISCERNIR", "AYUDA", "DUDA"],
            "respuestas_referencia": [
                "Escena 1: alguien con una duda importante, dudando si pedir ayuda. Escena 2: decide hablarlo con su catequista. Escena 3: toma una decisión con más claridad.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una duda juvenil común (una decisión, un compromiso) y cómo pedir consejo ayudaría."],
})

_agregar("C0N2-CO06", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: discernir acompañados",
    "items": [
        {
            "texto": "Completa: fue ______ quien ayudó a Samuel a entender que era Dios quien lo llamaba, y le enseñó cómo responder.",
            "respuesta": "ELI",
            "banco": ["ELI", "SAMUEL", "SAUL"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Con quién podrías compartir una duda importante de tu fe, como Samuel lo hizo con Elí? Coméntalo con tu catequista.",
    "pistas": ["Piensa en el sacerdote que acompañó a Samuel en el templo."],
})

_agregar("C0N2-CO06", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: buscar acompañamiento",
    "situacion": "Tanto Samuel como María recibieron ayuda de otras personas para discernir su llamada. Un joven de hoy también puede buscar ese acompañamiento.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para discernir una duda o decisión acompañado, en vez de completamente solo?",
            "opciones": [
                "Compartir una duda de fe con mi catequista",
                "Pedir el consejo de un familiar de confianza",
                "Hablarlo en mi grupo de catequesis",
                "Decidir todo siempre en completa soledad",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una persona concreta de tu confianza a quien podrías acudir.",
               "Descarta la única opción que evita el acompañamiento."],
    "feedback_ok": "¡Felicidades! Terminaste C0N2 «Jóvenes en la Biblia». Escuchar, confiar y dejarse acompañar son pasos firmes en tu camino de fe.",
})

# ==========================================================================
# C0N3 — Creer en tiempos de duda   (Hechos 17,16-34)
# ==========================================================================

# --- C0N3-CO01 — La duda puede abrir preguntas -----------------------------
_agregar("C0N3-CO01", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: preguntas honestas",
    "items": [
        {"texto": "Ciudad griega llena de ídolos que Pablo recorre antes de hablar en el Areópago.", "respuesta": "ATENAS"},
        {"texto": "Sentimiento de incertidumbre que puede abrir preguntas honestas o cerrar la fe.", "respuesta": "DUDA"},
        {"texto": "Lo que hace quien busca comprender mejor algo que no le queda claro.", "respuesta": "PREGUNTAR"},
        {"texto": "Lugar de Atenas donde Pablo fue invitado a explicar su enseñanza.", "respuesta": "AREOPAGO"},
        {"texto": "Palabra que describe rechazar algo de plano, sin siquiera considerarlo.", "respuesta": "NEGACION"},
        {"texto": "Cualidad de una pregunta que busca de verdad entender, no solo criticar.", "respuesta": "HONESTA"},
        {"texto": "Lo que sintió Pablo al ver la ciudad llena de ídolos: se llenó de...", "respuesta": "INDIGNACION"},
        {"texto": "Palabra que describe el proceso de buscar comprender algo con la razón.", "respuesta": "COMPRENDER"},
    ],
    "incluir": ["DUDA", "PREGUNTAR"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con el relato de Pablo en Atenas, Hechos 17,16-23.",
               "DUDA y PREGUNTAR son las palabras centrales: empieza por esas."],
})

_agregar("C0N3-CO01", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: preguntas honestas",
    "palabras": ["ATENAS", "DUDA", "PREGUNTAR", "AREOPAGO", "NEGACION", "HONESTA", "INDIGNACION", "COMPRENDER"],
    "incluir": ["DUDA", "PREGUNTAR"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: DUDA y ATENAS.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N3-CO01", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Hechos 17,16-23",
    "items": [
        {
            "texto": "Busca en tu Biblia Hechos 17,16 y completa: viendo Pablo la ciudad de Atenas entregada a la ______, se llenó de indignación en su espíritu.",
            "respuesta": "IDOLATRIA",
            "banco": ["IDOLATRIA", "POBREZA", "GUERRA"],
        },
        {
            "texto": "¿Alguna vez tuviste una duda honesta sobre tu fe? ¿Qué hiciste con ella: la escondiste, la ignoraste o buscaste entenderla mejor?",
            "abierta": True,
            "palabras_esperadas": ["DUDA", "PREGUNTAR", "BUSCAR", "ENTENDER", "FE", "HONESTA"],
            "respuestas_referencia": [
                "Tuve dudas sobre algunas cosas de la fe, y preferí hablarlas con mi catequista para entenderlas mejor.",
                "Alguna vez dudé, y traté de buscar respuestas en vez de simplemente ignorar la pregunta.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el libro de los Hechos de los Apóstoles, capítulo 17, versículos 16 al 23.",
               "La palabra que falta describe la adoración a los ídolos que Pablo ve en la ciudad."],
})

_agregar("C0N3-CO01", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: de la duda a la pregunta honesta",
    "items": [
        {"texto": "Esa búsqueda puede fortalecer la fe en vez de destruirla.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Aparece una duda o inquietud sobre algún aspecto de la fe.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se decide no ignorarla ni rechazarla de plano, sino considerarla.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se busca información, diálogo o acompañamiento para entenderla mejor.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué considerar la duda (paso 2), en vez de rechazarla de inmediato, es un paso importante?",
            "abierta": True,
            "palabras_esperadas": ["HONESTA", "COMPRENDER", "MADUREZ", "BUSCAR", "CRECER"],
            "respuestas_referencia": [
                "Porque rechazar la duda sin pensarla impide crecer; considerarla con honestidad abre camino a comprender mejor.",
                "Porque una duda tomada en serio, y no ignorada, puede llevar a una fe más madura y reflexionada.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de sentir la duda, a no rechazarla, a buscar entenderla, y solo después fortalecer la fe.",
               "Ignorar una duda no es lo mismo que resolverla."],
})

_agregar("C0N3-CO01", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Toda duda sobre la fe es automáticamente una falta de fe.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Una pregunta honesta busca comprender, no solo rechazar de plano.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Pablo se indignó al ver la ciudad de Atenas llena de ídolos.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Ignorar por completo una duda es la mejor forma de fortalecer la fe.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["DUDA", "HONESTA", "COMPRENDER", "IGNORAR", "MADUREZ"],
            "respuestas_referencia": [
                "Es falsa porque una duda honesta puede ser parte de crecer en la fe, no necesariamente una falta de ella.",
                "Es falsa porque ignorar una duda no la resuelve; buscar entenderla suele ser más útil.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa si toda pregunta sobre la fe es lo mismo que rechazarla.",
               "Recuerda qué sintió Pablo al ver la idolatría en Atenas."],
})

_agregar("C0N3-CO01", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: preguntar sin miedo",
    "items": [
        {
            "texto": "Caso 1: Ezequiel tiene una duda sobre algo que aprendió en catequesis, pero le da vergüenza preguntarla en público. ¿Qué actitud le convendría más?",
            "respuesta": "Hablarlo en privado con su catequista, sin avergonzarse de preguntar",
            "banco": ["Hablarlo en privado con su catequista, sin avergonzarse de preguntar", "Quedarse con la duda para siempre por vergüenza", "Fingir que ya lo entiende todo"],
        },
        {
            "texto": "Caso 2: Milena escuchó un argumento en contra de la fe y no supo qué responder. ¿Qué actitud refleja mejor lo que vivió Pablo en Atenas?",
            "respuesta": "Investigar y buscar entender mejor el argumento antes de responder",
            "banco": ["Investigar y buscar entender mejor el argumento antes de responder", "Enojarse y cortar la conversación de inmediato", "Aceptar el argumento sin pensarlo, para evitar el conflicto"],
        },
        {
            "texto": "Caso 3: Diego cree que tener dudas significa que no es un buen creyente. ¿Qué le ayudaría a ver esto de otra forma?",
            "respuesta": "Entender que las preguntas honestas pueden fortalecer la fe, no debilitarla",
            "banco": ["Entender que las preguntas honestas pueden fortalecer la fe, no debilitarla", "Reforzar la idea de que dudar es siempre malo", "Dejar de participar en la catequesis por sentirse mal creyente"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja una actitud sana frente a las dudas.",
            "abierta": True,
            "palabras_esperadas": ["DUDA", "PREGUNTAR", "HONESTA", "COMPRENDER", "FE"],
            "respuestas_referencia": [
                "Elegí el caso de Ezequiel, porque preguntar con confianza, sin vergüenza, ayuda a resolver mejor una duda.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre busca entender, nunca esconde ni rechaza la pregunta de plano.",
               "Tener dudas no es lo opuesto de tener fe."],
})

_agregar("C0N3-CO01", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mis preguntas honestas",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Una duda que tuve y lo que aprendí de ella». Incluye una idea central, una referencia a Hechos 17,16-23 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["DUDA", "PREGUNTA", "FE", "COMPRENDER", "HONESTA"],
            "respuestas_referencia": [
                "Idea central: las dudas honestas, como las de quienes escuchaban a Pablo, pueden abrir camino a comprender mejor la fe. Aplicación: no tener miedo de preguntar lo que no entiendo.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una duda real que hayas tenido (o que tengas) sobre la fe."],
})

_agregar("C0N3-CO01", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: preguntar sin miedo",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) sobre un joven que se anima a compartir una duda honesta de su fe en vez de esconderla. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["DUDA", "PREGUNTAR", "HONESTA", "COMPARTIR", "FE"],
            "respuestas_referencia": [
                "Escena 1: alguien con una duda que no se anima a compartir. Escena 2: decide hablarlo con su catequista. Escena 3: entiende mejor su fe gracias a esa conversación.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una duda juvenil común sobre la fe."],
})

_agregar("C0N3-CO01", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: preguntas honestas",
    "items": [
        {
            "texto": "Completa: Pablo se llenó de indignación al ver la ciudad de Atenas entregada a la ______.",
            "respuesta": "IDOLATRIA",
            "banco": ["IDOLATRIA", "POBREZA", "FIESTA"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué pregunta honesta tienes hoy sobre tu fe, que te gustaría conversar con tu catequista? Coméntalo con él o ella.",
    "pistas": ["Piensa en lo que Pablo vio al recorrer la ciudad de Atenas."],
})

_agregar("C0N3-CO01", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: hacer espacio a mis preguntas",
    "situacion": "Tener dudas honestas sobre la fe no es un problema: puede ser una oportunidad para comprenderla mejor, como muestra el relato de Pablo en Atenas.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana con una duda que tengas sobre tu fe?",
            "opciones": [
                "Escribirla para no olvidarla y poder hablarla después",
                "Compartirla con mi catequista o con mi grupo de catequesis",
                "Buscar con calma más información sobre el tema",
                "Guardarla para siempre sin decírselo a nadie",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una acción concreta para tu propia duda, no en una idea general.",
               "Descarta la única opción que no busca ninguna respuesta."],
    "feedback_ok": "¡Muy bien! Las preguntas honestas, bien acompañadas, pueden fortalecer tu fe.",
})


# --- C0N3-CO02 — Pablo dialoga con la cultura -------------------------------
_agregar("C0N3-CO02", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: Pablo dialoga en Atenas",
    "items": [
        {"texto": "Lo que Pablo hace antes de hablar: observar con atención la ciudad y su cultura.", "respuesta": "OBSERVAR"},
        {"texto": "Inscripción que Pablo encontró en un altar de Atenas: «Al Dios no...»", "respuesta": "CONOCIDO"},
        {"texto": "Acción de intercambiar ideas con respeto entre personas que piensan distinto.", "respuesta": "DIALOGAR"},
        {"texto": "Grupo de filósofos griegos que escuchó a Pablo en el Areópago.", "respuesta": "ESTOICOS"},
        {"texto": "Lugar público donde Pablo debatía cada día con quien pasaba por ahí.", "respuesta": "AGORA"},
        {"texto": "Actitud de Pablo antes de anunciar: partir de lo que la gente ya conoce o cree.", "respuesta": "PUNTODEPARTIDA"},
        {"texto": "Palabra que describe anunciar el Evangelio con palabras y gestos.", "respuesta": "ANUNCIAR"},
        {"texto": "Cualidad de un mensaje que se adapta al lenguaje de quien escucha, sin perder su verdad.", "respuesta": "RESPETUOSO"},
    ],
    "incluir": ["OBSERVAR", "DIALOGAR"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con cómo Pablo se acerca a la cultura ateniense.",
               "OBSERVAR y DIALOGAR son las palabras centrales: empieza por esas."],
})

_agregar("C0N3-CO02", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: Pablo dialoga en Atenas",
    "palabras": ["OBSERVAR", "CONOCIDO", "DIALOGAR", "ESTOICOS", "AGORA", "ANUNCIAR", "RESPETUOSO", "CULTURA"],
    "incluir": ["OBSERVAR", "DIALOGAR"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: AGORA y CULTURA.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad, salvo una que se cambió por CULTURA para que quepa mejor en la sopa."],
})

_agregar("C0N3-CO02", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Hechos 17,22-23",
    "items": [
        {
            "texto": "Busca en tu Biblia Hechos 17,23 y completa: Pablo dice que encontró un altar con la inscripción «AL DIOS NO ______», y que ese Dios es el que él anuncia.",
            "respuesta": "CONOCIDO",
            "banco": ["CONOCIDO", "VISIBLE", "AMADO"],
        },
        {
            "texto": "¿Qué te parece la forma en que Pablo empieza su discurso, partiendo de algo que los atenienses ya conocían (el altar), en vez de criticarlos de entrada?",
            "abierta": True,
            "palabras_esperadas": ["RESPETO", "DIALOGO", "ESCUCHAR", "OBSERVAR", "PUENTE", "CONECTAR"],
            "respuestas_referencia": [
                "Me parece una forma respetuosa de dialogar: conecta con lo que ellos ya creían para explicarles algo nuevo.",
                "Creo que fue inteligente, porque en vez de criticarlos, buscó un punto en común para empezar el diálogo.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el libro de los Hechos, capítulo 17, versículo 23.",
               "La palabra que falta aparece también en el título de esta actividad."],
})

_agregar("C0N3-CO02", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: cómo dialoga Pablo",
    "items": [
        {"texto": "Anuncia con respeto lo que él cree, partiendo de ese punto en común.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Pablo recorre la ciudad y observa con atención su cultura y sus creencias.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Nota un altar dedicado «al Dios no conocido».", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Usa ese altar como punto de partida para dialogar con los atenienses.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué observar primero (paso 1), en vez de hablar de inmediato, ayudó a Pablo a dialogar mejor?",
            "abierta": True,
            "palabras_esperadas": ["OBSERVAR", "ESCUCHAR", "ENTENDER", "RESPETO", "CONECTAR"],
            "respuestas_referencia": [
                "Porque observar antes de hablar le permitió entender mejor a quién se dirigía y cómo conectar con ellos.",
                "Porque conocer primero la cultura ajena ayuda a dialogar con respeto, en vez de imponer algo desde afuera.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso de Pablo va de observar, a notar un detalle, a usarlo de puente, y solo después anunciar.",
               "Pablo no empieza criticando, sino observando con atención."],
})

_agregar("C0N3-CO02", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Pablo observó la cultura de Atenas antes de hablar en el Areópago.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Pablo empezó su discurso criticando con dureza a los atenienses.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Pablo usó un altar que ya existía en la ciudad como punto de partida para su mensaje.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dialogar con otra cultura significa estar de acuerdo con todo lo que esa cultura cree.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["RESPETO", "PUNTO", "COMUN", "DIALOGO", "ANUNCIAR"],
            "respuestas_referencia": [
                "Es falsa porque Pablo partió de un punto en común (el altar) en vez de empezar criticando.",
                "Es falsa porque dialogar es buscar puntos de encuentro, no significa estar de acuerdo con todo.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en cómo empieza Pablo su discurso en el Areópago: con un elogio, no con una crítica.",
               "Dialogar no es lo mismo que aceptar todo sin ningún criterio propio."],
})

_agregar("C0N3-CO02", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: dialogar como Pablo",
    "items": [
        {
            "texto": "Caso 1: Un compañero de clase de Marcos tiene creencias muy distintas a las suyas. ¿Qué actitud se parece más a la de Pablo en Atenas?",
            "respuesta": "Escuchar primero para entender su punto de vista antes de compartir el propio",
            "banco": ["Escuchar primero para entender su punto de vista antes de compartir el propio", "Criticar de inmediato lo que piensa sin escucharlo", "Evitar cualquier conversación sobre el tema"],
        },
        {
            "texto": "Caso 2: Valeria quiere hablar de su fe con una amiga que no cree en Dios, sin imponerla. ¿Qué actitud de Pablo le podría servir?",
            "respuesta": "Buscar un punto en común desde donde empezar la conversación",
            "banco": ["Buscar un punto en común desde donde empezar la conversación", "Insistir hasta que su amiga cambie de opinión", "No hablar nunca del tema para evitar cualquier diferencia"],
        },
        {
            "texto": "Caso 3: En un grupo de amigos surge un debate sobre religión y ciencia. ¿Cuál sería la actitud más parecida a la de Pablo en el Areópago?",
            "respuesta": "Participar con respeto, escuchando y compartiendo su punto de vista con calma",
            "banco": ["Participar con respeto, escuchando y compartiendo su punto de vista con calma", "Imponer su opinión gritando más fuerte que los demás", "Quedarse callado por miedo a decir algo distinto"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja el diálogo respetuoso que vivió Pablo.",
            "abierta": True,
            "palabras_esperadas": ["DIALOGO", "RESPETO", "ESCUCHAR", "PABLO", "PUNTO COMUN"],
            "respuestas_referencia": [
                "Elegí el caso de Marcos, porque escuchar antes de opinar es justo la actitud que tuvo Pablo antes de hablar.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre escucha primero y busca puntos en común, sin imponer ni evitar el tema.",
               "Dialogar con respeto no significa quedarse callado ni imponer la propia opinión a la fuerza."],
})

_agregar("C0N3-CO02", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: dialogar sin imponer",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Cómo hablar de mi fe sin imponerla». Incluye una idea central, una referencia a Hechos 17,22-23 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["DIALOGO", "RESPETO", "ESCUCHAR", "PABLO", "FE"],
            "respuestas_referencia": [
                "Idea central: como Pablo en Atenas, se puede compartir la fe con respeto, partiendo de un punto en común. Aplicación: escuchar más antes de opinar en una conversación sobre fe.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una conversación real sobre fe que hayas tenido con alguien que piensa distinto."],
})

_agregar("C0N3-CO02", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: un diálogo respetuoso",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) sobre dos personas con creencias distintas que dialogan con respeto, inspirado en Pablo en el Areópago. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["DIALOGO", "RESPETO", "ESCUCHAR", "DISTINTO", "PUNTO COMUN"],
            "respuestas_referencia": [
                "Escena 1: dos personas con opiniones distintas. Escena 2: una de ellas escucha con atención antes de responder. Escena 3: encuentran un punto en común para seguir hablando.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un tema donde dos jóvenes puedan pensar distinto y aun así dialogar con respeto."],
})

_agregar("C0N3-CO02", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: Pablo dialoga con la cultura",
    "items": [
        {
            "texto": "Completa: Pablo usó un altar dedicado «al Dios no ______» como punto de partida para su discurso.",
            "respuesta": "CONOCIDO",
            "banco": ["CONOCIDO", "AMADO", "TEMIDO"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Con qué persona que piensa distinto a ti podrías intentar un diálogo respetuoso, como el de Pablo? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la inscripción del altar que Pablo encontró en Atenas."],
})

_agregar("C0N3-CO02", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: dialogar con respeto",
    "situacion": "Pablo dialogó con la cultura de Atenas partiendo de un punto en común, sin imponer ni evitar el tema de su fe.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para dialogar mejor con alguien que piensa distinto sobre la fe?",
            "opciones": [
                "Escuchar con atención antes de compartir mi propia opinión",
                "Buscar un punto en común desde donde empezar la conversación",
                "Compartir lo que creo con respeto, sin imponerlo",
                "Evitar por completo cualquier conversación sobre el tema",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una conversación real que podrías tener esta semana.",
               "Descarta la única opción que evita cualquier diálogo."],
    "feedback_ok": "¡Muy bien! Dialogar con respeto, como Pablo, es una forma valiosa de compartir la fe.",
})


# --- C0N3-CO03 — Fe y razón no son enemigas ---------------------------------
_agregar("C0N3-CO03", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: fe y razón",
    "items": [
        {"texto": "Capacidad de pensar, argumentar y buscar la verdad con la mente.", "respuesta": "RAZON"},
        {"texto": "Confianza y adhesión a Dios que va más allá de lo que se puede demostrar del todo.", "respuesta": "FE"},
        {"texto": "Palabra que describe algo que se puede pensar y sostener con argumentos.", "respuesta": "ARGUMENTO"},
        {"texto": "Lo que buscan tanto la fe como la razón, cada una a su manera.", "respuesta": "VERDAD"},
        {"texto": "Palabra que describe cuando dos cosas pueden coexistir sin oponerse.", "respuesta": "COMPLEMENTAR"},
        {"texto": "Idea de que la fe y la ciencia son enemigas irreconciliables (lo que este contenido cuestiona).", "respuesta": "OPOSICION"},
        {"texto": "Grupo de filósofos griegos (junto a los estoicos) que escuchó a Pablo.", "respuesta": "EPICUREOS"},
        {"texto": "Palabra que describe pensar con cuidado antes de aceptar o rechazar una idea.", "respuesta": "REFLEXIONAR"},
    ],
    "incluir": ["FE", "RAZON"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con la relación entre la fe y el pensamiento razonado.",
               "FE y RAZON son las palabras centrales: empieza por esas."],
})

_agregar("C0N3-CO03", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: fe y razón",
    "palabras": ["RAZON", "FE", "ARGUMENTO", "VERDAD", "COMPLEMENTAR", "OPOSICION", "EPICUREOS", "REFLEXIONAR"],
    "incluir": ["FE", "RAZON"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: FE y RAZON.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N3-CO03", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Hechos 17,22-31",
    "items": [
        {
            "texto": "Busca en tu Biblia Hechos 17,28 y completa: Pablo cita a poetas griegos para explicar algo sobre Dios: «En él vivimos, y nos movemos, y ______.»",
            "respuesta": "SOMOS",
            "banco": ["SOMOS", "CREEMOS", "ORAMOS"],
        },
        {
            "texto": "¿Por qué crees que Pablo usó ideas de la cultura griega (poetas, filósofos) para explicar su fe, en vez de rechazar por completo esa forma de pensar?",
            "abierta": True,
            "palabras_esperadas": ["DIALOGO", "RAZON", "PUENTE", "COMPRENDER", "COMPLEMENTAR"],
            "respuestas_referencia": [
                "Porque mostró que la fe puede dialogar con el pensamiento razonado, usando lo que ya conocían para explicar algo nuevo.",
                "Porque la fe y la razón no tienen por qué oponerse; Pablo tendió un puente entre ambas.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el libro de los Hechos, capítulo 17, versículo 28.",
               "Pablo cita una frase de poetas griegos para hablar de la cercanía de Dios."],
})

_agregar("C0N3-CO03", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: fe y razón dialogan",
    "items": [
        {"texto": "El resultado es una fe más reflexionada, sin dejar de ser fe.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Surge una pregunta que parece poner en tensión la fe y la razón.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se busca entender la pregunta con calma, sin miedo ni rechazo automático.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se descubre que la fe y la razón pueden dialogar, como hizo Pablo con los griegos.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué buscar entender con calma (paso 2) es mejor que rechazar de inmediato una pregunta difícil?",
            "abierta": True,
            "palabras_esperadas": ["COMPRENDER", "CALMA", "MADUREZ", "DIALOGO", "RAZON"],
            "respuestas_referencia": [
                "Porque rechazar sin pensar cierra la posibilidad de entender mejor; la calma ayuda a un diálogo más maduro.",
                "Porque, como Pablo mostró, la fe puede sostener preguntas razonadas sin sentirse amenazada por ellas.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de la pregunta, a la calma para pensarla, al descubrimiento de que fe y razón dialogan.",
               "Pablo no le tuvo miedo a pensar con los filósofos griegos."],
})

_agregar("C0N3-CO03", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "La fe y la razón siempre están en guerra, sin ninguna posibilidad de diálogo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Pablo usó ideas de poetas y filósofos griegos para explicar su mensaje.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Pensar con argumentos sobre la fe es una falta de confianza en Dios.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "La fe y la razón pueden buscar juntas la verdad, cada una a su manera.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["DIALOGO", "RAZON", "FE", "COMPLEMENTAR", "PENSAR"],
            "respuestas_referencia": [
                "Es falsa porque, como mostró Pablo, la fe y la razón pueden dialogar en vez de estar siempre en guerra.",
                "Es falsa porque pensar con argumentos sobre la fe puede fortalecerla, no debilitarla.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en cómo Pablo usó el pensamiento griego para explicar su mensaje, sin rechazarlo.",
               "Reflexionar sobre la fe no es lo mismo que dudar de Dios."],
})

_agregar("C0N3-CO03", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: fe y razón en la vida diaria",
    "items": [
        {
            "texto": "Caso 1: Un profesor de ciencias le dice a Tomás que la fe y la ciencia son incompatibles. ¿Qué actitud refleja mejor lo aprendido en este contenido?",
            "respuesta": "Pensar que ambas pueden buscar la verdad desde preguntas distintas",
            "banco": ["Pensar que ambas pueden buscar la verdad desde preguntas distintas", "Aceptar de inmediato que la fe no tiene ningún sentido", "Rechazar la ciencia por completo sin ningún argumento"],
        },
        {
            "texto": "Caso 2: Camila tiene preguntas científicas sobre el origen del universo y le preocupa que eso afecte su fe. ¿Qué actitud le ayudaría más?",
            "respuesta": "Investigar con calma y hablarlo con su catequista, sin miedo a la pregunta",
            "banco": ["Investigar con calma y hablarlo con su catequista, sin miedo a la pregunta", "Evitar para siempre cualquier tema relacionado con la ciencia", "Dejar de creer apenas surja la primera pregunta difícil"],
        },
        {
            "texto": "Caso 3: En un debate escolar, a Felipe le cuesta explicar por qué su fe tiene sentido razonable. ¿Qué le ayudaría, inspirado en Pablo?",
            "respuesta": "Prepararse con argumentos claros y respetuosos, como hizo Pablo en el Areópago",
            "banco": ["Prepararse con argumentos claros y respetuosos, como hizo Pablo en el Areópago", "Evitar el debate por miedo a no saber responder", "Responder con enojo en vez de con argumentos"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción muestra que la fe puede sostenerse con argumentos razonables.",
            "abierta": True,
            "palabras_esperadas": ["RAZON", "FE", "ARGUMENTO", "DIALOGO", "PABLO"],
            "respuestas_referencia": [
                "Elegí el caso de Camila, porque investigar con calma es una forma madura de sostener la fe frente a preguntas científicas.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre busca argumentos y diálogo, nunca el rechazo automático ni el miedo.",
               "Como Pablo, se puede sostener la fe con razones, sin necesidad de rechazar el pensamiento crítico."],
})

_agregar("C0N3-CO03", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: fe y razón pueden dialogar",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «¿Por qué mi fe también puede ser razonable?». Incluye una idea central, una referencia a Hechos 17,22-31 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["FE", "RAZON", "DIALOGO", "ARGUMENTO", "PABLO"],
            "respuestas_referencia": [
                "Idea central: como mostró Pablo en el Areópago, la fe puede dialogar con la razón. Aplicación: no tener miedo de pensar con argumentos mi propia fe.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una pregunta razonable que te hayas hecho sobre tu fe."],
})

_agregar("C0N3-CO03", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: fe pensada, no ciega",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) titulado «Mi fe también piensa», mostrando a un joven que sostiene su fe con argumentos razonables. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["FE", "RAZON", "ARGUMENTO", "PENSAR", "DIALOGO"],
            "respuestas_referencia": [
                "Escena 1: alguien recibe una pregunta difícil sobre su fe. Escena 2: se prepara e investiga con calma. Escena 3: responde con un argumento razonable y respetuoso.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una pregunta típica que alguien podría hacerle a un joven creyente."],
})

_agregar("C0N3-CO03", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: fe y razón",
    "items": [
        {
            "texto": "Completa: Pablo citó a poetas griegos para decir que «en Dios vivimos, nos movemos, y ______».",
            "respuesta": "SOMOS",
            "banco": ["SOMOS", "CREEMOS", "PENSAMOS"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué pregunta de la ciencia o de la razón te gustaría poder relacionar mejor con tu fe? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la frase que Pablo cita de los poetas griegos en Hechos 17,28."],
})

_agregar("C0N3-CO03", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: sostener mi fe con argumentos",
    "situacion": "Pablo mostró que la fe puede dialogar con la razón, sin miedo a pensar ni a argumentar con respeto.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para sostener tu fe con más argumentos, no solo con costumbre?",
            "opciones": [
                "Investigar más sobre una pregunta de fe que tengo pendiente",
                "Hablar con mi catequista sobre cómo la fe y la razón se relacionan",
                "Prepararme para poder explicar con calma por qué creo lo que creo",
                "Evitar pensar en preguntas difíciles sobre mi fe",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un paso concreto para entender mejor tu propia fe.",
               "Descarta la única opción que evita pensar en el tema."],
    "feedback_ok": "¡Muy bien! Una fe que también piensa y argumenta es una fe más firme y madura.",
})

# --- C0N3-CO04 — Dios cercano al ser humano ---------------------------------
_agregar("C0N3-CO04", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: un Dios cercano",
    "items": [
        {"texto": "Título que Pablo da a Dios: quien hizo el mundo y todo lo que hay en él.", "respuesta": "CREADOR"},
        {"texto": "Cualidad de Dios que Pablo destaca: no está lejos de cada uno de nosotros.", "respuesta": "CERCANIA"},
        {"texto": "Lo que Dios da a todos, junto con la vida y todas las cosas.", "respuesta": "ALIENTO"},
        {"texto": "Acción de intentar encontrar algo, como cuando se palpa en la oscuridad.", "respuesta": "BUSCAR"},
        {"texto": "Lo que hacemos cuando tratamos de tocar o alcanzar algo sin verlo del todo.", "respuesta": "PALPAR"},
        {"texto": "Relación de necesitar de otro para vivir, como toda la humanidad depende de Dios.", "respuesta": "DEPENDENCIA"},
        {"texto": "Palabra que describe a toda la familia humana, de un mismo origen según Pablo.", "respuesta": "HUMANIDAD"},
        {"texto": "Tipo de templo que Dios no necesita, según Pablo, porque no vive en edificios.", "respuesta": "HECHOPORMANOS"},
    ],
    "incluir": ["CREADOR", "CERCANIA"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con el discurso de Pablo sobre Dios en Hechos 17,24-28.",
               "CREADOR y CERCANIA son las palabras centrales: empieza por esas."],
})

_agregar("C0N3-CO04", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: un Dios cercano",
    "palabras": ["CREADOR", "CERCANIA", "ALIENTO", "BUSCAR", "PALPAR", "DEPENDENCIA", "HUMANIDAD", "TRASCENDENTE"],
    "incluir": ["CREADOR", "CERCANIA"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: ALIENTO y BUSCAR.",
               "Las ocho palabras son casi las mismas del crucigrama, salvo una que se cambió por TRASCENDENTE."],
})

_agregar("C0N3-CO04", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Hechos 17,24-28",
    "items": [
        {
            "texto": "Busca en tu Biblia Hechos 17,24 y completa: el Dios que hizo el mundo y todo lo que hay en él... no habita en templos hechos por manos ______.",
            "respuesta": "HUMANAS",
            "banco": ["HUMANAS", "SAGRADAS", "ANTIGUAS"],
        },
        {
            "texto": "Hechos 17,27 dice que Dios «no está lejos de cada uno de nosotros». ¿En qué momento de tu semana sentiste, aunque fuera un poco, esa cercanía de Dios?",
            "abierta": True,
            "palabras_esperadas": ["CERCANIA", "DIOS", "SENTIR", "PRESENCIA", "BUSCAR"],
            "respuestas_referencia": [
                "Sentí esa cercanía en un momento de oración tranquila, o al ayudar a alguien y sentir que no estaba solo.",
                "La sentí al notar algo bueno en mi día y pensar que Dios estaba presente en ese detalle.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el libro de los Hechos de los Apóstoles, capítulo 17, versículo 24.",
               "La palabra que falta describe que Dios no vive en construcciones hechas por personas."],
})

_agregar("C0N3-CO04", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: Dios, creador y cercano",
    "items": [
        {"texto": "Ese mismo Dios no está lejos de cada uno de nosotros, aunque no siempre lo notemos.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Dios crea el mundo y todo lo que existe en él.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Dios sostiene la vida, dando a todos aliento y todas las cosas.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Dios determina los tiempos y los lugares donde vive la humanidad.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué es importante recordar que Dios sostiene la vida (paso 2), y no solo que la creó al principio?",
            "abierta": True,
            "palabras_esperadas": ["SOSTENER", "CERCANIA", "DEPENDER", "VIDA", "CADA DIA"],
            "respuestas_referencia": [
                "Porque muestra que Dios no solo creó el mundo una vez, sino que sigue cerca y sosteniendo la vida cada día.",
                "Porque ayuda a ver a Dios no como algo lejano del pasado, sino presente en lo que vivo hoy.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de la creación, al sostenimiento de la vida, a los tiempos y lugares, y por último a la cercanía.",
               "Pablo no separa a Dios creador de un Dios cercano: son el mismo."],
})

_agregar("C0N3-CO04", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "Según Pablo, Dios necesita templos hechos por manos humanas para poder vivir.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dios da a todos vida, aliento y todas las cosas, según Hechos 17,25.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Para Pablo, Dios está muy lejos de cada persona y es casi imposible acercarse a él.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Pablo enseña que toda la humanidad viene de un mismo origen creado por Dios.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["DIOS", "CERCANIA", "CREADOR", "NECESITAR", "DEPENDER"],
            "respuestas_referencia": [
                "Es falsa porque Pablo dice que Dios no necesita nada de las manos humanas, ya que él es quien da la vida.",
                "Es falsa porque Pablo insiste en que Dios no está lejos de nosotros, sino cerca de cada persona.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en qué dice Pablo sobre si Dios necesita algo de las personas.",
               "Recuerda la frase de Hechos 17,27 sobre la cercanía de Dios."],
})

_agregar("C0N3-CO04", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: sentir a Dios cerca",
    "items": [
        {
            "texto": "Caso 1: Renata siente que Dios está muy lejos de su vida diaria y solo lo piensa los domingos. ¿Qué le ayudaría a reconocer su cercanía?",
            "respuesta": "Buscar momentos cotidianos para notar la presencia de Dios, no solo en la misa",
            "banco": ["Buscar momentos cotidianos para notar la presencia de Dios, no solo en la misa", "Aceptar que Dios solo importa un día a la semana", "Dejar de pensar en Dios durante la semana"],
        },
        {
            "texto": "Caso 2: Joaquín piensa que Dios necesita templos grandes y lujosos para estar presente. ¿Qué le ayudaría a pensarlo distinto, según Pablo?",
            "respuesta": "Recordar que Dios no depende de edificios, sino que está presente en toda la creación",
            "banco": ["Recordar que Dios no depende de edificios, sino que está presente en toda la creación", "Insistir en que sin templos grandes Dios no puede actuar", "Creer que solo en lugares lujosos se puede encontrar a Dios"],
        },
        {
            "texto": "Caso 3: Abril se pregunta cómo «palpar» o notar a un Dios que no puede ver. ¿Qué actitud le ayudaría más?",
            "respuesta": "Prestar atención a los signos de vida, bondad y cercanía en su día a día",
            "banco": ["Prestar atención a los signos de vida, bondad y cercanía en su día a día", "Dejar de buscar a Dios porque no se puede ver", "Esperar una señal enorme y dramática para creer que existe"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja mejor la enseñanza de Pablo sobre un Dios cercano.",
            "abierta": True,
            "palabras_esperadas": ["CERCANIA", "DIOS", "BUSCAR", "PRESENCIA", "COTIDIANO"],
            "respuestas_referencia": [
                "Elegí el caso de Renata, porque buscar a Dios en lo cotidiano, y no solo un día a la semana, ayuda a sentir su cercanía real.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre busca reconocer a Dios cerca, en lo cotidiano, no lejos ni encerrado en un edificio.",
               "Pablo insiste en que Dios no necesita nada material de nosotros."],
})

_agregar("C0N3-CO04", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: un Dios que no está lejos",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Un Dios que no está lejos de mí». Incluye una idea central, una referencia a Hechos 17,24-28 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["DIOS", "CERCANIA", "CREADOR", "PRESENCIA", "VIDA"],
            "respuestas_referencia": [
                "Idea central: como dice Pablo, Dios no está lejos de nosotros, sino que sostiene nuestra vida día a día. Aplicación: buscar momentos concretos de la semana para notar esa cercanía.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un momento reciente en el que hayas sentido, aunque sea un poco, la cercanía de Dios."],
})

_agregar("C0N3-CO04", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: señales de cercanía",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) mostrando a un joven que descubre señales de la cercanía de Dios en su día a día. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["DIOS", "CERCANIA", "COTIDIANO", "PRESENCIA", "DESCUBRIR"],
            "respuestas_referencia": [
                "Escena 1: un joven piensa que Dios está lejos. Escena 2: nota un gesto de bondad o un momento de calma. Escena 3: reconoce ahí una señal de la cercanía de Dios.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en pequeñas señales cotidianas donde alguien podría reconocer a Dios cerca."],
})

_agregar("C0N3-CO04", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: un Dios cercano",
    "items": [
        {
            "texto": "Completa: según Hechos 17,27, Dios no está ______ de cada uno de nosotros.",
            "respuesta": "LEJOS",
            "banco": ["LEJOS", "CERCA", "AUSENTE"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿En qué momento concreto de esta semana podrías buscar y reconocer la cercanía de Dios? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la frase de Pablo sobre la distancia entre Dios y cada persona."],
})

_agregar("C0N3-CO04", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: reconocer a Dios cerca",
    "situacion": "Pablo enseña que Dios no está lejos de nosotros: nos da vida, aliento y sostiene cada día nuestra existencia.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para reconocer mejor la cercanía de Dios en tu vida diaria?",
            "opciones": [
                "Dedicar un momento del día a agradecer por la vida y lo que tengo",
                "Prestar atención a los gestos de bondad que veo a mi alrededor",
                "Hacer una pausa breve para notar la presencia de Dios, no solo el domingo",
                "Pensar que solo en un templo se puede encontrar a Dios",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una acción cotidiana y concreta, no en una idea abstracta.",
               "Descarta la única opción que limita a Dios a un solo lugar."],
    "feedback_ok": "¡Muy bien! Reconocer a Dios cerca, cada día, fortalece tu fe como la de los primeros creyentes.",
})


# --- C0N3-CO05 — Responder a preguntas difíciles ----------------------------
_agregar("C0N3-CO05", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: preguntas difíciles",
    "items": [
        {"texto": "Reacción de burla que algunos atenienses tuvieron al escuchar sobre la resurrección.", "respuesta": "BURLA"},
        {"texto": "Actitud de mantener la calma frente a una reacción negativa o una burla.", "respuesta": "PACIENCIA"},
        {"texto": "Enseñanza de Pablo que causó más sorpresa entre los griegos: la vida después de la muerte.", "respuesta": "RESURRECCION"},
        {"texto": "Palabra con la que algunos atenienses llamaron a Pablo, con cierto desprecio, antes de escucharlo.", "respuesta": "PALABRERO"},
        {"texto": "Acción de sostener una idea con razones claras y ordenadas.", "respuesta": "ARGUMENTAR"},
        {"texto": "Tema difícil de responder que muchas personas jóvenes se preguntan: por qué existe el dolor.", "respuesta": "SUFRIMIENTO"},
        {"texto": "Lo que muchas preguntas difíciles buscan encontrar en la vida: un propósito, un para qué.", "respuesta": "SENTIDO"},
        {"texto": "Actitud de tomar en serio al otro aunque piense distinto, sin burlarse de él.", "respuesta": "RESPETO"},
    ],
    "incluir": ["BURLA", "PACIENCIA"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con cómo Pablo enfrenta las reacciones difíciles en Atenas.",
               "BURLA y PACIENCIA son las palabras centrales: empieza por esas."],
})

_agregar("C0N3-CO05", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: preguntas difíciles",
    "palabras": ["BURLA", "PACIENCIA", "RESURRECCION", "PALABRERO", "ARGUMENTAR", "SUFRIMIENTO", "SENTIDO", "RESPETO"],
    "incluir": ["BURLA", "PACIENCIA"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: BURLA y SENTIDO.",
               "Las ocho palabras son las mismas del crucigrama de esta actividad."],
})

_agregar("C0N3-CO05", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Hechos 17,18.32",
    "items": [
        {
            "texto": "Busca en tu Biblia Hechos 17,32 y completa: cuando oyeron lo de la resurrección de los muertos, unos se burlaban, y otros decían: ya te oiremos acerca de esto otra ______.",
            "respuesta": "VEZ",
            "banco": ["VEZ", "NOCHE", "SEMANA"],
        },
        {
            "texto": "¿Cómo reaccionarías si alguien se burlara de algo que crees firmemente sobre tu fe? ¿Con enojo, con indiferencia, o intentando explicarlo con calma?",
            "abierta": True,
            "palabras_esperadas": ["CALMA", "PACIENCIA", "EXPLICAR", "RESPETO", "REACCIONAR"],
            "respuestas_referencia": [
                "Trataría de mantener la calma y explicar con respeto lo que creo, sin enojarme ni burlarme yo también.",
                "Me costaría no molestarme, pero intentaría responder con paciencia, como parece que hizo Pablo.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca el libro de los Hechos, capítulo 17, versículo 32.",
               "La palabra que falta indica que algunos posponían la conversación para otro momento."],
})

_agregar("C0N3-CO05", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: responder con calma",
    "items": [
        {"texto": "Se acepta que no todos van a estar de acuerdo, y eso también está bien.", "respuesta": "5", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Alguien hace una pregunta difícil o incluso se burla de un tema de fe.", "respuesta": "1", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Se respira y se evita responder con enojo o a la defensiva.", "respuesta": "2", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Se intenta comprender qué hay detrás de esa pregunta o esa burla.", "respuesta": "3", "banco": ["1", "2", "3", "4", "5"]},
        {"texto": "Se responde con argumentos claros y con respeto, sin imponer.", "respuesta": "4", "banco": ["1", "2", "3", "4", "5"]},
        {
            "texto": "Justifica: ¿por qué aceptar que no todos van a creer (paso 5) no significa fracasar en la conversación?",
            "abierta": True,
            "palabras_esperadas": ["RESPETO", "LIBERTAD", "ACEPTAR", "SEMBRAR", "PACIENCIA"],
            "respuestas_referencia": [
                "Porque cada persona es libre de creer o no, y el objetivo es sembrar con respeto, no obligar a nadie a aceptar.",
                "Porque, como en Atenas, algunos creyeron y otros no; lo importante fue hablar con honestidad y respeto.",
            ],
        },
    ],
    "requisito": 5,
    "pistas": ["El proceso va de la pregunta o burla, a mantener la calma, a comprender, a responder, y a aceptar el resultado.",
               "No todas las conversaciones sobre fe terminan en que la otra persona esté de acuerdo."],
})

_agregar("C0N3-CO05", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "En Atenas, todos los que escucharon a Pablo creyeron de inmediato en la resurrección.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Algunos atenienses se burlaron cuando Pablo habló de la resurrección de los muertos.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Responder con enojo es la mejor forma de defender la fe ante una burla.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Es normal que algunas preguntas sobre la fe, la ciencia o el sufrimiento no tengan una respuesta fácil.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["BURLA", "CALMA", "RESPETO", "ARGUMENTAR", "PACIENCIA"],
            "respuestas_referencia": [
                "Es falsa porque en Atenas no todos creyeron: unos se burlaron y otros quisieron seguir escuchando después.",
                "Es falsa porque responder con calma y argumentos suele ser más útil que responder con enojo.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Piensa en las distintas reacciones que tuvo la gente de Atenas al escuchar a Pablo.",
               "El enojo rara vez ayuda a que una conversación difícil termine bien."],
})

_agregar("C0N3-CO05", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: preguntas incómodas",
    "items": [
        {
            "texto": "Caso 1: Un compañero le pregunta a Bruno por qué Dios permite el sufrimiento si es tan bueno. ¿Qué actitud le conviene más?",
            "respuesta": "Reconocer que es una pregunta difícil y compartir con humildad lo que él piensa y cree",
            "banco": ["Reconocer que es una pregunta difícil y compartir con humildad lo que él piensa y cree", "Responder con enojo porque siente que están atacando su fe", "Evitar cualquier conversación sobre el tema del sufrimiento"],
        },
        {
            "texto": "Caso 2: A Constanza se burlan de ella por creer en algo que «no se puede demostrar científicamente». ¿Qué actitud se parece más a la de Pablo en Atenas?",
            "respuesta": "Mantener la calma y explicar con respeto lo que cree, aunque no todos estén de acuerdo",
            "banco": ["Mantener la calma y explicar con respeto lo que cree, aunque no todos estén de acuerdo", "Dejar de creer para que no se burlen más de ella", "Burlarse también de quienes no creen, para defenderse"],
        },
        {
            "texto": "Caso 3: Iván no sabe cómo responder cuando le preguntan si la ciencia contradice a la Biblia. ¿Qué actitud le ayudaría más?",
            "respuesta": "Investigar con calma y aceptar que no siempre tiene todas las respuestas al instante",
            "banco": ["Investigar con calma y aceptar que no siempre tiene todas las respuestas al instante", "Inventar una respuesta con tal de no quedar mal", "Evitar el tema para siempre por miedo a equivocarse"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja una actitud madura ante una pregunta difícil.",
            "abierta": True,
            "palabras_esperadas": ["CALMA", "RESPETO", "HUMILDAD", "PREGUNTA", "MADUREZ"],
            "respuestas_referencia": [
                "Elegí el caso de Constanza, porque responder con calma y respeto, sin necesitar que todos crean lo mismo, es una actitud madura.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre responde con calma y humildad, nunca con enojo ni evitando el tema para siempre.",
               "No saber una respuesta al instante no es un fracaso: se puede investigar y volver a hablar del tema."],
})

_agregar("C0N3-CO05", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: cuando se burlan de mi fe",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «Cómo respondo cuando se burlan de mi fe». Incluye una idea central, una referencia a Hechos 17,18.32 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["BURLA", "CALMA", "RESPETO", "FE", "PACIENCIA"],
            "respuestas_referencia": [
                "Idea central: como Pablo en Atenas, no todos van a creer lo mismo, y eso no significa que mi fe esté equivocada. Aplicación: responder con calma la próxima vez que se burlen de algo que creo.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una situación real en la que alguien se haya burlado, aunque fuera un poco, de tu fe."],
})

_agregar("C0N3-CO05", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: responder sin pelear",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) sobre un joven al que le hacen una pregunta difícil sobre su fe y responde con calma, sin pelear. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["PREGUNTA", "CALMA", "RESPETO", "RESPONDER", "FE"],
            "respuestas_referencia": [
                "Escena 1: alguien hace una pregunta incómoda sobre la fe. Escena 2: el joven respira y piensa antes de responder. Escena 3: responde con respeto, aunque el otro no quede convencido del todo.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una pregunta difícil típica que un joven podría recibir sobre su fe."],
})

_agregar("C0N3-CO05", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: preguntas difíciles",
    "items": [
        {
            "texto": "Completa: al escuchar sobre la resurrección, algunos atenienses se ______ de Pablo.",
            "respuesta": "BURLARON",
            "banco": ["BURLARON", "ALEGRARON", "ASUSTARON"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿Qué pregunta difícil te gustaría aprender a responder con más calma y seguridad? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la reacción que tuvo parte del público de Pablo al escuchar sobre la resurrección."],
})

_agregar("C0N3-CO05", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: responder con calma",
    "situacion": "Como Pablo en Atenas, es normal encontrarse con burlas o preguntas difíciles al hablar de la fe: lo importante es responder con calma y respeto.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú la próxima vez que te hagan una pregunta difícil o se burlen de tu fe?",
            "opciones": [
                "Respirar y evitar responder con enojo",
                "Escuchar con atención qué hay detrás de la pregunta o la burla",
                "Responder con respeto, aunque no tenga todas las respuestas",
                "Dejar de creer para evitar cualquier burla",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una reacción concreta y tranquila, no en una reacción de enojo.",
               "Descarta la única opción que significa abandonar la fe."],
    "feedback_ok": "¡Muy bien! Responder con calma, como Pablo, fortalece tu fe y tu testimonio.",
})


# --- C0N3-CO06 — Dar razón de la esperanza ----------------------------------
_agregar("C0N3-CO06", "A01", {
    "tipo": "crucigrama",
    "titulo": "Crucigrama: dar razón de la esperanza",
    "items": [
        {"texto": "Confianza firme en que Dios cumple sus promesas, aun sin verlas del todo cumplidas.", "respuesta": "ESPERANZA"},
        {"texto": "Actitud con la que, según 1 Pedro 3,15, hay que responder sobre la propia fe.", "respuesta": "MANSEDUMBRE"},
        {"texto": "Mostrar con la propia vida y palabras aquello en lo que se cree.", "respuesta": "TESTIMONIO"},
        {"texto": "Cambio de vida al que Pablo invita a los atenienses en Hechos 17,30.", "respuesta": "CONVERSION"},
        {"texto": "Nombre de uno de los que creyeron a Pablo en Atenas: Dionisio el...", "respuesta": "AREOPAGITA"},
        {"texto": "Resultado bueno que se espera de una conversación de fe, aunque no dependa solo de nosotros.", "respuesta": "FRUTO"},
        {"texto": "Cualidad de vivir de acuerdo con lo que se cree y se anuncia.", "respuesta": "COHERENCIA"},
        {"texto": "Tarea de anunciar la fe a los demás, con palabras y con la vida.", "respuesta": "MISION"},
    ],
    "incluir": ["ESPERANZA", "MANSEDUMBRE"],
    "requisito": 6,
    "pistas": ["Todas las palabras tienen que ver con dar testimonio de la fe, según Hechos 17,30-34 y 1 Pedro 3,15.",
               "ESPERANZA y MANSEDUMBRE son las palabras centrales: empieza por esas."],
})

_agregar("C0N3-CO06", "A02", {
    "tipo": "sopa_letras",
    "titulo": "Sopa de letras: dar razón de la esperanza",
    "palabras": ["ESPERANZA", "MANSEDUMBRE", "TESTIMONIO", "CONVERSION", "FRUTO", "COHERENCIA", "MISION", "DAMARIS"],
    "incluir": ["ESPERANZA", "MANSEDUMBRE"],
    "requisito": 6,
    "pistas": ["Busca primero las palabras más cortas: FRUTO y MISION.",
               "Las ocho palabras son casi las mismas del crucigrama, salvo una que se cambió por DAMARIS."],
})

_agregar("C0N3-CO06", "A03", {
    "tipo": "completar",
    "titulo": "Práctica con la Biblia: Hechos 17,32-34 y 1 Pedro 3,15",
    "items": [
        {
            "texto": "Busca en tu Biblia 1 Pedro 3,15 y completa: estad siempre preparados para presentar defensa... ante todo el que os demande razón de la ______ que hay en vosotros.",
            "respuesta": "ESPERANZA",
            "banco": ["ESPERANZA", "FE", "PACIENCIA"],
        },
        {
            "texto": "Hechos 17,34 dice que, aunque muchos se burlaron o dudaron, algunos creyeron. ¿Qué te enseña ese final sobre hablar de tu fe con otros, incluso si no todos van a creer?",
            "abierta": True,
            "palabras_esperadas": ["FRUTO", "ESPERANZA", "RESPETO", "SEMBRAR", "RESULTADO"],
            "respuestas_referencia": [
                "Me enseña que no depende de mí que todos crean; mi tarea es compartir mi fe con respeto y confiar en el fruto.",
                "Que hablar de la fe vale la pena aunque solo algunas personas respondan bien, como pasó con Pablo en Atenas.",
            ],
        },
    ],
    "requisito": 2,
    "pistas": ["Busca la primera carta de Pedro, capítulo 3, versículo 15.",
               "La palabra que falta es también el título de esta actividad."],
})

_agregar("C0N3-CO06", "A04", {
    "tipo": "completar",
    "titulo": "Ordenar y reconstruir: dar razón de mi esperanza",
    "items": [
        {"texto": "Se confía en que el resultado de esa conversación no depende solo de uno mismo.", "respuesta": "4", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se busca vivir de manera coherente con lo que se cree, como primer testimonio.", "respuesta": "1", "banco": ["1", "2", "3", "4"]},
        {"texto": "Alguien pregunta, con curiosidad o incluso con desconfianza, por esa esperanza.", "respuesta": "2", "banco": ["1", "2", "3", "4"]},
        {"texto": "Se responde con mansedumbre y respeto, sin imponer ni agredir.", "respuesta": "3", "banco": ["1", "2", "3", "4"]},
        {
            "texto": "Justifica: ¿por qué vivir con coherencia (paso 1) es un paso necesario antes de poder dar razón de la esperanza con palabras?",
            "abierta": True,
            "palabras_esperadas": ["COHERENCIA", "TESTIMONIO", "VIDA", "EJEMPLO", "CREIBLE"],
            "respuestas_referencia": [
                "Porque las palabras sobre la fe son más creíbles cuando van acompañadas de una vida coherente con lo que se dice creer.",
                "Porque el testimonio de vida es la primera forma de dar razón de la esperanza, antes incluso de hablar.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["El proceso va de vivir con coherencia, a que alguien pregunte, a responder con mansedumbre, a confiar en el fruto.",
               "1 Pedro 3,15 no solo pide responder, sino hacerlo con mansedumbre y reverencia."],
})

_agregar("C0N3-CO06", "A05", {
    "tipo": "completar",
    "titulo": "Verdadero o falso, justificado",
    "items": [
        {"texto": "1 Pedro 3,15 pide responder sobre la propia esperanza con mansedumbre y respeto.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "En Atenas, absolutamente nadie creyó jamás en el mensaje de Pablo.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dar razón de la esperanza significa imponer la fe a los demás sin escucharlos.", "respuesta": "FALSO", "banco": ["VERDADERO", "FALSO"]},
        {"texto": "Dionisio el areopagita y Dámaris fueron algunas de las personas que creyeron en Atenas.", "respuesta": "VERDADERO", "banco": ["VERDADERO", "FALSO"]},
        {
            "texto": "Elige una de las afirmaciones falsas y explica por qué lo es.",
            "abierta": True,
            "palabras_esperadas": ["ESPERANZA", "TESTIMONIO", "RESPETO", "IMPONER", "MANSEDUMBRE"],
            "respuestas_referencia": [
                "Es falsa porque en Atenas algunas personas sí creyeron, como Dionisio el areopagita y Dámaris.",
                "Es falsa porque dar razón de la esperanza se hace con mansedumbre y respeto, no imponiendo nada a nadie.",
            ],
        },
    ],
    "requisito": 4,
    "pistas": ["Recuerda cómo terminó el discurso de Pablo en el Areópago: no todos rechazaron su mensaje.",
               "1 Pedro 3,15 habla de mansedumbre, que es lo contrario de imponer con fuerza."],
})

_agregar("C0N3-CO06", "A06", {
    "tipo": "completar",
    "titulo": "Caso juvenil: mi testimonio de esperanza",
    "items": [
        {
            "texto": "Caso 1: Un amigo le pregunta a Lucas por qué sigue yendo a misa si «total, nadie lo obliga». ¿Qué respuesta refleja mejor 1 Pedro 3,15?",
            "respuesta": "Explicar con calma y respeto por qué su fe le da sentido y esperanza",
            "banco": ["Explicar con calma y respeto por qué su fe le da sentido y esperanza", "Responder con fastidio que no es asunto de nadie más", "Inventar una excusa para no hablar del tema"],
        },
        {
            "texto": "Caso 2: Antonella quiere compartir su fe con una prima sin hacerla sentir juzgada. ¿Qué actitud le conviene, inspirada en Pablo y en 1 Pedro?",
            "respuesta": "Compartir su experiencia de fe con mansedumbre, sin imponerla ni presionar",
            "banco": ["Compartir su experiencia de fe con mansedumbre, sin imponerla ni presionar", "Insistir hasta que su prima piense igual que ella", "No decir nunca nada sobre su fe, por miedo a incomodar"],
        },
        {
            "texto": "Caso 3: Santiago siente que, aunque explique bien su fe, algunas personas nunca la van a aceptar. ¿Qué actitud le ayudaría, como a Pablo en Atenas?",
            "respuesta": "Confiar en que el fruto no depende solo de él, y seguir dando testimonio con coherencia",
            "banco": ["Confiar en que el fruto no depende solo de él, y seguir dando testimonio con coherencia", "Dejar de vivir su fe porque algunos no la van a aceptar", "Enojarse con quienes no creen lo mismo que él"],
        },
        {
            "texto": "Elige uno de los tres casos y justifica por qué esa opción refleja bien dar razón de la esperanza con mansedumbre.",
            "abierta": True,
            "palabras_esperadas": ["ESPERANZA", "MANSEDUMBRE", "TESTIMONIO", "RESPETO", "FRUTO"],
            "respuestas_referencia": [
                "Elegí el caso de Antonella, porque compartir la fe con mansedumbre, sin imponerla, es justo lo que pide 1 Pedro 3,15.",
            ],
        },
    ],
    "requisito": 3,
    "pistas": ["La opción correcta siempre responde con respeto y mansedumbre, sin imponer ni evitar el tema por completo.",
               "El fruto de una conversación de fe no depende solo de la persona que la comparte."],
})

_agregar("C0N3-CO06", "A07", {
    "tipo": "completar",
    "titulo": "Podcast juvenil: mi razón de esperanza",
    "items": [
        {
            "texto": "Escribe el guion de un podcast de 2 a 3 minutos: «La razón de mi esperanza». Incluye una idea central, una referencia a Hechos 17,32-34 o 1 Pedro 3,15 y una aplicación a tu vida.",
            "abierta": True,
            "palabras_esperadas": ["ESPERANZA", "TESTIMONIO", "MANSEDUMBRE", "FE", "COMPARTIR"],
            "respuestas_referencia": [
                "Idea central: como pide 1 Pedro 3,15, quiero estar preparado para dar razón de mi esperanza con mansedumbre. Aplicación: compartir con un amigo, con respeto, una razón concreta por la que tengo fe.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una razón concreta y personal por la que tienes esperanza en tu fe."],
})

_agregar("C0N3-CO06", "A08", {
    "tipo": "completar",
    "titulo": "Creación digital responsable: testigos de esperanza",
    "items": [
        {
            "texto": "Escribe el guion de un storyboard breve (3 escenas) titulado «Mi razón de esperanza», mostrando a un joven que comparte su fe con mansedumbre. No hace falta publicarlo.",
            "abierta": True,
            "palabras_esperadas": ["ESPERANZA", "TESTIMONIO", "MANSEDUMBRE", "COMPARTIR", "FE"],
            "respuestas_referencia": [
                "Escena 1: alguien pregunta por qué el joven tiene esperanza. Escena 2: él responde con calma y respeto. Escena 3: la conversación deja una semilla, aunque no haya una respuesta inmediata.",
            ],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en una conversación real, o posible, donde alguien te pregunte por tu esperanza."],
})

_agregar("C0N3-CO06", "A09", {
    "tipo": "recuperacion",
    "titulo": "Recuperación: dar razón de la esperanza",
    "items": [
        {
            "texto": "Completa: 1 Pedro 3,15 pide estar preparados para dar razón de la esperanza con ______ y reverencia.",
            "respuesta": "MANSEDUMBRE",
            "banco": ["MANSEDUMBRE", "FUERZA", "AUTORIDAD"],
        },
    ],
    "requisito": 1,
    "reflexion": "¿A quién te gustaría contarle, con mansedumbre y respeto, una razón de tu esperanza? Coméntalo con tu catequista.",
    "pistas": ["Piensa en la actitud que pide 1 Pedro 3,15 para responder sobre la fe."],
})

_agregar("C0N3-CO06", "A10", {
    "tipo": "aplicacion",
    "titulo": "Aplicación y misión: testigo de esperanza",
    "situacion": "Como los primeros creyentes de Atenas, estás llamado a dar razón de tu esperanza con mansedumbre, sin imponerla, confiando en el fruto que Dios da.",
    "items": [
        {
            "texto": "¿Qué puedes hacer tú esta semana para dar razón de tu esperanza, sin imponerla a nadie?",
            "opciones": [
                "Vivir con coherencia lo que digo creer, como primer testimonio",
                "Compartir con respeto una razón concreta de mi fe si alguien pregunta",
                "Escuchar antes de responder, con mansedumbre",
                "Evitar por completo hablar de mi fe para no incomodar a nadie",
            ],
            "correctas": [0, 1, 2],
        },
    ],
    "requisito": 1,
    "pistas": ["Piensa en un gesto concreto de testimonio o de palabra, no en evitar el tema.",
               "Descarta la única opción que significa quedarse en silencio siempre."],
    "feedback_ok": "¡Muy bien! Dar razón de tu esperanza, con mansedumbre, es una hermosa forma de vivir tu fe.",
})

# ==========================================================================
# Los bloques de contenido (C0N1, C0N2, C0N3) se agregan más abajo.
# ==========================================================================


def actividades_de_contenido(contenido_id):
    return [aid for aid, a in ACTIVIDADES.items() if a["contenido_id"] == contenido_id]


def contenido_de(contenido_id):
    return next((c for c in CONTENIDOS if c["id"] == contenido_id), None)


def encuentro_de(encuentro_id):
    return next((e for e in ENCUENTROS if e["id"] == encuentro_id), None)


def contenidos_de_encuentro(encuentro_id):
    """Los contenidos cuyo id empieza por «<encuentro_id>-», en el orden en
    que aparecen en CONTENIDOS (ej.: 'C0N2' -> los 6 contenidos C0N2-CO01
    a C0N2-CO06)."""
    return [c for c in CONTENIDOS if c["id"].split("-")[0] == encuentro_id]


def siguiente_contenido_de(contenido_id):
    """Contenido que sigue en el orden general (cruza de un tema al
    siguiente), o None si es el último de todos — usado para invitar a
    continuar apenas se completa un tema, y para saber cuándo se terminó
    todo este primer prototipo (C0N3-CO06)."""
    for i, c in enumerate(CONTENIDOS):
        if c["id"] == contenido_id:
            return CONTENIDOS[i + 1] if i + 1 < len(CONTENIDOS) else None
    return None


def anterior_contenido_de(contenido_id):
    """Contenido inmediatamente anterior en el orden general (CONTENIDOS
    recorre los temas en orden, así que esto también cruza de un tema al
    anterior), o None si es el primero de todos (C0N1-CO01). Se usa para
    exigir que ese contenido esté completo antes de desbloquear este — el
    itinerario se recorre en un único orden lineal, sin poder saltar
    contenidos ni temas."""
    for i, c in enumerate(CONTENIDOS):
        if c["id"] == contenido_id:
            return CONTENIDOS[i - 1] if i > 0 else None
    return None
