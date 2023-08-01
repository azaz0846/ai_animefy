import cv2
import numpy as np
import os

cap = cv2.VideoCapture('sample.mp4')
print('height:{} width:{}'.format(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
      int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))))
frame_num = 0
total_frame = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print(__file__)
# out_video = cv2.VideoWriter(
#    "MyDemo6.mp4", cv2.VideoWriter_fourcc(*'mp4v'), 60, (251, 533))
while frame_num < total_frame:
    ret, frame = cap.read()
    print(frame_num)
    print(frame.shape)
    if ret == False:
        break

    cv2.imwrite(os.path.dirname(os.path.abspath( __file__)) +"/temp/"+
                str(frame_num)+".jpg", frame)

    frame_num += 1
# out_video.release()
cap.release()
