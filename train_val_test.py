# -*- coding: utf-8

import os
from os import listdir, getcwd
import random
#import numpy as np

wd = getcwd()

lista = os.walk(wd+'/JPEGImages/')

size_train =int(input('¿Qué porcentaje le das al train?: '))*0.01

size_val = int(input('¿Qué porcentaje la das a la validación?: '))*0.01

print 'El resto se asignará automáticamente al conjunto de test.'
size_test = 1-(size_train + size_val)

if not os.path.exists(wd+'/ImageSets/'):
	os.mkdir(wd+'/ImageSets/')
	os.mkdir(wd+'/ImageSets/Main/')

for root, dirs, files in lista:
	
	random.shuffle(files)
	#Aquí cambia los porcentajes por aquellos que quieras, 
 	#es decir, el 0.6, 0.4 y 0
	#print random.shuffle(aleat)
	len_train_temp = int(len(files)*(size_train))	
	len_val_temp = int(len(files)*(size_val))
	len_test = int(len(files)*(size_test))
	#La longitud del conjunto de entrenamiento y validación 
	#ha de ser divisible por dos para que "encaje" el Batch:
	
	if (len_train_temp)%2==0:
		len_train = len_train_temp
	else:
		len_train = (len_train_temp)+1
	
	if (len_val_temp)%2==0:
		len_val = len_val_temp
	else:
		len_val = (len_val_temp)+1 #Le sumo uno porque mejor que tenga 
					     #más elementos

	#Creamos la lista con los números de los archivos aleatorios

	train_list = files[0:len_train]
	val_list = files[len_train:(len_train+len_val)]
	test_list = files[(len_train+len_val):]
	
	#Lo guardamos en sus respectivos archivos:
	
	train = open(wd+'/ImageSets/Main/train.txt','w')
	for i in range(len(train_list)):
		train.write(train_list[i].replace('.jpg','')+'\n')
	train.close()
	
	val = open(wd+'/ImageSets/Main/val.txt','w')
	for i in range(len(val_list)):
		val.write(val_list[i].replace('.jpg','')+'\n')
	val.close()

	test=open(wd+'/ImageSets/Main/test.txt','w')
		
	for i in range(len(test_list)):
		test.write(test_list[i].replace('.jpg','')+'\n')
	test.close()
