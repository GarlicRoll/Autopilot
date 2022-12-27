from PIL import Image, ImageDraw 

image = Image.open('test.jpg')  # Открываем изображение
draw = ImageDraw.Draw(image)  # Создаем инструмент для рисования
width = image.size[0]  # Определяем ширину
height = image.size[1]  # Определяем высоту
pix = image.load()  # Выгружаем значения пикселей

for x in range(width):
    for y in range(height):
       r, g, b = pix[x, y] #узнаём значение цветов пикселя
       sr = (r + g + b) // 3 #среднее значение
       draw.point((x, y), (sr, sr, sr)) #рисуем пиксель

image.save("result.jpg", "JPEG") #не забываем сохранить изображение
