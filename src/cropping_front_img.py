from PIL import Image
import json
import os
import glob
import pandas as pd

def crop_image(st_python, origin_path_image, new_file_path_base, new_file_path_mid, file_name):
    for i in range(len(st_python['learningDataInfo']['objects'])):
        if st_python['learningDataInfo']['objects'][i]['classId'] == 'P00.차량전체':
            left = st_python['learningDataInfo']['objects'][i]['left']
            top = st_python['learningDataInfo']['objects'][i]['top']
            width = st_python['learningDataInfo']['objects'][i]['width']
            height = st_python['learningDataInfo']['objects'][i]['height']

            img_origin = Image.open(origin_path_image)
            img_cropped = img_origin.crop((left, top, left+width, top+height))

            if os.path.exists(new_file_path_base+new_file_path_mid):
                img_cropped.save(new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg', 'JPEG')
                print(f"save crop image path : {new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg'}")
            else:
                os.makedirs(new_file_path_base+new_file_path_mid)
                img_cropped.save(new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg', 'JPEG')
                print(f"save crop image path : {new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg'}")

output = glob.glob('C:/Users/USER/cp2/integrated_data/*/*/*/*/*')

'C:/Users/USER/cp2/integrated_data\\VS4\\VV_볼보\\095_XC60\\2019_회색_트림\\C_211104_VV_095_19_GR_A_T_03_005.jpg'
for full_file_path in output:
    index = 0
    data = {}
    list = []

    full_file_name = full_file_path.split('\\')[-1]
    file_name = full_file_name.split('.')[0]
    file_ext = full_file_name.split('.')[1]
    
    if file_ext=='json':
        origin_path = full_file_path.split('\\')[:-1]
        origin_path_image = '/'.join(origin_path)+'/'+file_name+'.jpg'
        #print(origin_path_image)
        
        new_file_path = full_file_path.split('\\')
        new_file_path.pop()
        new_file_path = new_file_path[1:]

        with open(full_file_path, "r", encoding='UTF8') as st_json:
            st_python = json.load(st_json)

        for i in range(len(st_python['learningDataInfo']['objects'])):
            list.append(st_python['learningDataInfo']['objects'][i]['classId'])
        
        if list.count('P03.타이어(휠)')<=1:
            new_file_path_base = 'C:/Users/USER/cp2/crop_front_data/'
            new_file_path_mid = '/'.join(new_file_path) # VS1/AU_아우디/006_A4/2017_검정_트림
            crop_image(st_python, origin_path_image, new_file_path_base, new_file_path_mid, file_name)
        else:
            new_file_path_base = 'C:/Users/USER/cp2/crop_side_data/'
            new_file_path_mid = '/'.join(new_file_path) # VS1/AU_아우디/006_A4/2017_검정_트림
            crop_image(st_python, origin_path_image, new_file_path_base, new_file_path_mid, file_name)