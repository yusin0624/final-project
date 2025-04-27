import pygame
from character_oh import Player, Monster
import random
from renew_state_display import draw_hp
from draw_grid import draw_grid
import willlly
import math

# 初始化 Pygame
pygame.init()
font = pygame.font.SysFont("couriernew", 28, bold=True)
# 背景音樂播放
pygame.mixer.init()
pygame.mixer.music.load("assets/sailormusic.ogg")  # 建議用 ogg 檔
pygame.mixer.music.play(loops=-1)  # -1 代表無限循環


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
    Monster("Flame Tyrant", 1500, 1500, 100, (WIDTH - 500, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster1_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
    Monster("Void Spitter", 2000, 2000, 150, (WIDTH - 500, HEIGHT - 400), "assets/monster2.png", "assets/fireball2.png", "assets/monster2_state.png", "assets/transition_2.png", "assets/monster2_damage.png"),
    Monster("Volley Empress", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png"),
    Monster("Tennis Phantom", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400), "assets/monster4.png", "assets/fireball4.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png"),
]

attack_timer = 0
transition_timer = 0
flickering_timer = 0
mouse_timer = 0
chapter = 1
current_monster = 0     #index
phase = "transition"  # "transition" or "battle"
running = True
float_timer = 0  # 新增一個計時器

def update_and_draw_game():
    global chapter, float_timer  # <--- 加上 float_timer

    screen.blit(bg_img, (0, 0))

    # 雲朵更新
    for cloud in clouds:
        cloud["x"] -= cloud_speed
        if cloud["x"] <= -150:
            cloud["x"] = WIDTH + random.randint(0, 300)
            cloud["y"] = random.randint(30, 150)
            cloud["img"] = random.choice(cloud_images)
        screen.blit(cloud["img"], (cloud["x"], cloud["y"]))

    # 玩家浮動效果
    float_timer += 0.25
    float_offset = math.sin(float_timer) * 8  # 上下浮動 ±10像素

    # 玩家繪製（加上浮動）
    screen.blit(player.img, (player.x, player.y + float_offset))
    state_img = pygame.image.load("assets/player_state.png")
    state_img = pygame.transform.scale(state_img, (560, 280))
    draw_hp(player, screen, 275, 155, 20, -30, state_img)
    
    player.player_attack(projectiles, screen, monsters[current_monster], 100)

    # 怪物繪製
    if phase == "battle":
        if current_monster:
            monsters[current_monster].attack()
            monsters[current_monster].update_movement(HEIGHT)
            monsters[current_monster].update_bullets(player, screen)
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
        draw_hp(monsters[(chapter + 1) // 2], screen, 950, 150, 825, -30, monsters[(chapter + 1) // 2].state_img)
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

def gameover():
    screen.fill((0, 0, 0))  # 畫面變黑

    alpha = 0
    scale = 0.5
    start_time = pygame.time.get_ticks()

    while alpha < 255:
        now = pygame.time.get_ticks()
        elapsed = now - start_time

        screen.fill((0, 0, 0))

        alpha = min(255, elapsed // 5)
        scale = min(1.5, 0.5 + elapsed / 2000)

        dynamic_font_size = int(60 * scale)
        dynamic_font = pygame.font.SysFont("couriernew", dynamic_font_size, bold=True)

        game_over_text = dynamic_font.render("Game Over", True, (255, 0, 0))
        game_over_text.set_alpha(alpha)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // (2 - 40)))

        nothing_text = dynamic_font.render("Nothing can go wrong...", True, (255, 0, 0))
        nothing_text.set_alpha(alpha)
        nothing_rect = nothing_text.get_rect(center=(WIDTH // 2, HEIGHT // (2 + 40)))

        screen.blit(game_over_text, game_over_rect)
        screen.blit(nothing_text, nothing_rect)

        pygame.display.update()
        pygame.time.delay(30)

    # 全部出現後，停住讓玩家選擇
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Enter 鍵
                    return "restart"
                if event.key == pygame.K_ESCAPE:  # ESC 鍵
                    pygame.quit()
                    exit()

        screen.fill((0, 0, 0))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(nothing_text, nothing_rect)

        hint_font = pygame.font.SysFont("couriernew", 32, bold=True)
        hint_text = hint_font.render("Press ENTER to Restart or ESC to Quit", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
        screen.blit(hint_text, hint_rect)

        pygame.display.update()
        pygame.time.delay(30)
    

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
    
    if player.y < 220:
        player.y = 220
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

    #遊戲結束畫面
    if player.health <= 0:
        result = gameover()
        if result == "restart":
            # 重新設定初始狀態
            player = Player(100)
            projectiles.clear()
            monsters = [
                Monster("Transition", 100000, 100000, 0, (-100, -100), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
                Monster("Blazing Howler", 1500, 1500, 100, (WIDTH - 500, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
                Monster("Void Spitter", 2000, 2000, 150, (WIDTH - 500, HEIGHT - 400), "assets/monster2.png", "assets/fireball2.png", "assets/monster3_state.png", "assets/transition_2.png", "assets/monster2_damage.png"),
                Monster("Volley Empress", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png"),
            ]
            attack_timer = 0
            transition_timer = 0
            flickering_timer = 0
            mouse_timer = 0
            chapter = 1
            current_monster = 0
            phase = "transition"
        else:
            break  #退出遊戲

    if chapter == 19 :
        result = gameover()
        if result == "restart":
            # 重新設定初始狀態
            player = Player(100)
            projectiles.clear()
            monsters = [
                Monster("Transition", 100000, 100000, 0, (-100, -100), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
                Monster("Blazing Howler", 1500, 1500, 100, (WIDTH - 500, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png"),
                Monster("Void Spitter", 2000, 2000, 150, (WIDTH - 500, HEIGHT - 400), "assets/monster2.png", "assets/fireball2.png", "assets/monster3_state.png", "assets/transition_2.png", "assets/monster2_damage.png"),
                Monster("Volley Empress", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png"),
            ]
            attack_timer = 0
            transition_timer = 0
            flickering_timer = 0
            mouse_timer = 0
            chapter = 1
            current_monster = 0
            phase = "transition"
        else:
            break  #退出遊戲
        

    # draw_grid(screen, WIDTH, HEIGHT)

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()