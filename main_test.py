# Moon Warriors（修正版：加上角色圖片、攻擊邏輯、移除玩家輸入）

import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
font = pygame.font.SysFont(None, 28)
score_font = pygame.font.SysFont(None, 48)

player_img = pygame.Surface((60, 100), pygame.SRCALPHA)
pygame.draw.rect(player_img, (0, 100, 255), (0, 0, 60, 100))

# 攻擊物件
class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 15
        self.radius = 8

    def move(self):
        self.x += self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 0), (self.x, self.y), self.radius)

    def rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)

# Entity 物件
class Entity:
    def __init__(self, name, max_hp, attack=0, skills=None, boss=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.skills = skills or {}
        self.boss = boss
        self.alive = True

# 血條
def draw_health_bar(screen, entity, x, y):
    pygame.draw.rect(screen, RED, (x, y, 200, 25))
    hp_ratio = entity.hp / entity.max_hp
    pygame.draw.rect(screen, GREEN, (x, y, int(200 * hp_ratio), 25))
    name = font.render(f"{entity.name} HP: {entity.hp}/{entity.max_hp}", True, BLACK)
    screen.blit(name, (x + 210, y))

# 火球
class Fireball:
    def __init__(self, screen, start_pos, target_pos, speed=10):
        self.screen = screen
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.img = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.img, (255, 100, 0), (10, 10), 10)
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        dist = max(1, (dx**2 + dy**2)**0.5)
        self.dir_x = dx / dist
        self.dir_y = dy / dist
        self.active = True

    def update(self):
        if not self.active:
            return False
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed
        self.screen.blit(self.img, (int(self.x), int(self.y)))
        if abs(self.x - self.target_x) < 20 and abs(self.y - self.target_y) < 20:
            self.active = False
            return True
        return False

# 初始化
player = Entity("勇者", 2000, skills={"光耀審判": 1000})
minion = Entity("暗影使徒", 1500, attack=100)
boss = Entity("暗影指揮官", 2000, attack=150, boss=True)

player_x, player_y = 100, HEIGHT - 150
player_speed = 5
bg_x = 0
bg_speed = 5
fireballs = []
projectiles = []
triggered_willy_game = False

# 遊戲主迴圈
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectiles.append(Projectile(player_x + 60, player_y + 40))

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]: player_y -= player_speed
    if keys[pygame.K_DOWN]: player_y += player_speed
    player_y = max(0, min(HEIGHT - 100, player_y))

    # 背景
    bg_x -= bg_speed
    if bg_x <= -WIDTH: bg_x = 0
    pygame.draw.rect(screen, (65, 105, 225), (bg_x, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, (65, 105, 225), (bg_x + WIDTH, 0, WIDTH, HEIGHT))

    # 玩家角色
    screen.blit(player_img, (player_x, player_y))

    # 血條
    draw_health_bar(screen, player, 50, 20)
    draw_health_bar(screen, minion, 50, 60)
    draw_health_bar(screen, boss, 50, 100)

    # 發射火球（怪）
    if minion.hp > 0 and minion.hp < 1000:
        fireballs.append(Fireball(screen, (800, 100), (player_x, player_y)))

    for fb in fireballs[:]:
        if fb.update():
            if player.alive:
                player.hp -= 100
                if player.hp <= 0:
                    player.alive = False
            fireballs.remove(fb)
        elif not fb.active:
            fireballs.remove(fb)

    # 玩家攻擊
    for p in projectiles[:]:
        p.move()
        p.draw(screen)
        if minion.alive and p.rect().colliderect(pygame.Rect(800, 100, 60, 100)):
            minion.hp -= 300
            if minion.hp <= 0: minion.alive = False
            projectiles.remove(p)
        elif boss.alive and p.rect().colliderect(pygame.Rect(1000, 100, 60, 100)):
            boss.hp -= 300
            if boss.hp <= 0: boss.alive = False
            projectiles.remove(p)
        elif p.x > WIDTH:
            projectiles.remove(p)

    # 抓威力切換邏輯（簡化）
    if not minion.alive and not triggered_willy_game:
        triggered_willy_game = True
        result = 'win'  # 可替換 run_willy_game() 呼叫
        if result == 'fail':
            screen.blit(score_font.render("You Failed to Catch Willy!", True, RED), (WIDTH//2 - 200, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

    if not player.alive:
        screen.blit(score_font.render("Game Over!", True, RED), (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break
    if not boss.alive:
        screen.blit(score_font.render("You Win!", True, GREEN), (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()