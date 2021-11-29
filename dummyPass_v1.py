import cv2
import time
import os
import HandTrackingModule as htm
from datetime import datetime


passw = input('Enter password\n')

wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folPath = "numbers"

numList = os.listdir(folPath)

tipIds = [4,8,12,16,20]

# print(numList)

overlayList = []

enterPass=[]

for imPath in numList:
    image = cv2.imread(f'{folPath}/{imPath}')
    overlayList.append(image)
    print(f'{folPath}/{imPath}')

# print(len(overlayList))
prevTime = 0

detector = htm.handDetector(detectionCon=0.75)
fingers=[]
totalFingersUp=0
countZeros=[]
while countZeros.count(0)<30:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    # print(lmList)
    fingers = []
    if len(lmList) !=0:


        if lmList[17][1]<lmList[2][1]:
            if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)
        else:
            if lmList[tipIds[0]][1] < lmList[tipIds[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)




        for id in range(1,5):
            if lmList[tipIds[id]][2] <lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        # print(fingers)
        print(countZeros)
        totalFingersUp = fingers.count(1)
        if totalFingersUp==0:
            countZeros.append(0)

    seconds = int(round(time.time()))
    print(seconds%10)
    if seconds%5==0:
        enterPass.append(totalFingersUp)
    else:
        enterPass.append('#')
    # print(enterPass)




    h, w,c = overlayList[totalFingersUp].shape

    img[0:200, 0:200] = overlayList[totalFingersUp]
    # print(enterPass)
    # print(totalFingersUp)
    cTime = time.time()
    fps = 1 / (cTime - prevTime)
    prevTime = cTime
    cv2.imshow("image", img)
    # cv2.putText(img,f'FPS: {int(fps)}',(400,70), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,255),2)
    cv2.waitKey(1)

val = [x for x in str(enterPass) if x in ['1','2','3','4','5']]

print('done')

res = []
[res.append(x) for x in val if x not in res]


res = str(res)


listArr=[]
listArr.append(passw)
if listArr.__eq__(res):
    print("Password is correct")


