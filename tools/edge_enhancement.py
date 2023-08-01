import cv2
#import numpy as np
from glob import glob
import os


def edge_enhance(img):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    gauss_img = cv2.GaussianBlur(gray_img, (5, 5), sigmaX=1.5)
    equal_img = cv2.equalizeHist(gauss_img)

    #Canny#
    canny_img = cv2.Canny(equal_img, 70, 180, L2gradient=True, apertureSize=3)

    img[canny_img == 255, :] = 0
    return img


def edge_enhance_from_dir(tar_dir, save_dir):
    img_list = glob(tar_dir+"/*.*")
    for name in img_list:
        print(name)
        img = cv2.imread(name)
        img = edge_enhance(img)
        cv2.imwrite(save_dir+"/"+os.path.basename(name), img)


#Sobel#
#x = cv2.Sobel(equal_img, cv2.CV_16S, 1, 0)
##y = cv2.Sobel(equal_img, cv2.CV_16S, 0, 1)

#absX = cv2.convertScaleAbs(x)
#absY = cv2.convertScaleAbs(y)

#sobel_img = cv2.addWeighted(absX, 0.5, absY, 0.5, 0)
# sobel_img = cv2.adaptiveThreshold(sobel_img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#                                  cv2.THRESH_BINARY, 5, -12)
#Laplacian#
#log_img = cv2.Laplacian(equal_img, cv2.CV_16S, ksize=3)
#log_img = cv2.convertScaleAbs(log_img)


#Morphology#
#kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
# canny_img = cv2.morphologyEx(
#    canny_img, cv2.MORPH_CLOSE, kernel, iterations=2)
# canny_img = cv2.dilate(
#    canny_img, np.ones((2, 2), np.uint8), iterations=1)


#img[sobel_img == 255, :] = 0
#img[log_img > 150, :] = 0
