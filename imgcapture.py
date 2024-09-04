from djitellopy import tello
from time import sleep
import cv2

#control left click on tello to see all the commands
#https://djitellopy.readthedocs.io/en/latest/tello/

me = tello.Tello()
me.connect()
print(me.get_battery())

#img capture
me.streamon()
while (True):
    img = me.get_frame_read().frame
    img = cv2.resize(img, (360,240))
    cv2.imshow("Image",img)
    cv2.waitKey(1)#giving it a delay so we can see the frame
