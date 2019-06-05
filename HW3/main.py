#!/usr/bin/env python3

import segments
import imageDownloader
import imageStitcher

import os
import glob

files = glob.glob('./images/*')
for f in files:
    os.remove(f)

down = imageDownloader.TileDownloader()
seg = segments.Segmentor()
stitched = imageStitcher.Stitcher()

def getBlock(lat1, lon1, lat2, lon2):
	too_high = True
	img_check = False
	level = 23
	down = imageDownloader.TileDownloader()
	seg = segments.Segmentor()
	while(too_high==True):
		tile1 = seg.tilegen(lat1,lon1,level)
		tile2 = seg.tilegen(lat2,lon2,level)
		tiles = seg.segments(tile1[:2],tile2[:2])
		if (img_check == False):
			print("checking_level:")
			print(level)
			quadkey = seg.quadgen(tiles[0][0][0],tiles[0][0][1])
			img_check = down.download(quadkey,'check')
			level = level - 1
		else:
			files = glob.glob('./images/*')
			for f in files:
				os.remove(f)
			print("Using level:")
			print(level)
			for i in range(len(tiles)):
				for j in range(len(tiles[i])):

					quadkey = seg.quadgen(tiles[i][j][0],tiles[i][j][1])
					down.download(quadkey,str(i)+str(j))

			stitched_image = stitched.stitchAll("./images")
			stitched.cropper(stitched_image,tile1,tile2,tiles[0][0])
			too_high == False
			break
 

getBlock(-33.907287,18.397682,-33.903763,18.403344)