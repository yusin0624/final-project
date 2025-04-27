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
for i in range(5):  # 五朵雲
    clouds.append({
        "x": WIDTH + i * 500,
        "y": random.randint(30, 150),
        "img": random.choice(cloud_images)
    })

# 物件列表
projectiles = []
player = Player(100)
monsters = [
    Monster("Transition", 100000, 100000, 0, (-100, -100), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
    Monster("Flame Tyrant", 1500, 1500, 100, (WIDTH - 500, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
    Monster("Void Spitter", 2000, 2000, 150, (WIDTH - 500, HEIGHT - 400), "assets/monster2.png", "assets/fireball2.png", "assets/monster3_state.png", "assets/transition_2.png", "assets/monster2_damage.png"),
    Monster("Volley Empress", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png"),
]

attack_timer = 0
transition_timer = 0
flickering_timer = 0
mouse_timer = 0
chapter = 1
current_monster = 0     #index
phase = "transition"  # "transition" or "battle"
running = True

def update_and_draw_game():
    global chapter
    
    screen.blit(bg_img, (0, 0))

    # 雲朵更新
    for cloud in clouds:
        cloud["x"] -= cloud_speed
        if cloud["x"] <= -150:
            cloud["x"] = WIDTH + random.randint(0, 300)
            cloud["y"] = random.randint(30, 150)
            cloud["img"] = random.choice(cloud_images)
        screen.blit(cloud["img"], (cloud["x"], cloud["y"]))

    # 玩家繪製
    screen.blit(player.img, (player.x, player.y))
    state_img = pygame.image.load("assets/player_state.png")
    state_img = pygame.transform.scale(state_img, (560, 280))
    draw_hp(player, screen, 275, 155, 20, -30, state_img)
    
    player.player_attack(projectiles, screen, monsters[current_monster], 100)


    # 怪物繪製
    if phase == "battle":
        if current_monster:
            monsters[current_monster].attack()
            monsters[current_monster].update_movement(HEIGHT)
            monsters[current_monster].update_bullets(player, screen)  # 傳遞 player_rect 參數給怪物的子彈
            monsters[current_monster].draw(screen)
            draw_hp(monsters[current_monster], screen, 950, 150, 825, -30, monsters[current_monster].state_img)
 
def transition_phase(cloud_speed, transition_img):
    global phase, transition_timer, chapter, transition_y, transition_direction
    
    speed = cloud_speed
    transition_timer += speed
    
    # if transition_timer % 10 == 0: print(f"transition_timer: {transition_timer}")
    if transition_timer == speed:
        transition_y = -375
        transition_direction = "down"

    # 控制 transition 移動
    if transition_timer >= 300 and transition_timer < 800:
        if transition_direction == "down":
            transition_y += 675 / 500 * speed
            if transition_y >= 300:
                transition_y = 300

    elif transition_timer >= 800 and transition_timer < 1200:
        transition_y = 300

    elif transition_timer >= 1200 and transition_timer < 1700:
        transition_y += 675 / 500 * speed
        if transition_y <= -375:
            transition_y = -375
    
    screen.blit(transition_img, (600, transition_y))

    if (transition_timer >= 800):
        draw_hp(monsters[int(chapter / 2)], screen, 950, 150, 825, -30, monsters[int(chapter / 2)].state_img)
    if (transition_timer >= 1700):
        transition_timer = 0
        chapter += 1
        phase = "battle"
    
def battle_phase(monster):
    global phase, chapter, current_monster

    current_monster = monster
    if monsters[current_monster].health <= 0:
        current_monster = 0
        phase = "transition"
        chapter += 1

# 遊戲主迴圈
while running:
    cloud_speed = 10

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    update_and_draw_game()
    
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
    
    # 控制章節流程(1, 3, 5 transition; 2, 4, 6 balltle)
    if chapter % 2 != 0:
        transition_img = monsters[int((chapter + 1) / 2)].transition_img
        transition_phase(cloud_speed, transition_img)
    else:
        current_monster = int(chapter / 2)
        battle_phase(current_monster)
        
    # player攻擊
    player.player_attack(projectiles, screen, monsters[current_monster], 100)

    # draw_grid(screen, WIDTH, HEIGHT)

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()