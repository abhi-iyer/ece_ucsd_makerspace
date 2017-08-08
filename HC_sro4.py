import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
TRIG = 23
ECHO = 24
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)
GPIO.output(TRIG, False)
print "Waiting For Sensor To Settle"
time.sleep(2)
idle_distance = 0


def uh_control(control=0):
    if control == 0:
        #Turn ON by default
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()
        while GPIO.input(ECHO)==1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
        print "Distance:",distance,"cm"
        global idle_distance
        if (idle_distance):
            if (distance < 0.7*idle_distance):
                print "Intruder detected with distace", distance, "cm"
        else:
            idle_distance=distance
            print "idle_distance set as ", idle_distance
    if control == 1:
        #Turn OFF the sensor
        GPIO.output(TRIG, False)

if __name__ == "__main__" :
    while(True):
        uh_control(control=0)
        time.sleep(0.5)

