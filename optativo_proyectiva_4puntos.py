import cv2 as cv
import numpy as np

img1 = cv.imread('images/cats.png')
img2 = cv.imread('images/eii.png')
p1, p2 = [], []

def click_origen(evento, x, y, flags, param):
    if evento == cv.EVENT_LBUTTONDOWN and len(p1) < 4:
        p1.append((x, y))

def click_destino(evento, x, y, flags, param):
    if evento == cv.EVENT_LBUTTONDOWN and len(p2) < 4:
        p2.append((x, y))

cv.namedWindow('Origen'); cv.setMouseCallback('Origen', click_origen)
cv.namedWindow('Destino'); cv.setMouseCallback('Destino', click_destino)

while True:
    v1, v2 = img1.copy(), img2.copy()
    for p in p1: cv.circle(v1, p, 5, (0, 0, 255), -1)
    for p in p2: cv.circle(v2, p, 5, (255, 0, 0), -1)

    cv.imshow('Origen', v1)
    cv.imshow('Destino', v2)

    # Al tener 4 puntos en cada una, calculamos la homografía proyectiva
    if len(p1) == 4 and len(p2) == 4:
        M = cv.getPerspectiveTransform(np.float32(p1), np.float32(p2))
        res = cv.warpPerspective(img1, M, (img2.shape[1], img2.shape[0]))
        cv.imshow('Resultado Proyectivo', res)

    tecla = cv.waitKey(20) & 0xFF
    if tecla == 27: break
    elif tecla == ord('r'): p1.clear(); p2.clear()

cv.destroyAllWindows()
