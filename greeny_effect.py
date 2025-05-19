import pygame
import time

class GreenyEffect:
    def __init__(self, image_path, screen_width, screen_height):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.scale = 50
        self.max_scale = 800
        self.visible = False
        self.attack_count = 0
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.show_start_time = None  # ✅ 記錄出現的時間

    def register_attack(self):
        self.attack_count += 1
        if self.attack_count >= 10 and not self.visible:
            self.visible = True
            self.scale = 50  # 每次都從小放大
            self.show_start_time = time.time()  # ✅ 記錄開始時間

    def update_and_draw(self, screen):
        # ✅ 綠頭魚正在顯示中
        if self.visible:
            # 如果超過10秒就關閉並重設
            if time.time() - self.show_start_time > 10:
                self.visible = False
                self.attack_count = 0
                self.show_start_time = None
                return  # 不畫圖了，直接結束

            # 放大動畫
            if self.scale < self.max_scale:
                self.scale += 5
            scaled_img = pygame.transform.scale(self.original_image, (self.scale, self.scale))
            img_rect = scaled_img.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
            screen.blit(scaled_img, img_rect.topleft)
