"""
geometria.py - Funciones comunes de la Práctica 2 (PIAV)
=========================================================
Aquí están TODAS las matrices de transformación. El resto de scripts
importan este módulo, así la parte matemática está en un único sitio.

Convención: matrices 3x3 en coordenadas homogéneas (x, y, 1). Así
componer transformaciones es multiplicar con @ (se aplican de DERECHA
a IZQUIERDA). cv.warpAffine solo necesita las dos primeras filas: M[:2].
"""
import os
import sys

import cv2 as cv
import numpy as np

# Carpeta del proyecto: las rutas funcionan aunque se lance desde otro sitio
CARPETA = os.path.dirname(os.path.abspath(__file__))


def cargar_imagen(ruta):
    img = cv.imread(os.path.join(CARPETA, ruta))
    if img is None:
        sys.exit(f"Error: no se pudo cargar la imagen '{ruta}'.")
    return img


# ---------------------------------------------------------------
# Matrices básicas
# ---------------------------------------------------------------
def traslacion(tx, ty):
    """Mueve todos los puntos (tx, ty) píxeles."""
    return np.array([[1, 0, tx],
                     [0, 1, ty],
                     [0, 0, 1]], dtype=np.float64)


def rotacion(angulo_grados, cx, cy):
    """Rotación alrededor del punto (cx, cy).

    M = T(cx, cy) · R(θ) · T(-cx, -cy)
        (llevar el centro al origen -> girar -> devolverlo a su sitio)

    El eje Y de la imagen va hacia ABAJO, por eso los signos de sin están
    cambiados respecto a la matriz "de libro": así un ángulo positivo gira
    en sentido ANTIHORARIO en pantalla, igual que cv.getRotationMatrix2D.
    """
    t = np.radians(angulo_grados)
    c, s = np.cos(t), np.sin(t)
    R = np.array([[ c, s, 0],
                  [-s, c, 0],
                  [ 0, 0, 1]], dtype=np.float64)
    return traslacion(cx, cy) @ R @ traslacion(-cx, -cy)


def escalado(sx, sy, cx, cy):
    """Escalado con centro en (cx, cy): ese punto no se mueve.
    Uniforme si sx == sy, no uniforme si sx != sy."""
    S = np.array([[sx, 0, 0],
                  [0, sy, 0],
                  [0, 0, 1]], dtype=np.float64)
    return traslacion(cx, cy) @ S @ traslacion(-cx, -cy)


def especular_horizontal(ancho):
    """Imagen especular (espejo izquierda-derecha): x' = (ancho - 1) - x.
    Da exactamente lo mismo que cv.flip(img, 1)."""
    return np.array([[-1, 0, ancho - 1],
                     [ 0, 1, 0],
                     [ 0, 0, 1]], dtype=np.float64)


def reflexion_recta(p1, p2):
    """Reflexión respecto a la recta que pasa por p1 y p2.

    M = T(p1) · R⁻¹ · RefX · R · T(-p1)
      1º llevar p1 al origen
      2º girar para que la recta quede sobre el eje X
      3º reflejar respecto al eje X (y -> -y)
      4º deshacer el giro y 5º deshacer la traslación
    """
    (x1, y1), (x2, y2) = p1, p2
    angulo = np.degrees(np.arctan2(y2 - y1, x2 - x1))
    R = rotacion(angulo, 0, 0)          # lleva la recta al eje X
    RefX = np.array([[1, 0, 0],
                     [0, -1, 0],
                     [0, 0, 1]], dtype=np.float64)
    # La inversa de una rotación es su traspuesta
    return traslacion(x1, y1) @ R.T @ RefX @ R @ traslacion(-x1, -y1)


# ---------------------------------------------------------------
# Distorsión de lente
# ---------------------------------------------------------------
def matriz_camara(ancho, alto):
    """Matriz intrínseca K: focal f = ancho y centro óptico en el centro."""
    f = float(ancho)
    return np.array([[f, 0, ancho / 2.0],
                     [0, f, alto / 2.0],
                     [0, 0, 1]], dtype=np.float64)


def dibujar_rejilla(img, paso=40):
    """Copia de la imagen con una rejilla encima: las líneas rectas
    permiten ver claramente cómo se curva la imagen con la distorsión."""
    res = img.copy()
    alto, ancho = res.shape[:2]
    for x in range(0, ancho, paso):
        cv.line(res, (x, 0), (x, alto - 1), (255, 255, 255), 1)
    for y in range(0, alto, paso):
        cv.line(res, (0, y), (ancho - 1, y), (255, 255, 255), 1)
    return res
