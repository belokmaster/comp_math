import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Для 3D графиков
from scipy.interpolate import interp1d  # Для интерполяции

# Загрузка данных из CSV файлов для обоих методов
data_rk4 = np.loadtxt('rk4_trajectory.csv', delimiter=',', skiprows=1)
data_dopri5 = np.loadtxt('dopri5_trajectory.csv', delimiter=',', skiprows=1)
data_euler = np.loadtxt('euler_trajectory.csv', delimiter=',', skiprows=1)
data_houp3 = np.loadtxt('rk3_heun_trajectory.csv', delimiter=',', skiprows=1)

# Разделение данных на x, y, z и t для обоих методов
x_rk4 = data_rk4[:, 0]
y_rk4 = data_rk4[:, 1]
z_rk4 = data_rk4[:, 2]
t_rk4 = data_rk4[:, 3]

x_dopri5 = data_dopri5[:, 0]
y_dopri5 = data_dopri5[:, 1]
z_dopri5 = data_dopri5[:, 2]
t_dopri5 = data_dopri5[:, 3]

x_euler = data_euler[:, 0]
y_euler = data_euler[:, 1]
z_euler = data_euler[:, 2]
t_euler = data_euler[:, 3]

x_houp3 = data_houp3[:, 0]
y_houp3 = data_houp3[:, 1]
z_houp3 = data_houp3[:, 2]
t_houp3 = data_houp3[:, 3]

# Проверка длины данных
print(f"Размеры данных Eulere: {len(x_euler)}, {len(y_euler)}, {len(z_euler)}")
print(f"Размеры данных Houp3: {len(x_houp3)}, {len(y_houp3)}, {len(z_houp3)}")
print(f"Размеры данных RK4: {len(x_rk4)}, {len(y_rk4)}, {len(z_rk4)}")
print(f"Размеры данных Dopri5: {len(x_dopri5)}, {len(y_dopri5)}, {len(z_dopri5)}")

# Построение 2D графиков для x-y
plt.figure(figsize=(20, 5))

# График Euler
plt.subplot(1, 4, 1)
plt.plot(x_euler, y_euler, label='Euler', color='g')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Euler: x-y')
plt.legend()


# График RK4
plt.subplot(1, 4, 3)
plt.plot(x_rk4, y_rk4, label='RK4', color='b')
plt.xlabel('x')
plt.ylabel('y')
plt.title('RK4: x-y')
plt.legend()

# График Dopri5
plt.subplot(1, 4, 4)
plt.plot(x_dopri5, y_dopri5, label='Dopri5', color='r')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Dopri5: x-y')
plt.legend()

# График Houp3
plt.subplot(1, 4, 2)
plt.plot(x_houp3, y_houp3, label='Houp3', color='c')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Dopri5: x-y')
plt.legend()

# Сохранение 2D графиков
plt.tight_layout()
plt.savefig('individual_2d_plots.png', dpi=600)
plt.show()

# Построение наложенных 2D графиков для x-y
plt.figure(figsize=(10, 5))
plt.plot(x_rk4, y_rk4, label='RK4', color='b')
plt.plot(x_dopri5, y_dopri5, label='Dopri5', color='r')
plt.plot(x_euler, y_euler, label='Euler', color='g')
plt.plot(x_houp3, y_houp3, label='Houp3', color='c')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Наложение траекторий x-y')
plt.legend()

# Сохранение наложенного 2D графика
plt.tight_layout()
plt.savefig('overlay_2d_plots.png', dpi=600)
plt.show()

# Построение 3D графиков для траектории
fig = plt.figure(figsize=(20, 5))

# График Euler
ax3 = fig.add_subplot(141, projection='3d')
ax3.plot(x_euler, y_euler, z_euler, label='Euler', color='g')
ax3.set_xlabel('X')
ax3.set_ylabel('Y')
ax3.set_zlabel('Z')
ax3.set_title('Euler: Аттрактор Рёсслера')

# График Houp3
ax4 = fig.add_subplot(142, projection='3d')
ax4.plot(x_houp3, y_houp3, z_houp3, label='Houp3', color='c')
ax4.set_xlabel('X')
ax4.set_ylabel('Y')
ax4.set_zlabel('Z')
ax4.set_title('Houp3: Аттрактор Рёсслера')

# График RK4
ax = fig.add_subplot(143, projection='3d')
ax.plot(x_rk4, y_rk4, z_rk4, label='RK4', color='b')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('RK4: Аттрактор Рёсслера')

# График Dopri5
ax2 = fig.add_subplot(144, projection='3d')
ax2.plot(x_dopri5, y_dopri5, z_dopri5, label='Dopri5', color='r')
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_zlabel('Z')
ax2.set_title('Dopri5: Аттрактор Рёсслера')

# Сохранение общего графика
plt.tight_layout()
plt.savefig('rossler_comparison.png', dpi=600)
plt.show()

# Визуализация ошибки между траекториями по времени для RK4 и Dopri5
plt.figure(figsize=(10, 5))

# Интерполяция данных для RK4 и Dopri5
t_interp = np.linspace(min(t_rk4), max(t_rk4), num=10000)  # Увеличиваем количество точек
error_rk4_dopri5 = np.sqrt((x_rk4 - x_dopri5) ** 2 + (y_rk4 - y_dopri5) ** 2 + (z_rk4 - z_dopri5) ** 2)
interp_error_rk4_dopri5 = interp1d(t_rk4, error_rk4_dopri5, kind='cubic')  # Кубическая интерполяция

# Вычисление средней и глобальной ошибки
mean_error_rk4_dopri5 = np.mean(error_rk4_dopri5)
max_error_rk4_dopri5 = np.max(error_rk4_dopri5)

# Вывод ошибок в консоль
print(f"Средняя ошибка между методами RK4 и Dopri5: {mean_error_rk4_dopri5}")
print(f"Глобальная ошибка между методами RK4 и Dopri5: {max_error_rk4_dopri5}")

# Построение графика с интерполированными данными
plt.plot(t_interp, interp_error_rk4_dopri5(t_interp), label='Ошибка (RK4 vs Dopri5)', color='purple')
plt.xlabel('Время')
plt.ylabel('Ошибка')
plt.title('Ошибка между методами RK4 и Dopri5 по времени')
plt.legend()
plt.tight_layout()
plt.show()

# Визуализация ошибки между траекториями по времени для Houp3 и Dopri5
plt.figure(figsize=(10, 5))

# Интерполяция данных для Houp3 и Dopri5
t_interp = np.linspace(min(t_houp3), max(t_houp3), num=10000)  # Увеличиваем количество точек
error_houp3_dopri5 = np.sqrt((x_houp3 - x_dopri5) ** 2 + (y_houp3 - y_dopri5) ** 2 + (z_houp3 - z_dopri5) ** 2)
interp_error_houp3_dopri5 = interp1d(t_houp3, error_houp3_dopri5, kind='cubic')  # Кубическая интерполяция

# Вычисление средней и глобальной ошибки
mean_error_houp3_dopri5 = np.mean(error_houp3_dopri5)
max_error_houp3_dopri5 = np.max(error_houp3_dopri5)

# Вывод ошибок в консоль
print(f"Средняя ошибка между методами Houp3 и Dopri5: {mean_error_houp3_dopri5}")
print(f"Глобальная ошибка между методами Houp3 и Dopri5: {max_error_houp3_dopri5}")

# Построение графика с интерполированными данными
plt.plot(t_interp, interp_error_houp3_dopri5(t_interp), label='Ошибка (Houp3 vs Dopri5)', color='purple')
plt.xlabel('Время')
plt.ylabel('Ошибка')
plt.title('Ошибка между методами Houp3 и Dopri5 по времени')
plt.legend()
plt.tight_layout()
plt.show()


# взять эталон рк5. с шагом малым.
# сравнить с ним рк4 и метод 3 порядка