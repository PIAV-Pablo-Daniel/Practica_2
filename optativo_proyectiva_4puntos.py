"""
optativo_proyectiva_4puntos.py - Optativo 6: transformación proyectiva con 4 puntos
===================================================================================
Se marcan 4 puntos en 'Origen' y 4 en 'Destino' (en el mismo orden). La
homografía 3x3 tiene 8 grados de libertad (está definida salvo escala),
así que hacen falta 4 parejas de puntos = 8 ecuaciones.

Teclas: r borrar los puntos · ESC salir
"""
import cv2 as cv
import numpy as np

import geometria as geo

N = 4
img1 = geo.cargar_imagen('images/cats.png')
img2 = geo.cargar_imagen('images/eii.png')
p1, p2 = [], []


def click_origen(evento, x, y, flags, param):
    if evento == cv.EVENT_LBUTTONDOWN and len(p1) < N:
        p1.append((x, y))


def click_destino(evento, x, y, flags, param):
    if evento == cv.EVENT_LBUTTONDOWN and len(p2) < N:
        p2.append((x, y))


def dibujar_puntos(img, puntos, color):
    v = img.copy()
    for i, p in enumerate(puntos):
        cv.circle(v, p, 5, color, -1)
        cv.putText(v, str(i + 1), (p[0] + 8, p[1] - 8), cv.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)
    return v


cv.namedWindow('Origen')
cv.setMouseCallback('Origen', click_origen)
cv.namedWindow('Destino')
cv.setMouseCallback('Destino', click_destino)

while True:
    cv.imshow('Origen', dibujar_puntos(img1, p1, (0, 0, 255)))
    cv.imshow('Destino', dibujar_puntos(img2, p2, (255, 0, 0)))

    # Con 4 puntos en cada imagen se calcula la homografía
    if len(p1) == N and len(p2) == N:
        H = cv.getPerspectiveTransform(np.float32(p1), np.float32(p2))   # matriz 3x3
        res = cv.warpPerspective(img1, H, (img2.shape[1], img2.shape[0]))
        cv.imshow('Resultado Proyectivo', res)

    tecla = cv.waitKey(20) & 0xFF
    if tecla == 27:
        break
    elif tecla == ord('r'):
        p1.clear()
        p2.clear()

cv.destroyAllWindows()
