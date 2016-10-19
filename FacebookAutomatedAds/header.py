#Add to header of your file
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdUser
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adaccountuser import AdAccountUser
import os
import my_constants as constants
#Initialize a new Session and instantiate an API object:
FacebookAdsApi.init(constants.my_app_id, constants.my_app_secret, constants.my_access_token)
def get_ids():
	me = AdUser(fbid='me')
	my_account=me.get_ad_accounts(fields=[AdAccount.Field.name,AdAccount.Field.id])
	id_list={}
	for i in xrange(len(my_account)):
		id_list[str(my_account[i][AdAccount.Field.id])] = str(my_account[i][AdAccount.Field.name])
	print id_list
	return id_list