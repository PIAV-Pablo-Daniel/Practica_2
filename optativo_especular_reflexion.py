import cv2 as cv
import numpy as np

img = cv.imread('images/cats.png')
alto, ancho = img.shape[:2]
pts = []

def raton(evento, x, y, flags, param):
    if evento == cv.EVENT_LBUTTONDOWN:
        pts.append((x, y))
        if len(pts) > 2:
            pts.pop(0)

cv.namedWindow('Reflexion Recta')
cv.setMouseCallback('Reflexion Recta', raton)

# 1. Imagen especular (efecto espejo horizontal)
cv.imshow('Especular (cv.flip)', cv.flip(img, 1))

while True:
    vista = img.copy()

    # Si hay 2 puntos, reflejar respecto a la recta que los une
    if len(pts) == 2:
        (x1, y1), (x2, y2) = pts[0], pts[1]
        cv.line(vista, (x1, y1), (x2, y2), (0, 255, 255), 2)

        theta = np.arctan2(y2 - y1, x2 - x1)
        c, s = np.cos(theta), np.sin(theta)

        # Matriz afín: Trasladar -> Rotar -> Reflejar eje X -> Desrotar -> Destrasladar
        T1 = np.array([[1, 0, -x1], [0, 1, -y1], [0, 0, 1]], dtype=np.float32)
        R = np.array([[c, s, 0], [-s, c, 0], [0, 0, 1]], dtype=np.float32)
        RefX = np.array([[1, 0, 0], [0, -1, 0], [0, 0, 1]], dtype=np.float32)
        R_inv = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]], dtype=np.float32)
        T2 = np.array([[1, 0, x1], [0, 1, y1], [0, 0, 1]], dtype=np.float32)

        M = (T2 @ R_inv @ RefX @ R @ T1)[:2, :]
        vista = cv.warpAffine(img, M, (ancho, alto))
        cv.line(vista, (x1, y1), (x2, y2), (0, 255, 255), 2)

    cv.imshow('Reflexion Recta', vista)
    if cv.waitKey(20) & 0xFF == 27:
        break

cv.destroyAllWindows()
