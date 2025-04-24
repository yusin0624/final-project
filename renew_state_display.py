import pygame

# 顏色設定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class player :
    def __init__(self , name , max_hp , attack):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.alive = True
    
    def player_calclulate(self , attack):
        self.hp -= attack
        if self.hp < 0:
            self.hp == 0
            self.alive = False

    def player_draw(self , screen , font , x=50 , y=50 , spacing=60):

        death = []
        for i, entity in enumerate(player_monster):
            blood_y = y + i * spacing

            #✅ 印出目前血量（debug 用）
            print(f"{entity.name} 當前 HP：{entity.hp}")

            # 畫血條
            pygame.draw.rect(screen, RED, (x, blood_y, 100, 20))
            hp_ratio = entity.hp / entity.max_hp if entity.max_hp > 0 else 0
            pygame.draw.rect(screen, GREEN, (x, blood_y, int(100 * hp_ratio), 20))

            # 顯示 HP 數字
            name_text = font.render(f"{entity.name} HP: {entity.hp}/{entity.max_hp}", True, WHITE)
            screen.blit(name_text, (x + 110, blood_y))

            if not entity.alive:
                dead_text = font.render("DEAD", True, RED)
                screen.blit(dead_text, (x + 300, blood_y))

            death.append(not entity.alive)

        return death


#def calculate_update_state(screen, font, player_monster, damage_list, x=50, y=50, spacing=60):
    #death = []
    #for i, entity in enumerate(player_monster):
        #blood_y = y + i * spacing

        # 扣血
        #damage = damage_list[i]
        #entity.hp -= damage
        #if entity.hp < 0:
        #    entity.hp = 0
        #entity.alive = entity.hp > 0

        # ✅ 印出目前血量（debug 用）
        #print(f"{entity.name} 當前 HP：{entity.hp}")

        # 畫血條
        #pygame.draw.rect(screen, RED, (x, blood_y, 100, 20))
        #hp_ratio = entity.hp / entity.max_hp if entity.max_hp > 0 else 0
        #pygame.draw.rect(screen, GREEN, (x, blood_y, int(100 * hp_ratio), 20))

        # 顯示 HP 數字
        #name_text = font.render(f"{entity.name} HP: {entity.hp}/{entity.max_hp}", True, WHITE)
        #screen.blit(name_text, (x + 110, blood_y))

        #if not entity.alive:
        #    dead_text = font.render("DEAD", True, RED)
        #    screen.blit(dead_text, (x + 300, blood_y))

        #death.append(not entity.alive)

    #return death

#def calculate_update_state(screen, font, player_monster, damage_list, x=50, y=50, spacing=60):
    #death = []
    #for i, entity in enumerate(player_monster):
        #blood_y = y + i * spacing

        # ✅ 印出目前血量（debug 用）
        #print(f"{entity.name} 當前 HP：{entity.hp}")

        # 畫血條
        #pygame.draw.rect(screen, RED, (x, blood_y, 100, 20))
        #hp_ratio = entity.hp / entity.max_hp if entity.max_hp > 0 else 0
        #pygame.draw.rect(screen, GREEN, (x, blood_y, int(100 * hp_ratio), 20))

        # 顯示 HP 數字
        #name_text = font.render(f"{entity.name} HP: {entity.hp}/{entity.max_hp}", True, WHITE)
        #screen.blit(name_text, (x + 110, blood_y))

        #if not entity.alive:
        #    dead_text = font.render("DEAD", True, RED)
        #    screen.blit(dead_text, (x + 300, blood_y))

        #death.append(not entity.alive)

    #return death

class monster:
    def __init__(self , name , max_hp , attack):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.attack = attack
        self.alive = True
    def monster_calclulate(self , attack) :
        self.hp -= attack
        if self.hp < 0:
            self.hp == 0
            self.alive = False
    
    def monster_draw():

    