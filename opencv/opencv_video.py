import cv2
import time
import picamera

camera = picamera.PiCamera()

camera.start_preview()
camera.start_recording('/home/pi/video.h264')
time.sleep(10)
camera.stop_recording()
camera.stop_preview()
