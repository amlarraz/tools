# -*- coding: utf-8

#INFORMATION FOR USE:
#To use this script you must to comply this requeriments:
#	-The structure of the directory must to be:
#		|
#		|-- autotrain.py (this script)
#		|-- /dataset (contains the dataset you want to the training)
#		|	|-- train.txt (txt with the train images absolute paths) 
#		|	|-- val.txt (txt with the validation images absolute paths)
#		|	|-- test.txt (txt with the test images absolute paths)
#		|	|-- /JPEGImages (Contains all the images train, val and test)
#		|	|-- /labels (Contains the labels in Yolo format for all images)
#		|-- /backup (empty folder to stores the weights)
#		|-- /darknet (it is created automatically when you do the git clone for the darknet repo)
#
#	-The version of darknet you need for the correct working 
#	of this script is the one you find in this repo:(thanks Ning ;))
#		https://github.com/Guanghan/darknet.git


from os import listdir, getcwd, rename

wd = getcwd()

nc = input('How many classes do you want to train?: ')

listClasses = []

for i in range(nc):
	n=i+1
	print 'For the class number',n	
	new = raw_input('Write the name of the class: ')
	listClasses.append('"'+new+'"')

#Changes in /darknet/src/yolo.c :

yoloSRC = open(wd+'/darknet/src/yolo.c','rw')

yoloSRC_new = open(wd+'/darknet/src/yolo_new.c','w')

contador = 1

for line in yoloSRC:

	if contador == 13:
		line = line.replace(line[17:],str(nc)+'\n')		
		contador = contador +1
	elif contador == 16:
		line = line.replace(line[21:],",".join(listClasses))
		line = line + '};\n'		
		contador = contador +1
	elif contador == 22:
		line = line.replace(line[26:],wd+'/dataset/train.txt";\n')
		contador = contador +1
	elif contador == 25:
		line = line.replace(line[30:],wd+'/backup/";\n')
		contador = contador +1
	elif contador == 155:
		line = line.replace(line[29:],wd+'/dataset/val.txt");\n')
		contador = contador +1
	elif contador == 244:
		line = line.replace(line[29:],wd+'/dataset/test.txt");\n')
		contador = contador +1
	else:
		contador = contador+1
	
	yoloSRC_new.write(line)

yoloSRC.close()
yoloSRC_new.close()

rename(wd+'/darknet/src/yolo_new.c',wd+'/darknet/src/yolo.c')

#Changes in /darknet/src/yolo_kernels.cu :

yoloKernelsSRC=open(wd+'/darknet/src/yolo_kernels.cu','rw')

yoloKernelsSRC_new=open(wd+'/darknet/src/yolo_kernels_new.cu','w')

contador = 1

for line in yoloKernelsSRC:

	if contador == 17:
		line = line.replace(line[16:],str(nc))
		contador = contador+1
	else:
		contador = contador +1

	yoloKernelsSRC_new.write(line)

yoloKernelsSRC.close()
yoloKernelsSRC_new.close()

rename(wd+'/darknet/src/yolo_kernels_new.cu',wd+'/darknet/src/yolo_kernels.cu')

#Changes in /darknet/cfg/yolo.cfg :

yoloCFG = open(wd+'/darknet/cfg/yolo.cfg','rw')
yoloCFG_new = open(wd+'/darknet/cfg/yolo_new.cfg','w')

contador = 1

for line in yoloCFG:

	if contador == 218:
		line = line.replace(line[8:],str(7*7*(2*5+nc))+'\n')
		contador = contador+1
	elif contador == 222:
		line = line.replace(line[8:],str(nc)+'\n')
		contador = contador+1
	else:
		contador = contador+1

	yoloCFG_new.write(line)

yoloCFG.close()
yoloCFG_new.close()

rename(wd+'/darknet/cfg/yolo_new.cfg',wd+'/darknet/cfg/yolo.cfg')

#Changes in the Makefile:

quiz1 = raw_input('Do you want to use the GPU during the training? (y),(n): ')
quiz2 = raw_input('Do you want to use OpenCV? (y),(n): ')

makeFile = open(wd+'/darknet/Makefile','rw')
makeFile_new = open(wd+'/darknet/Makefile_new','w')

contador = 1	

for line in makeFile:

	if (contador == 1) & (quiz1 == 'y'):
		line = line.replace(line[4:],'1\n')
		contador = contador+1
	elif (contador == 2) & (quiz2 == 'y'):
		line = line.replace(line[7:],'1\n')
		contador = contador+1
	else:
		contador = contador+1
	
	makeFile_new.write(line)

makeFile.close()
makeFile_new.close()

rename(wd+'/darknet/Makefile_new',wd+'/darknet/Makefile')
