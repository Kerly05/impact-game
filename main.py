import pygame, sys

pygame.init()

ANCHO, ALTO = 960, 540

FPS = 100
clock = pygame.time.Clock()

VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("IMPACT")

icon = pygame.image.load("./assets/ico.png")
pygame.display.set_icon(icon)


class Jugador:
    def __init__(self, x):
        self.rect = pygame.Rect(x, ALTO // 2 - 60, 20, 120)
        self.velocidad = 7
        self.puntuacion = 0

    def mover(self, arriba, abajo):
        teclasPresionadas = pygame.key.get_pressed()
        if teclasPresionadas[arriba] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if teclasPresionadas[abajo] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad

    def pintar(self):
        pygame.draw.rect(VENTANA, (0, 191, 255), self.rect, border_radius=99)


class Pelota:
    def __init__(self):
        self.rect = pygame.Rect(ANCHO // 2 - 20, ALTO // 2 - 20, 40, 40)
        self.velocity_x = 7
        self.velocity_y = 7

    def mover(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        if self.rect.top < 0 or self.rect.bottom > ALTO:
            self.velocity_y *= -1

    def reaparecer(self):
        self.rect.y = ALTO // 2 - 25
        self.rect.x = ANCHO // 2 - 25
        self.velocity_x *= -1
        self.velocity_y *= -1

    def check_collision(self, jugador1, jugador2):
        if self.rect.colliderect(jugador1) and self.velocity_x < 0:
            self.velocity_x *= -1
        if self.rect.colliderect(jugador2) and self.velocity_x > 0:
            self.velocity_x *= -1

    def pintar(self):

        pygame.draw.ellipse(VENTANA, (0, 244, 0), self.rect)


jugador1 = Jugador(40)  #
jugador2 = Jugador(ANCHO - 40 - 20)
pelota = Pelota()

fondo = pygame.image.load("./assets/background.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

font = pygame.font.Font(None, 50)

while True:
    VENTANA.fill("black")
    marcador = font.render(
        f"{jugador1.puntuacion}   {jugador2.puntuacion}", True, "white"
    )

    VENTANA.blit(fondo, (0, 0))
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
    pygame.draw.rect(
        VENTANA,
        "orange",
        (ANCHO // 2, 18, marcador.get_width() // 2 + 4, marcador.get_height() + 4),
        width=4,
        border_bottom_right_radius=8,
        border_top_right_radius=8,
    )
    VENTANA.blit(marcador, (ANCHO // 2 - marcador.get_width() // 2, 20))

    jugador1.pintar()
    jugador2.pintar()
    pelota.pintar()

    jugador1.mover(pygame.K_w, pygame.K_s)
    jugador2.mover(pygame.K_UP, pygame.K_DOWN)

    pelota.mover()

    pelota.check_collision(jugador1, jugador2)

    if pelota.rect.right <= 0:
        jugador2.puntuacion += 1
        pelota.reaparecer()
    if pelota.rect.right >= ANCHO:
        jugador1.puntuacion += 1
        pelota.reaparecer()

    pygame.display.flip()

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    clock.tick(FPS)
