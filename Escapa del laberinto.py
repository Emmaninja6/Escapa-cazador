import tkinter as tk
from tkinter import *
import random
from PIL import ImageTk, Image
import pygame

def Ventana_principal():
    window = Tk()
    window.minsize(width=500, height=500)
    window.config(bg="green")
    window.title("Escapa/Cazador")

    textoPrincipal = Label(text="Escapa del Laberinto", font=("Impact", 20), fg="Black", bg="green")
    textoPrincipal.pack()

    elegir = Label( text= "Elija un modo de juego",font=("Impact", 15), fg="Black", bg="green")
    elegir.place(x= 60, y= 150)

    boton_escapa = Button(text="Escapar")
    boton_escapa.place(x=60,y= 200)

    boton_cazar = Button(text="Cazador")
    boton_cazar.place(x= 160,y=200)

    puntos = Label(text="Tabla de puntajes",font=("Impact", 15), fg="Black", bg="green")
    puntos.place(x= 300,y=150)

    boton_puntos = Button(text="Puntajes", command=lambda: Ventana_puntuaciones(window))
    boton_puntos.place(x=340, y=200)

    nombre= Label(text="Ingrese su nombre",font=("Impact", 17), fg="Black", bg="green")
    nombre.pack()

    entry1 = Entry()
    entry1.config(font=("elephant",12), bg="Gray", fg="red", width=15)
    entry1.place(x=157, y=70)


    window.mainloop()

def Ventana_puntuaciones(window):
    global puntaje
    window.destroy()
    window = Tk()
    window.minsize(width=600, height=600)
    window.config(bg="green")
    window.title("Salon de puntajes")

    Boton_atras = Button(text="Regresar a Menu principal", command=lambda: atras_ventana(window))
    Boton_atras.pack()

    window.mainloop()


def atras_ventana(window):
    window.destroy()
    window = Ventana_principal()


Ventana_principal()