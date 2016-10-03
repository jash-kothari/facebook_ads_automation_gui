from django.http import HttpResponse
from django.shortcuts import render
import create_carousel
import header
import logging
from datetime import date
from time import sleep

FORMAT = '%(asctime)-15s %(pathname)s %(message)s'
logging.basicConfig(filename='%s-facebook-automated.log' % date.today(),format=FORMAT, level=logging.DEBUG)
# Create your views here.
def index(request):
	id_list=header.get_ids
	return render(request, 'FacebookAutomatedAds/index.html',{'id_list': id_list})

def get_data(request):
	id_list=header.get_ids
	account_id = request.POST.get('id_select',False)
	campaign_id = request.POST.get('campaign_id',False)
	adset_id = request.POST.get('adset_id',False)
	design_ids = request.POST.get('product_ids').split(',')
	caption = request.POST.get('caption',False)
	ad_name = request.POST.get('ad_name',False)
	land_on_design = request.POST.get('design_landing',False) 
	if "on" in land_on_design:
		url=''
		land_on_design = True
	else:
		url = request.POST.get('URL',False)
		land_on_design = False
	campaign_tag = request.POST.get('campaign_tag',False)
	success = create_carousel.create_carousel_ad(caption,adset_id,ad_name,campaign_id,len(design_ids),design_ids,account_id,land_on_design,url,campaign_tag)
	if success:
		context = {
			'id_list':id_list,
			'campaign_id':campaign_id,
			'adset_id':adset_id,
			'campaign_tag':campaign_tag,
			'success': success
		}
	else:
		context = {
			'id_list':id_list,
			'campaign_id':campaign_id,
			'adset_id':adset_id,
			'campaign_tag':campaign_tag,
			'failure': success
		}
	logging.info(context)
	sleep(10)
	return render(request, 'FacebookAutomatedAds/index.html',context)