
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

wd = getcwd()

#Read the log file:

for k in listdir(wd+'/experiments/logs'):
	if 'faster_rcnn_end2end_VGG16_.txt.' in k:
		name_log = k

log_file = open(wd+'/experiments/logs/'+name_log,'r')

#Clean the log file, remove all the code we dont need:

lines_from_log = log_file.readlines()

for i in range(len(lines_from_log)):
	if str.find(lines_from_log[i],'Iteration 0, loss')!=-1:
		first_row = i #first row that we need
	if str.find(lines_from_log[i],'Wrote snapshot to:')!=-1:
		last_row = i #last row that we need
	
lines_we_need = lines_from_log[first_row:last_row]

output = open(wd+'/prueba_output.txt','w')

for i in range(len(lines_we_need)):
	if str.find(lines_we_need[i],'speed:')==-1:
		output.write(lines_we_need[i])

#Extract mAP and AP for each class:

APs = []
class_names = []

for i in range(len(lines_from_log)):
	if str.find(lines_from_log[i],'VOC07 metric? Yes')!=-1:
		first_row = i+1 #first row that we need
	if str.find(lines_from_log[i],'Mean AP')!=-1:
		last_row = i+1 #last row that we need

aux_ap = lines_from_log[first_row :last_row]


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
plt.plot(iterations,lr,'g',linewidth=2, label='lr')
plt.legend()
plt.title("Learning Rate",fontsize=18)
plt.xlabel("Iteration")
plt.ylabel("Learning Rate")
plt.ylim(0,0.002)

#Graph for APs:

plt.subplot(2,2,4)
plt.bar(range(len(class_names)-1),APs[:len(APs)-1],color ='#ff9999',align='center')
plt.title("mAP: "+str(APs[len(APs)-1]),fontsize=18)
plt.xticks(np.arange(len(class_names)-1),class_names[:len(class_names)-1],rotation = 90)
plt.xlim(-1,len(class_names)-1)

#Save the graph:

plt.savefig('learning_curve_'+str(max(iterations)))

#To show the graphs:

plt.show()
