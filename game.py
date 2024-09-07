import pygame
from math import sin, cos, sqrt
from random import randint
import os
import sys
from setup import SCREEN, WIDTH, HEIGHT, CLOCK, COLORS


def dist(e1, e2):
    d = sqrt(abs(e1.position.x - e2.position.x) ** 2 + abs(e1.position.y - e2.position.y) ** 2)
    return d
    

class Tower:
    def __init__(self):
        self.size = 35
        self.range_ = 200
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.bulletcount = 200
        self.bullets = [Bullet() for i in range(self.bulletcount)]
        self.health = 100
        self.enemy_queue = []
                
    def draw(self):
        pygame.draw.circle(SCREEN, COLORS["tower"], self.position, self.size)
        pygame.draw.circle(SCREEN, COLORS["debug"], self.position, self.range_, 1) # check the range
    
    def shoot(self):
        # How shall we implement this?
        # -- shoot from `enemy_queue` until enemy_queue[0] dies
        # -- then, `pop enemy_queue[0]` and continue
        # -- we also need to check the collision between the bullet just fired, and the first enemy in the queue
        # -- after a `collision`, we pop the bullet
        if (self.bullets != [] and self.enemy_queue != []):
            if self.enemy_queue[0].health != 0:
                self.bullets[0].move(self.enemy_queue[0])
                self.bullets[0].draw()
                self.bulletcount = len(self.bullets)
                if dist(self.bullets[0], self.enemy_queue[0]) < 5:
                    # 5 is an approx val, try changing, if collision doesn't occur as expected
                    self.enemy_queue[0].health -= self.bullets[0].damage
                    self.bullets.pop(0)
            else:
                self.enemy_queue[0].living = False
                self.enemy_queue.pop(0)

        
    def create_enemy_queue(self, enemy):
        if dist(self, enemy) < self.range_ and enemy not in self.enemy_queue:
            self.enemy_queue.append(enemy)
                    
        
class Bullet:
    def __init__(self):
        self.size = 5
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.speed = 5
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
            self.tower.shoot()
            
            for enemy in self.enemies:
                if enemy.living:
                    enemy.draw()
                    enemy.move()
                    self.tower.create_enemy_queue(enemy)

                
            # capture events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)

            pygame.display.flip()
            CLOCK.tick(30)
            # print(len(self.tower.enemy_queue))


if __name__ == "__main__":
    Game().run()
