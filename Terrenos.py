
class Terreno:
    def __init__(self, tipo, color, transitable_jugador, transitable_enemigo):
        self.tipo = tipo
        self.color = color
        self.transitable_jugador = transitable_jugador
        self.transitable_enemigo = transitable_enemigo

class Camino(Terreno):
    def __init__(self):
        super().__init__("camino", (200, 200, 200), True, True)

class Muro(Terreno):
    def __init__(self):
        super().__init__("muro", (0, 0, 0), False, False)

class Liana(Terreno):
    def __init__(self):
        super().__init__("liana", (0, 100, 0), False, True)

class Tunel(Terreno):
    def __init__(self):
        super().__init__("tunel", (139, 69, 19), True, False)