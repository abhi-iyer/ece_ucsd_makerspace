import cv2
import matplotlib.pyplot as plt
import numpy as np

img = cv2.imread('foo.jpeg')

height, width, channels = img.shape

blues = [img[0, 0, 0]]
greens = [img[0, 0, 1]]
reds = [img[0, 0, 2]]

blues_sum, greens_sum, reds_sum = 0, 0, 0

for r in range(1, height-1):
    for c in range(1, width-1):
        blues.extend([img[r, c, 0]]) # find blue layer values
        greens.extend([img[r, c, 1]]) # find green layer values
        reds.extend([img[r, c, 2]]) # find red layer values 
        
        blues_sum = blues_sum + img[r, c, 0]
        greens_sum = greens_sum + img[r, c, 1]
        reds_sum = reds_sum + img[r, c, 2]        

b = plt.figure(1)
plt.title("Blues Values")
plt.hist(blues, bins=100)
plt.xlabel("Value")
plt.ylabel("Frequency")
b.show()

g = plt.figure(2)
plt.title("Green Values")
plt.hist(greens, bins=100)
plt.xlabel("Value")
plt.ylabel("Frequency")
g.show()

r = plt.figure(3)
plt.title("Red Values")
plt.hist(reds, bins=100)
plt.xlabel("Value")
plt.ylabel("Frequency")
r.show()

plt.show()

print("Average blue color: ", blues_sum/len(blues))
print("Average green color: ", greens_sum/len(greens))
print("Average red color: ", reds_sum/len(reds))


    

