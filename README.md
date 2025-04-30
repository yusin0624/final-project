# final-project

[很厲害的google doc](https://docs.google.com/document/d/1KWhExE8u1lSftSq_JfSb_DvZU3WkM36czSTOOgYftfw/edit?usp=sharing)

main_test.py是我怕直接改在main.py會炸掉，不知道怎麼改回去，你們也可以用test試ㄏㄏ

0420
現在最厲害的版本是main_test_wow，但他自己跑一跑會報錯關掉
main_test_cindy沒有狀態列，但player跟monster都會乖乖射子彈了
血條顯示我都寫好了，自己複製去各自的檔案，我有分玩家、魔王、小兵的，差在y的值

0426
在寫transition，沒transition的話可以正常對打、顯示血量、換下一關
todo: 找好全部的monster圖片
      transition寫好

0427
要加上進度條，在transition呼叫時順便顯示進度條的變化
我想要試試看可不可以把攻擊招式增加，會再開一個新檔案試寫
我寫了角色hp ＝ 0 會退出遊戲

0430
1. willy  bullet寫好了
2. 測試，排列組合一下每個功能都要試到
   - 被monster1～9打到（傷害數字）
   - 打到monster1～9（傷害數字、聲音）
   - 死在monster1～9（gameover畫面、enter回start page）
   - victory（同上）
   - 重開之後音樂
   - battle/transition階段，從willy回來
   
   試完V
     monster  | hit player | being attack | gameover |
   - monster1 |      V     |      V       |     V    |
   - monster2 |      X     |      X       |     X    |
   - monster3 |      X     |      X       |     X    |
   - monster4 |      X     |      X       |     X    |
   - monster5 |      X     |      X       |     X    |
   - monster6 |      X     |      X       |     X    |
   - monster7 |      X     |      X       |     X    |
   - monster8 |      X     |      X       |     X    |
   - monster9 |      X     |      X       |     X    |

   victory | X |

   bgm
   | in game | back from willy | gameover restart | victory restart |
   |    X    |        X        |         X        |        X        |

   從willy回來
   battle     | X |
   transition | X |

3. bug
      - transition雲會在state上面

4. todo
   - check老師的google doc (basic/advanced part)，可能現在做不完錄完影片做
   - willy只能玩一次？多玩幾次機率up？
   - player rect改成圓形
   - sort：打怪獸用的時間or打怪獸用的子彈or總通關時間
