import pygame
import random

class Enemigo:
    def __init__(self, celda_x, celda_y, tamaño_celda):
        self.celda_x = celda_x
        self.celda_y = celda_y
        self.celda_objetivo_x = celda_x
        self.celda_objetivo_y = celda_y
        self.en_movimiento = False
        self.movimiento_parcial = False
        self.velocidad = 3
        self.ultimo_movimiento = 0.0
        self.tamaño_celda = tamaño_celda
        self.pixel_x = celda_x * tamaño_celda + tamaño_celda // 2
        self.pixel_y = celda_y * tamaño_celda + tamaño_celda // 2
        self.color = (255, 255, 0)  # Amarillo

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color,
                           (int(self.pixel_x), int(self.pixel_y)),
                           self.tamaño_celda // 3)

    def elegir_movimiento_aleatorio(self, mapa, columnas, filas):
        if self.en_movimiento:
            return

        opciones = []
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in direcciones:
            nx = self.celda_x + dx
            ny = self.celda_y + dy
            if 0 <= nx < columnas and 0 <= ny < filas:
                if mapa[ny][nx].transitable_enemigo:
                    opciones.append((nx, ny))

        if opciones:
            nx, ny = random.choice(opciones)
            self.celda_objetivo_x = nx
            self.celda_objetivo_y = ny
            self.en_movimiento = True

    def actualizar(self):
        if not self.en_movimiento:
            return

        objetivo_x = self.celda_objetivo_x * self.tamaño_celda + self.tamaño_celda // 2
        objetivo_y = self.celda_objetivo_y * self.tamaño_celda + self.tamaño_celda // 2

        dx = objetivo_x - self.pixel_x
        dy = objetivo_y - self.pixel_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5
        velocidad_pixels = 2  # Velocidad en píxeles por actualización

        if distancia > velocidad_pixels:
            self.pixel_x += (dx / distancia) * velocidad_pixels
            self.pixel_y += (dy / distancia) * velocidad_pixels
        else:
            self.pixel_x = objetivo_x
            self.pixel_y = objetivo_y
            self.celda_x = self.celda_objetivo_x
            self.celda_y = self.celda_objetivo_y
            self.en_movimiento = False




