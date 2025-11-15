import pygame
import random

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
                    fila.append(1)  # Muro en bordes
                elif random.random() < 0.65:  # 65% de caminos
                    fila.append(0)  # Camino
                elif random.random() < 0.15:
                    fila.append(3)  # tunel
                elif random.random() < 0.15:
                    fila.append(2)  # liana
                else:
                    fila.append(1)  # Muro
            mapa.append(fila)


        mapa[1][1] = 0  # Inicio
        mapa[FILAS - 2][COLUMNAS - 2] = 0  # Salida
        return mapa

    def dibujar_mapa(mapa):
        for i in range(FILAS):
            for j in range(COLUMNAS):
                x = j * TAMAÑO_CELDA
                y = i * TAMAÑO_CELDA

                if mapa[i][j] == 0:  # Camino
                    color = GRIS
                elif mapa[i][j] == 1:  # Muro
                    color = NEGRO
                elif mapa[i][j] == 2:  # Lianas
                    color = VERDE_OSCURO
                else:  # Túneles
                    color = MARRON

                pygame.draw.rect(screen, color, (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA))
                pygame.draw.rect(screen, (100, 100, 100), (x, y, TAMAÑO_CELDA, TAMAÑO_CELDA), 1)


    mapa = generar_mapa()
    jugador_x, jugador_y = 1, 1


    running = True
    clock = pygame.time.Clock()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Movimiento
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and jugador_y > 0 and mapa[jugador_y - 1][jugador_x] in [0, 3]:
                    jugador_y -= 1
                elif event.key == pygame.K_DOWN and jugador_y < FILAS - 1 and mapa[jugador_y + 1][jugador_x] in [0, 3]:
                    jugador_y += 1
                elif event.key == pygame.K_LEFT and jugador_x > 0 and mapa[jugador_y][jugador_x - 1] in [0, 3]:
                    jugador_x -= 1
                elif event.key == pygame.K_RIGHT and jugador_x < COLUMNAS - 1 and mapa[jugador_y][jugador_x + 1] in [0,
                                                                                                                     3]:
                    jugador_x += 1
                elif event.key == pygame.K_ESCAPE:  # Salir con ESC
                    running = False


        screen.fill(NEGRO)
        dibujar_mapa(mapa)

        #jugador
        pygame.draw.circle(screen, AZUL,
                           (jugador_x * TAMAÑO_CELDA + TAMAÑO_CELDA // 2,
                            jugador_y * TAMAÑO_CELDA + TAMAÑO_CELDA // 2),
                           TAMAÑO_CELDA // 3)

        #salida
        pygame.draw.rect(screen, AMARILLO,
                         ((COLUMNAS - 2) * TAMAÑO_CELDA + 5,
                          (FILAS - 2) * TAMAÑO_CELDA + 5,
                          TAMAÑO_CELDA - 10, TAMAÑO_CELDA - 10))


        if jugador_x == COLUMNAS - 2 and jugador_y == FILAS - 2:
            font = pygame.font.Font(None, 36)
            texto = font.render("¡GANASTE!", True, (255, 255, 255))
            screen.blit(texto, (ANCHO // 2 - 70, ALTO // 2 - 18))

        pygame.display.update()
        clock.tick(60)  # 60 FPS

    # Salir del juego
    pygame.quit()
    window.deiconify()
