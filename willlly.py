import pygame
import sys
import random
import math
def willy_rain(screen, clock):
    # 注意: 這裡 clock 傳進來，不用自己創
    import pygame
    import random

    WIDTH, HEIGHT = screen.get_size()

    willy_img_original = pygame.image.load("assets/willy.png").convert_alpha()
    drop_sound = pygame.mixer.Sound("assets/drop2.wav")

    class Willy:
        def __init__(self):
            scale = random.randint(100, 200)
            self.image = pygame.transform.scale(willy_img_original, (scale, scale))
            self.rect = self.image.get_rect()
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-600, -50)
            self.speed_y = random.uniform(40, 70)
            self.speed_x = random.uniform(-5, 5)
            self.stop_height = random.randint(0, HEIGHT)
            self.landed = False

        def update(self):
            if not self.landed:
                self.rect.x += self.speed_x
                self.rect.y += self.speed_y
                if self.rect.y >= self.stop_height:
                    self.landed = True

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    willies = []
    spawn_timer = 0
    spawn_interval = 30

    start_time = pygame.time.get_ticks()
    end_time = start_time + 3000  # 3秒

    drop_sound.play()


    running = True
    while running:


        dt = clock.tick(60)
        spawn_timer += dt

        now = pygame.time.get_ticks()
        if now > end_time:
            running = False
        if now - start_time >= 2500:
            drop_sound.stop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if spawn_timer > spawn_interval:
            willies.append(Willy())
            spawn_timer = 0

        for willy in willies:
            willy.update()

        screen.fill((255, 255, 255))
        for willy in willies:
            willy.draw(screen)

        pygame.display.flip()


def willy():
    """外部呼叫點：自動重開直到 _willy_game() 回傳 win"""
    while True:
        result = _willy_game()
        if result == "win":
            return "back_to_main"   # 成功後才真正離開
        # 若 result == "lose" 就 continue，自動重開


def _willy_game():
    
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 900, 600
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    willy_rain(screen, clock)
    pygame.mixer.music.stop()
    pygame.mixer.music.load("assets/background.wav")
    pygame.mixer.music.play(loops=-1)
    pygame.mixer.music.set_volume(1.0)

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    font = pygame.font.SysFont(None, 18)
    time_font = pygame.font.SysFont(None, 28)
    dialog_font_small = pygame.font.SysFont(None, 18)
    dialog_font_big = pygame.font.SysFont(None, 28)
    score_font = pygame.font.SysFont(None, 48)

    background_img = pygame.transform.scale(pygame.image.load("assets/find_willy.png"), (WIDTH, HEIGHT))

    player_img = pygame.transform.scale(pygame.image.load("assets/player.png").convert_alpha(), (150, 150))
    player_pos = [100, 100]
    player_speed = 5
    player_rect = player_img.get_rect()
    player_rect.topleft = player_pos
    float_timer = 0

    willly = pygame.transform.scale(pygame.image.load("assets/willy.png").convert_alpha(), (100, 80))
    willy_rect = willly.get_rect()
    willy_mask = pygame.mask.from_surface(willly)

    fake_willy = pygame.transform.scale(pygame.image.load("assets/fake_willy.png").convert_alpha(), (120, 120))
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
    fake_hit_timer = 0

    dialog_img = pygame.transform.scale(pygame.image.load("assets/dialog.png").convert_alpha(), (150, 90))
    dialog_rect = dialog_img.get_rect()

    voice_intro = pygame.mixer.Sound("assets/catchme.wav")
    voice_ouch = pygame.mixer.Sound("assets/ouch.wav")
    voice_ouch.set_volume(1.0)  

    voice_hit_fake = pygame.mixer.Sound("assets/fake.wav")
    voice_hit_fake.set_volume(0.5)


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

    #running = True
    #while running:
    while True:
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
        if keys[pygame.K_a]: player_pos[0] -= player_speed
        if keys[pygame.K_d]: player_pos[0] += player_speed
        if keys[pygame.K_w]: player_pos[1] -= player_speed
        if keys[pygame.K_s]: player_pos[1] += player_speed

        player_pos[0] = max(0, min(WIDTH - 150, player_pos[0]))
        player_pos[1] = max(0, min(HEIGHT - 150, player_pos[1]))
        player_rect.topleft = player_pos
        player_mask = pygame.mask.from_surface(player_img)

        offset_fake = (fake_willy_rect.left - player_rect.left, fake_willy_rect.top - player_rect.top)
        if player_mask.overlap(fake_willy_mask, offset_fake):
            if now - fake_hit_timer > 1000:
                score = max(0, score - 1)
                fake_hit_timer = now
                voice_hit_fake.play()

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
            pygame.mixer.music.fadeout(1500)  #  背景音樂淡出，用1.5秒慢慢消失

            gameclear_img = pygame.image.load("assets/win.jpg")
            gameclear_img = pygame.transform.scale(gameclear_img, (WIDTH, HEIGHT))
            screen.blit(gameclear_img, (0, 0))

            gameclear_sound = pygame.mixer.Sound("assets/win.wav")
            gameclear_sound.play()

            pygame.display.flip()
            pygame.time.wait(3000)
            # pygame.quit()
            # return True
            return "win"



        if now - start_time > level_timer and score < goal:
            pygame.mixer.music.fadeout(1500)  # 背景音樂淡出，用1.5秒慢慢消失

            gameover_img = pygame.image.load("assets/game_over.jpg")
            gameover_img = pygame.transform.scale(gameover_img, (WIDTH, HEIGHT))
            screen.blit(gameover_img, (0, 0))

            gameover_sound = pygame.mixer.Sound("assets/game_over.wav")
            gameover_sound.play()

            pygame.display.flip()
            pygame.time.wait(3000)
            # pygame.quit()
            # return False
            return "lose"


        screen.blit(willly, willy_rect)

        glow_radius = 70
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 100, 150), (glow_radius, glow_radius), glow_radius)
        glow_pos = (
            player_rect.centerx - glow_radius,
            player_rect.centery - glow_radius + animation_offset
        )
        screen.blit(glow_surface, glow_pos)

        fake_float_offset = int(3 * math.sin(float_timer * 1.5))
        screen.blit(fake_willy, (fake_willy_rect.x, fake_willy_rect.y + fake_float_offset))
        screen.blit(player_img, (player_rect.x, player_rect.y + animation_offset))

        time_left = max(0, (level_timer - (now - start_time)) // 1000)

        score_bg = pygame.Surface((200, 50), pygame.SRCALPHA)
        score_bg.fill((255, 255, 255, 200))
        screen.blit(score_bg, (5, 5))
        screen.blit(score_font.render(f"Score: {score}", True, BLACK), (15, 10))

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

        if show_begin and now - begin_timer < 1500:
            if not said_begin:
                voice_intro.play()
                said_begin = True
        else:
            if show_begin:  # 只在第一次從開場轉正常狀態時觸發
                pygame.mixer.music.play(-1)  # 🔥 背景音樂開始循環播放
                show_begin = False

            screen.blit(dialog_img, dialog_pos)
            screen.blit(dialog_font_small.render("Catch me if you can", True, BLACK),
                        (dialog_pos[0] + (dialog_rect.width - dialog_font_small.size("Catch me if you can")[0]) // 2,
                         dialog_pos[1] + 25))
            screen.blit(dialog_font_big.render("hehehe!", True, BLACK),
                        (dialog_pos[0] + (dialog_rect.width - dialog_font_big.size("hehehe!")[0]) // 2,
                         dialog_pos[1] + 40))

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
        
if __name__ == "__main__":
    willy()             # 正式遊戲