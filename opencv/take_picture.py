from time import sleep
from picamera import PiCamera

def take_photo():
    camera = PiCamera()
    camera.resolution = (1024, 768)
    camera.start_preview()
    sleep(2)
    camera.capture('foo.jpeg')
    camera.stop_preview()
