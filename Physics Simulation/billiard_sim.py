import pygame as pg  # type: ignore
import math

pg.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIN_WIDTH, WIN_HEIGHT = 1000, 1000
RES = (WIN_WIDTH, WIN_HEIGHT)

screen = pg.display.set_mode(RES)
pg.display.set_caption("Billiard Simulation")

class Obj:
    MASS = 1000
    RADIUS = 30
    FRICTION = 0.98  # Reibung, um den Ball zu verlangsamen

    def __init__(self, x=500, y=500):
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.mouse_pos1 = None
        self.t1 = None

    def draw(self, win):
        pg.draw.circle(win, WHITE, (int(self.x), int(self.y)), self.RADIUS)

    def check_onclick(self, mouse_pos):
        """Überprüft, ob auf den Kreis geklickt wurde."""
        d = math.sqrt((self.x - mouse_pos[0])**2 + (self.y - mouse_pos[1])**2)
        return d <= self.RADIUS

    def get_holding_dist(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.mouse_pos1 = pg.mouse.get_pos()
            self.t1 = pg.time.get_ticks()

        if event.type == pg.MOUSEBUTTONUP and self.mouse_pos1 and self.t1 is not None:
            mouse_pos2 = pg.mouse.get_pos()
            t2 = pg.time.get_ticks()

            # Berechnung der Distanz und Richtung
            dx = mouse_pos2[0] - self.mouse_pos1[0]
            dy = mouse_pos2[1] - self.mouse_pos1[1]
            dist = math.sqrt(dx**2 + dy**2)

            # Berechnung der Zeitdifferenz
            dt = max(abs(t2 - self.t1), 1) # Division durch null verhindern

            # Berechnung der Geschwindigkeit
            speed = dist / 50 * dt / 100
            angle = math.atan2(dy, dx)

            self.vel_x = -speed * math.cos(angle)
            self.vel_y = -speed * math.sin(angle)

            print(f"vel: {speed:.2f}, angle: {math.degrees(angle):.2f}°")

            # Zurücksetzen der Variablen
            self.mouse_pos1 = None
            self.t1 = None

    def update(self):
        

        """Bewegt den Ball basierend auf der aktuellen Geschwindigkeit."""
        self.x += self.vel_x
        self.y += self.vel_y

        # Geschwindigkeit verringern durch Reibung
        self.vel_x *= self.FRICTION
        self.vel_y *= self.FRICTION

        # Stoppe den Ball, wenn er fast stillsteht
        if abs(self.vel_x) < 0.1:
            self.vel_x = 0
        if abs(self.vel_y) < 0.1:
            self.vel_y = 0

        # Begrenzung innerhalb des Fensters
        if self.x - self.RADIUS < 0 or self.x + self.RADIUS > WIN_WIDTH:
            self.vel_x = -self.vel_x  # Rückstoß von der Wand
            self.x = max(self.RADIUS, min(self.x, WIN_WIDTH - self.RADIUS))

        if self.y - self.RADIUS < 0 or self.y + self.RADIUS > WIN_HEIGHT:
            self.vel_y = -self.vel_y  # Rückstoß von der Wand
            self.y = max(self.RADIUS, min(self.y, WIN_HEIGHT - self.RADIUS))

def check_collision(obj1, obj2):
    dx = obj1.x - obj2.x
    dy = obj1.y - obj2.y
    dist = math.sqrt(dx**2 + dy**2)
    
    return (dist <= obj1.RADIUS + obj2.RADIUS, (obj1, obj2))
    
def collision(objs):
    for i in range(len(objs)):
        for j in range(i + 1, len(objs)):
            has_collided, (obj1, obj2) = check_collision(objs[i], objs[j])
            if has_collided:
                # Richtungsvektor normalisieren
                dx = obj2.x - obj1.x
                dy = obj2.y - obj1.y
                dist = math.sqrt(dx ** 2 + dy ** 2)
                
                if dist == 0:  # Falls die Bälle sich genau überlagern (sollte selten passieren)
                    continue
                
                nx = dx / dist
                ny = dy / dist

                # Relative Geschwindigkeit
                dvx = obj2.vel_x - obj1.vel_x
                dvy = obj2.vel_y - obj1.vel_y

                # Skalarprodukt von Relativgeschwindigkeit und Normalenvektor
                impact_speed = dvx * nx + dvy * ny

                if impact_speed > 0:
                    continue  # Sie entfernen sich schon voneinander

                # Impulsberechnung (elastischer Stoß)
                impulse = (2 * impact_speed) / (obj1.MASS + obj2.MASS)
                obj1.vel_x += impulse * obj2.MASS * nx
                obj1.vel_y += impulse * obj2.MASS * ny
                obj2.vel_x -= impulse * obj1.MASS * nx
                obj2.vel_y -= impulse * obj1.MASS * ny

                # Rückversetzen, falls sich Bälle überlappen
                overlap = obj1.RADIUS + obj2.RADIUS - dist
                obj1.x -= overlap / 2 * nx
                obj1.y -= overlap / 2 * ny
                obj2.x += overlap / 2 * nx
                obj2.y += overlap / 2 * ny


def main():
    running = True
    clock = pg.time.Clock()
    objs = []

    while running:
        screen.fill(BLACK)
        clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = pg.mouse.get_pos()
                clicked_obj = None

                for obj in objs:
                    if obj.check_onclick(mouse_pos):
                        clicked_obj = obj
                        break

                if clicked_obj:
                    clicked_obj.get_holding_dist(event)
                else:
                    new_obj = Obj(mouse_pos[0], mouse_pos[1])
                    objs.append(new_obj)

            if event.type == pg.MOUSEBUTTONUP:
                for obj in objs:
                    obj.get_holding_dist(event)

        for obj in objs:
            obj.update()  # Bewegung aktualisieren
            obj.draw(screen)  # Ball zeichnen

        collision(objs)
        
        pg.display.flip()

    pg.quit()
    quit()

main()
