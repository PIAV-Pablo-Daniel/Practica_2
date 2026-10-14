"""
optativo_raton.py - Optativos 1, 2 y 3 (control con el ratón)
=============================================================
Reutiliza la ventana 1a de main.py y añade el ratón. Con el teclado se
elige qué hace el clic izquierdo:
  t -> Trasladar: arrastrar la imagen (se ve en tiempo real)
  g -> marcar el centro de Giro      (punto rojo)
  e -> marcar el centro de Escalado  (punto azul)

El ratón solo mueve los trackbars; la matriz se calcula con la misma
función procesar_1a de main.py.

Teclas: t / g / e cambiar de modo · ESC salir
"""
import cv2 as cv
import numpy as np

import geometria as geo
import main as obligatorio

WIN = obligatorio.WIN_1A
MODOS = {'t': 'Trasladar (arrastrar)', 'g': 'Centro de giro', 'e': 'Centro de escalado'}

img = geo.cargar_imagen('images/cats.png')
alto, ancho = img.shape[:2]

modo = 't'
arrastrando = False
raton_ini_x, raton_ini_y = 0, 0
tx_ini, ty_ini = 0, 0


def raton(evento, x, y, flags, param):
    global arrastrando, raton_ini_x, raton_ini_y, tx_ini, ty_ini

    if modo == 't':
        if evento == cv.EVENT_LBUTTONDOWN:
            # Guardamos dónde empieza el arrastre y la traslación que había
            arrastrando = True
            raton_ini_x, raton_ini_y = x, y
            tx_ini = cv.getTrackbarPos('Tx', WIN)
            ty_ini = cv.getTrackbarPos('Ty', WIN)
        elif evento == cv.EVENT_MOUSEMOVE and arrastrando:
            # Nueva traslación = la inicial + lo que se ha movido el ratón
            nuevo_tx = int(np.clip(tx_ini + (x - raton_ini_x), 0, ancho * 2))
            nuevo_ty = int(np.clip(ty_ini + (y - raton_ini_y), 0, alto * 2))
            cv.setTrackbarPos('Tx', WIN, nuevo_tx)
            cv.setTrackbarPos('Ty', WIN, nuevo_ty)
        elif evento == cv.EVENT_LBUTTONUP:
            arrastrando = False

    elif modo == 'g' and evento == cv.EVENT_LBUTTONDOWN:
        cv.setTrackbarPos('Giro X', WIN, int(np.clip(x, 0, ancho)))
        cv.setTrackbarPos('Giro Y', WIN, int(np.clip(y, 0, alto)))

    elif modo == 'e' and evento == cv.EVENT_LBUTTONDOWN:
        cv.setTrackbarPos('Escala centro X', WIN, int(np.clip(x, 0, ancho)))
        cv.setTrackbarPos('Escala centro Y', WIN, int(np.clip(y, 0, alto)))


obligatorio.crear_1a(ancho, alto)
cv.setMouseCallback(WIN, raton)

while True:
    res = obligatorio.procesar_1a(img)
    cv.putText(res, f'Modo: {MODOS[modo]}  (t/g/e)', (10, 25),
               cv.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv.imshow(WIN, res)

    tecla = cv.waitKey(20) & 0xFF
    if tecla == 27:
        break
    elif chr(tecla) in MODOS:
        modo = chr(tecla)
        arrastrando = False

cv.destroyAllWindows()
