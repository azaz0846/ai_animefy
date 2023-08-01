

from mrcnn import visualize
import mrcnn.model as modellib
from mrcnn import utils
import argparse
import cv2
import numpy as np
import math
import random
import sys
import os
import keras
import tensorflow as tf
from glob import glob
from tqdm import tqdm
config = tf.ConfigProto()
# 0.6 sometimes works better for folks
config.gpu_options.per_process_gpu_memory_fraction = 0.9
keras.backend.tensorflow_backend.set_session(tf.Session(config=config))


# Root directory of the project
project_root = str(os.path.dirname(os.path.abspath(__file__)))
ROOT_DIR = os.path.abspath(project_root+"/Mask_RCNN/")
print(ROOT_DIR)


# Import Mask RCNN
sys.path.append(ROOT_DIR)  # To find local version of the library
# Import COCO config
# To find local version
sys.path.append(os.path.join(ROOT_DIR, "samples/coco/"))
import coco

# Directory to save logs and trained model
MODEL_DIR = os.path.join(ROOT_DIR, "logs")

# Local path to trained weights file
COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
# Download COCO trained weights from Releases if needed
if not os.path.exists(COCO_MODEL_PATH):
    utils.download_trained_weights(COCO_MODEL_PATH)

# Directory of images to run detection on
IMAGE_DIR = os.path.join(ROOT_DIR, "images")


class InferenceConfig(coco.CocoConfig):
    # Set batch size to 1 since we'll be running inference on
    # one image at a time. Batch size = GPU_COUNT * IMAGES_PER_GPU
    GPU_COUNT = 1
    IMAGES_PER_GPU = 1


config = InferenceConfig()
# config.display()

model = modellib.MaskRCNN(mode="inference", model_dir=MODEL_DIR, config=config)

# Load weights trained on MS-COCO
model.load_weights(COCO_MODEL_PATH, by_name=True)

class_names = ['BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
               'bus', 'train', 'truck', 'boat', 'traffic light',
               'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
               'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
               'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
               'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
               'kite', 'baseball bat', 'baseball glove', 'skateboard',
               'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
               'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
               'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
               'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
               'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
               'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
               'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
               'teddy bear', 'hair drier', 'toothbrush']


path = project_root+"/temp_photos/target/"


with open(project_root+"/temp_photos/body_crop_position.txt", mode='w') as f:
    for image_path in tqdm(glob(path+"*.*")):
        print(image_path)
        image = cv2.imread(image_path)
        results = model.detect([image], verbose=0)
        r = results[0]
        c=0
        #print(r)
        #r.sort(key=lambda x:x['rois'][1])
        rr = list()
        for i,v in enumerate(r['rois']):
            rr.append([v])
        for i,v in enumerate(r['class_ids']):
            rr[i].append(v)
        for i,v in enumerate(r['scores']):
            rr[i].append(v)
        #print(r['masks'].shape)
        for i in range(len(r['masks'][1][1])):
            #print(v.shape)
            rr[i].append(r['masks'][ : , : , i ] )
            
        rr.sort(key=lambda x: x[0][1])

        for i, item in enumerate(rr):
            box = item[0]
            crop = image[box[0]:box[2], box[1]:box[3]]
            score = item[2]
            
            if  score<0.95 or  item[1] != 1:
                continue
            print(item)
            #print(c)

            

            print(box)
            image_name, extension = os.path.splitext(
                os.path.basename(image_path))

            cv2.imwrite(project_root+"/temp_photos/crop/body/" +
                        image_name+'-'+str(c)+extension, crop)
            mask = item[3]
            mask = np.where(mask == 1, 255, 0)
            cropmask = mask[box[0]:box[2], box[1]:box[3]]
            cv2.imwrite(project_root+"/temp_photos/mask/body/" +
                        image_name+'-'+str(c)+extension, cropmask)
            center_y = (box[0]+box[2])//2
            center_x = (box[1]+box[3])//2
            start_y = box[0]
            start_x = box[1]
            #f.write(image_name+'-'+str(i)+extension+" "+str(center_x)+" "+str(center_y)+" "+str(start_x)+" "+str(start_y)+"\n")
            f.write(
                f"{image_name}-{str(c)}{extension} {str(center_x)} {str(center_y)} {str(start_x)} {str(start_y)}\n")  # test
            #break #only one crop image per image
            c+=1
