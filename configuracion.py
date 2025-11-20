import tkinter as tk

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

    def cerrar_ventana():
        configuracion.destroy()
        window.deiconify()

    boton_salir = tk.Button(configuracion, text="Salir", command=cerrar_ventana)
    boton_salir.place(x=220, y=400)

    window.withdraw()

