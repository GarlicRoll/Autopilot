# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:09:15 2022

@author: user
"""
import numpy as np
import cv2 
import sys

# 1) Выделение области + пробел
# 2) Esc для выхода обратно в выделение области
# 3) Esc второй раз для выхода и корректной остановки записи
# *) Ваше окошечко записывается при работе 

if __name__ == '__main__' :
    
    # установка трекера
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output_test4.avi', fourcc, 15.0, (1280,  720)) # 640 480
    tracker = cv2.TrackerCSRT.create() # tracker = cv2.TrackerCSRT_create()
    # tracker = cv2.TrackerDaSiamRPN.create()
    # tracker = cv2.TrackerKCF.create()

    # считываем поток 
    video = cv2.VideoCapture(0)
    ret, frame = video.read()
    while True:
         # --- Детекция через фильтр (без накопления кадров) ---
         # полчаем фрйм
         ret, frame = video.read()
         # 
         if not ret:
             print("потока нет ")
             break
         # обработка 
         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) # перевод кадров в черно-белую градацию
         blur = cv2.GaussianBlur(gray, (5, 5), 0) # фильтрация лишних контуров
         edges = cv2.Canny(blur, 100, 300)
        
         # оператор собеля 
         kernel16 = np.array([[-1, -1, -1],
                              [0, 0, 0],
                              [1, 1, 1]])
         kernel17 = np.array([[-1, 0, 1],
                              [-1, 0, 1],
                              [-1, 0, 1]])
         kernel18 = np.array([[0, 1, 1],
                              [-1, 0, 1],
                              [-1, -1, 0]])
         kernel19 = np.array([[0, -1, -1],
                              [1, 0, -1],
                              [1, 1, 0]])
         Image_Sobel = cv2.filter2D(edges, -1, kernel16) + cv2.filter2D(edges, -1, kernel17) + cv2.filter2D(edges, -1, kernel18) + cv2.filter2D(edges, -1, kernel19)

         #размеры маски и ее создание 
         q=int((frame.shape[0])/5)
         b=int((frame.shape[1])/5)
         e=int((frame.shape[1])*(4/5))
         c=int((frame.shape[0])*(4/5))
         mask = np.zeros((frame.shape[0], frame.shape[1]), dtype = "uint8")
         cv2.rectangle(frame, (q, b), (e, c), (0, 255, 0), 2)
         cv2.rectangle(mask, (q, b), (e, c), 255, -1)
         #масочная фильтрация 
         Image_Sobel = mask & Image_Sobel
         #контуры    
         сontours, _ = cv2.findContours(Image_Sobel, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # нахождение массива контурных точек
         
         box_for_tracking = (0, 0, 0, 0)
         #механизм отрисовки всех контуров более 500
         for contour in сontours:
             (x, y, w, h) = cv2.boundingRect(contour) # преобразование массива из предыдущего этапа в кортеж из четырех координат
             
             # метод contourArea() по заданным contour точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить

             if cv2.contourArea(contour) > 500: # условие при котором площадь выделенного объекта меньше 500 px
                 print(cv2.contourArea(contour))
                 cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2) # получение прямоугольника из точек кортежа
                 box_for_tracking = (x, y, w, h) # Выбираем последний квадратик

         """  
         for contour in сontours:
             if cv2.contourArea(contour) < 500: # условие при котором площадь выделенного объекта меньше 500 px
                 сontours.remove(contour)
        """ 
        
        # cv2.imshow('frame', frame)
            
         # записыаем в видео кадр с детекцией
         for _ in range(10):
             out.write(frame)
         # --- Трекинг через CSRT Tracker ---    
         # получим координаты рамки
         # bbox = cv2.selectROI('frame', frame, False)
         print(box_for_tracking)
         # в случае, если ничего не задетектили
         if box_for_tracking == (0, 0, 0, 0):
            box_for_tracking = (240, 170, 80, 130)
         # инициализация трекинга
         ok = tracker.init(frame, box_for_tracking)
      
         while True:
             # считываем новый кадр
             ok, frame = video.read()
             if not ok:
                 break
              
             # запусим иаймер
             timer = cv2.getTickCount()
      
             # обновим трекер 
             ok, bbox = tracker.update(frame)
      
             # считаем количесво кадров в секунду 
             fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
             cv2.circle(frame, (340,240), radius=0, color=(0, 255, 0), thickness=10)
             # выделим йднное
             if ok:
                 p1 = (int(bbox[0]), int(bbox[1]))
                 p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
                 cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
                 
             else :
                 # Tracking failure
                 cv2.putText(frame, "сбой", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
                 
             # навание трекинга
             cv2.putText(frame, "CSRT Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
          
             # кадры в секунду
             cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2)
      
             #выведем изображение 
             cv2.imshow('frame', frame)
             out.write(frame)
             #выход из трекинга
             k = cv2.waitKey(1) & 0xff
             if k == 27 : break 
         
         #выход из детекции
         if cv2.waitKey(1) == ord('q'):
             break
cv2.destroyAllWindows()
#ссылка по ппм
#https://www.rcgroups.com/forums/showthread.php?2037080-DIY-Arduino-joystick-to-PPM
   
