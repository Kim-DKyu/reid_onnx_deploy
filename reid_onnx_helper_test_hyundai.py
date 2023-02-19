
import os
import numpy as np

def calc_distance(feat1, feat2):
    distance = np.linalg.norm(feat1 - feat2)
    return distance

if __name__ == "__main__":

    import cv2
    import settings
    from reid_onnx_helper import ReidHelper
    import pandas as pd
    import tqdm

    helper = ReidHelper(settings.ReID)

    df = pd.read_csv("C:/Users/USER/cp2/yolov5/hyundai_car_info.csv")
    df = df.drop_duplicates(['file_name'], ignore_index = True)
    df = df.drop(['Unnamed: 0'], axis=1)

    # df_Sedan = df[df['Car_type']=='Sedan']
    # df_Sedan_H0_10 = df_Sedan[(df_Sedan['horizontal_angle']==0) & (df_Sedan['time']=='10')]
    # df_query = df_Sedan_H0_10[df_Sedan_H0_10['file_name']=='현대_소나타_2014_10시대_H0_V0.jpg']
    # df_gallery = df_Sedan_H0_10.drop(df_query.index)

    # df_SUV = df[df['Car_type']=='SUV']
    # df_SUV_H0_10 = df_SUV[(df_SUV['horizontal_angle']==0) & (df_SUV['time']=='10')]
    # df_query = df_SUV_H0_10[df_SUV_H0_10['file_name']=='현대_팰리세이드_2019_10시대_H0_V0.jpg']
    # df_gallery = df_SUV_H0_10.drop(df_query.index)

    # df_mid = df[df['Car_type']=='준중형차']
    # df_mid_H0_10 = df_mid[(df_mid['horizontal_angle']==0) & (df_mid['time']=='10')]
    # df_query = df_mid_H0_10[df_mid_H0_10['file_name']=='현대_벨로스터_2018_10시대_H0_V15.jpg']
    # df_gallery = df_mid_H0_10.drop(df_query.index)

    df_H0_10 = df[(df['horizontal_angle']==0) & (df['time']=='18')]
    df_query = df_H0_10[df_H0_10['file_name']=='현대_그랜저_2014_18시대_H0_V0.jpg']
    df_gallery = df_H0_10.drop(df_query.index)

    print(settings.ReID.MODEL_PATH)
    # vehicleid, veri, veriwild
    # 현대_G80스포츠_2017_10시대_H0_V0.jpg
    # 현대_G90_2018_10시대_H0_V0.jpg
    # 현대_아슬란_2015_10시대_H0_V0.jpg
    # 현대_에쿠스_2013_10시대_H0_V15.jpg
    # 현대_그랜저_2014_10시대_H0_V15.jpg
    # 현대_소나타_2014_10시대_H0_V0.jpg

    # 현대_맥스크루즈_2016_10시대_H0_V0.jpg
    # 현대_싼타페_2012_10시대_H0_V0.jpg
    # 현대_투싼_2007_10시대_H0_V0.jpg
    # 현대_팰리세이드_2019_10시대_H0_V0.jpg

    # 현대_i30_2017_10시대_H0_V0.jpg
    # 현대_벨로스터_2018_10시대_H0_V15.jpg
    # 현대_엑센트_2015_10시대_H0_V60.jpg

    query_img_array = np.fromfile(df_query['file_path'].values[0], np.uint8)
    query_car_img = cv2.imdecode(query_img_array, cv2.IMREAD_COLOR)
    feat1 = helper.infer(query_car_img)

    min_distance = 0
    min_file = None
    
    #추가
    arr = {}
    #arr[df_query['file_name'].values[0]]='target_file'

    for cid, query in df_gallery.iterrows():
        gallery_img_array = np.fromfile(query['file_path'], np.uint8)
        gallery_car_img = cv2.imdecode(gallery_img_array, cv2.IMREAD_COLOR)

        feat = helper.infer(gallery_car_img)
        
        distance = calc_distance(feat1, feat)
        # print(file, distance)
        arr[query['file_name']] = [round(distance,8),query['file_path']]

    image_rank = sorted(arr.items(), key=lambda x: x[1], reverse=False)
    image_rank = image_rank[:9] 
    image_rank.insert(0, (df_query['file_name'].values[0],['target_file',df_query['file_path'].values[0]]))
    # print(image_rank[0][0]) #현대_G80스포츠_2017_10시대_H0_V0.jpg
    # print(image_rank[0][1][0]) #target_file
    # print(image_rank[0][1][1]) #path
    # print("target_file:", files[0])
    # print("min_file:", min_file)

    #print(len(image_rank))
    #이미지 출력
    # arr[files[0]]='target_file'

    import matplotlib.pyplot as plt
    import glob
    plt.rc('font', family='Malgun Gothic')

    fig = plt.figure() # rows*cols 행렬의 i번째 subplot 생성
    rows = 2
    cols = 5
    i = 1

    for index in range(len(image_rank)):
        # img = cv2.imread(list[index][1][1])
        # print(index)
        img_array = np.fromfile(image_rank[index][1][1], np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)

        ax = fig.add_subplot(rows, cols, i)
        ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))

        str = f'{image_rank[index][1][0]}\n{image_rank[index][0]}'
        ax.set_xlabel(str)
        ax.set_xticks([]), ax.set_yticks([])
        ax.xaxis.label.set_size(10)
        i += 1
    
    plt.show()



