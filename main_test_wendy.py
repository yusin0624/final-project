import pygame
import player_attack
from new_state import create_character, calculate_update_state
from monstertest_wendy import monster

# 初始化 Pygame
pygame.init()

# 設定視窗大小
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 顏色與圖片設定
DARK_SKY = (65, 105, 225)
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (250, 250))

# 角色座標
player_x = 100
player_y =  HEIGHT - 280
player_vel_y = 0

# 雲朵設定
cloud_x = WIDTH
cloud_y = 50

# 字型設定
font = pygame.font.Font(None, 36)

# 初始化角色資料
player_name = "勇者阿光"
level = 1
characters = create_character(level, player_name)  # [玩家, 小兵, boss]

# 玩家攻擊物件
projectiles = []

# 遊戲主迴圈
running = True
attack_timer = 0  # 怪物攻擊冷卻計時器

while running:
    screen.fill(DARK_SKY)
    pygame.time.delay(30)
    attack_timer += 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 玩家移動
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_vel_y = -5
    elif keys[pygame.K_s]:
        player_vel_y = 5
    else:
        player_vel_y = 0

    player_y += player_vel_y
    player_y = max(0, min(player_y, HEIGHT - 280))

    # 雲朵動畫
    cloud_x -= 5
    if cloud_x <= -100:
        cloud_x = WIDTH

    # 畫背景與雲朵
    pygame.draw.rect(screen, DARK_SKY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.ellipse(screen, (220, 220, 220), (cloud_x, cloud_y, 100, 50))

    # 畫角色
    screen.blit(player_img, (player_x, player_y))

    # 玩家攻擊（按空白鍵會新增 projectiles，並顯示在畫面）
    player_attack.handle_attack(player_x, player_y, projectiles, screen)

    # 怪物攻擊邏輯（每秒）
    if attack_timer >= 1000:
        if characters[1].alive:
            monster(1, characters)
        if characters[2].alive:
            monster(2, characters)

        damage_list = [
            0,
            characters[1].attack if characters[1].alive else 0,
            characters[2].attack if characters[2].alive else 0
        ]

        calculate_update_state(screen, font, characters, damage_list)
        attack_timer = 0
    else:
        # 沒有攻擊時只顯示血條
        calculate_update_state(screen, font, characters, [0, 0, 0])

    pygame.display.update()

pygame.quit()
