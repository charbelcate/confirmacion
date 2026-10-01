# Camino a la Confirmación — prototipo C0N1 a C0N3

Prototipo funcional (no de producción) del microservicio de formación y
reforzamiento catequético para el programa de **Confirmación**
(adolescentes y jóvenes, 14-16 años), construido reutilizando **el mismo
motor ya probado** del proyecto de Primera Comunión (`catequesis-pc01-pwa`):
misma API REST en Flask, mismo motor de reforzamiento por intentos, misma
persistencia en SQLite — solo cambian el contenido (`content.py`) y el
frontend (rebrandeado para Confirmación).

## Qué incluye este prototipo

Se entrega **a propósito** solo con los tres primeros temas del programa
completo de 22, para que la formadora los revise antes de continuar con
C0N4 a C0N22 — tal como pide el propio documento fuente en su sección 12
("Propuesta de revisión con el catequista").

- **C0N1 — "Jesús nos llama a seguirlo"** (Marcos 1,16-20 / Mateo
  28,19-20): la vocación, el seguimiento y el discipulado.
- **C0N2 — "Jóvenes en la Biblia"** (1 Samuel 3,1-10 / Lucas 1,26-38):
  Samuel y María como figuras juveniles de escucha y respuesta a la
  llamada de Dios.
- **C0N3 — "Creer en tiempos de duda"** (Hechos 17,16-34): fe, razón,
  cultura y anuncio del Evangelio, a partir del discurso de Pablo en el
  Areópago.

Cada tema tiene 6 contenidos (`C0N<n>-CO01` a `C0N<n>-CO06`) y cada
contenido 10 actividades — **18 contenidos y 180 actividades en total**:
crucigrama, sopa de letras, práctica con la Biblia, ordenar y
reconstruir, verdadero/falso justificado, caso juvenil, podcast
juvenil (guion escrito), creación digital responsable (guion escrito),
recuperación adaptativa y aplicación/misión.

Ver el docstring al comienzo de `backend/content.py` para el detalle
completo de cómo se mapearon las 10 familias de actividad que describe
el documento fuente (genéricas, sin contenido concreto) a los tipos ya
probados del motor de Primera Comunión, y la nota de diseño sobre cómo
se adaptaron las actividades de podcast/Reel (A07/A08) a texto escrito
en vez de audio/video real.

## Qué se probó

- Las 180 actividades quedan **LOGRADO en el primer intento** cuando se
  responden correctamente (regresión automática de extremo a extremo).
- El **bloqueo de avance** (gating) funciona: no se puede responder una
  actividad de un contenido cuyo contenido anterior no está completo.
- La señal `camino_completo` (que dispara la animación de cierre) se
  activa únicamente al terminar la última actividad cargada hasta ahora
  (`C0N3-CO06-A10`) — el texto de esa pantalla deja claro que es el
  cierre del **prototipo**, no del itinerario completo de 22 temas, para
  no confundir a quien lo pruebe.
- Los generadores de crucigrama y sopa de letras arman correctamente el
  tablero para las 180 actividades, sin colisiones de letras.

## Cómo probarlo

```
cd backend
pip install -r requirements.txt
python app.py
```

Luego abre `http://localhost:5000` en el navegador (o en el teléfono, si
está en la misma red, usando la IP de la computadora) y entra con
cualquier código, por ejemplo `LUCIA-G3`.

## Despliegue en producción

Igual que el proyecto de Primera Comunión: incluye `Dockerfile` y
`.dockerignore` listos para subir a un VPS (ver la guía de despliegue ya
entregada para `catequesis-pc01-pwa`, que aplica igual aquí cambiando
solo el nombre del proyecto y del volumen de la base de datos
`catequesis_confirmacion.db`).

## Estructura del proyecto

```
catequesis-confirmacion-pwa/
├── Dockerfile
├── .dockerignore
├── backend/
│   ├── app.py           (API REST — idéntico en lógica al de Primera Comunión)
│   ├── motor.py         (motor de reforzamiento — sin cambios)
│   ├── db.py             (persistencia SQLite — sin cambios, DB propia)
│   ├── nlp_eval.py       (similitud semántica opcional — sin cambios)
│   ├── content.py        (base de conocimiento — C0N1 a C0N3, 180 actividades)
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── manifest.json
    ├── sw.js
    ├── css/style.css
    ├── js/app.js
    └── icons/
```

## Pendiente (según lo conversado)

- Continuar con C0N4 a C0N22 (19 temas, ~190 contenidos, ~1900
  actividades) siguiendo exactamente esta misma arquitectura, una vez
  revisados estos tres primeros temas.
- La escala cualitativa de 7 niveles de mensajes que menciona la sección
  9 del documento fuente **no** se implementó todavía: por ahora se
  reutilizan los mismos mensajes de logro/falta genéricos del proyecto
  de Primera Comunión.
