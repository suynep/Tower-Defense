import pygame
from math import sin, cos
from random import randint
import os
import sys
from setup import SCREEN, WIDTH, HEIGHT, CLOCK, COLORS

class Tower:
    def __init__(self):
        self.size = 35
        self.range_ = 200
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.bulletcount = 200
        self.bullets = [Bullet() for i in range(self.bulletcount)]
        self.health = 100
        
        
    def draw(self):
        pygame.draw.circle(SCREEN, COLORS["tower"], self.position, self.size)
        pygame.draw.circle(SCREEN, COLORS["debug"], self.position, self.range_, 1) # check the range
    
    def shoot(self, enemy):
        if (self.bullets != []):
            self.bullets[0].move(enemy)
            self.bullets[0].draw()
            self.bulletcount = len(self.bullets)
        else:
            print("no bullets")

class Bullet:
    def __init__(self):
        self.size = 5
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.speed = 1
        self.damage = 5
                
    def draw(self):
        pygame.draw.circle(SCREEN, COLORS["bullet"], self.position, self.size)
    
    def move(self, dest):
        self.velocity = pygame.Vector2(dest.position.x - self.position.x, dest.position.y - self.position.y).normalize()
        self.position.x += self.velocity.x * self.speed
        self.position.y += self.velocity.y * self.speed

class Enemy:
    def __init__(self, tower: Tower):
        self.size = 12
        r = randint(tower.range_, WIDTH - tower.range_ )
        ang = randint(0, 360)
        self.position = pygame.Vector2(r * cos(ang) + tower.position.x, r * sin(ang) + tower.position.y)
        self.speed = 1
        self.velocity = pygame.Vector2(tower.position.x - self.position.x, tower.position.y - self.position.y).normalize()
        self.living = True
        self.health = 20
        
    def draw(self):
        pygame.draw.circle(SCREEN, COLORS["enemy"], self.position, self.size)
    
    def move(self):
        self.position.x += self.velocity.x * self.speed
        self.position.y += self.velocity.y * self.speed


class Game:
    def __init__(self):
        self.running = True
        self.tower = Tower()
        self.waves = [10, 20, 30]
        self.enemies = [Enemy(self.tower) for i in range(self.waves[0])]
    
    def run(self):
        # main loop
        while self.running:

            SCREEN.fill(COLORS["bg"])
            self.tower.draw()
            for enemy in self.enemies:
                enemy.draw()
                enemy.move()
                self.tower.shoot(enemy)

            # capture events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
            
            pygame.display.flip()
            CLOCK.tick(30)


if __name__ == "__main__":
    Game().run()
