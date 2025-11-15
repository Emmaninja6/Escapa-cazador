import tkinter as tk
from tkinter import *
import random
from PIL import ImageTk, Image
import pygame
import puntajes
import jugarescapar


window = tk.Tk()
window.title("Escapa/Cazador")
window.geometry("500x500")
window.configure(bg="green")
window.resizable(width=False, height=False)

textoPrincipal = Label(text="Escapa del Laberinto", font=("Impact", 20), fg="Black", bg="green")
textoPrincipal.pack()

elegir = Label( text= "Elija un modo de juego",font=("Impact", 15), fg="Black", bg="green")
elegir.place(x= 60, y= 150)

boton_escapa = Button(text="Escapar" ,command=lambda: jugarescapar.jugar(window))
boton_escapa.place(x=60,y= 200)

boton_cazar = Button(text="Cazador")
boton_cazar.place(x= 160,y=200)

puntos = Label(text="Tabla de puntajes",font=("Impact", 15), fg="Black", bg="green")
puntos.place(x= 300,y=150)

boton_puntos = Button(text="Puntajes", command=lambda: puntajes.abrir_puntaje(window))
boton_puntos.place(x=340, y=200)

nombre= Label(text="Ingrese su nombre",font=("Impact", 17), fg="Black", bg="green")
nombre.pack()

entry1 = Entry()
entry1.config(font=("elephant",12), bg="Gray", fg="red", width=15)
entry1.place(x=157, y=70)


window.mainloop()


