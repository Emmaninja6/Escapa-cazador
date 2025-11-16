import pygame
import random
from Terrenos import Camino, Muro, Liana, Tunel


class Jugador:
    def __init__(self, x, y, tamaño_celda):
        # Posición en celdas
        self.celda_x = x
        self.celda_y = y
        # Posición en píxeles
        self.pixel_x = x * tamaño_celda + tamaño_celda // 2
        self.pixel_y = y * tamaño_celda + tamaño_celda // 2
        # Movimiento
        self.velocidad = 3
        self.en_movimiento = False
        self.celda_objetivo_x = x
        self.celda_objetivo_y = y
        self.movimiento_parcial = False
        self.destino_parcial_x = self.pixel_x
        self.destino_parcial_y = self.pixel_y
        # correr
        self.corriendo= False
        self.energia = 100
        self.cansancio = False
        self.tamaño_celda = tamaño_celda
        self.ultimo_movimiento = 0  # Tiempo del último movimiento
        self.cooldown_movimiento = 0.2  # Segundos entre movimientos

    def puede_moverse(self):
        """Verifica si puede iniciar nuevo movimiento (cooldown)"""
        tiempo_actual = pygame.time.get_ticks() / 1000.0  # Convertir a segundos
        tiempo_desde_ultimo = tiempo_actual - self.ultimo_movimiento
        puede_mover = tiempo_desde_ultimo >= self.cooldown_movimiento

        if not puede_mover:
            print(f"Cooldown activo. Tiempo restante: {self.cooldown_movimiento - tiempo_desde_ultimo:.2f}s")

        return puede_mover

    def iniciar_movimiento(self, direccion, mapa, columnas, filas):
        """Inicia movimiento según el modo actual (normal o correr)"""

        if self.en_movimiento or not self.puede_moverse():
            return False


        exito = False
        if self.corriendo:
            exito= self._iniciar_movimiento_completo(direccion, mapa, columnas, filas)
        else:
            exito= self.iniciar_movimiento_medio(direccion, mapa, columnas, filas)

        if exito:
            self.ultimo_movimiento = pygame.time.get_ticks() / 1000.0
            print(f"Movimiento exitoso. Cooldown aplicado: {self.ultimo_movimiento}")

        return exito

    def _iniciar_movimiento_completo(self, direccion, mapa, columnas, filas):
        """Movimiento de UNA casilla completa (para correr)"""
        nuevo_x, nuevo_y = self.celda_x, self.celda_y

        if direccion == "UP":
            nuevo_y -= 1
        elif direccion == "DOWN":
            nuevo_y += 1
        elif direccion == "LEFT":
            nuevo_x -= 1
        elif direccion == "RIGHT":
            nuevo_x += 1

        if self.corriendo:
            self.energia -= 25
            print(f"Energía consumida: {self.energia}")
            if self.energia <= 0:
                self.energia = 0
                self.cansancio = True
                self.activar_correr(False)
                return False

        # Verificar si puede moverse ahí
        if (nuevo_x < 0 or nuevo_x >= columnas or
                nuevo_y < 0 or nuevo_y >= filas or
                not mapa[nuevo_y][nuevo_x].transitable_jugador):
            return False

        self.celda_objetivo_x = nuevo_x
        self.celda_objetivo_y = nuevo_y
        self.movimiento_parcial = False
        self.en_movimiento = True
        return True



    def iniciar_movimiento_medio(self, direccion, mapa, columnas, filas):
        """Inicia un movimiento de MEDIA casilla"""
        if self.en_movimiento:
            return False

        # Calcular destino de media casilla
        medio_celda = self.tamaño_celda / 2
        nuevo_pixel_x = self.pixel_x
        nuevo_pixel_y = self.pixel_y

        if direccion == "UP":
            nuevo_pixel_y -= medio_celda
        elif direccion == "DOWN":
            nuevo_pixel_y += medio_celda
        elif direccion == "LEFT":
            nuevo_pixel_x -= medio_celda
        elif direccion == "RIGHT":
            nuevo_pixel_x += medio_celda

        # Convertir a coordenadas de celda para verificación
        celda_x = int(nuevo_pixel_x / self.tamaño_celda)
        celda_y = int(nuevo_pixel_y / self.tamaño_celda)

        # Verificar si puede moverse ahí
        if (celda_x < 0 or celda_x >= columnas or
                celda_y < 0 or celda_y >= filas or
                not mapa[celda_y][celda_x].transitable_jugador):
            return False

        # Establecer destino parcial
        self.destino_parcial_x = nuevo_pixel_x
        self.destino_parcial_y = nuevo_pixel_y
        self.movimiento_parcial = True
        self.en_movimiento = True
        return True


    def actualizar(self):
        """Actualiza la posición del jugador cada frame"""
        if not self.en_movimiento:
            return False

        if self.movimiento_parcial:
            # Movimiento hacia destino parcial
            objetivo_x = self.destino_parcial_x
            objetivo_y = self.destino_parcial_y
        else:
            # Movimiento hacia celda completa
            objetivo_x = self.celda_objetivo_x * self.tamaño_celda + self.tamaño_celda // 2
            objetivo_y = self.celda_objetivo_y * self.tamaño_celda + self.tamaño_celda // 2

        dx = objetivo_x - self.pixel_x
        dy = objetivo_y - self.pixel_y
        distancia = (dx ** 2 + dy ** 2) ** 0.5

        if distancia > self.velocidad:
            self.pixel_x += (dx / distancia) * self.velocidad
            self.pixel_y += (dy / distancia) * self.velocidad
            return True
        else:
            # Llegó al destino
            self.pixel_x = objetivo_x
            self.pixel_y = objetivo_y

            if self.movimiento_parcial:
                # Actualizar posición en celdas (aproximada)
                self.celda_x = int(self.pixel_x / self.tamaño_celda)
                self.celda_y = int(self.pixel_y / self.tamaño_celda)
                self.movimiento_parcial = False
            else:
                # Movimiento completo a celda
                self.celda_x = self.celda_objetivo_x
                self.celda_y = self.celda_objetivo_y

            self.en_movimiento = False
            return False

    def activar_correr(self,activar):
        if activar and self.energia > 0 and not self.cansancio:
            self.corriendo = True
            self.movimiento_parcial = False  # Casilla completa
            self.velocidad = 6
        else:
            self.corriendo = False
            self.movimiento_parcial = True  # Media casilla
            self.velocidad = 3

    def recuperar_energia(self):
        if not self.corriendo and self.energia < 100:
            self.energia += 0.5
        if self.energia >= 30:
            self.cansancio = False

    def dibujar(self, pantalla, color):

        pygame.draw.circle(pantalla, color,
                           (int(self.pixel_x), int(self.pixel_y)),
                           self.tamaño_celda // 3)

    def get_posicion_celda(self):

        return (self.celda_x, self.celda_y)


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

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LSHIFT:
                    jugador.activar_correr(False)




        screen.fill(NEGRO)
        dibujar_mapa(mapa)
        jugador.recuperar_energia()
        jugador.actualizar()
        jugador.dibujar(screen, AZUL)



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
