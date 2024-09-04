from djitellopy import tello
from time import sleep

#import module for time:
import time

#import the previous keyboard input module file from the first step:
import KeyboardTelloModule as kp

#import the numpy library
import numpy as np

#import opencv python module:
import cv2
#Global Variable
global img
#Start Connection With Drone
Drone = tello.Tello()
Drone.connect()
    
#Get Battery Info
print(Drone.get_battery())

def getKeyboardInput():
    #LEFT RIGHT, FRONT BACK, UP DOWN, YAW VELOCITY
    lr, fb, ud, yv = 0,0,0,0
    speed = 80 
    liftSpeed = 80
    moveSpeed = 85
    rotationSpeed = 100

    if kp.getKey("LEFT"): lr = -speed #Controlling The Left And Right Movement
    elif kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = moveSpeed #Controlling The Front And Back Movement
    elif kp.getKey("DOWN"): fb = -moveSpeed

    if kp.getKey("w"): ud = liftSpeed #Controleling The Up And Down Movemnt:
    elif kp.getKey("s"): ud = -liftSpeed 

    if kp.getKey("d"): yv = rotationSpeed #Controlling the Rotation:
    elif kp.getKey("a"): yv = -rotationSpeed 

    if kp.getKey("q"): Drone.land(); time.sleep(3) #Landing The Drone
    elif kp.getKey("e"): Drone.takeoff() #Take Off The Drone

    if kp.getKey("z"): #Screen Shot Image From The Camera Display
        cv2.imwrite(f"tellopy/Resources/Images/{time.time()}.jpg", img)
        time.sleep(0.3)

    return [lr, fb, ud, yv] #Return The Given Value
#Initialize Keyboard Input
kp.init()


w,h = 360,240
fbRange = [6200,6800]
pid = [0.4, 0.4, 0]
pError = 0

def findFace(img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,1.2,8)

    myFaceListc = []
    myFaceListArea = []
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w, y+h),(0,0,255),2)
        cx = x+w//2
        cy = y+h//2
        area = w*h
        cv2.circle(img,(cx,cy),5,(0,255,0),cv2.FILLED)
        myFaceListc.append([cx,cy])
        myFaceListArea.append(area)
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListc[i], myFaceListArea[i]]
    else:
        return img, [[0,0],0]

def trackFace(info,w,pid,pError):
    area = info[1]
    x,y = info[0]
    fb = 0
    error = x-w//2
    speed = pid[0]*error + pid[1]*(error-pError)
    speed = int(np.clip(speed,-100,100))


    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    if area > fbRange[1]:
        fb = -20
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0
    #print(speed,fb)
    Drone.send_rc_control(0,fb,0,speed)
    return error


#Start Camera Display Stream
Drone.streamon()

#manual
while True:
#Get The Return Value And Stored It On Variable:
    keyValues = getKeyboardInput() #Get The Return Value And Stored It On Variable
#Control The Drone:
    Drone.send_rc_control(keyValues[0],keyValues[1],keyValues[2],keyValues[3]) 
#Get Frame From Drone Camera Camera 
    img = Drone.get_frame_read().frame
    img = cv2.resize(img, (500,400))
    img, info = findFace(img)
    pError = trackFace(info,w,pid,pError)
#Show The Frame
    cv2.imshow("DroneCapture", img)
    cv2.waitKey(1)




#automatic 
while True:
    Drone.send_rc_control(40,0,0,0)
    Drone.send_rc_control(0,40,0,0)
    img =Drone.get_frame_read().frame
    img = cv2.resize(img,(w,h))
    img, info = findFace(img)
    pError = trackFace(info,w,pid,pError)
    cv2.imshow("DroneCapture",img)
    cv2.waitley(1)
    