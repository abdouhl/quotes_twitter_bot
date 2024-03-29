
import json
import os
import sys
import random
import tweepy
from dotenv import load_dotenv
from os.path import join, dirname
from supabase import create_client, Client
load_dotenv(join(dirname(__file__), '.env'))


twitter_auth_keys = {
    "consumer_key"        : os.environ.get("QUOTES_TWITER_BOT_CONSUMER_KEY_1"),
    "consumer_secret"     : os.environ.get("QUOTES_TWITER_BOT_CONSUMER_SECRET_1"),
    "access_token"        : os.environ.get("QUOTES_AR_TWITER_BOT_ACCESS_TOKEN"),
    "access_token_secret" : os.environ.get("QUOTES_AR_TWITER_BOT_ACCESS_TOKEN_SECRET")
}

auth = tweepy.OAuthHandler(
        twitter_auth_keys['consumer_key'],
        twitter_auth_keys['consumer_secret']
        )
auth.set_access_token(
        twitter_auth_keys['access_token'],
        twitter_auth_keys['access_token_secret']
        )
api = tweepy.API(auth)




supabase: Client = create_client(os.environ.get("SUPABASE_URL"),os.environ.get("SUPABASE_KEY"))
quote_kkey = random.choice(range(0,1900))
data =supabase.table("quotes").select('*').eq('lang','ar').range(quote_kkey,quote_kkey+1).execute().data
title = data[0]['text']
author_name = data[0]['username']
quote_key = data[0]['key']
auth = author_name.lower()

site_url = "https://www.quotesandsayings.net/ar/quotes/"+author_name

tweet = f'"{title[:120]}"-@{auth}\n\n#{auth} #حكم #معاني #أقوال #أقتباس {site_url}-{quote_key}'
a=api.update_status(status=tweet)
