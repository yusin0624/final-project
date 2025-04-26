import pygame
from character_oh import Player, Monster
import random
from renew_state_display import draw_hp
from draw_grid import draw_grid
import willlly

# 初始化 Pygame
pygame.init()
font = pygame.font.SysFont("couriernew", 28, bold=True)

# 設定視窗大小
WIDTH, HEIGHT = 1400, 750
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

monster1 = Monster("Shadow Disciple", 1500, 1500, 100, (WIDTH - 500, HEIGHT - 400)) 
monster2 = Monster("Shadow Commander", 2000, 2000, 150, (WIDTH - 500, HEIGHT - 400)) 
monster3 = Monster("Volley Empress", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400)) 
transition = Monster("Transition", 100000, 100000, 0, (-100, -100))
player = Player(100)

attack_timer = 0
transition_timer = 0
flickering_timer = 0
mouse_timer = 0
chapter = 1

#1
def transition1():
    global chapter
    global current_monster
    current_monster = transition
    pass

#2
def battle1():
    global chapter
    global current_monster
    current_monster = monster1
    monster1.attack()
    monster1.update_movement(HEIGHT)
    monster1.update_bullets(player, screen)  # 傳遞 player_rect 參數給怪物的子彈
    monster1.draw(screen)
    state_img = pygame.image.load("assets/monster3_state.png")
    state_img = pygame.transform.scale(state_img, (560, 280))
    draw_hp(monster1, screen, 950, 150, 825, -30, state_img)
    if monster1.health <= 0: chapter = 3

#3    
def transition2():
    global chapter
    global current_monster
    current_monster = transition

#4    
def battle2():
    global chapter
    global current_monster
    current_monster = monster2
    monster2.attack()
    monster2.update_movement(HEIGHT)
    monster2.update_bullets(player, screen)  # 傳遞 player_rect 參數給怪物的子彈
    monster2.draw(screen)
    state_img = pygame.image.load("assets/monster3_state.png")
    state_img = pygame.transform.scale(state_img, (560, 280))
    draw_hp(monster2, screen, 950, 150, 825, -30, state_img)

#5
def transition3():
    global chapter
    global current_monster
    current_monster = transition

#6
def battle3():
    global chapter
    global current_monster
    current_monster = monster3
    monster3.attack()
    monster3.update_movement(HEIGHT)
    monster3.update_bullets(player, screen)  # 傳遞 player_rect 參數給怪物的子彈
    monster3.draw(screen)
    state_img = pygame.image.load("assets/monster3_state.png")
    state_img = pygame.transform.scale(state_img, (560, 280))
    draw_hp(monster3, screen, 950, 150, 825, -30, state_img)

#7    
def transition4():
    global chapter
    global current_monster
    current_monster = transition
        

# 遊戲主迴圈
running = True
while running:
    global current_monster
    cloud_speed = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 鍵盤輸入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        cloud_speed = 20
    elif keys[pygame.K_a]:
        cloud_speed = 2
    if keys[pygame.K_w]:
        player.y -= cloud_speed
        #player.rect.topleft = (player.x, player.y)  # 更新 player_rect 的位置
        player.rect.topleft = (player.x - 20, player.y + 20)
    if keys[pygame.K_s]:
        player.y += cloud_speed
        #player.rect.topleft = (player.x, player.y)  # 更新 player_rect 的位置
        player.rect.topleft = (player.x - 20, player.y + 20)
    if keys[pygame.K_q] or keys[pygame.K_e]:
        game_over = willlly.willy()
        if game_over == "back_to_main":
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Moon Warriors")
            continue
    
    if player.y < 280:
        player.y = 280
    if player.y > HEIGHT - 260:
        player.y = HEIGHT - 260
    
    mouse_pressed = pygame.mouse.get_pressed()
    if mouse_pressed[0]:  # 左鍵是 index 0
        player.shrink()
        #print("mouse pressed")
    else:
        player.grow()
        
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
    screen.blit(player.img, (player.x, player.y))
    state_img = pygame.image.load("assets/player_state.png")
    state_img = pygame.transform.scale(state_img, (560, 280))
    draw_hp(player, screen, 275, 155, 20, -30, state_img)

    if chapter == 1: transition1()
    elif chapter == 2: battle1()
    elif chapter == 3: transition2()
    elif chapter == 4: battle2()
    elif chapter == 5: transition3()
    elif chapter == 6: battle3()
        
    # player攻擊
    player.player_attack(projectiles, screen, current_monster, 100)
   
    #draw_grid(screen, WIDTH, HEIGHT)

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()

