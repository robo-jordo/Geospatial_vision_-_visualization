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

    	# Get an up to dat url to request images from
		BASEURL1 = "http://dev.virtualearth.net/REST/V1/Imagery/Metadata/Aerial?output=json&include=ImageryProviders&key="+str(key)
		f = request.urlopen(BASEURL1).read()
		data = json.loads(f.decode('utf-8'))
		CALLURL = data['resourceSets'][0]['resources'][0]['imageUrl']
		subDomains = data['resourceSets'][0]['resources'][0]['imageUrlSubdomains']
		# Set the subdomain and culture portions of the request URL
		CALLURL = CALLURL.replace("{subdomain}", str(subDomains[0])) #Use first listed subdomain
		CALLURL = CALLURL.replace("{culture}", 'en-US')              # Use english US culture based names

	def download(self, quadkey, name):
		# Insert quadkey to URL request
		CALLURL = CALLURL.replace("{quadkey}", quadkey)
		# Open the URL
		with request.urlopen(CALLURL) as file:
			saveable_image = Image.open(file)
		# Save the image retrieved from the URL
		saveable_image.save('./'+str(name)+'.png')
		print("Image saved as " + str(name)+'.png')