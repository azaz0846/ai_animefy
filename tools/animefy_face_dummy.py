import shutil
import os
from glob import glob
import cv2


def dummy_animefy_face(src_dir, dst_dir):
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    src_dir = os.path.join(project_root, src_dir)
    dst_dir = os.path.join(project_root, dst_dir)
    for path in glob(os.path.join(src_dir,"*.*")):
        # animefy here
        shutil.copy(path,dst_dir)
        print(f"Copied to:{os.path.join(dst_dir, os.path.basename(path))}")
