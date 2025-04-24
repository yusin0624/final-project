def monster(monster_id, characters):
    """
    怪物攻擊主角，僅印出攻擊訊息（不處理扣血）。
    
    參數：
        monster_id: 1 = 小兵, 2 = boss
        characters: [玩家, 小兵, boss]
    """
    monster_entity = characters[monster_id]
    player = characters[0]

    if monster_entity.alive:
        print(f"👾 怪獸 {monster_entity.name} 攻擊 {player.name}，造成 {monster_entity.attack} 點傷害！")
