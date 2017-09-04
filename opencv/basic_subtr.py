import cv2
import numpy

img_fg = cv2.imread('foreground.jpeg')
img_bg = cv2.imread('background.jpeg')

##cv2.imshow('fg', img_fg)
##cv2.imshow('bg', img_bg)
##cv2.waitKey(0)

img = cv2.absdiff(img_fg, img_bg)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#retval, img_gray2 = cv2.threshold(img_gray, 50, 255, cv2.THRESH_BINARY)

#img = cv2.subtract(img_fg, img_bg)
cv2.imshow('pain', img_gray)
cv2.waitKey(0)
#cv2.imwrite('total.jpeg', img)
