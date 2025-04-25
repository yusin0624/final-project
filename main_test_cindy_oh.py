import pygame
import player_test_cindy_oh
import monster_test_cindy_oh
import random

# 初始化 Pygame
pygame.init()

# 設定視窗大小
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 載入背景圖片
bg_img = pygame.image.load("assets/background.jpg")
bg_img = pygame.transform.scale(bg_img, (WIDTH, HEIGHT))

# 載入雲朵圖片（兩種）
cloud_images = [
    pygame.transform.scale(pygame.image.load("assets/cloud1.png"), (225, 135)),
    pygame.transform.scale(pygame.image.load("assets/cloud2.png"), (225, 135))
]

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

monster1 = monster_test_cindy_oh.Monster("Shadow Disciple", 1500, 1500, 100, (1000, HEIGHT - 200)) 
monster2 = monster_test_cindy_oh.Monster("Shadow Commander", 2000, 2000, 150, (1000, HEIGHT - 200)) 
monster3 = monster_test_cindy_oh.Monster("Volley Empress", 3000, 3000, 175, (1000, HEIGHT - 200)) 

attack_timer = 0

chapter = 1

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
        player_test_cindy_oh.player_y -= 5
        player_test_cindy_oh.player_rect.topleft = (player_test_cindy_oh.player_x, player_test_cindy_oh.player_y)  # 更新 player_rect 的位置
    if keys[pygame.K_s]:
        player_test_cindy_oh.player_y += 5
        player_test_cindy_oh.player_rect.topleft = (player_test_cindy_oh.player_x, player_test_cindy_oh.player_y)  # 更新 player_rect 的位置
    if keys[pygame.K_d]:
        cloud_speed = 20
    if keys[pygame.K_a]:
        cloud_speed = 2

    if player_test_cindy_oh.player_y < 0:
        player_test_cindy_oh.player_y = 0
    if player_test_cindy_oh.player_y > HEIGHT - 280:
        player_test_cindy_oh.player_y = HEIGHT - 280

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

    # 繪製角色、怪獸
    screen.blit(player_test_cindy_oh.player_img, (player_test_cindy_oh.player_x, player_test_cindy_oh.player_y))
    if(chapter == 1): monster_test_cindy_oh.monster1.draw(screen)
    if(chapter == 2): monster_test_cindy_oh.monster2.draw(screen)

    # 處理攻擊
    #player_attack.handle_attack(player_x, player_y, projectiles, screen)
    player_test_cindy_oh.player_attack(player_test_cindy_oh.player_x, player_test_cindy_oh.player_y, projectiles)
   
    # 怪獸攻擊計時器
    attack_timer += 1
    if attack_timer % 30 == 0:  # 每 30 幀攻擊一次
        if (chapter == 1):
            monster_test_cindy_oh.monster1.attack()
        elif (chapter == 2):
            monster_test_cindy_oh.monster2.attack()
        elif (chapter == 3):
            monster_test_cindy_oh.monster3.attack()
            
    if (chapter == 1):
        monster_test_cindy_oh.monster1.update_bullets(player_test_cindy_oh.player_rect)  # 傳遞 player_rect 參數給怪物的子彈
    elif (chapter == 2):
        monster_test_cindy_oh.monster2.update_bullets(player_test_cindy_oh.player_rect)  # 傳遞 player_rect 參數給怪物的子彈
    elif (chapter == 3):
        monster_test_cindy_oh.monster3.update_bullets(player_test_cindy_oh.player_rect)  # 傳遞 player_rect 參數給怪物的子彈

    # chapter
    if (monster_test_cindy_oh.monster1.health != 0): chapter = 1
    elif (monster_test_cindy_oh.monster2.health != 0): chapter = 2

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
