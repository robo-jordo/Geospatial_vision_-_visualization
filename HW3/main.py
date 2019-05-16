#!/usr/bin/env python3

import segments
import imageDownloader

down = imageDownloader.TileDownloader()
seg = segments.Segmentor()
tile1 = seg.tilegen(-33.907287,18.397682,20)
tile2 = seg.tilegen(-33.903763,18.403344,20)

tiles = seg.segments(tile1[:2],tile2[:2])

for i in range(len(tiles)):
	for j in range(len(tiles[i])):
		quadkey = seg.quadgen(tiles[i][j][0],tiles[i][j][1])
		down.download(quadkey,str(i)+str(j))

