"""
optativo_especular_reflexion.py - Optativos 7 y 8
=================================================
7. Imagen especular con una matriz (da lo mismo que cv.flip(img, 1)).
8. Reflexión respecto a una recta: dos clics marcan la recta (eje de
   reflexión) y la imagen se refleja respecto a ella.

Teclas: r borrar la recta · ESC salir
"""
import cv2 as cv
import numpy as np

import geometria as geo

img = geo.cargar_imagen('images/cats.png')
alto, ancho = img.shape[:2]
pts = []


def raton(evento, x, y, flags, param):
    if evento == cv.EVENT_LBUTTONDOWN:
        pts.append((x, y))
        if len(pts) > 2:     # solo se guardan los 2 últimos clics
            pts.pop(0)


# --- 7. Imagen especular (original | especular) ---
M_esp = geo.especular_horizontal(ancho)
especular = cv.warpAffine(img, M_esp[:2, :], (ancho, alto))
cv.imshow('Especular (original | espejo)', np.hstack([img, especular]))

# --- 8. Reflexión respecto a una recta ---
cv.namedWindow('Reflexion Recta')
cv.setMouseCallback('Reflexion Recta', raton)

while True:
    vista = img.copy()

    if len(pts) == 2:
        M = geo.reflexion_recta(pts[0], pts[1])
        vista = cv.warpAffine(img, M[:2, :], (ancho, alto))
        cv.line(vista, pts[0], pts[1], (0, 255, 255), 2)
    for p in pts:
        cv.circle(vista, p, 5, (0, 0, 255), -1)

    cv.imshow('Reflexion Recta', vista)
    tecla = cv.waitKey(20) & 0xFF
    if tecla == 27:
        break
    elif tecla == ord('r'):
        pts.clear()

cv.destroyAllWindows()
