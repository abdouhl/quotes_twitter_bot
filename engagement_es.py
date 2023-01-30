import tweepy
from os.path import join, dirname
from dotenv import load_dotenv
import os
from deta import Deta
import time
load_dotenv(join(dirname(__file__), '.env'))

deta = Deta(os.environ.get("DETA_KEY"))
done_qt_likes = deta.Base("done_qt_likes")
done_qt_users = deta.Base("done_qt_users")

twitter_auth_keys = {
    "consumer_key"        : os.environ.get("QUOTES_TWITER_BOT_CONSUMER_KEY"),
    "consumer_secret"     : os.environ.get("QUOTES_TWITER_BOT_CONSUMER_SECRET"),
    "access_token"        : os.environ.get("QUOTES_ES_TWITER_BOT_ACCESS_TOKEN"),
    "access_token_secret" : os.environ.get("QUOTES_ES_TWITER_BOT_ACCESS_TOKEN_SECRET")
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

influencers = ["SonCitas","PokeCitas","DalaiLama_Citas"]
done=0

#like tweets
for influencer in influencers:
    for tweet in tweepy.Cursor(api.search_tweets, q=f'to:{influencer}',result_type='recent').items(200):
        p = done_qt_likes.fetch({"value": tweet.id_str,"lang":"es"})
        if p.count != 0:
            continue
        try:
            api.create_favorite(tweet.id_str)
        except:
            continue
        print('tweet',tweet.id_str)
        done_qt_likes.put({"value": tweet.id_str,"lang":"es"})
        done=1
        break
    if done ==1:
        break

time.sleep(300)
#follow users
	
for user in api.get_followers(id ='1572685855',count=200):
    p = done_qt_users.fetch({"value": user.screen_name,"lang":"es"})
    if p.count != 0:
		    continue
    try:
        user.follow()
    except:
		    continue
    print('follow',user.screen_name)
    done_qt_users.put({"value": user.screen_name,"lang":"es"})
    break









