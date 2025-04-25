import pygame
from character_oh import Player, Monster
import random
from renew_state_display import draw_hp

# 初始化 Pygame
pygame.init()
font = pygame.font.SysFont("couriernew", 28, bold=True)

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

monster1 = Monster("Shadow Disciple", 1500, 1500, 100, (1000, HEIGHT - 400)) 
monster2 = Monster("Shadow Commander", 2000, 2000, 150, (1000, HEIGHT - 400)) 
monster3 = Monster("Volley Empress", 3000, 3000, 175, (1000, HEIGHT - 400)) 
player = Player(100)

attack_timer = 0
transition_timer = 0
flickering_timer = 0
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
        player.y -= 10
        #player.rect.topleft = (player.x, player.y)  # 更新 player_rect 的位置
        player.rect.topleft = (player.x - 30, player.y + 30)
    if keys[pygame.K_s]:
        player.y += 10
        #player.rect.topleft = (player.x, player.y)  # 更新 player_rect 的位置
        player.rect.topleft = (player.x - 30, player.y + 30)
    if keys[pygame.K_d]:
        cloud_speed = 20
    if keys[pygame.K_a]:
        cloud_speed = 2

    if player.y < 0:
        player.y = 0
    if player.y > HEIGHT - 280:
        player.y = HEIGHT - 280
        
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
    
    if (chapter < 10):      #in chapter(fighting monsters)
        if chapter == 1:
            current_monsters = monster1
        elif chapter == 2:
            current_monsters = monster2
        elif chapter == 3:
            current_monsters = monster3
        
        # 怪獸攻擊
        attack_timer += 1
        if attack_timer % 50 == 0:  # 每 50 幀攻擊一次
            if (chapter == 1):
                monster1.attack()
            elif (chapter == 2):
                monster2.attack()
            elif (chapter == 3):
                monster3.attack()
            print({chapter})

            
        if (chapter == 1):
            monster1.update_bullets(player)  # 傳遞 player_rect 參數給怪物的子彈
        elif (chapter == 2):
            monster2.update_bullets(player)  # 傳遞 player_rect 參數給怪物的子彈
        elif (chapter == 3):
            monster3.update_bullets(player)  # 傳遞 player_rect 參數給怪物的子彈
        
        #monster state
        if(chapter == 1): 
            monster1.draw(screen)
            draw_hp(monster1, screen, font, 50, 100)
        if(chapter == 2): 
            monster2.draw(screen)
            draw_hp(monster2, screen, font, 50, 100)
        elif(chapter == 3):
            monster3.draw(screen)
            draw_hp(monster3, screen, font, 50, 100)
        
        # player攻擊
        #player_attack.handle_attack(self, projectiles)
        player.player_attack(projectiles, screen, current_monsters, 100)

    else:       #transition
        print(f"chapter: {chapter}, transition_timer:{transition_timer}")
        # player攻擊
        #player_attack.handle_attack(self, projectiles)
        player.player_attack(projectiles, screen, current_monsters, 0)
        
        transition_timer += cloud_speed
        #if (cloud_speed > 1000):
            #flickering_timer += 5
            #if (flickering_timer % 10 == 0): 
        transition_img = pygame.image.load("assets/transition_1.png")
        transition_img = pygame.transform.scale(transition_img, (333, 188))
        screen.blit(transition_img, (500, 150))
                #screen.blit("assets/transition_1", (1000, 300))
   
    
    
    
    # 繪製角色
    screen.blit(player.img, (player.x, player.y))
    draw_hp(player, screen, font, 50, 50)
    
    # chapter
    if (monster1.health > 0): chapter = 1
    elif (monster1.health <= 0 and transition_timer < 2000): chapter = 11
    elif (monster2.health > 0): 
        transition_timer = 0
        chapter = 2
    elif(monster2.health == 0 and transition_timer < 2000): chapter = 22
    elif(monster3.health > 0): 
        transition_timer = 0
        chapter = 3
    
    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()

