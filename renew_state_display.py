import pygame
from character_oh import Player
from character_oh import Monster

# 顏色設定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# player draw
def draw_hp(character, screen, font, x, y, img_x, img_y, state_img) :
    # 畫血條 (用pygame.draw.rect畫出矩形)
    pygame.draw.rect(screen, RED, (x, y, 300, 30))
    hp_ratio = character.health / character.max_health if character.max_health > 0 else 0
    pygame.draw.rect(screen, GREEN, (x, y, int(300 * hp_ratio), 30))

    name = character.name if hasattr(character, "name") else "HP"
    #name_text = font.render(f"{name} HP: {character.health}/{character.max_health}", True, WHITE)

    screen.blit(state_img, (img_x, img_y))
    
    # 顯示 HP 數字
    # True：代表開啟抗鋸齒功能（讓字比較平滑）
    #name_text = font.render(f"{character.name} HP: {character.health}/{character.max_health}", True, WHITE)
    #畫出東西   #畫出的位置
    #screen.blit(name_text, (x + 110, y))

"""
# monster draw(小兵) (跟player_draw差在y)
def draw_hp(self , screen , font , x = 50 , y = 150 , spacing=60) :
    # 畫血條
    pygame.draw.rect(screen, RED, (x, y, 100, 20))
    hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
    pygame.draw.rect(screen, GREEN, (x, y, int(100 * hp_ratio), 20))

    # 顯示 HP 數字
    name_text = font.render(f"{self.name} HP: {self.hp}/{self.max_hp}", True, WHITE)
    screen.blit(name_text, (x + 110, y))

# monster draw(boss) (跟player_draw差在y)
def draw_hp(self , screen , font , x = 50 , y = 250 , spacing=60) :
    # 畫血條
    pygame.draw.rect(screen, RED, (x, y, 100, 20))
    hp_ratio = self.hp / self.max_hp if self.max_hp > 0 else 0
    pygame.draw.rect(screen, GREEN, (x, y, int(100 * hp_ratio), 20))

    # 顯示 HP 數字
    name_text = font.render(f"{self.name} HP: {self.hp}/{self.max_hp}", True, WHITE)
    screen.blit(name_text, (x + 110, y))
"""