from sklearn.cluster import KMeans
from matplotlib.pyplot as plt
import argparse
import utils
import cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="2017-08-15-151252_1366x768_scrot.png")
ap.add_argument("-c", "--clusters", required=True, type=int, help="# of clusters")
args = vars(ap.parse_args())

image = cv2.imread(args["image"])
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.figure()
plt.axis("off")
plt.imshow(image)
