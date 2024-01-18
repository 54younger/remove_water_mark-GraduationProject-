from PIL import Image, ImageDraw
import os
import cv2
from tqdm import tqdm
import shutil

def create_mask(path):
    file_count = 0
    os.makedirs(os.path.join(path, "mask"), exist_ok=True)
    for filename in tqdm(os.listdir(path)):
        if filename.endswith(".txt"):
            txt_filepath = os.path.join(path, filename)
            png_filename = os.path.splitext(filename)[0] + ".png"
            png_filepath = os.path.join(path, png_filename)
            mask_filepath = os.path.join(path, "mask", "mask_" + png_filename)
            if os.path.isfile(png_filepath):
                with open(txt_filepath, "r") as txt_file:
                    line = txt_file.readline().strip()
                    numbers = line.split(" ")
                    if len(numbers) == 6:
                        #获取照片宽高
                        img = cv2.imread(png_filepath)
                        height, width = img.shape[:2]

                        x_center = float(numbers[2]) * width
                        y_center = float(numbers[3]) * height
                        mask_width = float(numbers[4]) * width
                        mask_heigh = float(numbers[5]) * height

                        # 创建黑色背景图片
                        image = Image.new("RGB", (width, height), (0,0,0))
                        draw = ImageDraw.Draw(image)

                        x1 = (x_center - mask_width/2)
                        y1 = (y_center - mask_heigh/2)
                        x2 = (x_center + mask_width/2)
                        y2 = (y_center + mask_heigh/2)
                        draw.rectangle([(x1, y1), (x2, y2)], fill="white")

                        image.save(mask_filepath)
                        file_count += 1

def check(path):
    mask_path=os.path.join(path, "mask")
    #检查文件名编号是否一一对应
    for file in tqdm(os.listdir(path)):
        if file.endswith(".png"):
            png_filepath = os.path.join(path, file)
            mask_filename = "mask_" + file
            mask_filepath = os.path.join(mask_path, mask_filename)
            if os.path.isfile(mask_filepath):
                pass
            else:
                print("mask file not exist: ", mask_filepath)

def copy_and_rename_files(ori_dir, ori_mask_dir, tar_gir):
    file_num = 0
    for file in tqdm(os.listdir(ori_dir)):
        if file_num%50 == 0:
          if file.endswith(".jpg"):
              png_filepath = os.path.join(ori_dir, file)
              mask_filename = "mask_" + str(600000+file_num) + ".png"
              mask_filepath = os.path.join(ori_mask_dir, mask_filename)
              if os.path.isfile(mask_filepath):
                  shutil.copy(png_filepath, tar_gir)
                  shutil.copy(mask_filepath, tar_gir)
                  os.rename(os.path.join(tar_gir, file), os.path.join(tar_gir, "image" + str(int(file_num/50)) + ".png"))
                  os.rename(os.path.join(tar_gir, mask_filename), os.path.join(tar_gir, "image" + str(int(file_num/50)) + "_mask" + str('%03d' % (file_num/50)) + ".png"))
                  #print("copy and rename: ", file_num)
              else:
                  print("mask file not exist: ", mask_filepath)
        else:
            pass
        file_num += 1
if __name__ == '__main__':
    mask_path="./Large-scale_Visible_Watermark_Dataset/watermarked_images/train/mask"
    file_path="./Large-scale_Visible_Watermark_Dataset/original_images/train"
    #create_mask(file_path)
    #check(file_path)
    copy_and_rename_files(file_path, mask_path, "./lama/myown_dataset")
