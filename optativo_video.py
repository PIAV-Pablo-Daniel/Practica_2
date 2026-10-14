"""
optativo_video.py - Optativo 4: la parte obligatoria sobre vídeo
================================================================
Las mismas tres ventanas de main.py (1a, 1b y 1c), pero cada vuelta del
bucle se procesa un frame nuevo del vídeo en lugar de una imagen fija.
Se usa videos/Stairs.mp4 (ejemplos del profesor); si no está, la webcam.

Teclas: ESC salir · r reiniciar la ventana de proyección (1b)
"""
import os
import sys

import cv2 as cv

import geometria as geo
import main as obligatorio

RUTA_VIDEO = os.path.join(geo.CARPETA, 'videos', 'Stairs.mp4')
ANCHO_MAX = 640   # se reduce el vídeo si es más grande para que vaya fluido

cap = cv.VideoCapture(RUTA_VIDEO)
if not cap.isOpened():
    print("Aviso: no se encontró el vídeo, se usa la webcam.")
    cap = cv.VideoCapture(0)
if not cap.isOpened():
    sys.exit("Error: no hay vídeo ni webcam disponibles.")


def leer_frame():
    ret, frame = cap.read()
    if not ret:
        # Fin del vídeo: volver al principio para que se repita en bucle
        cap.set(cv.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()
        if not ret:
            return None
    alto, ancho = frame.shape[:2]
    if ancho > ANCHO_MAX:
        f = ANCHO_MAX / ancho
        frame = cv.resize(frame, None, fx=f, fy=f, interpolation=cv.INTER_AREA)
    return frame


frame = leer_frame()
if frame is None:
    sys.exit("Error: no se pudo leer el primer frame.")
alto, ancho = frame.shape[:2]
obligatorio.crear_interfaz(ancho, alto)

while frame is not None:
    obligatorio.mostrar(frame)

    tecla = cv.waitKey(20) & 0xFF
    if tecla == 27:
        break
    elif tecla == ord('r'):
        obligatorio.reiniciar_1b(ancho, alto)

    frame = leer_frame()

cap.release()
cv.destroyAllWindows()
