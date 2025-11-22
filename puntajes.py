import tkinter as tk
import os

RUTA_PUNTAJES_ESCAPE = "puntajes_escape.txt"
RUTA_PUNTAJES_CAZADOR = "puntajes_cazador.txt"

def cargar_puntajes_escapa():
    puntajes = []
    if not os.path.exists(RUTA_PUNTAJES_ESCAPE):
        return puntajes
    with open(RUTA_PUNTAJES_ESCAPE, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            nombre, pts = linea.rsplit(",", 1)
            try:
                pts = int(pts)
                puntajes.append((nombre, pts))
            except ValueError:
                continue
    puntajes.sort(key=lambda x: x[1], reverse=True)
    return puntajes[:5]

def cargar_puntajes_cazador():
    puntajes = []
    if not os.path.exists(RUTA_PUNTAJES_CAZADOR):
        return puntajes
    with open(RUTA_PUNTAJES_CAZADOR, "r", encoding="utf-8") as f:
        for linea in f:
            linea = linea.strip()
            if not linea:
                continue
            nombre, pts = linea.rsplit(",", 1)
            try:
                pts = int(pts)
                puntajes.append((nombre, pts))
            except ValueError:
                continue
    puntajes.sort(key=lambda x: x[1], reverse=True)
    return puntajes[:5]

def abrir_puntaje(window):
    puntaje = tk.Toplevel()
    puntaje.title("Puntajes")
    puntaje.geometry("400x400")
    puntaje.resizable(width=False, height=False)
    puntaje.configure(bg="green")

    # Pestañas o secciones para ambos modos
    label_titulo_escapa = tk.Label(puntaje, text="Top 5 - Modo Escapa", font=("Impact", 15), bg="green")
    label_titulo_escapa.place(x=100, y=20)

    lista_escapa = cargar_puntajes_escapa()
    y = 60
    for i, (nombre, pts) in enumerate(lista_escapa, start=1):
        texto = f"{i}. {nombre} - {pts} pts"
        lbl = tk.Label(puntaje, text=texto, font=("Arial", 12), bg="green")
        lbl.place(x=60, y=y)
        y += 25

    label_titulo_cazador = tk.Label(puntaje, text="Top 5 - Modo Cazador", font=("Impact", 15), bg="green")
    label_titulo_cazador.place(x=100, y=200)

    lista_cazador = cargar_puntajes_cazador()
    y = 240
    for i, (nombre, pts) in enumerate(lista_cazador, start=1):
        texto = f"{i}. {nombre} - {pts} pts"
        lbl = tk.Label(puntaje, text=texto, font=("Arial", 12), bg="green")
        lbl.place(x=60, y=y)
        y += 25

    def cerrar_ventana():
        puntaje.destroy()
        window.deiconify()

    boton_salir = tk.Button(puntaje, text="Salir", command=cerrar_ventana)
    boton_salir.place(x=180, y=350)

    window.withdraw()
