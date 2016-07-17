__author__ = 'kuolin'
import cv2
import time
from shutil import copyfile

camera_port = 0
ramp_frames = 30
def capture(filename=None):
    camera = cv2.VideoCapture(camera_port)
    for i in range(ramp_frames):
        temp = camera.read()
    camera_capture = get_image(camera)
    if not filename:
        filename = str(time.time())+".jpg"
    cv2.imwrite(filename,camera_capture)
    del(camera)
    copyfile(filename, 'newest.jpg')
    return filename

def get_image(camera):
    retval, im = camera.read()
    return im

if __name__ == '__main__':
    capture()