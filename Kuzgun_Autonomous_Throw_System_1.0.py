#This code created by Lutfi Emre Askin in 09.08.2020

import numpy as np
import time
import RPi.GPIO as GPIO
import dronekit_sitl as planesim
from dronekit import connect, VehicleMode

print "Simulator baslatiliyor..."
sitl = planesim.start_default()
sitl.launch

print "%s uzerinden araca baglaniliyor... " % ('127.0.0.1:14550')
plane = connect('127.0.0.1:14551', wait_ready=True)
R=6371 # The radius of world

optimumDistance=5 # Optimum distance required for the load to be put in coordinates.
GPIO.setmode(GPIO.BOARD)
GPIO.setup(17,GPIO.OUT)
pwm=GPIO.PWM(17,50)
pwm.start(0)

def coordinateCreator(Global_Location):
    Pure_Location=""
    Latitude=""
    Longtitude=""
    Pure_LocationList=[]
    var=0
    
    for i in str(Global_Location):
        if(i=="-"):
            Pure_Location+=i
        try:
            if(i=="."):
                Pure_Location+=i
            elif(i==","):
                Pure_Location+=" "
            int(i)
            Pure_Location+=i
        except ValueError:
            pass

    for i in Pure_Location:
        Pure_LocationList.append(i)
    
    Pure_LocationList.pop(-1)
    Pure_Location=""
    
    for i in Pure_LocationList:
        Pure_Location+=i
    
    for i in Pure_Location:
        if(i==" "):
            var+=1
            pass
        elif(var==0):
            Latitude+=i
        elif(var==1):
            Longtitude+=i    
    return float(Latitude),float(Longtitude) 

def polToCart(lat,long):
    lat, long = np.radians(lat), np.radians(long)
    return R*np.cos(lat) *np.cos(long),\
           R*np.cos(lat) *np.sin(long),\
           R*np.sin(lat)

def haversine(Location,Destination):
    loc_cart = np.array(polToCart(*Location))
    dest_cart = np.array(polToCart(*Destination))
    euclidean_dist = np.linalg.norm(loc_cart-dest_cart)
    sinus_theta_2 = euclidean_dist / (R * 2)
    theta = 2*np.arcsin(sinus_theta_2)
    distance = R*theta
    return int(1000*distance)
    #return int(distance) Returns a result of type kilometers.

def setAngel(angle):
    theAngel=angle/18+2
    GPIO.output(17,True)
    pwm.ChangeDutyCycle(theAngel)
    time.sleep(1)
    GPIO.output(17,False)
    pwm.ChangeDutyCycle(0)

while True:
    locGF=plane.location.global_frame
    myPlane=coordinateCreator(locGF)
    distanceByMeter=haversine(myPlane,(39.91397035193426,32.85812416080516)) #
    if(distanceByMeter==optimumDistance):
        setAngel(90)
        pwm.stop()
        GPIO.cleanup()
        break
print("Mission Completed!")
