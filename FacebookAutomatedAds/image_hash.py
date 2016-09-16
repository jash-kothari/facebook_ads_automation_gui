from facebookads.adobjects.adimage import AdImage
import header
import urllib
import os

def get_image_hash(url,name,account_id):
	try:
		print 'Downloading image'
		urllib.urlretrieve(url,name)
		image = AdImage(parent_id=account_id)
		image[AdImage.Field.filename] = name
		print 'Uploading image'
		image.remote_create()
		os.remove(name)
		print 'Deleted image locally'
	except OSError, e:
		print 'Error %s' % e
	return image[AdImage.Field.hash]