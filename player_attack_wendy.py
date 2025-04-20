import pygame

class Projectile:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def handle_attack(player_x, player_y, projectiles, screen):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        # 發射一發子彈（從玩家右側發射）
        projectiles.append(Projectile(player_x + 200, player_y + 100))
