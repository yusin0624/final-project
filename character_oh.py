import pygame
import random

class DamageImage:
    def __init__(self, x, y, image_path):
        self.x = x
        self.y = y
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (70, 35))  # 可以自己調大小
        self.lifetime = 800  # 存活時間（毫秒）
        self.start_time = pygame.time.get_ticks()

    def update(self):
        # 飄上去
        self.y -= 1

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_expired(self):
        return pygame.time.get_ticks() - self.start_time > self.lifetime


############
## player ##
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
        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.speed = 20
        elif keys[pygame.K_a]:
            self.speed = 5
        else: self.speed = 10
        self.x += self.speed  # 向右移動

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def is_off_screen(self, width):
        return self.x > width  # 如果攻擊物件超過畫面邊緣，返回 True        

class Player:
    def __init__(self, attack_power):
        self.name = "player"
        self.last_attack_time = 0  # 上次攻擊時間（毫秒）
        self.cooldown = 300        # 冷卻時間（300 毫秒 = 0.3 秒）
        self.max_health = 2000
        self.health = 2000
        self.attack_power = attack_power
        self.x = 100
        self.y = 600 - 280 #HEIGHT = 600
        # 載入角色圖片
        self.img = pygame.image.load("assets/player.png")
        self.img = pygame.transform.scale(self.img, (250, 250))
        #self.rect = self.img.get_rect(topleft=(self.x + 200, self.y + 200))
        self.rect = pygame.Rect(self.x - 30, self.y + 30, self.img.get_width() - 60, self.img.get_height() - 60)
        self.damage_images = []

    def player_attack(self, projectiles, screen, current_monster, attack_power):
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
            
            for dmg in self.damage_images[:]:
                dmg.update()
                dmg.draw(screen)
                if dmg.is_expired():
                    self.damage_images.remove(dmg)
                    
            if projectile.rect.colliderect(current_monster.rect):
                current_monster.health -= attack_power
                print(f"{current_monster.health} monster1目前血量")
                projectiles.remove(projectile)
                self.damage_images.append(DamageImage(projectile.x, projectile.y, "assets/player_damage.png"))

            elif projectile.is_off_screen(1500):
                projectiles.remove(projectile)

#############
## monster ##
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
            self.image = pygame.transform.scale(self.image, (300, 300))
            self.bullet_img = pygame.image.load("assets/fireball2.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        elif self.name == "Volley Empress":
            self.image = pygame.image.load("assets/monster3.png")
            self.image = pygame.transform.scale(self.image, (300, 300))
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
        #print(f"[debug] {self} {self.name} HP: {self.health}")
        for bullet in self.bullets[:]:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_d]:
                bullet.x -= 20
            if keys[pygame.K_a]:
                bullet.x -= 5
            else:
                bullet.x -= 10  # 火球向左移動
            if bullet.colliderect(player.rect):
                player.health -= self.attack_power
                print(f"{player.health} 玩家目前血量")
                self.bullets.remove(bullet)
            elif bullet.right < 0:
                self.bullets.remove(bullet)