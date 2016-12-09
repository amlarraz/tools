import os
from os import listdir, getcwd
import shutil

wd = getcwd()

#We create the directoris to store the data:

if not os.path.exists(wd+'/PERSON/'):
	os.mkdir(wd+'/PERSON/')

if not os.path.exists(wd+'/PERSON/JPEGImages'):
	os.mkdir(wd+'/PERSON/JPEGImages')

if not os.path.exists(wd+'/PERSON/Annotations'):
	os.mkdir(wd+'/PERSON/Annotations')

#Open the first file with the names of the archives:

train=open('ImageSets/Main/person_train.txt')

lista_train = train.readlines()

for n in range(len(lista_train)):

	if lista_train[n][12:14] != '-1':

		original_image_path = 'JPEGImages/'+lista_train[n][0:11].replace('\n','')+'.jpg'
		original_label_path = 'Annotations/'+lista_train[n][0:11].replace('\n','')+'.xml'
		final_image_path = 'PERSON/JPEGImages/'+lista_train[n][0:11].replace('\n','')+'.jpg'
		final_label_path = 'PERSON/Annotations/'+lista_train[n][0:11].replace('\n','')+'.xml'
		shutil.copy(original_image_path, final_image_path)
		shutil.copy(original_label_path, final_label_path)	

#Second archive:

train_val=open('ImageSets/Main/person_trainval.txt')

lista_train_val = train_val.readlines()

for n in range(len(lista_train_val)):

	if lista_train_val[n][12:14] != '-1':

		original_image_path = 'JPEGImages/'+lista_train_val[n][0:11].replace('\n','')+'.jpg'
		original_label_path = 'Annotations/'+lista_train_val[n][0:11].replace('\n','')+'.xml'
		final_image_path = 'PERSON/JPEGImages/'+lista_train_val[n][0:11].replace('\n','')+'.jpg'
		final_label_path = 'PERSON/Annotations/'+lista_train_val[n][0:11].replace('\n','')+'.xml'
		shutil.copy(original_image_path, final_image_path)
		shutil.copy(original_label_path, final_label_path)

#Third archive:

val=open('ImageSets/Main/person_val.txt')

lista_val = val.readlines()

for n in range(len(lista_val)):

	if lista_val[n][12:14] != '-1':

		original_image_path = 'JPEGImages/'+lista_val[n][0:11].replace('\n','')+'.jpg'
		original_label_path = 'Annotations/'+lista_val[n][0:11].replace('\n','')+'.xml'
		final_image_path = 'PERSON/JPEGImages/'+lista_val[n][0:11].replace('\n','')+'.jpg'
		final_label_path = 'PERSON/Annotations/'+lista_val[n][0:11].replace('\n','')+'.xml'
		shutil.copy(original_image_path, final_image_path)
		shutil.copy(original_label_path, final_label_path)

