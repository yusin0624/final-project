import pygame
# 顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

fireballs = []  # 儲存火球物件

def monster(monster_instance, player_instance, screen, monster_pos, player_pos, fireballs):
    # 判斷是哪個怪物
    if monster_instance.name == "monster1":
        monster_type = "怪獸一號"
    elif monster_instance.name == "monster2":
        monster_type = "怪獸二號"
    else:
        return False

    # 如果怪物還活著
    if monster_instance.malive:
        #當怪物的hp小於50時開始攻擊玩家
        if monster_instance.mhp < 50:

            new_fireball = Fireball(screen, monster_pos, player_pos)
            fireballs.append(new_fireball) # append : 把()中的東西加到list最後面

            return f"{monster_instance.name} 發射火球攻擊 {player_instance.name}!"
        else:
            return f"{monster_instance.name} 正在觀察局勢……（血量 > 50,不攻擊）"
    else:
        return f"{monster_instance.name} 已死亡，無法攻擊。"

# 火球類別
class Fireball:
    def __init__(self, screen, start_pos, target_pos, speed=10):
        self.screen = screen
        self.x, self.y = start_pos
        self.target_x, self.target_y = target_pos
        self.speed = speed
        self.img = pygame.image.load("fireball.png").convert_alpha()
        
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = max(1, (dx**2 + dy**2)**0.5)
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

        # 命中玩家
        # abs 絕對值
        if abs(self.x - self.target_x) < 10 and abs(self.y - self.target_y) < 10:
            self.hit = True
            self.active = False
            return True  # 命中
        return False  # 尚未命中




# 主程式
#screen = pygame.display.set_mode((800, 600))  # 這是畫面視窗
#player = Player("玩家A", 100)
#monster1 = Monster("monster1", 50)
# 讓怪物被打一下
#monster1.be_attacked(60)  # hp 現在變 40，符合攻擊條件

#message = monster(monster1, player, screen)
#print(message)

################################################
# fireballs = []  # 儲存火球物件

# 更新並繪製火球
        for fireball in fireballs[:]:
            if fireball.update():
                if player.alive:
                    player.be_attacked(20)
                fireballs.remove(fireball)
            elif not fireball.active:
                fireballs.remove(fireball)

