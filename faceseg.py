import face_recognition
import os
import cv2
import argparse
from tqdm import tqdm
from glob import glob


def main():
    project_root = project_root = str(
        os.path.dirname(os.path.abspath(__file__)))
    data_folder = project_root + "/temp_photos/crop/face/"
    batch_size = 1
    pretrained = project_root+"/face-seg/checkpoints/model.pt"
    mask_type = 'hf'
    output_dir = project_root + "/temp_photos/mask/face/"

    path = project_root + "/temp_photos/target/*.*"
    with open(project_root+"/temp_photos/face_crop_position.txt", mode='w') as f:
        for image_path in tqdm(glob(path)):
            cv2img = cv2.imread(image_path)
            cv2.destroyAllWindows()
            image = face_recognition.load_image_file(image_path)
            face_locations = face_recognition.face_locations(image)
            image_name, extension = os.path.splitext(
                os.path.basename(image_path))
            face_locations.sort(key=lambda x:x[3]-int((x[1]-x[3])*0.5))
            for i, face in enumerate(face_locations):
                y = face[0]-int((face[2]-face[0])*0.5)
                yi = face[2]+int((face[2]-face[0])*0.5)
                x = face[3]-int((face[1]-face[3])*0.5)
                xi = face[1]+int((face[1]-face[3])*0.5)
                if y < 0:
                    y = 0
                if yi < 0:
                    yi = 0
                if x < 0:
                    x = 0
                if xi < 0:
                    xi = 0
                crop_img = cv2img[y:yi, x:xi]
                if crop_img.shape[0]*crop_img.shape[1]<70*70:
                    continue
                center_x = (x+xi)//2
                center_y = (y+yi)//2
                #print("!!!"+image_path, ':', i, '- ', [y, yi, x, xi])
                #print("!!!"+str(image.shape[0]) + str(image.shape[1]))
                cv2.imwrite(project_root+"/temp_photos/crop/face/" +
                            image_name+'-'+str(i)+extension, crop_img)
                f.write(
                    f"{image_name}-{str(i)}{extension} {str(center_x)} {str(center_y)}\n")

    cmd = "conda run -n anime python ./face-seg/test.py --data-folder "+data_folder + \
        " --batch-size "+str(batch_size)+" --pre-trained " + \
        pretrained+" --mask-type "+mask_type+" --output_dir "+output_dir
    print(cmd)
    os.system(cmd)


if __name__ == '__main__':
    main()
