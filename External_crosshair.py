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

# 更新准星显示
def update_crosshair_display():
    screen.fill((0, 0, 0))  # 设置背景为黑色（透明色）
    center = tuple(crosshair_position)  # 使用校准后的准星位置
    crosshairs[crosshair_keys[current_index]](screen, center, colors[current_color_index], current_size)  # 绘制当前准星
    
    if show_text:
        hotkey_text = "Page Up/Down: 切换准星 | F1/F2/F3: 切换颜色 | F4/F5: 调整大小 | F6: 校准 | F7: 恢复初始 | F8: 隐藏/显示提示 | Ctrl+C: 退出"
        draw_text_with_border(screen, hotkey_text, (10, 10), font, (0, 0, 0), (255, 255, 255))
        if calibration_mode:
            calibration_text = "使用上下左右箭头键调整准星位置，F6退出"
            draw_text_with_border(screen, calibration_text, (10, 40), font, (0, 0, 0), (255, 255, 255))
    
    pygame.display.flip()  # 刷新屏幕

# 切换准星
def switch_crosshair():
    global current_index
    current_index = (current_index + 1) % len(crosshair_keys)
    update_crosshair_display()  # 更新显示

# 切换颜色
def switch_color():
    global current_color_index
    current_color_index = (current_color_index + 1) % len(colors)
    update_crosshair_display()  # 更新显示

# 调整大小
def adjust_size_up():
    global current_size
    current_size += size_step
    update_crosshair_display()  # 更新显示

def adjust_size_down():
    global current_size
    current_size = max(current_size - size_step, min_size)  # 确保不会小于最小大小
    update_crosshair_display()  # 更新显示

# 进入/退出校准模式
def enter_calibration_mode():
    global calibration_mode
    calibration_mode = not calibration_mode
    update_crosshair_display()  # 更新显示

# 调整准星位置
def move_up():
    global crosshair_position
    if calibration_mode:
        crosshair_position[1] -= 5
        update_crosshair_display()  # 更新显示

def move_down():
    global crosshair_position
    if calibration_mode:
        crosshair_position[1] += 5
        update_crosshair_display()  # 更新显示

def move_left():
    global crosshair_position
    if calibration_mode:
        crosshair_position[0] -= 5
        update_crosshair_display()  # 更新显示

def move_right():
    global crosshair_position
    if calibration_mode:
        crosshair_position[0] += 5
        update_crosshair_display()  # 更新显示

# 恢复默认设置
def reset_to_default():
    global current_size, current_color_index, crosshair_position, calibration_mode
    current_size = 1.0  # 恢复默认大小
    current_color_index = 0  # 恢复默认颜色（红色）
    crosshair_position = [screen_width // 2, screen_height // 2]  # 恢复默认位置（屏幕中心）
    calibration_mode = False  # 退出校准模式
    update_crosshair_display()  # 更新显示

# 隐藏/显示文字提示
def toggle_text():
    global show_text
    show_text = not show_text
    update_crosshair_display()  # 更新显示

# 退出程序
def exit_program():
    pygame.quit()
    sys.exit()

# 监听按键
keyboard.add_hotkey('page up', switch_crosshair)
keyboard.add_hotkey('page down', switch_crosshair)
keyboard.add_hotkey('f1', switch_color)
keyboard.add_hotkey('f2', switch_color)
keyboard.add_hotkey('f3', switch_color)
keyboard.add_hotkey('f4', adjust_size_up)
keyboard.add_hotkey('f5', adjust_size_down)
keyboard.add_hotkey('f6', enter_calibration_mode)
keyboard.add_hotkey('f7', reset_to_default)
keyboard.add_hotkey('f8', toggle_text)
keyboard.add_hotkey('up', move_up)
keyboard.add_hotkey('down', move_down)
keyboard.add_hotkey('left', move_left)
keyboard.add_hotkey('right', move_right)
keyboard.add_hotkey('ctrl+c', exit_program)

# 主循环
running = True
clock = pygame.time.Clock()  # 创建计时器

# 初始刷新
update_crosshair_display()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # 降低无操作时的刷新频率
    clock.tick(30)

pygame.quit()
sys.exit()
