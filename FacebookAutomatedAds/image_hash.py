from facebookads.adobjects.adimage import AdImage
import header
import urllib
import os
from PIL import Image as Img
import StringIO
import my_constants as constants
import logging
from datetime import date

def get_image_hash(url,name,account_id):
	try:
		logger=logging.getLogger('testlogger')
		logger.info('Downloading image')
		urllib.urlretrieve(url,name)
		image1 = Img.open(constants.PWD+'/'+name)
		width,height = image1.size
		size = width if width < height else height
		# The following is for center cropping
		image1 = image1.crop(((width/2)-(size/2),(height/2)-(size/2),(width/2)+(size/2),(height/2)+(size/2)))
		image1 = image1.resize((1080,1080),Img.ANTIALIAS)
		image1.save(name)
		image1.close()
		image = AdImage(parent_id=account_id)
		image[AdImage.Field.filename] = name
		logger.info('Uploading image')
		image.remote_create()
		os.remove(name)
		logger.info('Deleted image locally')
	except OSError, e:
		logger.error('Error %s' % e)
	return image[AdImage.Field.hash]

def get_image_link(name,image_id):
	image_link=""
	extensions=['jpg','tif','gif','bmp','png']
	for extension in extensions:
		if extension in name:
			image_link = constants.base_url+str(image_id)+'/'+name.replace('.'+extension,'') + constants.size+'.'+extension 
	return image_link