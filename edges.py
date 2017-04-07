import cv2
import numpy as np
from PIL import Image, ImageOps

############ Overlap image and segmentation ###############################

#Open images:

mask = cv2.imread('161.png')
orig = cv2.imread('161.jpg')

#Apply laplacian Algoritm to find edges:

laplacian = cv2.Laplacian(mask, cv2.CV_64F, ksize = 15)

#Save the edges image:

cv2.imwrite('Laplacian.png', laplacian)

laplacian=cv2.imread('Laplacian.png')


#Change the color of the edges:


for i in range(laplacian.shape[0]):
	for j in range(laplacian.shape[1]):
		if (laplacian[i][j]==[0,0,255]).all():
			laplacian[i][j]=[255,255,0]


#Overlap images: (output1 & 2 original+edge, output3 orig+completly mask)

output=cv2.addWeighted(orig,1,laplacian,1,0) #Edge
output2=cv2.addWeighted(orig,1,mask,0.6,0) #All

################ Draw Bboxes #####################################3

cv2.rectangle(output,(766,477),(938,735),(6,24,207),3)
cv2.rectangle(output,(115,90),(533,533),(6,24,207),3)
cv2.rectangle(output,(339,198),(696,768),(6,24,207),3)
cv2.rectangle(output,(832,55),(1023,564),(6,24,207),3)

cv2.rectangle(output2,(766,477),(938,735),(6,24,207),3)
cv2.rectangle(output2,(115,90),(533,533),(6,24,207),3)
cv2.rectangle(output2,(339,198),(696,768),(6,24,207),3)
cv2.rectangle(output2,(832,55),(1023,564),(6,24,207),3)

#Save the outputs:

cv2.imwrite('output.jpg',output)
cv2.imwrite('output2.jpg',output2)
