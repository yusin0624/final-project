import pygame

#初始化
pygame.init() 
print = pygame.font.SysFont("Arial" , 20) #字體，字大小

# 顏色設定
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

#存狀態
class Player :
    def __init__(self , name , Max_HP):  #初始化
        self.name = name  #角色名
        self.Max_HP = Max_HP #自行設定最大血量
        self.hp = Max_HP    #初始血量，之後的血量用這個算
        self.alive = True   #判斷是否存活
    def be_attacked(self , attack_data):
        if self.alive :
            self.hp -= attack_data
            if self.hp <= 0 :
                self.hp = 0
                self.alive = False
                return False #傳給主程式說此角色已死亡
class Monster :
    def __init__(self , name , M_HP):
        self.name = name
        self.M_HP = M_HP
        self.mhp = M_HP
        self.malive = True
    def be_attacked(self , attack_data):
        if self.malive :
            self.malive -= attack_data
            if self.mhp <= 0 :
                self.mhp = 0
                self.malive = False
                return False

#顯示血條量
def draw_hp(screen , Player , x , y , width=1500 , height=600) :
    # 外框
    pygame.draw.rect(screen , BLACK , (x - 2 , y - 2 , width + 4 , height + 4))
    # 背景
    pygame.draw.rect(screen, RED, (x , y , width , height))
    # 血量比例
    if Player.hp > 0 : #還沒死
        hp_ratio = Player.hp / Player.Max_HP
        pygame.draw.rect(screen , GREEN , (x , y , width * hp_ratio , height))
    # 名稱與血量數字
    name_text = print.render(f"{Player.name} ({Player.hp} / {Player.max_hp})", True, WHITE)
    screen.blit(name_text , (x , y - 25))

#計算角色狀態
    


        