import cv2 as cv
import numpy as np

# 1. Cargar imagen
img = cv.imread('images/cats.png')
alto, ancho = img.shape[:2]

# Variables de estado
tx, ty = 0, 0
cx, cy = ancho // 2, alto // 2
arrastrando = False
rx_ini, ry_ini = 0, 0

def raton(evento, x, y, flags, param):
    global tx, ty, cx, cy, arrastrando, rx_ini, ry_ini

    # Arrastrar con botón izquierdo -> Traslación
    if evento == cv.EVENT_LBUTTONDOWN:
        arrastrando, rx_ini, ry_ini = True, x - tx, y - ty
    elif evento == cv.EVENT_MOUSEMOVE and arrastrando:
        tx, ty = x - rx_ini, y - ry_ini
    elif evento == cv.EVENT_LBUTTONUP:
        arrastrando = False

    # Botón derecho -> Centro de giro y escalado
    elif evento == cv.EVENT_RBUTTONDOWN:
        cx, cy = x, y

cv.namedWindow('Optativo Raton')
cv.setMouseCallback('Optativo Raton', raton)
cv.createTrackbar('Angulo', 'Optativo Raton', 0, 360, lambda x: None)
cv.createTrackbar('Escala (%)', 'Optativo Raton', 100, 300, lambda x: None)

while True:
    angulo = cv.getTrackbarPos('Angulo', 'Optativo Raton')
    escala = max(cv.getTrackbarPos('Escala (%)', 'Optativo Raton') / 100.0, 0.01)

    # Matriz afín: Rotación + Escala alrededor de (cx, cy)
    M = cv.getRotationMatrix2D((cx, cy), angulo, escala)
    # Sumar traslación (tx, ty)
    M[0, 2] += tx
    M[1, 2] += ty

    resultado = cv.warpAffine(img, M, (ancho, alto))
    # Dibujar centro marcado
    cv.circle(resultado, (cx, cy), 5, (0, 0, 255), -1)

    cv.imshow('Optativo Raton', resultado)
    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()
