import pygame
from math import *

pygame.init

screen = pygame.display.set_mode((500, 500))

def get_holding_dist(event):
    if event.type == pygame.MOUSEBUTTONDOWN:
        mouse_pos1 = pygame.mouse.get_pos()  # Speichert die Position bei MOUSEBUTTONDOWN
        t1 = pygame.time.get_ticks()  # Speichert die Zeit bei MOUSEBUTTONDOWN
    
    if event.type == pygame.MOUSEBUTTONUP:
        mouse_pos2 = pygame.mouse.get_pos()  # Speichert die Position bei MOUSEBUTTONUP
        t2 = pygame.time.get_ticks()  # Speichert die Zeit bei MOUSEBUTTONUP
        
        # Berechnung der Distanz zwischen den beiden Mauspositionen
        dist = sqrt((mouse_pos2[0] - mouse_pos1[0])**2 + (mouse_pos2[1] - mouse_pos1[1])**2)
        
        # Berechnung der Zeitdifferenz
        dt = abs(t2 - t1)
        
        # Berechnung der Geschwindigkeit
        vel = dist * (1000 / dt)  # Umrechnen von Millisekunden in Sekunden und Berechnung der Geschwindigkeit
        
        print(vel)

    

r = True

while r:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            r = False
                 
        get_holding_dist(event=event)
        
    pygame.display.flip()    
    
    
pygame.quit()
quit()