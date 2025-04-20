# monster_test.py

def monster(monster_id, characters):
    """
    顯示怪物攻擊訊息（不實際扣血）。
    monster_id: 1 = 小兵，2 = boss
    characters: [player, minion, boss]
    """
    monster_entity = characters[monster_id]
    player = characters[0]

    if monster_entity.alive:
        damage = monster_entity.attack
        print(f"👾 怪獸 {monster_entity.name} 攻擊 {player.name}，造成 {damage} 點傷害！")
