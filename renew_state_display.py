import pygame
import monster_test_cindy_oh

# 顏色設定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def draw_hp(self , screen , font , x = 50 , y = 50 , spacing=60) :
    blood_y = y + spacing  #最上面的
    # 畫血條
    pygame.draw.rect(screen, RED, (x, blood_y, 100, 20))
    hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
    pygame.draw.rect(screen, GREEN, (x, blood_y, int(100 * hp_ratio), 20))

    # 顯示 HP 數字
    name_text = font.render(f"{self.name} HP: {self.hp}/{self.max_hp}", True, WHITE)
    screen.blit(name_text, (x + 110, blood_y))

