import pygame

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
        self.cooldown_movimiento = 0.2
        self.trampas = []
        self.max_trampas = 3
        self.cooldown_trampa = 0

    def puede_moverse(self):

        tiempo_actual = pygame.time.get_ticks() / 1000.0  # Convertir a segundos
        tiempo_desde_ultimo = tiempo_actual - self.ultimo_movimiento
        puede_mover = tiempo_desde_ultimo >= self.cooldown_movimiento


        return puede_mover

    def iniciar_movimiento(self, direccion, mapa, columnas, filas):

        if self.en_movimiento or not self.puede_moverse():
            return False


        exito = False
        if self.corriendo:
            exito= self._iniciar_movimiento_completo(direccion, mapa, columnas, filas)
        else:
            exito= self.iniciar_movimiento_medio(direccion, mapa, columnas, filas)

        if exito:
            self.ultimo_movimiento = pygame.time.get_ticks() / 1000.0

        return exito

    def _iniciar_movimiento_completo(self, direccion, mapa, columnas, filas):
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
            self.energia -= 23
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
        if not self.en_movimiento:
            return False

        if self.movimiento_parcial:
            objetivo_x = self.destino_parcial_x
            objetivo_y = self.destino_parcial_y
        else:
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
            #LLego
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

    def dibujar_barra_energia(self, pantalla, x, y, ancho, alto):


        pygame.draw.rect(pantalla, (100, 100, 100), (x, y, ancho, alto))

        ancho_energia = (self.energia / 100) * ancho

        # Color según la energía
        if self.energia > 60:
            color = (0, 255, 0)  # Verde
        elif self.energia > 30:
            color = (255, 255, 0)  # Amarillo
        else:
            color = (255, 0, 0)  # Rojo

        # Barra actual
        pygame.draw.rect(pantalla, color, (x, y, ancho_energia, alto))

        # Borde
        pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho, alto), 2)

        # Texto opcional
        font = pygame.font.Font(None, 24)
        texto = font.render(f"Energía: {int(self.energia)}", True, (255, 255, 255))
        pantalla.blit(texto, (x, y - 25))



    def dibujar(self, pantalla, color):

        pygame.draw.circle(pantalla, color,
                           (int(self.pixel_x), int(self.pixel_y)),
                           self.tamaño_celda // 3)

    def get_posicion_celda(self):

        return (self.celda_x, self.celda_y)

    def puede_colocar_trampa(self):
        tiempo_actual = pygame.time.get_ticks()
        return (len(self.trampas) < self.max_trampas and
                tiempo_actual - self.cooldown_trampa >= 5000)


    def colocar_trampa(self, mapa, columnas, filas):
        if not self.puede_colocar_trampa():
            return False

        # Verificar que la celda actual sea transitable
        if (not mapa[self.celda_y][self.celda_x].transitable_jugador or
                self.celda_x == 0 or self.celda_x >= columnas - 1 or
                self.celda_y == 0 or self.celda_y >= filas - 1):
            return False

        # Verificar que no haya ya una trampa en esta posición
        for trampa in self.trampas:
            if trampa.celda_x == self.celda_x and trampa.celda_y == self.celda_y:
                return False


        nueva_trampa = Trampa(self.celda_x, self.celda_y, self.tamaño_celda)
        self.trampas.append(nueva_trampa)
        self.cooldown_trampa = pygame.time.get_ticks()

        return True

    def dibujar_trampas(self, pantalla):
        for trampa in self.trampas:
            trampa.dibujar(pantalla)

    def eliminar_trampa(self, index):
        if 0 <= index < len(self.trampas):
            del self.trampas[index]
            return True
        return False


class Trampa:
    def __init__(self, x, y, tamaño_celda):
        self.celda_x = x
        self.celda_y = y
        self.tamaño_celda = tamaño_celda
        self.color = (255, 0, 0)  # Rojo
        self.activa = True
        self.tiempo_colocacion = pygame.time.get_ticks()

    def dibujar(self, pantalla):
        if self.activa:
            x_pixel = self.celda_x * self.tamaño_celda
            y_pixel = self.celda_y * self.tamaño_celda

            # Dibujar un símbolo de trampa (X roja)
            pygame.draw.line(pantalla, self.color,
                             (x_pixel + 5, y_pixel + 5),
                             (x_pixel + self.tamaño_celda - 5, y_pixel + self.tamaño_celda - 5), 3)
            pygame.draw.line(pantalla, self.color,
                             (x_pixel + self.tamaño_celda - 5, y_pixel + 5),
                             (x_pixel + 5, y_pixel + self.tamaño_celda - 5), 3)