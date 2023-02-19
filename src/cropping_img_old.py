from PIL import Image
import json
import os


# LABEL_BASE_FOLDER = 'C:/Users/USER/cp2/test/라벨링/2017_빨강_트림A'
# IMAGE_BASE_FOLDER = 'C:/Users/USER/cp2/test/원천/2017_빨강_트림A'
# label_file_path = os.listdir(LABEL_BASE_FOLDER)
# image_file_path = os.listdir(IMAGE_BASE_FOLDER)

def extract_bbox_info(path):
    label_list = os.listdir(path)
    bbox_arr = {}
    for file in label_list:
        split_t_name = file.split('_')
        if split_t_name[7]=='T':
            split_jpg_name = file.split('.')
            
            with open(path+'/'+file, "r", encoding='UTF8') as st_json:
                st_python = json.load(st_json)
            
            for i in range(len(st_python['learningDataInfo']['objects'])):
                if st_python['learningDataInfo']['objects'][i]['classId'] == 'P00.차량전체':
                    left = st_python['learningDataInfo']['objects'][i]['left']
                    top = st_python['learningDataInfo']['objects'][i]['top']
                    width = st_python['learningDataInfo']['objects'][i]['width']
                    height = st_python['learningDataInfo']['objects'][i]['height']
                    bbox_arr[split_jpg_name[0]+'.jpg']=[left,top,left+width,top+height]
    
    return path, bbox_arr

def cropping_image(path, bbox_arr):
    IMAGE_BASE_FOLDER = 'C:/Users/USER/Downloads/091.차량 외관 영상 데이터/01.데이터/2.Validation/원천데이터/'
    path = path.split('/')
    image_path = IMAGE_BASE_FOLDER+'/'.join(path[8:])
    image_list = os.listdir(image_path)
    crop_image_save_path = 'C:/Users/USER/Downloads/total/'

    for file in image_list:
        if file in bbox_arr:
            image_path_indiv = image_path+'/'+file
            img_origin = Image.open(image_path_indiv)
            img_cropped = img_origin.crop((bbox_arr[file][0], bbox_arr[file][1], bbox_arr[file][2], bbox_arr[file][3]))

            if os.path.exists(crop_image_save_path):
                img_cropped.save(crop_image_save_path+'/'+file, 'JPEG')
                print(f"save crop image path : {crop_image_save_path+'/'+file}")
            else:
                os.makedirs(crop_image_save_path)
                img_cropped.save(crop_image_save_path+'/'+file, 'JPEG')
                print(f"save crop image path : {crop_image_save_path+'/'+file}")

            image_path_indiv = image_path

array = {
            'VL1' : ['AU_아우디','BE_벤츠','BM_BMW','CH_쉐보레','FO_포드','GE_제네시스','HO_혼다'],
            'VL2' : ['HY_현대','JE_지프','KG_한국지엠'],
            'VL3' : ['KI_기아','LA_랜드로버','LE_렉서스','MI_미니','NI_닛산'],
            'VL4' : ['RE_르노','RS_르노삼성','SS_쌍용','TO_토요타','VO_폭스바겐','VV_볼보']
}

root_path = 'C:/Users/USER/Downloads/091.차량 외관 영상 데이터/01.데이터/2.Validation/라벨링데이터/'

for index, (key, value) in enumerate(array.items()):
    for j in range(len(array[key])):
        car_path = root_path+key+'/'+array[key][j]
        list_car_series = os.listdir(car_path)
        
        for k in range(len(list_car_series)):
            car_series_path = car_path +'/'+ list_car_series[k]
            list_car_color = os.listdir(car_series_path)
            
            for i in range(len(list_car_color)):
                car_color_path = car_series_path +'/'+ list_car_color[i]
                path, bbox_arr = extract_bbox_info(car_color_path)
                cropping_image(path, bbox_arr)
                car_color_path = car_series_path
            car_series_path = car_path
        car_path = root_path