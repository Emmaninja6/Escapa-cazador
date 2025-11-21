import pygame
import random
from Terrenos import Camino, Muro, Liana, Tunel

class Enemigo:
    def __init__(self, celda_x, celda_y, tamaño_celda,modo="escapar"):
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
        self.activo = True
        self.tiempo_muerte = 0
        self.modo = modo  # "escapar" o "cazador"

    def elegir_movimiento(self, mapa, columnas, filas, jugador_pos=None):
        if self.modo == "escapar":
            self.elegir_movimiento_aleatorio(mapa, columnas, filas,jugador_pos)
        elif self.modo == "cazador" and jugador_pos:
            self.elegir_movimiento_huida(mapa, columnas, filas, jugador_pos)

    def dibujar(self, pantalla):
        pygame.draw.circle(pantalla, self.color,
                           (int(self.pixel_x), int(self.pixel_y)),
                           self.tamaño_celda // 3)

    def elegir_movimiento_aleatorio(self, mapa, columnas, filas,jugador_pos):
        if self.en_movimiento or not self.activo:
            return

        jugador_x, jugador_y = jugador_pos
        opciones = []
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in direcciones:
            nx = self.celda_x + dx
            ny = self.celda_y + dy
            if (0 <= nx < columnas and 0 <= ny < filas and
                    self._es_transitable_para_modo(mapa, nx, ny)):
                # Calcular distancia al jugador (queremos minimizarla)
                dist = abs(nx - jugador_x) + abs(ny - jugador_y)
                opciones.append((nx, ny, dist))

        if opciones:
            # Elegir la dirección que más acerque al jugador
            opciones.sort(key=lambda x: x[2])  # Orden ascendente (menor distancia primero)
            nx, ny, _ = opciones[0]
            self.celda_objetivo_x = nx
            self.celda_objetivo_y = ny
            self.en_movimiento = True

    def elegir_movimiento_huida(self, mapa, columnas, filas, jugador_pos):
        if self.en_movimiento or not self.activo:
            return

        jugador_x, jugador_y = jugador_pos
        opciones = []
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        for dx, dy in direcciones:
            nx = self.celda_x + dx
            ny = self.celda_y + dy
            if (0 <= nx < columnas and 0 <= ny < filas and
                    self._es_transitable_para_modo(mapa, nx, ny)):
                # Calcular distancia al jugador
                dist = abs(nx - jugador_x) + abs(ny - jugador_y)
                opciones.append((nx, ny, dist))

        if opciones:
            # Elegir la dirección que más aleje del jugador
            opciones.sort(key=lambda x: x[2], reverse=True)
            nx, ny, _ = opciones[0]
            self.celda_objetivo_x = nx
            self.celda_objetivo_y = ny
            self.en_movimiento = True

    def elegir_movimiento_hacia_salida(self, mapa, columnas, filas, jugador_pos, salida_pos):
        if self.en_movimiento or not self.activo:
            return

        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Arriba, abajo, izquierda, derecha
        movimientos_validos = []

        # Calcular distancia actual a la salida y al jugador
        dist_a_salida_actual = abs(self.celda_x - salida_pos[0]) + abs(self.celda_y - salida_pos[1])
        dist_al_jugador_actual = abs(self.celda_x - jugador_pos[0]) + abs(self.celda_y - jugador_pos[1])

        for dx, dy in direcciones:
            nueva_x = self.celda_x + dx
            nueva_y = self.celda_y + dy

            if (0 <= nueva_x < columnas and 0 <= nueva_y < filas and
                    self._es_transitable_para_modo(mapa, nueva_x, nueva_y)):

                # Calcular nuevas distancias
                nueva_dist_a_salida = abs(nueva_x - salida_pos[0]) + abs(nueva_y - salida_pos[1])
                nueva_dist_al_jugador = abs(nueva_x - jugador_pos[0]) + abs(nueva_y - jugador_pos[1])

                # Sistema de puntuación por movimiento
                puntuacion = 0

                # PRIORIDAD 1: Si está muy cerca de la salida (2 casillas o menos), ESCAPAR
                if dist_a_salida_actual <= 2:
                    if nueva_dist_a_salida < dist_a_salida_actual:  # Se acerca a la salida
                        puntuacion += 100  # Máxima prioridad
                    elif nueva_dist_a_salida == dist_a_salida_actual:  # Se mantiene igual de cerca
                        puntuacion += 50
                    else:  # Se aleja de la salida
                        puntuacion -= 100

                # PRIORIDAD 2: Si el jugador está muy cerca (3 casillas o menos), HUIR
                elif dist_al_jugador_actual <= 3:
                    if nueva_dist_al_jugador > dist_al_jugador_actual:  # Se aleja del jugador
                        puntuacion += 80
                    elif nueva_dist_al_jugador == dist_al_jugador_actual:  # Se mantiene igual de lejos
                        puntuacion += 30
                    else:  # Se acerca al jugador
                        puntuacion -= 80

                # PRIORIDAD 3: Situación normal - buscar salida
                else:
                    if nueva_dist_a_salida < dist_a_salida_actual:  # Se acerca a la salida
                        puntuacion += 60
                    elif nueva_dist_a_salida == dist_a_salida_actual:  # Se mantiene igual
                        puntuacion += 20
                    else:  # Se aleja de la salida
                        puntuacion -= 40

                    # Bonus pequeño por alejarse del jugador
                    if nueva_dist_al_jugador > dist_al_jugador_actual:
                        puntuacion += 10

                movimientos_validos.append((dx, dy, puntuacion, nueva_dist_a_salida))

        if movimientos_validos:
            # Ordenar por puntuación descendente (mejores movimientos primero)
            movimientos_validos.sort(
                key=lambda x: (-x[2], x[3]))  # Primero por puntuación, luego por distancia a salida

            mejor_mov = movimientos_validos[0]

            # Solo moverse si la puntuación es positiva (evita movimientos "suicidas")
            if mejor_mov[2] > 0:
                self.celda_objetivo_x = self.celda_x + mejor_mov[0]
                self.celda_objetivo_y = self.celda_y + mejor_mov[1]
                self.en_movimiento = True
            else:
                # Si todos los movimientos son malos, quedarse quieto
                self.en_movimiento = False
        else:
            self.en_movimiento = False

    def actualizar(self):
        if not self.activo or not self.en_movimiento:
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

    def puede_reaparecer(self):
        if not self.activo:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_transcurrido = (tiempo_actual - self.tiempo_muerte) / 1000.0  # Convertir a segundos
            return tiempo_transcurrido >= 10.0  # 10 segundos
        return False

    def reaparecer(self, mapa, columnas, filas, jugador_pos):

        intentos = 0
        while intentos < 50:  # Límite de intentos
            x = random.randint(1, columnas - 2)
            y = random.randint(1, filas - 2)

            # posición sea válida
            if (mapa[y][x].transitable_enemigo and
                    (x, y) != jugador_pos and
                    self._tiene_vecinos_validos(x, y, mapa, columnas, filas)):
                self.celda_x = x
                self.celda_y = y
                self.pixel_x = x * self.tamaño_celda + self.tamaño_celda // 2
                self.pixel_y = y * self.tamaño_celda + self.tamaño_celda // 2
                self.celda_objetivo_x = x
                self.celda_objetivo_y = y
                self.en_movimiento = False
                self.activo = True
                return True
            intentos += 1
        return False

    def _tiene_vecinos_validos(self, x, y, mapa, columnas, filas):
        direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
        for dx, dy in direcciones:
            nx = x + dx
            ny = y + dy
            if 0 <= nx < columnas and 0 <= ny < filas:
                if self._es_transitable_para_modo(mapa, nx, ny):
                    return True
        return False

    def _es_transitable_para_modo(self, mapa, x, y):
        """Verifica si la celda es transitable según el modo"""
        terreno = mapa[y][x]

        if self.modo == "cazador":
            # En modo cazador: enemigos pueden pasar por Caminos y Túneles
            return isinstance(terreno, Camino) or isinstance(terreno, Tunel)
        else:  # modo escapar
            # En modo escapar: enemigos pueden pasar por Caminos y Lianas
            return isinstance(terreno, Camino) or isinstance(terreno, Liana)




