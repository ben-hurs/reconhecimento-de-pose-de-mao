import cv2
import time
import numpy as np
from cvzone.HandTrackingModule import HandDetector 
import mediapipe as mp
import math

wCam, hCam = 1280, 720

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(detectionCon=0.7)

length = 0
lengthPercentage = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img, draw=True)
    
    if hands:
        for hand in hands:
            lmList = hand["lmList"]  # Lista de pontos chave da mão
            if lmList:
                x1, y1 = lmList[4][0], lmList[4][1]  
                x2, y2 = lmList[8][0], lmList[8][1]  
                cx, cy = (x1+x2)//2, (y1+y2)//2

                cv2.circle(img, (x1, y1), 15, (255,0,255), cv2.FILLED)
                cv2.circle(img, (x2, y2), 15, (255,0,255), cv2.FILLED)
                cv2.line(img, (x1, y1), (x2, y2),(255,0,255),3)
                cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)

                length = int(math.hypot(x2-x1, y2-y1))
                lengthPercentage = int((length / 400) * 100)

                if length < 50:
                    cv2.circle(img, (cx, cy), 15, (0,255,0), cv2.FILLED)

    cv2.rectangle(img, (50, 200), (80, 600), (0,255,0), 3)
    cv2.rectangle(img, (50, 600 - length), (80, 600), (0,255,0), cv2.FILLED)

    cv2.putText(img, f'{lengthPercentage}%', (40, 650), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0,0), 2)

    cv2.imshow('Imagem',img)
    cv2.waitKey(1)
