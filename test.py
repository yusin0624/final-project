import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 設定遊戲視窗大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Cesium Game")

# 定義顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# 定義玩家的設定
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# 設定掉落物體
block_width = 50
block_height = 50
block_speed = 5
blocks = []

# 設定遊戲幀率
clock = pygame.time.Clock()

# 設定分數
score = 0

# 定義字型
font = pygame.font.SysFont("Arial", 30)

def draw_player(x, y):
    pygame.draw.rect(screen, BLACK, (x, y, player_width, player_height))

def draw_blocks(blocks):
    for block in blocks:
        pygame.draw.rect(screen, RED, block)

def create_new_block():
    block_x = random.randint(0, WIDTH - block_width)
    block_y = -block_height
    return pygame.Rect(block_x, block_y, block_width, block_height)

def game_over():
    text = font.render(f"Game Over! Score: {score}", True, BLACK)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.update()
    pygame.time.wait(2000)  # 顯示 2 秒後結束遊戲
    pygame.quit()
    sys.exit()

# 遊戲主循環
while True:
    screen.fill(WHITE)
    
    # 事件處理
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 玩家控制
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # 新的方塊掉落
    if random.randint(1, 100) <= 3:  # 有小機會掉落方塊
        blocks.append(create_new_block())

    # 更新方塊位置
    for block in blocks:
        block.y += block_speed
        if block.y > HEIGHT:  # 超過螢幕底部，重新出現
            blocks.remove(block)
            score += 1

        # 檢查碰撞
        if block.colliderect(pygame.Rect(player_x, player_y, player_width, player_height)):
            game_over()

    # 顯示分數
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # 繪製玩家和方塊
    draw_player(player_x, player_y)
    draw_blocks(blocks)

    # 更新畫面
    pygame.display.update()

    # 控制幀率
    clock.tick(60)
