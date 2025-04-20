import pygame
import sys
import random

pygame.init()
pygame.mixer.init()

WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))

clock = pygame.time.Clock()

# 顏色與字型
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
BLACK = (0, 0, 0)
font = pygame.font.SysFont(None, 18)
time_font = pygame.font.SysFont(None, 28)
dialog_font_small = pygame.font.SysFont(None, 18)
dialog_font_big = pygame.font.SysFont(None, 28)
score_font = pygame.font.SysFont(None, 48)

# 玩家設定
player_size = 40
player_pos = [100, 100]
player_speed = 5

# 載入圖片
willly = pygame.transform.scale(
    pygame.image.load("willy.png").convert_alpha(), (80, 80)
    # convert_alpha -> 把圖片轉成支援透明度
)
# pygame.transform.scale(..., (80, 80)) -> 縮成 80*80 的大小
willy_rect = willly.get_rect()
# .get_rect()函式會回傳一個矩形物件
willy_mask = pygame.mask.from_surface(willly)
# 從圖片建立一個遮罩（mask)記錄哪些像素是不透明的 → 用來進行像素級碰撞偵測

dialog_img = pygame.transform.scale(
    pygame.image.load("dialog.png").convert_alpha(), (150, 90)
)
dialog_rect = dialog_img.get_rect()

# 載入語音
voice_intro = pygame.mixer.Sound("catchme.wav")
voice_ouch = pygame.mixer.Sound("ouch.wav")

# 狀態變數
score = 0
show_begin = True # 控制是否顯示catch me...開場對話
said_begin = False # 控制開場語音只播一次
show_ouch = False # 控制是否顯示ouch...並播放語音
begin_timer = 0 # 紀錄開場開始的時間點（用來做倒數）
ouch_timer = 0 # 紀錄每次被抓時開始的時間（倒數關閉）
spawn_time = 0  # 威力出現時間
goal = 10  # 目標抓10次
level_timer = 30000  # 限時30秒
start_time = pygame.time.get_ticks()
willy_interval = 2000  # 初始Willy出現時間

# 重設威力
def reset_willy():
    willy_rect.center = [
        random.randint(60, WIDTH - 60),
        random.randint(60, HEIGHT - 60)
    ]

# 分行文字渲染
def render_multiline(text, font, color, surface, x, y, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word + " "
    lines.append(current_line)
    for i, line in enumerate(lines):
        surface.blit(font.render(line.strip(), True, color), (x, y + i * font.get_linesize()))

# 初始化
reset_willy()
begin_timer = pygame.time.get_ticks()
spawn_time = pygame.time.get_ticks()

# 遊戲主迴圈
running = True
while running:
    screen.fill(WHITE)
    now = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 玩家移動
    keys = pygame.key.get_pressed()
    # 回傳一個「鍵盤狀態的列表（list of bool），每個鍵的狀態（有沒有被按下）都儲存在keys裡
    # 如果←鍵被按下就會是 True
    if keys[pygame.K_LEFT]: player_pos[0] -= player_speed #x座標-5
    if keys[pygame.K_RIGHT]: player_pos[0] += player_speed
    if keys[pygame.K_UP]: player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]: player_pos[1] += player_speed

    # 限制玩家不出畫面邊界
    #x 座標
    if player_pos[0] < 0:
        player_pos[0] = 0
    elif player_pos[0] > WIDTH - player_size:
        player_pos[0] = WIDTH - player_size
    # y座標
    if player_pos[1] < 0:
        player_pos[1] = 0
    elif player_pos[1] > HEIGHT - player_size:
        player_pos[1] = HEIGHT - player_size

    # 玩家遮罩
    player_rect = pygame.Rect(*player_pos, player_size, player_size)
    player_surf = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
    pygame.draw.rect(player_surf, BLUE, (0, 0, player_size, player_size))
    player_mask = pygame.mask.from_surface(player_surf)

    # 碰撞偵測
    offset = (willy_rect.left - player_rect.left, willy_rect.top - player_rect.top)
    # 玩家抓到 Willy
    if player_mask.overlap(willy_mask, offset):
        score += 1
        reset_willy()
        spawn_time = now  # 重設威力出現時間
        show_ouch = True
        ouch_timer = now
        voice_ouch.play()
    
        # 每抓到一次，讓Willy的閃現速度加快（最多加速到0.6秒）
        willy_interval = max(600, willy_interval - 100)

    # 如果超過指定時間沒碰到 → 自動換威力
    if now - spawn_time > willy_interval:
        reset_willy()
        spawn_time = now  # 重設出現時間
        show_ouch = False

    # 判斷是否過關
    if score >= goal:
        screen.fill(WHITE)
        screen.blit(score_font.render("You Win!", True, (0, 180, 0)), (WIDTH//2 - 100, HEIGHT//2 - 30))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()


    # 判斷是否失敗（時間到還沒達成）
    if now - start_time > level_timer and score < goal:
    # 顯示失敗畫面
        screen.fill(WHITE)
        screen.blit(score_font.render("Game Over!", True, (200, 0, 0)), (WIDTH//2 - 120, HEIGHT//2 - 30))
        pygame.display.flip()
        pygame.time.wait(3000)
        pygame.quit()
        sys.exit()

    # 畫出角色 & 分數
    screen.blit(willly, willy_rect)
    screen.blit(player_surf, player_pos)
    screen.blit(score_font.render(f"Score: {score}", True, BLACK), (10, 10))
    # 顯示目前關卡與時間
    time_left = max(0, (level_timer - (now - start_time)) // 1000)
    screen.blit(time_font.render(f"Time Left: {time_left}s", True, BLACK), (10, 50))  # 上移


    # 對話框位置微調
    dialog_pos = (
        willy_rect.centerx - dialog_rect.width // 2 + 5,
        willy_rect.top - dialog_rect.height + 10
    )
    # 修正對話框位置不要超出邊界
    dialog_x = max(0, min(dialog_pos[0], WIDTH - dialog_rect.width))
    dialog_y = max(0, min(dialog_pos[1], HEIGHT - dialog_rect.height))
    dialog_pos = (dialog_x, dialog_y)


    # 對話顯示：開場只說一次
    if show_begin and now - begin_timer < 2500:
        if not said_begin:
            voice_intro.play()
            said_begin = True
        screen.blit(dialog_img, dialog_pos)
        screen.blit(dialog_font_small.render("Catch me if you can", True, BLACK),
                    (dialog_pos[0] + (dialog_rect.width - dialog_font_small.size("Catch me if you can")[0]) // 2,
                     dialog_pos[1] + 25))
        screen.blit(dialog_font_big.render("hehehe!", True, BLACK),
                    (dialog_pos[0] + (dialog_rect.width - dialog_font_big.size("hehehe!")[0]) // 2,
                     dialog_pos[1] + 40))
    else:
        show_begin = False

    # 播出 OUCH！
    if show_ouch:
        screen.blit(dialog_img, dialog_pos)
        screen.blit(dialog_font_big.render("OUCH!", True, BLACK),
                    (dialog_pos[0] + (dialog_rect.width - dialog_font_big.size("OUCH!")[0]) // 2,
                     dialog_pos[1] + 25))
        screen.blit(dialog_font_small.render("You got me!", True, BLACK),
                    (dialog_pos[0] + (dialog_rect.width - dialog_font_small.size("You got me!")[0]) // 2,
                     dialog_pos[1] + 43))
        if now - ouch_timer > 1000:
            show_ouch = False

    pygame.display.flip()
    clock.tick(60)