import pygame
from math import sqrt

pygame.init()
pygame.display.init()

WIDTH, HEIGHT = (900, 800)
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")
CLOCK = pygame.time.Clock()
FONT = pygame.font.SysFont("Hack", 18)

COLORS = {
    "bg": pygame.Color(50, 50, 97),
    "tower": pygame.Color(228, 253, 225),
    "bullet": pygame.Color(255, 191, 70),
    "enemy": pygame.Color(255, 95, 70),
    "debug": pygame.Color(255, 255, 255),
    "ui_fg": pygame.Color(80, 80, 80)
}

def dist(e1, e2):
    d = sqrt(abs(e1.position.x - e2.position.x) ** 2 + abs(e1.position.y - e2.position.y) ** 2)
    return d
