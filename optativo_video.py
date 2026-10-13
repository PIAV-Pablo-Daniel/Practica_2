import cv2 as cv
import numpy as np
import sys

# ==============================================================================
# OPTATIVO 2: PARTE OBLIGATORIA SOBRE VÍDEO
# Ejecuta exactamente las tres secciones obligatorias (1a, 1b, 1c) pero
# procesando cada frame de vídeo en tiempo real en lugar de una imagen estática.
# ==============================================================================

def nada(x):
    pass

# Inicialización de la captura de vídeo (cámara web)
cap = cv.VideoCapture(0)

# Verificación de la fuente de vídeo
if not cap.isOpened():
    print("Aviso: No se pudo abrir la cámara web (índice 0).")
    print("Intentando abrir una imagen como flujo de prueba...")
    # Si no hay cámara física disponible, usamos una imagen como fuente repetitiva
    img_fallback = cv.imread('images/cats.png')
    if img_fallback is None:
        sys.exit("Error: No hay cámara ni imagen disponible para la prueba.")
    usar_fallback = True
else:
    usar_fallback = False

# Obtener dimensiones del primer frame
if not usar_fallback:
    ret, frame_inicial = cap.read()
    if not ret or frame_inicial is None:
        sys.exit("Error: No se pudo leer el primer frame del vídeo.")
else:
    frame_inicial = img_fallback

alto, ancho = frame_inicial.shape[:2]

# ==========================================
# 1. CONFIGURACIÓN 1a: TRANSFORMACIONES EN VÍDEO
# ==========================================
win_1a = '1a - Video Transformaciones'
cv.namedWindow(win_1a)

cv.createTrackbar('Tx', win_1a, ancho, ancho * 2, nada)
cv.createTrackbar('Ty', win_1a, alto, alto * 2, nada)
cv.createTrackbar('Angulo', win_1a, 0, 360, nada)
cv.createTrackbar('Centro X', win_1a, ancho // 2, ancho, nada)
cv.createTrackbar('Centro Y', win_1a, alto // 2, alto, nada)
cv.createTrackbar('Escala X (%)', win_1a, 100, 300, nada)
cv.createTrackbar('Escala Y (%)', win_1a, 100, 300, nada)

# ==========================================
# 2. CONFIGURACIÓN 1b: PROYECCIÓN EN VÍDEO
# ==========================================
win_1b = '1b - Video Proyeccion'
cv.namedWindow(win_1b)

pts_origen_proy = np.float32([
    [0, 0],
    [ancho, 0],
    [ancho, alto],
    [0, alto]
])

cv.createTrackbar('Sup-Izq X', win_1b, 0, ancho // 2, nada)
cv.createTrackbar('Sup-Izq Y', win_1b, 0, alto // 2, nada)
cv.createTrackbar('Sup-Der X', win_1b, 0, ancho // 2, nada)
cv.createTrackbar('Sup-Der Y', win_1b, 0, alto // 2, nada)
cv.createTrackbar('Inf-Der X', win_1b, 0, ancho // 2, nada)
cv.createTrackbar('Inf-Der Y', win_1b, 0, alto // 2, nada)
cv.createTrackbar('Inf-Izq X', win_1b, 0, ancho // 2, nada)
cv.createTrackbar('Inf-Izq Y', win_1b, 0, alto // 2, nada)

# ==========================================
# 3. CONFIGURACIÓN 1c: DISTORSIÓN DE LENTE EN VÍDEO
# ==========================================
win_1c = '1c - Video Distorsion Lente'
cv.namedWindow(win_1c)

K = np.array([
    [ancho, 0, ancho / 2.0],
    [0, ancho, alto / 2.0],
    [0, 0, 1]
], dtype=np.float32)

cv.createTrackbar('k1 (Radial)', win_1c, 1000, 2000, nada)
cv.createTrackbar('k2 (Radial)', win_1c, 1000, 2000, nada)
cv.createTrackbar('p1 (Tangencial)', win_1c, 1000, 2000, nada)
cv.createTrackbar('p2 (Tangencial)', win_1c, 1000, 2000, nada)
cv.createTrackbar('k3 (Radial)', win_1c, 1000, 2000, nada)

print("Procesando vídeo en tiempo real. Pulsa ESC para salir.")

# ==========================================
# BUCLE PRINCIPAL DE VÍDEO
# ==========================================
while True:
    if not usar_fallback:
        ret, frame = cap.read()
        if not ret:
            # Si el vídeo termina, reiniciar o salir
            cap.set(cv.CAP_PROP_POS_FRAMES, 0)
            ret, frame = cap.read()
            if not ret:
                break
    else:
        frame = img_fallback.copy()

    # --- PROCESAMIENTO 1a ---
    tx = cv.getTrackbarPos('Tx', win_1a) - ancho
    ty = cv.getTrackbarPos('Ty', win_1a) - alto
    angulo = cv.getTrackbarPos('Angulo', win_1a)
    cx = cv.getTrackbarPos('Centro X', win_1a)
    cy = cv.getTrackbarPos('Centro Y', win_1a)
    sx = max(cv.getTrackbarPos('Escala X (%)', win_1a) / 100.0, 0.01)
    sy = max(cv.getTrackbarPos('Escala Y (%)', win_1a) / 100.0, 0.01)

    theta = np.radians(angulo)
    cos_t, sin_t = np.cos(theta), np.sin(theta)

    T_orig = np.array([[1, 0, -cx], [0, 1, -cy], [0, 0, 1]], dtype=np.float32)
    R_S = np.array([[sx * cos_t, -sy * sin_t, 0],
                    [sx * sin_t,  sy * cos_t, 0],
                    [0, 0, 1]], dtype=np.float32)
    T_dest = np.array([[1, 0, cx + tx], [0, 1, cy + ty], [0, 0, 1]], dtype=np.float32)

    M_afin = (T_dest @ R_S @ T_orig)[:2, :]
    res_1a = cv.warpAffine(frame, M_afin, (ancho, alto))

    # --- PROCESAMIENTO 1b ---
    d_x1 = cv.getTrackbarPos('Sup-Izq X', win_1b)
    d_y1 = cv.getTrackbarPos('Sup-Izq Y', win_1b)
    d_x2 = cv.getTrackbarPos('Sup-Der X', win_1b)
    d_y2 = cv.getTrackbarPos('Sup-Der Y', win_1b)
    d_x3 = cv.getTrackbarPos('Inf-Der X', win_1b)
    d_y3 = cv.getTrackbarPos('Inf-Der Y', win_1b)
    d_x4 = cv.getTrackbarPos('Inf-Izq X', win_1b)
    d_y4 = cv.getTrackbarPos('Inf-Izq Y', win_1b)

    pts_destino_proy = np.float32([
        [d_x1, d_y1],
        [ancho - d_x2, d_y2],
        [ancho - d_x3, alto - d_y3],
        [d_x4, alto - d_y4]
    ])

    M_proy = cv.getPerspectiveTransform(pts_origen_proy, pts_destino_proy)
    res_1b = cv.warpPerspective(frame, M_proy, (ancho, alto))
    poly = pts_destino_proy.astype(np.int32).reshape((-1, 1, 2))
    cv.polylines(res_1b, [poly], isClosed=True, color=(0, 255, 0), thickness=2)

    # --- PROCESAMIENTO 1c ---
    k1 = (cv.getTrackbarPos('k1 (Radial)', win_1c) - 1000) / 1000.0
    k2 = (cv.getTrackbarPos('k2 (Radial)', win_1c) - 1000) / 1000.0
    p1 = (cv.getTrackbarPos('p1 (Tangencial)', win_1c) - 1000) / 10000.0
    p2 = (cv.getTrackbarPos('p2 (Tangencial)', win_1c) - 1000) / 10000.0
    k3 = (cv.getTrackbarPos('k3 (Radial)', win_1c) - 1000) / 1000.0

    dist_coeffs = np.array([k1, k2, p1, p2, k3], dtype=np.float32)
    res_1c = cv.undistort(frame, K, dist_coeffs)

    # --- MOSTRAR RESULTADOS ---
    cv.imshow(win_1a, res_1a)
    cv.imshow(win_1b, res_1b)
    cv.imshow(win_1c, res_1c)

    if cv.waitKey(20) & 0xFF == 27:
        break

if not usar_fallback:
    cap.release()
cv.destroyAllWindows()
