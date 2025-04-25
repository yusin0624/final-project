import pygame
import player_test_cindy_oh

class Monster:
    def __init__(self, name, max_health, health, attack_power, position):
        self.name = name
        self.max_health = max_health
        self.health = health
        #self.image = pygame.image.load("assets/monster.png")
        #self.image = pygame.transform.scale(self.image, (200, 200))
        if self.name == "暗影使徒(Shadow Disciple)":
            self.image = pygame.image.load("assets/monster1.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
            self.bullet_img = pygame.image.load("assets/fireball.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        elif self.name == "暗影指揮官(Shadow Commander)":
            self.image = pygame.image.load("assets/monster2.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
            self.bullet_img = pygame.image.load("assets/fireball2.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        elif self.name == "排球姊姊":
            self.image = pygame.image.load("assets/monster3.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
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

    def update_bullets(self, player_rect):
        for bullet in self.bullets[:]:
            bullet.x -= 10  # 火球向左移動
            if bullet.colliderect(player_rect):
                player_test_cindy_oh.health -= self.attack_power
                print(f"{player_test_cindy_oh.health} 玩家目前血量")
                self.bullets.remove(bullet)
            elif bullet.right < 0:
                self.bullets.remove(bullet)
    
monster1 = Monster("暗影使徒(Shadow Disciple)", 1500, 1500, 100, (1000, 400)) 
monster2 = Monster("暗影指揮官(Shadow Commander)", 2000, 2000, 150, (1000, 400)) 
monster3 = Monster("排球姊姊", 3000, 3000, 175, (1000, 400))