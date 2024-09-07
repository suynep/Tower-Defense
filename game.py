import pygame
from math import sin, cos
from random import randint
import os
import sys
from setup import SCREEN, WIDTH, HEIGHT, CLOCK, FONT, COLORS, dist

class Button:
    def __init__(self, position, label):
        self.position = position
        self.color = COLORS["ui_fg"]
        self.label = label
        self.size = (len(self.label) * 10, 30)

    def draw(self):
        pygame.draw.rect(SCREEN, self.color, (*self.position, *self.size))
        text = FONT.render(self.label, True, COLORS["debug"])
        SCREEN.blit(text, self.position) # --> adjust the position later on to center the text in the rectangle

class Tower:
    def __init__(self):
        self.size = 35
        self.range_ = 200
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.bulletcount = 200
        self.bullets = [Bullet() for i in range(self.bulletcount)]
        self.health = 100
        self.enemy_queue = []
        self.money = 20
        self.cost_speed = 6
        self.cost_health = 6
        self.cost_range = 10
                
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
                self.bullets[0].is_shot = True
                self.bullets[0].move(self.enemy_queue[0])
                self.bullets[0].draw()
                self.bulletcount = len(self.bullets)
                if dist(self.bullets[0], self.enemy_queue[0]) < 3:
                    # 5 is an approx val, try changing, if collision doesn't occur as expected
                    self.enemy_queue[0].health -= self.bullets[0].damage
                    self.bullets.pop(0)
            else:
                self.enemy_queue[0].living = False
                self.enemy_queue.pop(0)
                self.money += 2
        
    def create_enemy_queue(self, enemy):
        if dist(self, enemy) < self.range_ and enemy not in self.enemy_queue:
            self.enemy_queue.append(enemy)
                    
    def display_health(self):
        text_surf = FONT.render(f"Health: {self.health}", False, COLORS["debug"])
        SCREEN.blit(text_surf, (0, 0))

    def display_money(self):
        text_surf = FONT.render(f"Money: {self.money}", False, COLORS["debug"])
        SCREEN.blit(text_surf, (WIDTH - 200, 0))
        
class Bullet:
    def __init__(self):
        self.size = 5
        self.position = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
        self.speed = 10
        self.damage = 5
        self.is_shot = False
                
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
        self.damage = 5
        self.has_hit = False
        
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
        self.btns = {"speed": Button((10, 50), "speed"), "range": Button((10, 90), "range"), "health": Button((10, 130), "health")}
    
    def run(self):
        # main loop
        while self.running:
            SCREEN.fill(COLORS["bg"])
            # draw btns
            for btn in self.btns.keys():
                self.btns[btn].draw()
            
            speed_label = FONT.render(f"{self.tower.bullets[0].speed}   (UP_COST: {self.tower.cost_speed})", False, COLORS["debug"])
            range_label = FONT.render(f"{self.tower.range_}   (UP_COST: {self.tower.cost_range})", False, COLORS["debug"])
            health_label = FONT.render(f"{self.tower.health}   (UP_COST: {self.tower.cost_health})", False, COLORS["debug"])            

            SCREEN.blit(speed_label, (100, 50))
            SCREEN.blit(range_label, (100, 90))
            SCREEN.blit(health_label, (100, 130))            
            self.tower.draw()
            self.tower.shoot()
            
            for enemy in self.enemies:
                if enemy.living:
                    enemy.draw()
                    if dist(self.tower, enemy) > 5:
                        enemy.move()
                    self.tower.create_enemy_queue(enemy)
                if dist(enemy, self.tower) < (self.tower.size + enemy.size) and not enemy.has_hit:
                    self.tower.health -= enemy.damage
                    enemy.has_hit = True
                    
            print(self.tower.health)
            
            # capture events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    click_pos = event.pos
                    for btn in self.btns.keys():
                        ref_btn = self.btns[btn]
                        if click_pos[0] > ref_btn.position[0] and click_pos[0] < ref_btn.position[0] + ref_btn.size[0] and click_pos[1] > ref_btn.position[1] and click_pos[1] < ref_btn.position[1] + ref_btn.size[1]:
                            if btn == "speed":
                                if self.tower.money >= self.tower.cost_speed:
                                    for bullet in self.tower.bullets:
                                        bullet.speed += 0.2
                                    self.tower.money -= self.tower.cost_speed
                            if btn == "health":
                                if self.tower.money >= self.tower.cost_health:
                                    self.tower.health += 5
                                    self.tower.money -= self.tower.cost_health
                            if btn == "range":
                                if self.tower.money >= self.tower.cost_range:
                                    self.tower.range_ += 10
                                    self.tower.money -= self.tower.cost_range

            self.tower.display_health()
            self.tower.display_money()            
            pygame.display.flip()
            CLOCK.tick(30)
            # print(len(self.tower.enemy_queue))


if __name__ == "__main__":
    Game().run()
