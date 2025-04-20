import pygame
# 顏色
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

def monster(monster_instance, player_instance, screen):
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

            # 播放動畫
            monster_attack_animation(screen, monster_instance, player_instance)

            # 攻擊行為（這裡不扣血，只回傳攻擊資訊）
            attack_message = f"{monster_type} 正在攻擊 {player_instance.name}!"
            # 你可以讓它回傳給 state_display 顯示
            return attack_message
        else:
            return f"don't attack"

    else:
        # 怪物已經死亡，不攻擊
        return f"{monster_type} 已經死亡，無法攻擊。"



def monster_attack_animation(screen, monster_instance, player_instance):
    font = pygame.font.SysFont("Arial", 40)
    attack_text = font.render(f"{monster_instance.name} 攻擊 {player_instance.name}!", True, RED)

    # 畫面閃紅
    for i in range(3):
        screen.fill(RED)
        screen.blit(attack_text, (200, 200))
        pygame.display.flip()
        pygame.time.delay(100)

        screen.fill(BLACK)
        screen.blit(attack_text, (200, 200))
        pygame.display.flip()
        pygame.time.delay(100)


# 主程式
#screen = pygame.display.set_mode((800, 600))  # 這是畫面視窗
#player = Player("玩家A", 100)
#monster1 = Monster("monster1", 50)
# 讓怪物被打一下
#monster1.be_attacked(60)  # hp 現在變 40，符合攻擊條件

#message = monster(monster1, player, screen)
#print(message)

