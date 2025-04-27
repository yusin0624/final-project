import pygame
import random
from character_oh import Player

WIDTH, HEIGHT = 1400, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))

def gameover(player):
    #player.hp == 0     結束遊戲
    if player.health == 0:
        screen.fill((0, 0, 0))  # 畫面變黑

        alpha = 0  # 透明度，從 0 到 255
        scale = 0.5  # 初始縮小一點點
        start_time = pygame.time.get_ticks()

        while alpha < 255:
            now = pygame.time.get_ticks()
            elapsed = now - start_time

            # 每次都清空畫面
            screen.fill((0, 0, 0))

            # 逐漸增加透明度和大小
            alpha = min(255, elapsed // 5)  # 5毫秒增加一點點透明度
            scale = min(1.5, 0.5 + elapsed / 2000)  # 2秒內從 0.5x 放大到 1.5x

            # 動態調整字型大小
            dynamic_font_size = int(60 * scale)
            dynamic_font = pygame.font.SysFont("couriernew" , dynamic_font_size , bold = True)

            # Game Over 字
            game_over_text = dynamic_font.render("Game Over" , True , (255 , 0 , 0))
            game_over_text.set_alpha(alpha)
            game_over_rect = game_over_text.get_rect(center = (WIDTH // 2 , HEIGHT // (2 - 40)))

            # Nothing can go wrong 字
            nothing_text = dynamic_font.render("Nothing can go wrong..." , True , (255 , 0 , 0))
            nothing_text.set_alpha(alpha)
            nothing_rect = nothing_text.get_rect(center = (WIDTH // 2 , HEIGHT // (2 + 40)))

            screen.blit(game_over_text, game_over_rect)
            screen.blit(nothing_text, nothing_rect)

            pygame.display.update()
            pygame.time.delay(30)  # 每 30 毫秒更新一次動畫

        pygame.time.wait(3000)  # 全部出現後等 3 秒
        running = False