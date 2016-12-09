# coding=utf-8

import xml.etree.ElementTree as ET
import pickle
import os
from os import listdir, getcwd
from os.path import join

#Aquí coloca los conjuntos de datos que quieras tener,
#están puestos train,val,test, pero por ejemplo, en PascalVOC
#estaban:
#('2012', 'train'), ('2012', 'val'), ('2007', 'train'), ('2007', 'val'), ('2007', 'test')
#así que al gusto de cada cual!

sets=[('train'), ('val'), ('test')]

#Nombres de las clases con las que vamos a trabajar, en este caso solamente hay
#una clase "boar", sin embargo, en PascalVOC había:
#classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow",
#"diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", 
#"tvmonitor"]

classes = ["boar"]


def convert(size, box):
    dw = 1./size[0]
    dh = 1./size[1]
    x = (box[0] + box[1])/2.0
    y = (box[2] + box[3])/2.0
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x*dw
    w = w*dw
    y = y*dh
    h = h*dh
    return (x,y,w,h)

def convert_annotation(image_id):
    
    #Donde pone 'Annotations/%s.xml' hay que poner la ruta donde están los xml creados con labelImg
    #OJO!! han de tener los mismos nombres que las imágenes JPEG:

    in_file = open('Annotations/%s.xml'%(image_id))
    
    #Puedes cambiar la ruta donde quieres que se almacenen los labels:
    
    out_file = open('labels/%s.txt'%(image_id), 'w')
    tree=ET.parse(in_file)
    root = tree.getroot()
    size = root.find('size')
    w = int(size.find('width').text)
    h = int(size.find('height').text)

    for obj in root.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult) == 1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
        bb = convert((w,h), b)
        out_file.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')

wd = getcwd()

for image_set in sets:
    if not os.path.exists('labels/'):
        os.makedirs('labels/')
    
    #La ruta 'ImageSets/Main/%s.txt' ha de apuntar a la carpeta donde hayas almacenado
    #los .txt con los nombres de las imágenes que quieres que vayan en cada grupo (train,val,test)

    image_ids = open('ImageSets/Main/%s.txt'%(image_set)).read().strip().split()
    list_file = open('%s.txt'%(image_set), 'w')
    for image_id in image_ids:
        #Ruta donde están TODAS las imágenes JPEG o jpg
        list_file.write('%s/JPEGImages/%s.jpg\n'%(wd,image_id))
        convert_annotation(image_id)
    list_file.close()

