# GUI Version for my repo of Facebook Ads Automation CLI

Pre Requisite
Needs Facebook-ads-python-sdk installed

Set Environment Variables

ADS_FB_APP_ID = Your Facebook App Id

ADS_FB_APP_SECRET = Your Facebook App Secret

ADS_FB_APP_ACCESS_TOKEN = Access token for ads management

FB_APP_DATABASE_URL = Your Database URL for Postgres

DJANGO_APP_SECRET = Your Django App Secret Key

Check if you have pip

    pip -V

If it outputs version then  proceed to migrations else get pip from [get-pip.py](https://bootstrap.pypa.io/get-pip.py)

Then do if you dont have pip

    python get-pip.py

After setting environment variables

    pip install -r requirments.txt

Then run migrations

    python manage.py migrate

To Run

    python manage.py runserver