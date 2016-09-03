from facebookads.adobjects.adimage import AdImage
import header
import urllib
import os
def get_image_hash(url,name):
	urllib.urlretrieve(url,name)
	image = AdImage(parent_id=header.my_account['id'])
	image[AdImage.Field.filename] = name
	image.remote_create()
	os.remove(name)
	# Output image Hash
	return image[AdImage.Field.hash]