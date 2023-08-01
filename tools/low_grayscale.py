import cv2
import numpy as np
from tkinter.filedialog import askopenfilename
import os

img_path = askopenfilename()
mask_path = askopenfilename()

img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
mask = mask != 0
#mask = np.ones_like(img)
modify_bits = 5  # 0~8
img_blur = cv2.GaussianBlur(img, ksize=(11, 11), sigmaX=3, sigmaY=3)
img[mask] = (img_blur[mask] // (2 ** modify_bits)) * (2 ** modify_bits)

#img = cv2.GaussianBlur(img, ksize=(5, 5), sigmaX=1, sigmaY=1)
#img[mask == 1] = img[mask == 1] * (2 ** modify_bits)

cv2.imshow("img", img)
cv2.waitKey(0)
print(os.path.dirname(img_path))
cv2.imwrite(os.path.dirname(img_path)+"/low_grayscale.jpg", img)
