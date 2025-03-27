import pygame
import random
import sys

# 初始化 pygame
pygame.init()

# 設定畫面
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Avoid the Falling Blocks")

# 顏色設定
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# 玩家方塊設定
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 10
player_speed = 5

# 障礙物設定
block_width = 50
block_height = 50
block_speed = 5
blocks = []

# 遊戲時鐘設定
clock = pygame.time.Clock()

# 文字設定
font = pygame.font.SysFont(None, 55)

# 顯示遊戲結束訊息
def game_over():
    text = font.render("Game Over!", True, RED)
    screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
    pygame.display.flip()
    pygame.time.delay(2000)  # 顯示 2 秒後結束遊戲
    pygame.quit()
    sys.exit()

# 主遊戲循環
def main():
    global player_x

    while True:
        # 處理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # 控制玩家移動
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed

        # 生成新的障礙物
        if random.randint(1, 20) == 1:
            block_x = random.randint(0, WIDTH - block_width)
            blocks.append([block_x, -block_height])  # 起始位置在畫面上方

        # 更新障礙物位置
        for block in blocks[:]:
            block[1] += block_speed
            if block[1] > HEIGHT:
                blocks.remove(block)

            # 檢查碰撞
            if player_x < block[0] + block_width and player_x + player_width > block[0] and player_y < block[1] + block_height and player_y + player_height > block[1]:
                game_over()

        # 塗背景顏色
        screen.fill(WHITE)

        # 畫玩家方塊
        pygame.draw.rect(screen, BLUE, (player_x, player_y, player_width, player_height))

        # 畫障礙物
        for block in blocks:
            pygame.draw.rect(screen, RED, (block[0], block[1], block_width, block_height))

        # 更新畫面
        pygame.display.flip()

        # 設定遊戲幀率
        clock.tick(60)

# 開始遊戲
if __name__ == "__main__":
    main()