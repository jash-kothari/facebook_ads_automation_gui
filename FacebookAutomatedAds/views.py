from django.http import HttpResponse
from django.shortcuts import render
import create_carousel

# Create your views here.
def index(request):
	return render(request, 'FacebookAutomatedAds/index.html')

def get_data(request):
	campaign_id = request.POST.get('campaign_id',False)
	adset_id = request.POST.get('adset_id',False)
	design_ids=[]
	for i in xrange(5):
		design_ids.append(request.POST.get('product_id'+str(i+1),False))
	caption = request.POST.get('caption',False)
	ad_name = request.POST.get('ad_name',False)
	if create_carousel.create_carousel_ad(caption,adset_id,ad_name,campaign_id,5,design_ids):
		return render(request, 'FacebookAutomatedAds/success.html')
	else:
		return render(request,'FacebookAutomatedAds/500.html',status=500)