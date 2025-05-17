import pygame

class GreenyEffect:
    def __init__(self, image_path, screen_width, screen_height):
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.scale = 50  # 初始縮放尺寸
        self.max_scale = 800  # 最大尺寸
        self.visible = False
        self.attack_count = 0  # 記錄成功命中次數
        self.screen_width = screen_width
        self.screen_height = screen_height

    def register_attack(self):
        """當攻擊命中時被呼叫一次"""
        self.attack_count += 1
        if self.attack_count >= 10:
            self.visible = True

    def update_and_draw(self, screen):
        """畫出綠頭魚並逐漸放大"""
        if self.visible and self.scale < self.max_scale:
            self.scale += 5  # 每幀放大一點
        if self.visible:
            # 縮放圖片
            scaled_img = pygame.transform.scale(self.original_image, (self.scale, self.scale))
            # 放在畫面中央稍微往下的位置
            img_rect = scaled_img.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 80))
            screen.blit(scaled_img, img_rect.topleft)
