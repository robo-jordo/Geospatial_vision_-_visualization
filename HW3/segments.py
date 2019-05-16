#!/usr/bin/env python3

import math
import baseconvert

class Segmentor():
	PI = math.pi
	TILESIZE = 256   # each tile is 256x256 pixels

	def tilegen(self, latitude, longitude, level):
		PI = math.pi
		TILESIZE = 256
		self.level = level
		sinLatitude = math.sin(latitude * PI/180)
		pixelX = ((longitude + 180)/360)*256*(2**self.level)
		pixelY = (0.5-math.log((1 + sinLatitude)/(1-sinLatitude))/(4 * PI))*256*(2**self.level)
		tileX = math.floor(pixelX/256)
		tileY = math.floor(pixelY/256)
		tileX_pix = pixelX - (math.floor(pixelX/256)*256)
		tileY_pix = pixelY - (math.floor(pixelY/256)*256)
		# print("tile x: "+str(tileX))
		# print("tile y: "+str(tileY))
		# print("tileX pix: " + str(tileX_pix))
		# print("tileY pix: " + str(tileY_pix))
		return [tileX, tileY, tileX_pix, tileY_pix]

	def segments(self, tile1, tile2): # tile = [tileX, tileY]
		if tile1[0]>tile2[0]:
			X_small=tile2[0]
			X_big = tile1[0]
		else:
			X_small=tile1[0]
			X_big = tile2[0]
		if tile1[1]>tile2[1]:
			Y_small=tile2[1]
			Y_big = tile1[1]
		else:
			Y_small=tile1[1]
			Y_big = tile2[1]
		table = []
		for i in range(X_small,X_big+1):
			row = []
			for j in range(Y_small,Y_big+1):
				row.append([i,j])
			table.append(row)
		return table

	def offcuts(self, tile1, tile2): # tile = [tileX_pix, tileY_pix]
		if tile1[0]>tile2[0]:
			left_cut=tile2[0]
			right_cut = 256 - tile1[0]
		else:
			left_cut=tile1[0]
			right_cut = 256 - tile2[0]
		if tile1[0]>tile2[0]:
			top_cut=tile2[0]
			bottom_cut = 256 - tile1[0]
		else:
			top_cut=tile1[0]
			bottom_cut = 256 - tile2[0]
		return [left_cut, right_cut, top_cut, bottom_cut]

	def quadgen(self, tileX, tileY):
		binTileX = format(tileX, '#0'+str(self.level+2)+'b')[2:]
		# print(binTileX)
		binTileY = format(tileY, '#0'+str(self.level+2)+'b')[2:]
		# print(binTileY)
		quadkey = ''
		for i in range(self.level):
			bit = self.level-i-1
			quadkey = (str(binTileX)[bit])+quadkey
			quadkey = (str(binTileY)[bit])+quadkey
		# print(quadkey)
		final = baseconvert.base((int(quadkey,2)),10,4,string=True)
		while(len(final)!=self.level):
			final = '0'+final

		return final
