
# This is client code to receive video frames over UDP
import cv2, imutils, socket
import numpy as np
import time
import base64

from SiamFC.tracker import TrackerSiamFC

def detection():
    # --- Детекция через фильтр (без накопления кадров) ---
        
        # обработка
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # перевод кадров в черно-белую градацию
        blur = cv2.GaussianBlur(gray, (5, 5), 0)  # фильтрация лишних контуров
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
        Image_Sobel = cv2.filter2D(edges, -1, kernel16) + cv2.filter2D(edges, -1, kernel17) + cv2.filter2D(edges, -1,
                                                                                                           kernel18) + cv2.filter2D(
            edges, -1, kernel19)

        # размеры маски и ее создание
        q = int((frame.shape[0]) / 5)
        b = int((frame.shape[1]) / 5)
        e = int((frame.shape[1]) * (4 / 5))
        c = int((frame.shape[0]) * (4 / 5))
        mask = np.zeros((frame.shape[0], frame.shape[1]), dtype="uint8")
        cv2.rectangle(frame, (q, b), (e, c), (0, 255, 0), 2)
        cv2.rectangle(mask, (q, b), (e, c), 255, -1)
        # масочная фильтрация
        Image_Sobel = mask & Image_Sobel
        # контуры
        сontour_points, _ = cv2.findContours(Image_Sobel, cv2.RETR_TREE,
                                             cv2.CHAIN_APPROX_SIMPLE)  # нахождение массива контурных точек

        box_for_tracking = (0, 0, 0, 0)
        # механизм отрисовки всех контуров более 500
        for point in сontour_points:
            (x, y, w, h) = cv2.boundingRect(
                point)  # преобразование массива из предыдущего этапа в кортеж из четырех координат

            # метод contourArea() по заданным point точкам, здесь кортежу, вычисляет площадь зафиксированного объекта в каждый момент времени, это можно проверить

            if cv2.contourArea(point) > 500:  # условие при котором площадь выделенного объекта меньше 500 px
                print(cv2.contourArea(point))
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0),
                              2)  # получение прямоугольника из точек кортежа
                box_for_tracking = (x, y, w, h)  # Выбираем последний квадратик

        """  
        for point in сontour_points:
            if cv2.contourArea(point) < 500: # условие при котором площадь выделенного объекта меньше 500 px
                сontour_points.remove(point)
       """

        # cv2.imshow('frame', frame)

        # записыаем в видео кадр с детекцией
        for _ in range(10):
            video_output.write(frame)

        return box_for_tracking

BUFF_SIZE = 65536
client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
host_name = socket.gethostname()
host_ip = 'localhost'#  socket.gethostbyname(host_name)
print(host_ip)
port = 9999

client_socket.sendto(b'',(host_ip,port))
fps,st,frames_to_count,cnt = (0,0,20,0)

tracker_name = "SiamFC"
if tracker_name == "CSRT":
	tracker = cv2.TrackerCSRT.create()  # tracker = cv2.TrackerCSRT_create()
elif tracker_name == "SiamFC":
	tracker = TrackerSiamFC("./SiamFC/model.pth") 

box_for_tracking = (0, 0, 0, 0)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
video_output = cv2.VideoWriter('output_test4.avi', fourcc, 15.0, (1280,  720)) # 640 480

while True:
	packet,_ = client_socket.recvfrom(BUFF_SIZE)
	data = base64.b64decode(packet,' /')
	npdata = np.fromstring(data,dtype=np.uint8)
	frame = cv2.imdecode(npdata,1)
	#frame = cv2.putText(frame,'FPS: '+str(fps),(10,40),cv2.FONT_HERSHEY_SIMPLEX,0.7,(0,0,255),2)

	###############
	timer = cv2.getTickCount()
            
	if box_for_tracking == (0, 0, 0, 0):
		box_for_tracking = detection()
		if box_for_tracking != (0, 0, 0, 0):
	        # --- Трекинг через Tracker ---
			ok = tracker.init(frame, box_for_tracking)
	else:
        # обновим трекер
		if tracker_name == "CSRT":
			ok, bbox = tracker.update(frame)
		elif tracker_name == "SiamFC":
			bbox = tracker.update(frame)

        # считаем количесво кадров в секунду
		fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
		cv2.circle(frame, (340, 240), radius=0, color=(0, 255, 0), thickness=10)
        # выделим йднное
		if (ok and tracker_name == "CSRT") or (tracker_name == "SiamFC"):
			p1 = (int(bbox[0]), int(bbox[1]))
			p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
			#cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
			cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3])), (0, 255, 255), 3)
		else:
            # Tracking failure
			cv2.putText(frame, "ERROR", (100, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
			box_for_tracking = (0, 0, 0, 0)

        # навание трекинга
		cv2.putText(frame, tracker_name + " Tracker", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

        # кадры в секунду
		cv2.putText(frame, "FPS : " + str(int(fps)), (100, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50, 170, 50), 2)

		video_output.write(frame)
    ########

	cv2.imshow("RECEIVING VIDEO",frame)
	key = cv2.waitKey(1) & 0xFF
	if key == ord('q'):
		client_socket.close()
		break
	if cnt == frames_to_count:
		try:
			fps = round(frames_to_count/(time.time()-st))
			st=time.time()
			cnt=0
		except:
			pass
	cnt+=1

'''
@inproceedings{Zhu_2018_ECCV,
  title={Distractor-aware Siamese Networks for Visual Object Tracking},
  author={Zhu, Zheng and Wang, Qiang and Bo, Li and Wu, Wei and Yan, Junjie and Hu, Weiming},
  booktitle={European Conference on Computer Vision},
  year={2018}
}

@InProceedings{Li_2018_CVPR,
  title = {High Performance Visual Tracking With Siamese Region Proposal Network},
  author = {Li, Bo and Yan, Junjie and Wu, Wei and Zhu, Zheng and Hu, Xiaolin},
  booktitle = {The IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2018}
}
'''
