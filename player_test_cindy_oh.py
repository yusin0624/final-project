import pygame
import random
import monster_test_cindy_oh
import main_test_cindy_oh

last_attack_time = 0  # 上次攻擊時間（毫秒）
cooldown = 300        # 冷卻時間（300 毫秒 = 0.3 秒）
max_health = 2000
health = 2000
attack_power = 100
player_x = 100
player_y = main_test_cindy_oh.HEIGHT - 280
# 載入角色圖片
player_img = pygame.image.load("assets/player.png")
player_img = pygame.transform.scale(player_img, (250, 250))
player_rect = player_img.get_rect(topleft=(player_x, player_y))


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
        
def player_attack(player_x, player_y, projectiles):
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

        if (monster_test_cindy_oh.chapter == 1): 
            if projectile_rect.colliderect(monster_test_cindy_oh.monster1.rect):
                monster_test_cindy_oh.monster1.health -= attack_power
                print(f"{monster_test_cindy_oh.monster1.health} monster1目前血量")
                projectile.remove(projectile)
            elif projectile.is_off_screen(projectile, main_test_cindy_oh.WIDTH):
                projectiles.remove(projectile)
        
        if (monster_test_cindy_oh.chapter == 2): 
            if projectile_rect.colliderect(monster_test_cindy_oh.monster2.rect):
                monster_test_cindy_oh.monster2.health -= attack_power
                print(f"{monster_test_cindy_oh.monster2.health} monster1目前血量")
                projectile.remove(projectile)
            elif projectile.is_off_screen(projectile, main_test_cindy_oh.WIDTH):
                projectiles.remove(projectile)
        
        #if projectile.is_off_screen(1500) or projectile_rect.colliderect(monster_rect):
        #    projectiles.remove(projectile)
        #else:
        #    projectile.draw(screen)
