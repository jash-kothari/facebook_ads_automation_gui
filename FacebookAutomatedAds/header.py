#Add to header of your file
from facebookads.api import FacebookAdsApi
from facebookads import objects
from facebookads.objects import AdUser
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.adaccountuser import AdAccountUser
import os
import my_constants as constants
from time import sleep
import logging
import urlparse
import psycopg2
import psycopg2.extras
import itertools
import image_hash
#Initialize a new Session and instantiate an API object:
FacebookAdsApi.init(constants.my_app_id, constants.my_app_secret, constants.my_access_token)
logger = logging.getLogger('testLogger')
def get_ids():
	me = AdUser(fbid='me')
	my_account=me.get_ad_accounts(fields=[AdAccount.Field.name,AdAccount.Field.id])
	id_list={}
	for i in xrange(len(my_account)):
		id_list[str(my_account[i][AdAccount.Field.id])] = str(my_account[i][AdAccount.Field.name])
	logger.info(id_list)
	return id_list

def get_category_list():
	urlparse.uses_netloc.append("postgres")
	database_url = urlparse.urlparse(constants.database_url)
	conn = psycopg2.connect( database=database_url.path[1:], user=database_url.username, password=database_url.password, host=database_url.hostname, port=database_url.port )
	curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	curr.execute('select id,name from categories')
	rows = curr.fetchall()
	category_hash={}
	conn.close()
	for row in rows:
		category_hash[int(row['id'])] = row['name']
	return category_hash

def get_top_selling_items(category_name):
	urlparse.uses_netloc.append("postgres")
	database_url = urlparse.urlparse(constants.database_url)
	conn = psycopg2.connect( database=database_url.path[1:], user=database_url.username, password=database_url.password, host=database_url.hostname, port=database_url.port )
	curr = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
	id_list=[]
	curr.execute("select id from categories where name ='"+category_name+"'")
	row=curr.fetchone()
	id_list.append(row['id'])
	curr.execute("select id from categories where parent_id ="+str(id_list[0]))
	rows=curr.fetchall()
	for id in rows:
		id_list.append(id['id'])
	curr.execute("SELECT l.design_id FROM line_items l,categories_designs cd,categories c,designs d WHERE cd.design_id=l.design_id AND c.id=cd.category_id AND l.design_id = d.id AND lower(d.state) like 'in_stock' AND l.created_at > current_date - interval '90' day and c.id in ("+','.join(map(str, id_list))+") GROUP BY l.design_id,c.name ORDER BY count(l.id) DESC LIMIT 100")
	design_ids = rows = list(set(list(itertools.chain.from_iterable(curr.fetchall()))))
	top_selling_list=[]
	top_selling_hash={}
	for design_id in design_ids:
		curr.execute('SELECT id,photo_file_name FROM images where design_id = '+str(design_id))
		rows = curr.fetchone()
		image_link = image_hash.get_image_link(rows['photo_file_name'],rows['id'],'_thumb')
		curr.execute('SELECT discount_percent from designs where id='+str(design_id))
		row = curr.fetchone()
		internal_hash = {'image_link': image_link,'discount': row['discount_percent'],'design_id': design_id}
		top_selling_list.append(internal_hash)
	top_selling_hash['top_items']=top_selling_list
	return top_selling_hash
