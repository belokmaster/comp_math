import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

# Загрузка данных
data_rk4 = np.loadtxt('rk4_trajectory.csv', delimiter=',', skiprows=1)
data_dopri5 = np.loadtxt('dopri5_trajectory.csv', delimiter=',', skiprows=1)
data_euler = np.loadtxt('euler_trajectory.csv', delimiter=',', skiprows=1)

# Разделение данных
x_rk4, y_rk4, z_rk4 = data_rk4[:, 0], data_rk4[:, 1], data_rk4[:, 2]
x_dopri5, y_dopri5, z_dopri5 = data_dopri5[:, 0], data_dopri5[:, 1], data_dopri5[:, 2]
x_euler, y_euler, z_euler = data_euler[:, 0], data_euler[:, 1], data_euler[:, 2]

# Настройка ускорения RK4
rk4_speedup = 7  # Ускорение синей точки в 3 раза

# Создание 3D-фигуры
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(min(x_euler.min(), x_rk4.min(), x_dopri5.min()), max(x_euler.max(), x_rk4.max(), x_dopri5.max()))
ax.set_ylim(min(y_euler.min(), y_rk4.min(), y_dopri5.min()), max(y_euler.max(), y_rk4.max(), y_dopri5.max()))
ax.set_zlim(min(z_euler.min(), z_rk4.min(), z_dopri5.min()), max(z_euler.max(), z_rk4.max(), z_dopri5.max()))

# Линии траекторий
line_rk4, = ax.plot([], [], [], 'b-', label='RK4')
line_dopri5, = ax.plot([], [], [], 'r-', label='Dopri5')
line_euler, = ax.plot([], [], [], 'g-', label='Euler')

# Точки, показывающие текущее положение
point_rk4, = ax.plot([], [], [], 'bo', markersize=5)
point_dopri5, = ax.plot([], [], [], 'ro', markersize=5)
point_euler, = ax.plot([], [], [], 'go', markersize=5)

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_title("Анимация траекторий")
ax.legend()

# Функция обновления кадров
def update(num):
    # Ускоренная точка RK4
    rk4_index = min(num * rk4_speedup, len(x_rk4) - 1)
    
    # Линия RK4 теперь обновляется с ускорением
    line_rk4.set_data(x_rk4[:rk4_index], y_rk4[:rk4_index])
    line_rk4.set_3d_properties(z_rk4[:rk4_index])
    
    point_rk4.set_data(x_rk4[rk4_index:rk4_index+1], y_rk4[rk4_index:rk4_index+1])
    point_rk4.set_3d_properties(z_rk4[rk4_index:rk4_index+1])
    
    line_dopri5.set_data(x_dopri5[:num], y_dopri5[:num])
    line_dopri5.set_3d_properties(z_dopri5[:num])
    point_dopri5.set_data(x_dopri5[num:num+1], y_dopri5[num:num+1])
    point_dopri5.set_3d_properties(z_dopri5[num:num+1])
    
    line_euler.set_data(x_euler[:num], y_euler[:num])
    line_euler.set_3d_properties(z_euler[:num])
    point_euler.set_data(x_euler[num:num+1], y_euler[num:num+1])
    point_euler.set_3d_properties(z_euler[num:num+1])

    return line_rk4, point_rk4, line_dopri5, point_dopri5, line_euler, point_euler

# Создание анимации
frames = min(len(x_rk4), len(x_dopri5), len(x_euler))  # Число кадров равно минимальному размеру массива
ani = FuncAnimation(fig, update, frames=frames, interval=30, blit=True)

plt.show()
