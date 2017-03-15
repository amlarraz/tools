
'''This script generates the learning curves: 

-loss
-learning rate
-mAP

during the training of py-faster-rcnn, for use you only need
to save the script in the root folder of py-faster-rcnn and
running in the terminal, notice about only works if you train 
the model with the faster_rcnn_end2end.sh script. 

Enjoy!'''

from os import getcwd, listdir
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import os

wd = getcwd()

#Read the log file:

for k in listdir(wd+'/experiments/logs'):
	if 'faster_rcnn_end2end_VGG16_.txt.' in k:
		name_log = k

log_file = open(wd+'/experiments/logs/'+name_log,'r')

#Clean the log file, remove all the code we dont need:

lines_from_log = log_file.readlines() #Read the log

num_iters=0 #Number of iterations for the training
first_row = 0 #First log line we need
last_row = 0 #Last log line we need
dataset_name=''

for i in range(len(lines_from_log)):

	if str.find(lines_from_log[i],'max_iters=')!=-1:
		n1 = lines_from_log[i].find('max_iters=')
		n2 = lines_from_log[i].find(', pretrained_model')
		num_iters = int(lines_from_log[i][n1:n2].replace('max_iters=',''))
		n1 = lines_from_log[i].find('imdb_name=')
		n2 = lines_from_log[i].find(', max_iters')
		dataset_name = lines_from_log[i][n1:n2].replace('imdb_name=','')[1:len(lines_from_log[i][n1:n2].replace('imdb_name=',''))-1]
		
	if str.find(lines_from_log[i],'Iteration 0, loss')!=-1:
		first_row = i #first row that we need

	if str.find(lines_from_log[i],'Iteration '+str(num_iters - 20)+', lr')!=-1:
		last_row = i #last row that we need

if last_row == 0:
	last_row = len(lines_from_log) #If the training hasnt finished

#Search the dataset name:

lines_we_need = lines_from_log[first_row:last_row]

output = open(wd+'/prueba_output.txt','w')

for i in range(len(lines_we_need)):
	if str.find(lines_we_need[i],'speed:')==-1:
		output.write(lines_we_need[i])

#Extract mAP and AP for each class: (Only if the training has finished)

if last_row != len(lines_from_log): #Check if the training has finished

	APs = []
	class_names = []

	for i in range(len(lines_from_log)):
		if str.find(lines_from_log[i],'AP for')!=-1:
			first_row_ap = i #first row that we need
			
		if str.find(lines_from_log[i],'Mean AP')!=-1:
			last_row_ap = i+1 #last row that we need

	aux_ap = lines_from_log[first_row_ap :last_row_ap]
	
	for i in range(len(aux_ap)-1):
		APs.append(float(aux_ap[i].replace('AP for ','').split('=')[1].strip()))
		class_names.append(aux_ap[i].replace('AP for ','').split('=')[0].strip())

	APs.append(float(aux_ap[len(aux_ap)-1].split('=')[1].strip()))

	class_names.append(aux_ap[len(aux_ap)-1].split('=')[0].strip())

output.close()

output=open('prueba_output.txt','rw')

lines_output =output.readlines()

lines=[]
iterations=[]
loss=[]
lr=[]

for i in range(len(lines_output)):
	#Lines with number of iteration and loss:
	if (str.find(lines_output[i],'Iteration')!=-1) & (str.find(lines_output[i],'loss')!=-1):
		iterations.append(int(lines_output[i][str.find(lines_output[i],'Iteration'):].split(',')[0].replace('Iteration ','').strip())) #part about Iteration number
		loss.append(float(lines_output[i][str.find(lines_output[i],'Iteration'):].split(',')[1].replace(' loss = ','').strip())) #part about loss
		lines.append(lines_output[i])
	#Lines with lr:
	if (str.find(lines_output[i],'lr =')!=-1):
		lr.append(float(lines_output[i][str.find(lines_output[i],'lr'):].replace('lr =','').strip()))

output.close()

#Delete the auxiliar file prueba_output.txt:

command = 'rm prueba_output.txt'
process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
process.wait()

################################## The graph ###############################################

#First create the figure:

fig = plt.figure(figsize = (15,20))

#Graph for loss:

plt.subplot(2,2,(1,2))
plt.plot(iterations,loss,'b',linewidth=1, label='loss')
plt.legend()
plt.title("Loss",fontsize=18)
plt.xlabel("Iteration")
plt.ylabel("Loss")

#Graph for learning rate:

plt.subplot(2,2,3)

#Necessary "if"...':)

if last_row != len(lines_from_log):
	plt.plot(iterations[:len(iterations)-1],lr,'g',linewidth=2, label='lr')
else:
	plt.plot(iterations,lr,'g',linewidth=2, label='lr')

plt.legend()
plt.title("Learning Rate",fontsize=18)
plt.xlabel("Iteration")
plt.ylabel("Learning Rate")
plt.ylim(0,0.002)

#Graph for APs:(only if the training finish)
if last_row != len(lines_from_log):
	plt.subplot(2,2,4)
	plt.bar(range(len(class_names)-1),APs[:len(APs)-1],color ='#ff9999',align='center')
	plt.title("mAP: "+str(APs[len(APs)-1]),fontsize=18)
	plt.xticks(np.arange(len(class_names)-1),class_names[:len(class_names)-1],rotation = 90)
	plt.xlim(-1,len(class_names)-1)

#Save the graph:

if not os.path.exists(wd+'/models/'+dataset_name.split('_')[0]+'/curves'):
	os.mkdir(wd+'/models/'+dataset_name.split('_')[0]+'/curves')

plt.savefig(wd+'/models/'+dataset_name.split('_')[0]+'/curves/'+'learning_curve_'+str(max(iterations)))

#To show the graphs:

plt.show()
