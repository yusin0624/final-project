import pygame
import player_attack
import random

# 初始化 Pygame
pygame.init()

# 設定視窗大小
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 顏色
WHITE = (255, 255, 255)
DARK_SKY = (65, 105, 225)

# 載入背景圖片
bg_img = pygame.image.load("assets/background.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# 載入角色圖片
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (250, 250))

# 載入雲朵圖片（兩種）
cloud_images = [
    pygame.transform.scale(pygame.image.load("assets/cloud1.png"), (150, 90)),
    pygame.transform.scale(pygame.image.load("assets/cloud2.png"), (150, 90))
]

# 角色設定
player_x = 100
player_y = HEIGHT - 280
player_speed = 5
player_vel_y = 0
player_gravity = 1

# 雲朵設定（隨機選圖）
cloud_speed = 5
clouds = []
for i in range(2):  # 兩朵雲
    clouds.append({
        "x": WIDTH + i * 500,
        "y": random.randint(30, 150),
        "img": random.choice(cloud_images)
    })

# 攻擊物件列表
projectiles = []

# 遊戲主迴圈
running = True
while running:
    screen.fill(DARK_SKY)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 鍵盤輸入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_vel_y = -5
    if keys[pygame.K_s]:
        player_vel_y = 5
    if keys[pygame.K_d]:
        cloud_speed = 20
    if keys[pygame.K_a]:
        cloud_speed = 2

    # 更新角色位置
    player_y += player_vel_y
    player_vel_y = 0

    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - 280:
        player_y = HEIGHT - 280

    # 繪製背景
    screen.blit(bg_img, (0, 0))

    # 更新並繪製雲朵
    for cloud in clouds:
        cloud["x"] -= cloud_speed
        if cloud["x"] <= -150:
            cloud["x"] = WIDTH + random.randint(0, 300)
            cloud["y"] = random.randint(30, 150)
            cloud["img"] = random.choice(cloud_images)
        screen.blit(cloud["img"], (cloud["x"], cloud["y"]))

    # 繪製角色
    screen.blit(player_img, (player_x, player_y))

    # 處理攻擊
    player_attack.handle_attack(player_x, player_y, projectiles, screen)

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
