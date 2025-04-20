import pygame
from new_state import create_character, calculate_update_state
from monstertest_wendy import monster

# 初始化 Pygame
pygame.init()

# 設定視窗大小
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 設定顏色
DARK_SKY = (65, 105, 225)

# 載入角色圖片
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (250, 250))

# 角色設定
player_x = 100
player_y = HEIGHT - 280
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

# 遊戲主迴圈
running = True
attack_timer = 0  # 怪物攻擊冷卻時間
while running:
    screen.fill(DARK_SKY)
    pygame.time.delay(30)
    attack_timer += 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 控制角色上下
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_vel_y = -5
    elif keys[pygame.K_s]:
        player_vel_y = 5
    else:
        player_vel_y = 0

    player_y += player_vel_y
    player_y = max(0, min(player_y, HEIGHT - 280))  # 限制不出界

    # 雲朵動畫
    cloud_x -= 5
    if cloud_x <= -100:
        cloud_x = WIDTH

    # 畫背景與雲朵
    pygame.draw.rect(screen, DARK_SKY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.ellipse(screen, (220, 220, 220), (cloud_x, cloud_y, 100, 50))

    # 畫角色
    screen.blit(player_img, (player_x, player_y))

    # 怪物每 1 秒攻擊一次
    if attack_timer >= 1000:
        monster(1, characters)  # 小兵攻擊
        monster(2, characters)  # boss 攻擊
        attack_timer = 0

    # 顯示血條
    calculate_update_state(screen, font, characters, [0, 0, 0])

    pygame.display.update()

pygame.quit()
