import pygame
import sys
import keyboard  # 用于监听按键
import win32gui
import win32api
import win32con
import os

# 初始化Pygame
pygame.init()

# 获取屏幕尺寸
screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h

# 创建全屏窗口
screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)
pygame.display.set_caption("Custom Crosshair Overlay")

# 设置窗口透明
hwnd = pygame.display.get_wm_info()['window']
win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT)
win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(0, 0, 0), 0, win32con.LWA_COLORKEY)  # 设置黑色为透明色

# 设置窗口置顶
win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, screen_width, screen_height, 0)

# 准星样式函数
def shotgun_crosshair(screen, center):
    pygame.draw.circle(screen, (255, 0, 0), center, 30, 2)
    pygame.draw.circle(screen, (255, 0, 0), center, 2, 0)

def smg_rifle_sniper_crosshair(screen, center):
    pygame.draw.line(screen, (255, 0, 0), (center[0] - 50, center[1]), (center[0] + 50, center[1]), 2)
    pygame.draw.line(screen, (255, 0, 0), (center[0], center[1] - 50), (center[0], center[1] + 50), 2)

def rpg_crosshair(screen, center):
    radius = 30
    pygame.draw.circle(screen, (255, 0, 0), center, radius, 2)
    pygame.draw.line(screen, (255, 0, 0), (center[0] - radius, center[1]), (center[0] + radius, center[1]), 2)
    pygame.draw.line(screen, (255, 0, 0), (center[0], center[1] - radius), (center[0], center[1] + radius), 2)

def vehicle_crosshair(screen, center):
    size = 30
    pygame.draw.rect(screen, (255, 0, 0), (center[0] - size, center[1] - size, size * 2, size * 2), 2)
    pygame.draw.line(screen, (255, 0, 0), (center[0] - 50, center[1]), (center[0] + 50, center[1]), 2)
    pygame.draw.line(screen, (255, 0, 0), (center[0], center[1] - 50), (center[0], center[1] + 50), 2)

def custom_crosshair(screen, center):
    line_length = 30
    gap = 10
    line_width = 2
    dot_radius = 2
    pygame.draw.line(screen, (255, 0, 0), (center[0] - line_length, center[1]), (center[0] - gap, center[1]), line_width)
    pygame.draw.line(screen, (255, 0, 0), (center[0] + gap, center[1]), (center[0] + line_length, center[1]), line_width)
    pygame.draw.line(screen, (255, 0, 0), (center[0], center[1] - line_length), (center[0], center[1] - gap), line_width)
    pygame.draw.line(screen, (255, 0, 0), (center[0], center[1] + gap), (center[0], center[1] + line_length), line_width)
    pygame.draw.circle(screen, (255, 0, 0), center, dot_radius, 0)

# 准星字典
crosshairs = {
    "Shotgun": shotgun_crosshair,
    "SMG/Rifle/Sniper": smg_rifle_sniper_crosshair,
    "RPG": rpg_crosshair,
    "Vehicle": vehicle_crosshair,
    "Custom": custom_crosshair
}

# 切换准星
current_index = 0
crosshair_keys = list(crosshairs.keys())

def switch_crosshair(event):
    global current_index
    if event.name == "page up":  # Page Up
        current_index = (current_index - 1) % len(crosshair_keys)
    elif event.name == "page down":  # Page Down
        current_index = (current_index + 1) % len(crosshair_keys)

# 退出程序
def exit_program():
    # 方法1：使用 taskkill 强制结束进程
    os.system('taskkill /f /im External_crosshair.exe')
    # 方法2：使用 Pygame 的退出机制
    pygame.quit()
    sys.exit()

# 监听按键
keyboard.add_hotkey('page up', switch_crosshair, args=[keyboard.KeyboardEvent('down', 0, 'page up')])
keyboard.add_hotkey('page down', switch_crosshair, args=[keyboard.KeyboardEvent('down', 0, 'page down')])
keyboard.add_hotkey('ctrl+w', exit_program)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # 设置背景为黑色（透明色）
    center = (screen_width // 2, screen_height // 2)  # 屏幕中心
    crosshairs[crosshair_keys[current_index]](screen, center)  # 绘制当前准星
    pygame.display.flip()
