
import os
import numpy as np

def calc_distance(feat1, feat2):
    distance = np.linalg.norm(feat1 - feat2)
    return distance

if __name__ == "__main__":

    import cv2
    import settings
    from reid_onnx_helper import ReidHelper
    
    helper = ReidHelper(settings.ReID)

    # BASE_FOLDER = "sample"
    BASE_FOLDER = "C:/Users/USER/Downloads/total_1000"

    feat1 = None
    min_distance = 0
    min_file = None
    
    #추가
    arr = {}

    files = os.listdir(BASE_FOLDER)
    for index, file in enumerate(files):
        file_path = os.path.join(BASE_FOLDER, file)
        car_img = cv2.imread(file_path)

        feat = helper.infer(car_img)
        if index == 0:
            feat1 = feat
        else:
            distance = calc_distance(feat1, feat)
            # print(file, distance)
            arr[file] = round(distance,8)

            if min_distance == 0 or min_distance > distance:
                min_distance = distance
                min_file = file
        print(index)

    image_rank = sorted(arr.items(), key=lambda x: x[1], reverse=False)

    print(image_rank[:20])
    # print("target_file:", files[0])
    # print("min_file:", min_file)


    #이미지 출력
    # arr[files[0]]='target_file'

    # import matplotlib.pyplot as plt
    # import glob

    # fig = plt.figure() # rows*cols 행렬의 i번째 subplot 생성
    # rows = 2
    # cols = 5
    # i = 1
    
    # #xlabels = ["xlabel", "(a)", "(b)", "(c)", "(d)"]
    
    # files = os.listdir(BASE_FOLDER)
    # for filename in files:
    #     file_path = os.path.join(BASE_FOLDER, filename)

    #     img = cv2.imread(file_path)
    #     ax = fig.add_subplot(rows, cols, i)
    #     ax.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #     ax.set_xlabel(arr[filename])
    #     ax.set_xticks([]), ax.set_yticks([])
    #     i += 1
    
    # plt.show()



