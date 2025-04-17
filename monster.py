import pygame
# 遊戲中的狀態
""" 
game_state = {
    "player_hp": 100,
    "monsters": {
        1: 30,
        2: 20,
        3: 10
    }
}
"""
def monster(monster):
    """
    已存在的怪獸根據 ID 攻擊主角，如果自己血量歸 0 則消失。
    傳送戰鬥結果給 state()。
    """
    m = state_display["monsters"][monster]

    # 攻擊主角判斷他有沒有攻擊到人 >> 回傳到state
    damage = 10
    state_display["player_hp"] -= damage
    print(f"👾 怪獸 {monster} 攻擊主角，造成 {damage} 點傷害！")

    # 如果怪獸血量 <= 0，自動消失
    if monster_hp <= 0:
        print(f"💀 怪獸 {monster} 血量為 0，已從遊戲中消失")
        del state_display["monsters"][monster]

    

    # 回傳給 state
    state_display()


    

