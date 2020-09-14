import praw
import tweepy
import time
import json
import random
import datetime
import os
import requests

# Getting them tokens
with open("secrets.json", "r") as f:
    config = json.load(f)

# Cache with all of the submission ids
with open('cache.json', 'r') as f:
    cache = json.load(f)

# Praw and Tweepy auth
reddit = praw.Reddit(client_id=config["Moe-Reddit-Client"],
                     client_secret=config["Moe-Reddit-Secret"],
                     user_agent="Reddit Twitter Bot")
auth = tweepy.OAuthHandler(config["Moe-Twitter-Consumer"], config["Moe-Twitter-Secret"])
auth.set_access_token(key=config["Moe-Twitter-Key"], secret=config["Moe-Twitter-Key-Secret"])
twitter = tweepy.API(auth)


def get_post():
    """Yoinks a random submission from r/awwnime to post on twitter"""
    print("Getting post from reddit")

    try:
        posts = [post for post in reddit.subreddit('Moescape').hot(limit=20)]
        random_post_number = random.randint(0, 20)
        random_post = posts[random_post_number]

        if random_post.id not in cache['post-ids']:
            post_name = random_post.title
            post_comments = random_post.num_comments
            post_likes = random_post.score
            post_link = random_post.shortlink
            post_image = get_image(random_post.url)

            cache['post-ids'].append(f'{random_post.id}')
            with open('cache.json', 'w+') as c:
                json.dump(cache, c, indent=4)
            tweet(post_name, post_comments, post_likes, post_link, post_image)

        else:
            print(f"already posted image {random_post.url}")
            get_post()

    except Exception as error:
        print(f"[EROR] MoeBot has run into an error: [{error}]")
        log = open('logs.txt', 'w')
        log.write(f'[{datetime.datetime.utcnow()}] [{error}] \n'
                  f'END OF ERROR \n')
        log.close()
        time.sleep(7200)

def get_image(url):
    file_name = os.path.basename(url[-18:])
    img_path = f"./pics/{file_name}"
    print(f"MoeBot is Downloading image: {url}")
    resp = requests.get(url, stream=True)

    try:
        with open(img_path, 'wb') as image:
            for chunk in resp:
                image.write(chunk)
        return img_path

    except Exception as error:
        print(f"[EROR] MoeBot has run into an error: [{error}]")
        log = open('logs.txt', 'w')
        log.write(f"[{datetime.datetime.utcnow()}] [{error}] \n"
                  f"END OF ERROR \n")
        log.close()
        time.sleep(7200)


def tweet(post_name, post_comments, post_likes, post_link, post_image):
    """Simply tweets out the submission"""
    print(f"Tweeting out post: {post_link} \n"
          f"with image {post_image}")

    try:
        twitter.update_with_media(post_image, f"{post_name} \n"
                                              f"💬 {post_comments} | ❤ {post_likes} \n \n"
                                              f"🔗 {post_link}")
        for file in os.listdir("./pics"):
            os.remove(file)
    except Exception as error:
        print(f"[EROR] MoeBot has run into an error: [{error}]")
        log = open('logs.txt', 'w')
        log.write(f"[{datetime.datetime.utcnow()}] [{error}] \n"
                  f"END OF ERROR \n")
        log.close()

    time.sleep(7200)


if __name__ == "__main__":
    get_post()
