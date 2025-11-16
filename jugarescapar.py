import pygame
import random
from Terrenos import Camino, Muro, Liana, Tunel
from Jugador import Jugador

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
                elif random.random() < 0.15:
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
    jugador = Jugador(jugador_x, jugador_y, TAMAÑO_CELDA)

    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Movimiento

            if event.type == pygame.KEYDOWN and not ganaste:
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
                if event.key == pygame.K_SPACE:
                    jugador.colocar_trampa(mapa, COLUMNAS, FILAS)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    jugador.activar_correr(False)




        screen.fill(NEGRO)
        dibujar_mapa(mapa)
        jugador.dibujar_barra_energia(screen, 20, 20, 200, 20)
        jugador.recuperar_energia()
        jugador.actualizar()
        jugador.dibujar(screen, AZUL)
        jugador.dibujar_trampas(screen)



        #salida
        pygame.draw.rect(screen, AMARILLO,
                         (salida_x * TAMAÑO_CELDA + 5,
                          salida_y * TAMAÑO_CELDA + 5,
                          TAMAÑO_CELDA - 10, TAMAÑO_CELDA - 10))

        if jugador.celda_x == salida_x and jugador.celda_y == salida_y:
            ganaste = True
            font = pygame.font.Font(None, 36)
            texto = font.render("¡GANASTE!", True, (255, 255, 255))
            screen.blit(texto, (ANCHO // 2 - 70, ALTO // 2 - 18))

        pygame.display.update()
        clock.tick(60)  # 60 FPS

    # Salir del juego
    pygame.quit()
    window.deiconify()
