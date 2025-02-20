package main

import (
	"bufio"
	"fmt"
	"image"
	"image/color"
	"image/gif"
	"os"
	"strconv"
	"strings"
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
	var xRK4, yRK4 []float64
	scanner := bufio.NewScanner(file)

	// Пропуск заголовка
	scanner.Scan()

	// Чтение данных из файла
	for scanner.Scan() {
		line := scanner.Text()
		values := strings.Fields(line)

		// Преобразование строки в числа
		xr, _ := strconv.ParseFloat(values[1], 64)
		yr, _ := strconv.ParseFloat(values[2], 64)

		// Добавление данных в слайсы
		xRK4 = append(xRK4, xr)
		yRK4 = append(yRK4, yr)
	}

	// Подготовка GIF-файла
	outFile, err := os.Create("rossler_attractor.gif")
	if err != nil {
		fmt.Println("Ошибка при создании файла:", err)
		return
	}
	defer outFile.Close()

	gifEncoder := gif.GIF{}
	delay := 5 // интервал между кадрами

	// Создание кадров для анимации
	for i := 0; i < len(xRK4); i++ {
		// Создание изображения для текущего кадра
		img := image.NewRGBA(image.Rect(0, 0, 400, 400))
		// Белый фон
		for y := 0; y < 400; y++ {
			for x := 0; x < 400; x++ {
				img.Set(x, y, color.White)
			}
		}

		// Параметры для отображения данных на изображении
		scale := 50.0
		offsetX, offsetY := 200.0, 200.0

		// Преобразуем координаты в пиксели на изображении
		x := int(scale*xRK4[i] + offsetX)
		y := int(scale*yRK4[i] + offsetY)

		// Рисуем точку на изображении
		img.Set(x, y, color.RGBA{R: 255, G: 0, B: 0, A: 255}) // красный цвет

		// Добавляем кадр в GIF-анимацию
		palettedImg := image.NewPaletted(img.Bounds(), color.Palette{color.White, color.RGBA{R: 255, G: 0, B: 0, A: 255}})
		for y := 0; y < img.Bounds().Dy(); y++ {
			for x := 0; x < img.Bounds().Dx(); x++ {
				c := img.At(x, y)
				palettedImg.Set(x, y, c)
			}
		}

		gifEncoder.Image = append(gifEncoder.Image, palettedImg)
		gifEncoder.Delay = append(gifEncoder.Delay, delay)
	}

	// Запись GIF в файл
	if err := gif.EncodeAll(outFile, &gifEncoder); err != nil {
		fmt.Println("Ошибка при создании GIF:", err)
		return
	}

	fmt.Println("Анимация успешно сохранена в 'rossler_attractor.gif'")
}
