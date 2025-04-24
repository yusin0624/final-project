import pygame
import player_test_cindy_oh

class Monster:
    def __init__(self, name, max_health, health, position):
        self.name = name
        self.max_health = max_health
        self.health = health
        #self.image = pygame.image.load("assets/monster.png")
        #self.image = pygame.transform.scale(self.image, (200, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = position
            
        self.bullets = []  # 儲存怪物發射的子彈
        #self.bullet_img = pygame.image.load("assets/fireball.png")
        #self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        self.attack_cooldown = 30  # 發射間隔（幀）
        self.last_attack_time = 0
        self.attack_power = 10  # 子彈傷害
        
        if self.type == 'monster1':
            self.image = pygame.image.load("assets/monster1.png")
            self.image = pygame.transform.scale(self.image, (200, 200))
            self.bullet_img = pygame.image.load("assets/fireball.png")
            self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
        #elif self.type == 'moon':
        #    self.image = pygame.image.load("assets/moon.png")
        #    self.image = pygame.transform.scale(self.image, (60, 60))
        #    self.bullet_img = pygame.image.load("assets/fireball.png")
        #    self.bullet_img = pygame.transform.scale(self.bullet_img, (60, 60))
    
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
                self.health -= self.attack_power
                #print(f"{self.name} 命中玩家！造成 {self.attack_power} 傷害，目前血量剩下 {self.health}。")
                self.bullets.remove(bullet)
                #if self.health <= 0:
                    #print(f"{self.name} 已死亡。")
            elif bullet.right < 0:
                self.bullets.remove(bullet)


