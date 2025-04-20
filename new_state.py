import pygame

# 顏色設定
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#設定資料類別
class player_and_monster :
    def __init__(self , name , max_hp , attack = 0 , skills = None , boss = False):
        self.name = name
        self.max_hp = max_hp  #初始血量
        self.hp = max_hp      #用來計算剩餘血量
        self.skills = skills or {} #大招
        self.attack = attack  #普攻
        self.boss = boss
        self.alive = True

#設定每個關卡的怪獸數值以及玩家預設血量
def create_monster(level , playername) :
    player = player_and_monster(playername , max_hp = 2000 , skills = {"星光閃耀斬": 300 , "流星聖槍": 200 , "光耀審判": 1000})  
    #玩家預設生命值，姓名自動輸入

    #處裡怪獸
    if level == 1 :
        monster = player_and_monster("暗影使徒(Shadow Disciple)" , max_hp=1500 , attack=100)
        boss = player_and_monster("暗影指揮官(Shadow Commander)" , max_hp=2000 , attack=150)
    elif level == 2 :
        monster = player_and_monster("烈焰魔狼(Flame Wolf)&詛咒妖精(Cursed Sprite)" , max_hp=1500 , attack=200)
        boss = player_and_monster("火焰妖后·瑪爾法(Flame Queen Marfa)" , max_hp=2000 , attack=250 , skills = {"大招": 300} , boss = True)
    elif level == 3 :
        monster = player_and_monster("雷電兵俑(Thunder Sentinel)&風刃劍士(Wind Blade Warrior)" , max_hp=2000 , attack=250)
        boss = player_and_monster("風暴騎士·萊因(Storm Knight Rhine)" , max_hp=3000 , attack=300 , skills = {"大招": 350} , boss = True)
    elif level == 4 :
        boss = player_and_monster("墮落月靈(Fallen Moon Spirit)" , max_hp=4000 , attack=400 , boss = True)
    elif level == 5 :
        monster = player_and_monster("虛無幽靈(Void Phantom)&混沌使徒(Chaos Disciple)" , max_hp=2500 , attack=300)
        boss = player_and_monster("終焉魔神·涅墨西斯(Apocalypse God Nemesis)" , max_hp=8000 , attack=500 , skills = {"大招": 800} , boss = True)
    
    return [player , monster , boss]

#顯示血條並判斷使否死亡
def calculate_update_state(screen , font , player_monster , damage_list , x=50 , y=50 , spacing=60) :
    #"""
    #更新並顯示每個角色的血條與死亡狀態。

    #參數：
    #    screen: pygame 畫布
    #    font: 字型
    #    player_monster: [player, minion, boss]
    #    damage_list: 對應傷害列表（[玩家受傷, 小兵受傷, boss受傷]）
    #    x=50, y=50, spacing=60：這是顯示血條的起始位置和垂直間距，x 和 y 是起始位置，spacing 是每個角色血條之間的間距，默認值分別為 50 和 60。
    #    entities：一個包含所有角色的列表。這些角色可以是玩家（player）、小兵（minion）和 Boss（boss）。每個角色物件應該有 hp（血量）、max_hp（最大血量）、name（名字）和 alive（是否活著）等屬性。
    
    #回傳：
    #    death: 每個角色是否死亡的布林值列表
    #"""
    death = []
    for i  , player_and_monster in enumerate(player_monster) :
        blood_y = y + i * spacing  #計算血條位置

        #算扣血
        damage = damage_list[i]
        player_and_monster.hp -= damage
        if player_and_monster.hp < 0 :
            player_and_monster.hp = 0

        #if_death
        player_and_monster.alive = player_and_monster.hp > 0

        #drawblood
        pygame.draw.rect(screen , RED , (x , blood_y , 100 , 20))

        #算血量比例
        hp_ratio = player_and_monster.hp / player_and_monster.max_hp if player_and_monster.max_hp > 0 else 0
        pygame.draw.rect(screen , GREEN , (x , player_and_monster , int(100 * hp_ratio) , 20))
        #計算當前血量與最大血量的比例 hp_ratio，如果 max_hp 大於 0，則 hp_ratio = entity.hp / entity.max_hp；
        #否則，將比例設為 0（防止除以 0）。接著，根據這個比例繪製顯示血量的綠色矩形，寬度是 100 * hp_ratio

        # 顯示名字 + HP
        name_text = font.render(f"{player_and_monster.name} HP: {player_and_monster.hp}/{player_and_monster.max_hp}" , True , BLACK)
        screen.blit(name_text , (x + 110 , blood_y))
        
        if not player_and_monster.alive :
            dead_text = font.render("DEAD" , True , RED)  #可以省略
            screen.blit(dead_text, (x + 300 , blood_y))
        
        death.append(not player_and_monster.alive)

    return death
            