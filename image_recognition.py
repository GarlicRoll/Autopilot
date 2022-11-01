from PIL import Image, ImageDraw 

image = Image.open('result.jpg')  # Открываем изображение
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

for x in range(width):
    med = 0 
    for y in range(height):
       med += pix[x, y][0]
    med //= height # Среднее значение серого в столбце
    wall = med // 1.5
    for y in range(height):
        if pix[x, y][0] < wall:
            draw.point((x, y), (255, 0, 0)) #рисуем пиксель
        else:
            draw.point((x, y), pix[x, y]) #рисуем пиксель

for y in range(height):
    med = 0 
    for x in range(width):
       med += pix[x, y][0]
    med //= height # Среднее значение серого в столбце
    wall = med // 2.5
    for x in range(width):
        if pix[x, y][0] < wall:
            draw.point((x, y), (0, 255, 0)) #рисуем пиксель

image.save("result2.jpg", "JPEG") #не забываем сохранить изображение