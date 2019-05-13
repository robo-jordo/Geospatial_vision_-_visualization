#!/usr/bin/env python3

from imutils import paths
import imutils
import cv2
import numpy as np
from PIL import Image

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""

class Stitcher():

	def stitch(self,path):

		print("loading images")
		images_paths = sorted(list(paths.list_images(path)))
		images = []

		for i in images_paths:
			print(i)
			im = cv2.imread(i)
			# print(type(im))
			images.append(im)

		cv_stitcher = cv2.Stitcher_create()
		# cv_stitcher.setRegistrationResol(-1);
		# cv_stitcher.setSeamEstimationResol(-1);
		# cv_stitcher.setCompositingResol(-1);
		# cv_stitcher.setPanoConfidenceThresh(-1);
		# cv_stitcher.setWaveCorrection(True);
		# cv_stitcher.setWaveCorrectKind(detail::WAVE_CORRECT_HORIZ);
		(stitched_check, stitched_image) = cv_stitcher.stitch(images)
		if stitched_check == 0:
			# cv2.imwrite("Stitched_Image.png", stitched_image)
			cv2.imshow("Stitched_Image", stitched_image)
			cv2.waitKey(0)
		else:
			print("Stitching no good")

	def stitchAll(self,path):

		images_paths = sorted(list(paths.list_images(path)))
		maxver = 0
		images = []
		verts = []

		for i in images_paths:
			im = Image.open(i)
			images.append(im)
			im_no = find_between(i,'images/','.png')
			if int(im_no[-1]) > maxver:
				maxver = int(im_no[-1])
		maxver+=1

		# VERTICAL STITCH
		wver = [0]*maxver
		hver = [0]*maxver
		i = 0 
		while i < len(images):
			for j in range(0,maxver):
				(wver[j], hver[j]) = images[i+j].size
			htotal = sum(hver)
			wtotal = max(wver)
			# print(htotal)
			# print(wtotal)
			result = Image.new('RGB',(wtotal,htotal))
			for j in range(0,maxver):
				result.paste(im =images[i+j],box = (0,int((htotal/maxver)*j)))
			verts.append(result)
			i+= (maxver)

		#HORIZONTAL STITCH
		whor = [0]*len(verts)
		hhor = [0]*len(verts)
		for i in range(len(verts)):
			(whor[i],hhor[i]) = verts[i].size
		htotal = max(hhor)
		wtotal = sum(whor)
		final = Image.new('RGB',(wtotal,htotal))
		for i in range(len(verts)):
			final.paste(im =verts[i],box = (int((wtotal/len(verts))*i),0))
		final.show()
		return final