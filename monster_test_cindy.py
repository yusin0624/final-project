import pygame
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

        if self.mhp >= 50:
            return f"{self.name} 正在觀察局勢……（血量 > 50,不攻擊）"

        # 冷卻時間：例如每 1.5 秒才能攻擊一次
        current_time = time.time()
        if current_time - self.last_attack_time < 1.5:
            return f"{self.name} 準備中，尚未冷卻完畢"

        self.last_attack_time = current_time

        # 發射火球
        new_fireball = Fireball(screen, self.pos, player_instance.pos)
        fireballs.append(new_fireball)

        return f"{self.name} 發射火球攻擊 {player_instance.name}!"
