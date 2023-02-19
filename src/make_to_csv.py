import json
import os
import glob
import pandas as pd

output = glob.glob('C:/Users/USER/cp2/crop_data/*/*/*/*/*')

'C:/Users/USER/cp2/integrated_data\\VS4\\VV_볼보\\095_XC60\\2019_회색_트림\\C_211104_VV_095_19_GR_A_T_03_005.jpg'
index = 0
data = {}
list = []

for full_file_path in output:
    full_file_name = full_file_path.split('\\')[-1]
    file_name = full_file_name.split('.')[0]
    file_ext = full_file_name.split('.')[1]

    if file_ext=='json':
        new_file_path = full_file_path.split('\\')
        new_file_path.pop()
        new_file_path = new_file_path[1:]

        new_file_path_base = 'C:/Users/USER/cp2/crop_data/'
        new_file_path_mid = '/'.join(new_file_path) # VS1/AU_아우디/006_A4/2017_검정_트림

        with open(full_file_path, "r", encoding='UTF8') as st_json:
            st_python = json.load(st_json)
        
        for i in range(len(st_python['learningDataInfo']['objects'])):
            list.append(st_python['learningDataInfo']['objects'][i]['classId'])

        if list.count('P03.타이어(휠)')<=1:
            if index==0:
                data['LargeCategoryId'] = [st_python['rawDataInfo']['LargeCategoryId']]
                data['MediumCategoryId'] = [st_python['rawDataInfo']['MediumCategoryId']]
                data['SmallCategoryId'] = [st_python['rawDataInfo']['SmallCategoryId']]
                data['yearId'] = [st_python['rawDataInfo']['yearId']]
                data['colorId'] = [st_python['rawDataInfo']['colorId']]
                data['segment'] = ['front_and_back']
                data['file_name'] = [file_name+".jpg"]
                data['file_path'] = [new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg']
            else:
                data['LargeCategoryId'].append(st_python['rawDataInfo']['LargeCategoryId'])
                data['MediumCategoryId'].append(st_python['rawDataInfo']['MediumCategoryId'])
                data['SmallCategoryId'].append(st_python['rawDataInfo']['SmallCategoryId'])
                data['yearId'].append(st_python['rawDataInfo']['yearId'])
                data['colorId'].append(st_python['rawDataInfo']['colorId'])
                data['segment'].append('front_and_back')
                data['file_name'].append(file_name+".jpg")
                data['file_path'].append(new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg')
            index+=1
        else:
            if index==0:
                data['LargeCategoryId'] = [st_python['rawDataInfo']['LargeCategoryId']]
                data['MediumCategoryId'] = [st_python['rawDataInfo']['MediumCategoryId']]
                data['SmallCategoryId'] = [st_python['rawDataInfo']['SmallCategoryId']]
                data['yearId'] = [st_python['rawDataInfo']['yearId']]
                data['colorId'] = [st_python['rawDataInfo']['colorId']]
                data['segment'] = ['side']
                data['file_name'] = [file_name+".jpg"]
                data['file_path'] = [new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg']
            else:
                data['LargeCategoryId'].append(st_python['rawDataInfo']['LargeCategoryId'])
                data['MediumCategoryId'].append(st_python['rawDataInfo']['MediumCategoryId'])
                data['SmallCategoryId'].append(st_python['rawDataInfo']['SmallCategoryId'])
                data['yearId'].append(st_python['rawDataInfo']['yearId'])
                data['colorId'].append(st_python['rawDataInfo']['colorId'])
                data['segment'].append('side')
                data['file_name'].append(file_name+".jpg")
                data['file_path'].append(new_file_path_base+new_file_path_mid+'/'+file_name+'.jpg')
            index+=1
        
        list = []

df = pd.DataFrame(data)
df.to_csv("C:/Users/USER/cp2/crop_data/car_info.csv")