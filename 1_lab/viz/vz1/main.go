package main

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"

	"gonum.org/v1/plot"
	"gonum.org/v1/plot/plotter"
	"gonum.org/v1/plot/vg"
)

func main() {
	// Открытие файла с результатами
	file, err := os.Open("rossler_comparison.txt")
	if err != nil {
		fmt.Println("Ошибка открытия файла:", err)
		return
	}
	defer file.Close()

	// Считывание данных из файла
	var times, xRK4, yRK4, zRK4, xDopri5, yDopri5, zDopri5, diffNorm []float64
	scanner := bufio.NewScanner(file)

	// Пропуск заголовка
	scanner.Scan()

	// Чтение данных из файла
	for scanner.Scan() {
		line := scanner.Text()
		values := strings.Fields(line)

		// Преобразование строки в числа
		t, _ := strconv.ParseFloat(values[0], 64)
		xr, _ := strconv.ParseFloat(values[1], 64)
		yr, _ := strconv.ParseFloat(values[2], 64)
		zr, _ := strconv.ParseFloat(values[3], 64)
		xd, _ := strconv.ParseFloat(values[4], 64)
		yd, _ := strconv.ParseFloat(values[5], 64)
		zd, _ := strconv.ParseFloat(values[6], 64)
		diff, _ := strconv.ParseFloat(values[7], 64)

		// Добавление данных в слайсы
		times = append(times, t)
		xRK4 = append(xRK4, xr)
		yRK4 = append(yRK4, yr)
		zRK4 = append(zRK4, zr)
		xDopri5 = append(xDopri5, xd)
		yDopri5 = append(yDopri5, yd)
		zDopri5 = append(zDopri5, zd)
		diffNorm = append(diffNorm, diff)
	}

	// Создание графика
	p := plot.New()

	p.Title.Text = "Сравнение решений для системы Рёсслера"
	p.X.Label.Text = "Время (t)"
	p.Y.Label.Text = "Значения"

	// Создание линии для x-RK4
	lineRK4, err := plotter.NewLine(plotter.XYs{})
	if err != nil {
		fmt.Println("Ошибка при создании линии x-RK4:", err)
		return
	}
	for i := 0; i < len(times); i++ {
		lineRK4.XYs = append(lineRK4.XYs, plotter.XY{X: times[i], Y: xRK4[i]})
	}

	// Создание линии для y-RK4
	lineRK4y, err := plotter.NewLine(plotter.XYs{})
	if err != nil {
		fmt.Println("Ошибка при создании линии y-RK4:", err)
		return
	}
	for i := 0; i < len(times); i++ {
		lineRK4y.XYs = append(lineRK4y.XYs, plotter.XY{X: times[i], Y: yRK4[i]})
	}

	// Создание линии для z-RK4
	lineRK4z, err := plotter.NewLine(plotter.XYs{})
	if err != nil {
		fmt.Println("Ошибка при создании линии z-RK4:", err)
		return
	}
	for i := 0; i < len(times); i++ {
		lineRK4z.XYs = append(lineRK4z.XYs, plotter.XY{X: times[i], Y: zRK4[i]})
	}

	// Создание линии для x-Dopri5
	lineDopri5, err := plotter.NewLine(plotter.XYs{})
	if err != nil {
		fmt.Println("Ошибка при создании линии x-Dopri5:", err)
		return
	}
	for i := 0; i < len(times); i++ {
		lineDopri5.XYs = append(lineDopri5.XYs, plotter.XY{X: times[i], Y: xDopri5[i]})
	}

	// Создание линии для y-Dopri5
	lineDopri5y, err := plotter.NewLine(plotter.XYs{})
	if err != nil {
		fmt.Println("Ошибка при создании линии y-Dopri5:", err)
		return
	}
	for i := 0; i < len(times); i++ {
		lineDopri5y.XYs = append(lineDopri5y.XYs, plotter.XY{X: times[i], Y: yDopri5[i]})
	}

	// Создание линии для z-Dopri5
	lineDopri5z, err := plotter.NewLine(plotter.XYs{})
	if err != nil {
		fmt.Println("Ошибка при создании линии z-Dopri5:", err)
		return
	}
	for i := 0; i < len(times); i++ {
		lineDopri5z.XYs = append(lineDopri5z.XYs, plotter.XY{X: times[i], Y: zDopri5[i]})
	}

	// Добавление линий на график
	p.Add(lineRK4, lineRK4y, lineRK4z, lineDopri5, lineDopri5y, lineDopri5z)

	// Сохранение графика в файл
	if err := p.Save(8*vg.Inch, 6*vg.Inch, "rossler_comparison_plot.png"); err != nil {
		fmt.Println("Ошибка сохранения графика:", err)
		return
	}

	fmt.Println("График успешно сохранен в 'rossler_comparison_plot.png'")
}
