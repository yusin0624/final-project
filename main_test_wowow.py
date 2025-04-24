import pygame
import player_attack
from new_state import create_character, calculate_update_state
import monster_test_cindy  # 加入這行
import random
from monstertest_wendy import monster               # ⬅️ 加上這一行
from new_state import RED, GREEN, WHITE, BLACK

# 初始化 Pygame
pygame.init()

# 設定視窗大小
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 字型設定
font = pygame.font.Font(None, 36)

# 載入背景圖片
bg_img = pygame.image.load("assets/background.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# 載入角色圖片
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (250, 250))

# 載入雲朵圖片（兩種）
cloud_images = [
    pygame.transform.scale(pygame.image.load("assets/cloud1.png"), (225, 135)),
    pygame.transform.scale(pygame.image.load("assets/cloud2.png"), (225, 135))
]

# 角色設定
player_x = 100
player_y = HEIGHT - 280
player_speed = 5
player_vel_y = 0
player_gravity = 1
player_rect = player_img.get_rect(topleft=(player_x, player_y))


# 雲朵設定（隨機選圖）
clouds = []
for i in range(5):  # 兩朵雲
    clouds.append({
        "x": WIDTH + i * 500,
        "y": random.randint(30, 150),
        "img": random.choice(cloud_images)
    })

# 攻擊物件列表
projectiles = []

# ✅ 建立怪獸物件
enemy_sprite = monster_test_cindy.Monster("小怪獸", 100, (1000, HEIGHT - 200))
enemy_sprite.name()
enemy_sprite.attack()

attack_timer = 0

# 初始化角色資料
player_name = "勇者阿光"
level = 1
characters = create_character(level, player_name)  # [玩家, 小兵, boss]

# 遊戲主迴圈
running = True
while running:
    cloud_speed = 5

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
    player_rect.topleft = (player_x, player_y)  # 更新 player_rect 的位置

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

    # ✅ 繪製怪獸
    enemy_sprite.draw(screen)

    # 處理攻擊
    #player_attack.handle_attack(player_x, player_y, projectiles, screen)
    player_attack.handle_attack(player_x, player_y, projectiles, screen, enemy_sprite.rect)
    attack_timer += 1
    # 怪獸攻擊計時器
    attack_timer += 1
    if attack_timer % 30 == 0:  # 每 30 幀攻擊一次
        enemy_sprite.attack()
    enemy_sprite.update_bullets(player_rect)  # 傳遞 player_rect 參數給怪物的子彈

    # ✅ 怪物攻擊邏輯（每秒）
    if attack_timer >= 1000:
        if characters[1].alive:
            monster(1, characters)
        if characters[2].alive:
            monster(2, characters)

        # 傳入實際傷害值給血條處理
        damage_list = [
            0, #test  #player never die
            characters[1].attack if characters[1].alive else 0,
            characters[2].attack if characters[2].alive else 0
        ]
        print(">>> 傷害清單：", damage_list)
        calculate_update_state(screen, font, characters, damage_list)
        attack_timer = 0
    else:
        # ✅ 改成「只更新畫面」但不扣血
        calculate_update_state(screen, font, characters, [0, 0, 0])

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()




