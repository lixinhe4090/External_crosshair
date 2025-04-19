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

# 设置字体支持中文，字号改小，并加粗
font = pygame.font.SysFont("SimHei", 24, bold=True)  # 使用黑体字体，字号为24，加粗

# 准星样式函数
def shotgun_crosshair(screen, center, color, size):
    pygame.draw.circle(screen, color, center, int(size * 30), int(size * 2))
    pygame.draw.circle(screen, color, center, int(size * 2), 0)

def smg_rifle_sniper_crosshair(screen, center, color, size):
    pygame.draw.line(screen, color, (center[0] - int(size * 50), center[1]), (center[0] + int(size * 50), center[1]), int(size * 2))
    pygame.draw.line(screen, color, (center[0], center[1] - int(size * 50)), (center[0], center[1] + int(size * 50)), int(size * 2))

def rpg_crosshair(screen, center, color, size):
    radius = int(size * 30)
    pygame.draw.circle(screen, color, center, radius, int(size * 2))
    pygame.draw.line(screen, color, (center[0] - radius, center[1]), (center[0] + radius, center[1]), int(size * 2))
    pygame.draw.line(screen, color, (center[0], center[1] - radius), (center[0], center[1] + radius), int(size * 2))

def vehicle_crosshair(screen, center, color, size):
    rect_size = int(size * 30)
    pygame.draw.rect(screen, color, (center[0] - rect_size, center[1] - rect_size, rect_size * 2, rect_size * 2), int(size * 2))
    pygame.draw.line(screen, color, (center[0] - int(size * 50), center[1]), (center[0] + int(size * 50), center[1]), int(size * 2))
    pygame.draw.line(screen, color, (center[0], center[1] - int(size * 50)), (center[0], center[1] + int(size * 50)), int(size * 2))

def custom_crosshair(screen, center, color, size):
    line_length = int(size * 30)
    gap = int(size * 10)
    line_width = int(size * 2)
    dot_radius = int(size * 2)
    pygame.draw.line(screen, color, (center[0] - line_length, center[1]), (center[0] - gap, center[1]), line_width)
    pygame.draw.line(screen, color, (center[0] + gap, center[1]), (center[0] + line_length, center[1]), line_width)
    pygame.draw.line(screen, color, (center[0], center[1] - line_length), (center[0], center[1] - gap), line_width)
    pygame.draw.line(screen, color, (center[0], center[1] + gap), (center[0], center[1] + line_length), line_width)
    pygame.draw.circle(screen, color, center, dot_radius, 0)

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

# 切换颜色
current_color_index = 0
colors = [(255, 0, 0), (51, 255, 51), (51, 153, 255)]  # 红、绿、蓝

# 调整大小
current_size = 1.0  # 初始大小为1.0（原始大小）
min_size = 1.0  # 最小大小为原始大小
size_step = 0.1  # 每次调整的步长

# 准星位置
crosshair_position = [screen_width // 2, screen_height // 2]  # 初始位置为屏幕中心
calibration_mode = False  # 校准模式
show_text = True  # 是否显示文字提示

# 绘制带边框的文字
def draw_text_with_border(surface, text, position, font, border_color, text_color, border_size=2):
    # 绘制边框
    border_text = font.render(text, True, border_color)
    surface.blit(border_text, (position[0] - border_size, position[1] - border_size))
    surface.blit(border_text, (position[0] + border_size, position[1] - border_size))
    surface.blit(border_text, (position[0] - border_size, position[1] + border_size))
    surface.blit(border_text, (position[0] + border_size, position[1] + border_size))
    # 绘制文字
    text_surface = font.render(text, True, text_color)
    surface.blit(text_surface, position)

# 切换准星
def switch_crosshair(event):
    global current_index
    if event.name == "page up":  # Page Up
        current_index = (current_index - 1) % len(crosshair_keys)
    elif event.name == "page down":  # Page Down
        current_index = (current_index + 1) % len(crosshair_keys)

# 切换颜色
def switch_color(event):
    global current_color_index
    if event.name == "f1":  # F1
        current_color_index = 0
    elif event.name == "f2":  # F2
        current_color_index = 1
    elif event.name == "f3":  # F3
        current_color_index = 2

# 调整大小
def adjust_size_up(event):
    global current_size
    if event.name == "f4":  # F4
        current_size += size_step

def adjust_size_down(event):
    global current_size
    if event.name == "f5":  # F5
        current_size = max(current_size - size_step, min_size)  # 确保不会小于最小大小

# 进入/退出校准模式
def enter_calibration_mode(event):
    global calibration_mode
    if event.name == "f6":  # F6
        calibration_mode = not calibration_mode

# 调整准星位置
def adjust_crosshair_position(event):
    global crosshair_position
    if calibration_mode:
        if event.name == "up":
            crosshair_position[1] -= 5
        elif event.name == "down":
            crosshair_position[1] += 5
        elif event.name == "left":
            crosshair_position[0] -= 5
        elif event.name == "right":
            crosshair_position[0] += 5

# 恢复默认设置
def reset_to_default(event):
    global current_size, current_color_index, crosshair_position, calibration_mode
    if event.name == "f7":  # F7
        current_size = 1.0  # 恢复默认大小
        current_color_index = 0  # 恢复默认颜色（红色）
        crosshair_position = [screen_width // 2, screen_height // 2]  # 恢复默认位置（屏幕中心）
        calibration_mode = False  # 退出校准模式

# 隐藏/显示文字提示
def toggle_text(event):
    global show_text
    if event.name == "f8":  # F8
        show_text = not show_text

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
keyboard.add_hotkey('f1', switch_color, args=[keyboard.KeyboardEvent('down', 0, 'f1')])
keyboard.add_hotkey('f2', switch_color, args=[keyboard.KeyboardEvent('down', 0, 'f2')])
keyboard.add_hotkey('f3', switch_color, args=[keyboard.KeyboardEvent('down', 0, 'f3')])
keyboard.add_hotkey('f4', adjust_size_up, args=[keyboard.KeyboardEvent('down', 0, 'f4')])
keyboard.add_hotkey('f5', adjust_size_down, args=[keyboard.KeyboardEvent('down', 0, 'f5')])
keyboard.add_hotkey('f6', enter_calibration_mode, args=[keyboard.KeyboardEvent('down', 0, 'f6')])
keyboard.add_hotkey('f7', reset_to_default, args=[keyboard.KeyboardEvent('down', 0, 'f7')])
keyboard.add_hotkey('f8', toggle_text, args=[keyboard.KeyboardEvent('down', 0, 'f8')])
keyboard.add_hotkey('up', adjust_crosshair_position, args=[keyboard.KeyboardEvent('down', 0, 'up')])
keyboard.add_hotkey('down', adjust_crosshair_position, args=[keyboard.KeyboardEvent('down', 0, 'down')])
keyboard.add_hotkey('left', adjust_crosshair_position, args=[keyboard.KeyboardEvent('down', 0, 'left')])
keyboard.add_hotkey('right', adjust_crosshair_position, args=[keyboard.KeyboardEvent('down', 0, 'right')])
keyboard.add_hotkey('ctrl+c', exit_program)

# 主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))  # 设置背景为黑色（透明色）
    center = tuple(crosshair_position)  # 使用校准后的准星位置
    crosshairs[crosshair_keys[current_index]](screen, center, colors[current_color_index], current_size)  # 绘制当前准星

    # 显示热键提示
    if show_text:
        hotkey_text = "Page Up/Down: 切换准星 | F1/F2/F3: 切换颜色 | F4/F5: 调整大小 | F6: 校准 | F7: 恢复初始 | F8: 隐藏/显示提示 | Ctrl+C: 退出"
        draw_text_with_border(screen, hotkey_text, (10, 10), font, (0, 0, 0), (255, 255, 255))
        if calibration_mode:
            calibration_text = "使用上下左右箭头键调整准星位置，F6退出"
            draw_text_with_border(screen, calibration_text, (10, 40), font, (0, 0, 0), (255, 255, 255))

    pygame.display.flip()
