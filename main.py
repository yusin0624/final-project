import pygame
from character_oh import Player, Monster
import random
from renew_state_display import draw_hp
from draw_grid import draw_grid
import willlly
import math
import time
from greeny_effect import GreenyEffect
import json
import sys

# =================
#    Initialize
# =================

def InitGame():
    global font, screen, bg_img, cloud_images, clouds, projectiles, player, monsters, WIDTH, HEIGHT, start_page
    global vic_img, greeny, success_images, fail_images, moon_warriors_score, leaderboard_img, collection_img
    
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
    start_page = pygame.image.load("assets/start.png")
    vic_img = pygame.image.load("assets/victory.png")
    leaderboard_img = pygame.image.load("assets/leaderboard.png")
    collection_img = pygame.image.load("assets/collection.png")

    # 載入雲朵圖片（兩種）
    cloud_images = [
        pygame.transform.scale(pygame.image.load("assets/cloud1.png"), (225, 135)),
        pygame.transform.scale(pygame.image.load("assets/cloud2.png"), (225, 135))
    ]
    
    #載入綠頭魚
    greeny = GreenyEffect("assets/greeny.png", WIDTH, HEIGHT)

    # 雲朵設定（隨機選圖）
    clouds = []
    for i in range(5):  # 五朵雲
        clouds.append({
            "x": WIDTH + i * 500,
            "y": random.randint(30, 150),
            "img": random.choice(cloud_images)
        })

    #怪獸徽章（成功跟失敗的）
    success_images = [
        None,
        pygame.image.load("assets/monster1_success.png"),
        pygame.image.load("assets/monster2_success.png"),
        pygame.image.load("assets/monster3_success.png"),
        pygame.image.load("assets/monster4_success.png"),
        pygame.image.load("assets/monster5_success.png"),
        pygame.image.load("assets/monster6_success.png"),
        pygame.image.load("assets/monster7_success.png"),
        pygame.image.load("assets/monster8_success.png"),
        pygame.image.load("assets/monster9_success.png"),
    ]

    fail_images = [
        None,
        pygame.image.load("assets/monster1_fail.png"),
        pygame.image.load("assets/monster2_fail.png"),
        pygame.image.load("assets/monster3_fail.png"),
        pygame.image.load("assets/monster4_fail.png"),
        pygame.image.load("assets/monster5_fail.png"),
        pygame.image.load("assets/monster6_fail.png"),
        pygame.image.load("assets/monster7_fail.png"),
        pygame.image.load("assets/monster8_fail.png"),
        pygame.image.load("assets/monster9_fail.png"),
    ]
    
    for i in range(1, len(success_images)):
        success_images[i] = pygame.transform.scale(success_images[i], (200, 200))
        fail_images[i] = pygame.transform.scale(fail_images[i], (200, 200))

    moon_warriors_score = []
    moon_warriors_score = load_scoreboard()

# =====================
#    Pre-Game Setup    is_in_game == 0
# =====================

# 每次遊戲重置數據
def ResetGame():
    global attack_timer, transition_timer, flickering_timer, mouse_timer
    global chapter, current_monster, phase, start_page, running, float_timer, willy, is_in_game
    global start_time, end_time, find_willy, name, ending
    global projectiles, player, monsters

    # 物件列表
    projectiles = []
    player = Player(100, -250)
    monsters = [
        Monster("Transition", 100000, 100000, 0, (-100, -100), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_1.png", "assets/monster1_damage.png", "assets/gameover_1.png"),
        Monster("Flame Tyrant", 1500, 1500, 100, (WIDTH + 150, HEIGHT - 400), "assets/monster1.png", "assets/fireball.png", "assets/monster1_state.png", "assets/transition_1.png", "assets/monster1_damage.png", "assets/gameover_1.png"),
        Monster("Void Spitter", 2000, 2000, 150, (WIDTH + 150, HEIGHT - 400), "assets/monster2.png", "assets/fireball2.png", "assets/monster2_state.png", "assets/transition_2.png", "assets/monster2_damage.png", "assets/gameover_2.png"),
        Monster("Volley Empress", 3000, 3000, 175, (WIDTH + 150, HEIGHT - 400), "assets/monster3.png", "assets/fireball3.png", "assets/monster3_state.png", "assets/transition_3.png", "assets/monster3_damage.png", "assets/gameover_3.png"),
        Monster("Tennis Phantom", 3000, 3000, 200, (WIDTH + 150, HEIGHT - 400), "assets/monster4.png", "assets/fireball4.png", "assets/monster4_state.png", "assets/transition_4.png", "assets/monster4_damage.png", "assets/gameover_4.png"),
        Monster("Basketball Ace", 5000, 5000, 250, (WIDTH + 150, HEIGHT - 400), "assets/monster5.png", "assets/fireball5.png", "assets/monster5_state.png", "assets/transition_5.png", "assets/monster5_damage.png", "assets/gameover_5.png"),
        Monster("Banana Bomber", 4000, 4000, 200, (WIDTH + 150, HEIGHT - 400), "assets/monster6.png", "assets/fireball6.png", "assets/monster6_state.png", "assets/transition_6.png", "assets/monster6_damage.png", "assets/gameover_6.png"),
        Monster("Goblin", 4000, 4000, 200, (WIDTH + 150, HEIGHT - 400), "assets/monster7.png", "assets/fireball7.png", "assets/monster7_state.png", "assets/transition_7.png", "assets/monster7_damage.png", "assets/gameover_7.png"),
        Monster("Blood Drainer", 7000, 7000, 300, (WIDTH + 150, HEIGHT - 400), "assets/monster8.png", "assets/fireball8.png", "assets/monster8_state.png", "assets/transition_8.png", "assets/monster8_damage.png", "assets/gameover_8.png"),
        Monster("Storm Sovereign", 10000, 10000, 400, (WIDTH + 150, HEIGHT - 400), "assets/monster9.png", "assets/fireball9.png", "assets/monster9_state.png", "assets/transition_9.png", "assets/monster9_damage.png", "assets/gameover_9.png"),
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
    willy = 0
    is_in_game = 0
    find_willy = 0
    name = "Sailor Moon"
    ending = 0

# 操作教學、輸入名字
def StartPage():
    global name, is_in_game
    input_rect = pygame.Rect(50, 300, 400, 50)
    color_active = pygame.Color('lightskyblue3')

    while is_in_game == 0:
        screen.blit(start_page, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:   
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    is_in_game = 1  # 名字輸入完畢，進入遊戲
                elif event.key == pygame.K_BACKSPACE:
                    name = name[:-1]
                elif len(name) < 20 and event.unicode.isprintable():
                    name += event.unicode

        # 畫輸入框和文字
        txt_surface = font.render(name, True, (255, 255, 255))
        pygame.draw.rect(screen, color_active, input_rect, 2)
        screen.blit(txt_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()
        pygame.time.delay(30)

    
# =====================
#    Gameplay phase    is_in_game == 1
# =====================

# Main Game Loop
def update_and_draw_game(screen):
    global chapter, float_timer, HEIGHT, WIDTH, cloud_speed, current_monster, is_in_game, willy, player
    global start_time, end_time, find_willy, ending
    cloud_speed = 15

    screen.blit(bg_img, (0, 0))
    
    # 鍵盤輸入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        cloud_speed = 35
    elif keys[pygame.K_a]:
        cloud_speed = 7
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
    
    prev_projectile_count = len(projectiles)
    player.player_attack(projectiles, screen, monsters[current_monster], willy)
    if len(projectiles) > prev_projectile_count:
        greeny.register_attack()

    # 怪物繪製
    if phase == "battle":
        if current_monster:
            if monsters[current_monster].rect.x <= (WIDTH - 500):
                monsters[current_monster].attack()
            monsters[current_monster].update_movement(HEIGHT)
            monsters[current_monster].update_bullets(player, screen)
            monsters[current_monster].draw(screen)
            draw_hp(monsters[current_monster], screen, 950, 150, 825, -30, monsters[current_monster].state_img)
            
    #遊戲結束
    if player.health <= 0:
        end_time = time.time()
        is_in_game = 2
        ending = 0      #lose

    if monsters[9].health <= 0:
        end_time = time.time()
        is_in_game = 2
        ending = 1      #victory
        
    greeny.update_and_draw(screen)

# 關卡間過場     
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

# 在打怪獸
def battle_phase(monster):
    global phase, chapter, current_monster

    current_monster = monster
    if monsters[current_monster].health <= 0:
        current_monster = 0
        phase = "transition"
        chapter += 1


# =============
#    Ending    is_in_game == 2
# =============
def lose():
    global is_in_game
    screen.blit(monsters[current_monster].gameover, (0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        is_in_game = 3
        
def victory():
    global is_in_game
    screen.blit(vic_img, (0, 0))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RETURN]:
        is_in_game = 3


# ==================
#    Leaderboard    is_in_game == 3
# ==================

#display
def show_leaderboard(moon_warriors_score, start_time, end_time, find_willy, player_name):
    global player
    
    screen.blit(leaderboard_img, (0, 0))

    # 新增玩家成績(先檢查排行榜中是否已有此玩家的紀錄，沒有的話就新增)
    if not any(score["name"] == player_name for score in moon_warriors_score):
        player_score_time = end_time - start_time # 計算打怪時間
        moon_warriors_score.append({"name": player_name, "score": player.score, "time": player_score_time})
    
    # 顯示本次成績
    player_score_time = end_time - start_time
    tip_text = font.render("Your Score:", True, (255, 255, 255))
    name_text = font.render(player_name, True, (255, 255, 255))
    score_text = font.render(str(player.score), True, (255, 255, 255))
    time_text = font.render(f"{player_score_time:.2f}s", True, (255, 255, 255))

    screen.blit(tip_text, (200, 180))   
    screen.blit(name_text, (435, 180))   
    screen.blit(score_text, (835, 180))   
    screen.blit(time_text, (1025, 180))

    # 排序 : 先依造成傷害總量(由多到少)，再比時間(由快到慢)
    moon_warriors_score.sort(key=lambda x: (-x["score"], x["time"]))

    # 儲存排行榜
    save_scoreboard(moon_warriors_score)

    # 沒找到威力，排名下降一位
    if find_willy != 1:
        for j, playerrr in enumerate(moon_warriors_score[:5]):
            if playerrr["name"] == player_name and j < 4:
                # 第 j 行跟第 j+1 行交換
                moon_warriors_score[j], moon_warriors_score[j+1] = moon_warriors_score[j+1], moon_warriors_score[j] 
                

    # 把記分板印出來(前五名)
    for i, playerrr in enumerate(moon_warriors_score[:5]):
        
        time_str = f"{playerrr['time']:.2f}"
        score_str = f"{playerrr['score']}" # text must be a unicode or bytes
        rank_text = font.render(f"{i+1}.", True, (255, 255, 255))   
        name_text = font.render(playerrr["name"], True, (255, 255, 255))    
        score_text = font.render(score_str, True, (255, 255, 255))    
        time_text = font.render(time_str + "s", True, (255, 255, 255))
        tip_text = font.render("Watch out! You didn't FIND WILLY and fall one rank!", True, (255, 255, 255))
  

        y = 285 + i * 70   # 每一行的 y 座標：每行往下 70px
        screen.blit(rank_text, (200, y))   
        screen.blit(name_text, (260, y))   
        screen.blit(score_text, (660, y))   
        screen.blit(time_text, (850, y))  
    
    # 沒找到威力
    if find_willy != 1:
        screen.blit(tip_text, (250,630))   
        
# 成績資料
def save_scoreboard(scoreboard, filename="score.json"):
    with open(filename, "w") as f:  # 檔案原本就存在 : 直接清空原本內容並覆蓋 / 檔案不存在 : 會自動建立新檔案
        json.dump(scoreboard, f)

def load_scoreboard(filename="score.json"):
    try:
        with open(filename, "r") as f:  # 使用 "r" 開啟、讀取檔案，若檔案不存在 --> FileNotFoundError
            return json.load(f)
    except FileNotFoundError:
        return []  # 如果檔案不存在就回傳空列表
    
    
# =================
#    Collection    is_in_game == 3
# =================

#根據traverse_check的結果印出相對應的怪獸徽章
def show_collection(screen, monsters, results, success_images, fail_images):
    global is_in_game
    screen.blit(collection_img, (0, 0))  # 背景圖
    
    # 可調整的排版參數
    spacing_x = 220      # 圖片間的水平距離
    spacing_y = 200      # 圖片間的垂直距離（行與行之間）
    start_x = 150        # 第一列圖的起始 x 座標
    start_y = 200        # 第一列圖的起始 y 座標
    max_per_row = 5      # 每列最多幾個

    for i in range(1, len(monsters)):
        row = 0 if i <= 5 else 1                     # 前5隻在第0列，其餘在第1列
        col = (i - 1) % max_per_row                  # 第幾欄（0-4）
        x = start_x + col * spacing_x
        y = start_y + row * spacing_y

        if results[i] == 1:
            screen.blit(success_images[i], (x, y))
        else:
            screen.blit(fail_images[i], (x, y))
        
#確認打敗哪些怪獸，打敗1，沒打敗0
def traverse_check(monsters):  
    results = [0] * len(monsters)  # 預設都是0
    # 跳過 monsters[0]
    for i in range(1, len(monsters)):
        if monsters[i].health <= 0:
            results[i] = 1
    return results


InitGame()
ResetGame()

# =====================
#    MAIN GAME LOOP    
# =====================
while running:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_ESCAPE]:
        running = False    
    elif keys[pygame.K_RETURN]:
        if enter_released:  # 只有剛放開又按下才執行
            if is_in_game == 3:
                is_in_game = 4
                delay = 0
            elif is_in_game == 4:
                ResetGame()
                is_in_game = 0
            enter_released = False  # 防止連續觸發
    else:
        enter_released = True  # 放開後可以再觸發

    #start page, input player name
    if is_in_game == 0:
        StartPage()
        start_time = time.time()
    
    #game    
    elif is_in_game == 1:
        update_and_draw_game(screen)
    
    #ending
    elif is_in_game == 2:
        if ending == 0:
            lose()
        elif ending == 1:
            victory()
                
    #leaderboard
    elif is_in_game == 3:
        show_leaderboard(moon_warriors_score, start_time, end_time, find_willy, name)
    
    #collection    
    elif is_in_game == 4:
        show_collection(screen, monsters, traverse_check(monsters), success_images, fail_images)

    #draw_grid(screen, WIDTH, HEIGHT)

    pygame.display.update()
    pygame.time.delay(30)

pygame.quit()
sys.exit()