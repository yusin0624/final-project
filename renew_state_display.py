import pygame

# 顏色設定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# player draw
def draw_hp(character, screen, x, y, img_x, img_y, state_img) :
    # 畫血條 (用pygame.draw.rect畫出矩形)
    pygame.draw.rect(screen, RED, (x, y, 250, 30))
    hp_ratio = character.health / character.max_health if character.max_health > 0 else 0
    pygame.draw.rect(screen, GREEN, (x, y, int(250 * hp_ratio), 30))
    screen.blit(state_img, (img_x, img_y))