import os
import shutil
from os import listdir, getcwd

train=open('ImageSets/Main/train.txt','r')
lista_train=train.readlines()

wd = getcwd()

if not os.path.exists(wd+'/Digits/'):
	os.mkdir(wd+'/Digits/')

if not os.path.exists(wd+'/Digits/train/'):
	os.mkdir(wd+'/Digits/train/')

if not os.path.exists(wd+'/Digits/train/images/'):
	os.mkdir(wd+'/Digits/train/images/')

if not os.path.exists(wd+'/Digits/train/labels/'):
	os.mkdir(wd+'/Digits/train/labels/')

if not os.path.exists(wd+'/Digits/val/'):
	os.mkdir(wd+'/Digits/val/')

if not os.path.exists(wd+'/Digits/val/images/'):
	os.mkdir(wd+'/Digits/val/images/')

if not os.path.exists(wd+'/Digits/val/labels/'):
	os.mkdir(wd+'/Digits/val/labels/')



for n in range(len(lista_train)):
	original_image_path = 'JPEGImages/'+lista_train[n].replace('\n','')+'.jpg'
	original_label_path = 'labelsKitti/'+lista_train[n].replace('\n','')+'.txt'
	final_image_path = wd+'/Digits/train/images/'+lista_train[n].replace('\n','')+'.jpg'
	final_label_path = wd+'/Digits/train/labels/'+lista_train[n].replace('\n','')+'.txt'
	shutil.copy(original_image_path, final_image_path)
	shutil.copy(original_label_path, final_label_path)	

train.close()

val = open('ImageSets/Main/val.txt','r')
lista_val = val.readlines()

for n in range(len(lista_val)):
	original_image_path = 'JPEGImages/'+lista_val[n].replace('\n','')+'.jpg'
	original_label_path = 'labelsKitti/'+lista_val[n].replace('\n','')+'.txt'
	final_image_path = wd+'/Digits/val/images/'+lista_val[n].replace('\n','')+'.jpg'
	final_label_path = wd+'/Digits/val/labels/'+lista_val[n].replace('\n','')+'.txt'
	shutil.copy(original_image_path, final_image_path)
	shutil.copy(original_label_path, final_label_path)	

val.close()
