#!/usr/bin/python


image_split = 4
import cv2
from pathlib import Path
import glob
import numpy as np

path=Path(".")

path=path.glob("hey/*.jpg")

images=[]
finalarray=[]
backSub1 = cv2.createBackgroundSubtractorMOG2()
backSub2 = cv2.createBackgroundSubtractorKNN()
backSub3 = cv2.bgsegm.createBackgroundSubtractorMOG()
# path=Path(".")
# files=(path.glob(("hey/*.jpg")).sort()
# print(files)

filenames = glob.glob("hey/*.jpg")
filenames.sort()

#images = [cv2.imread(img) for img in filenames]
# for img in images:
#     print img

for imagepath in filenames:
		img=cv2.imread(str(imagepath))
		print(imagepath)
		#img=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)                         
		img=cv2.resize(img,(400,400))
		images.append(img)

for i in images:
	img_yuv = cv2.cvtColor(i, cv2.COLOR_BGR2YUV)

# equalize the histogram of the Y channel
	img_yuv[:,:,0] = cv2.equalizeHist(img_yuv[:,:,0])

# convert the YUV image back to RGB format
	img_output = cv2.cvtColor(img_yuv, cv2.COLOR_YUV2BGR)
	img_output = cv2.cvtColor(img_output,cv2.COLOR_BGR2GRAY)

	median = cv2.medianBlur(img_output,3)
	height, width, channels = img.shape
	median1 = img_output[:width/2,:height/2]
	median2 = img_output[:width/2,height/2:]
	median3 = img_output[width/2:,:height/2]
	median4 = img_output[width/2:,height/2:]
	
	mean1 = (median[:width/2,:height/2]).mean()
	mean2 = (median[:width/2,height/2:]).mean()
	mean3 = (median[width/2:,:height/2]).mean()
	mean4 = (median[width/2:,height/2:]).mean()
	print(mean1)

	ret1,thresh1 = cv2.threshold(median1,mean1-(mean1/4),255,cv2.THRESH_BINARY)
	ret2,thresh2 = cv2.threshold(median2,mean2-(mean2/4),255,cv2.THRESH_BINARY)
	ret3,thresh3 = cv2.threshold(median3,mean3-(mean3/4),255,cv2.THRESH_BINARY)
	ret4,thresh4 = cv2.threshold(median4,mean4-(mean4/4),255,cv2.THRESH_BINARY)
	# median1 = cv2.medianBlur(thresh1,5)
	# median2 = cv2.medianBlur(thresh2,5)
	# median3 = cv2.medianBlur(thresh3,5)
	# median4 = cv2.medianBlur(thresh4,5)
	final1 = np.concatenate((thresh1, thresh2), axis=1)
	final2 = np.concatenate((thresh3, thresh4), axis=1)
	final = np.concatenate((final1, final2), axis=0)
	final = cv2.medianBlur(final,5)
	finalarray.append(final)
	# ret,newthresh = cv2.threshold(final,200,255,cv2.THRESH_BINARY)

	# new =cv2.adaptiveThreshold(final,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 101, 11)
	
	

	# clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
	# cl1 = clahe.apply(i)
	# cl1*1.2
	# median = cv2.medianBlur(cl1,3)
	# fgMask = backSub1.apply(median)
	# edges1 = cv2.Canny(median,100,200)

	# fgMask = backSub1.apply(equ)
	# edges2 = cv2.Canny(fgMask,0,200)
	# #median = cv2.medianBlur(edges2,5)
	# fgMask2 = backSub2.apply(median)
	# #fgMask3 = backSub1.apply(fgMask2)
	# #fgMask4 = backSub1.apply(fgMask3)

	# cv2.imshow('Frame', i)
	# cv2.imshow('cl1', img_output)
	# cv2.imshow('q1', thresh1)
	# cv2.imshow('q2', thresh2)
	# cv2.imshow('q3', thresh3)
	# cv2.imshow('q4', thresh4)
	# cv2.imshow('fin', final)

	# cv2.imshow('final2', fgMask2)
	#cv2.imshow('FG Mask4', fgMask4)
	# cv2.waitKey(0)

smear_min_r =  6
smear_max_r =  10
smear_min_a =  3.14*smear_min_r**2
smear_max_a =  3.14*smear_max_r**2
avg = np.zeros((400,400),np.float)
count = 0

for i in range(len(images)):
	avg += np.array(finalarray[i],dtype=np.float)
	count +=1
	if count==20 or i ==0:
		newavg = avg/count
		newavg = np.array(np.round(newavg),dtype=np.uint8)
		threshnew = cv2.adaptiveThreshold(newavg,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY, 101, 101)
		# ret,threshnew = cv2.threshold(final,200,255,cv2.THRESH_BINARY)
		newinv = cv2.bitwise_not(threshnew)
		avg = np.zeros((400,400),np.float)
		count = 0

	#Contours
	_,contours,_ = cv2.findContours(newinv,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) 

	if contours:
		if (cv2.contourArea(contours[0])>smear_min_a and cv2.contourArea(contours[0])<smear_max_a):
			smudge = cv2.drawContours(images[i],contours,-1,(0,255,0),2) 
			cv2.imshow('contour', smudge)
			cv2.waitKey(0)

	cv2.imshow('zefsothresh',newavg)
	cv2.imshow('invvv', newinv)
	cv2.imshow('final',images[i])
	# cv2.imshow('cover',coverblur)
	cv2.waitKey(0)