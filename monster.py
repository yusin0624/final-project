import pygame
# 顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

def monster(monster_instance, player_instance, screen, monster_pos, player_pos):
    # 判斷是哪個怪物
    if monster_instance.name == "monster1":
        monster_type = "怪獸一號"
    elif monster_instance.name == "monster2":
        monster_type = "怪獸二號"
    else:
        monster_type = "未知怪獸"

    # 如果怪物還活著
    if monster_instance.malive:
        #當怪物的hp小於50時開始攻擊玩家
        if monster_instance.mhp < 50:

            # 播放動畫(攻擊玩家)
            hit = fireball_attack_animation(screen, monster_pos, player_pos)
            if hit:
                player_instance.be_attacked(20) #讓玩家扣血
                return f"{monster_instance.name} 發射火球攻擊 {player_instance.name}!"
        else:
            return f"{monster_instance.name} 正在觀察局勢……（血量 > 50,不攻擊）"
    else:
        return f"{monster_instance.name} 已死亡，無法攻擊。"


def fireball_attack_animation(screen, monster_pos, player_pos):
    # 載入火球圖片（圖片尺寸建議小一點，約 32x32）(還沒有圖片)
    fireball_img = pygame.image.load("fireball.png").convert_alpha()

    # 初始位置
    x, y = monster_pos

    # 終點位置
    target_x, target_y = player_pos

    # 移動速度
    speed = 10

    # 計算方向向量
    dx = target_x - x # x距離差
    dy = target_y - y # y距離差

    distance = max(1, (dx**2 + dy**2) ** 0.5)  # 用max防止除以 0
    dir_x = dx / distance
    dir_y = dy / distance

    while True:
        screen.fill(BLACK)  # 清除畫面

        # 更新火球位置
        x += dir_x * speed
        y += dir_y * speed

        # 畫出火球
        screen.blit(fireball_img, (x, y))

        # 顯示畫面
        pygame.display.flip()
        pygame.time.delay(30)

        # 到達目標就結束
        # abs : 絕對值
        if abs(x - target_x) < 10 and abs(y - target_y) < 10:
            return True # 回傳命中


# 主程式
#screen = pygame.display.set_mode((800, 600))  # 這是畫面視窗
#player = Player("玩家A", 100)
#monster1 = Monster("monster1", 50)
# 讓怪物被打一下
#monster1.be_attacked(60)  # hp 現在變 40，符合攻擊條件

#message = monster(monster1, player, screen)
#print(message)

