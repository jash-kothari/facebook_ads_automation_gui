from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from time import sleep
import get_campaign_list
import create_carousel
import header
import logging

logger=logging.getLogger('testlogger')
# Create your views here.
def index(request):
	id_list=header.get_ids
	return render(request, 'FacebookAutomatedAds/index.html',{'id_list': id_list})

def get_data(request):
	id_list=header.get_ids
	account_id = request.POST.get('account_id',False)
	account_name = request.POST.get('account_name',False)
	adset_id = request.POST.get('adset_select',False)
	campaign_id = request.POST.get('campaign_id',False)
	campaign_name =  request.POST.get('campaign_name',False)
	adset_list = get_campaign_list.get_adset_list(campaign_id)
	design_ids = request.POST.get('product_ids').split(',')
	caption = request.POST.get('caption',False)
	ad_name = request.POST.get('ad_name',False)
	if "design_landing" not in request.POST:
		land_on_design = False
	else:
		land_on_design = True
	print account_id
	print land_on_design
	url = request.POST.get('url',False)
	print url
	campaign_tag = request.POST.get('campaign_tag',False)
	print campaign_tag
	logger.debug("Going to create ad now")
	success = create_carousel.create_carousel_ad(caption,adset_id,ad_name,len(design_ids),design_ids,account_id,land_on_design,url,campaign_tag)
	# logger.info(context)
	ad_creation = "alert alert-success" if success else "alert alert-failure"
	message = "Your ad has been created!" if success else "Error Creating ad"	
	context = {
		'account_id': account_id,
		'account_name': account_name,
		'campaign_name': campaign_name,
		'adset_list': adset_list,
		'campaign_id': campaign_id,
		'success': ad_creation,
		'message': message
		}
	return render(request, 'FacebookAutomatedAds/adset_list.html',context)


def get_campaigns(request):
	account_id = request.POST.get('id_select',False)
	account_name = request.POST.get('account_name',False)
	campaign_list = get_campaign_list.get_campaign_list(account_id)
	context = {
		'campaign_list': campaign_list,
		'account_id': account_id,
		'account_name': account_name
		}
	return render(request, 'FacebookAutomatedAds/campaign_list.html',context)

def get_adsets(request):
	account_name = request.POST.get('account_name',False)
	account_id = request.POST.get('account_id',False)
	campaign_id = request.POST.get('campaign_select',False)
	campaign_name = request.POST.get('campaign_name',False)
	adset_list = get_campaign_list.get_adset_list(campaign_id)
	context = {
	'adset_list': adset_list,
	'account_name': account_name,
	'account_id': account_id,
	'campaign_name': campaign_name,
	'campaign_id': campaign_id
	}
	return render(request, 'FacebookAutomatedAds/adset_list.html',context)