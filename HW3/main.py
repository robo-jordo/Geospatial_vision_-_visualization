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
tile1 = seg.tilegen(-33.907287,18.397682,18)
tile2 = seg.tilegen(-33.903763,18.403344,18)
>>>>>>> 8a902ea0285be7117f2c9658b2353b094c633552

tiles = seg.segments(tile1[:2],tile2[:2])
# print(tiles[0][0][1])
# for i in range(len(tiles)):
# 	print("table entry "+str(i)+": "+str(tiles[i]))

for i in range(len(tiles)):
	for j in range(len(tiles[i])):
		quadkey = seg.quadgen(tiles[i][j][0],tiles[i][j][1])
		down.download(quadkey,str(i)+str(j))

stitched_image = stitched.stitchAll("./images")
stitched.cropper(stitched_image,tile1,tile2,tiles[0][0])