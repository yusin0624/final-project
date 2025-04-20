"""import pygame
import time

# 顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 火球類別
class Fireball:
    def __init__(self, screen, start_pos, target_pos, speed=10):
        self.screen = screen
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.img = pygame.image.load("fireball.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (30, 30))  # 可調整火球大小

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.dir_x = dx / distance
        self.dir_y = dy / distance

        self.hit = False
        self.active = True

    def update(self):
        if not self.active:
            return False

        # 移動火球
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

        # 畫出火球
        self.screen.blit(self.img, (int(self.x), int(self.y)))

        # 判斷是否命中目標
        if abs(self.x - self.target_x) < 10 and abs(self.y - self.target_y) < 10:
            self.hit = True
            self.active = False
            return True
        return False

class Monster:
    def __init__(self, name, hp, pos):
        self.name = name
        self.hp = hp
        self.img = pygame.image.load("assets/monster.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (150, 150))
        self.rect = self.img.get_rect(topleft=pos)
        
        self.fireball_img = pygame.image.load("assets/fireball.png").convert_alpha()
        self.fireball_img = pygame.transform.scale(self.fireball_img, (20, 20))
        self.fireballs = []

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        # 畫出怪獸的子彈
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet)

    def attack(self):
        # 發射一顆子彈（從怪獸中心發射）
        bullet = pygame.Rect(self.rect.centerx - 10, self.rect.centery, 20, 5)
        self.bullets.append(bullet)

    def update_bullets(self):
        # 子彈往左移動
        for bullet in self.bullets:
            bullet.x -= 10
        # 檢查火球是否碰到玩家
            if fb.colliderect(player_rect):
                self.fireballs.remove(fb)  # 火球與玩家碰撞，移除火球
                print("玩家中火球！")
                continue  # 進行下一個火球的檢查

            # 檢查火球是否超出畫面範圍（左邊邊界）
            if fb.x < -20:
                self.fireballs.remove(fb)  # 火球離開畫面，移除火球
        # 刪除已飛出畫面的子彈
        self.bullets = [b for b in self.bullets if b.x > 0]"""


"""
# 怪物類別
class Monster:
    def __init__(self, name, hp, pos):
        self.name = name
        self.mhp = hp
        self.malive = True
        self.pos = pos  # (x, y)
        #self.img = pygame.image.load("monster.png").convert_alpha()
        self.img = pygame.image.load("assets/monster.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (80, 80))  # 可調整怪物大小
        self.last_attack_time = 0  # 紀錄上次攻擊時間（用於冷卻）

    def draw(self, screen):
        if self.malive:
            screen.blit(self.img, self.pos)

    def be_attacked(self, dmg):
        self.mhp -= dmg
        if self.mhp <= 0:
            self.malive = False

    def try_attack(self, player_instance, fireballs, screen):
        if not self.malive:
            return f"{self.name} 已死亡，無法攻擊。"

        #if self.mhp >= 50:
        #    return f"{self.name} 正在觀察局勢……（血量 > 50,不攻擊）"

        # 冷卻時間：例如每 1.5 秒才能攻擊一次
        current_time = time.time()
        if current_time - self.last_attack_time < 1.5:
            return f"{self.name} 準備中，尚未冷卻完畢"

        self.last_attack_time = current_time

        # 發射火球
        new_fireball = Fireball(screen, self.pos, player_instance.pos)
        fireballs.append(new_fireball)

        return f"{self.name} 發射火球攻擊 {player_instance.name}!"
"""

import pygame
import time

# 顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# 子彈類別
class Bullet:
    def __init__(self, screen, start_pos, target_pos, speed=10):
        self.screen = screen
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.img = pygame.image.load("fireball.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (30, 30))  # 可調整子彈大小

        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = max(1, (dx ** 2 + dy ** 2) ** 0.5)
        self.dir_x = dx / distance
        self.dir_y = dy / distance

        self.hit = False
        self.active = True

    def update(self):
        if not self.active:
            return False

        # 移動子彈
        self.x += self.dir_x * self.speed
        self.y += self.dir_y * self.speed

        # 畫出子彈
        self.screen.blit(self.img, (int(self.x), int(self.y)))

        # 判斷是否命中目標
        if abs(self.x - self.target_x) < 10 and abs(self.y - self.target_y) < 10:
            self.hit = True
            self.active = False
            return True
        return False

class Monster:
    def __init__(self, name, hp, pos):
        self.name = name
        self.hp = hp
        self.img = pygame.image.load("assets/monster.png").convert_alpha()
        self.img = pygame.transform.scale(self.img, (150, 150))
        self.rect = self.img.get_rect(topleft=pos)
        self.fireball_img = pygame.image.load("assets/fireball.png")

        
        self.bullets = []  # 儲存子彈的列表

    """def draw(self, screen):
        screen.blit(self.img, self.rect)
        # 畫出怪獸的子彈
        for bullet in self.bullets:
            pygame.draw.rect(screen, (255, 0, 0), bullet)"""
            
    def draw(self, screen):
        screen.blit(self.img, self.rect)  # 繪製怪物

        # 繪製怪獸的子彈
        for bullet in self.bullets:
            screen.blit(self.fireball_img, bullet)  # 使用 fireball.png 繪製子彈



    def attack(self):
        # 發射一顆子彈（從怪獸中心發射）
        bullet = pygame.Rect(self.rect.centerx - 10, self.rect.centery, 20, 5)
        self.bullets.append(bullet)

    def update_bullets(self, player_rect):
        # 子彈往左移動
        for bullet in self.bullets:
            bullet.x -= 10
        # 檢查子彈是否碰到玩家
            if bullet.colliderect(player_rect):  # 需要定義 player_rect
                self.bullets.remove(bullet)  # 子彈與玩家碰撞，移除子彈
                continue  # 進行下一個子彈的檢查

            # 檢查子彈是否超出畫面範圍（左邊邊界）
            if bullet.x < -20:
                self.bullets.remove(bullet)  # 子彈離開畫面，移除子彈
