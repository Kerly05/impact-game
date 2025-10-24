import pygame, sys  # Importa la librería Pygame para gráficos y sys para salir del programa

# Inicializa todos los módulos de Pygame
pygame.init()  # time, display, image

# Define el tamaño de la ventana
ANCHO, ALTO = 960, 540

# Define los fotogramas por segundo y crea el reloj para controlar el tiempo
FPS = 60
clock = pygame.time.Clock()

# Crea la ventana principal del juego
# libreria.modulo.metodo
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("IMPACT")  # Establece el título de la ventana

# Carga el ícono de la ventana desde los archivos
icon = pygame.image.load("./assets/ico.png")
pygame.display.set_icon(icon)  # Establece el ícono de la ventana


# Clase que representa a cada jugador
class Jugador:
    def __init__(jugador, x):
        # Constructor que recibe la posición horizontal inicial
        jugador.rect = pygame.Rect(
            x, ALTO // 2 - 60, 20, 120  # centrar verticalmente al jugador
        )
        jugador.velocidad = 7  # Velocidad de movimiento vertical
        jugador.puntuacion = 0  # Puntos del jugador

    def mover(jugador, arriba, abajo):  # Método para mover el jugador
        teclasPresionadas = pygame.key.get_pressed()  # Detecta teclas presionadas
        if (
            teclasPresionadas[arriba] and jugador.rect.top > 0
        ):  # Mueve hacia arriba si no sale de la pantalla
            jugador.rect.y -= jugador.velocidad
        if (
            teclasPresionadas[abajo] and jugador.rect.bottom < ALTO
        ):  # Mueve hacia abajo si no sale de la pantalla
            jugador.rect.y += jugador.velocidad

    def pintar(self):  # Dibuja el jugador en pantalla
        pygame.draw.rect(VENTANA, (0, 191, 255), self.rect, border_radius=99)


# Clase que representa la pelota
class Pelota:
    def __init__(pelota):  # Constructor
        pelota.rect = pygame.Rect(
            ANCHO // 2 - 20, ALTO // 2 - 20, 40, 40
        )  # Crea el rectángulo de la pelota centrado en todo el medio
        pelota.velocity_x = 7  # Velocidad horizontal
        pelota.velocity_y = 7  # Velocidad vertical

    def mover(pelota):  # Mueve la pelota
        pelota.rect.x += pelota.velocity_x
        pelota.rect.y += pelota.velocity_y

        # Rebota si toca el borde superior o inferior
        if pelota.rect.top < 0 or pelota.rect.bottom > ALTO:
            pelota.velocity_y *= -1

    def reaparecer(pelota):  # Reaparece en el centro y cambia dirección
        pelota.rect.y = ALTO // 2 - 25  # centra verticalmente
        pelota.rect.x = ANCHO // 2 - 25  # centra horizontalmente
        pelota.velocity_x *= -1
        pelota.velocity_y *= -1

    def check_collision(
        pelota, jugador1, jugador2
    ):  # Detecta colisiones con los jugadores
        if pelota.rect.colliderect(jugador1) and pelota.velocity_x < 0:
            pelota.velocity_x *= -1
        if pelota.rect.colliderect(jugador2) and pelota.velocity_x > 0:
            pelota.velocity_x *= -1

    def pintar(pelota):  # Dibuja la pelota
        pygame.draw.ellipse(VENTANA, (0, 244, 0), pelota.rect)


# Instancia los jugadores y la pelota
jugador1 = Jugador(40)  # Jugador izquierdo
jugador2 = Jugador(ANCHO - 40 - 20)  # Jugador derecho
pelota = Pelota()


# Carga y escala el fondo
fondo = pygame.image.load("./assets/background.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

# Fuente para el marcador
font = pygame.font.Font(None, 50)

# Bucle principal del juego
while True:
    # VENTANA.fill("black")  # Limpia la pantalla con color negro

    # Crea el marcador con las puntuaciones
    marcador = font.render(
        f"{jugador1.puntuacion}   {jugador2.puntuacion}", True, "white"
    )

    VENTANA.blit(fondo, (0, 0))  # Dibuja el fondo desde la esquina superior izquierda

    # Dibuja el marco del marcador
    pygame.draw.rect(
        VENTANA,
        "orange",
        (
            ANCHO // 2 - marcador.get_width() // 2 - 2,
            18,
            marcador.get_width() + 4,
            marcador.get_height() + 4,
        ),
        width=4,
        border_radius=8,
    )

    # Dibuja la mitad derecha del marco del marcador
    pygame.draw.rect(
        VENTANA,
        "orange",
        (ANCHO // 2, 18, marcador.get_width() // 2 + 4, marcador.get_height() + 4),
        width=4,
        border_bottom_right_radius=8,
        border_top_right_radius=8,
    )

    VENTANA.blit(
        marcador, (ANCHO // 2 - marcador.get_width() // 2, 20)
    )  # Dibuja el marcador
    # images, texto -> ventana.blit()
    # formas, circulos, rectangulos ... pygame.draw.<forma>

    jugador1.pintar()  # Dibuja jugador 1
    jugador2.pintar()  # Dibuja jugador 2
    pelota.pintar()  # Dibuja la pelota

    jugador1.mover(pygame.K_w, pygame.K_s)  # Movimiento jugador 1 con W y S
    jugador2.mover(pygame.K_UP, pygame.K_DOWN)  # Movimiento jugador 2 con flechas

    pelota.mover()  # Mueve la pelota

    pelota.check_collision(jugador1, jugador2)  # Verifica colisiones

    # Si la pelota sale por la izquierda, punto para jugador 2
    if pelota.rect.right <= 0:
        jugador2.puntuacion += 1
        pelota.reaparecer()

    # Si la pelota sale por la derecha, punto para jugador 1

    pygame.display.flip()  # Actualiza la pantalla

    # Maneja eventos (como cerrar la ventana)
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)  # Limita el bucle a 60 FPS
