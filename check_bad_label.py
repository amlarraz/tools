import os
from os import listdir, getcwd
from lxml import etree

lista = os.walk('Annotations/')

for root, dirs, files in lista:
	
	for nameF in files:
		
		k=0
		doc = etree.parse('Annotations/'+nameF)
		raiz=doc.getroot()
						
		for n in range(len(raiz)):
			
			if raiz[n].tag == 'object':
				
				name = raiz[n].find('name').text
				#Here change the name of the desired labels
				if (name == 'deer')|(name=='boar')|(name=='person'):
					k=k+1
					
		if k==0:
			print nameF				
				
			
		

