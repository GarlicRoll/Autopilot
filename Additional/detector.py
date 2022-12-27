import cv2
import numpy as np
import math

def get_difference(image1, image2):
    src1 = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY) # перевод кадров в черно-белую градацию
    src1 = cv2.GaussianBlur(src1, (5, 5), 0) # фильтрация лишних контуров
    src2 = cv2.cvtColor(image2, cv2.COLOR_BGR2GRAY)       # load second image in grayscale
    src2 = cv2.GaussianBlur(src2, (5, 5), 0) # фильтрация лишних контуров
    src1 = np.float32(src1)             # convert first into float32
    src2 = np.float32(src2)             # convert second into float32

    (sx, sy), sf = cv2.phaseCorrelate(src1,src2) # now calculate the phase correlation

    cx=0
    cy=0
    cx = math.ceil(cx - sx)
    cy = math.ceil(cy - sy)
    xform = np.float32([[1, 0, cx], [0, 1, cy]])

    im_stb = cv2.warpAffine(src2.astype('float32'), xform, dsize=(1280,720))
    dst = cv2.addWeighted(im_stb,0.5,src1,0.5,0)
    diff_i = cv2.absdiff(dst, src1) # нахождение разницы двух кадров, которая проявляется лишь при изменении одного из них, т.е. с этого момента наша программа реагирует на любое движение.
    diff_i = diff_i.astype(dtype='uint8')

    return diff_i

def stab_and_dviJ_det(imageI, imageII):  
    imageIII = imageII
    src1 = cv2.cvtColor(imageI, cv2.COLOR_BGR2GRAY) # перевод кадров в черно-белую градацию
    src1 = cv2.GaussianBlur(src1, (5, 5), 0) # фильтрация лишних контуров
    src2 = cv2.cvtColor(imageII, cv2.COLOR_BGR2GRAY)       # load second image in grayscale
    src2 = cv2.GaussianBlur(src2, (5, 5), 0) # фильтрация лишних контуров
    src1 = np.float32(src1)             # convert first into float32
    src2 = np.float32(src2)             # convert second into float32
    (sx, sy), sf = cv2.phaseCorrelate(src1,src2) # now calculate the phase correlation
    cx= 0
    cy=0
    cx =  math.ceil(cx - sx)
    cy =  math.ceil(cy - sy)
    xform = np.float32([[1, 0, cx], [0, 1, cy]])
    im_stb = cv2.warpAffine(src1.astype('float32'), xform, dsize=(src2.shape[1], src2.shape[0]))
    dst = cv2.addWeighted(src1,0.5,im_stb,0.5,0)
    # define the kernel
    kernel = np.ones((15, 15), np.uint8)
    # opening the image
    diff_i = get_difference(image1, image2)
    opening = cv2.morphologyEx(diff_i, cv2.MORPH_OPEN,kernel, iterations=1)
    opening=opening.astype(dtype='uint8')

    сontours, _ = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # нахождение массива контурных точек
    for contour in сontours:
        (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат
    
        # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить
        if cv2.contourArea(contour) > 5000: # условие при котором площадь выделенного объекта меньше 700 px
            #print(cv2.contourArea(contour))
            cv2.rectangle(imageIII, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
    return imageIII

image1 = cv2.imread('0069.jpg')
image2 = cv2.imread('0070.jpg')


im = stab_and_dviJ_det(image1, image2)

cv2.imwrite("D:\Programming\Python\Autopilot\detected.jpg", im)