#!/usr/bin/env python3

import sys, io, os
from urllib import request
from PIL import Image
import json

class TileDownloader:
	
	def __init__(self):
		# Get bing maps api key from config file
		with open('config.json') as data_file:
			data = json.load(data_file)
			key = data['bing-tile-key']
		print("refreshed")
		# Get an up to date url to request images from
		BASEURL1 = "http://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?output=json&include=ImageryProviders&key="+str(key)
		f = request.urlopen(BASEURL1).read()
		data = json.loads(f.decode('utf-8'))
		print(data)
		self.CALLURL = data['resourceSets'][0]['resources'][0]['imageUrl']
		print(self.CALLURL)
		subDomains = data['resourceSets'][0]['resources'][0]['imageUrlSubdomains']
		# Set the subdomain and culture portions of the request URL
		self.CALLURL = self.CALLURL.replace("{subdomain}", str(subDomains[1])) #Use first listed subdomain
		self.CALLURL = self.CALLURL.replace("{culture}", 'en-US')              # Use english US culture based names

	def download(self, quadkey, name):
		# Insert quadkey to URL request
		self.CALLURL1 = self.CALLURL.replace("{quadkey}", quadkey)
		# Open the URL
		# print(self.CALLURL1)
		with request.urlopen(self.CALLURL1) as file:
			saveable_image = Image.open(file)
			if (len(saveable_image.info)==0):
				return False
			else:
		# Save the image retrieved from the URL
				saveable_image.save('./images/'+str(name)+'.png')
				print("Tile saved as " + str(name)+'.png')
				return True

