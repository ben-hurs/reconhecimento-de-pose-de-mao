import cv2
import numpy as np
from cvzone.HandTrackingModule import HandDetector 
import mediapipe as mp
import math


class VideoCamera(object):
    def __init__(self):
        wCam, hCam = 1280, 720
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, wCam)
        self.cap.set(4, hCam)
        self.detector = HandDetector(detectionCon=0.7)

    def __del__(self):
        self.cap.release()

    def get_frames(self):         
        length = 0
        lengthPercentage = 0

        success, img = self.cap.read()
        hands, img = self.detector.findHands(img, draw=True)
        
        if hands:
            for hand in hands:
                lmList = hand["lmList"]  # Lista de pontos chave da mão
                if lmList:
                    x1, y1 = lmList[4][0], lmList[4][1]  
                    x2, y2 = lmList[8][0], lmList[8][1]  
                    cx, cy = (x1+x2)//2, (y1+y2)//2

                    cv2.circle(img, (x1, y1), 15, (255,0,0), cv2.FILLED)  
                    cv2.circle(img, (x2, y2), 15, (255,0,0), cv2.FILLED)  
                    cv2.line(img, (x1, y1), (x2, y2),(255,0,0),3)  

                    length = int(math.hypot(x2-x1, y2-y1))
                    lengthPercentage = int((length / 400) * 100)

                    barHeight = np.interp(length, [50, 400], [0, 400])
                    barColor = (0, 255, 0) if barHeight != 0 else (0, 0, 255)
                    cv2.rectangle(img, (50, 200), (80, 600), barColor, 3)
                    cv2.rectangle(img, (50, 600 - int(barHeight)), (80, 600), barColor, cv2.FILLED)
                
                break
        cv2.putText(img, f'{lengthPercentage}%', (40, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)
        
        ret, jpeg = cv2.imencode('.jpg', img)
        return jpeg.tobytes()
