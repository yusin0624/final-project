import pygame
import random
import sys

# 初始化 Pygame
pygame.init()

# 設置窗口
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("猜數字遊戲")

# 顏色
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# 字體設置
font = pygame.font.SysFont(None, 36)

# 隨機生成要猜的數字
number_to_guess = random.randint(1, 100)

# 遊戲狀態
guesses = []
attempts = 0
game_over = False

# 函數：顯示文本
def draw_text(text, x, y, color=BLACK):
    rendered_text = font.render(text, True, color)
    screen.blit(rendered_text, (x, y))

# 主遊戲循環
while True:
    screen.fill(WHITE)

    # 檢查事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and not game_over:
            if event.key == pygame.K_1:
                guesses.append(1)
                attempts += 1
            elif event.key == pygame.K_2:
                guesses.append(2)
                attempts += 1
            elif event.key == pygame.K_3:
                guesses.append(3)
                attempts += 1
            # 可以繼續添加其他鍵來對應不同的數字

    # 顯示猜測的數字
    if not game_over:
        draw_text(f"請按 1、2、3 等數字鍵來猜測！", 150, 50)
        draw_text(f"你已經猜了 {attempts} 次", 150, 100)
        draw_text(f"你猜過的數字: {', '.join(map(str, guesses))}", 150, 150)
    else:
        if guesses[-1] == number_to_guess:
            draw_text("恭喜！你猜對了！", 200, 50, GREEN)
        else:
            draw_text("遊戲結束，請再試一次！", 200, 50, RED)

    # 檢查是否猜對了
    if guesses and guesses[-1] == number_to_guess:
        game_over = True

    pygame.display.update()
