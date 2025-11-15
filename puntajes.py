import tkinter as tk

def abrir_puntaje(window):
    puntaje = tk.Toplevel()
    puntaje.title("Puntajes")
    puntaje.geometry("350x350")
    puntaje.resizable(width=False, height=False)
    puntaje.configure(bg="green")

    label_titulo = tk.Label(puntaje, text="Top 3 Puntajes.", font=("Impact", 15), bg="green")
    label_titulo.place(x=110, y=40)



    def cerrar_ventana():
        puntaje.destroy()
        window.deiconify()

    boton_salir = tk.Button(puntaje, text="Salir", command=cerrar_ventana)
    boton_salir.place(x=160, y=250)

    window.withdraw() 
