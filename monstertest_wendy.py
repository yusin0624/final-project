# monster_test.py

def monster(monster_id, characters):
    """
    由怪獸發動攻擊。
    monster_id: 1 代表小兵，2 代表 boss。
    characters: [player, minion, boss]
    """
    monster_entity = characters[monster_id]
    player = characters[0]

    if monster_entity.alive:
        damage = monster_entity.attack
        player.hp -= damage
        print(f"👾 怪獸 {monster_entity.name} 攻擊 {player.name}，造成 {damage} 點傷害！")

        if player.hp <= 0:
            player.hp = 0
            player.alive = False
            print(f"💀 {player.name} 倒下了...")
