import pygame
import random
import time

WIDTH, HEIGHT = 800, 600

class Player:
    def __init__(self, x, y, width, height, Vel, Screen_Width, Screen_Height, health):
        self.rect = pygame.Rect(x, y, width, height)
        self.Vel = Vel
        self.Screen_Width = Screen_Width
        self.Screen_Height = Screen_Height
        self.attack_cooldown = 0
        self.attack_timer = 0
        self.current_attack = None
        self.health = health
        self.max_health = health
    
    def move(self, keys):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.x - self.Vel >= 0:
            self.rect.x -= self.Vel
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.x + self.Vel + self.rect.width <= self.Screen_Width:
            self.rect.x += self.Vel
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.rect.y - self.Vel >= 0:
            self.rect.y -= self.Vel
        if (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.rect.y + self.Vel + self.rect.height <= self.Screen_Height:
            self.rect.y += self.Vel
    
    def update_cooldown(self):
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def attack(self):
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 30
            return pygame.Rect(self.rect.x - 20, self.rect.y - 20, self.rect.width + 40, self.rect.height + 40)
        return None
    
    def start_attack(self):
        self.hit_enemies = set()
        if self.attack_cooldown <= 0:
            self.attack_cooldown = 120
            self.attack_timer = 15
            self.current_attack = pygame.Rect(self.rect.x -20, self.rect.y - 20, self.rect.width + 40, self.rect.height + 40)
            return self.current_attack
        
        self.hit_enemies = set()

        return None

    def draw(self, screen, colour = (0, 255, 0)):
        pygame.draw.rect(screen, colour, self.rect)

class Enemy:
    def __init__(self, x, y, width, height, health, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.health = health
        self.max_health = health
    
    def update(self, player_rect):
        dx = player_rect.x - self.rect.x
        dy = player_rect.y - self.rect.y
        if dx != 0:
            self.rect.x += self.speed if dx > 0 else -self.speed
        if dy != 0:
            self.rect.y += self.speed if dy > 0 else -self.speed

    def spawn_enemies(player, level, size = 40):
        enemies = []
        count  = 3 + (level - 1)
        for _ in range(count):
            while True:
                x = random.randint(0, WIDTH - 40)
                y = random.randint(0, HEIGHT - 40)

                if abs(x - player.rect.x) > 100 and abs(y - player.rect.y) > 100:
                    a = random.randint(0, 100)
                    if a <= 20:
                        enemies.append(Tanker(x, y, size, size))
                    elif a <= 55:
                        enemies.append(Speedster(x, y, size, size))
                    else:
                        enemies.append(Soldier(x, y, size, size))
                    break
        return enemies
    
    def next_level(self, level):
        self.reset()
        self.speed = self.speed + (level - 1) * (1/3)
    
    def draw(self, screen, colour = (255, 0, 0)):
        pygame.draw.rect(screen, colour, self.rect)

class Speedster(Enemy):
    def __init__(self, x, y, width, height, health = 50, speed = 3, damage = 20):
        super().__init__(x, y, width, height, health, speed)
        self.damage = damage
    
    def draw(self, screen, colour = (255, 0, 0)):
        pygame.draw.rect(screen, colour, self.rect)

class Soldier(Enemy):
    def __init__(self, x, y, width, height, health = 75, speed = 2, damage = 40):
        super().__init__(x, y, width, height, health, speed)
        self.damage = damage
    
    def draw(self, screen, colour = (205, 0, 0)):
        pygame.draw.rect(screen, colour, self.rect)

class Tanker(Enemy):
    def __init__(self, x, y, width, height, health = 100, speed = 1, damage = 9999):
        super().__init__(x, y, width, height, health, speed)
        self.damage = damage
    
    def draw(self, screen, colour = (155, 0, 0)):
        pygame.draw.rect(screen, colour, self.rect)




class GameInfo:
    LEVELS = 10

    def __init__(self, level = 1):
        self.level = level
        self.started = False
        self.level_start_time = 0
    
    def next_level(self):
        self.level += 1
        self.started = False
    
    def reset(self):
        self.level = False
        self.started = False
        self.level_start_time = 0

    def game_finished(self):
        return self.level > self.LEVELS
    
    def start_level(self):
        self.started = True
        self.level_start_time = time.time()

    def get_level_time(self):
        if not self.started:
            return 0
        return time.time() - self.level_start_time