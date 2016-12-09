#This script must be in the same folder than the Annotations directory
#(note that annotations directory contains the xml labels)
#Create a new dir called "labelsKitti" that contains the kitti labels

import os
from os import listdir, getcwd
from lxml import etree

wd = getcwd()
#if not exits, create the results folder 
if not os.path.exists(wd+'/labelsKitti/'):
	os.mkdir(wd+'/labelsKitti/')
k=1
for dirName, subdirList, nameFile in os.walk(wd+'/Annotations/'):
	
	for nameF in nameFile:
		
		nameF=nameF.replace('.xml','')
		
		doc = etree.parse(wd+'/Annotations/'+nameF+'.xml')
		raiz=doc.getroot()
		labelkitti=open('%s/labelsKitti/%s.txt'%(wd,nameF),'w')
		
		for n in range(len(raiz)):
			
			if raiz[n].tag == 'object':
		
				name = raiz[n].find('name').text
								
				if raiz[n].find('truncated')==None:
					truncated =float(0)
				else:
					truncated = float(raiz[n].find('truncated').text)
				
				occluded = int(0) #Ignored by DetecNet
				alpha = float(0) #Ignored by DetecNet
				bbox_xmin = float(raiz[n].find('bndbox/xmin').text)				
				bbox_ymin = float(raiz[n].find('bndbox/ymin').text)
				bbox_xmax = float(raiz[n].find('bndbox/xmax').text)
				bbox_ymax = float(raiz[n].find('bndbox/ymax').text)
				dimHeight = float(0) #Ignored by DetecNet
				dimWidth = float(0) #Ignored by DetecNet
				dimLength = float(0) #Ignored by DetecNet
				locationX = float(0) #Ignored by DetecNet
				locationY = float(0) #Ignored by DetecNet
				locationZ = float(0) #Ignored by DetecNet
				rotationY = float(0) #Ignored by DetecNet

				labelkitti.write( '%s' % (name))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(truncated))
				labelkitti.write(' ')
				labelkitti.write('%.0f'%(occluded))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(alpha))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(bbox_xmin))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(bbox_ymin))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(bbox_xmax))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(bbox_ymax))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(dimHeight))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(dimWidth))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(dimLength))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(locationX))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(locationY))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(locationZ))
				labelkitti.write(' ')
				labelkitti.write('%.2f'%(rotationY))
				labelkitti.write('\n')
		
		labelkitti.close()

