import os
from tools.rename_all_images import rename_all
from tools.clear_all_images import save_and_clear_all_images
from tools.seamless_clone import merge_image_from_dir
from tools.animefy_face_dummy import dummy_animefy_face
from tools.resize_to_original import folder_resize,save_size,folder_resize_specified
from tools.clone_to_folder import clone_to_folder
import time


def main():
    
    t = time.time()
    style_name ="genshin"#"genshin"#"shinchan"#"borderland"
    edge_enhance = "0"

    # step1 rename all
    #rename_all()
    #time.sleep(5)

    # step2 animefy background
    save_size("temp_photos/target_size.txt","temp_photos/target")
    os.system(
        f"python animefy_background.py --style_name {style_name} --if_edge_enhancement {edge_enhance}")
    #time.sleep(5)
    folder_resize("temp_photos/target_size.txt",f"temp_photos/anime_background/{style_name}")
    
    # step3 rcnn crop body
    os.system("python rcnn.py")
    #time.sleep(5)

    
    # step4 faceseg crop face
    os.system("python faceseg.py")
    #time.sleep(5)


    # step5 animefy face

    save_size("temp_photos/crop_face_size.txt","temp_photos/crop/face")
    os.system("conda run -n ugatit python UGATIT/main.py --phase test --dataset temp_photos/crop/face --result_dir temp_photos/anime_face")
    folder_resize("temp_photos/crop_face_size.txt","temp_photos/anime_face")

    # step6(original 7) animefy body

    save_size("temp_photos/crop_body_size.txt","temp_photos/crop/body")
    os.system("conda run -n ugatit python UGATIT/main.py --phase test --dataset temp_photos/crop/body --result_dir temp_photos/anime_body")
    folder_resize("temp_photos/crop_body_size.txt","temp_photos/anime_body")


    # step7(original 6) merge face and body
    merge_image_from_dir(position_file_path="temp_photos/face_crop_position.txt",
                         body_position_file_path="temp_photos/body_crop_position.txt",
                         main_dir="temp_photos/anime_body",
                         sub_dir="temp_photos/anime_face",
                         mask_dir="temp_photos/mask/face",
                         save_dir="temp_photos/merged_body_anime_face")
    time.sleep(5)





    # step8 merge body and background
    merge_image_from_dir(position_file_path="temp_photos/body_crop_position.txt",
                         main_dir="temp_photos/anime_background/"+style_name,
                         sub_dir="temp_photos/merged_body_anime_face",
                         mask_dir="temp_photos/mask/body",
                         save_dir="temp_photos/result")
    #time.sleep(5)


    
    #time.sleep(5)
    
    
    #step5 upsampling using Real-ESRGAN
    folder_resize_specified("temp_photos/result",ratio=0.25)
    os.system(f"conda run -n anime python Real-ESRGAN/inference_realesrgan.py  --input temp_photos/result --output temp_photos/result --face_enhance ")
    folder_resize("temp_photos/target_size.txt",f"temp_photos/result")

    # step6 save to result and clear all temp photo
    save_and_clear_all_images()

    print("Successfully animefied! Terminating...")
    print(f"total time taken:{time.time()-t}s")
    return

    
if __name__ == "__main__":
    main()
