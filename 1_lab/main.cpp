#include <iostream>
#include <fstream>
#include <cmath>
#include <array>
#include <vector>

// Определяем тип для вектора состояния (x, y, z)
using state = std::array<double, 3>;

// Параметры системы Рёсслера
const double a = 0.2;
const double b = 0.2;
const double c = 5.7;

// Функция для расчета производных по уравнениям Рёсслера
void rossler_derivatives(const state &s, state &ds) {
    ds[0] = -s[1] - s[2];
    ds[1] = s[0] + a * s[1];
    ds[2] = b + s[2] * (s[0] - c);
}

// Функция для решения системы Рёсслера
void euler(state &s, double dt, double t_max, std::ofstream &outFile) {
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

// Второй метод Рунге-Кутты 3-го порядка (Хойна)
void rk3_heun(state &s, double dt, double t_max, std::ofstream &outFile) {
    double t = 0.0;
    while (t < t_max) {
        outFile << s[0] << "," << s[1] << "," << s[2] << "," << t << "\n";
        state k1, k2, k3, s_temp;

        // k1 = f(s)
        rossler_derivatives(s, k1);
        for (int i = 0; i < 3; i++) k1[i] *= dt;

        // k2 = f(s + k1/3)
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + k1[i] / 3;
        rossler_derivatives(s_temp, k2);
        for (int i = 0; i < 3; i++) k2[i] *= dt;

        // k3 = f(s + 2k2/3)
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + 2 * k2[i] / 3;
        rossler_derivatives(s_temp, k3);
        for (int i = 0; i < 3; i++) k3[i] *= dt;

        // Обновление: s = s + (k1 + 3k3)/4
        for (int i = 0; i < 3; i++) s[i] += (k1[i] + 3 * k3[i]) / 4;

        t += dt;
    }
}

// Метод Рунге-Кутты 4-го порядка
void rk4(state &s, double dt, double t_max, std::ofstream &outFile) {
    double t = 0.0;
    while (t < t_max) {
        // Запись данных в файл для РК4
        outFile << s[0] << "," << s[1] << "," << s[2] << "," << t << "\n";

        // Вычисление производных для метода РК4
        state k1, k2, k3, k4, s_temp;

        rossler_derivatives(s, k1);  // k1 = f(s)
        for (int i = 0; i < 3; i++) k1[i] *= dt;

        // k2 = f(s + k1/2)
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + k1[i] / 2;
        rossler_derivatives(s_temp, k2);
        for (int i = 0; i < 3; i++) k2[i] *= dt;

        // k3 = f(s + k2/2)
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + k2[i] / 2;
        rossler_derivatives(s_temp, k3);
        for (int i = 0; i < 3; i++) k3[i] *= dt;

        // k4 = f(s + k3)
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + k3[i];
        rossler_derivatives(s_temp, k4);
        for (int i = 0; i < 3; i++) k4[i] *= dt;

        // Обновление значений переменных
        for (int i = 0; i < 3; i++) s[i] += (k1[i] + 2 * k2[i] + 2 * k3[i] + k4[i]) / 6;

        // Увеличение времени
        t += dt;
    }
}

// Метод Допри-5
void dopri5(state &s, double dt, double t_max, std::ofstream &outFile) {
    double t = 0.0;
    while (t < t_max) {
        // Запись данных в файл для Допри-5
        outFile << s[0] << "," << s[1] << "," << s[2] << "," << t << "\n";

        // Здесь должен быть код метода Допри-5 (для примера используется стандартная схема)
        state k1, k2, k3, k4, k5, k6, k7, s_temp;

        // Шаг 1
        rossler_derivatives(s, k1);
        for (int i = 0; i < 3; i++) k1[i] *= dt;

        // Шаг 2
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + k1[i] / 5.0;
        rossler_derivatives(s_temp, k2);
        for (int i = 0; i < 3; i++) k2[i] *= dt;

        // Шаг 3
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + (3.0/40.0) * k1[i] + (9.0/40.0) * k2[i];
        rossler_derivatives(s_temp, k3);
        for (int i = 0; i < 3; i++) k3[i] *= dt;

        // Шаг 4
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + (44.0/45.0) * k1[i] - (56.0/15.0) * k2[i] + (32.0/9.0) * k3[i];
        rossler_derivatives(s_temp, k4);
        for (int i = 0; i < 3; i++) k4[i] *= dt;

        // Шаг 5
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + (19372.0/6561.0) * k1[i] - (25360.0/2187.0) * k2[i] + (64448.0/6561.0) * k3[i] - (212.0/729.0) * k4[i];
        rossler_derivatives(s_temp, k5);
        for (int i = 0; i < 3; i++) k5[i] *= dt;

        // Шаг 6
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + (9017.0/3168.0) * k1[i] - (355.0/33.0) * k2[i] + (46732.0/5247.0) * k3[i] + (49.0/176.0) * k4[i] - (5103.0/18656.0) * k5[i];
        rossler_derivatives(s_temp, k6);
        for (int i = 0; i < 3; i++) k6[i] *= dt;

        // Шаг 7
        for (int i = 0; i < 3; i++) s_temp[i] = s[i] + (35.0/384.0) * k1[i] + (500.0/1113.0) * k3[i] + (125.0/192.0) * k4[i] - (2187.0/6784.0) * k5[i] + (11.0/84.0) * k6[i];
        rossler_derivatives(s_temp, k7);
        for (int i = 0; i < 3; i++) k7[i] *= dt;

        // Обновление состояния
        for (int i = 0; i < 3; i++) s[i] += (35.0/384.0) * k1[i] + (500.0/1113.0) * k3[i] + (125.0/192.0) * k4[i] - (2187.0/6784.0) * k5[i] + (11.0/84.0) * k6[i];

        // Увеличение времени
        t += dt;
    }
}

int main() {
    // Начальные условия
    state s = {1, 1, 1};
    double dt = 0.001;  // Шаг по времени
    double t_max = 300.0;  // Максимальное время

    // Открытие файла для записи данных Допри-5
    std::ofstream outFileDopri5("dopri5_trajectory.csv");
    outFileDopri5 << "x,y,z,t\n"; // Заголовки столбцов для CSV

    // Решение системы Рёсслера методом Допри-5
    dopri5(s, dt, t_max, outFileDopri5);

    s = {1, 1, 1};
    // Открытие файла для записи данных РК4
    std::ofstream outFileRK4("rk4_trajectory.csv");
    outFileRK4 << "x,y,z,t\n"; // Заголовки столбцов для CSV

    // Решение системы Рёсслера методом РК4 для одной траектории
    rk4(s, dt, t_max, outFileRK4);

    s = {1, 1, 1};
    // Открытие файла для записи данных Хойна 3 порядка
    std::ofstream outFileRK3Heun("rk3_heun_trajectory.csv");
    outFileRK3Heun << "x,y,z,t\n";

    // Решение системы Рёсслера методом Хойна
    rk3_heun(s, dt, t_max, outFileRK3Heun);

    s = {1, 1, 1};
    // Открытие файла для записи данных Эйлера
    std::ofstream outFileEuler("euler_trajectory.csv");
    outFileEuler << "x,y,z,t\n"; // Заголовки столбцов для CSV

    // Решение системы Рёсслера методом Эйлера
    euler(s, dt, t_max, outFileEuler);

    // Закрытие файлов
    outFileEuler.close();
    outFileRK4.close();
    outFileRK3Heun.close();
    outFileDopri5.close();

    std::cout << "Данные сохранены в файлы rk4_trajectory.csv и dopri5_trajectory.csv и euler_trajectory.csv и rk3_heun_trajectory.csv\n";
    return 0;
}
