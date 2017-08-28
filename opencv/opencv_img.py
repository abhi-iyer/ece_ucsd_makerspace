import cv2

img = cv2.imread('foo.jpeg')
height, width, channels = img.shape

blues = [img[0, 0, 0]]
greens = [img[0, 0, 1]]
reds = [img[0, 0, 2]]

for r in range(1, height-1):
    for c in range(1, width-1):
        blues.extend([img[r, c, 0]]) # find blue layer values
        greens.extend([img[r, c, 1]]) # find green layer values
        reds.extend([img[r, c, 2]]) # find red layer values 


    

