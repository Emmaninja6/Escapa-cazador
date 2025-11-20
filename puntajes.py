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

def abrir_puntaje(window):
    puntaje = tk.Toplevel()
    puntaje.title("Puntajes")
    puntaje.geometry("350x350")
    puntaje.resizable(width=False, height=False)
    puntaje.configure(bg="green")

    label_titulo = tk.Label(puntaje, text="Top 5 Escapa", font=("Impact", 15), bg="green")
    label_titulo.place(x=110, y=40)

    lista = cargar_puntajes_escapa()

    y = 90
    for i, (nombre, pts) in enumerate(lista, start=1):
        texto = f"{i}. {nombre} - {pts} pts"
        lbl = tk.Label(puntaje, text=texto, font=("Arial", 12), bg="green")
        lbl.place(x=60, y=y)
        y += 25

    def cerrar_ventana():
        puntaje.destroy()
        window.deiconify()

    boton_salir = tk.Button(puntaje, text="Salir", command=cerrar_ventana)
    boton_salir.place(x=160, y=250)

    window.withdraw()




    def cerrar_ventana():
        puntaje.destroy()
        window.deiconify()

    boton_salir = tk.Button(puntaje, text="Salir", command=cerrar_ventana)
    boton_salir.place(x=160, y=250)

    window.withdraw() 
