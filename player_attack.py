import pygame
import random

last_attack_time = 0  # 上次攻擊時間（毫秒）
cooldown = 300        # 冷卻時間（300 毫秒 = 0.3 秒）

# 定義星星和月亮攻擊物件
class Projectile:
    def __init__(self, x, y, type):
        self.x = x
        self.y = y
        self.type = type  # 'star' 或 'moon'
        self.speed = 10  # 攻擊物件的速度
        self.width = 20   # 攻擊物件的寬度
        self.height = 20  # 攻擊物件的高度
        
        # 根據類型載入圖片
        if self.type == 'star':
            self.image = pygame.image.load("assets/star.png")
            self.image = pygame.transform.scale(self.image, (60, 60))
        elif self.type == 'moon':
            self.image = pygame.image.load("assets/moon.png")
            self.image = pygame.transform.scale(self.image, (60, 60))
        

    def move(self):
        self.x += self.speed  # 向右移動

    def draw(self, screen):
        # 繪製圖片
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self, width):
        return self.x > width  # 如果攻擊物件超過畫面邊緣，返回 True


"""# 處理玩家攻擊
def handle_attack(player_x, player_y, projectiles, screen):
    global last_attack_time  # 用 global 把上面的變數拉進來
    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and current_time - last_attack_time > cooldown:
        projectile_type = random.choice(['star', 'moon'])
        projectile = Projectile(player_x + 50, player_y + 140, projectile_type)
        projectiles.append(projectile)
        last_attack_time = current_time  # 更新攻擊時間

    for projectile in projectiles[:]:
        projectile.move()
        if projectile.is_off_screen(1500):
            projectiles.remove(projectile)
        else:
            projectile.draw(screen)"""
            
def handle_attack(player_x, player_y, projectiles, screen, monster_rect):
    global last_attack_time
    current_time = pygame.time.get_ticks()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE] and current_time - last_attack_time > cooldown:
        projectile_type = random.choice(['star', 'moon'])
        projectile = Projectile(player_x + 50, player_y + 140, projectile_type)
        projectiles.append(projectile)
        last_attack_time = current_time

    for projectile in projectiles[:]:
        projectile.move()

        projectile_rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)

        if projectile.is_off_screen(1500) or projectile_rect.colliderect(monster_rect):
            projectiles.remove(projectile)
        else:
            projectile.draw(screen)
