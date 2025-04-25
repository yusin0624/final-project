import pygame
import sys
import random
import math

def willy():
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 800, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont(None, 18)
    time_font = pygame.font.SysFont(None, 28)
    dialog_font_small = pygame.font.SysFont(None, 18)
    dialog_font_big = pygame.font.SysFont(None, 28)
    score_font = pygame.font.SysFont(None, 48)

    # 🔹 背景圖設定
    background_img = pygame.transform.scale(pygame.image.load("find_willy.png"), (WIDTH, HEIGHT))

    # 玩家設定
    player_img = pygame.transform.scale(pygame.image.load("player.png").convert_alpha(), (150, 150))
    player_pos = [100, 100]
    player_speed = 5
    player_rect = player_img.get_rect()
    player_rect.topleft = player_pos
    float_timer = 0

    # 真威力圖片
    willly = pygame.transform.scale(pygame.image.load("willy.png").convert_alpha(), (80, 80))
    willy_rect = willly.get_rect()
    willy_mask = pygame.mask.from_surface(willly)

    # 假威力圖片
    fake_willy = pygame.transform.scale(pygame.image.load("fake_willy.png").convert_alpha(), (120, 120))
    fake_willy_rect = fake_willy.get_rect()
    fake_willy_mask = pygame.mask.from_surface(fake_willy)

    fake_willy_y = random.randint(100, HEIGHT - 150)
    start_on_left = random.choice([True, False])
    if start_on_left:
        fake_willy_rect.topleft = (0, fake_willy_y)
        fake_willy_direction = 1
    else:
        fake_willy_rect.topright = (WIDTH, fake_willy_y)
        fake_willy_direction = -1
    fake_willy_speed = 3
    fake_willy_shift_timer = pygame.time.get_ticks()
    fake_hit_timer = 0  # 加上 cooldown 時間

    dialog_img = pygame.transform.scale(pygame.image.load("dialog.png").convert_alpha(), (150, 90))
    dialog_rect = dialog_img.get_rect()

    voice_intro = pygame.mixer.Sound("catchme.wav")
    voice_ouch = pygame.mixer.Sound("ouch.wav")

    score = 0
    show_begin = True
    said_begin = False
    show_ouch = False
    begin_timer = 0
    ouch_timer = 0
    spawn_time = 0
    goal = 15
    level_timer = 60000
    start_time = pygame.time.get_ticks()
    willy_interval = 2000

    def reset_willy():
        while True:
            willy_rect.center = [
                random.randint(60, WIDTH - 60),
                random.randint(60, HEIGHT - 60)
            ]
            distance = math.hypot(
                willy_rect.centerx - fake_willy_rect.centerx,
                willy_rect.centery - fake_willy_rect.centery
            )
            if distance > 150:
                break

    reset_willy()
    begin_timer = pygame.time.get_ticks()
    spawn_time = pygame.time.get_ticks()

    running = True
    while running:
        # 🔹 畫背景圖
        screen.blit(background_img, (0, 0))
        now = pygame.time.get_ticks()
        float_timer += 0.1
        animation_offset = int(5 * math.sin(float_timer))

        fake_willy_rect.x += fake_willy_direction * fake_willy_speed
        if fake_willy_rect.left <= 0 or fake_willy_rect.right >= WIDTH:
            fake_willy_direction *= -1

        if now - fake_willy_shift_timer > 3000:
            fake_willy_rect.y = random.randint(80, HEIGHT - 150)
            fake_willy_shift_timer = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: player_pos[0] -= player_speed
        if keys[pygame.K_RIGHT]: player_pos[0] += player_speed
        if keys[pygame.K_UP]: player_pos[1] -= player_speed
        if keys[pygame.K_DOWN]: player_pos[1] += player_speed

        player_pos[0] = max(0, min(WIDTH - 150, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - 150, player_pos[1]))
        player_rect.topleft = player_pos
        player_mask = pygame.mask.from_surface(player_img)

        # 假威力碰撞（加 cooldown）
        offset_fake = (fake_willy_rect.left - player_rect.left, fake_willy_rect.top - player_rect.top)
        if player_mask.overlap(fake_willy_mask, offset_fake):
            if now - fake_hit_timer > 1000:
                score = max(0, score - 1)
                fake_hit_timer = now

        # 真威力碰撞
        offset = (willy_rect.left - player_rect.left, willy_rect.top - player_rect.top)
        if player_mask.overlap(willy_mask, offset):
            score += 1
            reset_willy()
            spawn_time = now
            show_ouch = True
            ouch_timer = now
            voice_ouch.play()
            willy_interval = max(600, willy_interval - 100)

        if now - spawn_time > willy_interval:
            reset_willy()
            spawn_time = now
            show_ouch = False

        if score >= goal:
            screen.blit(score_font.render("You Win!", True, (0, 180, 0)), (WIDTH//2 - 100, HEIGHT//2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        if now - start_time > level_timer and score < goal:
            screen.blit(score_font.render("Game Over!", True, (200, 0, 0)), (WIDTH//2 - 120, HEIGHT//2 - 30))
            pygame.display.flip()
            pygame.time.wait(3000)
            pygame.quit()
            sys.exit()

        screen.blit(willly, willy_rect)
        # 光環效果：畫在角色底下
        glow_radius = 70
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 100, 150), (glow_radius, glow_radius), glow_radius)
        glow_pos = (
        player_rect.centerx - glow_radius,
        player_rect.centery - glow_radius + animation_offset  # +動畫浮動補正
        )
        screen.blit(glow_surface, glow_pos)


        fake_float_offset = int(3 * math.sin(float_timer * 1.5))
        screen.blit(fake_willy, (fake_willy_rect.x, fake_willy_rect.y + fake_float_offset))
        screen.blit(player_img, (player_rect.x, player_rect.y + animation_offset))
        time_left = max(0, (level_timer - (now - start_time)) // 1000)
        # 畫白色半透明框（Score）
        score_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        score_bg.fill((255, 255, 255, 200))  # RGBA, 最後一個是透明度
        screen.blit(score_bg, (5, 5))
        screen.blit(score_font.render(f"Score: {score}", True, BLACK), (15, 10))

        # 畫白色半透明框（Time Left）
        time_bg = pygame.Surface((200, 40), pygame.SRCALPHA)
        time_bg.fill((255, 255, 255, 200))
        screen.blit(time_bg, (5, 60))
        screen.blit(time_font.render(f"Time Left: {time_left}s", True, BLACK), (15, 65))



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
