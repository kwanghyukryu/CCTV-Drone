from djitellopy import tello
from time import sleep
import cv2

#control left click on tello to see all the commands
#https://djitellopy.readthedocs.io/en/latest/tello/

me = tello.Tello()
me.connect()
print(me.get_battery())

#basic movment
me.takeoff()
me.send_rc_control(0,50,0,0) # left right(- is left), forward backwards(- is back),up down(- is up), yaw(- will look left, positive will look right)
sleep(2)
me.send_rc_control(30,0,0,0)
sleep(2)
me.send_rc_control(0,0,0,0)
me.land()

