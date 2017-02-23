# -*- coding: utf-8

import os
import numpy as np
import scipy.io as io
import cv2
from PIL import Image, ImageOps
import ImageDraw

#Create the directory to storage the inferences:

wd = os.getcwd()

if not os.path.exists(wd+'/nectarines/inferences/'):
	
	os.mkdir(wd+'/nectarines/inferences/')

#Read the test names from test_id.txt:

test_id = open('nectarines/list/test_id.txt','r')

list_test = test_id.readlines()

test_id.close()

#Open the necesary files:

for i in range(len(list_test)):
	
	#Open .mat file obtanied in the inference:

	inFile = io.loadmat('nectarines/features/vgg16/test/fc8/'+list_test[i].replace('\n','')+'_blob_0.mat',mat_dtype=True, squeeze_me=True, struct_as_record=False) 
		
	data = np.asarray(inFile['data'],np.uint8) #Extract the image data Matrix from .mat file

	#Mask transformations (flip horizontally and rotate 90 degrees)
	
	data = np.rot90(cv2.flip(data,1))
	
	print 'Data shape: ', data.shape
	
	#Open original image:
	
	orig = np.asarray(Image.open('/home/poto/Escritorio/DATASETS/NECTARINES/test/'+list_test[i].replace('\n','')+'.jpg')) 
	
	print 'Orig shape: ', orig.shape
	
	#Crop Mask to adjust with the original:
	
	if data.shape[0] > orig.shape[0]:
		data = data[:orig.shape[0],:]

	if data.shape[1] > orig.shape[1]:
		data = data[:,:orig.shape[1]]
	
	#Crop original to adjust with the Mask:
	
	orig_aux = orig
	
	if orig_aux.shape[0] > data.shape[0]:
		m = (orig.shape[0]-data.shape[0])/2
		orig_aux = orig_aux[m:orig_aux.shape[0]-m,:,:]
		
	if orig_aux.shape[1] > data.shape[1]:
		m = (orig.shape[1]-data.shape[1])/2
		orig_aux = orig_aux[:,m:orig_aux.shape[1]-m,:]	
	
	orig_aux_image = Image.fromarray(orig_aux)
	orig_aux_image.save(wd+'/nectarines/inferences/'+list_test[i].replace('\n','')+'_originalCrop.jpg')

	#Create the image original overlay the inference:
	
	mask = Image.fromarray(data[:,:,1])
	data_image = Image.fromarray(data)
	orig_image = Image.fromarray(orig)
	
	new1 = Image.new('RGBA', size=(orig_aux.shape[1], orig_aux.shape[0]), color=(0, 0, 0, 0))
	new1.paste(orig_aux_image,(0,0))

	new2 = Image.new('RGBA', size=(orig_aux.shape[1], orig_aux.shape[0]), color=(0, 0, 0, 0))
	new2.paste(mask,(0,0))
	
	output=cv2.addWeighted(np.asarray(new1),1,np.asarray(new2),1,0)
	output = Image.fromarray(output)	
	
	#Save all:
	
	data_image.save(wd+'/nectarines/inferences/'+list_test[i].replace('\n','')+'_inference.png')
	orig_image.save(wd+'/nectarines/inferences/'+list_test[i].replace('\n','')+'_original.jpg')
	orig_aux_image.save(wd+'/nectarines/inferences/'+list_test[i].replace('\n','')+'_output.png')
	output.save(wd+'/nectarines/inferences/'+list_test[i].replace('\n','')+'_output.png')

print 'Felicidades, ha terminado la inferencia'
