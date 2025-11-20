import pygame
import random
from Terrenos import Camino, Muro, Liana, Tunel
from Jugador import Jugador
from Enemigos import Enemigo
import tkinter as tk
import time
import configuracion
import puntajes
import os

RUTA_PUNTAJES_ESCAPA = "puntajes_escape.txt"

def guardar_puntaje_escapa(nombre, puntos):
    nombre = nombre.strip()
    print("Guardando puntaje para:", repr(nombre))  # debug

    if not nombre:
        nombre = "Jugador"

    # Leer los existentes
    puntajes = []
    if os.path.exists(RUTA_PUNTAJES_ESCAPA):
        with open(RUTA_PUNTAJES_ESCAPA, "r", encoding="utf-8") as f:
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

    with open(RUTA_PUNTAJES_ESCAPA, "w", encoding="utf-8") as f:
        for n, p in puntajes:
            f.write(f"{n},{p}\n")

def jugar(window, nombre_jugador):

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
    PUNTOS_POR_TRAMPA = 50

    HUD_ALTO = 70
    ANCHO, ALTO = 550, 550 + HUD_ALTO
    screen = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Escapa del Laberinto")
    tiempo_inicio = time.time()
    tiempo_transcurrido = 0

    try:
        dificultad = configuracion.dificultad_actual
    except AttributeError:
        dificultad = "Medio"

    def mostrar_resultado_tk(mensaje, tiempo_final=0, puntos_trampas=0, puntaje_total=0):
        resultado = tk.Toplevel(window)
        resultado.title("Resultado Final")
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
        Tiempo: {minutos:02d}:{segundos:02d}

        Puntos por trampas: {puntos_trampas}

        Puntaje total: {puntaje_total}
        """

        label_stats = tk.Label(frame, text=stats_text,
                               font=("Impact", 14), bg="#2E8B57", fg="white",
                               justify='left')
        label_stats.pack(pady=15)

        # Botón de salir
        boton_salir = tk.Button(frame, text="Volver al Menú Principal",
                                command=lambda: [resultado.destroy(), window.deiconify()],
                                font=("Arial", 12), bg="#FF6B35", fg="white",)

        boton_salir.place(x=100, y=300)

        window.withdraw()

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
    perdiste = False
    jugador = Jugador(jugador_x, jugador_y, TAMAÑO_CELDA, modo="escapar")

    enemigos = []

    # Ajustar parámetros según dificultad
    if dificultad == "Facil":
        NUM_ENEMIGOS = 1
        velocidad_enemigo = 1
    elif dificultad == "Dificil":
        NUM_ENEMIGOS = 5
        velocidad_enemigo = 5
    else:  # Medio
        NUM_ENEMIGOS = 3
        velocidad_enemigo = 3

    # Puntos por trampa según dificultad
    if dificultad == "Facil":
        PUNTOS_POR_TRAMPA = 25
    elif dificultad == "Dificil":
        PUNTOS_POR_TRAMPA = 75
    else:  # Medio
        PUNTOS_POR_TRAMPA = 50

    for _ in range(NUM_ENEMIGOS):
        while True:
            x = random.randint(1, COLUMNAS - 2)
            y = random.randint(1, FILAS - 2)
            if (
                    mapa[y][x].transitable_enemigo and (x, y) != (jugador_x, jugador_y)
            ):
                # Verifica que tenga al menos una salida libre
                vecinos_validos = 0
                direcciones = [(0, -1), (0, 1), (-1, 0), (1, 0)]
                for dx, dy in direcciones:
                    nx = x + dx
                    ny = y + dy
                    if 0 <= nx < COLUMNAS and 0 <= ny < FILAS:
                        if mapa[ny][nx].transitable_enemigo:
                            vecinos_validos += 1
                if vecinos_validos > 0:
                    ocupado = any(e.celda_x == x and e.celda_y == y for e in enemigos)
                    if ocupado:
                        continue

                    nuevo_enemigo = Enemigo(x, y, TAMAÑO_CELDA)
                    nuevo_enemigo.velocidad = velocidad_enemigo
                    enemigos.append(nuevo_enemigo)
                    break

    running = True
    clock = pygame.time.Clock()

    juego_iniciado = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Movimiento

            if event.type == pygame.KEYDOWN and not ganaste and not perdiste:
                juego_iniciado = True


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
        pygame.draw.rect(screen, (50, 50, 50), (0, 550, 550, HUD_ALTO))

        font = pygame.font.SysFont(None, 28)

        # Calcula valores actuales
        energia = jugador.energia
        trampas_disponibles = jugador.max_trampas - len(jugador.trampas)
        puntaje = jugador.puntos_trampas

        tiempo_transcurrido = time.time() - tiempo_inicio

        # Convertir a formato minutos:segundos
        minutos = int(tiempo_transcurrido // 60)
        segundos = int(tiempo_transcurrido % 60)
        tiempo_formateado = f"{minutos:02d}:{segundos:02d}"

        # Cálculo del cooldown de trampas (en segundos)
        if jugador.cooldown_trampa is None:
            cooldown_seg = 0  # Sin cooldown activo aún
        else:
            tiempo_actual = pygame.time.get_ticks()
            tiempo_desde_ultima = tiempo_actual - jugador.cooldown_trampa
            tiempo_restante_ms = 5000 - tiempo_desde_ultima

            if tiempo_restante_ms <= 0:
                cooldown_seg = 0
            else:
                cooldown_seg = tiempo_restante_ms // 1000

        texto_trampas = font.render(f"Trampas: {trampas_disponibles}", True, (255, 255, 255))
        texto_puntos = font.render(f"Puntos: {puntaje}", True, (255, 255, 0))
        texto_cooldown = font.render(f"Cooldown: {cooldown_seg}s", True, (255, 100, 100))
        texto_tiempo = font.render(f"Tiempo: {tiempo_formateado}", True, (255, 255, 255))

        # textos en el HUD
        screen.blit(texto_trampas, (230, 570))
        screen.blit(texto_puntos, (350, 570))
        screen.blit(texto_cooldown, (230, 590))
        screen.blit(texto_tiempo, (375, 590))

        dibujar_mapa(mapa)
        dibujar_mapa(mapa)
        jugador.dibujar_barra_energia(screen, 20, 590, 200, 20)
        jugador.recuperar_energia()
        jugador.actualizar()
        jugador.dibujar(screen, AZUL)
        jugador.dibujar_trampas(screen)



        # Elementos relacionados a los enemigos y trampas

        # Enemigos que pisan trampas
        for enemigo in enemigos:
            if not enemigo.activo:
                continue

            for trampa in jugador.trampas:
                if (enemigo.celda_x == trampa.celda_x and
                        enemigo.celda_y == trampa.celda_y and
                        trampa.activa):
                    enemigo.activo = False
                    enemigo.tiempo_muerte = pygame.time.get_ticks()
                    jugador.puntos_trampas += PUNTOS_POR_TRAMPA
                    trampa.activa = False
                    break

        # Eliminar todas las trampas inactivas de una vez
        jugador.trampas = [t for t in jugador.trampas if t.activa]

        # Manejar reaparición de enemigos
        for enemigo in enemigos:
                if not enemigo.activo and enemigo.puede_reaparecer():
                    jugador_pos = (jugador.celda_x, jugador.celda_y)
                    enemigo.reaparecer(mapa, COLUMNAS, FILAS, jugador_pos)

        #  Actualizar enemigos activos
        # Actualizar enemigos activos SOLO si el juego ya empezó
        if juego_iniciado and not ganaste and not perdiste:
            for enemigo in enemigos:
                if enemigo.activo:
                    jugador_pos = (jugador.celda_x, jugador.celda_y)
                    enemigo.elegir_movimiento_aleatorio(mapa, COLUMNAS, FILAS, jugador_pos)
                    enemigo.actualizar()

        #  Verificar si el jugador fue atrapado por enemigos ACTIVOS
        if not ganaste and not perdiste:
                for enemigo in enemigos:
                    if (enemigo.activo and
                            enemigo.celda_x == jugador.celda_x and
                            enemigo.celda_y == jugador.celda_y):
                        perdiste = True
                        break

        # 5. Dibujar enemigos activos
        for enemigo in enemigos:
                if enemigo.activo:
                    enemigo.dibujar(screen)



        #salida
        pygame.draw.rect(screen, AMARILLO,
                         (salida_x * TAMAÑO_CELDA + 5,
                          salida_y * TAMAÑO_CELDA + 5,
                          TAMAÑO_CELDA - 10, TAMAÑO_CELDA - 10))

        salida_pixel_x = salida_x * TAMAÑO_CELDA + TAMAÑO_CELDA // 2
        salida_pixel_y = salida_y * TAMAÑO_CELDA + TAMAÑO_CELDA // 2
        jugador_radio = jugador.tamaño_celda // 3  # Mismo radio usado para dibujar
        margen = TAMAÑO_CELDA // 2 - jugador_radio

        if (abs(jugador.pixel_x - salida_pixel_x) <= margen and
                abs(jugador.pixel_y - salida_pixel_y) <= margen):
            ganaste = True

        if enemigo.celda_x == jugador.celda_x and enemigo.celda_y == jugador.celda_y:
            perdiste = True

        if perdiste:
            font = pygame.font.Font(None, 36)
            texto = font.render("¡PERDISTE!", True, (255, 0, 0))
            screen.blit(texto, (ANCHO // 2 - 70, ALTO // 2 - 18))
        elif ganaste:
            font = pygame.font.Font(None, 36)
            texto = font.render("¡GANASTE!", True, (255, 255, 255))
            screen.blit(texto, (ANCHO // 2 - 70, ALTO // 2 - 18))

        if perdiste or ganaste:
            tiempo_final = tiempo_transcurrido
            puntos_obtenidos= puntaje
            pygame.display.update()
            pygame.time.delay(500)
            running = False

        pygame.display.update()
        clock.tick(60)  # 60 FPS



    puntaje_total = jugador.puntos_trampas  # Por ahora solo puntos de trampas

    # Salir del juego
    pygame.quit()


    puntaje_total = jugador.puntos_trampas

    if perdiste:
        guardar_puntaje_escapa(nombre_jugador, puntaje_total)
        mostrar_resultado_tk("¡PERDISTE!", tiempo_transcurrido,
                             jugador.puntos_trampas, puntaje_total)

    elif ganaste:
        guardar_puntaje_escapa(nombre_jugador, puntaje_total)
        mostrar_resultado_tk("¡GANASTE!", tiempo_transcurrido,
                             jugador.puntos_trampas, puntaje_total)




