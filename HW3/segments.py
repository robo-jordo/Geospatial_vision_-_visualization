#!/usr/bin/env python3

import math

class Segmentor(self):
	PI = math.pi
	TILESIZE = 256   # each tile is 256x256 pixels

	def decompose(latitude, longitude, level):
		sinLatitude = math.sin(latitude * PI/180)
		pixelX = ((longitude + 180)/360)*256*(2**(level))
		pixelY = (0.5-math.log((1 + sinLatitude)/(1-sinLatitude))/(4 * PI))*256*(2**level)
		tileX = math.floor(pixelX/256)
		tileY = math.floor(pixelY/256)
		binTileX = format(tileX, '#0'+str(level+2)+'b')[2:]
		print(binTileX)
		binTileY = format(tileY, '#0'+str(level+2)+'b')[2:]
		print(binTileY)
		quadkey = ''
		for i in range(level):
			bit = level-i-1
			quadkey = (str(binTileX)[bit])+quadkey
			quadkey = (str(binTileY)[bit])+quadkey

		return quadkey