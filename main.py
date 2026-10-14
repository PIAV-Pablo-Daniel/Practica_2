"""
main.py - Parte obligatoria de la Práctica 2 (1a, 1b y 1c)
==========================================================
Tres ventanas que se actualizan en tiempo real:
  1a - Traslación, rotación y escalado (uniforme y no uniforme) con trackbars.
  1b - Ventana de proyección: se trazan sus 4 esquinas con el ratón
       (la esquina más cercana va a donde hagas clic / arrastres) y la
       imagen se proyecta dentro con una homografía.
  1c - Distorsión de lente gobernada por k1, k2, p1, p2 y k3.

optativo_raton.py y optativo_video.py reutilizan estas funciones; por eso
el bucle principal va dentro de  if __name__ == '__main__'.

Teclas: ESC salir · r reiniciar la ventana de proyección (1b)
"""
import cv2 as cv
import numpy as np

import geometria as geo

WIN_1A = '1a - Transformaciones'
WIN_1B = '1b - Proyeccion'
WIN_1C = '1c - Distorsion Lente'


def nada(x):
    pass


# ==========================================
# 1a: TRASLACIÓN, ROTACIÓN Y ESCALADO
# ==========================================
def crear_1a(ancho, alto):
    cv.namedWindow(WIN_1A)
    # Los trackbars no admiten negativos: Tx va de 0 a 2*ancho y luego se le
    # resta 'ancho', así se puede trasladar hacia la izquierda y la derecha.
    cv.createTrackbar('Tx', WIN_1A, ancho, ancho * 2, nada)
    cv.createTrackbar('Ty', WIN_1A, alto, alto * 2, nada)
    # Rotación: ángulo y centro de giro
    cv.createTrackbar('Angulo', WIN_1A, 0, 360, nada)
    cv.createTrackbar('Giro X', WIN_1A, ancho // 2, ancho, nada)
    cv.createTrackbar('Giro Y', WIN_1A, alto // 2, alto, nada)
    # Escalado: factores (en %) y centro de escalado
    cv.createTrackbar('Escala X (%)', WIN_1A, 100, 300, nada)
    cv.createTrackbar('Escala Y (%)', WIN_1A, 100, 300, nada)
    cv.createTrackbar('Escala centro X', WIN_1A, ancho // 2, ancho, nada)
    cv.createTrackbar('Escala centro Y', WIN_1A, alto // 2, alto, nada)


def procesar_1a(img):
    alto, ancho = img.shape[:2]
    tx = cv.getTrackbarPos('Tx', WIN_1A) - ancho
    ty = cv.getTrackbarPos('Ty', WIN_1A) - alto
    angulo = cv.getTrackbarPos('Angulo', WIN_1A)
    gx = cv.getTrackbarPos('Giro X', WIN_1A)
    gy = cv.getTrackbarPos('Giro Y', WIN_1A)
    sx = max(cv.getTrackbarPos('Escala X (%)', WIN_1A) / 100.0, 0.01)  # evitar escala 0
    sy = max(cv.getTrackbarPos('Escala Y (%)', WIN_1A) / 100.0, 0.01)
    ex = cv.getTrackbarPos('Escala centro X', WIN_1A)
    ey = cv.getTrackbarPos('Escala centro Y', WIN_1A)

    # De derecha a izquierda: 1º escalado, 2º rotación, 3º traslación
    M = geo.traslacion(tx, ty) @ geo.rotacion(angulo, gx, gy) @ geo.escalado(sx, sy, ex, ey)
    res = cv.warpAffine(img, M[:2, :], (ancho, alto))

    cv.circle(res, (gx, gy), 5, (0, 0, 255), -1)   # rojo: centro de giro
    cv.circle(res, (ex, ey), 5, (255, 0, 0), -1)   # azul: centro de escalado
    return res


# ==========================================
# 1b: VENTANA DE PROYECCIÓN
# ==========================================
esquinas = None        # 4 esquinas de la ventana destino (sup-izq, sup-der, inf-der, inf-izq)
esquina_activa = -1    # esquina que se está arrastrando (-1 = ninguna)


def reiniciar_1b(ancho, alto):
    """Ventana inicial: un rectángulo con un margen del 15 %."""
    global esquinas
    mx, my = 0.15 * ancho, 0.15 * alto
    esquinas = np.float32([[mx, my], [ancho - mx, my],
                           [ancho - mx, alto - my], [mx, alto - my]])


def raton_1b(evento, x, y, flags, param):
    global esquina_activa
    if evento == cv.EVENT_LBUTTONDOWN:
        # La esquina más cercana al clic salta ahí y se puede arrastrar
        distancias = np.hypot(esquinas[:, 0] - x, esquinas[:, 1] - y)
        esquina_activa = int(np.argmin(distancias))
        esquinas[esquina_activa] = (x, y)
    elif evento == cv.EVENT_MOUSEMOVE and esquina_activa >= 0:
        esquinas[esquina_activa] = (x, y)
    elif evento == cv.EVENT_LBUTTONUP:
        esquina_activa = -1


def crear_1b(ancho, alto):
    cv.namedWindow(WIN_1B)
    reiniciar_1b(ancho, alto)
    cv.setMouseCallback(WIN_1B, raton_1b)


def procesar_1b(img):
    alto, ancho = img.shape[:2]
    # Origen: las 4 esquinas de la imagen, en el mismo orden que 'esquinas'
    origen = np.float32([[0, 0], [ancho - 1, 0], [ancho - 1, alto - 1], [0, alto - 1]])

    H = cv.getPerspectiveTransform(origen, esquinas)   # 4 puntos -> matriz 3x3
    res = cv.warpPerspective(img, H, (ancho, alto))

    cv.polylines(res, [esquinas.astype(np.int32)], True, (0, 255, 0), 2)
    for x, y in esquinas.astype(int):
        cv.circle(res, (int(x), int(y)), 6, (0, 255, 255), -1)
    return res


# ==========================================
# 1c: DISTORSIÓN DE LENTE
# ==========================================
def crear_1c():
    cv.namedWindow(WIN_1C)
    # Trackbars de 0 a 2000 con el 1000 como cero (permite valores negativos)
    cv.createTrackbar('k1 (Radial)', WIN_1C, 1000, 2000, nada)
    cv.createTrackbar('k2 (Radial)', WIN_1C, 1000, 2000, nada)
    cv.createTrackbar('k3 (Radial)', WIN_1C, 1000, 2000, nada)
    cv.createTrackbar('p1 (Tangencial)', WIN_1C, 1000, 2000, nada)
    cv.createTrackbar('p2 (Tangencial)', WIN_1C, 1000, 2000, nada)
    cv.createTrackbar('Rejilla', WIN_1C, 1, 1, nada)


def procesar_1c(img):
    alto, ancho = img.shape[:2]
    # Radiales en [-1, 1]; tangenciales en [-0.1, 0.1] porque su efecto es mucho mayor
    k1 = (cv.getTrackbarPos('k1 (Radial)', WIN_1C) - 1000) / 1000.0
    k2 = (cv.getTrackbarPos('k2 (Radial)', WIN_1C) - 1000) / 1000.0
    k3 = (cv.getTrackbarPos('k3 (Radial)', WIN_1C) - 1000) / 1000.0
    p1 = (cv.getTrackbarPos('p1 (Tangencial)', WIN_1C) - 1000) / 10000.0
    p2 = (cv.getTrackbarPos('p2 (Tangencial)', WIN_1C) - 1000) / 10000.0

    K = geo.matriz_camara(ancho, alto)
    coef = np.array([k1, k2, p1, p2, k3])   # orden que espera OpenCV

    if cv.getTrackbarPos('Rejilla', WIN_1C) == 1:
        img = geo.dibujar_rejilla(img)
    # k > 0 -> barril, k < 0 -> cojín (almohadilla)
    return cv.undistort(img, K, coef)


# ==========================================
# FUNCIONES COMUNES (también las usa optativo_video.py)
# ==========================================
def crear_interfaz(ancho, alto):
    crear_1a(ancho, alto)
    crear_1b(ancho, alto)
    crear_1c()


def mostrar(img):
    # Siempre se transforma la imagen ORIGINAL: así no se acumulan
    # pérdidas por interpolación entre una vuelta y la siguiente.
    cv.imshow(WIN_1A, procesar_1a(img))
    cv.imshow(WIN_1B, procesar_1b(img))
    cv.imshow(WIN_1C, procesar_1c(img))


if __name__ == '__main__':
    img = geo.cargar_imagen('images/cats.png')
    alto, ancho = img.shape[:2]
    crear_interfaz(ancho, alto)

    while True:
        mostrar(img)
        tecla = cv.waitKey(20) & 0xFF
        if tecla == 27:
            break
        elif tecla == ord('r'):
            reiniciar_1b(ancho, alto)

    cv.destroyAllWindows()
