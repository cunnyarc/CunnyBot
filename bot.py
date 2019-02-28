
import tweepy, praw, time, json, urllib.parse, sys, distutils.core, itertools, csv, os
from getmedia import get_media
from imgurpython import ImgurClient

with open('./json/setup.json') as data_file:
    setup = json.load(data_file)

__author__ = "Glitchy_Red"
__version__ = "0.1"
name = "MoeBot"


def get_moe_posts(subreddit_info):
    post_dict = {}
    print("[Bot] Getting Moe from Reddit")
    for submission in subreddit_info.new(limit=10):
        if(submission.over_18):
            print("[Bot] skipping post beacause of NSFW")
            continue
        elif(submission.stickied):
            print("[Bot] skipping post because of stickied")
            continue
        else:
            post_dict[submission.id] = submission
    return post_dict

def get_twitter_caption(submission):
    hastag_string = ''
    twitter_max_title_length = 280 - len(submission.shortlink) - len(hastag_string) - 1
    if len(submission.title) < twitter_max_title_length:
        twitter_caption = submission.title + ' ' + hastag_string + submission.shortlink
    else:
        twitter_caption = submission.title[:twitter_max_title_length] + '... ' + hastag_string + submission.shortlink
    return twitter_caption

def make_post(post_dict):
    for post in post_dict:
        post_id = post_dict[post].id
        media_file = get_media(post_dict[post].url, setup["iClientId"], setup["iClientSecret"])
        if(media_file):
            try:
                caption = get_twitter_caption(post_dict[post])
                if(media_file):
                    print("[Bot] Posting this on Twitter with media attachment", caption)
                    tweet = twitter.update_with_media(filename=media_file, status=caption)
                    try:
                        os.remove(media_file)
                        print("[Bot] Deleting media file at", media_file)
                    except BaseException as e:
                        print("[EROR] Error when trying to delete media file", str(e))
                else:
                    print("[Bot] Posting this on Twitter:", caption)
                    tweet = twitter.update_status(status=caption)
            except BaseException as e:
                print("[EROR] Error while posting tweet:" + str(e))
        else:
            print('[WARN] Twitter: Skipping', post_id, 'because non-media posts are disabled or the media file was not found')
    else:
        ("[Bot] Skipping", post_id, "because it was already posted")



while True:
    try:
        print("[Bot] Conntecting to Reddit")
        auth = tweepy.OAuthHandler(setup["tConsumerKey"], setup["tConsumerSecret"])
        auth.set_access_token(setup["tAccessTokenKey"], setup["tAccessTokenSecret"])
        twitter = tweepy.API(auth)
        twitter_username = twitter.me().screen_name
        r = praw.Reddit(client_id = setup["rClientId"],
                        client_secret = setup["rClientSecret"],
                        user_agent = setup["rUserAgent"])
        subreddit = r.subreddit('awwnime')
        post_dict = get_moe_posts(subreddit)
        make_post(post_dict)
    except BaseException as e:
        print('[EROR] Error in main process:', str(e))
    print('[Bot] Sleeping for 3600 seconds')
    time.sleep(3600)
    print('[Bot] Restarting main process...')
