# 遊戲中的狀態
""" 
game_state = {
    "player_hp": 100,
    "monster_list": []
}
"""

def state():
    """顯示目前狀態"""
    print("=== 遊戲狀態 ===")
    print(f"主角 HP：{game_state['player_hp']}")
    print("怪獸們狀態：")
    for m in game_state["monster_list"]:
        print(f"  怪獸 ID: {m['id']}, HP: {m['hp']}")
        # m是monster的名稱
        # f >> formatted string literal(格式化字串), {}內可插入變數
    print("================")

def monster(monster_id):
    """怪獸行為模擬"""
    # 建立怪獸資料，如果不存在的話
    """""
    existing = next((m for m in game_state["monster_list"] if m['id'] == monster_id), None)
    if not existing:
        new_monster = {"id": monster_id, "hp": 30}  # 每隻怪獸初始 30 HP
        game_state["monster_list"].append(new_monster)
        existing = new_monster
        print(f"⚠️ 新怪獸 {monster_id} 出現！")
    """""
    

    # 攻擊主角
    damage = 10
    game_state["player_hp"] -= damage
    print(f"👾 怪獸 {monster_id} 攻擊主角，造成 {damage} 點傷害！")

    # 如果主角血量低於 0，強制歸零
    if game_state["player_hp"] < 0:
        game_state["player_hp"] = 0

    # 如果怪獸自己血量 <= 0，從列表中移除
    if existing["hp"] <= 0:
        print(f"💥 怪獸 {monster_id} 消失了！")
        game_state["monster_list"] = [
            m for m in game_state["monster_list"] if m['id'] != monster_id
        ]

    # 回傳到 state
    state()


    #我只要判斷他有沒有攻擊到人 >> 回傳到state

