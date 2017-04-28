import numpy as np
import cv2
from matplotlib import pyplot as plt

imgL = cv2.imread('/home/poto/Escritorio/pruebas/depth/SuXT483.png', 0)
imgR = cv2.imread('/home/poto/Escritorio/pruebas/depth/Yeuna9x.png', 0)

list_dispar = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
list_block = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

b = 5  # Distance between cameras in cm
l = 5  # Focal length in cm

for i in list_dispar:
    for j in list_block:
        stereo = cv2.StereoBM_create(numDisparities=16 * i, blockSize=5 + 2 * j)
        disparity = stereo.compute(imgL, imgR)  # .astype(np.float32) / 16.0
        cv2.imwrite(
            '/home/poto/Escritorio/pruebas/depth/disparity_' + str(i * 16) + '_block_' + str(5 + 2 * j) + '.png',
            disparity)
        # threshold = cv2.threshold(disparity, 100, 255, cv2.THRESH_BINARY)[1]
        # print threshold
        # cv2.imwrite('/home/poto/Escritorio/pruebas/depth/threshold_'+str(i*16)+'_block_'+str(5+2*j)+'.png',threshold)

print len(disparity), len(disparity[0])
# print len(threshold),len(threshold[0])