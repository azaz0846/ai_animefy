import cv2
import numpy as np
import tensorflow as tf
from tqdm import tqdm
import glob
import os
path = glob.glob(os.path.dirname(os.path.abspath( __file__))+"/temp_result/*.*")
path.sort(key=lambda x: int(os.path.splitext(os.path.basename(x))[0]))
img = list()
for p in tqdm(path):
    img.append(cv2.imread(p))

# init writer
out_video = cv2.VideoWriter(
    "sample_result2.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 30, (img[0].shape[1], img[0].shape[0]))

for i in tqdm(img):
    # Save to writer
    out_video.write(i)

# close file and clean up
out_video.release()
