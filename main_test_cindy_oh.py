import pygame
from character_oh import Player, Monster
import random
from renew_state_display import draw_hp
from draw_grid import draw_grid
import willlly
import math
import time

def InitGame():
    global font, screen, bg_img, cloud_images, clouds, projectiles, player, monsters, WIDTH, HEIGHT
    global attack_timer, transition_timer, flickering_timer, mouse_timer
    global chapter, current_monster, phase, start_page, running, float_timer, willy, is_in_game
    global start_time, end_time, find_willy
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
    bg_img = pygame.image.load("assets/background.jpeg")
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
    player = Player(100, -250)
    monsters = [
        Monster("Transition", 100000, 100000, 0, (-100, -100), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png", "assets/gameover_1.png"),
        #Monster("Flame Tyrant", 1500, 1500, 100, (WIDTH - 500, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster1_state.png", "assets/transition_1.png", "assets/monster1_damage.png", "assets/gameover_1.png"),
        Monster("Flame Tyrant", 1500, 1500, 100, (WIDTH + 150, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster1_state.png", "assets/transition_1.png", "assets/monster1_damage.png", "assets/gameover_1.png"),
        Monster("Void Spitter", 2000, 2000, 150, (WIDTH - 500, HEIGHT - 400), "assets/monster2.png", "assets/fireball2.png", "assets/monster2_state.png", "assets/transition_2.png", "assets/monster2_damage.png", "assets/gameover_2.png"),
        Monster("Volley Empress", 3000, 3000, 175, (WIDTH - 500, HEIGHT - 400), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png", "assets/gameover_3.png"),
        Monster("Tennis Phantom", 3000, 3000, 200, (WIDTH - 500, HEIGHT - 400), "assets/monster4.png", "assets/fireball4.png", "assets/monster4_state.png", "assets/transition_4.png", "assets/monster4_damage.png", "assets/gameover_4.png"),
        Monster("Basketball Ace", 5000, 5000, 250, (WIDTH - 500, HEIGHT - 400), "assets/monster5.png", "assets/fireball5.png", "assets/monster5_state.png", "assets/transition_5.png", "assets/monster5_damage.png", "assets/gameover_5.png"),
        Monster("Banana Bomber", 4000, 4000, 200, (WIDTH - 500, HEIGHT - 400), "assets/monster6.png", "assets/fireball6.png", "assets/monster6_state.png", "assets/transition_6.png", "assets/monster6_damage.png", "assets/gameover_6.png"),
        Monster("Greenfin Warden", 4000, 4000, 200, (WIDTH - 500, HEIGHT - 400), "assets/monster7.png", "assets/fireball7.png", "assets/monster7_state.png", "assets/transition_7.png", "assets/monster7_damage.png", "assets/gameover_7.png"),
        Monster("Blood Drainer", 7000, 7000, 300, (WIDTH - 500, HEIGHT - 400), "assets/monster8.png", "assets/fireball8.png", "assets/monster8_state.png", "assets/transition_8.png", "assets/monster8_damage.png", "assets/gameover_8.png"),
        Monster("Storm Sovereign", 10000, 10000, 400, (WIDTH - 500, HEIGHT - 400), "assets/monster9.png", "assets/fireball9.png", "assets/monster9_state.png", "assets/transition_9.png", "assets/monster9_damage.png", "assets/gameover_9.png"),
    ]

    attack_timer = 0
    transition_timer = 0
    flickering_timer = 0
    mouse_timer = 0
    chapter = 1
    current_monster = 0     #index
    phase = "transition"  # "transition" or "battle"
    start_page = pygame.image.load("assets/start.png")
    screen.blit(start_page, (0, 0))
    running = True
    float_timer = 0  # 新增一個計時器
    willy = 0
    is_in_game = 0
    find_willy = 0

def update_and_draw_game(screen):
    global chapter, float_timer, HEIGHT, WIDTH, cloud_speed, current_monster, is_in_game, willy, player
    global start_time, end_time, find_willy
    cloud_speed = 10

    screen.blit(bg_img, (0, 0))
    
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
        find_willy = 1 # 有玩 willy
        # 音樂淡出 1 秒
        start_volume = pygame.mixer.music.get_volume()
        steps = 20  # 要分幾次變小，越大越滑順
        delay_per_step = 50  # 每次間隔多少毫秒，50ms

        for i in range(steps):
            volume = start_volume * (1 - i / steps)  # 音量每次變小一點
            pygame.mixer.music.set_volume(volume)
            pygame.time.delay(delay_per_step)

        # 保證最後音量是0
        pygame.mixer.music.set_volume(0)

        # 再跳進小遊戲
        game_over = willlly.willy()

        if game_over == "back_to_main":
            willy = 1
            screen = pygame.display.set_mode((WIDTH, HEIGHT))
            pygame.display.set_caption("Moon Warriors")

            # 只延遲一下下（讓小遊戲完全關閉乾淨）
            pygame.time.delay(1000)  # 停1秒，但畫面不動，不黑屏

            # 播放背景音樂，音量慢慢變大
            pygame.mixer.music.load("assets/sailormusic.ogg")
            pygame.mixer.music.play(loops=-1)
            pygame.mixer.music.set_volume(0)

            for i in range(10):  # 把音量慢慢增加
                pygame.mixer.music.set_volume(i / 10)
                pygame.time.delay(100)  # 每100ms提升一點點

    if player.x < 100:
        player.x += cloud_speed
        player.rect.topleft = (player.x - 20, player.y + 20)
    #print(player.x)
    
    if monsters[current_monster].rect.x > (WIDTH - 500):
        monsters[current_monster].rect.x -= cloud_speed
        
    if player.y < 220:
        player.y = 220
    if player.y > HEIGHT - player.rect.height:
        player.y = HEIGHT - player.rect.height
    
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

    # 雲朵更新
    for cloud in clouds:
        #if chapter % 2 != 0 and monsters[current_monster].rect.x > (WIDTH - 500):
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
    draw_hp(player, screen, 275, 155, 20, -30, player.state)
    
    player.player_attack(projectiles, screen, monsters[current_monster], willy)

    # 怪物繪製
    if phase == "battle":
        if current_monster:
            monsters[current_monster].attack()
            monsters[current_monster].update_movement(HEIGHT)
            monsters[current_monster].update_bullets(player, screen)
            monsters[current_monster].draw(screen)
            draw_hp(monsters[current_monster], screen, 950, 150, 825, -30, monsters[current_monster].state_img)
            
    #遊戲結束畫面
    if player.health <= 0:
        
        end_time = time.time()
        is_in_game = 2
        #gameover()

    if monsters[9].health <= 0:
        end_time = time.time()
        is_in_game = 3
        #gameover()     

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

def lose():
    global is_in_game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        is_in_game = 4
        
def victory():
    global is_in_game
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        is_in_game = 4

def traverse():  
    pass

# 成績資料
moon_warriors_score = []
moon_warriors_score = [
    {"name": "Joy", "time": 785},
    {"name": "Roe", "time": 358},
    {"name": "Cindy", "time": 266},
    {"name": "Wendy", "time": 30},
]

def show_leaderboard(moon_warriors_score, start_time, end_time, find_willy):

    # screen.fill((0, 0, 0)) # 轉換頁面 #黑色
    title = font.render("LEADERBOARD", True, (225, 225, 0)) # 黃色
    screen.blit(title, (450, 20))

    # 新增玩家成績
    if not any(score["name"] == "Player" for score in moon_warriors_score):
        player_score = end_time - start_time
        moon_warriors_score.append({"name": "Player", "time": player_score})

    # 排序
    moon_warriors_score.sort(key=lambda x: x["time"])

    # 沒找到威力，排名下降一位
    if find_willy != 1:
        
        for j, playerrr in enumerate(moon_warriors_score[:5]):
            if playerrr["name"] == "Player" and j != 5:
                moon_warriors_score[j], moon_warriors_score[j+1] = moon_warriors_score[j+1], moon_warriors_score[j] # 第 j 行跟第 j+1 行交換
                

    # 把記分板印出來
    for i, playerrr in enumerate(moon_warriors_score[:5]):
        time_str = f"{playerrr['time']:.2f}"
        text = f"{i+1}. {playerrr['name']} - {time_str}s"
        line = font.render(text, True, (255, 255, 255))
        screen.blit(line, (450, 70 + i*100))

    pygame.display.flip()
    
    
def restart_detect():
    if keys[pygame.K_RETURN]:
        #gameover()
        InitGame()
    else:
        vic_img = pygame.image.load("assets/victory.png")
        vic_img = pygame.transform.scale(vic_img, (WIDTH, HEIGHT))
        screen.blit(vic_img, (0, 0))
        traverse()
        # show_leaderboard(moon_warriors_score, start_time, end_time, find_willy)
    
InitGame()


# 遊戲主迴圈
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False
        
    if is_in_game == 0:
        start_time = time.time()
        if keys[pygame.K_RETURN]:
            is_in_game = 1
        
    if is_in_game == 1:
       
        update_and_draw_game(screen)
    
    elif is_in_game == 2:
        show_leaderboard(moon_warriors_score, start_time, end_time, find_willy)
        lose()
    
    elif is_in_game == 3:
        # show_leaderboard(moon_warriors_score, start_time, end_time)
        victory()
        
    elif is_in_game == 4:
        # show_leaderboard(moon_warriors_score, start_time, end_time)
        restart_detect()

    # draw_grid(screen, WIDTH, HEIGHT)

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()