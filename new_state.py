import pygame

# 顏色設定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class player_and_monster:
    def __init__(self, name, max_hp, attack=0, skills=None, boss=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.skills = skills or {}
        self.attack = attack
        self.boss = boss
        self.alive = True

def create_character(level, playername):
    player = player_and_monster(playername, 2000, skills={"星光閃耀斬": 300, "流星聖槍": 200, "光耀審判": 1000})
    monster = None

    if level == 1:
        monster = player_and_monster("暗影使徒(Shadow Disciple)", 1500, attack=100)
        boss = player_and_monster("暗影指揮官(Shadow Commander)", 2000, attack=150)
    else:
        monster = player_and_monster("無", 1, attack=0)
        monster.alive = False
        boss = player_and_monster("無", 1, attack=0)
        boss.alive = False

    return [player, monster, boss]

def calculate_update_state(screen, font, player_monster, damage_list, x=50, y=50, spacing=60):
    death = []
    for i, entity in enumerate(player_monster):
        blood_y = y + i * spacing

        # 扣血
        damage = damage_list[i]
        entity.hp -= damage
        if entity.hp < 0:
            entity.hp = 0
        entity.alive = entity.hp > 0

        # ✅ 印出目前血量（debug 用）
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
