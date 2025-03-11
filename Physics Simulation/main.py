import pygame#type: ignore
import math

pygame.init()

FONT = pygame.font.SysFont("Arial", 16, bold=True)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIN_WIDTH, WIN_HEIGHT = 1000, 1000
RES = (WIN_WIDTH, WIN_HEIGHT)

screen = pygame.display.set_mode(RES)
pygame.display.set_caption("Physics Simulation")


class Ball:
    GRAVITY = 9.81
    RADIUS = 20
    MASS = 20
    COR = 0.7  # Coefficient of Restitution (Energieverlust beim Aufprall)

    def __init__(self, x, y, i):
        self.i = i # index
        self.x = x
        self.y = y
        self.vel = 0
        self.t1 = pygame.time.get_ticks()

    def draw(self, win):
        pygame.draw.circle(win, WHITE, (int(self.x), int(self.y)), self.RADIUS)

    def fall(self):
        dt = 1 / 60  # Konstante Zeit pro Frame (besser für Physik-Simulationen)
        self.vel += self.GRAVITY * dt
        self.y += self.vel

    def bounce(self):
        if self.y > RES[1] - self.RADIUS:
            self.y = RES[1] - self.RADIUS  # Verhindert, dass der Ball durch den Boden geht
            self.vel *= -self.COR  # Geschwindigkeit umkehren und verringern
            
    def show_height_and_i(self, win):
        txt_surface_ball = FONT.render(f"Ball {self.i}: {self.y:.2f}", True, WHITE)
        txt_surface_i = FONT.render(f"{self.i}", True, BLACK)

        # Hintergrund für bessere Sichtbarkeit
        pygame.draw.rect(win, BLACK, (0, 20 * self.i, txt_surface_ball.get_width(), txt_surface_ball.get_height()))

        win.blit(txt_surface_ball, (0, 20 * self.i))
        win.blit(txt_surface_i, (self.x - 5, self.y - 10))

    
def check_collision(ball1, ball2):
    dx = ball2.x - ball1.x
    dy = ball2.y - ball1.y
    dist = math.sqrt(dx**2 + dy**2)

    if dist < ball1.RADIUS + ball2.RADIUS:
        # Normalisierte Richtung des Kollisionsvektors
        nx = dx / dist
        ny = dy / dist

        # Geschwindigkeit tauschen
        ball1.vel, ball2.vel = ball2.vel, ball1.vel

        # Positionskorrektur (um Überschneidung zu vermeiden)
        overlap = (ball1.RADIUS + ball2.RADIUS - dist) / 2
        ball1.x -= overlap * nx
        ball1.y -= overlap * ny
        ball2.x += overlap * nx
        ball2.y += overlap * ny



def main():
    

    running = True
    clock = pygame.time.Clock()

    balls = []
    ball = Ball(0, 0, 0)
    
    i = 0

    while running:
        screen.fill(BLACK)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                i += 1
                balls.append(Ball(mouse_x, mouse_y, i))
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    balls.clear()
                    i = 0
                
        for i in range(len(balls)):
            for j in range(i + 1, len(balls)):  # Vermeidet doppelte Vergleiche
                check_collision(balls[i], balls[j])
                

        for ball in balls:
            ball.draw(screen)
            ball.fall()
            ball.bounce()
            ball.show_height_and_i(screen)

        pygame.display.flip()

    pygame.quit()
    quit()

main()
