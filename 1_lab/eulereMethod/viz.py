import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D  # Для 3D графиков

# Загрузка данных из CSV файла
data = np.loadtxt('trajectory.csv', delimiter=',', skiprows=1)

# Разделение данных на x, y, z и t
x = data[:, 0]
y = data[:, 1]
z = data[:, 2]
t = data[:, 3]

# Построение графика x-y
plt.plot(x, y)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Аттрактор Рёсслера. Метод Ньютона: 2D')
# Сохранение графика x-y
plt.savefig('rossler_xy_trajectory.png')

# Построение 3D графика для траектории
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(x, y, z)

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('Аттрактор Рёсслера. Метод Ньютона: 3D')
# Сохранение 3D графика
plt.savefig('rossler_3d_trajectory.png')

# Отображаем графики
plt.show()
