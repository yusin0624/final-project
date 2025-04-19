import pygame
import player_attack

# 初始化 Pygame
pygame.init()

# 設定視窗大小
WIDTH, HEIGHT = 1500, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moon Warriors")

# 設定顏色
WHITE = (255, 255, 255)
DARK_SKY = (65, 105, 225)

# 載入角色圖片
player_img = pygame.image.load("assets/player.png")  # 載入圖片
#player_img = pygame.transform.scale(player_img, (188, 280))  # 縮放至適當大小
player_img = pygame.transform.scale(player_img, (250, 250))  # 縮放至適當大小


# 角色設定
player_x = 100  # 初始位置
player_y = HEIGHT - 280  # 放在地面上
player_speed = 5  # 移動速度
player_vel_y = 0  # 垂直速度
player_gravity = 1  # 重力效果

# 背景設定
bg_x = 0  # 背景 X 座標
bg_speed = 7  # 預設背景移動速度

# 雲朵設定
cloud_x = WIDTH  # 雲朵從畫面右側開始
cloud_y = 50  # 雲朵的 Y 位置

# 攻擊物件列表
projectiles = []

# 遊戲主迴圈
running = True
while running:
    cloud_speed = 5  # 雲朵的移動速度

    screen.fill(DARK_SKY)  # 清空畫面
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 取得鍵盤輸入
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_vel_y = -5  # 向上移動
    if keys[pygame.K_s]:
        player_vel_y = 5  # 向下移動
    if keys[pygame.K_d]:
        cloud_speed = 20  # 增加背景速度
    if keys[pygame.K_a]:
        cloud_speed = 2  # 減少背景速度
            
    # 更新角色位置
    player_y += player_vel_y
    player_vel_y = 0  # 防止持續加速
    
    # 限制角色不超出視窗範圍
    if player_y < 0:
        player_y = 0
    if player_y > HEIGHT - 280:
        player_y = HEIGHT - 280
    
    """
    # 更新背景位置
    bg_x -= bg_speed  # 背景往左移動
    if bg_x <= -WIDTH:
        bg_x = 0  # 無限循環背景
    """
    
    # 更新雲朵位置
    cloud_x -= cloud_speed
    if cloud_x <= -100:
        cloud_x = WIDTH  # 讓雲朵重新進入畫面
    
    # 繪製背景（這裡用填充顏色，未來可以改成背景圖片）
    pygame.draw.rect(screen, DARK_SKY, (bg_x, 0, WIDTH, HEIGHT))
    pygame.draw.rect(screen, DARK_SKY, (bg_x + WIDTH, 0, WIDTH, HEIGHT))
    
    # 繪製雲朵
    pygame.draw.ellipse(screen, (220, 220, 220), (cloud_x, cloud_y, 100, 50))
    
    # 繪製角色
    screen.blit(player_img, (player_x, player_y))
    
    # 處理攻擊
    player_attack.handle_attack(player_x, player_y, projectiles, screen)
    
    pygame.display.update()
    pygame.time.delay(30)  # 控制遊戲速度

pygame.quit()
