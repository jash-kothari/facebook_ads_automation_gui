#Add to header of your file
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdUser
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adaccountuser import AdAccountUser
import os
import json
#Initialize a new Session and instantiate an API object:

my_app_id = os.environ['ADS_FB_APP_ID']
my_app_secret = os.environ['ADS_FB_APP_SECRET']
my_access_token = os.environ['ADS_FB_APP_ACCESS_TOKEN'] # Your user access token
page_id = os.environ['FB_PAGE_ID']
database = os.environ['FB_APP_DATABASE']
host = os.environ['FB_APP_DATABASE_HOST']
port = os.environ['FB_APP_DATABASE_PORT']
user = os.environ['FB_APP_DATABASE_USER']
password = os.environ['FB_APP_DATABASE_PASSWORD']
FacebookAdsApi.init(my_app_id, my_app_secret, my_access_token)
me = AdUser(fbid='me')
my_account = me.get_ad_accounts()[1]
my_account=json.loads(str(my_account).replace('<AdAccount> ',''))