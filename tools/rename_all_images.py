from glob import glob
import os

# this function renames all images in target to a sequential number starting from 0


def rename_all():
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    img_list = glob(project_root+"/temp_photos/target/*.*")
    with open(os.path.join(project_root, "filename_mapping.txt"), mode="w") as f:
        for i, path in enumerate(img_list):
            extension = os.path.splitext(os.path.basename(path))[1]
            f.write(f"{os.path.basename(path)} {str(i)+extension}\n")
            os.rename(path, project_root +
                      "/temp_photos/target/"+str(i)+extension)
if __name__ == "__main__":
    rename_all()
