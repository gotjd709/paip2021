from tqdm import tqdm
import numpy as np

import multiprocessing
import openslide
import glob, os
import cv2

# colon, pancreas
svs_col_path = glob.glob('./WSI/WSI_input/test_col_*/*.svs')
svs_pan_path = glob.glob('./WSI/WSI_input/test_pan_*/*.svs')
svs_path_list = svs_col_path + svs_pan_path

# prostate
svs_path_list_p = glob.glob('./WSI/WSI_input/test_pros_*/*.svs')

# radius
radius = 25

def json2mask(svs_path, radius, pros=False):
    json_path = './WSI/WSI_output/' + svs_path.split('/')[-1][:-4] + '/nuclei_dict.json'
    WSI_img = openslide.OpenSlide(svs_path)
    dims_level_0 = WSI_img.level_dimensions[0]
    mask_h = WSI_img.level_dimensions[0][1]
    mask_w = WSI_img.level_dimensions[0][0]
    mask = np.zeros((mask_h, mask_w))

    with open(json_path, 'r') as f:
        line = f.readline()
        num = line.count('centroid')
        sample = line.split(': {"centroid": ')
        if pros == False:
            for i in tqdm(range(num+1)):
                if (sample[i].rfind('"type": 1') != -1):
                    cell = [int(sample[i].split(',')[0][1:]), int(sample[i].split(',')[1][1:-1])]
                    cv2.circle(mask, (cell[0], cell[1]), radius, 1, cv2.FILLED)
                else:
                    pass
        elif pros == True:
            for i in tqdm(range(num+1)):
                if (sample[i].rfind('"type": 1') != -1) or (sample[i].rfind('"type": 4') != -1) or (sample[i].rfind('"type": 5') != -1):
                    cell = [int(sample[i].split(',')[0][1:]), int(sample[i].split(',')[1][1:-1])]
                    cv2.circle(mask, (cell[0], cell[1]), radius, 1, cv2.FILLED)
                else:
                    pass            
        cv2.imwrite('./WSI_mask/' + svs_path.split('/')[-1][:-4] + '.png', mask)

        
#### multiprocessing

if __name__=='__main__':
    for svs_path in svs_path_list:
        p = multiprocessing.Process(target=json2mask, args=(svs_path, radius, pros=False, ))
        p.start()
    for svs_path in svs_path_list_p:
        p = multiprocessing.Process(target=json2mask, args=(svs_path, radius, pros=True, ))
        p.start()
    

