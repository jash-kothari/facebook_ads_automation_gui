import json
import my_constants as constants
from facebookads.adobjects.adaccount import AdAccount
from facebookads.adobjects.campaign import Campaign
from facebookads.adobjects.adset import AdSet
import header
import logging
from datetime import date
logger=logging.getLogger('testlogger')
def get_campaign_list(account_id):
	ad_account = AdAccount(account_id)
	campaigns = ad_account.get_campaigns(fields=[Campaign.Field.name,Campaign.Field.id,Campaign.Field.status])
	active_campaign_hash = {}
	for campaign in campaigns:
		if 'ACTIVE' in campaign[Campaign.Field.status]:
			active_campaign_hash[campaign[Campaign.Field.id]]=campaign[Campaign.Field.name]
	logger.info(active_campaign_hash)
	return active_campaign_hash

def get_adset_list(campaign_id):
	campaign = Campaign(campaign_id)
	adsets = campaign.get_ad_sets(fields=[AdSet.Field.name,AdSet.Field.id,AdSet.Field.status])
	active_adset_hash = {}
	for adset in adsets:
		if 'ACTIVE' in adset[AdSet.Field.status]:
			active_adset_hash[adset[AdSet.Field.id]]=adset[AdSet.Field.name]
	logger.info(active_adset_hash)
	return active_adset_hash