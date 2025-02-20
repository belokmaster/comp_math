#include <iostream>
#include <fstream>
#include <cmath>
#include <array>

// Определяем тип для вектора состояния (x, y, z)
using state = std::array<double, 3>;

// Параметры системы Рёсслера
const double a = 0.2;
const double b = 0.2;
const double c = 5.7;

// Функция для решения системы Рёсслера
void rossler3(state &s, double dt, double t_max, std::ofstream &outFile) {
    double t = 0.0;
    while (t < t_max) {
        // Запись данных в файл для одной траектории
        outFile << s[0] << "," << s[1] << "," << s[2] << "," << t << "\n";

        // Расчет производных по уравнениям Рёсслера
        double dx = -s[1] - s[2];
        double dy = s[0] + a * s[1];
        double dz = b + s[2] * (s[0] - c);

        // Обновление значений переменных
        s[0] += dx * dt;
        s[1] += dy * dt;
        s[2] += dz * dt;

        // Увеличение времени
        t += dt;
    }
}

int main() {
    // Начальные условия
    state s = {0.1, 0.1, 0.1};
    double dt = 0.01;  // Шаг по времени
    double t_max = 45.0;  // Максимальное время

    // Открытие файла для записи
    std::ofstream outFile("trajectory.csv");
    outFile << "x,y,z,t\n"; // Заголовки столбцов для CSV

    // Решение системы Рёсслера для одной траектории
    rossler3(s, dt, t_max, outFile);

    // Закрытие файла
    outFile.close();
    
    std::cout << "Данные сохранены в trajectory.csv\n";
    return 0;
}
