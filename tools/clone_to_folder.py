from distutils.dir_util import copy_tree
import os

def clone_to_folder(src_dir,dst_dir):
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    
    src_dir = os.path.join(project_root,src_dir)
    dst_dir = os.path.join(project_root,dst_dir)
    
    copy_tree(src_dir, dst_dir)
    
    
    