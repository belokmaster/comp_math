package main

import (
	"fmt"
	"image/color"
	"math"
	"os"
	"strconv"
	"strings"
	"time"

	"bufio"

	"fyne.io/fyne/v2"
	"fyne.io/fyne/v2/app"
	"fyne.io/fyne/v2/canvas"
	"fyne.io/fyne/v2/container"
	"fyne.io/fyne/v2/widget"
)

// Глобальные переменные
var xData, yData []float64
var speedFactor float64 = 1.0
var running bool = true

func main() {
	// Открываем файл с данными
	file, err := os.Open("rossler_comparison.txt")
	if err != nil {
		fmt.Println("Ошибка открытия файла:", err)
		return
	}
	defer file.Close()

	// Читаем данные
	scanner := bufio.NewScanner(file)
	scanner.Scan() // Пропускаем заголовок

	for scanner.Scan() {
		line := scanner.Text()
		values := strings.Fields(line)

		x, _ := strconv.ParseFloat(values[1], 64)
		y, _ := strconv.ParseFloat(values[2], 64)

		xData = append(xData, x)
		yData = append(yData, y)
	}

	// Создаем GUI приложение
	a := app.New()
	w := a.NewWindow("Rossler Attractor Animation")
	w.Resize(fyne.NewSize(500, 500))

	// Полотно для отрисовки
	circle := canvas.NewCircle(color.RGBA{255, 0, 0, 255}) // Красная точка
	circle.Resize(fyne.NewSize(5, 5))                      // Размер точки

	// Холст для отображения точки
	canvasContainer := container.NewWithoutLayout(circle)

	// Ползунок для изменения скорости
	speedSlider := widget.NewSlider(0.1, 5)
	speedSlider.SetValue(1)
	speedSlider.OnChanged = func(val float64) {
		speedFactor = val
	}

	// Кнопка старта/остановки
	startButton := widget.NewButton("Старт / Стоп", func() {
		running = !running
	})

	// Контейнер с элементами
	ui := container.NewVBox(
		widget.NewLabel("Скорость движения:"),
		speedSlider,
		startButton,
		canvasContainer,
	)

	// Анимация
	go func() {
		scale := 100.0
		offsetX, offsetY := 250.0, 250.0

		for i := 0; i < len(xData); i++ {
			if !running {
				time.Sleep(100 * time.Millisecond)
				continue
			}

			x := int(math.Round(scale*xData[i] + offsetX))
			y := int(math.Round(scale*yData[i] + offsetY))

			circle.Move(fyne.NewPos(float32(x), float32(y)))

			// Обновление UI
			canvasContainer.Refresh()

			// Управление скоростью
			time.Sleep(time.Duration(100/speedFactor) * time.Millisecond)
		}
	}()

	w.SetContent(ui)
	w.ShowAndRun()
}
