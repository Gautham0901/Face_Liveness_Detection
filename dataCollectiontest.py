import cvzone
from cvzone.FaceDetectionModule import FaceDetector
import cv2
from time import time

#####################################
classID = 0 #0 is fake , 1 is real
outputFolderPath = 'Dataset/DataCollect'
confidence = 0.6
save = True
BlurThreshold = 50 #larger is more focus

offsetPercentagew = 10
offsetPercentageh = 20
camWidth, camHeight = 640,480
floatingpoints  = 6
debug = False
######################################


cap = cv2.VideoCapture(0)
cap.set(3,camWidth)
cap.set(4,camHeight)
detector = FaceDetector()

while True:
    success, img = cap.read()
    imgOut = img.copy()
    img, bboxs = detector.findFaces(img,draw=False)

    listblur = []  # True False values indicating faces are blur or not
    listinfo = []  # normalized values and cls names or label txt files

    if bboxs:
        # bboxsinfo
        for bbox in bboxs:
            x,y,w,h = bbox["bbox"]
            score= bbox["score"][0]
            #print(x,y,w,h)

            # -------- check the score  --------
            if score>confidence:

                # -------- adding an offset to the face detected --------
                offsetW = (offsetPercentagew/100)*w
                x = int(x - offsetW)
                w = int(w + offsetW * 2)

                offsetH = (offsetPercentageh / 100) * h
                y = int(y - offsetH*3)
                h = int(h + offsetH * 3.5)

                # -------- to avoid values below 0 --------
                if x<0: x=0
                if y < 0: y = 0
                if w < 0: w = 0
                if h < 0: h = 0

                # -------- find blurriness--------
                imgFace = img[y:y+h, x:x+w]
                cv2.imshow("Face",imgFace)
                blurValue = int(cv2.Laplacian(imgFace,cv2.CV_64F).var())
                if blurValue>BlurThreshold:
                    listblur.append(True)
                else:
                    listblur.append(False)

                # -------- normalize values --------
                ih, iw, _ = img.shape
                xc, yc = x+w/2, y+h/2

                xcn, ycn= round(xc/iw,floatingpoints), round(yc/ih,floatingpoints)
                wn,hn =  round(w/iw,floatingpoints), round(h/ih,floatingpoints)
                # print(xcn, ycn,  wn,hn )

                # -------- to avoid values above 1 --------
                if xcn > 1: xcn = 1
                if ycn > 1: ycn = 1
                if wn > 1: wn = 1
                if hn > 1: hn = 1

                listinfo.append(f"{classID} {xcn} {ycn} {wn} {hn}\n")


                # -------- drawing --------
                cv2.rectangle(imgOut, (x, y, w, h), (255, 0, 0), 3)
                cvzone.putTextRect(imgOut,f'Score : {int(score*100)}% Blur: {blurValue}',(x,y-20),
                                   scale=2,thickness=3)
                if debug:
                    cv2.rectangle(img, (x, y, w, h), (255, 0, 0), 3)
                    cvzone.putTextRect(img, f'Score : {int(score * 100)}% Blur: {blurValue}', (x, y - 20),
                                   scale=2, thickness=3)

        #----- To save ------
        if save:
            if all(listblur) and listblur!=[]:
                # ---- save image ----
                timeNow = time()
                timeNow = str(timeNow).split('.')
                timeNow = timeNow[0]+timeNow[1]
                cv2.imwrite(f"{outputFolderPath}/{timeNow}.jpg",img)

                # ---- save label txt file ----
                for info in listinfo:
                    f = open(f"{outputFolderPath}/{timeNow}.txt",'a')
                    f.write(info)
                    f.close()








    cv2.imshow("Image", imgOut)

    cv2.waitKey(1)