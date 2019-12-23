import praw
import tweepy
import time
import requests
import os
import urllib.parse
from glob import glob

r_client = "reddit_client"
r_client_secret = "reddit_client_secret"
t_consumer = "twitter_consumer_key"
t_secret = "twitter_consumer_secret"
t_key = "twitter_key"
t_key_secret = "twitter_secret"

# Praw and Tweepy Auth
r = praw.Reddit(client_id=r_client, client_secret=r_client_secret, user_agent="Reddit Bot")
auth = tweepy.OAuthHandler(t_consumer, t_secret)
auth.set_access_token(key=t_key, secret=t_key_secret)
t = tweepy.API(auth)


def tweet_creator():
    print('[bot] getting post from reddit')

    for submission in r.subreddit('awwnime').new(limit=10):
        if not tweeted(submission.id):
            post_name = submission.title
            post_link = submission.permalink
            post_url = get_image(submission.url)
            break
        else:
            print(f"Already tweeted {submission.id}")
    
    log_tweet(submission.id)
    return post_name, post_link, post_url

def tweeted(id):
    found = False
    with open('cache.txt', 'r') as file:
        for line in file:
            if id in line:
                found = True
                break
    return found

def get_image(url):
    file_name = os.path.basename(urllib.parse.urlsplit(url).path)
    img_path = f"./pics/{file_name}"
    print("[bot] Downloading image")
    resp = requests.get(url, stream=True)

    if resp.status_code == 200:
        with open(img_path, 'wb') as image:
            for chunk in resp:
                image.write(chunk)

        return img_path

    else:
        print(f"[bot] Failed to download image. Status code: {resp.status_code}")

def tweet(post_name, post_link, post_url):
    print(f"Tweeting {post_link}")
    try:
        t.update_with_media(post_url, f"{post_name} \n #moe \n https://reddit.com{post_link}")
    except Exception as error:
        print(f"[bot] Error Occured: {error}")
        main()
    
    for file in glob('./pics/*'):
        os.remove(file)

    time.sleep(3600)
    
def log_tweet(id):
    with open('cache.txt', 'a') as file:
        file.write(f"{id}\n")      

def main():
    post_link, post_name, post_url = tweet_creator()
    tweet(post_link, post_name, post_url)

while True:
    main()
