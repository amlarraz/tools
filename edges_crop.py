import cv2
import numpy as np
import os
import argparse

############## Parameters default values ############################################

TEST_FILE = '/home/poto/Escritorio/DATASETS/GRAPES/ImageSets/Main/test_old.txt'
IMG_DIR = '/home/poto/Escritorio/DATASETS/GRAPES/JPEGImages/'

INFER_FASTER = '/home/poto/py-faster-rcnn/tools/infer_grapes.py'
WEIGHTS_FASTER = '/home/poto/py-faster-rcnn/output/faster_rcnn_end2end/grapes_trainval/vgg16_faster_rcnn_iter_70000.caffemodel'

INFER_DEEPLABV2 = '/home/poto/Escritorio/deeplabv2/TF/tensorflow-deeplab-resnet/inference.py'
WEIGHTS_DEEPLABV2 = '/home/poto/Escritorio/deeplabv2/TF/tensorflow-deeplab-resnet/models/grapes/snapshots_finetune/model.ckpt-20000'

SAVE_DIR = '/home/poto/Escritorio/DATASETS/GRAPES/final_results/'

############## Arguments and flags ##################################################

def get_arguments(TEST_FILE,IMG_DIR,SAVE_DIR):
    """Parse all the arguments provided from the CLI.
    
    Returns:
      A list of parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Faster and deeplabv2 inference.")
    parser.add_argument("--test_file", type=str, default=TEST_FILE,
                        help="Path to the test.txt file.")
    parser.add_argument("--infer_faster", type=str, default=INFER_FASTER,
                        help="Path to the faster-rcnn infer script.")
    parser.add_argument("--weights_faster", type=str, default=WEIGHTS_FASTER,
                        help="Path to the faster .caffemodel file.")
    parser.add_argument("--weights_deeplabv2", type=str, default=WEIGHTS_DEEPLABV2,
                        help="Path to the .ckpt file.")
    parser.add_argument("--infer_deeplabv2", type=str, default=INFER_DEEPLABV2,
                        help="Path to the deeplabv2 infer script.")
    parser.add_argument("--img_dir", type=str, default=IMG_DIR,
                        help="Where to save inferences.")
    parser.add_argument("--save_dir", type=str, default=SAVE_DIR,
                        help="Where to save inferences.")
    return parser.parse_args()

############## Main function ########################################################

def main():

    #Read test.txt:

    args = get_arguments(TEST_FILE,IMG_DIR,SAVE_DIR)
    test_file = open(args.test_file, 'r')
    test_list = test_file.readlines()

    #Create the final_results dir:

    if not os.path.exists(args.save_dir):
		os.mkdir(args.save_dir)
		os.mkdir(args.save_dir+'results_faster')
		os.mkdir(args.save_dir+'crops')
		os.mkdir(args.save_dir+'results_deeplabv2')

    ################# Inference from Faster-RCNN ####################################

    os.system('python '+args.infer_faster+' --net '+args.weights_faster+' --imgfolder '+args.img_dir+' --outfolder '+args.save_dir+'results_faster --imgsetfile '+args.test_file)

    ################# Crop the images to obtain only the areas with detection #######    

    bboxes_file = open(args.save_dir+'results_faster/bboxes.txt', 'r')
    bboxes_list = bboxes_file.readlines()

    for i in range(len(test_list)):
    	for j in range(len(bboxes_list)):
    		if bboxes_list[j][:bboxes_list[j].find(' ')].replace('.jpg','') == test_list[i].replace('\n',''):

    			x_min = int(bboxes_list[j].split(' ')[2].split('.')[0])
    			y_min = int(bboxes_list[j].split(' ')[3].split('.')[0])
    			x_max = int(bboxes_list[j].split(' ')[4].split('.')[0])
    			y_max = int(bboxes_list[j].split(' ')[5].split('.')[0])

    			full_img = cv2.imread(args.img_dir+test_list[i].replace('\n','')+'.jpg')
    			crop = full_img[y_min:y_max,x_min:x_max ,:]
    			cv2.imwrite(args.save_dir+'crops/'+test_list[i].replace('\n','')+'_'+str(j)+'.jpg',crop)

    ################# Inference from DeepLabV2 ######################################

    lista = os.walk(args.save_dir+'crops')

    for root, dirs, files in lista:
    	for i in range(len(files)):
    		os.system('python '+args.infer_deeplabv2+' '+args.save_dir+'crops/'+files[i]+' '+args.weights_deeplabv2+' --save-dir '+args.save_dir+'results_deeplabv2/')

    ################# Overlap image and segmentation ################################

    for i in range(len(test_list)):
	
	full_img = cv2.imread(args.img_dir+test_list[i].replace('\n','')+'.jpg')
	crops = os.listdir(args.save_dir+'crops')
    		
	for k in range(len(crops)):
		
		if crops[k][:crops[k].find('_')]==test_list[i].replace('\n',''):

			#Open images:
	
			orig = cv2.imread(args.save_dir+'crops/'+crops[k])
			mask = cv2.imread(args.save_dir+'results_deeplabv2/'+crops[k].replace('jpg','png'))
	
	    		#Apply laplacian Algoritm to find edges:
	
	    		laplacian = cv2.Laplacian(mask, cv2.CV_64F, ksize = 5)

	    		#Save the edges image:

	    		cv2.imwrite(args.save_dir+'results_deeplabv2/Laplacian.png', laplacian)

    			laplacian=cv2.imread(args.save_dir+'results_deeplabv2/Laplacian.png')

       			#Change the color of the edges:

       			laplacian[laplacian[:,:,2]==255] = [255,255,0]

       			#Overlap images: (output_edge = original+edge, output_mask = orig+mask)

       			output_edge=cv2.addWeighted(orig,1,laplacian,1,0)
       			output_mask=cv2.addWeighted(orig,1,mask,0.6,0)
		
			#Paste the crops+edge in the original image:

			for j in range(len(bboxes_list)):
				if crops[k] == bboxes_list[j][:bboxes_list[j].find(' ')].replace('.jpg','_'+str(j)+'.jpg'):
    					
					x_min = int(bboxes_list[j].split(' ')[2].split('.')[0])
					y_min = int(bboxes_list[j].split(' ')[3].split('.')[0])
					x_max = int(bboxes_list[j].split(' ')[4].split('.')[0])
					y_max = int(bboxes_list[j].split(' ')[5].split('.')[0])

				
					full_img[y_min:y_max,x_min:x_max ,:] = output_edge
					cv2.rectangle(full_img,(x_min,y_min),(x_max,y_max),(6,24,207),3)
    	
			cv2.imwrite(args.save_dir+crops[i][:crops[i].find('_')]+'_edges.jpg',full_img)	
					
			# Remove the Edge image:

       			os.system('rm '+args.save_dir+'results_deeplabv2/Laplacian.png')

    print ''
    print 'All is done'
    print ''

if __name__ == "__main__":
    main()
