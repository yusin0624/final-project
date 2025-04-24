import pygame
import random
from newnew_state import create_character, calculate_update_state
from monstertest_wendy import monster

pygame.init()

# 畫面設定
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 顏色與圖片設定
DARK_SKY = (65, 105, 225)
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (250, 250))

# 角色座標與雲朵
player_x = 100
player_y = HEIGHT - 280
player_vel_y = 0
cloud_x = WIDTH
cloud_y = 50

# 字體
font = pygame.font.Font(None, 36)

# 建立角色
player_name = "勇者阿光"
level = 1
characters = create_character(level, player_name)  # [玩家, 小兵, boss]
player, minion, boss = characters

# 玩家子彈
projectiles = []

# 遊戲迴圈
running = True
attack_timer = 0

while running:
    screen.fill(DARK_SKY)
    pygame.time.delay(30)
    attack_timer += 30

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 移動
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

    # 畫背景與雲
    pygame.draw.rect(screen, DARK_SKY, (0, 0, WIDTH, HEIGHT))
    pygame.draw.ellipse(screen, (220, 220, 220), (cloud_x, cloud_y, 100, 50))

    # 畫角色
    screen.blit(player_img, (player_x, player_y))

    # 玩家攻擊：按空白鍵發射子彈
    if keys[pygame.K_SPACE]:
        if len(projectiles) < 5:
            projectiles.append({
                "x": player_x + 200,
                "y": player_y + 100,
                "skill": random.choice(list(player.skills.items()))  # 選技能 (名稱, 傷害)
            })

    # 更新子彈
    for projectile in projectiles[:]:
        projectile["x"] += 20
        pygame.draw.circle(screen, (255, 255, 0), (projectile["x"], projectile["y"]), 10)

        skill_name, damage = projectile["skill"]

        # 子彈碰撞小兵
        if minion.alive and projectile["x"] > 1000 and projectile["y"] >= 100:
            minion.receive_damage(damage)
            print(f"{minion.name} 被擊中：{skill_name}，受到 {damage} 傷害")
            projectiles.remove(projectile)
            continue

        # 子彈碰撞 boss
        if boss.alive and projectile["x"] > 1200 and projectile["y"] >= 100:
            boss.receive_damage(damage)
            print(f"{boss.name} 被擊中：{skill_name}，受到 {damage} 傷害")
            projectiles.remove(projectile)
            continue

        # 超出畫面移除
        if projectile["x"] > WIDTH:
            projectiles.remove(projectile)

    # 怪物攻擊（每秒）
    if attack_timer >= 1000:
        if minion.alive:
            monster(1, characters)
        if boss.alive:
            monster(2, characters)

        damage_list = [
            0,
            minion.attack if minion.alive else 0,
            boss.attack if boss.alive else 0
        ]
        calculate_update_state(screen, font, characters, damage_list)
        attack_timer = 0
    else:
        calculate_update_state(screen, font, characters, [0, 0, 0])

    pygame.display.update()

pygame.quit()
