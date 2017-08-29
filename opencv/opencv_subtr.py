import cv2
import numpy

img_fg = cv2.imread('foreground.jpeg')
img_bg = cv2.imread('background.jpeg')

img = cv2.absdiff(img_fg, img_bg)

cv2.imwrite('total.jpeg', img)
