import pygame, sys
# pygame -> trabaja elementos visuales y ventana
# sys -> finalizar el proceso de python

pygame.init()

ANCHO, ALTO = 960, 540 # dimensiones de la ventana

FPS= 100
clock = pygame.time.Clock()

VENTANA = pygame.display.set_mode((ANCHO, ALTO)) # dibujar la ventana y guardar su referencia en WINDOW
pygame.display.set_caption("IMPACT") # Titulo de la ventana

icon = pygame.image.load("./assets/ico.png")
pygame.display.set_icon(icon)


class Jugador: #Define la clase jugador
    def __init__(self, x): #Inicializa los atributos del jugador
        self.rect = pygame.Rect(x, ALTO//2 - 60, 20, 120) # Define posiciones y dimensiones del jugador (paleta)
        self.velocidad = 7 #colocar velocidad del jugador
        self.puntuacion = 0
    def mover(self, arriba, abajo): # Define método mover (funcionalidad de mover)
        teclasPresionadas = pygame.key.get_pressed() # obtener teclas presionadas en una lista
        if teclasPresionadas[arriba] and self.rect.top > 0: # si se presiona la tecla de arriba y la parte superior de la paleta está posicionada debajo del tope de la ventana
            self.rect.y -= self.velocidad # sube la paleta, disminuye y
        if teclasPresionadas[abajo] and self.rect.bottom < ALTO: # si se presiona la tecla de abajo y la parte inferior de la paleta está posicionada encima del fondo de la ventana
            self.rect.y += self.velocidad # baja la paleta, aumenta y
    def pintar(self): # Define método pintar (dibuja el jugador en la ventana)
        pygame.draw.rect(VENTANA, (0,191,255), self.rect, border_radius=99) # dibuja un rectángulo blanco en la ventana en la posición y dimensiones definidas por self.rect

class Pelota:#Define la clase Pelota
    def __init__(self): #Inicializa los atributos de la pelota
        self.rect = pygame.Rect(ANCHO//2 - 20, ALTO//2 - 20, 40, 40) # Define posiciones y dimensiones de la pelota
        self.velocity_x = 7 # velocidad en x
        self.velocity_y = 7 # velocidad en y
        
    def mover(self): # Define método mover (funcionalidad de mover)
        self.rect.x += self.velocity_x # mueve la pelota en x
        self.rect.y += self.velocity_y # mueve la pelota en y
        
        if self.rect.top < 0 or self.rect.bottom > ALTO: # si la pelota toca el tope o el fondo de la ventana
            self.velocity_y *= -1 # invierte la dirección en y
        # if self.rect.right < 0 or self.rect.left > ANCHO: # si la pelota sale por la izquierda o derecha de la ventana
        #     self.reaparecer() # reaparece la pelota en el centro
    def reaparecer(self): # Define método reaparecer (reubica la pelota en el centro)
        self.rect.y = ALTO//2 - 25 # centra la pelota en y
        self.rect.x = ANCHO//2 - 25 # centra la pelota en x
        self.velocity_x *=-1 # invierte la dirección en x
        self.velocity_y *=-1 # invierte la dirección en y
    
    def check_collision(self, jugador1, jugador2): # Define método check_collision (verifica colisiones con los jugadores)
        if self.rect.colliderect(jugador1) and self.velocity_x < 0:
            self.velocity_x *=-1 # invierte la dirección en x si colisiona con algún jugador
        if self.rect.colliderect(jugador2) and self.velocity_x > 0:
            self.velocity_x *=-1 # invierte la dirección en x si colisiona con algún jugador
    
    def pintar(self): # Define método pintar (dibuja la pelota en la ventana)
        # pygame.draw.ellipse(VENTANA, (0, 206, 237), self.rect) # dibuja una elipse blanca en la ventana en la posición y dimensiones definidas por self.rect
        pygame.draw.ellipse(VENTANA, (0, 244, 0), self.rect) # dibuja una elipse blanca en la ventana en la posición y dimensiones definidas por self.rect
        # pygame.draw.ellipse(VENTANA, "pink", self.rect, width=4) # dibuja una elipse blanca en la ventana en la posición y dimensiones definidas por self.rect
        
        
jugador1 = Jugador(40) # crea una instancia de Jugador en la posición x=40
jugador2 = Jugador(ANCHO - 40 - 20) # crea una instancia de Jugador en la posición x=900
pelota = Pelota() # crea una instancia de Pelota

fondo = pygame.image.load("./assets/background.png")
fondo = pygame.transform.scale(fondo, (ANCHO, ALTO))

font = pygame.font.Font(None, 50)

while True: # ciclo principal del juego
    VENTANA.fill("black")
    marcador = font.render(f"{jugador1.puntuacion}   {jugador2.puntuacion}", True, "white")
    
    
    
    VENTANA.blit(fondo, (0,0))
    pygame.draw.rect(VENTANA, "orange", (ANCHO//2 - marcador.get_width()//2 - 2, 18, marcador.get_width() + 4, marcador.get_height() + 4), width=4, border_radius=8)
    pygame.draw.rect(VENTANA, "orange", (ANCHO//2 , 18, marcador.get_width() // 2 + 4, marcador.get_height() + 4), width=4, border_bottom_right_radius=8, border_top_right_radius=8)
    VENTANA.blit(marcador, (ANCHO //2 - marcador.get_width()//2, 20))
    # contenedor del marcador
    
    jugador1.pintar() # dibuja el jugador 1
    jugador2.pintar() # dibuja el jugador 2
    pelota.pintar() # dibuja la pelota
    
    jugador1.mover(pygame.K_w, pygame.K_s) # mueve el jugador 1 con las teclas W y S
    jugador2.mover(pygame.K_UP, pygame.K_DOWN)# mueve el jugador 2 con las flechas arriba y abajo
    
    pelota.mover()# mueve la pelota
    
    pelota.check_collision(jugador1, jugador2) # verifica colisiones de la pelota con los jugadores
    
    
    if pelota.rect.right <= 0:
        jugador2.puntuacion += 1
        pelota.reaparecer()
    if pelota.rect.right >= ANCHO:
        jugador1.puntuacion +=1
        pelota.reaparecer()
    
    pygame.display.flip()# actualizar la pantalla
    
    
    for evento in pygame.event.get(): # ciclo para revisar eventos
        if evento.type == pygame.QUIT: # si el evento es salir
            pygame.quit() # cerrar pygame
            sys.exit() # finalizar el proceso de python
            
    clock.tick(FPS)