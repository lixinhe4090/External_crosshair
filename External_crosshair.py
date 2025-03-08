import tkinter as tk
import pyautogui

# 初始化屏幕参数
screen_width, screen_height = pyautogui.size()
center_x, center_y = screen_width // 2, screen_height // 2

# 创建透明窗口
window = tk.Tk()
window.overrideredirect(True)
window.attributes("-transparentcolor", "white", "-topmost", True, "-alpha", 0.5)
window.geometry(f"{screen_width}x{screen_height}+0+0")
window.configure(bg="white")

# 创建画布
canvas = tk.Canvas(window, bg="white", highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# 准星样式
def shotgun_crosshair():
    # 霰弹枪：一个圆，分成4段 + 中间一个点
    canvas.create_oval(center_x - 30, center_y - 30, center_x + 30, center_y + 30, outline="red", width=2)
    canvas.create_oval(center_x - 2, center_y - 2, center_x + 2, center_y + 2, fill="red", outline="red")

def smg_rifle_sniper_crosshair():
    # 冲锋枪、步枪、狙击枪：默认的十字准星
    canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=2)
    canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=2)

def rpg_crosshair():
    # RPG：类似于飞机高度表
    radius = 30
    canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline="red", width=2)
    canvas.create_line(center_x - radius, center_y, center_x + radius, center_y, fill="red", width=2)
    canvas.create_line(center_x, center_y - radius, center_x, center_y + radius, fill="red", width=2)

def vehicle_crosshair():
    # 载具：正方形 + 十字准星
    size = 30
    canvas.create_rectangle(center_x - size, center_y - size, center_x + size, center_y + size, outline="red", width=2)
    canvas.create_line(center_x - 50, center_y, center_x + 50, center_y, fill="red", width=2)
    canvas.create_line(center_x, center_y - 50, center_x, center_y + 50, fill="red", width=2)

def custom_crosshair():
    # 自定义准星样式
    line_length = 30
    gap = 10
    line_width = 2
    dot_radius = 2
    canvas.create_line(center_x - line_length, center_y, center_x - gap, center_y, width=line_width, fill="red")
    canvas.create_line(center_x + gap, center_y, center_x + line_length, center_y, width=line_width, fill="red")
    canvas.create_line(center_x, center_y - line_length, center_x, center_y - gap, width=line_width, fill="red")
    canvas.create_line(center_x, center_y + gap, center_x, center_y + line_length, width=line_width, fill="red")
    canvas.create_oval(center_x - dot_radius, center_y - dot_radius, center_x + dot_radius, center_y + dot_radius, fill="red", outline="red")

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
    canvas.delete("all")  # 清除当前准星
    if event.keysym == "Prior":  # Page Up
        current_index = (current_index - 1) % len(crosshair_keys)
    elif event.keysym == "Next":  # Page Down
        current_index = (current_index + 1) % len(crosshair_keys)
    crosshairs[crosshair_keys[current_index]]()  # 绘制新的准星

# 绑定按键事件
window.bind("<Prior>", switch_crosshair)  # Page Up
window.bind("<Next>", switch_crosshair)  # Page Down

# 初始化第一个准星
crosshairs[crosshair_keys[current_index]]()

# 运行主循环
window.mainloop()