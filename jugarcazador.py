import pygame
import random
from Terrenos import Camino, Muro, Liana, Tunel
from Enemigos import Enemigo
from Jugador import Jugador
import tkinter as tk
import time


class ModoCazador:
    def __init__(self, mapa, jugador, enemigos, columnas, filas):
        self.mapa = mapa
        self.jugador = jugador
        self.enemigos = enemigos
        self.columnas = columnas
        self.filas = filas
        self.puntos = 0
        self.enemigos_eliminados = 0

    def actualizar_enemigos(self):
        jugador_pos = (self.jugador.celda_x, self.jugador.celda_y)

        for enemigo in self.enemigos:
            if enemigo.activo:
                # Los enemigos huyen del jugador
                enemigo.elegir_movimiento(self.mapa, self.columnas, self.filas, jugador_pos)
                enemigo.actualizar()

    def verificar_colisiones(self):
        for i, enemigo in enumerate(self.enemigos):
            if (enemigo.activo and
                    enemigo.celda_x == self.jugador.celda_x and
                    enemigo.celda_y == self.jugador.celda_y):
                # Jugador atrapó enemigo
                self.puntos += 100
                self.enemigos_eliminados += 1
                enemigo.activo = False
                enemigo.tiempo_muerte = pygame.time.get_ticks()
                return True
        return False

    def reaparecer_enemigos(self):
        jugador_pos = (self.jugador.celda_x, self.jugador.celda_y)

        for enemigo in self.enemigos:
            if not enemigo.activo and enemigo.puede_reaparecer():
                enemigo.reaparecer(self.mapa, self.columnas, self.filas, jugador_pos)

def jugar(window):

    window.withdraw()

    pygame.init()

    ANCHO, ALTO = 550, 550
    FILAS, COLUMNAS = 14, 14
    TAMAÑO_CELDA = 40

    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    VERDE_OSCURO = (0, 100, 0)
    MARRON = (139, 69, 19)
    AZUL = (0, 0, 255)
    AMARILLO = (255, 255, 0)

    HUD_ALTO = 70
    ANCHO, ALTO = 550, 550 + HUD_ALTO
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto")

    def generar_mapa():
        mapa = []
        for i in range(FILAS):
            fila = []
            for j in range(COLUMNAS):
                if i == 0 or i == FILAS - 1 or j == 0 or j == COLUMNAS - 1:
                    fila.append(Muro())  # Muro en bordes
                elif random.random() < 0.65:  # 65% de caminos
                    fila.append(Camino())  # Camino
                elif random.random() < 0.20:
                    fila.append(Tunel())  # tunel
                elif random.random() < 0.15:
                    fila.append(Liana())  # liana
                else:
                    fila.append(Muro())  # Muro
            mapa.append(fila)


        mapa[1][1] = Camino()  # Inicio
        mapa[FILAS - 2][COLUMNAS - 2] = Camino()  # Salida
        return mapa

    def elegir_puntos_inicio_y_salida(mapa):
        caminos = []
        for y in range(FILAS):
            for x in range(COLUMNAS):
                if mapa[y][x].transitable_jugador:  # Caminos o túneles
                    caminos.append((x, y))
        inicio = random.choice(caminos)
        caminos.remove(inicio)
        salida = random.choice(caminos)
        return inicio, salida

    def distancia(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def es_resoluble(mapa, x, y,salida, visitado):
        if (x, y) == salida:
            return True
        if x < 0 or x >= COLUMNAS or y < 0 or y >= FILAS:
            return False
        terreno = mapa[y][x]
        if not terreno.transitable_jugador or visitado[y][x]:
            return False

        visitado[y][x] = True

        return (es_resoluble(mapa, x + 1, y, salida, visitado) or
                es_resoluble(mapa, x - 1, y, salida, visitado) or
                es_resoluble(mapa, x, y + 1, salida, visitado) or
                es_resoluble(mapa, x, y - 1, salida, visitado))

    def generar_mapa_valido():
        while True:
            mapa = generar_mapa()
            inicio, salida = elegir_puntos_inicio_y_salida(mapa)
            if distancia(inicio, salida) < 10:
                continue  # Demasiado cerca, generar otro mapa
            visitado = [[False for _ in range(COLUMNAS)] for _ in range(FILAS)]
            if es_resoluble(mapa, inicio[0], inicio[1], salida, visitado):
                return mapa, inicio, salida

    def dibujar_mapa(mapa):
        for i in range(FILAS):
            for j in range(COLUMNAS):
                x = j * TAMAÑO_CELDA
                y = i * TAMAÑO_CELDA

                terreno = mapa[i][j]

                pygame.draw.rect(screen, terreno.color, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA))
                pygame.draw.rect(screen, (100, 100, 100), (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA), 1)


    mapa, (jugador_x, jugador_y), (salida_x, salida_y) = generar_mapa_valido()
    ganaste = False #Bandera para las teclas de movimiento
    perdiste = False
    jugador = Jugador(jugador_x, jugador_y, TAMAÑO_CELDA, modo="cazador")

    enemigos = []
    NUM_ENEMIGOS = 3
    for _ in range(NUM_ENEMIGOS):
        while True:
            x = random.randint(1, COLUMNAS - 2)
            y = random.randint(1, FILAS - 2)
            if (mapa[y][x].transitable_enemigo and
                    (x, y) != (jugador_x, jugador_y)):

                # Verifica que tenga al menos una salida libre
                vecinos_validos = 0
                direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                for dx, dy in direcciones:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < COLUMNAS and 0 <= ny < FILAS:
                        if mapa[y][x].transitable_enemigo:
                            vecinos_validos += 1
                if vecinos_validos > 0:
                    enemigos.append(Enemigo(x, y, TAMAÑO_CELDA, modo="cazador"))
                    break

    modo_cazador = ModoCazador(mapa, jugador, enemigos, COLUMNAS, FILAS)
    running = True
    clock = pygame.time.Clock()
    tiempo_inicio = time.time()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

                # Movimiento

            if event.type == pygame.KEYDOWN and not ganaste and not perdiste:
                if event.key == pygame.K_UP:
                    jugador.iniciar_movimiento("UP", mapa, COLUMNAS, FILAS)
                elif event.key == pygame.K_DOWN:
                    jugador.iniciar_movimiento("DOWN", mapa, COLUMNAS, FILAS)
                elif event.key == pygame.K_LEFT:
                    jugador.iniciar_movimiento("LEFT", mapa, COLUMNAS, FILAS)
                elif event.key == pygame.K_RIGHT:
                    jugador.iniciar_movimiento("RIGHT", mapa, COLUMNAS, FILAS)
                elif event.key == pygame.K_LSHIFT:
                    jugador.activar_correr(True)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    jugador.activar_correr(False)

        screen.fill(NEGRO)
        pygame.draw.rect(screen, (50, 50, 50), (0, 550, 550, HUD_ALTO))

        font = pygame.font.SysFont(None, 28)

        dibujar_mapa(mapa)
        dibujar_mapa(mapa)
        jugador.actualizar()
        jugador.dibujar(screen, AZUL)
        jugador.recuperar_energia()
        jugador.dibujar_barra_energia(screen, 20, 570, 200, 15)
        modo_cazador.actualizar_enemigos()
        modo_cazador.verificar_colisiones()
        modo_cazador.reaparecer_enemigos()

        for enemigo in enemigos:
            if enemigo.activo:
                enemigo.dibujar(screen)

        tiempo_transcurrido = time.time() - tiempo_inicio
        minutos = int(tiempo_transcurrido // 60)
        segundos = int(tiempo_transcurrido % 60)
        tiempo_formateado = f"{minutos:02d}:{segundos:02d}"

        texto_puntos = font.render(f"Puntos: {modo_cazador.puntos}", True, (255, 255, 0))
        texto_eliminados = font.render(f"Eliminados: {modo_cazador.enemigos_eliminados}", True, (255, 255, 255))
        texto_tiempo = font.render(f"Tiempo: {tiempo_formateado}", True, (255, 255, 255))
        texto_enemigos_activos = font.render(f"Enemigos: {sum(1 for e in enemigos if e.activo)}", True, (255, 255, 255))

        screen.blit(texto_puntos, (20, 590))
        screen.blit(texto_eliminados, (150, 590))
        screen.blit(texto_tiempo, (300, 570))
        screen.blit(texto_enemigos_activos, (300, 590))

        # DIBUJAR SALIDA
        salida_pixel_x = salida_x * TAMAÑO_CELDA + TAMAÑO_CELDA // 2
        salida_pixel_y = salida_y * TAMAÑO_CELDA + TAMAÑO_CELDA // 2
        pygame.draw.rect(screen, AMARILLO,
                         (salida_x * TAMAÑO_CELDA + 5,
                          salida_y * TAMAÑO_CELDA + 5,
                          TAMAÑO_CELDA - 10, TAMAÑO_CELDA - 10))



        pygame.display.update()
        clock.tick(60)  # 60 FPS



    # Salir del juego
    pygame.quit()

