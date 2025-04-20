# 完整整合版：Moon Warriors（含抓威力小遊戲）

import pygame
import sys
import random

# 初始化
pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")
clock = pygame.time.Clock()

# ==================== 顏色與字型 ====================
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 100, 255)
font = pygame.font.SysFont(None, 28)
score_font = pygame.font.SysFont(None, 48)

def run_willy_game():
    WIDTH, HEIGHT = 640, 480
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    font_small = pygame.font.SysFont(None, 18)
    font_big = pygame.font.SysFont(None, 28)
    dialog_img = pygame.Surface((150, 90), pygame.SRCALPHA)
    dialog_img.fill((255, 255, 255, 200))
    player_pos = [100, 100]
    player_size = 40
    player_speed = 5
    score = 0
    show_begin = True
    said_begin = False
    show_ouch = False
    begin_timer = pygame.time.get_ticks()
    ouch_timer = 0
    spawn_time = pygame.time.get_ticks()
    goal = 10
    level_timer = 30000
    start_time = pygame.time.get_ticks()
    willy_interval = 2000
    willy = pygame.Surface((80, 80), pygame.SRCALPHA)
    pygame.draw.circle(willy, (255, 200, 0), (40, 40), 40)
    willy_rect = willy.get_rect()
    willy_mask = pygame.mask.from_surface(willy)
    def reset_willy():
        willy_rect.center = [random.randint(60, WIDTH - 60), random.randint(60, HEIGHT - 60)]
    reset_willy()

    while True:
        screen.fill(WHITE)
        now = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]: player_pos[0] += player_speed
        if keys[pygame.K_UP]: player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]: player_pos[1] += player_speed
        player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - player_size, player_pos[1]))

        player_rect = pygame.Rect(*player_pos, player_size, player_size)
        player_surf = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        pygame.draw.rect(player_surf, BLUE, (0, 0, player_size, player_size))
        player_mask = pygame.mask.from_surface(player_surf)

        offset = (willy_rect.left - player_rect.left, willy_rect.top - player_rect.top)
        if player_mask.overlap(willy_mask, offset):
            score += 1
            reset_willy()
            spawn_time = now
            show_ouch = True
            ouch_timer = now
            willy_interval = max(600, willy_interval - 100)

        if now - spawn_time > willy_interval:
            reset_willy()
            spawn_time = now
            show_ouch = False

        if score >= goal:
            screen.fill(WHITE)
            screen.blit(score_font.render("You Win!", True, (0, 180, 0)), (WIDTH//2 - 100, HEIGHT//2 - 30))
            pygame.display.flip()
            pygame.time.wait(2000)
            return 'win'

        if now - start_time > level_timer and score < goal:
            screen.fill(WHITE)
            screen.blit(score_font.render("Game Over!", True, (200, 0, 0)), (WIDTH//2 - 120, HEIGHT//2 - 30))
            pygame.display.flip()
            pygame.time.wait(2000)
            return 'fail'

        screen.blit(willy, willy_rect)
        screen.blit(player_surf, player_pos)
        screen.blit(score_font.render(f"Score: {score}", True, BLACK), (10, 10))
        time_left = max(0, (level_timer - (now - start_time)) // 1000)
        screen.blit(font_big.render(f"Time Left: {time_left}s", True, BLACK), (10, 50))

        dialog_pos = (willy_rect.centerx - 75, willy_rect.top - 100)
        if show_begin and now - begin_timer < 2500:
            screen.blit(dialog_img, dialog_pos)
            screen.blit(font_small.render("Catch me if you can", True, BLACK), (dialog_pos[0]+10, dialog_pos[1]+25))
            screen.blit(font_big.render("hehehe!", True, BLACK), (dialog_pos[0]+30, dialog_pos[1]+45))
        else:
            show_begin = False
        if show_ouch:
            screen.blit(dialog_img, dialog_pos)
            screen.blit(font_big.render("OUCH!", True, BLACK), (dialog_pos[0]+30, dialog_pos[1]+30))
            screen.blit(font_small.render("You got me!", True, BLACK), (dialog_pos[0]+20, dialog_pos[1]+55))
            if now - ouch_timer > 1000:
                show_ouch = False

        pygame.display.flip()
        clock.tick(60)

# ==================== 玩家與怪物物件 ====================
class Entity:
    def __init__(self, name, max_hp, attack=0, skills=None, boss=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.skills = skills or {}
        self.boss = boss
        self.alive = True

# ==================== 創建角色與怪物 ====================
def create_entities(level):
    player = Entity("Player", 2000, skills={"星光閃耀斬":300, "流星聖槍":200, "光耀審判":1000})
    if level == 1:
        monster = Entity("暗影使徒", 1500, attack=100)
        boss = Entity("暗影指揮官", 2000, attack=150)
    else:
        monster = Entity("虛無幽靈", 2500, attack=300)
        boss = Entity("終焉魔神·涅墨西斯", 8000, attack=500, skills={"大招":800}, boss=True)
    return [player, monster, boss]

# ==================== 血條顯示函式 ====================
def draw_health_bar(screen, entity, x, y):
    pygame.draw.rect(screen, RED, (x, y, 200, 25))
    hp_ratio = entity.hp / entity.max_hp
    pygame.draw.rect(screen, GREEN, (x, y, int(200 * hp_ratio), 25))
    name = font.render(f"{entity.name} HP: {entity.hp}/{entity.max_hp}", True, BLACK)
    screen.blit(name, (x + 210, y))

# ==================== 火球類別 ====================
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
        self.hit = False
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

# ==================== 遊戲初始化 ====================
entities = create_entities(1)
player, minion, boss = entities
player_x, player_y = 100, HEIGHT - 280
player_speed = 5
bg_x = 0
bg_speed = 7
fireballs = []
triggered_willy_game = False

# ==================== 遊戲主迴圈 ====================
running = True
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_y -= player_speed
    if keys[pygame.K_DOWN]:
        player_y += player_speed
    player_y = max(0, min(HEIGHT - 280, player_y))

    bg_x -= bg_speed
    if bg_x <= -WIDTH:
        bg_x = 0
    pygame.draw.rect(screen, (65, 105, 225), (bg_x, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, (65, 105, 225), (bg_x + WIDTH, 0, WIDTH, HEIGHT))
    pygame.draw.ellipse(screen, (220, 220, 220), (bg_x + 1000, 100, 120, 60))
    pygame.draw.rect(screen, BLUE, (player_x, player_y, 50, 80))

    draw_health_bar(screen, player, 50, 20)
    draw_health_bar(screen, minion, 50, 60)
    draw_health_bar(screen, boss, 50, 100)

    if minion.hp > 0 and minion.hp < 1000:
        new_fb = Fireball(screen, (800, 100), (player_x, player_y))
        fireballs.append(new_fb)

    for fb in fireballs[:]:
        if fb.update():
            if player.alive:
                player.hp -= 100
                if player.hp <= 0:
                    player.alive = False
            fireballs.remove(fb)
        elif not fb.active:
            fireballs.remove(fb)

    if not minion.alive and not triggered_willy_game:
        triggered_willy_game = True
        result = run_willy_game()
        WIDTH, HEIGHT = 1280, 720
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        if result == 'fail':
            screen.fill(WHITE)
            screen.blit(score_font.render("You Failed to Catch Willy!", True, RED), (WIDTH//2 - 200, HEIGHT//2))
            pygame.display.flip()
            pygame.time.wait(3000)
            break

    if not player.alive:
        lose_txt = score_font.render("Game Over!", True, RED)
        screen.blit(lose_txt, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break
    elif not boss.alive:
        win_txt = score_font.render("You Win!", True, GREEN)
        screen.blit(win_txt, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        break

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

