import pygame #type: ignore
import math

pygame.init()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

WIN_WIDTH, WIN_HEIGHT = 1600, 900
RES = (WIN_WIDTH, WIN_HEIGHT)

screen = pygame.display.set_mode(RES)

class Obj:
    
    GRV = 9.81
    RADIUS = 30
    MASS = 40
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
        
        self.vel = 0
        self.F = 0
        self.cor = 1 - 0.005 * self.MASS
        
        self.t1 = pygame.time.get_ticks()
        self.t2 = 0
        self.dt = 0
        
        self.h_i = RES[1]
        
    def draw_obj(self, win):
        pygame.draw.circle(win, WHITE, (self.x, self.y), self.RADIUS)
    
    def fall(self):
        self.t2 = pygame.time.get_ticks()
        self.dt = (self.t2 - self.t1) / 1000
        
        self.F = self.MASS * self.GRV
        self.vel += self.dt * self.GRV
        self.y += self.vel
        
    def bounce(self):
        if self.y > self.h_i - self.RADIUS:  
            self.y = self.h_i - self.RADIUS  
            self.vel = -self.vel * self.cor  
            

def check_collision(obj1, obj2):
    
    dx = abs(obj1.x - obj2.x)
    dy = abs(obj1.y - obj2.y)
    
    dist = math.sqrt((dx**2) + (dy**2))
    
    if dist <= obj1.RADIUS + obj2.RADIUS:
        obj1.vel, obj2.vel = obj2.vel, obj1.vel
        
        
        
        
def main():
    
    running = True
    clock = pygame.time.Clock()
    
    objs = []
    

    while running:
        
        screen.fill(BLACK)
        clock.tick(60)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    objs.clear()
                                   
            if event.type == pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                objs.append(Obj(mouse_pos[0], mouse_pos[1]))
                
        for i in range(0, len(objs)):
            for j in range(i + 1, len(objs)):
                check_collision(objs[i], objs[j])
                            
        for obj in objs:
            obj.draw_obj(screen)
            obj.fall()
            obj.bounce()
            
            
            
        pygame.display.flip()
        
    pygame.quit()
    quit()
main()
    