import pygame
import random
from Terrenos import Camino, Muro, Liana, Tunel
from Enemigos import Enemigo
from Jugador import Jugador
import tkinter as tk
import time
import configuracion
import os

RUTA_PUNTAJES_CAZADOR = "puntajes_cazador.txt"

def guardar_puntaje_cazador(nombre, puntos):
    nombre = nombre.strip()
    if not nombre:
        nombre = "Jugador"

    puntajes = []
    if os.path.exists(RUTA_PUNTAJES_CAZADOR):
        with open(RUTA_PUNTAJES_CAZADOR, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                n, pts = linea.rsplit(",", 1)
                try:
                    pts = int(pts)
                    puntajes.append((n, pts))
                except ValueError:
                    continue

    puntajes.append((nombre, puntos))
    puntajes.sort(key=lambda x: x[1], reverse=True)
    puntajes = puntajes[:5]

    with open(RUTA_PUNTAJES_CAZADOR, "w", encoding="utf-8") as f:
        for n, p in puntajes:
            f.write(f"{n},{p}\n")

def calcular_puntaje_cazador(puntos_actuales, enemigos_eliminados, enemigos_escapados, tiempo_restante, dificultad):

        puntos_base = puntos_actuales

        bonificacion_tiempo = int(tiempo_restante * 2)

        penalizacion_escape = enemigos_escapados * 50
        if dificultad == "Dificil":
            penalizacion_escape = enemigos_escapados * 75

        # Multiplicador por dificultad
        if dificultad == "Facil":
            multiplicador = 0.8  # Menos puntos en fácil
        elif dificultad == "Medio":
            multiplicador = 1.0
        else:  # Dificil
            multiplicador = 1.5  # Más puntos en difícil

        puntaje_final = int((puntos_base + bonificacion_tiempo - penalizacion_escape) * multiplicador)

        return max(0, puntaje_final)

class ModoCazador:
    def __init__(self, mapa, jugador, enemigos, columnas, filas, salida_x, salida_y):
        self.mapa = mapa
        self.jugador = jugador
        self.enemigos = enemigos
        self.columnas = columnas
        self.filas = filas
        self.salida_x = salida_x
        self.salida_y = salida_y
        self.puntos = 0
        self.enemigos_eliminados = 0
        self.enemigos_escapados = 0

    def actualizar_enemigos(self):
        jugador_pos = (self.jugador.celda_x, self.jugador.celda_y)
        salida_pos = (self.salida_x, self.salida_y)

        for enemigo in self.enemigos:
            if enemigo.activo:
                # Los enemigos huyen del jugador
                if not enemigo.en_movimiento:
                    enemigo.elegir_movimiento_hacia_salida(self.mapa, self.columnas, self.filas, jugador_pos,
                                                           salida_pos)
                enemigo.actualizar()

    def verificar_colisiones(self,puntos_por_eliminacion):
        for i, enemigo in enumerate(self.enemigos):
            if (enemigo.activo and
                    enemigo.celda_x == self.jugador.celda_x and
                    enemigo.celda_y == self.jugador.celda_y):
                # Jugador atrapó enemigo
                self.puntos += puntos_por_eliminacion
                self.enemigos_eliminados += 1
                enemigo.activo = False
                enemigo.tiempo_muerte = pygame.time.get_ticks()
                return True
        return False

    def verificar_escapadas(self, puntos_por_escape):
        for enemigo in self.enemigos:
            if (enemigo.activo and
                    enemigo.celda_x == self.salida_x and
                    enemigo.celda_y == self.salida_y):
                # Enemigo llegó a la salida
                self.puntos -= puntos_por_escape
                self.enemigos_escapados += 1
                enemigo.activo = False
                enemigo.tiempo_muerte = pygame.time.get_ticks()
                return True
        return False

    def reaparecer_enemigos(self):
        jugador_pos = (self.jugador.celda_x, self.jugador.celda_y)

        for enemigo in self.enemigos:
            if not enemigo.activo and enemigo.puede_reaparecer():
                enemigo.reaparecer(self.mapa, self.columnas, self.filas, jugador_pos)

def mostrar_resultado_cazador_tk(mensaje, puntos, enemigos_eliminados, enemigos_escapados, tiempo_final, window):
    resultado = tk.Toplevel(window)
    resultado.title("Resultado Final - Modo Cazador")
    resultado.geometry("450x450")
    resultado.resizable(width=False, height=False)
    resultado.configure(bg="#2E8B57")  # Verde más oscuro

    # Frame principal
    frame = tk.Frame(resultado, bg="#2E8B57")
    frame.pack(expand=True, fill='both', padx=20, pady=20)

    # Título principal
    label_titulo = tk.Label(frame, text=mensaje,
                            font=("Impact", 24), bg="#2E8B57", fg="white")
    label_titulo.pack(pady=10)

    # Línea separadora
    separator = tk.Frame(frame, height=2, bg="white")
    separator.pack(fill='x', pady=5)

    # Información de estadísticas
    minutos = int(tiempo_final // 60)
    segundos = int(tiempo_final % 60)

    stats_text = f"""
    Tiempo total: {minutos:02d}:{segundos:02d}

    Puntos obtenidos: {puntos}

    Enemigos eliminados: {enemigos_eliminados}

    Enemigos escapados: {enemigos_escapados}
    """

    label_stats = tk.Label(frame, text=stats_text,
                           font=("Impact", 14), bg="#2E8B57", fg="white",
                           justify='left')
    label_stats.pack(pady=15)

    # Botón de salir
    boton_salir = tk.Button(frame, text="Volver al Menú Principal",
                            command=lambda: [resultado.destroy(), window.deiconify()],
                            font=("Arial", 12), bg="#FF6B35", fg="white")
    boton_salir.pack(pady=20)

    window.withdraw()

def jugar(window,nombre_jugador):

    window.withdraw()

    pygame.init()

    pygame.mixer.init()

    ANCHO, ALTO = 550, 550
    FILAS, COLUMNAS = 14, 14
    TAMAÑO_CELDA = 40

    NEGRO = (0, 0, 0)
    GRIS = (200, 200, 200)
    VERDE_OSCURO = (0, 100, 0)
    MARRON = (139, 69, 19)
    AZUL = (0, 0, 255)
    AMARILLO = (255, 255, 0)

    TIEMPO_LIMITE = 180
    HUD_ALTO = 70
    ANCHO, ALTO = 550, 550 + HUD_ALTO
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto")

    try:
        pygame.mixer.music.load("persecucion.mp3")  # Cambia por el nombre de tu archivo
        pygame.mixer.music.set_volume(0.5)  # Volumen entre 0.0 y 1.0
        pygame.mixer.music.play(-1)  # -1 significa loop infinito
    except pygame.error as e:
        print(f"No se pudo cargar la música: {e}")

    try:
        dificultad = configuracion.dificultad_actual
    except AttributeError:
        dificultad = "Medio"

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
    if dificultad == "Facil":
        NUM_ENEMIGOS = 1
        velocidad_enemigo = 1
        PUNTOS_POR_ELIMINACION = 50  # Menos puntos en fácil
        PUNTOS_POR_ESCAPE = 25
    elif dificultad == "Dificil":
        NUM_ENEMIGOS = 5
        velocidad_enemigo = 5
        PUNTOS_POR_ELIMINACION = 100 # Más puntos en difícil
        PUNTOS_POR_ESCAPE = 50
    else:  # Medio
        NUM_ENEMIGOS = 3
        velocidad_enemigo = 3
        PUNTOS_POR_ELIMINACION = 75  # Puntos estándar
        PUNTOS_POR_ESCAPE = 35


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
                    nuevo_enemigo = Enemigo(x, y, TAMAÑO_CELDA, modo="cazador")
                    nuevo_enemigo.velocidad = velocidad_enemigo  # Aplicar velocidad según dificultad
                    enemigos.append(nuevo_enemigo)
                    break

    modo_cazador = ModoCazador(mapa, jugador, enemigos, COLUMNAS, FILAS, salida_x, salida_y)
    running = True
    clock = pygame.time.Clock()
    tiempo_inicio = time.time()

    while running:
        tiempo_transcurrido = time.time() - tiempo_inicio
        tiempo_restante = max(0, TIEMPO_LIMITE - tiempo_transcurrido)

        if tiempo_restante <= 0 and not ganaste:
            ganaste = True  # Tiempo terminado - fin del juego
            tiempo_final = TIEMPO_LIMITE


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
        jugador.actualizar()
        jugador.dibujar(screen, AZUL)
        jugador.recuperar_energia()
        jugador.dibujar_barra_energia(screen, 20, 570, 200, 15)
        if not ganaste and tiempo_restante > 0:
            modo_cazador.actualizar_enemigos()
            modo_cazador.verificar_colisiones(PUNTOS_POR_ELIMINACION)
            modo_cazador.verificar_escapadas(PUNTOS_POR_ESCAPE)
            modo_cazador.reaparecer_enemigos()

        for enemigo in enemigos:
            if enemigo.activo:
                enemigo.dibujar(screen)

        minutos_rest = int(tiempo_restante // 60)
        segundos_rest = int(tiempo_restante % 60)
        tiempo_restante_formateado = f"{minutos_rest:02d}:{segundos_rest:02d}"

        texto_puntos = font.render(f"Puntos: {modo_cazador.puntos}", True, (255, 255, 0))
        texto_eliminados = font.render(f"Eliminados: {modo_cazador.enemigos_eliminados}", True, (255, 255, 255))
        texto_tiempo_restante = font.render(f"Restante: {tiempo_restante_formateado}", True,
                                            (255, 255, 255) if tiempo_restante > 30 else (255, 100, 100))
        texto_enemigos_activos = font.render(f"Enemigos: {sum(1 for e in enemigos if e.activo)}", True, (255, 255, 255))
        texto_escapados = font.render(f"Escapados: {modo_cazador.enemigos_escapados}", True, (255, 100, 100))

        screen.blit(texto_escapados, (220, 570))
        screen.blit(texto_puntos, (20, 590))
        screen.blit(texto_eliminados, (220, 590))
        screen.blit(texto_tiempo_restante, (350, 570))
        screen.blit(texto_enemigos_activos, (350, 590))

        # DIBUJAR SALIDA
        salida_pixel_x = salida_x * TAMAÑO_CELDA + TAMAÑO_CELDA // 2
        salida_pixel_y = salida_y * TAMAÑO_CELDA + TAMAÑO_CELDA // 2
        pygame.draw.rect(screen, AMARILLO,
                         (salida_x * TAMAÑO_CELDA + 5,
                          salida_y * TAMAÑO_CELDA + 5,
                          TAMAÑO_CELDA - 10, TAMAÑO_CELDA - 10))

        if ganaste and tiempo_restante <= 0:
            font_fin = pygame.font.Font(None, 36)
            texto_fin = font_fin.render("¡TIEMPO AGOTADO!", True, (255, 255, 0))
            screen.blit(texto_fin, (ANCHO // 2 - 120, ALTO // 2 - 18))


        pygame.display.update()
        clock.tick(60)  # 60 FPS
        if ganaste:
            pygame.display.update()
            pygame.time.delay(2000)  # Esperar 2 segundos antes de mostrar resultados
            running = False


    puntaje_final = calcular_puntaje_cazador(
        modo_cazador.puntos,
        modo_cazador.enemigos_eliminados,
        modo_cazador.enemigos_escapados,
        tiempo_restante,  # Este valor ya lo tienes
        dificultad
    )
    pygame.mixer.music.stop()
    # Salir del juego
    pygame.quit()


    guardar_puntaje_cazador(nombre_jugador, puntaje_final)
    if ganaste:
        mostrar_resultado_cazador_tk("¡TIEMPO AGOTADO!",
                                     puntaje_final,
                                     modo_cazador.enemigos_eliminados,
                                     modo_cazador.enemigos_escapados,
                                     TIEMPO_LIMITE,
                                     window)
