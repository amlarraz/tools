import os
from os import listdir, getcwd
import xml.etree.ElementTree as ET

wd = getcwd()

lista = os.walk('Annotations/')

#Change the classes do you want to train:

classes =["person","car","motorcicle","boar","deer"] 

if not os.path.exists(wd+'/AnnotationsNEW/'):
	os.mkdir(wd+'/AnnotationsNEW/')

for root, dirs, files in lista:
	
	for nameF in files:
		
		doc = ET.parse('Annotations/'+nameF)
		raiz=doc.getroot()		
		
		for object in raiz.findall('object'):
			
			if object.find('name').text not in classes:
				
				raiz.remove(object)
						
		tree = ET.ElementTree(raiz)
		tree.write(wd+'/AnnotationsNEW/'+nameF)

				
