#把它變成function用於主程式呼叫
import pygame
import sys
import random

def willy():
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 800,600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    # 顏色與字型
    WHITE = (255, 255, 255)
    BLUE = (0, 100, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont(None, 18)
    time_font = pygame.font.SysFont(None, 28)
    dialog_font_small = pygame.font.SysFont(None, 18)
    dialog_font_big = pygame.font.SysFont(None, 28)
    score_font = pygame.font.SysFont(None, 48)

    # 玩家設定
    player_size = 40
    player_pos = [100, 100]
    player_speed = 5

    # 載入圖片
    willly = pygame.transform.scale(pygame.image.load("assets/willy.png").convert_alpha(), (80, 80))
    willy_rect = willly.get_rect()
    willy_mask = pygame.mask.from_surface(willly)

    fake_willy = pygame.transform.scale(pygame.image.load("assets/fake_willy.png").convert_alpha(), (200, 200))
    fake_willy_rect = fake_willy.get_rect()
    fake_willy_mask = pygame.mask.from_surface(fake_willy)

    dialog_img = pygame.transform.scale(pygame.image.load("assets/dialog.png").convert_alpha(), (150, 90))
    dialog_rect = dialog_img.get_rect()

    # 音效
    voice_intro = pygame.mixer.Sound("assets/catchme.wav")
    voice_ouch = pygame.mixer.Sound("assets/ouch.wav")

    # 狀態變數
    score = 0
    show_begin = True
    said_begin = False
    show_ouch = False
    begin_timer = 0
    ouch_timer = 0
    spawn_time = 0
    fake_willy_timer = 0
    goal = 15
    level_timer = 60000
    start_time = pygame.time.get_ticks()
    willy_interval = 2000

    def reset_willy():
        willy_rect.center = [
            random.randint(60, WIDTH - 60),
            random.randint(60, HEIGHT - 60)
        ]

    def reset_fake_willy():
        while True:
            fake_willy_rect.center = [
                random.randint(60, WIDTH - 60),
                random.randint(60, HEIGHT - 60)
            ]
            if fake_willy_rect.colliderect(willy_rect) == 0:
                break

    reset_willy()
    reset_fake_willy()
    begin_timer = pygame.time.get_ticks()
    spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        screen.fill(WHITE)
        now = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]: player_pos[0] += player_speed
        if keys[pygame.K_UP]: player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]: player_pos[1] += player_speed

        player_pos[0] = max(0, min(WIDTH - player_size, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - player_size, player_pos[1]))

        player_rect = pygame.Rect(*player_pos, player_size, player_size)
        player_surf = pygame.Surface((player_size, player_size), pygame.SRCALPHA)
        pygame.draw.rect(player_surf, BLUE, (0, 0, player_size, player_size))
        player_mask = pygame.mask.from_surface(player_surf)

        offset_fake = (fake_willy_rect.left - player_rect.left, fake_willy_rect.top - player_rect.top)
        if player_mask.overlap(fake_willy_mask, offset_fake):
            score = max(0, score - 1)
            reset_fake_willy()
            fake_willy_timer = now

        offset = (willy_rect.left - player_rect.left, willy_rect.top - player_rect.top)
        if player_mask.overlap(willy_mask, offset):
            score += 1
            reset_willy()
            reset_fake_willy()
            spawn_time = now
            show_ouch = True
            ouch_timer = now
            voice_ouch.play()
            willy_interval = max(600, willy_interval - 100)

        if now - fake_willy_timer > 2000:
            reset_fake_willy()
            fake_willy_timer = now
        if now - spawn_time > willy_interval:
            reset_willy()
            reset_fake_willy()
            spawn_time = now
            show_ouch = False

        if score >= goal:
            screen.fill(WHITE)
            screen.blit(score_font.render("You Win!", True, (0, 180, 0)), (WIDTH//2 - 100, HEIGHT//2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        if now - start_time > level_timer and score < goal:
            screen.fill(WHITE)
            screen.blit(score_font.render("Game Over!", True, (200, 0, 0)), (WIDTH//2 - 120, HEIGHT//2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        screen.blit(willly, willy_rect)
        screen.blit(fake_willy, fake_willy_rect)
        screen.blit(player_surf, player_pos)
        screen.blit(score_font.render(f"Score: {score}", True, BLACK), (10, 10))
        time_left = max(0, (level_timer - (now - start_time)) // 1000)
        screen.blit(time_font.render(f"Time Left: {time_left}s", True, BLACK), (10, 50))

        dialog_pos = (
            willy_rect.centerx - dialog_rect.width // 2 + 5,
            willy_rect.top - dialog_rect.height + 10
        )
        dialog_x = max(0, min(dialog_pos[0], WIDTH - dialog_rect.width))
        dialog_y = max(0, min(dialog_pos[1], HEIGHT - dialog_rect.height))
        dialog_pos = (dialog_x, dialog_y)

        if show_begin and now - begin_timer < 2500:
            if not said_begin:
                voice_intro.play()
                said_begin = True
            screen.blit(dialog_img, dialog_pos)
            screen.blit(dialog_font_small.render("Catch me if you can", True, BLACK),
                        (dialog_pos[0] + (dialog_rect.width - dialog_font_small.size("Catch me if you can")[0]) // 2,
                        dialog_pos[1] + 25))
            screen.blit(dialog_font_big.render("hehehe!", True, BLACK),
                        (dialog_pos[0] + (dialog_rect.width - dialog_font_big.size("hehehe!")[0]) // 2,
                        dialog_pos[1] + 40))
        else:
            show_begin = False

        if show_ouch:
            screen.blit(dialog_img, dialog_pos)
            screen.blit(dialog_font_big.render("OUCH!", True, BLACK),
                        (dialog_pos[0] + (dialog_rect.width - dialog_font_big.size("OUCH!")[0]) // 2,
                        dialog_pos[1] + 25))
            screen.blit(dialog_font_small.render("You got me!", True, BLACK),
                        (dialog_pos[0] + (dialog_rect.width - dialog_font_small.size("You got me!")[0]) // 2,
                        dialog_pos[1] + 43))
            if now - ouch_timer > 1000:
                show_ouch = False

        pygame.display.flip()
        clock.tick(60)
