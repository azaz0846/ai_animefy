import cv2
import os
import numpy as np
import shutil
from glob import glob
from tqdm import tqdm


def merge_image_from_dir(position_file_path, main_dir, sub_dir, mask_dir, save_dir, body_position_file_path=None):
    """warning: the images in the main folder WILL be changed"""
    # change from relative path
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    position_file_path = os.path.join(project_root, position_file_path)
    if body_position_file_path is not None:
        body_position_file_path = os.path.join(
            project_root, body_position_file_path)
    main_dir = os.path.join(project_root, main_dir)
    sub_dir = os.path.join(project_root, sub_dir)
    mask_dir = os.path.join(project_root, mask_dir)
    save_dir = os.path.join(project_root, save_dir)
    print(f"main_dir={main_dir}")
    print(f"sub_dir={sub_dir}")
    print(f"mask_dir={mask_dir}")
    print(f"save_dir={save_dir}")

    # move all main images to save folder to process
    for path in glob(os.path.join(main_dir, "*.*")):
        shutil.copy(path, save_dir)

    with open(position_file_path) as f:
        for sub_info in tqdm(f.readlines()):
            sub_info = sub_info.strip()
            try:
                sub_name, center_x, center_y = sub_info.split()
            except:
                sub_name, center_x, center_y, not_used1, not_used2 = sub_info.split()
            center_x = int(center_x)
            center_y = int(center_y)
            if body_position_file_path is not None:
                with open(body_position_file_path) as f2:
                    for body_sub_info in f2.readlines():
                        body_sub_info = body_sub_info.strip()
                        b_sub_name, b_center_x, b_center_y, b_start_x, b_start_y = body_sub_info.split()
                        if sub_name == b_sub_name:
                            center_x -= int(b_start_x)
                            center_y -= int(b_start_y)
                            break

            # read images
            sub_img = cv2.imread(os.path.join(sub_dir, sub_name))
            mask_img = cv2.imread(os.path.join(mask_dir, sub_name))

            # try to find correspond main image
            main_name = sub_name
            main_img = cv2.imread(os.path.join(save_dir, main_name))
            print(os.path.join(save_dir, main_name))
            if main_img is None:
                start = sub_name.find("-")
                end = sub_name.find(".")
                filename = sub_name[:start]
                extension = sub_name[end:]
                main_name2 = filename + extension
                main_img = cv2.imread(os.path.join(save_dir, main_name2))
                main_name=main_name2
                print(os.path.join(save_dir, main_name2))
                if main_img is None:
                    print(
                        f"Error: image:{sub_name} cannot find correspond main image to merge.")
                    print(
                        f"tried:{os.path.join(save_dir, main_name)},{os.path.join(save_dir, main_name2)}\n")
                    continue

            #merge and save
            result = merge_image(
                main_img, sub_img, mask_img, center_x, center_y)
            if result is not None:
                cv2.imwrite(os.path.join(save_dir, main_name), result)
                print(f"Successfully merged:{os.path.join(save_dir, main_name)}")
            else:
                print(f"failed file:{os.path.join(sub_dir, sub_name)}")


def correct_center(main,mask, center):
    mask_flat = mask[:, :, 0]
    mask_x = np.sum(mask_flat, axis=0)
    mask_y = np.sum(mask_flat, axis=1)
    x_min = np.min(np.nonzero(mask_x))
    x_max = np.max(np.nonzero(mask_x))
    y_min = np.min(np.nonzero(mask_y))
    y_max = np.max(np.nonzero(mask_y))
    h, w, c = mask.shape
    obj_w = x_max-x_min
    obj_h = y_max-y_min
    center_x = center[0]+(x_min - w + x_max)/2
    center_y = center[1]+(y_min - h + y_max)/2
    h,w,c = main.shape
    if center_x-obj_w/2<=0:
        center_x = obj_w/2
    if center_y-obj_h/2<=0:
        center_y = obj_h/2
    if center_x+obj_w/2>=w:
        center_x = w-obj_w/2
    if center_y+obj_h/2>=h:
        center_y = h-obj_h/2
    return (int(center_x), int(center_y))

def check_boundary(main,mask,center):
    mask_flat = mask[:, :, 0]
    mask_x = np.sum(mask_flat, axis=0)
    mask_y = np.sum(mask_flat, axis=1)
    x_min = np.min(np.nonzero(mask_x))
    x_max = np.max(np.nonzero(mask_x))
    y_min = np.min(np.nonzero(mask_y))
    y_max = np.max(np.nonzero(mask_y))
    obj_w = x_max-x_min
    obj_h = y_max-y_min
    h, w, c = main.shape
    center_x,center_y = center
    print(f"object size: w:{obj_w},h:{obj_h}")
    
    print(f"center_x:{center_x} + obj_w/2:{obj_w/2} > w:{w}")
    
    print(f"center_y:{center_y} + obj_h/2:{obj_h/2} > h:{h}")

    print(f"center_x:{center_x} - obj_w/2:{obj_w/2} < 0")

    print(f"center_y:{center_y} - obj_h/2:{obj_h/2} < 0")
    return obj_w,obj_h

def merge_image(main, sub, sub_mask, center_x, center_y):
    
    sub_mask = cv2.resize(
        sub_mask, (int(sub.shape[1])-2, int(sub.shape[0])-2), interpolation=cv2.INTER_NEAREST)
    sub = cv2.resize(
        sub, (int(sub.shape[1])-2, int(sub.shape[0])-2), interpolation=cv2.INTER_NEAREST)
    center=(center_x,center_y)
    print("center:")
    print(center)
    center = correct_center(main,sub_mask, (center_x, center_y))
    print(center)
    obj_w,obj_h = check_boundary(main,sub_mask,center)
    #cv2.rectangle(main, (center[0]-obj_w//2,center[1]-obj_h//2), (center[0]+obj_w//2,center[1]+obj_h//2), (0, 255, 0), 2)
    #return main
    h,w,c = main.shape
    #main = cv2.copyMakeBorder(main, 20,20,20,20, cv2.BORDER_CONSTANT, value=[255, 255,255])
    #center = (center[0]+20,center[1]+20)
    #cv2.rectangle(main, (center[0]-obj_w//2,center[1]-obj_h//2), (center[0]+obj_w//2,center[1]+obj_h//2), (0, 255, 0), 2)
    """
    print(main.shape)
    main_blur = cv2.GaussianBlur(main, (13, 13), sigmaX=5)
    mask_mainsize = np.zeros_like(main)
    print("mask_mainsize:")
    if center_x - sub_mask.shape[1]//2<0:
        center_x = sub_mask.shape[1]//2
    if center_y - sub_mask.shape[0]//2<0:
        center_y = sub_mask.shape[0]//2
    print(int(center_y-sub_mask.shape[0]//2))
    print(int(center_y-sub_mask.shape[0]//2)+sub_mask.shape[0])
    mask_mainsize[int(center_y-sub_mask.shape[0]//2):int(center_y-sub_mask.shape[0]//2)+sub_mask.shape[0] ,int(center_x-sub_mask.shape[1]//2):int(center_x-sub_mask.shape[1]//2)+sub_mask.shape[1], : ]=sub_mask
    main[np.where(mask_mainsize!=0)] = main_blur[np.where(mask_mainsize!=0)]
    print(main.shape)
    """
    try:
        #img_clone = main
        img_clone = cv2.seamlessClone(
        sub, main, sub_mask, center, cv2.NORMAL_CLONE)
        return img_clone#[20:h-19,20:w-19,:]
    except:
        print(f"merge failed:\nmain:{main.shape}\nsub:{sub.shape}\nmask:{sub_mask.shape}\ncenter:{center}")
        return None
