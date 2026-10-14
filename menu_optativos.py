import os
import sys
import subprocess
import tkinter as tk
from tkinter import font

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Procesos activos para poder cerrarlos ordenadamente
procesos = []

def ejecutar(script):
    ruta = os.path.join(BASE_DIR, script)
    # Ejecuta en paralelo para no congelar la ventana del menú
    p = subprocess.Popen([sys.executable, ruta], cwd=BASE_DIR)
    procesos.append(p)

def cerrar_todo():
    for p in procesos:
        if p.poll() is None:
            p.terminate()
    root.destroy()

# Configuración de la ventana principal
root = tk.Tk()
root.title("Práctica 2 - Transformaciones Geométricas")
root.geometry("480x560")
root.resizable(False, False)
root.configure(bg="#1E1E2E")  # Fondo oscuro moderno

# Tipografías
fuente_titulo = font.Font(family="Helvetica", size=15, weight="bold")
fuente_subtitulo = font.Font(family="Helvetica", size=10)
fuente_btn = font.Font(family="Helvetica", size=11, weight="bold")
fuente_desc = font.Font(family="Helvetica", size=9)

# Encabezado
header_frame = tk.Frame(root, bg="#1E1E2E")
header_frame.pack(pady=15)

lbl_titulo = tk.Label(header_frame, text="PRÁCTICA 2: TRANSFORMACIONES",
                      font=fuente_titulo, fg="#CDD6F4", bg="#1E1E2E")
lbl_titulo.pack()

lbl_sub = tk.Label(header_frame, text="Haz clic en cualquier botón para abrir la demo",
                   font=fuente_subtitulo, fg="#A6ADC8", bg="#1E1E2E")
lbl_sub.pack(pady=3)

# Botones de las funcionalidades
opciones = [
    ("1. Parte Obligatoria (1a, 1b, 1c)", "main.py", "#89B4FA", "#11111B",
     "1a trackbars · 1b arrastrar esquinas · 1c coeficientes de lente"),
    ("2. Control con Ratón (Optativo)", "optativo_raton.py", "#A6E3A1", "#11111B",
     "Teclas t/g/e: arrastrar, centro de giro, centro de escalado"),
    ("3. Transformación Afín 3 Puntos", "optativo_afin_3puntos.py", "#F9E2AF", "#11111B",
     "Seleccionar 3 puntos en origen y 3 en destino con ratón"),
    ("4. Transformación Proyectiva 4 Puntos", "optativo_proyectiva_4puntos.py", "#FAB387", "#11111B",
     "Seleccionar 4 puntos con ratón y proyectar homografía"),
    ("5. Especular y Eje de Reflexión", "optativo_especular_reflexion.py", "#CBA6F7", "#11111B",
     "Espejo horizontal y reflexión sobre recta trazada en vivo"),
    ("6. Modo Vídeo en Vivo", "optativo_video.py", "#F38BA8", "#11111B",
     "1a, 1b y 1c sobre videos/Stairs.mp4 (o webcam)")
]

btn_container = tk.Frame(root, bg="#1E1E2E")
btn_container.pack(fill="x", padx=30)

for texto, script, color_bg, color_fg, desc in opciones:
    f = tk.Frame(btn_container, bg="#1E1E2E")
    f.pack(fill="x", pady=4)

    btn = tk.Button(f, text=texto, font=fuente_btn, bg=color_bg, fg=color_fg,
                    activebackground="#B4BEFE", relief="flat", cursor="hand2",
                    command=lambda s=script: ejecutar(s), height=1)
    btn.pack(fill="x")

    lbl = tk.Label(f, text=desc, font=fuente_desc, fg="#6C7086", bg="#1E1E2E")
    lbl.pack(anchor="w", padx=2)

# Botón Salir
btn_salir = tk.Button(root, text="Cerrar Todo y Salir", font=fuente_btn,
                      bg="#313244", fg="#F38BA8", relief="flat", cursor="hand2",
                      command=cerrar_todo)
btn_salir.pack(pady=15, ipadx=10, ipady=3)

root.protocol("WM_DELETE_WINDOW", cerrar_todo)
root.mainloop()
