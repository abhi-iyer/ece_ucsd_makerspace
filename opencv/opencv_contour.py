import cv2
import matplotlib.pyplot as plt
import numpy as np
from take_picture import take_photo

take_photo()

im = cv2.imread('foo.jpeg')
img = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

cv2.imwrite('foo_bw.jpg', img)


