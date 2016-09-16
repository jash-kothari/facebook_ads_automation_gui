from facebookads.adobjects.adimage import AdImage
import header
import urllib
import os
from PIL import Image as Img
import StringIO

def get_image_hash(url,name,account_id):
	try:
		print 'Downloading image'
		urllib.urlretrieve(url,name)
		image1 = Img.open('/home/mirrawdev3/ads_automation_facebook/python_trial/Facebook_Ads/'+name)
		width,height = image1.size
		size = width if width < height else height
		# The following is for center cropping
		image1 = image1.crop(((width/2)-(size/2),(height/2)-(size/2),(width/2)+(size/2),(height/2)+(size/2)))
		image1 = image1.resize((1080,1080),Img.ANTIALIAS)
		image1.save(name)
		image1.close()
		image = AdImage(parent_id=account_id)
		image[AdImage.Field.filename] = name
		print 'Uploading image'
		image.remote_create()
		os.remove(name)
		print 'Deleted image locally'
	except OSError, e:
		print 'Error %s' % e
	return image[AdImage.Field.hash]