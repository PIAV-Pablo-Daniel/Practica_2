# Práctica 2 — Transformaciones geométricas

**Procesamiento de Imágenes, Audio y Vídeo (PIAV)**

Aplicación en Python + OpenCV que aplica transformaciones geométricas a imágenes y vídeo en tiempo real: traslación, rotación, escalado, proyección (homografía), distorsión de lente, transformaciones afín y proyectiva por puntos, imagen especular y reflexión respecto a una recta.

---

## Requisitos e instalación

- Python 3.9 o superior
- OpenCV y NumPy

```bash
# (Opcional) crear un entorno virtual
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

## Cómo ejecutarlo

Desde la carpeta del proyecto:

```bash
python3 menu_optativos.py        # menú con un botón para cada apartado
```

En macOS también se puede hacer doble clic en `Lanzar_Practica.command`.

Cada script también se puede lanzar por separado:

| Script | Apartado | Comando |
|---|---|---|
| `main.py` | Obligatorio 1a, 1b y 1c | `python3 main.py` |
| `optativo_raton.py` | Optativos 1, 2 y 3 (ratón) | `python3 optativo_raton.py` |
| `optativo_video.py` | Optativo 4 (vídeo) | `python3 optativo_video.py` |
| `optativo_afin_3puntos.py` | Optativo 5 (afín, 3 puntos) | `python3 optativo_afin_3puntos.py` |
| `optativo_proyectiva_4puntos.py` | Optativo 6 (proyectiva, 4 puntos) | `python3 optativo_proyectiva_4puntos.py` |
| `optativo_especular_reflexion.py` | Optativos 7 y 8 (espejo y reflexión) | `python3 optativo_especular_reflexion.py` |

En todas las ventanas, **ESC** cierra el programa.

---

## Estructura del proyecto

```
Practica_2/
├── geometria.py                     # Módulo común: TODAS las matrices de transformación
├── main.py                          # Parte obligatoria (1a, 1b, 1c)
├── optativo_raton.py                # Optativos 1-3
├── optativo_video.py                # Optativo 4
├── optativo_afin_3puntos.py         # Optativo 5
├── optativo_proyectiva_4puntos.py   # Optativo 6
├── optativo_especular_reflexion.py  # Optativos 7 y 8
├── menu_optativos.py                # Menú gráfico (Tkinter) para lanzar las demos
├── Lanzar_Practica.command          # Lanzador para macOS
├── requirements.txt
├── images/                          # Imágenes de prueba
└── videos/                          # Vídeo de prueba (Stairs.mp4)
```

**Decisión de diseño:** las matrices se escriben una sola vez en `geometria.py`, y el resto de scripts solo se ocupan de la interfaz (trackbars, ratón y bucle). Además, `optativo_raton.py` y `optativo_video.py` reutilizan las funciones de `main.py` en lugar de copiar su código.

---

## Fundamento teórico

**Coordenadas homogéneas.** Un punto `(x, y)` se representa como `(x, y, 1)`. Así, todas las transformaciones (incluida la traslación) son una multiplicación por una matriz 3×3, y componerlas es multiplicar matrices. Las matrices se aplican **de derecha a izquierda**.

```
[x']   [a11 a12 tx] [x]
[y'] = [a21 a22 ty] [y]
[1 ]   [ 0   0   1] [1]
```

`cv.warpAffine` recibe solo las dos primeras filas (2×3). `cv.warpPerspective` recibe la matriz 3×3 completa.

**Girar o escalar respecto a un punto `(cx, cy)`.** Se lleva el centro al origen, se transforma y se devuelve a su sitio:

```
M = T(cx, cy) · R(θ) · T(-cx, -cy)
```

**El eje Y va hacia abajo.** Por eso la matriz de rotación es `[[cos, sin], [-sin, cos]]`. Con ella, un ángulo positivo gira en sentido antihorario en pantalla, igual que `cv.getRotationMatrix2D`.

| Transformación | Grados de libertad | Conserva | Función OpenCV |
|---|---|---|---|
| Traslación | 2 | todo menos la posición | `warpAffine` |
| Euclídea (rígida) | 3 | distancias y ángulos | `getRotationMatrix2D` |
| Similaridad | 4 | ángulos y proporciones | `getRotationMatrix2D` |
| Afín | 6 → 3 puntos | rectas y paralelismo | `getAffineTransform` |
| Proyectiva | 8 → 4 puntos | solo rectas | `getPerspectiveTransform` |

---

## Parte obligatoria (`main.py`)

Abre tres ventanas que se actualizan en tiempo real. Siempre se transforma la imagen **original**, para no acumular pérdidas por interpolación entre una iteración y la siguiente.

### 1a — Traslación, rotación y escalado

Ventana controlada con trackbars:

| Trackbar | Significado |
|---|---|
| `Tx`, `Ty` | Magnitud de la traslación en X e Y (el centro del trackbar equivale a 0, así se admiten valores negativos) |
| `Angulo` | Ángulo de giro en grados (0–360) |
| `Giro X`, `Giro Y` | Centro de giro (punto **rojo**) |
| `Escala X (%)`, `Escala Y (%)` | Factores de escala. Si son iguales, el escalado es uniforme; si son distintos, no uniforme |
| `Escala centro X`, `Escala centro Y` | Centro de escalado (punto **azul**) |

Matriz final (primero escalado, luego rotación y por último traslación):

```
M = T(tx, ty) · Rot(θ, centro_giro) · Esc(sx, sy, centro_escala)
```

### 1b — Ventana de proyección

La ventana de proyección se traza con el ratón. Al hacer clic, la esquina más cercana salta a esa posición y se puede arrastrar. Las 4 esquinas de la imagen se proyectan sobre el cuadrilátero con `getPerspectiveTransform` y `warpPerspective`. El contorno de la ventana se dibuja en verde.

- **Clic / arrastrar:** mover una esquina
- **r:** reiniciar la ventana

### 1c — Distorsión de lente

Trackbars para los coeficientes del modelo de lente de OpenCV:

- **Radiales `k1`, `k2`, `k3`** en el rango [-1, 1]. Con valores positivos la imagen se deforma en **barril**; con negativos, en **cojín**.
- **Tangenciales `p1`, `p2`** en el rango [-0.1, 0.1]. Tienen un efecto mucho mayor, por eso el rango es más pequeño.
- **`Rejilla`** dibuja líneas rectas sobre la imagen para que se aprecie cómo se curvan.

Se usa una matriz de cámara `K` con focal igual al ancho de la imagen y el centro óptico en el centro, y se aplica `cv.undistort`.

---

## Parte optativa

### Optativos 1, 2 y 3 — Control con el ratón (`optativo_raton.py`)

Reutiliza la ventana 1a. Con el teclado se elige qué hace el clic izquierdo (el modo activo se muestra en pantalla):

| Tecla | Modo | Acción del ratón |
|---|---|---|
| `t` | Trasladar | Arrastrar la imagen en tiempo real |
| `g` | Centro de giro | Clic para marcar el punto de giro |
| `e` | Centro de escalado | Clic para marcar el punto de escalado |

El ratón solo mueve los trackbars, de modo que el cálculo es exactamente el mismo que en el apartado 1a.

### Optativo 4 — Parte obligatoria sobre vídeo (`optativo_video.py`)

Abre las mismas tres ventanas de `main.py` (1a, 1b y 1c), pero en cada iteración procesa un nuevo fotograma de `videos/Stairs.mp4`. El vídeo se repite en bucle y, si es más ancho de 640 px, se reduce con `INTER_AREA` para que vaya fluido. Si no encuentra el vídeo, usa la webcam.

### Optativo 5 — Transformación afín con 3 puntos (`optativo_afin_3puntos.py`)

Se marcan 3 puntos en la ventana *Origen* y otros 3 en *Destino*, en el mismo orden (los puntos aparecen numerados). Tres parejas dan 6 ecuaciones para las 6 incógnitas de la matriz afín, que se calcula con `getAffineTransform`. La tecla **r** borra los puntos.

### Optativo 6 — Transformación proyectiva con 4 puntos (`optativo_proyectiva_4puntos.py`)

Funciona igual que el anterior, pero con 4 puntos. La homografía 3×3 tiene 8 grados de libertad (está definida salvo un factor de escala), así que hacen falta 4 parejas de puntos. Se calcula con `getPerspectiveTransform`. La tecla **r** borra los puntos.

### Optativos 7 y 8 — Especular y reflexión respecto a una recta (`optativo_especular_reflexion.py`)

- **Imagen especular:** se aplica la matriz `x' = (ancho - 1) - x`. El resultado es idéntico a `cv.flip(img, 1)` y se muestra junto a la original.
- **Reflexión respecto a una recta:** dos clics definen el eje de reflexión. La matriz se construye así:

  ```
  M = T(p1) · R⁻¹ · RefX · R · T(-p1)
  ```

  Primero se lleva `p1` al origen, después se gira para que la recta quede sobre el eje X, se refleja respecto a ese eje y por último se deshacen el giro y la traslación. La tecla **r** borra la recta.

### Otras aportaciones

- Menú gráfico (`menu_optativos.py`) para lanzar todas las demos desde una sola ventana.
- Módulo común `geometria.py`, que separa las matemáticas de la interfaz.
- Rejilla de referencia para visualizar la distorsión de lente.
