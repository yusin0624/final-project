import pygame
import random

############
###player###
############

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
        
        self.rect = self.image.get_rect(topleft=(self.x, self.y))


    def move(self):
        self.x += self.speed  # 向右移動

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self, width):
        return self.x > width  # 如果攻擊物件超過畫面邊緣，返回 True        

class Player:
    def __init__(self):
        self.name = "player"
        self.last_attack_time = 0  # 上次攻擊時間（毫秒）
        self.cooldown = 300        # 冷卻時間（300 毫秒 = 0.3 秒）
        self.max_health = 2000
        self.health = 2000
        self.attack_power = 100
        self.x = 100
        self.y = 600 - 280 #HEIGHT = 600
        # 載入角色圖片
        self.img = pygame.image.load("assets/player.png")
        self.img = pygame.transform.scale(self.img, (250, 250))
        self.rect = self.img.get_rect(topleft=(self.x + 200, self.y + 200))
    
    def player_attack(self, projectiles, screen):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and current_time - self.last_attack_time > self.cooldown:
            projectile_type = random.choice(['star', 'moon'])
            new_projectile = Projectile(self.x + 100, self.y + 80, projectile_type)
            projectiles.append(new_projectile)
            self.last_attack_time = current_time

        for projectile in projectiles[:]:
            projectile.move()
            projectile.rect = pygame.Rect(projectile.x, projectile.y, projectile.width, projectile.height)
            projectile.draw(screen)
            
            if projectile.rect.colliderect(monster1.rect):
                monster1.health -= self.attack_power
                print(f"{monster1.health} monster1目前血量")
                projectiles.remove(projectile)
            elif projectile.is_off_screen(1500):
                projectiles.remove(projectile)

    
player = Player()

#############
###monster###
#############

class Monster:
    def __init__(self, name, max_health, health, attack_power, position):
        self.name = name
        self.max_health = max_health
        self.health = health
        #self.image = pygame.image.load("assets/monster.png")
        #self.image = pygame.transform.scale(self.image, (200, 200))
        if self.name == "Shadow Disciple":
            self.image = pygame.image.load("assets/monster1.png")
            self.image = pygame.transform.scale(self.image, (400, 400))
            self.bullet_img = pygame.image.load("assets/fireball.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        elif self.name == "Shadow Commander":
            self.image = pygame.image.load("assets/monster2.png")
            self.image = pygame.transform.scale(self.image, (400, 400))
            self.bullet_img = pygame.image.load("assets/fireball2.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        elif self.name == "Volley Empress":
            self.image = pygame.image.load("assets/monster3.png")
            self.image = pygame.transform.scale(self.image, (400, 400))
            self.bullet_img = pygame.image.load("assets/fireball3.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
            
        self.bullets = []  # 儲存怪物發射的子彈
        #self.bullet_img = pygame.image.load("assets/fireball.png")
        #self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        self.attack_power = attack_power  # 子彈傷害
    
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        for bullet in self.bullets:
            screen.blit(self.bullet_img, bullet)

    def attack(self):
        # 發射火球（從怪物中間靠右的位置）
        bullet_x = self.rect.centerx - 30
        bullet_y = self.rect.centery - 10
        self.bullets.append(pygame.Rect(bullet_x, bullet_y, 60, 60))
    
    def update_bullets(self, player):
        print(f"[debug] {self} {self.name} HP: {self.health}")
        for bullet in self.bullets[:]:
            bullet.x -= 10  # 火球向左移動
            if bullet.colliderect(player.rect):
                player.health -= self.attack_power
                print(f"{player.health} 玩家目前血量")
                self.bullets.remove(bullet)
            elif bullet.right < 0:
                self.bullets.remove(bullet)
    
monster1 = Monster("Shadow Disciple", 1500, 1500, 100, (1000, 200)) 
monster2 = Monster("Shadow Commander", 2000, 2000, 150, (1000, 200)) 
monster3 = Monster("Volley Empress", 3000, 3000, 175, (1000, 200))