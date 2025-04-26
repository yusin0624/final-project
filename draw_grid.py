import pygame

def draw_grid(screen, width, height, grid_size=50):
    """
    在給定的screen上畫出座標網格與標籤。
    :param screen: pygame畫面
    :param width: 畫面寬度
    :param height: 畫面高度
    :param grid_size: 每格的間距（預設50像素）
    """
    # 顏色設定
    GRAY = (200, 200, 200)

    # 畫格子線
    for x in range(0, width, grid_size):
        pygame.draw.line(screen, GRAY, (x, 0), (x, height))
    for y in range(0, height, grid_size):
        pygame.draw.line(screen, GRAY, (0, y), (width, y))