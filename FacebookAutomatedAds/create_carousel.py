from facebookads.objects import Ad
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adcreative import AdCreative
from facebookads.adobjects.adcreativelinkdata import AdCreativeLinkData
from facebookads.adobjects.adcreativeobjectstoryspec import AdCreativeObjectStorySpec
from facebookads.adobjects.adcreativelinkdatachildattachment import AdCreativeLinkDataChildAttachment
import header
import json
import psycopg2
import image_hash
import sys

def create_carousel_ad(caption,adset_id,ad_name,campaign_id,times,design_list):
	con = None
	simple_list=[]
	try:
		con = psycopg2.connect(database=header.database, user=header.user, password=header.password,host=header.host,port=header.port)
		cur = con.cursor()
		for i in xrange(times):
			design_id=design_list[i]
			cur.execute('SELECT discount_percent,designer_id from designs where id='+str(design_id))
			row=cur.fetchone()
			#row[0] is discount percentage and row[1] is designer_id
			cur.execute('SELECT id,photo_file_name FROM images where design_id = '+str(design_id))
			rows=cur.fetchone()
			#rows[0] is image id and rows[1] is photo file name
			cur.execute('SELECT name FROM "categories" INNER JOIN "categories_designs" ON "categories"."id" = "categories_designs"."category_id" WHERE design_id ='+str(design_id))
			category_name = cur.fetchone()
			image_link=""
			if 'jpg' in rows[1]:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows[0])+'/'+rows[1].replace('.jpg','')+'_large.jpg' 
			elif 'tif' in rows[1]:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows[0])+'/'+rows[1].replace('.tif','')+'_large.tif' 
			elif 'gif' in rows[1]:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows[0])+'/'+rows[1].replace('.gif','')+'_large.gif' 
			elif 'bmp' in rows[1]:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows[0])+'/'+rows[1].replace('.bmp','')+'_large.bmp' 
			elif 'png' in rows[1]:
				image_link = 'https://assets1.mirraw.com/images/'+str(rows[0])+'/'+rows[1].replace('.png','')+'_large.png' 
			if row[0] is None:
				row[0]=0
			product1 = AdCreativeLinkDataChildAttachment()
			product1[AdCreativeLinkDataChildAttachment.Field.link] = 'www.mirraw.com/designers/'+str(row[1])+'/designs/'+design_id+'?utm_source=facebook&utm_medium=cpc&utm_campaign='+str(campaign_id)
			product1[AdCreativeLinkDataChildAttachment.Field.name] = category_name[0]
			product1[AdCreativeLinkDataChildAttachment.Field.description] = 'Discount '+str(row[0])+'%'
			product1[AdCreativeLinkDataChildAttachment.Field.image_hash] = image_hash.get_image_hash(image_link,rows[1])
			simple_list.append(product1)

		link = AdCreativeLinkData()
		link[link.Field.link] = 'www.mirraw.com'
		link[link.Field.child_attachments] = simple_list
		link[link.Field.caption] = caption

		story = AdCreativeObjectStorySpec()
		story[story.Field.page_id] = header.page_id
		story[story.Field.link_data] = link

		creative = AdCreative(parent_id=header.my_account['id'])
		creative[AdCreative.Field.name] = 'MPA Creative'
		creative[AdCreative.Field.object_story_spec] = story
		creative.remote_create()
		creative=json.loads(str(creative).replace('<AdCreative> ',''))

		ad = Ad(parent_id=header.my_account['id'])
		ad[Ad.Field.name] = ad_name
		ad[Ad.Field.adset_id] = adset_id
		ad[Ad.Field.status] = Campaign.Status.paused
		ad[Ad.Field.creative] = {'creative_id': str(creative['id'])}
		ad.remote_create()

	except psycopg2.DatabaseError, e:
		print 'Error %s' % e
		return False
		sys.exit(1)

	except StandardError, e:
		print 'Error %s' % e
		return False

	finally:
		if con:
			con.close()
	return True