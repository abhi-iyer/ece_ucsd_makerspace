import cv2
import time
import picamera

camera = picamera.PiCamera()

camera.start_preview()
camera.start_recording('people_walking.h264')
time.sleep(15)
camera.stop_recording()
camera.stop_preview()
