import tkinter as tk
import os

RUTA_HISTORIAL = "historial_jugadores.txt"

def registrar_jugador(nombre):
    nombre = nombre.strip()
    if not nombre:
        return

    jugadores = {}

    # Leer lo que ya exista
    if os.path.exists(RUTA_HISTORIAL):
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    n, veces = linea.rsplit(",", 1)
                    jugadores[n] = int(veces)
                except ValueError:
                    continue


    jugadores[nombre] = jugadores.get(nombre, 0) + 1

    # Guardar de nuevo
    with open(RUTA_HISTORIAL, "w", encoding="utf-8") as f:
        for n, veces in jugadores.items():
            f.write(f"{n},{veces}\n")




def abrir_configuracion(window):
    configuracion = tk.Toplevel(window)
    configuracion.title("Configuración")
    configuracion.geometry("500x500")
    configuracion.resizable(width=False, height=False)
    configuracion.configure(bg="green")

    label_titulo = tk.Label(configuracion, text="Configuración del Juego", font=("Impact", 15), bg="green")
    label_titulo.place(x=140, y=40)

    def set_dificultad(valor):
        global dificultad_actual
        dificultad_actual = valor
        print("Dificultad seleccionada:", dificultad_actual)

    label_dificultad = tk.Label(configuracion, text="Dificultad",
                                font=("Impact", 13), bg="green")
    label_dificultad.place(x=210, y=120)

    boton_facil = tk.Button(configuracion, text="Fácil",
                            command=lambda: set_dificultad("Facil"))
    boton_facil.place(x=120, y=160)

    boton_medio = tk.Button(configuracion, text="Medio",
                            command=lambda: set_dificultad("Medio"))
    boton_medio.place(x=220, y=160)

    boton_dificil = tk.Button(configuracion, text="Difícil",
                              command=lambda: set_dificultad("Dificil"))
    boton_dificil.place(x=320, y=160)

    # ---- Historial de jugadores con scroll ----
    label_historial = tk.Label(configuracion, text="Historial de jugadores",
                               font=("Impact", 13), bg="green")
    label_historial.place(x=160, y=220)

    frame_historial = tk.Frame(configuracion, bg="green")
    frame_historial.place(x=60, y=250, width=380, height=130)

    scrollbar = tk.Scrollbar(frame_historial)
    scrollbar.pack(side="right", fill="y")

    text_historial = tk.Text(frame_historial, width=40, height=7, yscrollcommand=scrollbar.set)
    text_historial.pack(side="left", fill="both")

    scrollbar.config(command=text_historial.yview)

    # Cargar historial desde archivo
    if os.path.exists(RUTA_HISTORIAL):
        jugadores = []
        with open(RUTA_HISTORIAL, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                try:
                    n, veces = linea.rsplit(",", 1)
                    veces = int(veces)
                    jugadores.append((n, veces))
                except ValueError:
                    continue

        # Ordenar por cantidad de partidas (descendente)
        jugadores.sort(key=lambda x: x[1], reverse=True)

        for i, (n, veces) in enumerate(jugadores, start=1):
            text_historial.insert("end", f"{i}. {n} - {veces} partidas\n")

    text_historial.config(state="disabled")

    def cerrar_ventana():
        configuracion.destroy()
        window.deiconify()

    boton_salir = tk.Button(configuracion, text="Salir", command=cerrar_ventana)
    boton_salir.place(x=220, y=400)

    window.withdraw()

