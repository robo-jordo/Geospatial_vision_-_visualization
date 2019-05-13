#!/usr/bin/env python3

import segments
import imageDownloader
import imageStitcher

down = imageDownloader.TileDownloader()
seg = segments.Segmentor()
stitched = imageStitcher.Stitcher()
tile1 = seg.tilegen(-33.907287,18.397682,18)
tile2 = seg.tilegen(-33.903763,18.403344,18)

tiles = seg.segments(tile1[:2],tile2[:2])

for i in range(len(tiles)):
	for j in range(len(tiles[i])):
		quadkey = seg.quadgen(tiles[i][j][0],tiles[i][j][1])
		down.download(quadkey,str(i)+str(j))

# stitched.stitch("./images")
stitched_image = stitched.stitchAll("./images")
