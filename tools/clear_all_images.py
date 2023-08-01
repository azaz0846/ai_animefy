import os
import shutil
import glob

def clear_all():
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    try:
        shutil.rmtree(project_root+'/temp_photos')
    except:
        pass
    os.mkdir(project_root + '/temp_photos')
    os.mkdir(project_root+'/temp_photos/anime_background')
    os.mkdir(project_root+'/temp_photos/anime_background/genshin')
    os.mkdir(project_root+'/temp_photos/anime_background/borderland')
    os.mkdir(project_root+'/temp_photos/anime_background/shinchan')
    os.mkdir(project_root+'/temp_photos/anime_body')
    os.mkdir(project_root+'/temp_photos/anime_face')
    os.mkdir(project_root+'/temp_photos/mask')
    os.mkdir(project_root+'/temp_photos/mask/body')
    os.mkdir(project_root+'/temp_photos/mask/face')
    os.mkdir(project_root+'/temp_photos/target')
    os.mkdir(project_root+'/temp_photos/target/edge')
    os.mkdir(project_root+'/temp_photos/crop')
    os.mkdir(project_root+'/temp_photos/crop/body')
    os.mkdir(project_root+'/temp_photos/crop/face')
    os.mkdir(project_root+'/temp_photos/result')
    os.mkdir(project_root+'/temp_photos/merged_body_anime_face')
    print("All images have been cleared!")



def save_and_clear_all_images():
    # do not modify
    project_root = str(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))

    # copies result to outside and rename to original name
    """
    try:
        with open(os.path.join(project_root, "filename_mapping.txt"), mode="r") as f:
            for line in f.readlines():
                origin_name, new_name = line.strip().split()
                shutil.move(os.path.join(
                    project_root, "temp_photos/result/"+new_name), os.path.join(
                    project_root, "result/"+origin_name))
                print(
                    f"Move {os.path.join(project_root, 'temp_photos/result/'+new_name)} to ||{os.path.join(project_root, 'result/'+origin_name)} | |")

        print("Successfully move all results to outside and rename")
    except:
        pass
    """
    paths = glob.glob(project_root+"/temp_photos/result/*.*")
    for path in paths:
        shutil.move(path, os.path.join(
                    project_root, "result/"+os.path.basename(path)))

    clear_all()
if __name__ =="__main__":
    clear_all()
    
