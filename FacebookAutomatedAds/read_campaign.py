import sys
import header
import os
from facebookads.adobjects.campaign import Campaign

campaign = Campaign('6058189894517')
print campaign[Campaign.Field.name]