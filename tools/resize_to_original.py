import cv2
from glob import glob
import os


def folder_resize_specified(resize_dir, ratio):
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    print(project_root+resize_dir+"/*.*")
    for path in glob(project_root+"/"+resize_dir+"/*.*"):
        print(f"filename={path}")

        img = cv2.imread(path)
        print(img.shape)
        if max(img.shape[0],img.shape[1])>1000:
            img = cv2.resize(img, dsize=(
                int(img.shape[1]*ratio), int(img.shape[0]*ratio)))
        cv2.imwrite(path, img)




def folder_resize(size_file_path, resize_dir):
    project_root = str(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    os.system(f"conda run -n anime python Real-ESRGAN/inference_realesrgan.py  --input {resize_dir} --output {resize_dir} --face_enhance")

    with open(os.path.join(project_root, size_file_path), mode='r') as f:
        for p in f.readlines():
            #p = p.strip()
            filename, width, height = p.split()
            print(
                f"filename={os.path.join(resize_dir,os.path.basename(filename))}")

            img = cv2.imread(os.path.join(
                resize_dir, os.path.basename(filename)))
            print(img.shape)
            img = cv2.resize(img, dsize=(int(width), int(height)))
            cv2.imwrite(os.path.join(
                resize_dir, os.path.basename(filename)), img)


def save_size(size_file_path, resize_dir):
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    with open(os.path.join(project_root, size_file_path), mode='w') as f:
        for path in glob(os.path.join(project_root, resize_dir)+"/*.*"):
            print(f"path={path}")
            img = cv2.imread(path)
            f.write(f"{path} {img.shape[1]} {img.shape[0]}\n")
