import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# 全局变量，用于记录动画是否暂停，按空格可以暂停
paused = False

# 定义信号函数
def signal(x):
    return np.sin(2 * np.pi * x)  # 信号函数为正弦函数


# 定义卷积函数
def convolution(x, h, dt):
    result = np.convolve(x, h, mode='same') * dt  # 对两个信号进行卷积
    return result


# 创建动画函数
def animate(i):
    if not paused:  # 如果动画未暂停，则绘制下一帧
        ax.clear()

        # 生成时间轴
        t = np.linspace(0, 10, 1000)
        dt = t[1] - t[0]

        # 生成信号函数
        x = signal(t)
        h = np.exp(-t) * (t >= 0)  # 定义一个简单的卷积核函数（指数衰减函数）

        # 计算卷积结果
        shift = i * 0.1  # 设置卷积核每帧移动的步长
        h_shifted = np.roll(h, int(shift / dt))  # 将卷积核向右移动
        y = convolution(x, h_shifted, dt)

        # 绘制信号函数和卷积结果
        ax.plot(t, x, label='Signal Function (x)')
        ax.plot(t, h_shifted, label='Convolutional Kernel (h)')
        ax.plot(t, y, label='Convolution Result (x * h)')
        ax.fill_between(t, 0, h_shifted, alpha=0.3, color='gray')  # 用灰色区域表示卷积核的范围
        ax.legend(loc='upper right')


# 定义键盘事件处理函数
def on_key(event):
    global paused
    if event.key == ' ':  # 如果按下空格键，则暂停或恢复动画
        paused = not paused


# 创建画布和子图
fig, ax = plt.subplots(figsize=(10, 6))

# 绑定键盘事件处理函数
fig.canvas.mpl_connect('key_press_event', on_key)

# 创建动画
ani = FuncAnimation(fig, animate, frames=range(100), interval=100)

plt.show()
