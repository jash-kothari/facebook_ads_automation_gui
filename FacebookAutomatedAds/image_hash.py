from facebookads.adobjects.adimage import AdImage
import header
import urllib
import os

def get_image_hash(url,name,account_id):
	urllib.urlretrieve(url,name)
	image = AdImage(parent_id=account_id)
	image[AdImage.Field.filename] = name
	image.remote_create()
	os.remove(name)
	# Output image Hash
	return image[AdImage.Field.hash]