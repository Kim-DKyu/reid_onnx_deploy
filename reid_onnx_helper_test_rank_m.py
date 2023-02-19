import pandas as pd
from tqdm import tqdm
import cv2
import numpy as np
import settings
from reid_onnx_helper import ReidHelper

import time
import datetime # datetime 라이브러리 import

import os
import re
#pd.set_option('display.max_columns', None) ## 모든 열을 출력한다.
#pd.set_option('display.max_rows', None) ## 모든 열을 출력한다.

start = time.time() # 시작

def calc_distance(feat1, feat2):
    distance = np.linalg.norm(feat1 - feat2)
    return distance

helper = ReidHelper(settings.ReID)

df = pd.read_csv('C:/Users/USER/cp2/crop_data/car_info.csv')

df = df.astype({'yearId':'str'})
df['ClassId'] = df['LargeCategoryId'] +'_'+ df['MediumCategoryId'] +'_'+ df['SmallCategoryId'] +'_'+ df['yearId'] +'_'+ df['colorId']
df = df.drop('Unnamed: 0',axis=1)
df = df[['ClassId', 'LargeCategoryId', 'MediumCategoryId', 'SmallCategoryId', 'yearId', 'colorId', 'segment','file_name','file_path']]

df_front_and_back = df[df['colorId']=='흰색']
df_ = df_front_and_back.groupby('ClassId').apply(lambda group:group if len(group) > 1 else None).reset_index(drop=True)
query_df = df_.groupby("ClassId").first()
gallary_df = df_.groupby('ClassId').apply(lambda group:group.iloc[1:]).reset_index(drop=True)

rank1 = 0
rank5 = 0
rank10 = 0
i = 0 # 실제 클래스의 수

for cid, query in tqdm(query_df.iterrows(), total = query_df.shape[0]):
    #query_img = cv2.imread(query['file_path'])
    query_img_array = np.fromfile(query['file_path'], np.uint8)
    query_img = cv2.imdecode(query_img_array, cv2.IMREAD_COLOR)
    query_img_feat = helper.infer(query_img)

    gallary_similarity = []

    for _cid, gallary in gallary_df.groupby("ClassId").agg(pd.DataFrame.sample).iterrows():
        #gallary_img = cv2.imread(gallary['file_path'])
        gallary_img_array = np.fromfile(gallary['file_path'], np.uint8)
        gallary_img = cv2.imdecode(gallary_img_array, cv2.IMREAD_COLOR)

        gallary_img_feat = helper.infer(gallary_img)
        similarity = calc_distance(query_img_feat, gallary_img_feat)
        gallary_similarity.append(tuple([similarity, _cid]))
    
    gallary_similarity.sort()

    rank1 += 1 if list(filter(lambda x:x[1] == cid, gallary_similarity[:1])) else 0
    rank5 += 1 if list(filter(lambda x:x[1] == cid, gallary_similarity[:5])) else 0
    rank10 += 1 if list(filter(lambda x:x[1] == cid, gallary_similarity[:10])) else 0
    i+=1

# rank1 /= i
# rank5 /= i
# rank10 /= i

print(f'rank1:{rank1}/{i} persent:{rank1/i}')
print(f'rank5:{rank5}/{i} persent:{rank5/i}')
print(f'rank10:{rank10}/{i} persent:{rank10/i}')
# print(rank1, rank5, rank10)

sec = time.time()-start # 종료 - 시작 (걸린 시간)
times = str(datetime.timedelta(seconds=sec)) # 걸린시간 보기좋게 바꾸기
short = times.split(".")[0] # 초 단위 까지만

print(f"{short} sec")