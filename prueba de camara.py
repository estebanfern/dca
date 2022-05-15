import time
import picamera

imagen=r"./foto.jpg"

with picamera.PiCamera() as picam:
    picam.start_preview()
    time.sleep(1)
    picam.capture(imagen)
    picam.stop_preview()
    picam.close()