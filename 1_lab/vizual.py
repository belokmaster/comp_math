import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import matplotlib.animation as animation

# Загружаем данные
data_rk4 = np.loadtxt("rk4_trajectory.csv", delimiter=',', skiprows=1)
data_dopri5 = np.loadtxt("dopri5_trajectory.csv", delimiter=',', skiprows=1)
data_euler = np.loadtxt("euler_trajectory.csv", delimiter=',', skiprows=1)
data_rk3_heun = np.loadtxt("rk3_heun_trajectory.csv", delimiter=',', skiprows=1)  # Добавляем данные для RK3 Heun

# Извлекаем данные
x_rk4, y_rk4, z_rk4, t_rk4 = data_rk4[:, 0], data_rk4[:, 1], data_rk4[:, 2], data_rk4[:, 3]
x_dopri5, y_dopri5, z_dopri5, t_dopri5 = data_dopri5[:, 0], data_dopri5[:, 1], data_dopri5[:, 2], data_dopri5[:, 3]
x_euler, y_euler, z_euler, t_euler = data_euler[:, 0], data_euler[:, 1], data_euler[:, 2], data_euler[:, 3]
x_rk3_heun, y_rk3_heun, z_rk3_heun, t_rk3_heun = data_rk3_heun[:, 0], data_rk3_heun[:, 1], data_rk3_heun[:, 2], data_rk3_heun[:, 3]  # Данные для RK3 Heun

# Вычисляем ошибки между методами
error_x_euler_dopri5 = np.abs(x_euler - x_dopri5)  # Ошибка по x между Euler и Dopri5
error_y_euler_dopri5 = np.abs(y_euler - y_dopri5)  # Ошибка по y между Euler и Dopri5
error_z_euler_dopri5 = np.abs(z_euler - z_dopri5)  # Ошибка по z между Euler и Dopri5

error_x_rk3_heun_dopri5 = np.abs(x_rk3_heun - x_dopri5)  # Ошибка по x между RK3 Heun и Dopri5
error_y_rk3_heun_dopri5 = np.abs(y_rk3_heun - y_dopri5)  # Ошибка по y между RK3 Heun и Dopri5
error_z_rk3_heun_dopri5 = np.abs(z_rk3_heun - z_dopri5)  # Ошибка по z между RK3 Heun и Dopri5

error_x_rk4_dopri5 = np.abs(x_rk4 - x_dopri5)  # Ошибка по x между RK4 и Dopri5
error_y_rk4_dopri5 = np.abs(y_rk4 - y_dopri5)  # Ошибка по y между RK4 и Dopri5
error_z_rk4_dopri5 = np.abs(z_rk4 - z_dopri5)  # Ошибка по z между RK4 и Dopri5

# Создаем фигуру
fig = plt.figure(figsize=(18, 12))
plt.subplots_adjust(bottom=0.2)

# Графики фазового пространства
ax1 = fig.add_subplot(2, 4, 1, projection='3d')  # Euler
ax2 = fig.add_subplot(2, 4, 2, projection='3d')  # RK3 Heun
ax3 = fig.add_subplot(2, 4, 3, projection='3d')  # RK4
ax4 = fig.add_subplot(2, 4, 4, projection='3d')  # Dopri5

# Графики ошибок
ax5 = fig.add_subplot(2, 4, 5)  # Ошибка Euler vs Dopri5
ax6 = fig.add_subplot(2, 4, 6)  # Ошибка RK3 Heun vs Dopri5
ax7 = fig.add_subplot(2, 4, 7)  # Ошибка RK4 vs Dopri5

# Настройка фазовых графиков
for ax in (ax1, ax2, ax3, ax4):
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.set_xlim(np.min([x_rk4, x_dopri5, x_euler, x_rk3_heun]) - 0.5, np.max([x_rk4, x_dopri5, x_euler, x_rk3_heun]) + 0.5)
    ax.set_ylim(np.min([y_rk4, y_dopri5, y_euler, y_rk3_heun]) - 0.5, np.max([y_rk4, y_dopri5, y_euler, y_rk3_heun]) + 0.5)
    ax.set_zlim(np.min([z_rk4, z_dopri5, z_euler, z_rk3_heun]) - 0.5, np.max([z_rk4, z_dopri5, z_euler, z_rk3_heun]) + 0.5)

ax1.set_title("Euler")
ax2.set_title("RK3 Heun")
ax3.set_title("RK4")
ax4.set_title("Dopri5")

# Настройка графиков ошибок
ax5.set_xlabel("Time")
ax5.set_ylabel("Error in x")
ax5.set_title("Error in x (Euler vs Dopri5)")
ax5.set_xlim(0, t_rk4[-1])
ax5.set_ylim(0, np.max(error_x_euler_dopri5) + 0.1)

ax6.set_xlabel("Time")
ax6.set_ylabel("Error in x")
ax6.set_title("Error in x (RK3 Heun vs Dopri5)")
ax6.set_xlim(0, t_rk4[-1])
ax6.set_ylim(0, np.max(error_x_rk3_heun_dopri5) + 0.1)

ax7.set_xlabel("Time")
ax7.set_ylabel("Error in x")
ax7.set_title("Error in x (RK4 vs Dopri5)")
ax7.set_xlim(0, t_rk4[-1])
ax7.set_ylim(0, np.max(error_x_rk4_dopri5) + 0.1)

# Графические объекты
line_euler, = ax1.plot([], [], [], 'g-', lw=0.5)  # Euler
line_rk3_heun, = ax2.plot([], [], [], 'c-', lw=0.5)  # RK3 Heun
line_rk4, = ax3.plot([], [], [], 'b-', lw=0.5)  # RK4
line_dopri5, = ax4.plot([], [], [], 'r-', lw=0.5)  # Dopri5

line_error_euler, = ax5.plot([], [], color='gray', label='Error in x (Euler)')
line_error_rk3, = ax6.plot([], [], color='orange', label='Error in x (RK3 Heun)')
line_error_rk4, = ax7.plot([], [], color='purple', label='Error in x (RK4)')

# Текстовые аннотации для ошибок
text_error_euler = ax5.text(0.02, 0.95, '', transform=ax5.transAxes, fontsize=10, color='red')
text_error_rk3 = ax6.text(0.02, 0.95, '', transform=ax6.transAxes, fontsize=10, color='red')
text_error_rk4 = ax7.text(0.02, 0.95, '', transform=ax7.transAxes, fontsize=10, color='red')

ax5.legend()
ax6.legend()
ax7.legend()

# Добавляем виджеты
ax_slider = plt.axes([0.15, 0.05, 0.7, 0.03])
ax_play = plt.axes([0.15, 0.01, 0.1, 0.03])
ax_stop = plt.axes([0.3, 0.01, 0.1, 0.03])

slider = Slider(ax_slider, 'Time', 0, len(t_rk4) - 1, valinit=0, valstep=1)
button_play = Button(ax_play, 'Play')
button_stop = Button(ax_stop, 'Stop')

anim = None
current_frame = 0

# Функция обновления графиков
def update(frame):
    line_euler.set_data(x_euler[:frame], y_euler[:frame])
    line_euler.set_3d_properties(z_euler[:frame])

    line_rk3_heun.set_data(x_rk3_heun[:frame], y_rk3_heun[:frame])
    line_rk3_heun.set_3d_properties(z_rk3_heun[:frame])

    line_rk4.set_data(x_rk4[:frame], y_rk4[:frame])
    line_rk4.set_3d_properties(z_rk4[:frame])

    line_dopri5.set_data(x_dopri5[:frame], y_dopri5[:frame])
    line_dopri5.set_3d_properties(z_dopri5[:frame])

    line_error_euler.set_data(t_euler[:frame], error_x_euler_dopri5[:frame])
    line_error_rk3.set_data(t_rk3_heun[:frame], error_x_rk3_heun_dopri5[:frame])
    line_error_rk4.set_data(t_rk4[:frame], error_x_rk4_dopri5[:frame])

    # Обновляем текстовые аннотации
    text_error_euler.set_text(f"Max Error: {np.max(error_x_euler_dopri5):.4f}\nCurrent Error: {error_x_euler_dopri5[frame]:.4f}")
    text_error_rk3.set_text(f"Max Error: {np.max(error_x_rk3_heun_dopri5):.4f}\nCurrent Error: {error_x_rk3_heun_dopri5[frame]:.4f}")
    text_error_rk4.set_text(f"Max Error: {np.max(error_x_rk4_dopri5):.4f}\nCurrent Error: {error_x_rk4_dopri5[frame]:.4f}")

    fig.canvas.draw_idle()

# Функция для слайдера
def update_slider(val):
    global current_frame
    current_frame = int(val)
    update(current_frame)

# Функция анимации
def animate(frame):
    global current_frame
    current_frame = frame
    update(frame)
    slider.set_val(frame)
    return line_euler, line_rk3_heun, line_rk4, line_dopri5, line_error_euler, line_error_rk3, line_error_rk4

# Функция запуска анимации
def play(event):
    global anim
    if anim is None or anim.event_source is None:
        anim = animation.FuncAnimation(
            fig, animate, frames=range(current_frame, len(t_rk4)), interval=5, blit=False, repeat=True
        )
    fig.canvas.draw_idle()

# Функция остановки анимации
def stop(event):
    global anim
    if anim is not None:
        anim.event_source.stop()
        anim = None
    update(current_frame)

slider.on_changed(update_slider)
button_play.on_clicked(play)
button_stop.on_clicked(stop)

update(0)

plt.show()